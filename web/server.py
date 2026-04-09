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
import traceback

# Tentar importar bibliotecas externas
try:
    import PyPDF2
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

try:
    from duckduckgo_search import DDGS
    HAS_WEB_SEARCH = True
except ImportError:
    HAS_WEB_SEARCH = False

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
active_simulations: Dict[str, asyncio.Task] = {}

def initialize_iags():
    global iag_animals, iag_pokemons, refinement_animals, refinement_pokemons
    print("[SERVER] Inicializando ecossistemas IAG...")
    # Animais
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
        
    # Pokemons
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
        if client in connected_clients:
            connected_clients.remove(client)

async def call_llm(provider: str, api_key: str, prompt: str) -> str:
    if not api_key: return ""
    if provider == "gemini":
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            response = await asyncio.to_thread(model.generate_content, prompt)
            return response.text.strip().replace('"', '').replace('`', '')
        except Exception as e:
            return f"[ERRO_GEMINI: {str(e)[:100]}]"
    return ""

async def perform_web_research(query: str) -> str:
    """Realiza uma busca no DuckDuckGo para enriquecer o contexto dos agentes."""
    if not HAS_WEB_SEARCH: return ""
    try:
        print(f"[WEB-SEARCH] Consultando rede mundial por: {query}")
        results = []
        with DDGS() as ddgs:
            # Busca livre em toda a rede (Top 5 resultados)
            for r in ddgs.text(query, max_results=5):
                results.append(f"ORIGEM: {r['href']}\nCONTEÚDO: {r['body']}")
        
        return "\n\n--- INFORMAÇÕES DA WEB (TEMPO REAL) ---\n" + "\n---\n".join(results)
    except Exception as e:
        print(f"[WEB-SEARCH ERROR] {e}")
        return f"[Aviso: Falha na conexão externa: {e}]"

