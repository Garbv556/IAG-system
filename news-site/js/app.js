// --- DATA ---
const CATEGORIES = {
    GERAL: { name: 'Geral', color: '#e31212' },
    BRASIL: { name: 'Brasil', color: '#009b3a' },
    MUNDO: { name: 'Mundo', color: '#002776' },
    ECONOMIA: { name: 'Economia', color: '#ffb400' },
    TECNOLOGIA: { name: 'Tecnologia', color: '#00bcd4' },
    ESPORTES: { name: 'Esportes', color: '#4caf50' }
};

const NEWS_DATA = [
    {
        id: 1,
        category: 'BRASIL',
        title: 'Nova Reforma Tributária: O que muda no seu bolso a partir de 2026',
        excerpt: 'O Congresso Nacional aprovou as novas diretrizes que prometem simplificar o sistema de impostos brasileiro.',
        content: 'Brasília presenciou um momento histórico nesta tarde com a aprovação da nova reforma tributária. Especialistas afirmam que a simplificação pode elevar o PIB em até 2% nos próximos cinco anos. O novo sistema unifica impostos federais e estaduais, criando o IVA (Imposto sobre Valor Agregado).',
        author: 'Ricardo Silveira',
        date: '2026-04-10T14:30:00',
        image: 'assets/reforma_tributaria.jpg',
        isFeatured: true
    },
    {
        id: 2,
        category: 'MUNDO',
        title: 'Conferência de Paz em Genebra: Líderes globais buscam cessar-fogo',
        excerpt: 'Delegações de 50 países se reúnem em Genebra para discutir o fim dos conflitos na região do Oriente Médio.',
        content: 'A cúpula de Genebra começou com um tom de otimismo moderado. O Secretário-Geral da ONU destacou a urgência de um acordo humanitário imediato. Espera-se que as negociações durem pelo menos três dias, focando na abertura de corredores de assistência.',
        author: 'Helena Costa',
        date: '2026-04-10T16:15:00',
        image: 'assets/genebra_paz.jpg',
        isFeatured: false
    },
    {
        id: 3,
        category: 'TECNOLOGIA',
        title: 'IA Generativa alcança novo marco na medicina diagnóstica',
        excerpt: 'Novo modelo de Inteligência Artificial consegue identificar patologias raras com 99% de precisão em segundos.',
        content: 'Pesquisadores do MIT e da USP anunciaram hoje um avanço significativo. O software de código aberto promete revolucionar hospitais de áreas remotas, oferecendo diagnósticos de alta precisão via dispositivos móveis.',
        author: 'Marcos Vinícius',
        date: '2026-04-10T11:00:00',
        image: 'assets/ia_medicina.jpg',
        isFeatured: false
    },
    {
        id: 4,
        category: 'ECONOMIA',
        title: 'Bolsa de Valores fecha em alta recorde impulsionada por setor tech',
        excerpt: 'O Ibovespa superou a marca dos 150 mil pontos pela primeira vez na história no pregão de hoje.',
        content: 'O mercado reagiu positivamente aos dados de inflação abaixo do esperado e à robustez do setor de tecnologia nacional. Analistas projetam uma tendência de alta contínua para o próximo trimestre.',
        author: 'Juliana Mendes',
        date: '2026-04-10T18:05:00',
        image: 'assets/bolsa_valores.jpg',
        isFeatured: false
    },
    {
        id: 5,
        category: 'ESPORTES',
        title: 'Brasil se prepara para a final da Copa América com força total',
        excerpt: 'Seleção Brasileira realiza último treino aberto antes de enfrentar a Argentina no Maracanã.',
        content: 'O clima é de festa no Rio de Janeiro. O técnico confirmou que não terá desfalques para a grande final. A expectativa é de casa cheia e um jogo histórico entre os maiores rivais do continente.',
        author: 'Felipe Santana',
        date: '2026-04-10T19:00:00',
        image: 'assets/copa_america.jpg',
        isFeatured: true
    }
];

const BREAKING_NEWS = [
    "Urgente: Nova vazão de reservatório em SC preocupa autoridades locais.",
    "Mercado: Dólar recua após anúncio do Banco Central sobre intervenção.",
    "Ciência: Astrônomos detectam sinal de rádio repetitivo de galáxia distante.",
    "Esportes: Neymar anuncia retorno aos gramados para a próxima rodada."
];

// --- COMPONENTS ---
const createNewsCard = (news) => {
    const cat = CATEGORIES[news.category] || CATEGORIES.GERAL;
    return `
        <article class="news-card" data-id="${news.id}">
            <img src="${news.image}" alt="${news.title}" class="news-card-img" onerror="this.src='https://via.placeholder.com/400x200?text=News+Image'">
            <div class="news-card-content">
                <span class="badge" style="background: ${cat.color}; color: #fff;">${cat.name}</span>
                <h3 class="news-card-title">${news.title}</h3>
                <p class="news-card-excerpt">${news.excerpt}</p>
                <div style="font-size: 0.75rem; color: var(--text-secondary);">Por ${news.author}</div>
            </div>
        </article>
    `;
};

const createHeroCard = (news) => {
    const cat = CATEGORIES[news.category] || CATEGORIES.GERAL;
    return `
        <article class="hero-card" data-id="${news.id}" style="cursor: pointer;">
            <img src="${news.image}" alt="${news.title}" onerror="this.src='https://via.placeholder.com/1200x600?text=Featured+News'">
            <div class="hero-overlay">
                <span class="badge" style="background: ${cat.color}; color: #fff;">${cat.name}</span>
                <h1 class="hero-title">${news.title}</h1>
                <p>${news.excerpt}</p>
            </div>
        </article>
    `;
};

