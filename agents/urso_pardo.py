"""
Agente Urso Pardo - 🐻
Espécie: Urso Kodiak
Ambiente: Florestas frias
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import random
from core.base_agent import AnimalAgent


class UrsoPardoAgent(AnimalAgent):
    """Agente representando um(a) Urso Pardo."""
    
    def __init__(self, agent_id: str = "urso_pardo_001"):
        super().__init__(agent_id=agent_id)
        
    def _set_animal_characteristics(self) -> None:
        """Define as características específicas do Urso Pardo."""
        self.species = "Urso Kodiak"
        self.environment = "Florestas frias"
        self.characteristics = ['Forca extrema', 'Resistencia', 'Predador dominante']
        self.solo_behavior = "Predador dominante e territorial"
        self.group_behavior = "Solitario, exceto maes com filhotes"
        self.attacks = ['Garras + mordida', 'Investida', 'Esmagamento']
        self.rival_response = "Combate direto"
        
        # Fatores de adaptação
        self.adaptation_solo = 0.9
        self.adaptation_group = 0.3
        self.intelligence = 0.75
        self.aggressiveness = 0.8
        self.stealth = 0.6
        self.strength = 0.95
        self.speed = 0.65
    
    def get_special_abilities(self) -> Dict[str, float]:
        """Retorna habilidades especiais do Urso Pardo."""
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
        return (f"🐻 {self.animal_name}({self.agent_id}) - {self.environment}\n"
                f"   Características: {', '.join(self.characteristics)}")