async def simulate_learning_and_conversation(task_name: str, raw_content: str, api_keys: dict, iag_instance, system_name: str):
    """Motor Principal da Matrix: Loop Perpétuo de Especialização Suprema"""
    cycle_num = 0
    try:
        while True:
            cycle_num += 1
            print(f"[MATRIX-{system_name.upper()}] Ciclo #{cycle_num} Iniciado: {task_name}")
            text_content = raw_content or "Exploração de novos horizontes teóricos."
            
            await broadcast_message({
                "type": "system", "system": system_name,
                "message": f"🔄 INICIANDO CICLO DE EVOLUÇÃO #{cycle_num}...",
                "cycle": cycle_num, "timestamp": datetime.now().isoformat()
            })

            # FASE 0: Global Research (Evolutiva)
            await broadcast_message({
                "type": "system", "system": system_name,
                "message": "🌐 FASE 0: Escaneando rede global por atualizações técnicas...",
                "timestamp": datetime.now().isoformat()
            })
            
            search_query = task_name if cycle_num == 1 else f"{task_name} advanced details"
            web_content = await perform_web_research(search_query)
            if web_content:
                text_content = f"{text_content}\n\n{web_content}"
                count_res = web_content.count("ORIGEM:")
                await broadcast_message({
                    "type": "system", "system": system_name,
                    "message": f"✅ {count_res} novas fontes de dados incorporadas ao Córtex.",
                    "timestamp": datetime.now().isoformat()
                })

            await broadcast_message({
                "type": "system", "system": system_name,
                "message": "🔰 FASE 1: Sincronizando Extração e Refinamento...",
                "timestamp": datetime.now().isoformat()
            })

        # 1. Extração
        if raw_content.startswith("data:application/pdf;base64,"):
            if HAS_PYPDF:
                try:
                    b64_data = raw_content.split(",")[1]
                    pdf_bytes = base64.b64decode(b64_data)
                    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes), strict=False)
                    text_content = ""
                    for i in range(min(3, len(pdf_reader.pages))):
                        page_text = pdf_reader.pages[i].extract_text()
                        if page_text: text_content += page_text + "\n"
                    await broadcast_message({
                        "type": "system", "system": system_name,
                        "message": f"✅ PDF Extraído com sucesso. {len(text_content)} caracteres localizados.",
                        "timestamp": datetime.now().isoformat()
                    })
                except Exception as e:
                    text_content = f"Falha PDF: {e}"
            else:
                text_content = "PyPDF2 não disponível no servidor."

        # 2. Refinamento e Sincronia
        await broadcast_message({
            "type": "system", "system": system_name,
            "message": "🌀 FASE 2: Sincronizando Frequências Rítmicas dos Agentes...",
            "timestamp": datetime.now().isoformat()
        })
        
        engine = refinement_animals if system_name == 'animals' else refinement_pokemons
        masteries_snapshot = {aid: a.get_proficiency(task_name) for aid, a in iag_instance.agents.items()}
        
        refinement_events = []
        if engine:
            try:
                refinement_events = engine.run_cycle(masteries_snapshot)
            except Exception as e:
                print(f"Refinement error: {e}")

        for ev in refinement_events:
            await broadcast_message({
                "type": "refinement", "system": system_name,
                "message": f"[{ev['reason']}] {ev['log']}",
                "timestamp": datetime.now().isoformat()
            })
            await asyncio.sleep(0.05)
            
        solo_speed = engine.global_params["solo_speed_multiplier"] if engine else 1.0
        group_boost = engine.global_params["group_boost_multiplier"] if engine else 1.0
        
        # 3. Aprendizado Progressivo
        await broadcast_message({
            "type": "system", "system": system_name,
            "message": f"🧠 FASE 3: Processando Cargas Neurais (Iteração #{cycle_num})...",
            "timestamp": datetime.now().isoformat()
        })

        learning_results = {}
        for agent_id, agent in iag_instance.agents.items():
            current_p = agent.knowledge.get(task_name, 0.1)
            gap = 1.0 - current_p
            # Ganho ponderado para maestria final
            base_gain = (agent.learn(task_name, text_content[:500]) or 0.1) * 0.4
            new_p = min(1.0, current_p + (base_gain * gap))
            agent.knowledge[task_name] = new_p
            learning_results[agent_id] = {"proficiency": new_p, "animal": agent.animal_name}
            
            if random.random() > 0.7: # Reduzir spam
                await broadcast_message({
                    "type": "learning", "system": system_name,
                    "agent_id": agent_id, "animal": agent.animal_name, "task": task_name,
                    "proficiency": round(new_p, 3), "timestamp": datetime.now().isoformat()
                })
            await asyncio.sleep(0.05)

        # 4. Diálogo de Peer-Learning
        if not learning_results: return
        sorted_results = sorted(learning_results.items(), key=lambda x: x[1]["proficiency"], reverse=True)
        best_id, worst_id = sorted_results[0][0], sorted_results[-1][0]
        
        helper = iag_instance.agents[best_id]
        learner = iag_instance.agents[worst_id]
        
        await broadcast_message({
            "type": "system", "system": system_name,
            "message": "💬 FASE 4: Acionando IA para Diálogo de Feedback...",
            "timestamp": datetime.now().isoformat()
        })
        
        # Simulação de Diálogo (Fallback Robusto)
        helper_msg = f"🐾 [AVISO] {learner.animal_name}, observe o padrão de '{text_content[:30]}...'! Use seu instinto!"
        learner_msg = f"🐺 Entendido! Vou fortalecer minha defesa e focar nos detalhes."

        # Se houver Gemini
        if api_keys and api_keys.get('gemini'):
            prompt = f"Roleplay: {helper.animal_name} ensinando {learner.animal_name} sobre {task_name}. Curto."
            res = await call_llm('gemini', api_keys['gemini'], prompt)
            if res and not res.startswith("[ERRO"): helper_msg = res

        await broadcast_message({
            "type": "conversation", "system": system_name,
            "from_agent": helper.animal_name, "to_agent": learner.animal_name,
            "message": helper_msg, "is_helper": True, "timestamp": datetime.now().isoformat()
        })
        await asyncio.sleep(1.5)
        await broadcast_message({
            "type": "conversation", "system": system_name,
            "from_agent": learner.animal_name, "to_agent": helper.animal_name,
            "message": learner_msg, "is_helper": False, "timestamp": datetime.now().isoformat()
        })

        await broadcast_message({
            "type": "system", "system": system_name,
            "message": f"⌛ Ciclo #{cycle_num} finalizado. Hibernação de 8s para consolidação...",
            "cycle": cycle_num,
            "timestamp": datetime.now().isoformat()
        })
        await asyncio.sleep(8) 

    except asyncio.CancelledError:
        print(f"[MATRIX-{system_name.upper()}] Sincronia Encerrada pelo Usuário.")
    except Exception as e:
        print(f"[CRITICAL_ERROR] {e}")
        traceback.print_exc()
        await broadcast_message({
            "type": "system", "system": system_name, "message": f"❌ ERRO NA MATRIZ: {str(e)[:50]}"
        })

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
        
        def get_st(inst):
            return [{"id": aid, "animal": a.animal_name, "knowledge": list(a.knowledge.keys())} 
                   for aid, a in inst.agents.items()]

        await websocket.send_json({
            "type": "init", "animals": get_st(iag_animals), "pokemons": get_st(iag_pokemons)
        })
        
        while True:
            data = await websocket.receive_text()
            msg = json.loads(data)
            if msg.get("action") == "start_learning":
                target = msg.get("target_system")
                systems = [target] if target else ["animals", "pokemons"]
                
                for sys_name in systems:
                    # Cancelar ciclo anterior se houver
                    if sys_name in active_simulations:
                        active_simulations[sys_name].cancel()
                    
                    iag = iag_animals if sys_name == "animals" else iag_pokemons
                    task = asyncio.create_task(simulate_learning_and_conversation(
                        msg["task"], msg["content"], msg["api_keys"], iag, sys_name
                    ))
                    active_simulations[sys_name] = task
            
            if msg.get("action") == "stop_learning":
                target = msg.get("target_system")
                systems = [target] if target else ["animals", "pokemons"]
                for sys_name in systems:
                    if sys_name in active_simulations:
                        active_simulations[sys_name].cancel()
                        del active_simulations[sys_name]
                await broadcast_message({"type": "system", "message": "🛑 MATRIX ENCERRADA.", "system": target or "both"})

            if msg.get("action") == "direct_chat":
                asyncio.create_task(handle_direct_chat(msg, websocket))

    except Exception as e:
        print(f"WS Erro: {e}")
    finally:
        if websocket in connected_clients: connected_clients.remove(websocket)

