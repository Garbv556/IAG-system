"""
Agente Lobo - 🐺
Espécie: Lobo-cinzento
Ambiente: Florestas e tundra
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import random
from core.base_agent import AnimalAgent


class LoboAgent(AnimalAgent):
    """Agente representando um(a) Lobo."""
    
    def __init__(self, agent_id: str = "lobo_001"):
        super().__init__(agent_id=agent_id)
        
    def _set_animal_characteristics(self) -> None:
        """Define as características específicas do Lobo."""
        self.species = "Lobo-cinzento"
        self.environment = "Florestas e tundra"
        self.characteristics = ['Estrategia em grupo', 'Hierarquia forte', 'Resistencia']
        self.solo_behavior = "Cauteloso e observador"
        self.group_behavior = "Hierarquia forte, caca coordenada"
        self.attacks = ['Cercar e desgastar', 'Mordida coordenada', 'Perseguicao em equipe']
        self.rival_response = "Defesa coordenada do pacote"
        
        # Fatores de adaptação
        self.adaptation_solo = 0.6
        self.adaptation_group = 0.95
        self.intelligence = 0.85
        self.aggressiveness = 0.7
        self.stealth = 0.75
        self.strength = 0.7
        self.speed = 0.8
    
    def get_special_abilities(self) -> Dict[str, float]:
        """Retorna habilidades especiais do Lobo."""
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
        return (f"🐺 {self.animal_name}({self.agent_id}) - {self.environment}\n"
                f"   Características: {', '.join(self.characteristics)}")
