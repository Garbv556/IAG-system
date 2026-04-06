"""
Agente Coelho - 🐇
Espécie: Coelho-europeu
Ambiente: Campos e bosques
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import random
from ..core.base_agent import AnimalAgent


class CoelhoAgent(AnimalAgent):
    """Agente representando um(a) Coelho."""
    
    def __init__(self, agent_id: str = "coelho_001"):
        super().__init__(agent_id=agent_id)
        
    def _set_animal_characteristics(self) -> None:
        """Define as características específicas do Coelho."""
        self.species = "Coelho-europeu"
        self.environment = "Campos e bosques"
        self.characteristics = ['Sobrevivencia por fuga', 'Alerta constante', 'Reproducao rapida']
        self.solo_behavior = "Alerta e cauteloso"
        self.group_behavior = "Colonia organizada"
        self.attacks = ['Nenhum']
        self.rival_response = "Fuga rapida"
        
        # Fatores de adaptação
        self.adaptation_solo = 0.7
        self.adaptation_group = 0.75
        self.intelligence = 0.6
        self.aggressiveness = 0.2
        self.stealth = 0.7
        self.strength = 0.3
        self.speed = 0.85
    
    def get_special_abilities(self) -> Dict[str, float]:
        """Retorna habilidades especiais do Coelho."""
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
        return (f"🐇 {self.animal_name}({self.agent_id}) - {self.environment}\n"
                f"   Características: {', '.join(self.characteristics)}")
