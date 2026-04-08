"""
Agente Hipopotamo - 🦛
Espécie: Hipopotamo comum
Ambiente: Rios e lagos africanos
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import random
from core.base_agent import AnimalAgent


class HipoAgent(AnimalAgent):
    """Agente representando um(a) Hipopotamo."""
    
    def __init__(self, agent_id: str = "hipopotamo_001"):
        super().__init__(agent_id=agent_id)
        
    def _set_animal_characteristics(self) -> None:
        """Define as características específicas do Hipopotamo."""
        self.species = "Hipopotamo comum"
        self.environment = "Rios e lagos africanos"
        self.characteristics = ['Agressividade extrema', 'Altamente territorial', 'Mordida devastadora']
        self.solo_behavior = "Altamente territorial e agressivo"
        self.group_behavior = "Agrupados na agua, protecao mutua"
        self.attacks = ['Mordida devastadora', 'Investida subaquatica', 'Esmagamento']
        self.rival_response = "Ataque imediato sem hesitacao"
        
        # Fatores de adaptação
        self.adaptation_solo = 0.85
        self.adaptation_group = 0.7
        self.intelligence = 0.75
        self.aggressiveness = 0.98
        self.stealth = 0.4
        self.strength = 0.95
        self.speed = 0.65

        # ═══ DOUTRINA TÁTICA ═══
        self.solo_tactics = ['Defina limites claros', 'Não permita invasão de espaço']
        self.collective_tactics = ['Proteja zonas críticas', 'Reaja rápido a qualquer risco']
        self.threat_tactics = ['Ataque imediato se invadido', 'Não hesite sob pressão']
    
    def get_special_abilities(self) -> Dict[str, float]:
        """Retorna habilidades especiais do Hipopotamo."""
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
        return (f"🦛 {self.animal_name}({self.agent_id}) - {self.environment}\n"
                f"   Características: {', '.join(self.characteristics)}")
