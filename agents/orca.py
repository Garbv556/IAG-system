"""
Agente Orca - 🐋
Espécie: Orca (ecotipo cacador)
Ambiente: Oceanos
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import random
from core.base_agent import AnimalAgent


class OrcaAgent(AnimalAgent):
    """Agente representando um(a) Orca."""
    
    def __init__(self, agent_id: str = "orca_001"):
        super().__init__(agent_id=agent_id)
        
    def _set_animal_characteristics(self) -> None:
        """Define as características específicas do Orca."""
        self.species = "Orca (ecotipo cacador)"
        self.environment = "Oceanos"
        self.characteristics = ['Inteligencia maxima', 'Estrategia coletiva', 'Forca do pod']
        self.solo_behavior = "Raro, mas capaz"
        self.group_behavior = "Caca em equipe altamente coordenada"
        self.attacks = ['Estrategia coletiva', 'Ondas para derrubar presas', 'Ataques coordenados']
        self.rival_response = "Dominacao total em grupo"
        
        # Fatores de adaptação
        self.adaptation_solo = 0.5
        self.adaptation_group = 0.98
        self.intelligence = 0.95
        self.aggressiveness = 0.8
        self.stealth = 0.7
        self.strength = 0.9
        self.speed = 0.85
    
    def get_special_abilities(self) -> Dict[str, float]:
        """Retorna habilidades especiais do Orca."""
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
        return (f"🐋 {self.animal_name}({self.agent_id}) - {self.environment}\n"
                f"   Características: {', '.join(self.characteristics)}")
