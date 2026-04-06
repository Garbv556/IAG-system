"""
Agente Cavalo - 🐎
Espécie: Cavalo selvagem
Ambiente: Campos e pradarias
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import random
from core.base_agent import AnimalAgent


class CavaloAgent(AnimalAgent):
    """Agente representando um(a) Cavalo."""
    
    def __init__(self, agent_id: str = "cavalo_001"):
        super().__init__(agent_id=agent_id)
        
    def _set_animal_characteristics(self) -> None:
        """Define as características específicas do Cavalo."""
        self.species = "Cavalo selvagem"
        self.environment = "Campos e pradarias"
        self.characteristics = ['Velocidade', 'Resistencia', 'Manada forte']
        self.solo_behavior = "Vulneravel e alerta"
        self.group_behavior = "Manada coesa e protetora"
        self.attacks = ['Coice poderoso', 'Mordida', 'Pisoteamento']
        self.rival_response = "Fuga em grupo"
        
        # Fatores de adaptação
        self.adaptation_solo = 0.5
        self.adaptation_group = 0.88
        self.intelligence = 0.7
        self.aggressiveness = 0.5
        self.stealth = 0.4
        self.strength = 0.75
        self.speed = 0.9
    
    def get_special_abilities(self) -> Dict[str, float]:
        """Retorna habilidades especiais do Cavalo."""
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
        return (f"🐎 {self.animal_name}({self.agent_id}) - {self.environment}\n"
                f"   Características: {', '.join(self.characteristics)}")
