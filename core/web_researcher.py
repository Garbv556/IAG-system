import urllib.request
import urllib.parse
import re
from duckduckgo_search import DDGS
from tenacity import retry, stop_after_attempt, wait_exponential
from functools import lru_cache
import time

class WebResearcher:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    def _scrape_url(self, url: str) -> str:
        """Acessa a URL e extrai o texto limpo da página."""
        try:
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('utf-8', errors='ignore')
                
                # Cleanup básico de HTML via Regex
                html = re.sub(r'<(script|style).*?>.*?</\1>', '', html, flags=re.DOTALL)
                text = re.sub(r'<.*?>', ' ', html)
                text = re.sub(r'\s+', ' ', text).strip()
                
                return text[:5000]
        except Exception as e:
            # Print limpo sem emojis
            print(f"[SCRAPER] Erro ao ler {url}: {str(e).encode('ascii', 'ignore').decode('ascii')}")
            return ""

    @lru_cache(maxsize=100)
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def learn_from_web(self, query: str, max_results: int = 3) -> str:
        """
        Realiza uma pesquisa real e lê o conteúdo dos principais sites.
        """
        print(f"[WEB-RESEARCHER] Iniciando busca profunda por: {query}")
        try:
            results = []
            with DDGS() as ddgs:
                search_results = list(ddgs.text(query, max_results=max_results))
                
                for i, r in enumerate(search_results):
                    url = r.get('href', '')
                    title = r.get('title', 'N/A')
                    snippet = r.get('body', '')
                    
                    print(f"[WEB-RESEARCHER] Lendo site {i+1}: {title.encode('ascii', 'ignore').decode('ascii')}")
                    
                    # Tentar ler o conteúdo real do site
                    full_text = self._scrape_url(url)
                    content = full_text if len(full_text) > 200 else snippet
                    
                    results.append(
                        f"--- FONTE {i+1}: {title} ---\n"
                        f"URL: {url}\n"
                        f"CONTEÚDO EXTRAÍDO:\n{content}\n"
                    )
                    time.sleep(0.5)
            
            if not results:
                return "A busca não retornou dados relevantes no momento."
            
            return "\n".join(results)
            
        except Exception as e:
            print(f"❌ [WEB-RESEARCHER ERROR] {e}")
            return f"Erro na conexão com a rede global: {str(e)}"

    def estimate_data_quality(self, content: str) -> float:
        """Estima a qualidade dos dados baseada na densidade de informação."""
        if not content or len(content) < 100: return 0.3
        return min(0.95, len(content) / 2000)
