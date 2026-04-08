#!/usr/bin/env python3
"""
Script para iniciar o servidor web dos Agentes Animais.
Basta executar: python start_web.py
Depois acesse: http://localhost:8000
"""

import sys
import os

# Adicionar o workspace ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from web.server import app
import uvicorn

if __name__ == "__main__":
    print("=" * 60)
    print("SISTEMA DE AGENTES ANIMAIS - IAG")
    print("=" * 60)
    print()
    print("Iniciando servidor web...")
    print()
    print("Acesse no navegador:")
    print("   -> http://localhost:8000")
    print("   -> http://127.0.0.1:8000")
    print()
    print("Funcionalidades:")
    print("   * Visualize 22 agentes animais em tempo real")
    print("   * Inicie sessões de aprendizado")
    print("   * Veja os agentes aprendendo individualmente")
    print("   * Acompanhe a colaboração")
    print("   * Observe conversas entre todos os agentes")
    print()
    print("Para parar: Pressione Ctrl+C")
    print("=" * 60)
    print()
    
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
