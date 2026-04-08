"""
Agente Kyogre (Pokémon)
"""

from typing import Dict, Any
import os
import sys
# Resolve o import para a raiz do projeto
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
from core.base_agent import AnimalAgent, State


class KyogreAgent(AnimalAgent):
    def __init__(self, agent_id: str = "kyogre_001"):
        super().__init__(agent_id=agent_id)
        # O construtor chama _set_animal_characteristics internamente.
        
    def _set_animal_characteristics(self) -> None:
        self.animal_name = "Kyogre"
        self.species = "Pokémon"
        self.environment = "Mundo Pokémon"
        self.characteristics = ["domínio ambiental total"]
        # Adicionamos "powers" dinamicamente no dict ou na base se quiser
        self.powers = ["controle oceânico", "chuva"]
        
        self.solo_behavior = "adapte o ambiente a seu favor"
        self.group_behavior = "amplifique o poder dos aliados"
        self.rival_response = "controle o cenário antes de agir"
        
        # ═══ DOUTRINA TÁTICA ═══
        self.solo_tactics = ['adapte o ambiente a seu favor']
        self.collective_tactics = ['amplifique o poder dos aliados']
        self.threat_tactics = ['controle o cenário antes de agir']
        
        # Fatores base
        self.adaptation_solo = 0.8
        self.adaptation_group = 0.8
        self.intelligence = 0.8
        self.aggressiveness = 0.7
        self.stealth = 0.5
        self.strength = 0.8
        self.speed = 0.8

    def get_doctrine_summary(self) -> Dict[str, Any]:
        doc = super().get_doctrine_summary()
        doc["powers"] = self.powers
        return doc
