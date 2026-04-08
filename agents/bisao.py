"""
Agente Bisão - 🦬
Espécie: Bisão-americano (Bison bison)
Ambiente: Planícies e campos da América do Norte

Características:
- Massa enorme + força bruta
- Alta resistência
- Capacidade de corrida surpreendente

Comportamento:
- Sozinho: Machos podem ser extremamente agressivos
- Em grupo (manada): Proteção coletiva, forte instinto de grupo

Ataques/Defesa:
- Investida em alta velocidade
- Golpes com a cabeça e chifres
- Pisoteamento
- Contra predador/rival: Enfrenta diretamente, não recua facilmente
- Em grupo: formam barreira defensiva
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import random
from core.base_agent import AnimalAgent


class BisaoAgent(AnimalAgent):
    """Agente representando um Bisão-americano."""

    def __init__(self, agent_id: str = "bisao_001"):
        super().__init__(agent_id=agent_id)

        # Características específicas do Bisão
        self.resistance = 0.95  # Alta resistência
        self.brute_force = 0.92  # Força bruta extrema
        self.charge_speed = 0.85  # Corrida surpreendente para o tamanho
        self.group_defense = 0.95  # Proteção coletiva poderosa

    def _set_animal_characteristics(self) -> None:
        """Define as características específicas do Bisão."""
        self.species = "Bisão-americano (Bison bison)"
        self.environment = "Planícies e campos da América do Norte"
        self.characteristics = [
            "Massa enorme + força bruta",
            "Alta resistência",
            "Capacidade de corrida surpreendente"
        ]
        self.solo_behavior = "Machos podem ser extremamente agressivos"
        self.group_behavior = "Proteção coletiva, forte instinto de grupo, formam barreira defensiva"
        self.attacks = [
            "Investida em alta velocidade",
            "Golpes com a cabeça e chifres",
            "Pisoteamento"
        ]
        self.rival_response = "Enfrenta diretamente, não recua facilmente, barreira defensiva em grupo"

        # Fatores de adaptação
        self.adaptation_solo = 0.75  # Agressivo sozinho
        self.adaptation_group = 0.95  # Excelente em grupo com proteção coletiva
        self.intelligence = 0.78
        self.aggressiveness = 0.85  # Alta agressividade quando ameaçado
        self.stealth = 0.3  # Baixa furtividade devido ao tamanho
        self.strength = 0.95  # Força extrema
        self.speed = 0.75  # Velocidade boa para o tamanho

        # ═══ DOUTRINA TÁTICA ═══
        self.solo_tactics = ['Resista e persista', 'Mantenha posição firme']
        self.collective_tactics = ['Mova-se como unidade', 'Proteja os flancos do grupo']
        self.threat_tactics = ['Carga frontal coordenada', 'Nunca quebre a formação']

    def get_special_abilities(self) -> Dict[str, float]:
        """Retorna habilidades especiais do Bisão."""
        return {
            "resistance": self.resistance,
            "brute_force": self.brute_force,
            "charge_speed": self.charge_speed,
            "group_defense": self.group_defense,
            "trample_power": 0.90  # Poder de pisoteamento
        }

    def adapt_learning(self, topic: str, context: str = "solo") -> Dict[str, Any]:
        """
        Adapta o aprendizado baseado no contexto (solo ou grupo).
        Bisões aprendem melhor em grupo devido à sensação de proteção.
        """
        base_proficiency = self.get_overall_programming_skill()

        if context == "solo":
            # Sozinho: mais agressivo mas menos focado
            adaptation_factor = 0.70
            strategy = "aprendizado_agressivo"
            description = "Aprendendo de forma intensa mas menos focada, pronto para defender território"
        else:  # group
            # Em grupo: proteção coletiva permite foco total
            adaptation_factor = 0.95
            strategy = "aprendizado_manada_protegida"
            description = "Aprendendo com confiança, protegido pela manada, foco máximo"

        final_proficiency = min(1.0, base_proficiency * adaptation_factor)

        learning_result = {
            "topic": topic,
            "proficiency": final_proficiency,
            "strategy": strategy,
            "description": description,
            "context": context,
            "timestamp": datetime.now().isoformat()
        }

        self.learning_history.append(learning_result)
        return learning_result

    def special_ability(self, target: Optional[Any] = None, **kwargs) -> Dict[str, Any]:
        """
        Habilidade especial: Investida Poderosa
        O bisão realiza uma investida em alta velocidade com força bruta extrema.
        """
        ability_name = "Investida Poderosa"
        description = "O bisão acelera em alta velocidade e usa sua massa enorme para impactar o alvo."
        
        effectiveness = self.brute_force * self.charge_speed
        
        is_alone = kwargs.get('is_alone', True)
        if not is_alone:
            effectiveness *= self.group_defense
            description += " A manada oferece cobertura durante a investida."
        
        result = {
            "ability": ability_name,
            "description": description,
            "effectiveness": effectiveness,
            "target": str(target) if target else "Nenhum",
            "used_by": self.animal_name
        }
        
        return result

    def defensive_stance(self, allies: List[Any] = None) -> Dict[str, Any]:
        """
        Formação defensiva: Barreira Imparável
        O bisão forma uma barreira defensiva com outros aliados.
        """
        if allies is None:
            allies = []

        ability_name = "Barreira Imparável"
        description = "O bisão assume posição defensiva, pronto para investir contra qualquer ameaça."

        defense_power = self.resistance * self.brute_force

        if allies:
            total_allies = len(allies) + 1  # +1 para si mesmo
            defense_power *= (1 + 0.15 * total_allies)
            description = f"Formação defensiva com {total_allies} membros! Barreira quase impenetrável."
        else:
            description = "Posição defensiva individual. Pronto para enfrentar qualquer ameaça!"

        return {
            "ability": ability_name,
            "description": description,
            "defense_power": min(defense_power, 2.0),
            "allies_count": len(allies),
            "used_by": self.animal_name
        }

    def communicate(self, message: str, recipients: List[Any] = None) -> Dict[str, Any]:
        """
        Comunicação do Bisão - direta, protetora e encorajadora.
        """
        if recipients is None:
            recipients = []

        prefixes = [
            "🦬 *Em tom grave e protetor*",
            "🦬 *Com voz firme*",
            "🦬 *Encorajando a manada*",
            "🦬 *Alertando sobre perigo*"
        ]

        prefix = random.choice(prefixes)

        if recipients:
            full_message = f"{prefix} Atenção manada: {message}"
        else:
            full_message = f"{prefix} {message}"

        return {
            "from": self.animal_name,
            "message": full_message,
            "recipients_count": len(recipients),
            "tone": "protetor e firme"
        }

    def collaborate(self, task: str, partners: List[Any]) -> Dict[str, Any]:
        """
        Colaboração em tarefas.
        Bisões são excelentes em defesa coletiva e trabalhos que requerem força bruta.
        """
        if not partners:
            return {
                "task": task,
                "status": "incompleto",
                "reason": "Bisões trabalham melhor em grupo",
                "efficiency": 0.6
            }

        collaboration_score = 0.85 + (0.05 * len(partners))
        collaboration_score = min(collaboration_score, 1.0)

        return {
            "task": task,
            "status": "concluído",
            "collaboration_score": collaboration_score,
            "partners_count": len(partners),
            "strategy": "Força bruta coordenada e proteção mútua",
            "efficiency": collaboration_score
        }

    def get_status_report(self) -> Dict[str, Any]:
        """
        Relatório de status detalhado do Bisão.
        """
        base_report = super().get_status_report()

        base_report.update({
            "specialty": "Resistência e Força Bruta",
            "combat_style": "Investida frontal + Pisoteamento",
            "group_role": "Tanque/Protetor da manada",
            "resistance_level": self.resistance,
            "brute_force_level": self.brute_force,
            "defensive_capability": self.group_defense
        })

        return base_report
