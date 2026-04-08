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
from core.refinement import RefinementEngine
from agents import (
    LeaoAgent, TigreAgent, ElefanteAgent, HipoAgent, PolvoAgent,
    LoboAgent, TubaraoAgent, OrcaAgent, RinoceronteAgent, FalcaoAgent,
    CrocodiloAgent, CavaloAgent, GorilaAgent, OvelhaAgent, CarneiroAgent,
    CoelhoAgent, AlceAgent, MarlinAgent, UrsoPardoAgent, LeopardoAgent,
    CanguruAgent, BisaoAgent
)
from agents_pokemon import (
    PyroarAgent, IncineroarAgent, CopperajahAgent, HippowdonAgent, OctilleryAgent,
    LycanrocAgent, GarchompAgent, KyogreAgent, RhyperiorAgent, TalonflameAgent,
    FeraligatrAgent, RapidashAgent, RillaboomAgent, WoolooAgent, DubwoolAgent,
    CinderaceAgent, StantlerAgent, BarraskewdaAgent, UrsaringAgent, LiepardAgent,
    KangaskhanAgent, BouffalantAgent
)

app = FastAPI(title="Sistema Duplo - IAG com LLM")
app.mount("/static", StaticFiles(directory=current_dir), name="static")

iag_animals: IAGCentral = None
iag_pokemons: IAGCentral = None
refinement_animals = None
refinement_pokemons = None
connected_clients: List[WebSocket] = []

def initialize_iags():
    global iag_animals, iag_pokemons, refinement_animals, refinement_pokemons
    iag_animals = IAGCentral()
    refinement_animals = RefinementEngine('animals')
    agents_anim = [
        LeaoAgent("leao"), TigreAgent("tigre"), ElefanteAgent("elefante"), HipoAgent("hipopotamo"),
        PolvoAgent("polvo"), LoboAgent("lobo"), TubaraoAgent("tubarao"), OrcaAgent("orca"),
        RinoceronteAgent("rinoceronte"), FalcaoAgent("falcao"), CrocodiloAgent("crocodilo"), CavaloAgent("cavalo"),
        GorilaAgent("gorila"), OvelhaAgent("ovelha"), CarneiroAgent("carneiro"), CoelhoAgent("coelho"),
        AlceAgent("alce"), MarlinAgent("marlin"), UrsoPardoAgent("urso_pardo"), LeopardoAgent("leopardo"),
        CanguruAgent("canguru"), BisaoAgent("bisao")
    ]
    for agent in agents_anim:
        iag_animals.register_agent(agent.agent_id, agent)
        
    iag_pokemons = IAGCentral()
    refinement_pokemons = RefinementEngine('pokemons')
    agents_poke = [
        PyroarAgent("pyroar"), IncineroarAgent("incineroar"), CopperajahAgent("copperajah"), HippowdonAgent("hippowdon"),
        OctilleryAgent("octillery"), LycanrocAgent("lycanroc"), GarchompAgent("garchomp"), KyogreAgent("kyogre"),
        RhyperiorAgent("rhyperior"), TalonflameAgent("talonflame"), FeraligatrAgent("feraligatr"), RapidashAgent("rapidash"),
        RillaboomAgent("rillaboom"), WoolooAgent("wooloo"), DubwoolAgent("dubwool"), CinderaceAgent("cinderace"),
        StantlerAgent("stantler"), BarraskewdaAgent("barraskewda"), UrsaringAgent("ursaring"), LiepardAgent("liepard"),
        KangaskhanAgent("kangaskhan"), BouffalantAgent("bouffalant")
    ]
    for agent in agents_poke:
        iag_pokemons.register_agent(agent.agent_id, agent)

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

