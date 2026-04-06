"""
Agente Marlin - 🐟
Espécie: Marlim-azul
Ambiente: Oceano aberto
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import random
from ..core.base_agent import AnimalAgent


class MarlinAgent(AnimalAgent):
    """Agente representando um(a) Marlin."""
    
    def __init__(self, agent_id: str = "marlin_001"):
        super().__init__(agent_id=agent_id)
        
    def _set_animal_characteristics(self) -> None:
        """Define as características específicas do Marlin."""
        self.species = "Marlim-azul"
        self.environment = "Oceano aberto"
        self.characteristics = ['Velocidade extrema', 'Bico perfurante', 'Agilidade']
        self.solo_behavior = "Predador rapido"
        self.group_behavior = "Nao cooperativo"
        self.attacks = ['Bico perfurante', 'Investida rapida', 'Golpe lateral']
        self.rival_response = "Fuga ou ataque rapido"
        
        # Fatores de adaptação
        self.adaptation_solo = 0.9
        self.adaptation_group = 0.3
        self.intelligence = 0.6
        self.aggressiveness = 0.7
        self.stealth = 0.6
        self.strength = 0.7
        self.speed = 0.95
    
    def get_special_abilities(self) -> Dict[str, float]:
        """Retorna habilidades especiais do Marlin."""
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
        return (f"🐟 {self.animal_name}({self.agent_id}) - {self.environment}\n"
                f"   Características: {', '.join(self.characteristics)}")
