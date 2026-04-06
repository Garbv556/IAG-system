"""
Agente Polvo - 🐙
Espécie: Polvo-gigante-do-Pacifico
Ambiente: Fundo oceanico
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import random
from ..core.base_agent import AnimalAgent


class PolvoAgent(AnimalAgent):
    """Agente representando um(a) Polvo."""
    
    def __init__(self, agent_id: str = "polvo_001"):
        super().__init__(agent_id=agent_id)
        
    def _set_animal_characteristics(self) -> None:
        """Define as características específicas do Polvo."""
        self.species = "Polvo-gigante-do-Pacifico"
        self.environment = "Fundo oceanico"
        self.characteristics = ['Inteligencia absurda', 'Camuflagem', 'Flexibilidade extrema']
        self.solo_behavior = "Estrategico e calculista"
        self.group_behavior = "Nao existe comportamento em grupo"
        self.attacks = ['Tentáculos constritores', 'Jato de tinta', 'Veneno']
        self.rival_response = "Camuflagem e fuga estrategica"
        
        # Fatores de adaptação
        self.adaptation_solo = 1.0
        self.adaptation_group = 0.2
        self.intelligence = 1.0
        self.aggressiveness = 0.5
        self.stealth = 0.98
        self.strength = 0.6
        self.speed = 0.7
    
    def get_special_abilities(self) -> Dict[str, float]:
        """Retorna habilidades especiais do Polvo."""
        return {
            "intelligence": self.intelligence,
            "aggressiveness": self.aggressiveness,
            "stealth": self.stealth,
            "strength": self.strength,
            "speed": self.speed,
            "adaptation_solo": self.adaptation_solo,
            "adaptation_group": self.adaptation_group
        }
    
    def __str__(self) -> str:
        return (f"🐙 {self.animal_name}({self.agent_id}) - {self.environment}\n"
                f"   Características: {', '.join(self.characteristics)}")
