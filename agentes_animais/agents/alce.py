"""
Agente Alce - 🦌
Espécie: Alce adulto macho
Ambiente: Regioes frias e florestas
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import random
from ..core.base_agent import AnimalAgent


class AlceAgent(AnimalAgent):
    """Agente representando um(a) Alce."""
    
    def __init__(self, agent_id: str = "alce_001"):
        super().__init__(agent_id=agent_id)
        
    def _set_animal_characteristics(self) -> None:
        """Define as características específicas do Alce."""
        self.species = "Alce adulto macho"
        self.environment = "Regioes frias e florestas"
        self.characteristics = ['Forca inesperada', 'Chifres enormes', 'Solitario']
        self.solo_behavior = "Solitario e territorial"
        self.group_behavior = "Raro, apenas em acasalamento"
        self.attacks = ['Chifres + coice', 'Investida', 'Pisoteamento']
        self.rival_response = "Defesa agressiva"
        
        # Fatores de adaptação
        self.adaptation_solo = 0.82
        self.adaptation_group = 0.4
        self.intelligence = 0.65
        self.aggressiveness = 0.7
        self.stealth = 0.5
        self.strength = 0.85
        self.speed = 0.6
    
    def get_special_abilities(self) -> Dict[str, float]:
        """Retorna habilidades especiais do Alce."""
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
        return (f"🦌 {self.animal_name}({self.agent_id}) - {self.environment}\n"
                f"   Características: {', '.join(self.characteristics)}")
