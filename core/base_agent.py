"""
Classe Base para Agentes Animais
Todos os agentes herdam desta classe e implementam suas características específicas
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum


class State(Enum):
    """Estados possíveis do agente"""
    SOLO = "solo"
    GROUP = "group"
    LEARNING = "learning"
    COMMUNICATING = "communicating"
    HUNTING = "hunting"
    RESTING = "resting"


class AnimalAgent(ABC):
    """
    Classe base para todos os agentes animais.
    Cada agente tem:
    - Características únicas do animal
    - Conhecimento básico de linguagens de programação
    - Capacidade de aprender individualmente e em grupo
    - Consciência de adaptação sozinho vs em grupo
    """
    
    def __init__(self, agent_id: str, iag_central=None):
        self.agent_id = agent_id
        self.animal_name = self.__class__.__name__
        self.iag_central = iag_central
        self.state = State.SOLO
        self.knowledge: Dict[str, float] = {}  # topic -> proficiency (0-1)
        self.messages_received: List[Dict] = []
        self.active = True
        self.learning_history: List[Dict] = []
        
        # Conhecimento básico de programação (todos sabem o básico)
        self.programming_languages = {
            'python': 0.5,
            'javascript': 0.5,
            'java': 0.5,
            'cpp': 0.5,
            'go': 0.5,
            'rust': 0.5
        }
        self.knowledge.update(self.programming_languages)
        
        # Características específicas do animal (sobrescritas pelas subclasses)
        self.species = ""
        self.environment = ""
        self.characteristics: List[str] = []
        self.powers: List[str] = []              # ⚡ Poderes Especiais (Usado primariamente por Pokémon)
        self.solo_behavior = ""
        self.group_behavior = ""
        self.attacks: List[str] = []
        self.rival_response = ""
        
        # ═══════════════════════════════════════════════════
        # DOUTRINA TÁTICA — Comportamento Adaptativo por Modo
        # ═══════════════════════════════════════════════════
        self.solo_tactics: List[str] = []       # 🧍 Modo Solo
        self.collective_tactics: List[str] = []  # 🤝 Modo Coletivo
        self.threat_tactics: List[str] = []      # ⚠️ Reação a Ameaça
        
        # Fatores de adaptação
        self.adaptation_solo = 0.5  # Quão bem se adapta sozinho
        self.adaptation_group = 0.5  # Quão bem se adapta em grupo
        self.intelligence = 0.5  # Capacidade de aprendizado
        self.aggressiveness = 0.5  # Tendência agressiva
        self.stealth = 0.5  # Furtividade
        self.strength = 0.5  # Força
        self.speed = 0.5  # Velocidade
        
        self._set_animal_characteristics()
    
    @abstractmethod
    def _set_animal_characteristics(self) -> None:
        """
        Método abstrato que cada subclasse deve implementar
        para definir as características específicas do animal
        """
        pass
    
    def learn(self, topic: str, content: Any) -> float:
        """
        Agente aprende um novo tópico.
        Retorna a proficiência alcançada.
        Considera inteligência do animal e estado (solo/grupo).
        """
        old_state = self.state
        self.state = State.LEARNING
        
        # Fator de aprendizado baseado na inteligência e estado
        learning_factor = self.intelligence
        
        # Se estiver em grupo, pode aprender melhor (para animais sociais)
        if old_state == State.GROUP:
            learning_factor *= (1 + self.adaptation_group * 0.3)
        else:
            learning_factor *= (1 + self.adaptation_solo * 0.3)
        
        # Simula aprendizado (na prática, seria mais complexo)
        improvement = learning_factor * 0.3  # Ganho por sessão de aprendizado
        
        if topic in self.knowledge:
            self.knowledge[topic] = min(1.0, self.knowledge[topic] + improvement)
        else:
            self.knowledge[topic] = improvement
        
        self.learning_history.append({
            'timestamp': datetime.now(),
            'topic': topic,
            'proficiency': self.knowledge[topic],
            'state': old_state.value
        })
        
        self.state = old_state
        
        print(f"  [{self.animal_name}] Aprendeu {topic}: proficiência = {self.knowledge[topic]:.2f}")
        return self.knowledge[topic]
    
    def get_proficiency(self, topic: str) -> float:
        """Retorna proficiência em um tópico específico"""
        return self.knowledge.get(topic, 0.0)
    
    def receive_message(self, message: str, sender_id: Optional[str], auto_reply: bool = True) -> None:
        """Recebe mensagem de outro agente ou da IAG"""
        self.messages_received.append({
            'timestamp': datetime.now(),
            'sender': sender_id,
            'message': message
        })
        
        old_state = self.state
        self.state = State.COMMUNICATING
        
        # Processa mensagem baseado nas características do animal
        response = self._process_message(message, sender_id)
        
        self.state = old_state
        
        # Evita loop infinito: só envia resposta se auto_reply for True
        if response and self.iag_central and auto_reply:
            # Envia resposta sem gerar nova resposta automática
            self.iag_central.send_direct_message(sender_id, response, self.agent_id, auto_reply=False)
    
    def _process_message(self, message: str, sender_id: Optional[str]) -> Optional[str]:
        """
        Processa mensagem recebida e gera resposta.
        Comportamento varia conforme características do animal.
        """
        # Resposta básica - pode ser sobrescrita
        if sender_id:
            return f"[{self.animal_name}] Recebi sua mensagem: {message[:50]}..."
        return None
    
    def set_state(self, new_state: State) -> None:
        """Muda o estado do agente"""
        old_state = self.state
        self.state = new_state
        
        # Verifica se a transição é adequada para o animal
        if new_state == State.GROUP and self.adaptation_group < 0.3:
            print(f"[{self.animal_name}] Aviso: Não me adapto bem a grupos!")
        elif new_state == State.SOLO and self.adaptation_solo < 0.3:
            print(f"[{self.animal_name}] Aviso: Prefiro estar em grupo!")
    
    def interact_with_agent(self, other_agent: 'AnimalAgent', topic: str = None) -> Dict:
        """
        Interage com outro agente.
        Pode ser para colaboração, competição, ou comunicação.
        """
        interaction_result = {
            'initiator': self.animal_name,
            'target': other_agent.animal_name,
            'type': 'collaboration',
            'outcome': 'neutral'
        }
        
        # Se ambos conhecem o tópico, podem colaborar
        if topic:
            self_proficiency = self.get_proficiency(topic)
            other_proficiency = other_agent.get_proficiency(topic)
            
            if self_proficiency > other_proficiency + 0.2:
                # Este agente é mais proficiente, pode ensinar
                interaction_result['outcome'] = 'teaching'
                print(f"[{self.animal_name}] Ensinando {topic} para {other_agent.animal_name}")
            elif other_proficiency > self_proficiency + 0.2:
                # Outro agente é mais proficiente, pode aprender
                interaction_result['outcome'] = 'learning'
                print(f"[{self.animal_name}] Aprendendo {topic} com {other_agent.animal_name}")
            else:
                # Proficiências similares, troca de conhecimento
                interaction_result['outcome'] = 'exchange'
                print(f"[{self.animal_name}] Trocando conhecimento sobre {topic} com {other_agent.animal_name}")
        
        return interaction_result
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna status completo do agente"""
        return {
            'agent_id': self.agent_id,
            'animal_name': self.animal_name,
            'species': self.species,
            'environment': self.environment,
            'state': self.state.value,
            'characteristics': self.characteristics,
            'solo_behavior': self.solo_behavior,
            'group_behavior': self.group_behavior,
            'adaptation_solo': self.adaptation_solo,
            'adaptation_group': self.adaptation_group,
            'intelligence': self.intelligence,
            'knowledge_summary': {k: f"{v:.2f}" for k, v in self.knowledge.items() if v > 0.3},
            'messages_count': len(self.messages_received)
        }
    
    def __str__(self) -> str:
        return f"{self.animal_name} ({self.species}) - Estado: {self.state.value}"
    
    # ═══════════════════════════════════════════════════════════
    # 🔥 INTELIGÊNCIA COLETIVA ADAPTATIVA — REGRAS GLOBAIS
    # ═══════════════════════════════════════════════════════════
    # 👉 Nenhum agente é líder. Nenhum agente é subordinado.
    # Se um falha, todos ajustam.
    # Se um ataca, todos sustentam.
    # Se um recua, todos protegem.
    # ═══════════════════════════════════════════════════════════
    
    def get_active_tactics(self) -> List[str]:
        """Retorna as táticas ativas baseadas no estado atual do agente."""
        if self.state == State.SOLO:
            return self.solo_tactics
        elif self.state == State.GROUP:
            return self.collective_tactics
        elif self.state == State.HUNTING:
            return self.threat_tactics
        return self.solo_tactics
    
    def make_tactical_decision(self, situation: str = "normal") -> Dict[str, Any]:
        """
        Toma uma decisão tática baseada na doutrina do animal e situação atual.
        Situações: 'normal', 'threat', 'opportunity', 'failure', 'support'
        """
        tactics = self.get_active_tactics()
        
        if situation == "threat":
            tactics = self.threat_tactics
        elif situation == "support":
            # REGRA GLOBAL: Se um falha, todos ajustam
            tactics = self.collective_tactics
        
        return {
            "agent": self.animal_name,
            "state": self.state.value,
            "situation": situation,
            "active_tactics": tactics,
            "adaptation_score": self.adaptation_group if self.state == State.GROUP else self.adaptation_solo
        }
    
    def support_ally(self, ally: 'AnimalAgent', topic: str = None) -> str:
        """
        PRINCÍPIO: Se um recua, todos protegem / Se um falha, todos ajustam.
        Compensar fraquezas uns dos outros.
        """
        if topic and self.get_proficiency(topic) > ally.get_proficiency(topic):
            boost = (self.get_proficiency(topic) - ally.get_proficiency(topic)) * 0.15
            ally.knowledge[topic] = min(1.0, ally.get_proficiency(topic) + boost)
            return f"[{self.animal_name}] Apoiando {ally.animal_name} em {topic}: +{boost:.2f}"
        return f"[{self.animal_name}] Compartilhando informação com {ally.animal_name}"
    
    def respond_to_group_threat(self) -> Dict[str, Any]:
        """
        PRINCÍPIO: Se um ataca, todos sustentam.
        Nunca agir contra o grupo.
        """
        return {
            "agent": self.animal_name,
            "response": "sustaining",
            "tactics": self.threat_tactics,
            "strength_committed": self.strength,
            "message": f"[{self.animal_name}] Ativando protocolo de defesa coletiva!"
        }

    def get_doctrine_summary(self) -> Dict[str, Any]:
        """Retorna o resumo completo da doutrina tática do agente."""
        return {
            "agent": self.animal_name,
            "species": self.species,
            "solo_tactics": self.solo_tactics,
            "collective_tactics": self.collective_tactics,
            "threat_tactics": self.threat_tactics,
            "attributes": {
                "intelligence": self.intelligence,
                "aggressiveness": self.aggressiveness,
                "stealth": self.stealth,
                "strength": self.strength,
                "speed": self.speed,
                "adaptation_solo": self.adaptation_solo,
                "adaptation_group": self.adaptation_group
            }
        }

