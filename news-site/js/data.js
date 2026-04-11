export const CATEGORIES = {
    GERAL: { name: 'Geral', color: '#e31212' },
    BRASIL: { name: 'Brasil', color: '#009b3a' },
    MUNDO: { name: 'Mundo', color: '#002776' },
    ECONOMIA: { name: 'Economia', color: '#ffb400' },
    TECNOLOGIA: { name: 'Tecnologia', color: '#00bcd4' },
    ESPORTES: { name: 'Esportes', color: '#4caf50' }
};

export const NEWS_DATA = [
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

export const BREAKING_NEWS = [
    "Urgente: Nova vazão de reservatório em SC preocupa autoridades locais.",
    "Mercado: Dólar recua após anúncio do Banco Central sobre intervenção.",
    "Ciência: Astrônomos detectam sinal de rádio repetitivo de galáxia distante.",
    "Esportes: Neymar anuncia retorno aos gramados para a próxima rodada."
];
