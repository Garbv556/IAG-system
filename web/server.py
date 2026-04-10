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
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
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
from core.web_researcher import WebResearcher
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

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da Matrix e do WebResearcher Turbo v2.0."""
    global web_researcher
    web_researcher = WebResearcher()
    await web_researcher.initialize()
    initialize_iags()
    print("[SERVER] WebResearcher e Ecossistemas Inicializados")
    
    yield  # Matrix em funcionamento
    
    if web_researcher:
        await web_researcher.close()
        print("[SERVER] WebResearcher Desconectado")

app = FastAPI(title="Sistema Duplo - IAG com LLM", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=current_dir), name="static")

iag_animals: IAGCentral = None
iag_pokemons: IAGCentral = None
refinement_animals = None
refinement_pokemons = None
connected_clients: List[WebSocket] = []
active_simulations: Dict[str, asyncio.Task] = {}
web_researcher: WebResearcher = None
systems_active = {"animals": True, "pokemons": True}
POWER_STATES_FILE = os.path.join(parent_dir, "core", "power_states.json")

def load_power_states():
    global systems_active
    if os.path.exists(POWER_STATES_FILE):
        try:
            with open(POWER_STATES_FILE, "r") as f:
                data = json.load(f)
                systems_active = data.get("systems", {"animals": True, "pokemons": True})
                return data.get("agents", {})
        except Exception as e:
            print(f"[SERVER] Erro ao carregar estados: {e}")
    return {}

def save_power_states():
    try:
        agent_states = {}
        for aid, a in iag_animals.agents.items(): agent_states[aid] = getattr(a, 'active', True)
        for aid, a in iag_pokemons.agents.items(): agent_states[aid] = getattr(a, 'active', True)
        
        with open(POWER_STATES_FILE, "w") as f:
            json.dump({"systems": systems_active, "agents": agent_states}, f, indent=4)
    except Exception as e:
        print(f"[SERVER] Erro ao salvar estados: {e}")

def initialize_iags():
    global iag_animals, iag_pokemons, refinement_animals, refinement_pokemons
    print("[SERVER] Inicializando ecossistemas IAG...")
    
    saved_agents = load_power_states()
    
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
        # Aplicar estado salvo
        if agent.agent_id in saved_agents:
            agent.active = saved_agents[agent.agent_id]
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
        # Aplicar estado salvo
        if agent.agent_id in saved_agents:
            agent.active = saved_agents[agent.agent_id]
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
            # Prompt reforçado para Tópicos + Código (Matrix Blue)
            enhanced_prompt = (
                f"{prompt}\n\n"
                "REGRAS DE FORMATAÇÃO ESTRITA:\n"
                "1. Use apenas Tópicos (###) e Bullet Points para explicar.\n"
                "2. Sempre inclua um bloco de código (```language) se o tema for técnico ou segurança.\n"
                "3. Responda de forma concisa e direta, simulando um download de dados mentais."
            )
            response = await asyncio.to_thread(model.generate_content, enhanced_prompt)
            return response.text.strip().replace('"', '').replace('`', '')
        except Exception as e:
            return f"[ERRO_GEMINI: {str(e)[:100]}]"
    return ""

async def perform_web_research(query: str) -> str:
    """Invoca o motor central de pesquisa web (ASSÍNCRONO)."""
    if not web_researcher:
        return "⚠️ Motor de pesquisa offline."
    return await web_researcher.learn_from_web(query)

async def simulate_learning_and_conversation(task_name: str, raw_content: str, api_keys: dict, iag_instance, system_name: str):
    """Motor Principal da Matrix: Loop Perpétuo de Especialização Suprema"""
    cycle_num = 0
    try:
        while True:
            # Check de Sistema Ativo
            if not systems_active.get(system_name, True):
                print(f"[MATRIX-{system_name.upper()}] Pausada/Desligada.")
                break

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
                
            # 3. Aprendizado Progressivo
            await broadcast_message({
                "type": "system", "system": system_name,
                "message": f"🧠 FASE 3: Processando Cargas Neurais (Iteração #{cycle_num})...",
                "timestamp": datetime.now().isoformat()
            })

            learning_results = {}
            for agent_id, agent in iag_instance.agents.items():
                if not getattr(agent, 'active', True): continue 

                current_p = agent.get_proficiency(task_name)
                gap = 1.0 - current_p
                base_gain = (agent.learn(task_name, text_content[:500]) or 0.1) * 0.4
                new_p = min(1.0, current_p + (base_gain * gap))
                agent.knowledge[task_name] = new_p
                learning_results[agent_id] = {"proficiency": new_p, "animal": agent.animal_name}
                
                if random.random() > 0.7: 
                    await broadcast_message({
                        "type": "learning", "system": system_name,
                        "agent_id": agent_id, "animal": agent.animal_name, "task": task_name,
                        "proficiency": round(new_p, 3), "timestamp": datetime.now().isoformat()
                    })
                await asyncio.sleep(0.05)

            # 4. Diálogo de Peer-Learning
            active_results = {aid: data for aid, data in learning_results.items() 
                             if getattr(iag_instance.agents[aid], 'active', True)}
            
            if not active_results: 
                await asyncio.sleep(8)
                continue
                
            sorted_results = sorted(active_results.items(), key=lambda x: x[1]["proficiency"], reverse=True)
            best_id, worst_id = sorted_results[0][0], sorted_results[-1][0]
            
            helper = iag_instance.agents[best_id]
            learner = iag_instance.agents[worst_id]
            
            await broadcast_message({
                "type": "system", "system": system_name,
                "message": "💬 FASE 4: Acionando IA para Diálogo de Feedback...",
                "timestamp": datetime.now().isoformat()
            })
            
            helper_msg = f"🐾 [AVISO] {learner.animal_name}, observe o padrão de '{text_content[:30]}...'! Use seu instinto!"
            learner_msg = f"🐺 Entendido! Vou fortalecer minha defesa e focar nos detalhes."

            if api_keys and api_keys.get('gemini_key'):
                prompt = f"Roleplay: {helper.animal_name} ensinando {learner.animal_name} sobre {task_name}. Curto."
                
                # Iniciar Fluxo Visual
                await broadcast_message({"type": "data_flow", "agent_id": best_id, "system": system_name, "active": True})
                
                res = await call_llm('gemini', api_keys['gemini_key'], prompt)
                
                # Parar Fluxo Visual
                await broadcast_message({"type": "data_flow", "agent_id": best_id, "system": system_name, "active": False})
                
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

# O evento startup foi migrado para o lifespan acima

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
            return [{"id": aid, "animal": a.animal_name, "active": getattr(a, 'active', True), "knowledge": list(a.knowledge.keys())} 
                   for aid, a in inst.agents.items()]

        await websocket.send_json({
            "type": "init", 
            "animals": get_st(iag_animals), 
            "pokemons": get_st(iag_pokemons),
            "systems_active": systems_active
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

            if msg.get("action") == "toggle_agent":
                sys_name, aid = msg["system"], msg["agent_id"]
                iag = iag_animals if sys_name == "animals" else iag_pokemons
                if aid in iag.agents:
                    iag.agents[aid].active = not getattr(iag.agents[aid], 'active', True)
                    save_power_states() # Persistir no HD
                    await broadcast_message({
                        "type": "agent_status", "system": sys_name, 
                        "agent_id": aid, "active": iag.agents[aid].active
                    })

            if msg.get("action") == "toggle_system":
                sys_name = msg["system"]
                systems_active[sys_name] = not systems_active.get(sys_name, True)
                save_power_states() # Persistir no HD
                if not systems_active[sys_name] and sys_name in active_simulations:
                    active_simulations[sys_name].cancel()
                await broadcast_message({
                    "type": "system_status", "system": sys_name, "active": systems_active[sys_name]
                })

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
    uvicorn.run(app, host="0.0.0.0", port=8000)
