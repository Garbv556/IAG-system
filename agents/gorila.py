"""
Agente Gorila - 🦍
Espécie: Gorila-da-montanha
Ambiente: Florestas densas
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import random
from core.base_agent import AnimalAgent


class GorilaAgent(AnimalAgent):
    """Agente representando um(a) Gorila."""
    
    def __init__(self, agent_id: str = "gorila_001"):
        super().__init__(agent_id=agent_id)
        
    def _set_animal_characteristics(self) -> None:
        """Define as características específicas do Gorila."""
        self.species = "Gorila-da-montanha"
        self.environment = "Florestas densas"
        self.characteristics = ['Forca extrema', 'Intimidacao', 'Lideranca silverback']
        self.solo_behavior = "Muito perigoso e territorial"
        self.group_behavior = "Lideranca forte, protecao familiar"
        self.attacks = ['Forca bruta', 'Socos no peito', 'Investida']
        self.rival_response = "Intimidacao seguida de ataque"
        
        # Fatores de adaptação
        self.adaptation_solo = 0.7
        self.adaptation_group = 0.9
        self.intelligence = 0.85
        self.aggressiveness = 0.75
        self.stealth = 0.5
        self.strength = 0.95
        self.speed = 0.6

        # ═══ DOUTRINA TÁTICA ═══
        self.solo_tactics = ['Demonstre presença', 'Evite conflito desnecessário']
        self.collective_tactics = ['Proteja aliados próximos', 'Imponha respeito']
        self.threat_tactics = ['Intimide primeiro', 'Ataque se necessário']
    
    def get_special_abilities(self) -> Dict[str, float]:
        """Retorna habilidades especiais do Gorila."""
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
        return (f"🦍 {self.animal_name}({self.agent_id}) - {self.environment}\n"
                f"   Características: {', '.join(self.characteristics)}")
