"""
IAG - Inteligência Artificial Central
Conecta todos os agentes/animais e coordena o aprendizado coletivo
"""

from typing import Dict, List, Any
from datetime import datetime


class IAGCentral:
    """
    Inteligência Artificial Central que conecta todos os agentes animais.
    Responsável por:
    - Coordenar comunicação entre agentes
    - Gerenciar aprendizado coletivo
    - Facilitar colaboração entre agentes
    """
    
    def __init__(self):
        self.agents: Dict[str, Any] = {}
        self.knowledge_base: Dict[str, Any] = {}
        self.communication_log: List[Dict] = []
        self.created_at = datetime.now()
    
    def register_agent(self, agent_id: str, agent: Any) -> None:
        """Registra um agente no sistema central"""
        self.agents[agent_id] = agent
        print(f"[IAG] Agente {agent_id} ({agent.animal_name}) registrado com sucesso!")
    
    def unregister_agent(self, agent_id: str) -> None:
        """Remove um agente do sistema"""
        if agent_id in self.agents:
            del self.agents[agent_id]
            print(f"[IAG] Agente {agent_id} removido.")
    
    def broadcast_message(self, message: str, sender_id: str = None) -> None:
        """Envia mensagem para todos os agentes conectados"""
        for agent_id, agent in self.agents.items():
            if agent_id != sender_id:
                agent.receive_message(message, sender_id)
        
        self.communication_log.append({
            'timestamp': datetime.now(),
            'type': 'broadcast',
            'sender': sender_id,
            'message': message
        })
    
    def send_direct_message(self, target_id: str, message: str, sender_id: str, auto_reply: bool = True) -> None:
        """Envia mensagem direta de um agente para outro"""
        if target_id in self.agents:
            self.agents[target_id].receive_message(message, sender_id, auto_reply=auto_reply)
            self.communication_log.append({
                'timestamp': datetime.now(),
                'type': 'direct',
                'sender': sender_id,
                'target': target_id,
                'message': message
            })
    
    def distribute_learning_task(self, topic: str, content: Any) -> None:
        """Distribui tarefa de aprendizado para todos os agentes"""
        print(f"\n[IAG] Distribuindo tarefa de aprendizado: {topic}")
        for agent_id, agent in self.agents.items():
            agent.learn(topic, content)
    
    def facilitate_collaboration(self, topic: str) -> None:
        """
        Facilita colaboração entre agentes após aprendizado.
        Agentes mais adaptados ajudam os menos adaptados.
        """
        print(f"\n[IAG] Iniciando sessão de colaboração sobre: {topic}")
        
        # Avalia proficiência de cada agente
        proficiency_scores = {}
        for agent_id, agent in self.agents.items():
            score = agent.get_proficiency(topic)
            proficiency_scores[agent_id] = score
            print(f"  - {agent.animal_name}: Proficiência = {score:.2f}")
        
        # Ordena por proficiência
        sorted_agents = sorted(proficiency_scores.items(), key=lambda x: x[1], reverse=True)
        
        if len(sorted_agents) < 2:
            return
        
        # Agente mais proficiente ajuda os menos proficientes
        top_agent_id, top_score = sorted_agents[0]
        bottom_agent_id, bottom_score = sorted_agents[-1]
        
        if top_score > bottom_score:
            top_agent = self.agents[top_agent_id]
            bottom_agent = self.agents[bottom_agent_id]
            
            help_message = f"Vou te ajudar a melhorar em {topic}. Minha experiência: {top_score:.2f}"
            self.send_direct_message(bottom_agent_id, help_message, top_agent_id)
            
            print(f"\n[IAG] {top_agent.animal_name} está ajudando {bottom_agent.animal_name}")
    
    def get_all_agents_status(self) -> Dict[str, Dict]:
        """Retorna status de todos os agentes"""
        status = {}
        for agent_id, agent in self.agents.items():
            status[agent_id] = {
                'animal': agent.animal_name,
                'state': agent.state,
                'knowledge': list(agent.knowledge.keys())
            }
        return status
    
    def __str__(self) -> str:
        return f"IAG Central com {len(self.agents)} agentes conectados"
