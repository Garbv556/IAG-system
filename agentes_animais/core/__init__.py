"""
Módulo Core do Sistema de Agentes Animais
Contém a IAG Central e classes base
"""

from .iag_central import IAGCentral
from .base_agent import AnimalAgent, State

__all__ = ['IAGCentral', 'AnimalAgent', 'State']
