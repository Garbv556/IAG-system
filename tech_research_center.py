import os
import sys
import time
import random
import json
import asyncio
from datetime import datetime
import websockets

# Configurando path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from core.web_researcher import WebResearcher
    from core.iag_central import IAGCentral
    from agents.__init__ import *
    from agents_pokemon.__init__ import *
except ImportError as e:
    print(f"Erro ao importar modulos: {e}")
    sys.exit(1)

class UnifiedResearchCenter:
    def __init__(self):
        self.researcher = WebResearcher()
        self.animal_team = [
            PolvoAgent("polvo_001"), LeaoAgent("leao_001"), 
            ElefanteAgent("elefante_001"), TigreAgent("tigre_001"), 
            OrcaAgent("orca_001")
        ]
        self.pokemon_team = [
            PyroarAgent("pyroar_001"), IncineroarAgent("incineroar_001"), 
            CopperajahAgent("copperajah_001"), OctilleryAgent("octillery_001"),
            GarchompAgent("garchomp_001")
        ]
        self.active_team = self.animal_team
        self.system_name = "animals"
        self.conhecimento_coletivo = {}
        self.ws_uri = "ws://localhost:8000/ws"

    async def _send_to_ui(self, message_type, payload):
        try:
            async with websockets.connect(self.ws_uri) as websocket:
                data = {"type": message_type, "system": self.system_name, **payload}
                await websocket.send(json.dumps(data))
        except:
            pass

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def header(self):
        self.clear()
        print("="*70)
        print(f"CENTRO DE PESQUISA UNIFICADO - [{self.system_name.upper()}]")
        print("="*70)
        print(f"Matriz Operacional: {self.system_name.upper()}")
        print("-" * 70)

    async def run_research(self, topic):
        self.header()
        print(f"MISSAO: {topic.upper()}")
        print("-" * 70)

        # 1. Web Scan
        print("\n[PASSO 1] Varredura Profunda na Internet...")
        await self._send_to_ui("system", {"message": f"CLI: Iniciando pesquisa sobre {topic}"})
        
        content = self.researcher.learn_from_web(topic)
        if not content:
            print("Erro: Fontes digitais inacessiveis.")
            return

        print(f"Dados Brutos Coletados: {len(content)} bytes.")

        # 2. Collaborative Learning
        print("\n[PASSO 2] Distribuicao de Carga Neural...")
        selected = random.sample(self.active_team, 3)
        
        for agent in selected:
            print(f"   * {agent.animal_name} processando...")
            await asyncio.sleep(0.5)
            prof = agent.learn(topic, content)
            self.conhecimento_coletivo[agent.animal_name] = prof
            
            await self._send_to_ui("learning", {
                "agent_id": agent.agent_id,
                "animal": agent.animal_name,
                "proficiency": prof,
                "message": f"CLI Research: {agent.animal_name} analisando {topic}"
            })

        # 3. Collaborative Debate
        print("\n[PASSO 3] Debate Tecnico Consolidado...")
        best = max(selected, key=lambda a: self.conhecimento_coletivo.get(a.animal_name, 0))
        worst = min(selected, key=lambda a: self.conhecimento_coletivo.get(a.animal_name, 0))

        msg_best = f"Observei padroes de evolucao em {topic}."
        msg_worst = f"Entendido. Base neural adaptada."

        print(f"   {best.animal_name}: {msg_best}")
        print(f"   {worst.animal_name}: {msg_worst}")
        
        await self._send_to_ui("conversation", {
            "from_agent": best.animal_name, "to_agent": worst.animal_name, "message": msg_best, "is_helper": True
        })
        await asyncio.sleep(1)
        await self._send_to_ui("conversation", {
            "from_agent": worst.animal_name, "to_agent": best.animal_name, "message": msg_worst, "is_helper": False
        })

        # 4. Report Generation
        report_file = "report_latest.md"
        with open(report_file, "w") as f:
            f.write(f"# RELATORIO: {topic.upper()}\n\n")
            f.write(f"Data: {datetime.now().isoformat()}\n")
            f.write(f"Setor: {self.system_name}\n")
        print("Relatorio Gerado.")

    async def main_menu(self):
        # Para fins de demo automatica, vamos rodar uma pesquisa direto se houver argumento
        if len(sys.argv) > 1:
            await self.run_research(" ".join(sys.argv[1:]))
            return

        while True:
            self.header()
            print("COMANDOS: pesquisar [tema] | time [escolha] | sair")
            cmd = input("CLI >> ").strip().lower()
            if cmd == "sair": break
            elif cmd.startswith("pesquisar"):
                await self.run_research(cmd.split(" ", 1)[1])

if __name__ == "__main__":
    center = UnifiedResearchCenter()
    asyncio.run(center.main_menu())
