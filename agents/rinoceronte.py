"""
Agente Rinoceronte - 🦏
Espécie: Rinoceronte-indiano
Ambiente: Savanas e pradarias
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import random
from core.base_agent import AnimalAgent


class RinoceronteAgent(AnimalAgent):
    """Agente representando um(a) Rinoceronte."""
    
    def __init__(self, agent_id: str = "rinoceronte_001"):
        super().__init__(agent_id=agent_id)
        
    def _set_animal_characteristics(self) -> None:
        """Define as características específicas do Rinoceronte."""
        self.species = "Rinoceronte-indiano"
        self.environment = "Savanas e pradarias"
        self.characteristics = ['Forca bruta', 'Chifre poderoso', 'Pele grossa']
        self.solo_behavior = "Territorial e imprevisivel"
        self.group_behavior = "Raro, geralmente solitario"
        self.attacks = ['Investida com chifre', 'Esmagamento', 'Carga frontal']
        self.rival_response = "Ataque direto e brutal"
        
        # Fatores de adaptação
        self.adaptation_solo = 0.8
        self.adaptation_group = 0.3
        self.intelligence = 0.6
        self.aggressiveness = 0.85
        self.stealth = 0.3
        self.strength = 0.95
        self.speed = 0.7
    
    def get_special_abilities(self) -> Dict[str, float]:
        """Retorna habilidades especiais do Rinoceronte."""
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
        return (f"🦏 {self.animal_name}({self.agent_id}) - {self.environment}\n"
                f"   Características: {', '.join(self.characteristics)}")
