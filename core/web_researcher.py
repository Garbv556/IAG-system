"""
WebResearcher - Acesso assíncrono à internet
"""
import re
import asyncio
import logging
from typing import Optional
import httpx
from duckduckgo_search import DDGS
from tenacity import retry, stop_after_attempt, wait_exponential
from cachetools import TTLCache, cached

logger = logging.getLogger(__name__)

WEB_REQUEST_SEMAPHORE = asyncio.Semaphore(3)
_search_cache = TTLCache(maxsize=50, ttl=300)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

class WebResearcher:
    def __init__(self, timeout: float = 10.0):
        self.timeout = timeout
        self.http_client: Optional[httpx.AsyncClient] = None
    
    async def initialize(self):
        if self.http_client is None:
            self.http_client = httpx.AsyncClient(
                timeout=self.timeout,
                follow_redirects=True,
                headers=HEADERS
            )
            logger.info("[WEB] WebResearcher inicializado")
    
    async def close(self):
        if self.http_client:
            await self.http_client.aclose()
            self.http_client = None
            logger.info("[WEB] WebResearcher fechado")
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def learn_from_web(self, query: str, max_results: int = 3) -> str:
        await self.initialize()
        
        async with WEB_REQUEST_SEMAPHORE:
            logger.info(f"🔍 Buscando: {query}")
            
            try:
                # Na versão 8.1.1 o DDGS deve ser usado assim:
                results = await asyncio.to_thread(self._cached_search, query, max_results)
                
                if not results:
                    return f"⚠️ Nenhum resultado para: {query}"
                
                blocks = [f"🌐 PESQUISA: '{query}'\n{'='*60}"]
                
                for i, r in enumerate(results, 1):
                    block = f"\n[{i}] {r.get('title', 'Sem título')}"
                    block += f"\n🔗 {r.get('href', '')}"
                    block += f"\n📝 {r.get('body', '')}"
                    
                    url = r.get('href', '')
                    if url:
                        content = await self._scrape_url(url)
                        if content:
                            block += f"\n📖 Conteúdo: {content[:1000]}..."
                    
                    blocks.append(block)
                    await asyncio.sleep(0.5)
                
                return "\n".join(blocks)
                
            except Exception as e:
                logger.error(f"❌ Erro: {e}")
                return f"Erro na pesquisa: {str(e)[:200]}"
    
    @cached(cache=_search_cache)
    def _cached_search(self, query: str, max_results: int) -> list:
        try:
            with DDGS() as ddgs:
                return list(ddgs.text(query, max_results=max_results))
        except Exception as e:
            logger.warning(f"Falha na busca: {e}")
            return []
    
    async def _scrape_url(self, url: str) -> str:
        if not self.http_client:
            await self.initialize()
        
        try:
            response = await self.http_client.get(url)
            response.raise_for_status()
            
            html = response.text
            # Limpeza rápida
            text = re.sub(r'<(script|style|nav|footer)[^>]*>.*?</\1>', '', html, flags=re.DOTALL | re.IGNORECASE)
            text = re.sub(r'<.*?>', ' ', text)
            text = re.sub(r'\s+', ' ', text).strip()
            return text[:2000]
            
        except Exception:
            return ""
