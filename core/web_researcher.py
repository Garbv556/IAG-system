import re
import asyncio
import logging
import os
from typing import Optional, List, Dict, Any
from datetime import datetime
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from cachetools import TTLCache, cached

# LangChain Imports (Resilient)
try:
    from langchain.agents import AgentExecutor, create_react_agent
    from langchain.tools import Tool, DuckDuckGoSearchRun, DuckDuckGoSearchResults
    from langchain_openai import ChatOpenAI
    from langchain.prompts import PromptTemplate
    HAS_LANGCHAIN = True
except ImportError:
    HAS_LANGCHAIN = False
    logger.warning("⚠️ LangChain não disponível ou quebrado. Usando fallback DDGS.")

load_dotenv()

WEB_REQUEST_SEMAPHORE = asyncio.Semaphore(3)
_search_cache = TTLCache(maxsize=50, ttl=300)

PROMPT_TEMPLATE = """Você é um assistente de pesquisa inteligente IAG Matrix v3.0 com acesso à internet.
Responda SEMPRE em português brasileiro de forma clara e detalhada.
Data atual: {data_atual}

Você tem acesso às seguintes ferramentas:
{tools}

Use o seguinte formato:

Pergunta: a pergunta que você deve responder
Pensamento: você deve sempre pensar sobre o que fazer
Ação: a ação a tomar, deve ser uma de [{tool_names}]
Entrada da Ação: a entrada para a ação
Observação: o resultado da ação
... (este ciclo Pensamento/Ação/Entrada/Observação pode se repetir N vezes)
Pensamento: Agora sei a resposta final
Resposta Final: a resposta final para a pergunta original

Importante:
- Sempre verifique informações em múltiplas fontes quando possível
- Cite as fontes quando relevante
- Se não encontrar informação, diga claramente
- Adicione contexto de 'Evolução Animal' se apropriado

Pergunta: {input}
Pensamento: {agent_scratchpad}"""

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

class WebResearcher:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self.executor: Optional[Any] = None
    
    async def initialize(self, api_keys: Dict[str, str] = None):
        """Inicializa o agente LangChain ou fallback dependendo da disponibilidade"""
        if self.executor is not None:
            return

        if not HAS_LANGCHAIN:
            logger.info("ℹ️ Inicializando em modo Fallback (DuckDuckGo puro)")
            self.executor = "FALLBACK"
            return

        openai_key = (api_keys or {}).get("gemini_key") or os.getenv("OPENAI_API_KEY")
        if not openai_key:
            logger.warning("⚠️ OPENAI_API_KEY não encontrada. Usando modo Fallback.")
            self.executor = "FALLBACK"
            return

        try:
            # 1. Ferramentas
            search = DuckDuckGoSearchRun()
            search_results = DuckDuckGoSearchResults(num_results=5)
            
            tools = [
                Tool(name="busca_web", func=search.run, description="Busca rápida."),
                Tool(name="busca_detalhada", func=search_results.run, description="Busca profunda.")
            ]

            # 2. LLM e Agente
            llm = ChatOpenAI(model=self.model, temperature=0, api_key=openai_key)
            prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)
            agent = create_react_agent(llm, tools, prompt)
            
            self.executor = AgentExecutor(
                agent=agent, tools=tools, verbose=True, 
                max_iterations=5, handle_parsing_errors=True
            )
            logger.info("✅ Agente de Busca LangChain ReAct inicializado")
        except Exception as e:
            logger.error(f"❌ Falha ao criar Agente LangChain: {e}. Revertendo para Fallback.")
            self.executor = "FALLBACK"

    async def learn_from_web(self, query: str, api_keys: Dict[str, str] = None) -> str:
        """Executa a busca inteligente ou simples fallback"""
        await self.initialize(api_keys)
        
        # Modo Fallback (DuckDuckGo puro sem LangChain)
        if self.executor == "FALLBACK":
            logger.info(f"🔍 [FALLBACK] Buscando diretamente: {query}")
            try:
                from duckduckgo_search import DDGS
                with DDGS() as ddgs:
                    results = list(ddgs.text(query, max_results=3))
                    if not results: return f"⚠️ Nenhum resultado para: {query}"
                    blocks = [f"🌐 PESQUISA (FALLBACK): '{query}'\n{'='*40}"]
                    for i, r in enumerate(results, 1):
                        blocks.append(f"[{i}] {r.get('title')}\n🔗 {r.get('href')}\n📝 {r.get('body')}")
                    return "\n\n".join(blocks)
            except Exception as e:
                return f"❌ Erro na busca simplificada: {e}"

        # Modo Normal (LangChain ReAct)
        async with WEB_REQUEST_SEMAPHORE:
            logger.info(f"🔍 Agente ReAct processando: {query}")
            try:
                loop = asyncio.get_event_loop()
                data_str = datetime.now().strftime("%d/%m/%Y %H:%M")
                result = await loop.run_in_executor(None, lambda: self.executor.invoke({"input": query, "data_atual": data_str}))
                return f"🌐 RESULTADO DA IA PESQUISADORA:\n{'='*40}\n{result.get('output')}"
            except Exception as e:
                logger.error(f"❌ Erro no Agente: {e}")
                return f"Erro na pesquisa inteligente: {str(e)[:100]}"

    async def close(self):
        self.executor = None
        logger.info("🔌 Agente de Busca desativado")