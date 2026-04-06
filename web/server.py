"""
API WebSocket para conectar os agentes animais a um frontend web.
Permite visualizar em tempo real o aprendizado e conversas entre os agentes, com integração Generativa LLM e Extração de PDF.
"""

import asyncio
import json
import base64
import io
from datetime import datetime
from typing import Dict, List, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
import urllib.request
import urllib.error
import random
import google.generativeai as genai

# Tentar importar o PyPDF2 (pode falhar se o pip install não tiver finalizado)
try:
    import PyPDF2
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from core.iag_central import IAGCentral
from agents import (
    LeaoAgent, TigreAgent, ElefanteAgent, HipoAgent, PolvoAgent,
    LoboAgent, TubaraoAgent, OrcaAgent, RinoceronteAgent, FalcaoAgent,
    CrocodiloAgent, CavaloAgent, GorilaAgent, OvelhaAgent, CarneiroAgent,
    CoelhoAgent, AlceAgent, MarlinAgent, UrsoPardoAgent, LeopardoAgent,
    CanguruAgent, BisaoAgent
)

app = FastAPI(title="Sistema de Agentes Animais - IAG com LLM")

app.mount("/static", StaticFiles(directory=current_dir), name="static")

iag: IAGCentral = None
connected_clients: List[WebSocket] = []

def initialize_iag():
    global iag
    iag = IAGCentral()
    agents = [
        LeaoAgent("leao"), TigreAgent("tigre"), ElefanteAgent("elefante"), HipoAgent("hipopotamo"),
        PolvoAgent("polvo"), LoboAgent("lobo"), TubaraoAgent("tubarao"), OrcaAgent("orca"),
        RinoceronteAgent("rinoceronte"), FalcaoAgent("falcao"), CrocodiloAgent("crocodilo"), CavaloAgent("cavalo"),
        GorilaAgent("gorila"), OvelhaAgent("ovelha"), CarneiroAgent("carneiro"), CoelhoAgent("coelho"),
        AlceAgent("alce"), MarlinAgent("marlin"), UrsoPardoAgent("urso_pardo"), LeopardoAgent("leopardo"),
        CanguruAgent("canguru"), BisaoAgent("bisao")
    ]
    for agent in agents:
        iag.register_agent(agent.agent_id, agent)
    return iag

async def broadcast_message(message: dict):
    if not connected_clients: return
    msg_json = json.dumps(message)
    disconnected = []
    for client in connected_clients:
        try:
            await client.send_text(msg_json)
        except:
            disconnected.append(client)
    for client in disconnected:
        connected_clients.remove(client)

async def call_llm(provider: str, api_key: str, prompt: str) -> str:
    """Faz a chamada assíncrona para a API escolhida."""
    if not api_key:
        return ""
        
    if provider == "gemini":
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            response = await asyncio.to_thread(model.generate_content, prompt)
            return response.text.strip().replace('"', '').replace('`', '')
        except Exception as e:
            return f"[ERRO_GEMINI: {str(e)[:100]}]"
            
    elif provider == "openai":
        url = "https://api.openai.com/v1/chat/completions"
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
        data = {"model": "gpt-4o-mini", "messages": [{"role": "user", "content": prompt}]}
        return await _make_rest_call(url, headers, data, provider)
        
    elif provider == "claude":
        url = "https://api.anthropic.com/v1/messages"
        headers = {"x-api-key": api_key, "anthropic-version": "2023-06-01", "content-type": "application/json"}
        data = {"model": "claude-3-haiku-20240307", "max_tokens": 1024, "messages": [{"role": "user", "content": prompt}]}
        return await _make_rest_call(url, headers, data, provider)
        
    elif provider == "grok":
        url = "https://api.x.ai/v1/chat/completions"
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
        data = {"model": "grok-2-latest", "messages": [{"role": "user", "content": prompt}]}
        return await _make_rest_call(url, headers, data, provider)

    return ""

async def _make_rest_call(url, headers, data, provider):
    def sync_req():
        req = urllib.request.Request(url, headers=headers, data=json.dumps(data).encode('utf-8'))
        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                if provider == "claude": return result['content'][0]['text']
                return result['choices'][0]['message']['content']
        except urllib.error.URLError as e:
            err = e.read().decode('utf-8') if hasattr(e, 'read') else str(e)
            return f"[ERRO_{provider.upper()}: {err[:150]}]"
        except Exception as e:
            return f"[ERRO_{provider.upper()}: {str(e)[:150]}]"
            
    res = await asyncio.to_thread(sync_req)
    return res.strip().replace('"', '').replace('`', '')

