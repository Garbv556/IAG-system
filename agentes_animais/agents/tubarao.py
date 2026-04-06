"""
Agente Tubarao - 🦈
Espécie: Tubarao-branco
Ambiente: Oceanos
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import random
from ..core.base_agent import AnimalAgent


class TubaraoAgent(AnimalAgent):
    """Agente representando um(a) Tubarao."""
    
    def __init__(self, agent_id: str = "tubarao_001"):
        super().__init__(agent_id=agent_id)
        
    def _set_animal_characteristics(self) -> None:
        """Define as características específicas do Tubarao."""
        self.species = "Tubarao-branco"
        self.environment = "Oceanos"
        self.characteristics = ['Predador perfeito', 'Sensores agucados', 'Forca mortal']
        self.solo_behavior = "Cacador solitario eficiente"
        self.group_behavior = "Nao cooperativo"
        self.attacks = ['Investida de baixo', 'Mordida letal', 'Serra com dentes']
        self.rival_response = "Avalia antes de atacar"
        
        # Fatores de adaptação
        self.adaptation_solo = 0.9
        self.adaptation_group = 0.3
        self.intelligence = 0.7
        self.aggressiveness = 0.85
        self.stealth = 0.8
        self.strength = 0.9
        self.speed = 0.85
    
    def get_special_abilities(self) -> Dict[str, float]:
        """Retorna habilidades especiais do Tubarao."""
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
        return (f"🦈 {self.animal_name}({self.agent_id}) - {self.environment}\n"
                f"   Características: {', '.join(self.characteristics)}")
