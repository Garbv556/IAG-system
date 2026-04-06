import asyncio
import json
import random
from datetime import datetime
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from sse_starlette.sse import EventSourceResponse
import os

# Importar os agentes (simulado para o server não quebrar se faltar import específico)
# Em produção, importaríamos de agents.leao, etc. Aqui vamos simular o comportamento baseado na sua lista.

app = FastAPI()

# Configurar pasta estática para servir o HTML/CSS
os.makedirs("static", exist_ok=True)

# Dados dos 24 Agentes (22 originais + Canguru + Bisão)
ANIMALS_DB = [
    {"id": "leao", "name": "Leão", "icon": "🦁", "type": "Líder", "group_factor": 0.95, "solo_factor": 0.60},
    {"id": "tigre", "name": "Tigre", "icon": "🐅", "type": "Solitário", "group_factor": 0.40, "solo_factor": 0.98},
    {"id": "elefante", "name": "Elefante", "icon": "🐘", "type": "Inteligente", "group_factor": 0.92, "solo_factor": 0.85},
    {"id": "hipopotamo", "name": "Hipopótamo", "icon": "🦛", "type": "Agressivo", "group_factor": 0.80, "solo_factor": 0.90},
    {"id": "polvo", "name": "Polvo", "icon": "🐙", "type": "Estratégico", "group_factor": 0.30, "solo_factor": 0.99},
    {"id": "lobo", "name": "Lobo", "icon": "🐺", "type": "Estrategista", "group_factor": 0.95, "solo_factor": 0.50},
    {"id": "tubarao", "name": "Tubarão", "icon": "🦈", "type": "Predador", "group_factor": 0.20, "solo_factor": 0.90},
    {"id": "orca", "name": "Orca", "icon": "🐋", "type": "Mestre Tático", "group_factor": 0.98, "solo_factor": 0.60},
    {"id": "rinoceronte", "name": "Rinoceronte", "icon": "🦏", "type": "Tanque", "group_factor": 0.50, "solo_factor": 0.80},
    {"id": "falcao", "name": "Falcão", "icon": "🦅", "type": "Veloz", "group_factor": 0.40, "solo_factor": 0.99},
    {"id": "crocodilo", "name": "Crocodilo", "icon": "🐊", "type": "Emboscada", "group_factor": 0.30, "solo_factor": 0.88},
    {"id": "cavalo", "name": "Cavalo", "icon": "🐎", "type": "Manada", "group_factor": 0.88, "solo_factor": 0.40},
    {"id": "gorila", "name": "Gorila", "icon": "🦍", "type": "Força", "group_factor": 0.90, "solo_factor": 0.75},
    {"id": "ovelha", "name": "Ovelha", "icon": "🐑", "type": "Rebanho", "group_factor": 0.82, "solo_factor": 0.10},
    {"id": "carneiro", "name": "Carneiro", "icon": "🐏", "type": "Impacto", "group_factor": 0.60, "solo_factor": 0.70},
    {"id": "coelho", "name": "Coelho", "icon": "🐇", "type": "Fuga", "group_factor": 0.70, "solo_factor": 0.88},
    {"id": "alce", "name": "Alce", "icon": "🦌", "type": "Selvagem", "group_factor": 0.40, "solo_factor": 0.82},
    {"id": "marlin", "name": "Marlin", "icon": "🐟", "type": "Velocidade", "group_factor": 0.20, "solo_factor": 0.90},
    {"id": "urso_pardo", "name": "Urso Pardo", "icon": "🐻", "type": "Dominante", "group_factor": 0.30, "solo_factor": 0.95},
    {"id": "leopardo", "name": "Leopardo", "icon": "🐆", "type": "Furtivo", "group_factor": 0.25, "solo_factor": 0.95},
    {"id": "canguru", "name": "Canguru", "icon": "🦘", "type": "Mobilidade", "group_factor": 0.75, "solo_factor": 0.65},
    {"id": "bisao", "name": "Bisão", "icon": "🦬", "type": "Resistência", "group_factor": 0.95, "solo_factor": 0.70},
]

# Estado global da simulação
agents_state = {a["id"]: {"progress": 0, "status": "Aguardando", "knowledge": 0} for a in ANIMALS_DB}
chat_log = []
is_learning = False
current_topic = ""