async def simulate_learning_and_conversation(task_name: str, raw_content: str, api_keys: dict = None):
    text_content = raw_content
    
    await broadcast_message({
        "type": "system",
        "message": f"IAG: Analisando Arquivos Binários e acionando IA Generativa...",
        "timestamp": datetime.now().isoformat()
    })
    
    # 1. Decodificador Inteligente de PDF (Base64) ou Textos
    if raw_content.startswith("data:application/pdf;base64,"):
        if HAS_PYPDF:
            try:
                b64_data = raw_content.split(",")[1]
                pdf_bytes = base64.b64decode(b64_data)
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes), strict=False)
                text_content = ""
                # Lê apenas as primeiras 3 páginas para economizar tokens e tempo do Gemini
                for i in range(min(3, len(pdf_reader.pages))):
                    page_text = pdf_reader.pages[i].extract_text()
                    if page_text:
                        text_content += page_text + "\n"
                        
                if not text_content.strip():
                    text_content = "O PDF parece estar vazio ou não contém texto legível (pode ser uma imagem escaneada)."
                    
                await broadcast_message({
                    "type": "system",
                    "message": f"IAG: PDF Extraído com sucesso. {len(text_content)} caracteres localizados.",
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                text_content = f"Falha ao ler o PDF: {str(e)}"
        else:
            text_content = "Biblioteca PyPDF2 não instalada no servidor."
            
    # Processo Central Padrão
    learning_results = {}
    for agent_id, agent in iag.agents.items():
        proficiency = iag.distribute_learning_task(task_name, text_content[:500])
        agent_proficiency = agent.learn(task_name, text_content[:500])
        learning_results[agent_id] = {
            "proficiency": agent_proficiency,
            "animal": agent.animal_name,
            "context": "group" if agent.adaptation_group > 0.7 else "solo"
        }
        
        await broadcast_message({
            "type": "learning",
            "agent_id": agent_id,
            "animal": agent.animal_name,
            "task": task_name,
            "proficiency": round(agent_proficiency, 3),
            "context": learning_results[agent_id]["context"],
            "message": f"{agent.animal_name}: Lendo e aprendendo ({round(agent_proficiency * 100)}%)",
            "timestamp": datetime.now().isoformat()
        })
        await asyncio.sleep(0.1)

    sorted_agents = sorted(learning_results.items(), key=lambda x: x[1]["proficiency"], reverse=True)
    best_learner = sorted_agents[0]
    worst_learner = sorted_agents[-1]
    
    helper_agent = iag.agents[best_learner[0]]
    learner_agent = iag.agents[worst_learner[0]]
    
    # 2. IA Dinâmica (Papo entre Professor e Aluno)
    helper_msg = ""
    learner_msg = ""
    
    if api_keys is None: api_keys = {}
    active_providers = [k for k, v in api_keys.items() if v]
    
    if active_providers:
        provider_helper = random.choice(active_providers)
        prompt_helper = f"Aja como um {helper_agent.animal_name}. O animal {learner_agent.animal_name} teve dificuldades com o seguinte texto: '{text_content[:800]}'. Como você é o professor animal mais esperto da turma, dê uma explicação direta de no máximo duas frases ensinando a parte principal do texto para o {learner_agent.animal_name} na sua linguagem cheia de analogias do seu animal. [MENTE: {provider_helper.upper()}]"
        helper_msg = await call_llm(provider_helper, api_keys[provider_helper], prompt_helper)
        
        if helper_msg and not helper_msg.startswith("[ERRO"):
            provider_learner = random.choice(active_providers)
            prompt_learner = f"Aja como um {learner_agent.animal_name}. O professor ensinou a matéria com essa frase: '{helper_msg}'. Responda ao professor em apenas uma frase, agradecendo, validando que você entendeu a analogia do conteúdo usando uma analogia selvagem do seu próprio animal. [MENTE: {provider_learner.upper()}]"
            learner_msg = await call_llm(provider_learner, api_keys[provider_learner], prompt_learner)

    # Fallback caso API falhe ou não tenha sido passada
    if not helper_msg or helper_msg.startswith("[ERRO"):
        if helper_msg and helper_msg.startswith("[ERRO"):
            await broadcast_message({
                "type": "system",
                "message": f"❌ Falha na API: {helper_msg}",
                "timestamp": datetime.now().isoformat()
            })
        helper_msg = f"Atenção {learner_agent.animal_name}! Li sobre '{text_content[:60]}...'. Preste bastante atenção nisso na floresta!"
        
    if not learner_msg or learner_msg.startswith("[ERRO"):
        learner_msg = f"Nossa! Muito obrigado pela explicação, minhas engrenagens mentais giraram."

    await broadcast_message({
        "type": "conversation",
        "from_agent": helper_agent.animal_name,
        "to_agent": learner_agent.animal_name,
        "message": helper_msg,
        "is_helper": True,
        "proficiency_diff": 0,
        "timestamp": datetime.now().isoformat()
    })
    
    await asyncio.sleep(2)
    
    improvement = min(0.3, (best_learner[1]["proficiency"] - worst_learner[1]["proficiency"]) * 0.4)
    new_proficiency = min(1.0, worst_learner[1]["proficiency"] + improvement)
    
    await broadcast_message({
        "type": "conversation",
        "from_agent": learner_agent.animal_name,
        "to_agent": helper_agent.animal_name,
        "message": learner_msg,
        "is_helper": False,
        "timestamp": datetime.now().isoformat()
    })
    
    await broadcast_message({
        "type": "learning_update",
        "agent_id": worst_learner[0],
        "animal": learner_agent.animal_name,
        "old_proficiency": round(worst_learner[1]["proficiency"], 3),
        "new_proficiency": round(new_proficiency, 3),
        "improvement": round(improvement, 3),
        "message": f"Proficiência Atualizada após Ensino.",
        "timestamp": datetime.now().isoformat()
    })
    
    await asyncio.sleep(2)
    
    # 3. Restantes dos agentes comentando inteligentemente o material (Geramos 3 e reciclamos para ser mais rapido)
    if active_providers:
        provider_group = random.choice(active_providers)
        prompt_group = f"Faça 5 frases minúsculas de 1 linha de 5 animais diferentes da selva onde eles contam com entusiasmo algo que acharam legal neste artigo: '{text_content[:600]}'. Retorne no formato: JSON List of strings com 5 frases."
        group_lines = await call_llm(provider_group, api_keys[provider_group], prompt_group)
    else:
        group_lines = ""

    snippet = text_content[:40].replace('\n', ' ') if len(text_content) > 10 else "esse texto genérico"
    fallback_phrases = [
        f"Líder aprova a interpretação sobre '{snippet}'",
        f"Meu radar natural já mapeou todo sobre '{snippet}'",
        f"Incrível abordagem de leitura",
        f"Memorizei o contexto de '{snippet}'"
    ]

    for i, (agent_id, agent) in enumerate(iag.agents.items()):
        # Para economizar banda/tempo API, não chamamos Gemini pra todo mundo, só usamos a pool de quotes.
        phrase = fallback_phrases[i % len(fallback_phrases)]
        
        # Ignorar helper e learner para não ficar muito longo
        if agent_id == best_learner[0] or agent_id == worst_learner[0]:
            continue
            
        await broadcast_message({
            "type": "conversation",
            "from_agent": agent.animal_name,
            "to_agent": "all",
            "message": phrase,
            "is_helper": False,
            "language": task_name,
            "proficiency": round(learning_results[agent_id]["proficiency"], 3),
            "timestamp": datetime.now().isoformat()
        })
        await asyncio.sleep(0.5)

@app.on_event("startup")
async def startup_event():
    initialize_iag()

@app.get("/")
async def get_index():
    with open(os.path.join(current_dir, "index.html"), "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    
    agents_state = []
    for agent_id, agent in iag.agents.items():
        agents_state.append({
            "id": agent_id,
            "animal": agent.animal_name,
            "solo_factor": round(agent.adaptation_solo, 2),
            "group_factor": round(agent.adaptation_group, 2),
            "skills": agent.characteristics,
            "knowledge": list(agent.knowledge.keys())
        })
    
    await websocket.send_json({
        "type": "init",
        "agents": agents_state,
        "message": "Conectado ao sistema LLM!"
    })
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("action") == "start_learning":
                task_name = message.get("task", "Novo Material")
                content = message.get("content", "")
                api_keys = message.get("api_keys", {})
                
                asyncio.create_task(simulate_learning_and_conversation(task_name, content, api_keys))
    
    except WebSocketDisconnect:
        connected_clients.remove(websocket)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
