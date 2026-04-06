"""
Agente Elefante - Características de força extrema e inteligência
"""

from typing import Any
from core.base_agent import AnimalAgent, State


class Elefante(AnimalAgent):
    """
    Agente representando um Elefante Africano.
    
    Características:
    - Espécie dominante: Elefante-africano
    - Ambiente: Savanas
    - Características: Força extrema + inteligência
    - Sozinho: Machos perigosos
    - Em grupo: Estrutura familiar forte
    """
    
    def _set_animal_characteristics(self) -> None:
        self.species = "Elefante-africano"
        self.environment = "Savanas"
        self.characteristics = ["Força extrema", "Inteligência", "Memória"]
        self.solo_behavior = "Machos perigosos"
        self.group_behavior = "Estrutura familiar forte"
        self.attacks = ["Investida", "Esmagamento"]
        self.rival_response = "Proteção coletiva"
        
        self.adaptation_solo = 0.7
        self.adaptation_group = 0.95
        self.intelligence = 0.92
        self.aggressiveness = 0.6
        self.stealth = 0.3
        self.strength = 1.0
        self.speed = 0.5
    
    def _process_message(self, message: str, sender_id: str) -> str:
        if self.state == State.GROUP:
            return f"[🐘 Elefante] Em família, recebemos: {message[:40]}..."
        else:
            return f"[🐘 Elefante] Recebi: {message[:40]}... Cuidado comigo."
    
    def learn(self, topic: str, content: Any) -> float:
        if self.state == State.GROUP:
            self.intelligence = 0.95
        else:
            self.intelligence = 0.85
        return super().learn(topic, content)
    
    def set_state(self, new_state: State) -> None:
        if new_state == State.GROUP:
            print(f"[🐘 Elefante] Protegendo a manada!")
            self.aggressiveness = 0.7
        elif new_state == State.SOLO:
            print(f"[🐘 Elefante] Sozinho e perigoso.")
            self.aggressiveness = 0.85
        super().set_state(new_state)
