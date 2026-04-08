"""
Agente Hippowdon (Pokémon)
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


class HippowdonAgent(AnimalAgent):
    def __init__(self, agent_id: str = "hippowdon_001"):
        super().__init__(agent_id=agent_id)
        # O construtor chama _set_animal_characteristics internamente.
        
    def _set_animal_characteristics(self) -> None:
        self.animal_name = "Hippowdon"
        self.species = "Pokémon"
        self.environment = "Mundo Pokémon"
        self.characteristics = ["controle de ambiente"]
        # Adicionamos "powers" dinamicamente no dict ou na base se quiser
        self.powers = ["tempestade de areia", "domínio de território"]
        
        self.solo_behavior = "estabeleça domínio local"
        self.group_behavior = "controle área para o grupo"
        self.rival_response = "ataque imediato"
        
        # ═══ DOUTRINA TÁTICA ═══
        self.solo_tactics = ['estabeleça domínio local']
        self.collective_tactics = ['controle área para o grupo']
        self.threat_tactics = ['ataque imediato']
        
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
