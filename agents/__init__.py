"""
Pacote de Agentes Animais - Todos os 21 agentes implementados
Cada agente representa um animal com características únicas de aprendizado e comportamento.
"""

from .leao import Leao as LeaoAgent
from .tigre import Tigre as TigreAgent
from .elefante import Elefante as ElefanteAgent
from .hipopotamo import HipoAgent
from .polvo import PolvoAgent
from .lobo import LoboAgent
from .tubarao import TubaraoAgent
from .orca import OrcaAgent
from .rinoceronte import RinoceronteAgent
from .falcao import FalcaoAgent
from .crocodilo import CrocodiloAgent
from .cavalo import CavaloAgent
from .gorila import GorilaAgent
from .ovelha import OvelhaAgent
from .carneiro import CarneiroAgent
from .coelho import CoelhoAgent
from .alce import AlceAgent
from .marlin import MarlinAgent
from .urso_pardo import UrsoPardoAgent
from .leopardo import LeopardoAgent
from .canguru import CanguruAgent
from .bisao import BisaoAgent

__all__ = [
    'LeaoAgent',      # 🦁 Líder, grupo: 0.95
    'TigreAgent',     # 🐅 Solitário, furtivo: 0.98
    'ElefanteAgent',  # 🐘 Inteligente, família: 0.92
    'HipoAgent',      # 🦛 Agressivo, territorial: 0.98
    'PolvoAgent',     # 🐙 Inteligência máxima, solo: 1.0
    'LoboAgent',      # 🐺 Estratégia em grupo: 0.95
    'TubaraoAgent',   # 🦈 Predador solitário: 0.90
    'OrcaAgent',      # 🐋 Estratégia pod: 0.98
    'RinoceronteAgent',  # 🦏 Força bruta: 0.80
    'FalcaoAgent',    # 🦅 Velocidade máxima: 0.99
    'CrocodiloAgent', # 🐊 Paciência extrema: 0.88
    'CavaloAgent',    # 🐎 Manada forte: 0.88
    'GorilaAgent',    # 🦍 Liderança silverback: 0.90
    'OvelhaAgent',    # 🐑 Segurança manada: 0.82
    'CarneiroAgent',  # 🐏 Combate impacto: 0.82
    'CoelhoAgent',    # 🐇 Fuga/alerta: 0.88
    'AlceAgent',      # 🦌 Solitário forte: 0.82
    'MarlinAgent',    # 🐟 Velocidade oceano: 0.90
    'UrsoPardoAgent', # 🐻 Força dominante: 0.85
    'LeopardoAgent',  # 🐆 Furtividade: 0.95
    'CanguruAgent',   # 🦘 Mobilidade/salto: 0.92
    'BisaoAgent',     # 🦬 Resistência/força bruta: 0.95
]

# Dicionário de todos os agentes para fácil acesso
ALL_AGENTS = {
    'leao': LeaoAgent,
    'tigre': TigreAgent,
    'elefante': ElefanteAgent,
    'hipopotamo': HipoAgent,
    'polvo': PolvoAgent,
    'lobo': LoboAgent,
    'tubarao': TubaraoAgent,
    'orca': OrcaAgent,
    'rinoceronte': RinoceronteAgent,
    'falcao': FalcaoAgent,
    'crocodilo': CrocodiloAgent,
    'cavalo': CavaloAgent,
    'gorila': GorilaAgent,
    'ovelha': OvelhaAgent,
    'carneiro': CarneiroAgent,
    'coelho': CoelhoAgent,
    'alce': AlceAgent,
    'marlin': MarlinAgent,
    'urso_pardo': UrsoPardoAgent,
    'leopardo': LeopardoAgent,
    'canguru': CanguruAgent,
    'bisao': BisaoAgent,
}