async def generate_events():
    """Gera eventos SSE para o frontend"""
    while True:
        if is_learning:
            # Simular aprendizado
            for agent in ANIMALS_DB:
                aid = agent["id"]
                # Fator de aprendizado baseado em grupo vs solo (simplificado para demo)
                # Se o progresso está baixo, aprende mais rápido. Se alto, desacelera.
                base_speed = random.uniform(1, 5)
                
                # Lógica de adaptação: Alguns aprendem melhor sozinhos, outros em grupo
                # Para simplificar a demo visual, vamos usar uma média ponderada aleatória
                efficiency = random.uniform(0.5, 1.0) 
                
                increment = base_speed * efficiency
                agents_state[aid]["progress"] = min(100, agents_state[aid]["progress"] + increment)
                
                # Atualizar status
                if agents_state[aid]["progress"] < 30:
                    agents_state[aid]["status"] = "Estudando..."
                elif agents_state[aid]["progress"] < 70:
                    agents_state[aid]["status"] = "Processando..."
                elif agents_state[aid]["progress"] < 99:
                    agents_state[aid]["status"] = "Consolidando..."
                else:
                    agents_state[aid]["status"] = "Domínio Total"
                    agents_state[aid]["knowledge"] = 100

            # Gerar logs de conversa aleatórios quando alguém atinge marcos
            if random.random() < 0.15: # 15% de chance de falar a cada tick
                speaker = random.choice(ANIMALS_DB)
                sid = speaker["id"]
                prog = agents_state[sid]["progress"]
                
                msg = ""
                if prog > 90:
                    msgs_help = [
                        f"Eu posso ajudar quem está com dificuldade em {current_topic}!",
                        f"A sintaxe de {current_topic} é clara para mim agora.",
                        f"Quem precisa de revisão? Eu domino isso.",
                        f"{speaker['icon']} {speaker['name']}: A lógica de {current_topic} segue um padrão hierárquico interessante."
                    ]
                    msg = random.choice(msgs_help)
                elif prog > 50:
                    msgs_mid = [
                        f"Estou começando a entender {current_topic}...",
                        f"Ainda tenho dúvidas, mas estou evoluindo.",
                        f"{speaker['icon']} {speaker['name']}: Interessante como {current_topic} se conecta com minha natureza."
                    ]
                    msg = random.choice(msgs_mid)
                else:
                    msgs_low = [
                        f"Isso é difícil... preciso focar.",
                        f"Adaptando meus neurônios para {current_topic}.",
                        f"{speaker['icon']} {speaker['name']}: *observa atentamente*"
                    ]
                    msg = random.choice(msgs_low)
                
                if msg:
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    chat_entry = {"time": timestamp, "agent": speaker["name"], "icon": speaker["icon"], "text": msg, "color": "blue" if prog > 80 else "gray"}
                    chat_log.insert(0, chat_entry)
                    if len(chat_log) > 50: chat_log.pop()

        # Enviar estado atualizado
        data = {
            "agents": agents_state,
            "chat": chat_log[:10], # Últimas 10 mensagens
            "topic": current_topic,
            "active": is_learning
        }
        
        yield {
            "event": "update",
            "data": json.dumps(data)
        }
        
        await asyncio.sleep(1) # Atualiza a cada 1 segundo

@app.get("/")
async def root():
    return FileResponse('static/index.html')

@app.get("/stream")
async def stream():
    return EventSourceResponse(generate_events())

@app.post("/start/{topic}")
async def start_learning(topic: str):
    global is_learning, current_topic, agents_state, chat_log
    if not is_learning:
        is_learning = True
        current_topic = topic
        # Resetar progresso se quiser reiniciar, ou continuar de onde parou
        # agents_state = {a["id"]: {"progress": 0, "status": "Iniciando", "knowledge": 0} for a in ANIMALS_DB}
        chat_log.insert(0, {
            "time": datetime.now().strftime("%H:%M:%S"),
            "agent": "IAG Central",
            "icon": "🤖",
            "text": f"Iniciando protocolo de aprendizado distribuído: {topic}. Todos os agentes conectados.",
            "color": "green"
        })
        return {"status": "started", "topic": topic}
    return {"status": "already_running"}

@app.post("/stop")
async def stop_learning():
    global is_learning, current_topic
    is_learning = False
    chat_log.insert(0, {
        "time": datetime.now().strftime("%H:%M:%S"),
        "agent": "IAG Central",
        "icon": "🤖",
        "text": "Protocolo de aprendizado pausado. Analisando resultados...",
        "color": "red"
    })
    return {"status": "stopped"}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Servidor Iniciado! Acesse http://localhost:8001")
    uvicorn.run(app, host="0.0.0.0", port=8001)