"""
Módulo WebResearcher - Acesso inteligente à internet para agentes IAG
Versão: 2.0 (Assíncrona e Resiliente)
"""

import re
import asyncio
import logging
from typing import Optional
from urllib.parse import quote_plus

import httpx
from duckduckgo_search import DDGS
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from cachetools import TTLCache, cached

# Configuração de logging
logger = logging.getLogger(__name__)

# =============================================================================
# CONFIGURAÇÕES GLOBAIS
# =============================================================================

# Limite de requisições web simultâneas (evita sobrecarga)
WEB_REQUEST_SEMAPHORE = asyncio.Semaphore(3)

# Cache para resultados de busca (TTL: 5 minutos)
_search_cache = TTLCache(maxsize=50, ttl=300)

# Headers para parecer um navegador real
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
}

# =============================================================================
# CLASSE WebResearcher
# =============================================================================

class WebResearcher:
    """
    Pesquisador web assíncrono para agentes IAG.
    
    Funcionalidades:
    - Busca via DuckDuckGo (sem API key)
    - Scraping assíncrono de páginas com httpx
    - Rate limiting e retry automático
    - Cache inteligente de resultados de busca
    - Limpeza e extração de texto de HTML
    """
    
    def __init__(self, timeout: float = 15.0, max_retries: int = 3):
        """
        Inicializa o WebResearcher.
        
        Args:
            timeout: Timeout em segundos para requisições HTTP
            max_retries: Número máximo de tentativas para operações falhas
        """
        self.timeout = timeout
        self.max_retries = max_retries
        self.http_client: Optional[httpx.AsyncClient] = None
        
    async def __aenter__(self):
        """Suporte a async context manager."""
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Fecha o cliente HTTP ao sair do contexto."""
        await self.close()
    
    async def initialize(self):
        """Inicializa o cliente HTTP assíncrono."""
        if self.http_client is None:
            self.http_client = httpx.AsyncClient(
                timeout=self.timeout,
                follow_redirects=True,
                headers=DEFAULT_HEADERS,
                http2=True  # Melhor performance
            )
            logger.info("🌐 WebResearcher inicializado")
    
    async def close(self):
        """Fecha o cliente HTTP e libera recursos."""
        if self.http_client:
            await self.http_client.aclose()
            self.http_client = None
            logger.info("🔌 WebResearcher fechado")
    
    # =========================================================================
    # MÉTODO PRINCIPAL: learn_from_web
    # =========================================================================
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.RequestError, httpx.TimeoutException)),
        before_sleep=lambda retry_state: logger.warning(
            f"Tentativa {retry_state.attempt_number} falhou, retrying..."
        )
    )
    async def learn_from_web(self, query: str, max_results: int = 3) -> str:
        """
        Pesquisa na internet e retorna conhecimento estruturado.
        
        Args:
            query: Termo de busca
            max_results: Número máximo de resultados a processar (1-5 recomendado)
            
        Returns:
            String com conteúdo extraído dos resultados
        """
        await self.initialize()  # Garante que o client está pronto
        
        async with WEB_REQUEST_SEMAPHORE:  # Controla concorrência global
            logger.info(f"🔍 [WEB] Buscando: '{query}' (max_results={max_results})")
            
            try:
                # 1. Busca no DuckDuckGo (com cache)
                search_results = self._cached_search(query, max_results)
                
                if not search_results:
                    return f"⚠️ Nenhum resultado encontrado para: '{query}'"
                
                # 2. Processa cada resultado assincronamente
                knowledge_blocks = []
                
                for i, result in enumerate(search_results, 1):
                    title = result.get('title', 'Sem título')
                    url = result.get('href', '')
                    snippet = result.get('body', '')
                    
                    block = [f"\n{'='*60}", f"📄 RESULTADO {i}/{len(search_results)}"]
                    block.append(f"🔗 Título: {title}")
                    block.append(f"🌐 URL: {url}")
                    block.append(f"📝 Resumo: {snippet}")
                    
                    # 3. Scraping opcional do conteúdo completo (se URL válida)
                    if url and self._is_scrapable_url(url):
                        content = await self._scrape_url(url)
                        if content:
                            block.append(f"\n📖 Conteúdo extraído ({len(content)} chars):")
                            block.append(content[:2000] + ("..." if len(content) > 2000 else ""))
                    
                    knowledge_blocks.append("\n".join(block))
                    
                    # Rate limiting entre requisições
                    await asyncio.sleep(0.5)
                
                # 4. Formata resposta final
                header = [
                    f"🌐 PESQUISA WEB: '{query}'",
                    f"📊 Resultados: {len(search_results)} | Timestamp: {asyncio.get_event_loop().time():.0f}",
                    f"{'-'*60}"
                ]
                
                return "\n".join(header + knowledge_blocks)
                
            except Exception as e:
                logger.error(f"❌ Erro em learn_from_web('{query}'): {type(e).__name__}: {e}")
                return f"⚠️ Erro ao pesquisar '{query}': {str(e)[:200]}"
    
    # =========================================================================
    # MÉTODOS AUXILIARES
    # =========================================================================
    
    @cached(cache=_search_cache)
    def _cached_search(self, query: str, max_results: int) -> list:
        """
        Busca no DuckDuckGo com cache TTL.
        Executada em thread síncrona (DDGS não é async).
        """
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=max_results))
                logger.debug(f"✅ DuckDuckGo: {len(results)} resultados para '{query}'")
                return results
        except Exception as e:
            logger.warning(f"⚠️ Falha na busca DuckDuckGo: {e}")
            return []
    
    async def _scrape_url(self, url: str) -> str:
        """
        Faz scraping assíncrono de uma URL e extrai texto limpo.
        """
        if not self.http_client:
            await self.initialize()
        
        try:
            response = await self.http_client.get(url)
            response.raise_for_status()
            
            html = response.text
            return self._clean_html(html)
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 403:
                logger.debug(f"🚫 Acesso negado (403) para {url}")
            else:
                logger.warning(f"⚠️ HTTP {e.response.status_code} para {url}")
            return ""
        except httpx.RequestError as e:
            logger.debug(f"🔌 Erro de rede em {url}: {e}")
            return ""
        except Exception as e:
            logger.debug(f"❌ Erro inesperado em {url}: {e}")
            return ""
    
    def _clean_html(self, html: str) -> str:
        """
        Limpa HTML e extrai texto legível.
        """
        # Remove scripts, styles e elementos não visíveis
        html = re.sub(r'<(script|style|nav|footer|header)[^>]*>.*?</\1>', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove tags HTML restantes
        text = re.sub(r'<[^>]+>', ' ', html)
        
        # Normaliza espaços e quebras de linha
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Limita tamanho para evitar memória excessiva
        return text.strip()[:5000]
    
    def _is_scrapable_url(self, url: str) -> bool:
        """
        Verifica se uma URL é segura e apropriada para scraping.
        """
        if not url:
            return False
        
        # Bloqueia URLs potencialmente problemáticas
        blocked_patterns = [
            r'\.(pdf|jpg|jpeg|png|gif|zip|exe)$',  # Arquivos binários
            r'^(https?://)?(www\.)?(youtube|facebook|twitter|instagram)\.',  # Redes sociais
            r'login|signin|register|checkout',  # Páginas sensíveis
        ]
        
        for pattern in blocked_patterns:
            if re.search(pattern, url, re.I):
                return False
        
        # Permite apenas HTTP/HTTPS
        return url.startswith(('http://', 'https://'))
    
    # =========================================================================
    # UTILITÁRIOS PÚBLICOS
    # =========================================================================
    
    async def search_only(self, query: str, max_results: int = 5) -> list[dict]:
        """
        Apenas busca no DuckDuckGo, sem scraping de conteúdo.
        Útil para listagens rápidas.
        """
        await self.initialize()
        return self._cached_search(query, max_results)
    
    async def fetch_url_content(self, url: str) -> str:
        """
        Faz scraping direto de uma URL específica.
        """
        await self.initialize()
        return await self._scrape_url(url)
    
    def get_stats(self) -> dict:
        """
        Retorna estatísticas do cache e estado atual.
        """
        return {
            "cache_size": len(_search_cache),
            "cache_max": _search_cache.maxsize,
            "cache_ttl": _search_cache.ttl,
            "semaphore_value": WEB_REQUEST_SEMAPHORE._value,
            "client_initialized": self.http_client is not None
        }

# =============================================================================
# FACTORY FUNCTION (para injeção de dependência no FastAPI)
# =============================================================================

async def get_web_researcher() -> WebResearcher:
    """
    Factory para injeção de dependência no FastAPI.
    Uso: researcher: WebResearcher = Depends(get_web_researcher)
    """
    researcher = WebResearcher()
    await researcher.initialize()
    try:
        yield researcher
    finally:
        await researcher.close()


# =============================================================================
# TESTE RÁPIDO (executar com: python -m core.web_researcher)
# =============================================================================

if __name__ == "__main__":
    import sys
    
    async def main():
        query = sys.argv[1] if len(sys.argv) > 1 else "Python async programming"
        
        async with WebResearcher() as researcher:
            print(f"\n🚀 Testando WebResearcher com: '{query}'\n")
            result = await researcher.learn_from_web(query, max_results=2)
            print(result)
            print(f"\n📊 Stats: {researcher.get_stats()}")
    
    asyncio.run(main())