async def simulate_learning_and_conversation(task_name: str, raw_content: str, api_keys: dict, iag_instance, system_name: str):
    text_content = raw_content
    
    await broadcast_message({
        "type": "system",
            "system": system_name,
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
            "system": system_name,
                    "message": f"IAG: PDF Extraído com sucesso. {len(text_content)} caracteres localizados.",
                    "timestamp": datetime.now().isoformat()
                })
            except Exception as e:
                text_content = f"Falha ao ler o PDF: {str(e)}"
        else:
            text_content = "Biblioteca PyPDF2 não instalada no servidor."
            
    # Processo Central Padrão + Inteligência Rítmica
    engine = refinement_animals if system_name == 'animals' else refinement_pokemons
    
    # 1.1 Snapshot de proficiência atual para detectar gargalos
    masteries_snapshot = {aid: a.get_proficiency(task_name) for aid, a in iag_instance.agents.items()}
    refinement_events = engine.run_cycle(masteries_snapshot)
    
    # 1.2 Broadcast dos logs de refinamento para o UI (Painéis de Chat)
    for ev in refinement_events:
        await broadcast_message({
            "type": "refinement",
            "system": system_name,
            "message": f"[{ev['reason']}] {ev['log']}",
            "timestamp": datetime.now().isoformat()
        })
        await asyncio.sleep(0.1)
        
    solo_speed = engine.global_params["solo_speed_multiplier"]
    group_boost = engine.global_params["group_boost_multiplier"]
    
    learning_results = {}
    for agent_id, agent in iag_instance.agents.items():
        base_proficiency = iag_instance.distribute_learning_task(task_name, text_content[:500])
        
        is_group_learning = agent.adaptation_group > 0.7
        rhythm_multiplier = group_boost if is_group_learning else solo_speed
        
        raw_agent_proficiency = agent.learn(task_name, text_content[:500])
        agent_proficiency = min(1.0, raw_agent_proficiency * rhythm_multiplier)
        
        # Override do conhecimento no agente com o multiplicador rítmico aplicado
        agent.knowledge_base[task_name] = agent_proficiency
        
        learning_results[agent_id] = {
            "proficiency": agent_proficiency,
            "animal": agent.animal_name,
            "context": "group" if is_group_learning else "solo"
        }
        
        await broadcast_message({
            "type": "learning",
            "system": system_name,
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
    
    helper_agent = iag_instance.agents[best_learner[0]]
    learner_agent = iag_instance.agents[worst_learner[0]]
    
    # 2. IA Dinâmica (Papo entre Professor e Aluno)
    helper_msg = ""
    learner_msg = ""
    
    if api_keys is None: api_keys = {}
    active_providers = [k for k, v in api_keys.items() if v]
    
    if active_providers:
        provider_helper = random.choice(active_providers)
        tactics_helper = " | ".join(helper_agent.collective_tactics)
        powers_helper_str = ""
        if hasattr(helper_agent, "powers") and helper_agent.powers:
            powers_helper_str = f"SEUS PODERES ESPECIAIS (USE-OS NA ANALOGIA): {', '.join(helper_agent.powers)}"
            
        prompt_helper = f"""INSTRUÇÕES DE ROLEPLAY EXTREMO:
Você é um(a) {helper_agent.animal_name}.
SUAS TÁTICAS COLETIVAS (SIGA À RISCA E DEMONSTRE EM SUA FALA): {tactics_helper}
{powers_helper_str}

O aprendiz {learner_agent.animal_name} teve dificuldades com este texto: '{text_content[:600]}'
Como o animal experiente, ensine isso a ele em até 3 frases. 
OBRIGATÓRIO: Fale estritamente como o seu animal (use onomatopeias, trejeitos) e FORCE as suas Táticas Coletivas na própria forma de explicar! [MENTE: {provider_helper.upper()}]"""
        helper_msg = await call_llm(provider_helper, api_keys[provider_helper], prompt_helper)
        
        if helper_msg and not helper_msg.startswith("[ERRO"):
            provider_learner = random.choice(active_providers)
            tactics_learner = " | ".join(learner_agent.solo_tactics)
            powers_learner_str = ""
            if hasattr(learner_agent, "powers") and learner_agent.powers:
                powers_learner_str = f"SEUS PODERES ESPECIAIS (USE-OS NA RESPOSTA): {', '.join(learner_agent.powers)}"
                
            prompt_learner = f"""INSTRUÇÕES DE ROLEPLAY EXTREMO:
Você é um(a) {learner_agent.animal_name}.
SEUS INSTINTOS TÁTICOS (OBEÇA-OS CEGAMENTE): {tactics_learner}
{powers_learner_str}

O professor {helper_agent.animal_name} te ensinou isto: '{helper_msg}'
Responda a ele em 1 ou 2 frases.
OBRIGATÓRIO: Demonstre como VOCÊ absorveu o conteúdo USANDO SEUS INSTINTOS TÁTICOS (ex: se é furtivo, escondeu a lição. Se agressivo, atacou a dúvida). Haja exatamente como seu animal! [MENTE: {provider_learner.upper()}]"""
            learner_msg = await call_llm(provider_learner, api_keys[provider_learner], prompt_learner)

    # Fallback caso API falhe ou não tenha sido passada
    if not helper_msg or helper_msg.startswith("[ERRO"):
        if helper_msg and helper_msg.startswith("[ERRO"):
            await broadcast_message({
                "type": "system",
            "system": system_name,
                "message": f"❌ Falha na API: {helper_msg}",
                "timestamp": datetime.now().isoformat()
            })
        if system_name == 'pokemons':
            pow_str = helper_agent.powers[0] if hasattr(helper_agent, 'powers') and helper_agent.powers else 'energia mística'
            helper_msg = f"🔥 [CANALIZANDO {pow_str.upper()}] Ouça com atenção {learner_agent.animal_name}! O conceito de '{text_content[:40]}...' afeta nossa arena! Prepare-se!"
        else:
            helper_msg = f"🐾 [ROSNADO DE AVISO] Fique atento {learner_agent.animal_name}! Farejei algo sobre '{text_content[:40]}...'. Fique na espreita!"
        
    if not learner_msg or learner_msg.startswith("[ERRO"):
        if system_name == 'pokemons':
            pow_str = learner_agent.powers[0] if hasattr(learner_agent, 'powers') and learner_agent.powers else 'força interior'
            learner_msg = f"⚡ Entendido! Minha {pow_str} ressoa com esse ensinamento. Vou adaptar minha postura de batalha!"
        else:
            learner_msg = f"🐺 [UIVO DE COMPREENSÃO] Captei o sinal. Minhas garras e instintos estão mais afiados agora."

    await broadcast_message({
        "type": "conversation",
            "system": system_name,
        "from_agent": helper_agent.animal_name,
        "to_agent": learner_agent.animal_name,
        "message": helper_msg,
        "is_helper": True,
        "proficiency_diff": 0,
        "timestamp": datetime.now().isoformat()
    })
    
    await asyncio.sleep(2)
    
    # Integração Convergência Rítmica ao Peer Teaching
    gap = best_learner[1]["proficiency"] - worst_learner[1]["proficiency"]
    convergence = engine.global_params["convergence_bonus"]
    improvement = min(0.5, (gap * 0.4) + convergence)
    new_proficiency = min(1.0, worst_learner[1]["proficiency"] + improvement)
    
    await broadcast_message({
        "type": "conversation",
            "system": system_name,
        "from_agent": learner_agent.animal_name,
        "to_agent": helper_agent.animal_name,
        "message": learner_msg,
        "is_helper": False,
        "timestamp": datetime.now().isoformat()
    })
    
    await broadcast_message({
        "type": "learning_update",
            "system": system_name,
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
        prompt_group = f"""ATUE COMO 5 ANIMAIS SELVAGENS DIFERENTES JUNTOS EM BANDO.
Você acabou de ver este texto brilhando na floresta: '{text_content[:400]}'
REGRA GLOBAL: Nenhum animal julga o outro. Protejam e compensem as fraquezas uns dos outros.
Cada animal deve dizer 1 fala bem curta mostrando entusiasmo com o texto baseado no SEU instinto animal. Use emojis!
Formato OBRIGATÓRIO e EXCLUSIVO: Retorne APENAS um JSON array de 5 strings. Ex: ["🐅 Tigre: *rugido* A espreita, vejo...", "🦅 Falcão: *grito* Do alto, enxergo a luz clara da ideia..."]"""
        group_lines = await call_llm(provider_group, api_keys[provider_group], prompt_group)
    else:
        group_lines = ""

    snippet = text_content[:40].replace('\n', ' ') if len(text_content) > 10 else "esse texto genérico"

    for i, (agent_id, agent) in enumerate(iag_instance.agents.items()):
        # Para economizar banda/tempo API, não chamamos Gemini pra todo mundo, só usamos a pool de quotes.
        if system_name == 'pokemons':
            pow_str = agent.powers[0] if hasattr(agent, 'powers') and agent.powers else 'magia'
            phrase = f"✨ Meu instinto focado em {pow_str} me permite ver a teoria '{snippet}' com total clareza na arena!"
        else:
            tactic_str = agent.solo_tactics[0] if hasattr(agent, 'solo_tactics') and agent.solo_tactics else 'sobrevivência'
            phrase = f"🍃 Baseado na minha tática de {tactic_str}, já assimilei a ideia de '{snippet}'."
        
        # Ignorar helper e learner para não ficar muito longo
        if agent_id == best_learner[0] or agent_id == worst_learner[0]:
            continue
            
        await broadcast_message({
            "type": "conversation",
            "system": system_name,
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
    initialize_iags()

@app.get("/")
async def get_index():
    with open(os.path.join(current_dir, "index.html"), "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await websocket.accept()
        connected_clients.append(websocket)
        
        def extract_state(iag_inst):
            st = []
            for agent_id, agent in iag_inst.agents.items():
                st.append({
                    "id": agent_id,
                    "animal": agent.animal_name,
                    "solo_factor": round(agent.adaptation_solo, 2),
                    "group_factor": round(agent.adaptation_group, 2),
                    "skills": agent.characteristics,
                    "knowledge": list(agent.knowledge.keys()),
                    "powers": getattr(agent, "powers", [])
                })
            return st
        
        await websocket.send_json({
            "type": "init",
            "animals": extract_state(iag_animals),
            "pokemons": extract_state(iag_pokemons),
            "message": "Conectado ao MULTI-SISTEMA IAG Duplo!"
        })
        
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("action") == "start_learning":
                task_name = message.get("task", "Novo Material")
                content = message.get("content", "")
                api_keys = message.get("api_keys", {})
                target = message.get("target_system") # animals, pokemons ou null
                
                # Disparo condicional
                if target == "animals" or target is None:
                    asyncio.create_task(simulate_learning_and_conversation(task_name, content, api_keys, iag_animals, "animals"))
                
                if target == "pokemons" or target is None:
                    asyncio.create_task(simulate_learning_and_conversation(task_name, content, api_keys, iag_pokemons, "pokemons"))
            elif "type" in message:
                await broadcast_message(message)
    
    except (WebSocketDisconnect, RuntimeError):
        if websocket in connected_clients:
            connected_clients.remove(websocket)
    except Exception as e:
        print(f"Erro WS: {e}")
        if websocket in connected_clients:
            connected_clients.remove(websocket)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
