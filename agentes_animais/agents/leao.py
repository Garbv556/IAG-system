"""
Agente Leão - Características de liderança e domínio
"""

from typing import Dict, Any
from ..core.base_agent import AnimalAgent, State


class Leao(AnimalAgent):
    """
    Agente representando um Leão Africano.
    
    Características:
    - Espécie dominante: Leão-africano
    - Ambiente: Savanas abertas
    - Características: Força, domínio territorial, liderança
    - Sozinho: Mais agressivo e instável
    - Em grupo: Caça coordenada (pride)
    """
    
    def _set_animal_characteristics(self) -> None:
        # Informações básicas
        self.species = "Leão-africano"
        self.environment = "Savanas abertas"
        
        # Características principais
        self.characteristics = ["Força", "Domínio territorial", "Liderança"]
        
        # Comportamentos
        self.solo_behavior = "Mais agressivo e instável"
        self.group_behavior = "Caça coordenada (pride)"
        
        # Ataques
        self.attacks = ["Mordida no pescoço", "Emboscada em grupo"]
        self.rival_response = "Enfrenta diretamente e defende território"
        
        # Fatores de adaptação (0-1)
        self.adaptation_solo = 0.6  # Consegue ficar sozinho mas prefere grupo
        self.adaptation_group = 0.95  # Excelente em grupo
        
        # Atributos
        self.intelligence = 0.75  # Inteligente
        self.aggressiveness = 0.85  # Muito agressivo quando sozinho
        self.stealth = 0.6  # Moderadamente furtivo
        self.strength = 0.9  # Muito forte
        self.speed = 0.7  # Rápido
    
    def _process_message(self, message: str, sender_id: str) -> str:
        """Leão processa mensagens com postura de liderança"""
        if self.state == State.GROUP:
            return f"[🦁 Leão] Como líder, recebi: {message[:40]}... Vamos coordenar!"
        else:
            return f"[🦁 Leão] Recebi sua mensagem: {message[:40]}... Estou vigilante."
    
    def learn(self, topic: str, content: Any) -> float:
        """Leões aprendem melhor em grupo (pride)"""
        if self.state == State.GROUP:
            self.intelligence = 0.85  # Mais inteligente em grupo
        else:
            self.intelligence = 0.65  # Menos focado sozinho
        
        return super().learn(topic, content)
    
    def set_state(self, new_state: State) -> None:
        """Leões mudam comportamento drasticamente entre solo/grupo"""
        old_state = self.state
        super().set_state(new_state)
        
        if new_state == State.GROUP:
            print(f"[🦁 Leão] Em grupo! Pronto para caça coordenada!")
            self.aggressiveness = 0.7  # Mais controlado em grupo
        elif new_state == State.SOLO:
            print(f"[🦁 Leão] Sozinho no território. Mais agressivo!")
            self.aggressiveness = 0.95  # Mais agressivo sozinho
