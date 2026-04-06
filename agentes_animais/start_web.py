#!/usr/bin/env python3
"""
Script para iniciar o servidor web dos Agentes Animais.
Basta executar: python start_web.py
Depois acesse: http://localhost:8000
"""

import sys
import os

# Adicionar o workspace ao path
sys.path.insert(0, '/workspace')

from agentes_animais.web.server import app
import uvicorn

if __name__ == "__main__":
    print("=" * 60)
    print("🦁 SISTEMA DE AGENTES ANIMAIS - IAG")
    print("=" * 60)
    print()
    print("🚀 Iniciando servidor web...")
    print()
    print("📍 Acesse no navegador:")
    print("   👉 http://localhost:8000")
    print("   👉 http://127.0.0.1:8000")
    print()
    print("✨ Funcionalidades:")
    print("   • Visualize 22 agentes animais em tempo real")
    print("   • Inicie sessões de aprendizado (ex: mandarim)")
    print("   • Veja os agentes aprendendo individualmente")
    print("   • Acompanhe a colaboração (mais proficiente ajuda o menos)")
    print("   • Observe conversas entre todos os agentes")
    print()
    print("🛑 Para parar: Pressione Ctrl+C")
    print("=" * 60)
    print()
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