async def handle_direct_chat(msg: dict, websocket: WebSocket):
    """Processa uma entrevista direta com um agente específico."""
    try:
        system_name = msg.get("system")
        agent_id = msg.get("agent_id")
        user_query = msg.get("message")
        api_keys = msg.get("api_keys", {})
        
        iag = iag_animals if system_name == 'animals' else iag_pokemons
        agent = iag.agents.get(agent_id)
        
        if not agent: return
        
        # Preparar contexto da Persona
        characteristics = ", ".join(agent.characteristics)
        tactics = ", ".join(agent.solo_tactics + agent.collective_tactics)
        powers = ", ".join(getattr(agent, 'powers', []))
        knowledge_summary = ", ".join([f"{k} ({round(v*100)}%)" for k, v in agent.knowledge.items()])

        prompt = f"""VOCÊ É UM AGENTE IAG: {agent.animal_name.upper()}.
CARACTERÍSTICAS: {characteristics}
DOUTRINA TÁTICA: {tactics}
PODERES/HABILIDADES: {powers}
SEU CONHECIMENTO ATUAL: {knowledge_summary}

USUÁRIO ESTÁ TE ENTREVISTANDO.
PERGUNTA: "{user_query}"

REGRAS DE RESPOSTA:
1. Responda estritamente como o seu animal/Pokémon (use onomatopeias, estilo de fala, analogias do seu habitat).
2. Se a pergunta for sobre programação, use o que você sabe, mas explique de forma "animalesca".
3. Seja curto e impactante (máximo 3 frases).
4. Se você não souber muito sobre o assunto (proficiência baixa), demonstre curiosidade instintiva ou cautela.
[MODO: ENTREVISTA DIRETA]"""

        response_text = "🐾 *O agente te observa com curiosidade, mas permanece em silêncio...*"
        
        gemini_key = api_keys.get('gemini_key') or api_keys.get('gemini')
        if gemini_key:
            res = await call_llm('gemini', gemini_key, prompt)
            if res and not res.startswith("[ERRO"):
                response_text = res
        else:
             response_text = f"🐾 [{agent.animal_name.upper()}] *Interesse instintivo demonstrado, mas a conexão mental (API) está offline.*"

        await websocket.send_json({
            "type": "agent_response",
            "system": system_name,
            "agent_id": agent_id,
            "animal": agent.animal_name,
            "message": response_text,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        print(f"Erro no Chat Direto: {e}")

if __name__ == "__main__":
    initialize_iags()
    uvicorn.run(app, host="0.0.0.0", port=8000)
