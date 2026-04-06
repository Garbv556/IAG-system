"""
Sistema de Agentes Animais Conectados à IAG Central

Este pacote implementa um sistema de agentes baseados em animais,
cada um com características únicas, conectados a uma Inteligência
Artificial Central (IAG).

Características:
- Cada agente representa um animal com comportamento único
- Todos sabem o básico de linguagens de programação
- Aprendizado individual e coletivo
- Colaboração entre agentes (mais proficientes ajudam menos proficientes)
- Conexão total através da IAG Central
"""

__version__ = "1.0.0"
__author__ = "Animal Agents System"

from .core import IAGCentral, AnimalAgent, State
from .agents import (
    LeaoAgent, TigreAgent, ElefanteAgent, HipoAgent, PolvoAgent, LoboAgent,
    TubaraoAgent, OrcaAgent, RinoceronteAgent, FalcaoAgent,
    CrocodiloAgent, CavaloAgent, GorilaAgent, OvelhaAgent,
    CarneiroAgent, CoelhoAgent, AlceAgent, MarlinAgent,
    UrsoPardoAgent, LeopardoAgent, CanguruAgent, BisaoAgent
)

__all__ = [
    'IAGCentral',
    'AnimalAgent', 
    'State',
    'LeaoAgent',
    'TigreAgent',
    'ElefanteAgent',
    'HipoAgent',
    'PolvoAgent',
    'LoboAgent',
    'TubaraoAgent',
    'OrcaAgent',
    'RinoceronteAgent',
    'FalcaoAgent',
    'CrocodiloAgent',
    'CavaloAgent',
    'GorilaAgent',
    'OvelhaAgent',
    'CarneiroAgent',
    'CoelhoAgent',
    'AlceAgent',
    'MarlinAgent',
    'UrsoPardoAgent',
    'LeopardoAgent',
    'CanguruAgent',
    'BisaoAgent'
]
