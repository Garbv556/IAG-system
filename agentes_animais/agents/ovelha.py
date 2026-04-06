"""
Agente Ovelha - 🐑
Espécie: Ovelha domestica robusta
Ambiente: Campos e pastos
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import random
from ..core.base_agent import AnimalAgent


class OvelhaAgent(AnimalAgent):
    """Agente representando um(a) Ovelha."""
    
    def __init__(self, agent_id: str = "ovelha_001"):
        super().__init__(agent_id=agent_id)
        
    def _set_animal_characteristics(self) -> None:
        """Define as características específicas do Ovelha."""
        self.species = "Ovelha domestica robusta"
        self.environment = "Campos e pastos"
        self.characteristics = ['Defesa em grupo', 'Seguranca da manada', 'Resistencia']
        self.solo_behavior = "Fragil e vulneravel"
        self.group_behavior = "Forte manada protetora"
        self.attacks = ['Nenhum relevante']
        self.rival_response = "Fuga em grupo"
        
        # Fatores de adaptação
        self.adaptation_solo = 0.3
        self.adaptation_group = 0.82
        self.intelligence = 0.5
        self.aggressiveness = 0.2
        self.stealth = 0.3
        self.strength = 0.4
        self.speed = 0.5
    
    def get_special_abilities(self) -> Dict[str, float]:
        """Retorna habilidades especiais do Ovelha."""
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
        return (f"🐑 {self.animal_name}({self.agent_id}) - {self.environment}\n"
                f"   Características: {', '.join(self.characteristics)}")
