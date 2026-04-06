"""
Agente Leopardo - 🐆
Espécie: Leopardo-africano
Ambiente: Florestas e savanas
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import random
from core.base_agent import AnimalAgent


class LeopardoAgent(AnimalAgent):
    """Agente representando um(a) Leopardo."""
    
    def __init__(self, agent_id: str = "leopardo_001"):
        super().__init__(agent_id=agent_id)
        
    def _set_animal_characteristics(self) -> None:
        """Define as características específicas do Leopardo."""
        self.species = "Leopardo-africano"
        self.environment = "Florestas e savanas"
        self.characteristics = ['Furtividade extrema', 'Cacador perfeito', 'Agil em arvores']
        self.solo_behavior = "Cacador solitario perfeito"
        self.group_behavior = "Nao existe"
        self.attacks = ['Emboscada', 'Subida em arvores', 'Mordida na garganta']
        self.rival_response = "Evita ou ataca rapido"
        
        # Fatores de adaptação
        self.adaptation_solo = 0.95
        self.adaptation_group = 0.2
        self.intelligence = 0.8
        self.aggressiveness = 0.7
        self.stealth = 0.98
        self.strength = 0.75
        self.speed = 0.85
    
    def get_special_abilities(self) -> Dict[str, float]:
        """Retorna habilidades especiais do Leopardo."""
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
        return (f"🐆 {self.animal_name}({self.agent_id}) - {self.environment}\n"
                f"   Características: {', '.join(self.characteristics)}")
