from .base_agent import AnimalAgent, State
from typing import List

class LionAgent(AnimalAgent):
    def _set_animal_characteristics(self) -> None:
        self.species = "Panthera leo"
        self.environment = "Savana"
        self.characteristics = ["Líder nato", "Forte", "Social"]
        self.solo_behavior = "Patrulhamento territorial e observação estratégica."
        self.group_behavior = "Coordenação de caça tática e proteção da alcateia."
        self.solo_tactics = ["Emboscada furtiva", "Rugido de intimidação"]
        self.collective_tactics = ["Flanqueamento coordenado", "Círculo de proteção"]
        self.threat_tactics = ["Ataque frontal massivo", "Defesa de território"]
        self.intelligence = 0.85
        self.strength = 0.95
        self.speed = 0.80
        self.adaptation_group = 0.90

class TigerAgent(AnimalAgent):
    def _set_animal_characteristics(self) -> None:
        self.species = "Panthera tigris"
        self.environment = "Florestas densas"
        self.characteristics = ["Solitário", "Ágil", "Poderoso"]
        self.solo_behavior = "Caça furtiva baseada em paciência e precisão."
        self.group_behavior = "Aliança temporária incomum para grandes ameaças."
        self.solo_tactics = ["Ataque surpresa letal", "Camuflagem em sombras"]
        self.collective_tactics = ["Divisão de atenção", "Ataques alternados"]
        self.threat_tactics = ["Contragolpe explosivo", "Escalada tática"]
        self.intelligence = 0.88
        self.strength = 0.90
        self.speed = 0.92
        self.adaptation_solo = 0.95

class ElephantAgent(AnimalAgent):
    def _set_animal_characteristics(self) -> None:
        self.species = "Loxodonta"
        self.environment = "Diversos (Savana/Floresta)"
        self.characteristics = ["Memória excepcional", "Resistente", "Sentimental"]
        self.solo_behavior = "Navegação por longas distâncias e busca por recursos."
        self.group_behavior = "Matriarcado forte e proteção extrema de membros jovens."
        self.solo_tactics = ["Carga de dissuasão", "Uso de ferramentas naturais"]
        self.collective_tactics = ["Formação de barreira intransponível", "Troca de frequências infra-sônicas"]
        self.threat_tactics = ["Pisotear tático", "Sincronização de manada"]
        self.intelligence = 0.98
        self.strength = 1.0
        self.speed = 0.40
        self.adaptation_group = 0.98

class FoxAgent(AnimalAgent):
    def _set_animal_characteristics(self) -> None:
        self.species = "Vulpes vulpes"
        self.environment = "Diversos (Urbano/Floresta)"
        self.characteristics = ["Astuto", "Adaptável", "Pequeno"]
        self.solo_behavior = "Infiltração silenciosa e resolução de quebra-cabeças."
        self.group_behavior = "Compartilhamento de segredos e rotas de fuga."
        self.solo_tactics = ["Desvio de atenção", "Despistamento por trilha"]
        self.collective_tactics = ["Logística de suprimentos", "Vigilância em rede"]
        self.threat_tactics = ["Bico de fuga", "Enterre de recursos críticos"]
        self.intelligence = 0.92
        self.strength = 0.30
        self.speed = 0.85
        self.adaptation_solo = 0.90

# Mapeamento para fácil inst instanciação
AGENT_CLASSES = {
    'LionAgent': LionAgent,
    'TigerAgent': TigerAgent,
    'ElephantAgent': ElephantAgent,
    'FoxAgent': FoxAgent
}
