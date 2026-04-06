"""
API WebSocket para conectar os agentes animais a um frontend web.
Permite visualizar em tempo real o aprendizado e conversas entre os agentes.
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn

# Importar sistema de agentes
import sys
sys.path.insert(0, '/workspace')
from agentes_animais.core.iag_central import IAGCentral
from agentes_animais.agents import (
    LeaoAgent, TigreAgent, ElefanteAgent, HipoAgent, PolvoAgent,
    LoboAgent, TubaraoAgent, OrcaAgent, RinoceronteAgent, FalcaoAgent,
    CrocodiloAgent, CavaloAgent, GorilaAgent, OvelhaAgent, CarneiroAgent,
    CoelhoAgent, AlceAgent, MarlinAgent, UrsoPardoAgent, LeopardoAgent,
    CanguruAgent, BisaoAgent
)

app = FastAPI(title="Sistema de Agentes Animais - IAG")

# Servir arquivos estáticos (frontend)
app.mount("/static", StaticFiles(directory="/workspace/agentes_animais/web"), name="static")

# Instância global da IAG
iag: IAGCentral = None
connected_clients: List[WebSocket] = []

def initialize_iag():
    """Inicializa a IAG com todos os 22 agentes"""
    global iag
    iag = IAGCentral()
    
    # Adicionar todos os agentes com seus IDs
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
    """Envia mensagem para todos os clientes conectados"""
    if not connected_clients:
        return
    
    message_json = json.dumps(message)
    disconnected = []
    
    for client in connected_clients:
        try:
            await client.send_text(message_json)
        except:
            disconnected.append(client)
    
    # Remover clientes desconectados
    for client in disconnected:
        connected_clients.remove(client)

async def simulate_learning_and_conversation(task_name: str, content: str):
    """Simula o processo completo de aprendizado e conversa"""
    
    # 1. Distribuir tarefa de aprendizado
    await broadcast_message({
        "type": "system",
        "message": f"IAG: Distribuindo tarefa de aprendizado '{task_name}' para todos os agentes...",
        "timestamp": datetime.now().isoformat()
    })
    
    await asyncio.sleep(1)
    
    # 2. Cada agente aprende individualmente
    learning_results = {}
    for agent_id, agent in iag.agents.items():
        proficiency = iag.distribute_learning_task(task_name, content)
        agent_proficiency = agent.learn(task_name, content)
        learning_results[agent_id] = {
            "proficiency": agent_proficiency,
            "animal": agent.animal_type,
            "context": "group" if agent.group_factor > 0.7 else "solo"
        }
        
        await broadcast_message({
            "type": "learning",
            "agent_id": agent_id,
            "animal": agent.animal_type,
            "task": task_name,
            "proficiency": round(agent_proficiency, 3),
            "context": learning_results[agent_id]["context"],
            "message": f"{agent.animal_type}: Aprendendo {task_name}... (Proficiência: {round(agent_proficiency, 2)})",
            "timestamp": datetime.now().isoformat()
        })
        
        await asyncio.sleep(0.3)  # Pequeno delay para visualização
    
    await asyncio.sleep(1)
    
    # 3. IAG avalia e identifica quem pode ajudar quem
    await broadcast_message({
        "type": "system",
        "message": "IAG: Avaliando proficiências e organizando colaboração...",
        "timestamp": datetime.now().isoformat()
    })
    
    await asyncio.sleep(1)
    
    # Ordenar por proficiência
    sorted_agents = sorted(learning_results.items(), key=lambda x: x[1]["proficiency"], reverse=True)
    best_learner = sorted_agents[0]
    worst_learner = sorted_agents[-1]
    
    await broadcast_message({
        "type": "collaboration_start",
        "helper": best_learner[1]["animal"],
        "learner": worst_learner[1]["animal"],
        "message": f"IAG: {best_learner[1]['animal']} (mais proficiente) vai ajudar {worst_learner[1]['animal']} (menos proficiente)",
        "timestamp": datetime.now().isoformat()
    })
    
    await asyncio.sleep(1)
    
    # 4. Agente mais proficiente ajuda o menos proficiente
    helper_agent = iag.agents[best_learner[0]]
    learner_agent = iag.agents[worst_learner[0]]
    
    await broadcast_message({
        "type": "conversation",
        "from_agent": helper_agent.animal_type,
        "to_agent": learner_agent.animal_type,
        "message": f"{helper_agent.animal_type}: Vou te ajudar com {task_name}. Preste atenção!",
        "proficiency_diff": round(best_learner[1]["proficiency"] - worst_learner[1]["proficiency"], 3),
        "timestamp": datetime.now().isoformat()
    })
    
    await asyncio.sleep(1.5)
    
    # Simular melhoria do agente menos proficiente
    improvement = min(0.3, (best_learner[1]["proficiency"] - worst_learner[1]["proficiency"]) * 0.4)
    new_proficiency = min(1.0, worst_learner[1]["proficiency"] + improvement)
    
    await broadcast_message({
        "type": "learning_update",
        "agent_id": worst_learner[0],
        "animal": learner_agent.animal_type,
        "old_proficiency": round(worst_learner[1]["proficiency"], 3),
        "new_proficiency": round(new_proficiency, 3),
        "improvement": round(improvement, 3),
        "message": f"{learner_agent.animal_type}: Obrigado! Agora entendi melhor {task_name}. Minha proficiência subiu de {round(worst_learner[1]['proficiency'], 2)} para {round(new_proficiency, 2)}",
        "timestamp": datetime.now().isoformat()
    })
    
    await asyncio.sleep(1)
    
    # 5. Conversa geral entre todos os agentes na nova linguagem
    await broadcast_message({
        "type": "system",
        "message": f"IAG: Iniciando conversa geral em {task_name} para validação...",
        "timestamp": datetime.now().isoformat()
    })
    
    await asyncio.sleep(1)
    
    # Cada agente fala algo na nova linguagem
    conversation_phrases = {
        "Leão": f"Em {task_name}: 'Eu sou o líder e domino esta linguagem!'",
        "Tigre": f"Em {task_name}: 'Aprendi sozinho e perfeitamente.'",
        "Elefante": f"Em {task_name}: 'Minha inteligência me permite entender profundamente.'",
        "Hipopótamo": f"Em {task_name}: 'Se alguém errar, vou corrigir agressivamente!'",
        "Polvo": f"Em {task_name}: 'Analisei todas as nuances desta linguagem.'",
        "Lobo": f"Em {task_name}: 'Vamos praticar juntos em grupo.'",
        "Tubarão": f"Em {task_name}: 'Sou eficiente, sem necessidade de ajuda.'",
        "Orca": f"Em {task_name}: 'Nossa estratégia em grupo é imbatível.'",
        "Rinoceronte": f"Em {task_name}: 'Força bruta também funciona para aprender.'",
        "Falcão": f"Em {task_name}: 'Aprendi na velocidade da luz!'",
        "Crocodilo": f"Em {task_name}: 'Esperei o momento certo para absorver tudo.'",
        "Cavalo": f"Em {task_name}: 'Na manada aprendemos mais rápido.'",
        "Gorila": f"Em {task_name}: 'Como líder, garanto que todos aprendam.'",
        "Ovelha": f"Em {task_name}: 'Me sinto seguro aprendendo com o grupo.'",
        "Carneiro": f"Em {task_name}: 'Vou competir para ver quem aprende melhor!'",
        "Coelho": f"Em {task_name}: 'Fico alerta para não cometer erros.'",
        "Alce": f"Em {task_name}: 'Prefiro aprender no meu ritmo.'",
        "Marlin": f"Em {task_name}: 'Nado rapidamente através deste conhecimento.'",
        "Urso Pardo": f"Em {task_name}: 'Minha resistência me ajuda a persistir.'",
        "Leopardo": f"Em {task_name}: 'Aprendi nas sombras, silenciosamente.'",
        "Canguru": f"Em {task_name}: 'Dou saltos de progresso no aprendizado!'",
        "Bisão": f"Em {task_name}: 'Nossa manada é imparável!'"
    }
    
    for agent_id, agent in iag.agents.items():
        phrase = conversation_phrases.get(agent.animal_type, f"Em {task_name}: 'Estou aprendendo!'")
        
        await broadcast_message({
            "type": "conversation",
            "from_agent": agent.animal_type,
            "to_agent": "all",
            "message": phrase,
            "language": task_name,
            "proficiency": round(learning_results[agent_id]["proficiency"], 3),
            "timestamp": datetime.now().isoformat()
        })
        
        await asyncio.sleep(0.5)
    
    await asyncio.sleep(1)
    
    # 6. Resumo final
    await broadcast_message({
        "type": "summary",
        "task": task_name,
        "total_agents": len(iag.agents),
        "average_proficiency": round(sum(r["proficiency"] for r in learning_results.values()) / len(learning_results), 3),
        "best_learner": best_learner[1]["animal"],
        "best_proficiency": round(best_learner[1]["proficiency"], 3),
        "most_improved": worst_learner[1]["animal"],
        "improvement": round(improvement, 3),
        "message": f"✅ Sessão de {task_name} concluída! Média de proficiência: {round(sum(r['proficiency'] for r in learning_results.values()) / len(learning_results), 2)}. Todos os agentes agora podem conversar nesta linguagem!",
        "timestamp": datetime.now().isoformat()
    })

@app.on_event("startup")
async def startup_event():
    """Inicializa a IAG quando o servidor inicia"""
    initialize_iag()
    print(f"✅ IAG inicializada com {len(iag.agents)} agentes animais")

@app.get("/")
async def get_index():
    """Serve a página HTML principal"""
    with open("/workspace/agentes_animais/web/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Endpoint WebSocket para comunicação em tempo real"""
    await websocket.accept()
    connected_clients.append(websocket)
    
    # Enviar estado atual dos agentes
    agents_state = []
    for agent_id, agent in iag.agents.items():
        agents_state.append({
            "id": agent_id,
            "animal": agent.animal_type,
            "solo_factor": round(agent.solo_factor, 2),
            "group_factor": round(agent.group_factor, 2),
            "skills": agent.skills,
            "knowledge": list(agent.knowledge.keys())
        })
    
    await websocket.send_json({
        "type": "init",
        "agents": agents_state,
        "message": "Conectado ao sistema de agentes animais!"
    })
    
    try:
        while True:
            # Receber mensagens do cliente (comandos)
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("action") == "start_learning":
                task_name = message.get("task", "mandarim")
                content = message.get("content", "Conteúdo básico de " + task_name)
                
                # Iniciar simulação em background
                asyncio.create_task(simulate_learning_and_conversation(task_name, content))
                
            elif message.get("action") == "get_status":
                await websocket.send_json({
                    "type": "status",
                    "agents_count": len(iag.agents),
                    "connected_clients": len(connected_clients),
                    "message": "Sistema operacional"
                })
    
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        await broadcast_message({
            "type": "system",
            "message": "Um cliente desconectou",
            "timestamp": datetime.now().isoformat()
        })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
