#!/usr/bin/env python3
"""
Demonstração do Sistema de Agentes Animais
Mostra como os agentes aprendem e colaboram entre si
"""

import sys
sys.path.insert(0, '/workspace')

from agentes_animais import IAGCentral, Leao, Tigre, Elefante, State


def main():
    print("=" * 60)
    print("🦁 SISTEMA DE AGENTES ANIMAIS - DEMONSTRAÇÃO 🦁")
    print("=" * 60)
    
    # Criar IAG Central
    print("\n[1] Inicializando IAG Central...")
    iag = IAGCentral()
    print(f"✓ {iag}")
    
    # Criar agentes
    print("\n[2] Criando agentes animais...")
    leao = Leao("agent_001", iag)
    tigre = Tigre("agent_002", iag)
    elefante = Elefante("agent_003", iag)
    
    # Registrar agentes na IAG
    print("\n[3] Registrando agentes na IAG...")
    iag.register_agent("agent_001", leao)
    iag.register_agent("agent_002", tigre)
    iag.register_agent("agent_003", elefante)
    
    # Mostrar status inicial
    print("\n[4] Status inicial dos agentes:")
    print("-" * 60)
    for agent_id, agent in iag.agents.items():
        status = agent.get_status()
        print(f"\n{agent.animal_name.upper()} ({agent.species})")
        print(f"  Estado: {status['state']}")
        print(f"  Adaptação Solo: {status['adaptation_solo']:.2f}")
        print(f"  Adaptação Grupo: {status['adaptation_group']:.2f}")
        print(f"  Inteligência: {status['intelligence']:.2f}")
        print(f"  Características: {', '.join(status['characteristics'])}")
    
    # Simular aprendizado de Mandarim
    print("\n" + "=" * 60)
    print("[5] TAREFA DE APRENDIZADO: MANDARIM")
    print("=" * 60)
    
    conteudo_mandarim = {
        'basico': 'Nǐ hǎo (Olá), Xièxiè (Obrigado)',
        'gramatica': 'Estrutura sujeito-verbo-objeto',
        'vocabulario': ['mao (gato)', 'gou (cão)', 'ren (pessoa)']
    }
    
    print("\nDistribuindo conteúdo para todos os agentes...")
    iag.distribute_learning_task("mandarim", conteudo_mandarim)
    
    # Sessão de colaboração
    print("\n" + "=" * 60)
    print("[6] SESSÃO DE COLABORAÇÃO")
    print("=" * 60)
    iag.facilitate_collaboration("mandarim")
    
    # Testar comunicação entre agentes
    print("\n" + "=" * 60)
    print("[7] COMUNICAÇÃO ENTRE AGENTES")
    print("=" * 60)
    
    print("\nLeão enviando mensagem para Tigre:")
    iag.send_direct_message("agent_002", "Vamos caçar juntos!", "agent_001")
    
    print("\nElefante enviando mensagem para todos:")
    iag.broadcast_message("Precisamos nos proteger!", "agent_003")
    
    # Mudar estados
    print("\n" + "=" * 60)
    print("[8] MUDANÇA DE ESTADOS")
    print("=" * 60)
    
    print("\nColocando Leão em grupo:")
    leao.set_state(State.GROUP)
    
    print("\nColocando Tigre sozinho:")
    tigre.set_state(State.SOLO)
    
    print("\nColocando Elefante em grupo:")
    elefante.set_state(State.GROUP)
    
    # Mais aprendizado com estados diferentes
    print("\n" + "=" * 60)
    print("[9] NOVO APRENDIZADO COM ESTADOS DIFERENTES")
    print("=" * 60)
    
    print("\nAprendendo Python avançado:")
    leao.learn("python_avancado", {"decoradores": "syntax", "generators": "yield"})
    tigre.learn("python_avancado", {"decoradores": "syntax", "generators": "yield"})
    elefante.learn("python_avancado", {"decoradores": "syntax", "generators": "yield"})
    
    # Colaboração em Python
    print("\nColaboração em Python avançado:")
    iag.facilitate_collaboration("python_avancado")
    
    # Status final
    print("\n" + "=" * 60)
    print("[10] STATUS FINAL")
    print("=" * 60)
    
    print(f"\n{iag}")
    print("\nConhecimento adquirido:")
    for agent_id, agent in iag.agents.items():
        status = agent.get_status()
        print(f"\n{agent.animal_name}:")
        print(f"  Conhecimento: {status['knowledge_summary']}")
        print(f"  Mensagens recebidas: {status['messages_count']}")
    
    print("\n" + "=" * 60)
    print("✅ DEMONSTRAÇÃO CONCLUÍDA!")
    print("=" * 60)


if __name__ == "__main__":
    main()
