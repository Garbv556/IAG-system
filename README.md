# 🦁 Sistema de Agentes Animais - IAG Central

## Visão Geral

Este projeto implementa um sistema de agentes baseados em animais, cada um com características únicas, conectados a uma **Inteligência Artificial Central (IAG)**.

## 🎯 Características Principais

### Cada Agente/Animal:
- ✅ Representa um animal com comportamento único baseado em características reais
- ✅ Possui conhecimento básico de linguagens de programação (Python, JavaScript, Java, C++, Go, Rust)
- ✅ Aprende individualmente e em grupo
- ✅ Tem consciência de adaptação (sozinho vs em grupo)
- ✅ Colabora com outros agentes (mais proficientes ajudam menos proficientes)
- ✅ Conecta-se à IAG Central e comunica-se com outros agentes

### IAG Central:
- 🧠 Coordena todos os agentes
- 📚 Distribui tarefas de aprendizado
- 🤝 Facilita colaboração entre agentes
- 💬 Gerencia comunicação (mensagens diretas e broadcast)
- 📊 Monitora status de todos os agentes

## 📁 Estrutura do Projeto

```
agentes_animais/
├── __init__.py           # Pacote principal
├── demo.py               # Demonstração do sistema
├── README.md             # Este arquivo
├── core/                 # Módulo central
│   ├── __init__.py
│   ├── iag_central.py    # Inteligência Artificial Central
│   └── base_agent.py     # Classe base para agentes
├── agents/               # Agentes animais
│   ├── __init__.py
│   ├── leao.py           # Agente Leão
│   ├── tigre.py          # Agente Tigre
│   └── elefante.py       # Agente Elefante
├── config/               # Configurações
└── utils/                # Utilitários
```

## 🦴 Animais Implementados

### 🦁 Leão
- **Espécie**: Leão-africano
- **Ambiente**: Savanas abertas
- **Características**: Força, domínio territorial, liderança
- **Sozinho**: Mais agressivo e instável
- **Em grupo**: Caça coordenada (pride)
- **Adaptação**: Solo 0.6 | Grupo 0.95

### 🐅 Tigre
- **Espécie**: Tigre-siberiano
- **Ambiente**: Florestas densas
- **Características**: Força + furtividade máxima
- **Sozinho**: Predador perfeito
- **Em grupo**: Não existe (solitário)
- **Adaptação**: Solo 0.98 | Grupo 0.1

### 🐘 Elefante
- **Espécie**: Elefante-africano
- **Ambiente**: Savanas
- **Características**: Força extrema + inteligência
- **Sozinho**: Machos perigosos
- **Em grupo**: Estrutura familiar forte
- **Adaptação**: Solo 0.7 | Grupo 0.95

## 🚀 Como Usar

### Executar Demonstração

```bash
cd /workspace
python agentes_animais/demo.py
```

### Uso Básico

```python
from agentes_animais import IAGCentral, Leao, Tigre, Elefante

# Criar IAG Central
iag = IAGCentral()

# Criar agentes
leao = Leao("agent_001", iag)
tigre = Tigre("agent_002", iag)
elefante = Elefante("agent_003", iag)

# Registrar na IAG
iag.register_agent("agent_001", leao)
iag.register_agent("agent_002", tigre)
iag.register_agent("agent_003", elefante)

# Distribuir aprendizado
iag.distribute_learning_task("mandarim", {"basico": "Nǐ hǎo"})

# Facilitar colaboração
iag.facilitate_collaboration("mandarim")

# Enviar mensagens
iag.send_direct_message("agent_002", "Vamos caçar!", "agent_001")
iag.broadcast_message("Atenção!", "agent_003")
```

## 🔄 Fluxo de Aprendizado Colaborativo

1. **Distribuição**: IAG distribui conteúdo para todos os agentes
2. **Aprendizado Individual**: Cada agente aprende conforme suas capacidades
3. **Avaliação**: IAG avalia proficiência de cada agente
4. **Colaboração**: Agente mais proficiente ajuda o menos proficiente
5. **Comunicação**: Agentes conversam no idioma/conteúdo aprendido

## 📊 Estados dos Agentes

- `SOLO`: Agente operando sozinho
- `GROUP`: Agente em grupo
- `LEARNING`: Agente aprendendo
- `COMMUNICATING`: Agente comunicando
- `HUNTING`: Agente caçando
- `RESTING`: Agente descansando

## 🔮 Próximos Passos (Animais Pendentes)

Os seguintes animais podem ser implementados seguindo o mesmo padrão:

- 🦛 Hipopótamo
- 🐙 Polvo
- 🐺 Lobo
- 🦈 Tubarão-branco
- 🐋 Orca
- 🦏 Rinoceronte
- 🦅 Falcão
- 🐊 Crocodilo
- 🐎 Cavalo
- 🦍 Gorila
- 🐑 Ovelha
- 🐏 Carneiro
- 🐇 Coelho
- 🦌 Alce
- 🐟 Marlin
- 🐻 Urso-pardo
- 🐆 Leopardo

## 📝 Criando Novo Agente Animal

```python
from ..core.base_agent import AnimalAgent, State

class NovoAnimal(AnimalAgent):
    def _set_animal_characteristics(self) -> None:
        self.species = "Nome da espécie"
        self.environment = "Ambiente"
        self.characteristics = ["Caract1", "Caract2"]
        self.solo_behavior = "Comportamento sozinho"
        self.group_behavior = "Comportamento em grupo"
        self.attacks = ["Ataque1", "Ataque2"]
        self.rival_response = "Resposta a rivais"
        
        # Fatores de adaptação (0-1)
        self.adaptation_solo = 0.5
        self.adaptation_group = 0.5
        
        # Atributos (0-1)
        self.intelligence = 0.5
        self.aggressiveness = 0.5
        self.stealth = 0.5
        self.strength = 0.5
        self.speed = 0.5
```

## 👥 Autores

Sistema desenvolvido para demonstrar conceitos de:
- Agentes inteligentes
- Aprendizado colaborativo
- Comportamento emergente
- Sistemas multi-agentes

## 📄 Licença

MIT License
