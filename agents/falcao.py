"""
Agente Falcao - 🦅
Espécie: Falcao-peregrino
Ambiente: Diverso (montanhas, cidades)
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import random
from core.base_agent import AnimalAgent


class FalcaoAgent(AnimalAgent):
    """Agente representando um(a) Falcao."""
    
    def __init__(self, agent_id: str = "falcao_001"):
        super().__init__(agent_id=agent_id)
        
    def _set_animal_characteristics(self) -> None:
        """Define as características específicas do Falcao."""
        self.species = "Falcao-peregrino"
        self.environment = "Diverso (montanhas, cidades)"
        self.characteristics = ['Velocidade maxima', 'Visao agucada', 'Precisao']
        self.solo_behavior = "Cacador aereo solitario"
        self.group_behavior = "Raro, apenas em acasalamento"
        self.attacks = ['Mergulho supersonico', 'Golpe de asas', 'Garras afiadas']
        self.rival_response = "Ataque ou fuga rapida"
        
        # Fatores de adaptação
        self.adaptation_solo = 0.95
        self.adaptation_group = 0.4
        self.intelligence = 0.75
        self.aggressiveness = 0.7
        self.stealth = 0.6
        self.strength = 0.5
        self.speed = 0.99
    
    def get_special_abilities(self) -> Dict[str, float]:
        """Retorna habilidades especiais do Falcao."""
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
        return (f"🦅 {self.animal_name}({self.agent_id}) - {self.environment}\n"
                f"   Características: {', '.join(self.characteristics)}")
