"""
Agente Canguru - 🦘
Espécie: Canguru-vermelho (Macropus rufus)
Ambiente: Regiões áridas e savanas da Austrália

Características:
- Pernas extremamente fortes
- Equilíbrio com a cauda
- Alta resistência e mobilidade

Comportamento:
- Sozinho: Mais cauteloso, evita confronto direto
- Em grupo (mob): Organização leve, sem hierarquia rígida; machos disputam dominância

Ataques/Defesa:
- Chutes frontais poderosos
- Uso da cauda como apoio para golpear
- Agarrar e "rasgar" com as patas traseiras
- Se encurralado: luta com chutes extremamente fortes
- Em água: tenta afogar o oponente
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import random
from core.base_agent import AnimalAgent


class CanguruAgent(AnimalAgent):
    """Agente representando um Canguru-vermelho."""
    
    def __init__(self, agent_id: str = "canguru_001"):
        super().__init__(agent_id=agent_id)
        
        # Características específicas do Canguru
        self.jump_power = 0.9  # Poder de salto
        self.tail_balance = 0.85  # Equilíbrio com a cauda
        self.endurance = 0.88  # Resistência
        self.mobility = 0.92  # Mobilidade
        
    def _set_animal_characteristics(self) -> None:
        """Define as características específicas do Canguru."""
        self.species = "Canguru-vermelho (Macropus rufus)"
        self.environment = "Regiões áridas e savanas da Austrália"
        self.characteristics = [
            "Pernas extremamente fortes",
            "Equilíbrio com a cauda",
            "Alta resistência e mobilidade"
        ]
        self.solo_behavior = "Mais cauteloso, evita confronto direto"
        self.group_behavior = "Organização leve, sem hierarquia rígida; machos disputam dominância"
        self.attacks = [
            "Chutes frontais poderosos",
            "Uso da cauda como apoio para golpear",
            "Agarrar e rasgar com patas traseiras"
        ]
        self.rival_response = "Fuga rápida ou chutes devastadores se encurralado"
        
        # Fatores de adaptação
        self.adaptation_solo = 0.65  # Cauteloso sozinho
        self.adaptation_group = 0.75  # Melhor em grupo (mob)
        self.intelligence = 0.75
        self.aggressiveness = 0.4  # Baixa agressividade, prefere fuga
        self.stealth = 0.5
        self.strength = 0.7
        self.speed = 0.85
        
    def get_special_abilities(self) -> Dict[str, float]:
        """Retorna habilidades especiais do Canguru."""
        return {
            "jump_power": self.jump_power,
            "tail_balance": self.tail_balance,
            "endurance": self.endurance,
            "mobility": self.mobility,
            "kick_strength": 0.95  # Força do chute
        }
    
    def adapt_learning(self, topic: str, context: str = "solo") -> Dict[str, Any]:
        """
        Adapta o aprendizado baseado no contexto (solo ou grupo).
        Cangurus são mais cautelosos sozinhos, mas mais eficazes em mobilidade em grupo.
        """
        base_proficiency = self.get_overall_programming_skill()
        
        if context == "solo":
            # Sozinho: mais cauteloso, aprendizado mais lento mas cuidadoso
            adaptation_factor = 0.75
            strategy = "aprendizado_cauteloso"
            description = "Aprendendo de forma cautelosa e metódica, evitando riscos"
        else:  # group
            # Em grupo: organização leve, aprendizado colaborativo com mobilidade
            adaptation_factor = 0.85
            strategy = "aprendizado_mob_coordenado"
            description = "Aprendendo com mobilidade entre conceitos, saltando entre tópicos relacionados"
        
        final_proficiency = min(1.0, base_proficiency * adaptation_factor)
        
        learning_result = {
            "topic": topic,
            "proficiency": final_proficiency,
            "adaptation_factor": adaptation_factor,
            "strategy": strategy,
            "context": context,
            "description": description,
            "timestamp": datetime.now().isoformat(),
            "special_notes": f"Canguru usa sua alta mobilidade para navegar entre conceitos de {topic}"
        }
        
        self.learning_history.append(learning_result)
        return learning_result
    
    def communicate(self, message: str, recipient: Optional[str] = None) -> Dict[str, Any]:
        """
        Comunica-se com personalidade de Canguru.
        Mensagens diretas e energéticas, com saltos entre idéias.
        """
        communication = {
            "sender": self.agent_id,
            "recipient": recipient or "broadcast",
            "message": message,
            "style": "energético_e_direto",
            "characteristics": [
                "Saltos entre conceitos relacionados",
                "Comunicação direta e objetiva",
                "Ênfase em mobilidade e adaptação"
            ],
            "tone": "cauteloso_se_sozinho_entusiasta_em_grupo",
            "timestamp": datetime.now().isoformat()
        }
        
        self.communication_log.append(communication)
        return communication
    
    def execute_action(self, action_type: str, target: Optional[str] = None, 
                      context: str = "solo") -> Dict[str, Any]:
        """
        Executa uma ação baseada no tipo e contexto.
        """
        action_result = {
            "agent": self.agent_id,
            "action_type": action_type,
            "target": target,
            "context": context,
            "timestamp": datetime.now().isoformat(),
            "success": False,
            "details": {}
        }
        
        if action_type == "attack":
            if context == "solo":
                # Sozinho: cauteloso, prefere fuga
                action_result["success"] = random.random() < 0.6
                action_result["details"] = {
                    "strategy": "chute_defensivo_se_encurralado",
                    "power": self.kick_strength if hasattr(self, 'kick_strength') else 0.95,
                    "description": "Canguru evita confronto, mas se encurralado desferre chutes poderosos"
                }
            else:
                # Em grupo: mais confiante
                action_result["success"] = random.random() < 0.8
                action_result["details"] = {
                    "strategy": "chutes_coordenados_com_cauda",
                    "power": 0.9,
                    "description": "Canguru usa cauda como apoio para chutes coordenados"
                }
        
        elif action_type == "defend":
            if context == "solo":
                action_result["success"] = random.random() < 0.7
                action_result["details"] = {
                    "strategy": "fuga_rapida_ou_chute_defensivo",
                    "mobility_used": self.mobility,
                    "description": "Prefere fuga, mas luta se necessário"
                }
            else:
                action_result["success"] = random.random() < 0.85
                action_result["details"] = {
                    "strategy": "defesa_com_mobilidade_em_grupo",
                    "group_coordination": 0.6,
                    "description": "Organização leve para defesa mútua"
                }
        
        elif action_type == "learn":
            learning = self.adapt_learning(target or "generic", context)
            action_result["success"] = True
            action_result["details"] = learning
        
        elif action_type == "move":
            # Ação de movimento - especialidade do Canguru
            action_result["success"] = True
            action_result["details"] = {
                "jump_distance": self.jump_power * 10,  # metros simulados
                "speed": self.mobility * 100,  # km/h simulados
                "balance": self.tail_balance,
                "description": "Canguru salta com alta mobilidade e equilíbrio"
            }
        
        else:
            action_result["details"] = {
                "error": f"Ação '{action_type}' não reconhecida",
                "available_actions": ["attack", "defend", "learn", "move"]
            }
        
        return action_result
    
    def help_other_agent(self, learner: AnimalAgent, topic: str) -> Dict[str, Any]:
        """
        Ajuda outro agente a aprender, usando mobilidade para explicar conceitos.
        Cangurus são bons em mostrar diferentes ângulos de um problema.
        """
        my_proficiency = self.get_knowledge_level(topic)
        learner_proficiency = learner.get_knowledge_level(topic)
        
        if my_proficiency <= learner_proficiency:
            return {
                "success": False,
                "reason": "Minha proficiência não é maior que a do aprendiz",
                "my_proficiency": my_proficiency,
                "learner_proficiency": learner_proficiency
            }
        
        # Canguru ensina com saltos entre conceitos relacionados
        teaching_effectiveness = min(1.0, (my_proficiency - learner_proficiency) * 0.8 + 0.5)
        
        improvement = teaching_effectiveness * 0.3  # Melhoria de até 30%
        
        return {
            "success": True,
            "teacher": self.agent_id,
            "learner": learner.agent_id,
            "topic": topic,
            "teaching_style": "saltos_conceituais_multiplos_angulos",
            "initial_proficiency": learner_proficiency,
            "final_proficiency": min(1.0, learner_proficiency + improvement),
            "improvement": improvement,
            "description": f"Canguru ajuda {learner.name} a ver {topic} de múltiplos ângulos, saltando entre conceitos relacionados",
            "timestamp": datetime.now().isoformat()
        }
    
    def __str__(self) -> str:
        return (f"🦘 Canguru({self.agent_id}) - {self.environment}\n"
                f"   Características: {', '.join(self.characteristics)}\n"
                f"   Habilidades Especiais: Salto({self.jump_power:.2f}), "
                f"Equilíbrio({self.tail_balance:.2f}), Mobilidade({self.mobility:.2f})")
