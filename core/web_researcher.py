"""
WebResearcher - Acesso assíncrono à internet
Versão 2.2 - Multi-Thread Compatibility (DDGS v8.1.1)
"""
import re
import asyncio
import logging
import traceback
from typing import Optional, List, Dict
import httpx
from duckduckgo_search import DDGS
from tenacity import retry, stop_after_attempt, wait_exponential
from cachetools import TTLCache, cached

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# SEMAPHORE: Limita o paralelismo de rede
WEB_REQUEST_SEMAPHORE = asyncio.Semaphore(3)

# CACHE COM TTL
_search_cache = TTLCache(maxsize=100, ttl=600)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

class WebResearcher:
    def __init__(self, timeout: float = 15.0):
        self.timeout = timeout
        self.http_client: Optional[httpx.AsyncClient] = None
    
    async def initialize(self):
        """Inicializa cliente HTTP assíncrono"""
        if self.http_client is None:
            self.http_client = httpx.AsyncClient(
                timeout=self.timeout,
                follow_redirects=True,
                headers=HEADERS,
                http2=True
            )
            logger.info("[WEB] Motor httpx v2.2 inicializado.")
    
    async def close(self):
        """Fecha conexões"""
        if self.http_client:
            await self.http_client.aclose()
            self.http_client = None
            logger.info("[WEB] Motor desconectado.")
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def learn_from_web(self, query: str, max_results: int = 3) -> str:
        """Busca REAL utilizando isolamento em Thread para evitar bloqueio do loop"""
        await self.initialize()
        
        async with WEB_REQUEST_SEMAPHORE:
            logger.info(f"🔍 [MATRIX-SEARCH] Varrendo a rede: {query}")
            
            try:
                # 1. Busca via Thread (DDGS v8 é síncrono)
                results = await asyncio.to_thread(self._sync_search, query, max_results)
                
                if not results:
                    logger.warning(f"⚠️ [WEB] Busca retornou vazia para '{query}'.")
                    return f"⚠️ Nenhum dado capturado para: {query}"
                
                # 2. Processamento
                blocks = [f"🌐 CONHECIMENTO FILTRADO: '{query}'\n{'='*60}"]
                
                for i, r in enumerate(results, 1):
                    url = r.get('href', '')
                    title = r.get('title', 'Fonte Anônima')
                    snippet = r.get('body', '')
                    
                    block = [
                        f"\n📄 [FONTE {i}] {title}",
                        f"🌐 ORIGEM: {url}",
                        f"📝 RESUMO: {snippet}"
                    ]
                    
                    # 3. Scraping Assíncrono do Conteúdo Bruto
                    if url and self._is_scrapable(url):
                        content = await self._scrape_url(url)
                        if content:
                            block.append(f"📖 CONTEÚDO EXTRAÍDO: {content[:1000]}...")
                    
                    blocks.append("\n".join(block))
                    await asyncio.sleep(0.3)
                
                return "\n".join(blocks)
                
            except Exception as e:
                logger.error(f"❌ [WEB-FAIL] {e}")
                traceback.print_exc()
                return f"❌ Falha crítica na Matrix de Dados: {str(e)[:150]}"

    def _sync_search(self, query: str, max_results: int) -> List[Dict]:
        """Core de busca síncrona isolado em thread"""
        try:
            with DDGS() as ddgs:
                # A versão 8.1.1 retorna uma lista ou gerador
                return list(ddgs.text(query, max_results=max_results))
        except Exception as e:
            logger.error(f"⚠️ [DDGS-ERROR] {e}")
            return []
    
    async def _scrape_url(self, url: str) -> str:
        """Extração de alta performance via httpx"""
        if not self.http_client: await self.initialize()
        try:
            response = await self.http_client.get(url)
            if response.status_code == 200:
                html = response.text
                # Cleanup robusto
                text = re.sub(r'<(script|style|nav|footer|form|header)[^>]*>.*?</\1>', '', html, flags=re.DOTALL | re.IGNORECASE)
                text = re.sub(r'<[^>]+>', ' ', text)
                text = re.sub(r'\s+', ' ', text).strip()
                return text[:5000]
            return ""
        except:
            return ""

    def _is_scrapable(self, url: str) -> bool:
        blocked = ['youtube.com', 'facebook.com', 'twitter.com', 'instagram.com', '.pdf', '.zip']
        return not any(domain in url.lower() for domain in blocked)

# =============================================================================
# BOOT DIAGNÓSTICO
# =============================================================================

if __name__ == "__main__":
    async def test():
        q = "Hacking Etico"
        researcher = WebResearcher()
        print(f"\n🚀 TESTE DE MOTOR v2.2 (Sincronia Global): {q}...\n")
        res = await researcher.learn_from_web(q, max_results=2)
        print(res)
        await researcher.close()
    
    asyncio.run(test())
