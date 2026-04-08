"""
Agente Crocodilo - 🐊
Espécie: Crocodilo-de-agua-salgada
Ambiente: Rios e mares tropicais
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import random
from core.base_agent import AnimalAgent


class CrocodiloAgent(AnimalAgent):
    """Agente representando um(a) Crocodilo."""
    
    def __init__(self, agent_id: str = "crocodilo_001"):
        super().__init__(agent_id=agent_id)
        
    def _set_animal_characteristics(self) -> None:
        """Define as características específicas do Crocodilo."""
        self.species = "Crocodilo-de-agua-salgada"
        self.environment = "Rios e mares tropicais"
        self.characteristics = ['Emboscada perfeita', 'Paciencia extrema', 'Mandibula poderosa']
        self.solo_behavior = "Predador paciente e silencioso"
        self.group_behavior = "Nao cooperativo"
        self.attacks = ['Giro da morte', 'Embosca aquatica', 'Mordida esmagadora']
        self.rival_response = "Ataque surpresa"
        
        # Fatores de adaptação
        self.adaptation_solo = 0.88
        self.adaptation_group = 0.3
        self.intelligence = 0.7
        self.aggressiveness = 0.8
        self.stealth = 0.9
        self.strength = 0.9
        self.speed = 0.6

        # ═══ DOUTRINA TÁTICA ═══
        self.solo_tactics = ['Espere o momento certo', 'Não revele intenções']
        self.collective_tactics = ['Aproveite distrações criadas por outros', 'Atue no momento exato']
        self.threat_tactics = ['Ataque surpresa', 'Finalize rapidamente']
    
    def get_special_abilities(self) -> Dict[str, float]:
        """Retorna habilidades especiais do Crocodilo."""
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
        return (f"🐊 {self.animal_name}({self.agent_id}) - {self.environment}\n"
                f"   Características: {', '.join(self.characteristics)}")
