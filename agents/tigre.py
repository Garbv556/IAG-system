"""
Agente Tigre - Características de furtividade e poder solitário
"""

from typing import Any
from core.base_agent import AnimalAgent, State


class Tigre(AnimalAgent):
    """
    Agente representando um Tigre Siberiano.
    
    Características:
    - Espécie dominante: Tigre-siberiano
    - Ambiente: Florestas densas
    - Características: Força + furtividade máxima
    - Sozinho: Predador perfeito
    - Em grupo: Não existe
    """
    
    def _set_animal_characteristics(self) -> None:
        # Informações básicas
        self.species = "Tigre-siberiano"
        self.environment = "Florestas densas"
        
        # Características principais
        self.characteristics = ["Força", "Furtividade máxima", "Independência"]
        
        # Comportamentos
        self.solo_behavior = "Predador perfeito"
        self.group_behavior = "Não existe (solitário)"
        
        # Ataques
        self.attacks = ["Emboscada silenciosa", "Mordida letal"]
        self.rival_response = "Evita ou elimina rapidamente"
        
        # Fatores de adaptação (0-1)
        self.adaptation_solo = 0.98  # Perfeito sozinho
        self.adaptation_group = 0.1  # Péssimo em grupo
        
        # Atributos
        self.intelligence = 0.85  # Muito inteligente
        self.aggressiveness = 0.8  # Agressivo quando necessário
        self.stealth = 0.98  # Furtividade máxima
        self.strength = 0.92  # Muito forte
        self.speed = 0.75  # Rápido

        # ═══ DOUTRINA TÁTICA ═══
        self.solo_tactics = ['Observe antes de agir', 'Ataque apenas quando tiver vantagem']
        self.collective_tactics = ['Atue como executor silencioso', 'Entre apenas no momento decisivo']
        self.threat_tactics = ['Evite conflito desnecessário', 'Elimine rapidamente se inevitável']
    
    def _process_message(self, message: str, sender_id: str) -> str:
        """Tigres são diretos e preferem comunicação mínima"""
        if self.state == State.SOLO:
            return f"[🐅 Tigre] ... {message[:30]} ... Entendido."
        else:
            return f"[🐅 Tigre] Preferia estar sozinho. Mensagem: {message[:30]}"
    
    def learn(self, topic: str, content: Any) -> float:
        """Tigres aprendem melhor sozinhos"""
        if self.state == State.GROUP:
            self.intelligence = 0.6  # Menos focado em grupo
            print(f"[🐅 Tigre] Incomodado por estar em grupo para aprender...")
        else:
            self.intelligence = 0.9  # Foco máximo sozinho
        
        return super().learn(topic, content)
    
    def set_state(self, new_state: State) -> None:
        """Tigres evitam estado de grupo"""
        if new_state == State.GROUP:
            print(f"[🐅 Tigre] ⚠️ Alerta: Em grupo! Isso é incomum para mim.")
            self.aggressiveness = 0.9  # Mais agressivo em grupo
        elif new_state == State.SOLO:
            print(f"[🐅 Tigre] Sozinho na floresta. Estado perfeito.")
            self.aggressiveness = 0.7  # Mais calmo sozinho
        
        super().set_state(new_state)
