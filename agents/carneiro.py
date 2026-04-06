"""
Agente Carneiro - 🐏
Espécie: Carneiro-selvagem
Ambiente: Montanhas rochosas
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import random
from core.base_agent import AnimalAgent


class CarneiroAgent(AnimalAgent):
    """Agente representando um(a) Carneiro."""
    
    def __init__(self, agent_id: str = "carneiro_001"):
        super().__init__(agent_id=agent_id)
        
    def _set_animal_characteristics(self) -> None:
        """Define as características específicas do Carneiro."""
        self.species = "Carneiro-selvagem"
        self.environment = "Montanhas rochosas"
        self.characteristics = ['Combate por impacto', 'Chifres fortes', 'Hierarquia']
        self.solo_behavior = "Competitivo e desafiador"
        self.group_behavior = "Hierarquia por combate"
        self.attacks = ['Cabecada poderosa', 'Investida', 'Empurrao']
        self.rival_response = "Confronto direto"
        
        # Fatores de adaptação
        self.adaptation_solo = 0.7
        self.adaptation_group = 0.75
        self.intelligence = 0.6
        self.aggressiveness = 0.7
        self.stealth = 0.4
        self.strength = 0.8
        self.speed = 0.65
    
    def get_special_abilities(self) -> Dict[str, float]:
        """Retorna habilidades especiais do Carneiro."""
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
        return (f"🐏 {self.animal_name}({self.agent_id}) - {self.environment}\n"
                f"   Características: {', '.join(self.characteristics)}")