const createTickerItem = (text) => {
    return `<span class="ticker-item"><strong>AGORA:</strong> ${text}</span>`;
};

const createMostReadItem = (news, index) => {
    return `
        <div class="most-read-item" data-id="${news.id}" style="cursor: pointer;">
            <span class="number">${index + 1}</span>
            <p style="font-size: 0.95rem; font-weight: 600;">${news.title}</p>
        </div>
    `;
};

// --- APP LOGIC ---
class NewsPortal {
    constructor() {
        this.news = NEWS_DATA;
        this.currentCategory = 'TODAS';
        this.init();
    }

    init() {
        this.renderCategories();
        this.renderTicker();
        this.renderContent();
        this.setupEventListeners();
    }

    renderCategories() {
        const nav = document.getElementById('navCategories');
        if (!nav) return;
        const categoriesHTML = Object.entries(CATEGORIES).map(([key, cat]) => `
            <li><a href="#" data-category="${key}">${cat.name}</a></li>
        `).join('');
        nav.innerHTML = `<li><a href="#" data-category="TODAS" style="color: var(--accent-red)">Início</a></li>` + categoriesHTML;
    }

    renderTicker() {
        const ticker = document.getElementById('tickerItems');
        if (!ticker) return;
        ticker.innerHTML = BREAKING_NEWS.map(createTickerItem).join('') + BREAKING_NEWS.map(createTickerItem).join('');
    }

    renderContent(filteredNews = this.news) {
        const heroSection = document.getElementById('heroSection');
        const newsGrid = document.getElementById('newsGrid');
        const mostRead = document.getElementById('mostRead');

        const featured = filteredNews.find(n => n.isFeatured) || filteredNews[0];
        if (featured && heroSection) {
            heroSection.innerHTML = createHeroCard(featured);
        }

        const regular = filteredNews.filter(n => n.id !== featured?.id);
        if (newsGrid) newsGrid.innerHTML = regular.map(createNewsCard).join('');

        if (mostRead) mostRead.innerHTML = this.news.slice(0, 5).map((n, i) => createMostReadItem(n, i)).join('');
    }

    setupEventListeners() {
        const nav = document.getElementById('navCategories');
        if (nav) {
            nav.addEventListener('click', (e) => {
                if (e.target.tagName === 'A') {
                    e.preventDefault();
                    const cat = e.target.dataset.category;
                    this.filterByCategory(cat);
                }
            });
        }

        const search = document.getElementById('searchInput');
        if (search) {
            search.addEventListener('input', (e) => {
                this.searchNews(e.target.value);
            });
        }

        const toggle = document.getElementById('themeToggle');
        if (toggle) {
            toggle.addEventListener('click', () => {
                const current = document.body.getAttribute('data-theme');
                const next = current === 'dark' ? 'light' : 'dark';
                document.body.setAttribute('data-theme', next);
                toggle.innerText = next === 'dark' ? '☀️' : '🌓';
            });
        }

        document.addEventListener('click', (e) => {
            const clickable = e.target.closest('.news-card, .hero-card, .most-read-item');
            if (clickable) {
                const id = parseInt(clickable.dataset.id);
                this.openArticle(id);
            }
        });

        const closeBtn = document.getElementById('closeModal');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                document.getElementById('articleModal').style.display = 'none';
                document.body.style.overflow = 'auto';
            });
        }

        window.onclick = (event) => {
            const modal = document.getElementById('articleModal');
            if (event.target == modal) {
                modal.style.display = 'none';
                document.body.style.overflow = 'auto';
            }
        };
    }

    filterByCategory(category) {
        this.currentCategory = category;
        const filtered = category === 'TODAS' ? this.news : this.news.filter(n => n.category === category);
        this.renderContent(filtered);
        
        document.querySelectorAll('#navCategories a').forEach(a => {
            a.style.color = a.dataset.category === category ? 'var(--accent-red)' : 'inherit';
        });
    }

    searchNews(query) {
        const q = query.toLowerCase();
        const filtered = this.news.filter(n => 
            n.title.toLowerCase().includes(q) || 
            n.excerpt.toLowerCase().includes(q) ||
            n.category.toLowerCase().includes(q)
        );
        this.renderContent(filtered);
    }

    openArticle(id) {
        const article = this.news.find(n => n.id === id);
        if (!article) return;

        const cat = CATEGORIES[article.category] || CATEGORIES.GERAL;
        const modalBody = document.getElementById('modalContentBody');
        modalBody.innerHTML = `
            <img src="${article.image}" class="article-img" alt="${article.title}">
            <div class="article-header">
                <span class="badge" style="background: ${cat.color}; color: #fff;">${cat.name}</span>
                <h1 style="font-size: 2.5rem; margin-top: 10px;">${article.title}</h1>
                <p style="color: var(--text-secondary); margin-top: 15px;">Por <strong>${article.author}</strong> | 10 de Abril de 2026</p>
            </div>
            <div class="article-body">
                <p style="font-weight: 700; font-size: 1.3rem; margin-bottom: 30px;">${article.excerpt}</p>
                <p>${article.content}</p>
                <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid var(--border-color); display: flex; gap: 20px;">
                    <button style="padding: 10px 20px; background: #1877f2; color: #fff; border: none; border-radius: 4px; cursor: pointer;">Compartilhar no Facebook</button>
                    <button style="padding: 10px 20px; background: #1da1f2; color: #fff; border: none; border-radius: 4px; cursor: pointer;">Postar no X</button>
                </div>
            </div>
        `;

        const modal = document.getElementById('articleModal');
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
}

window.addEventListener('DOMContentLoaded', () => {
    new NewsPortal();
});
