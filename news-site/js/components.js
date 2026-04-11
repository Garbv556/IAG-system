import { CATEGORIES } from './data.js';

export const createNewsCard = (news) => {
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

export const createHeroCard = (news) => {
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

export const createTickerItem = (text) => {
    return `<span class="ticker-item"><strong>AGORA:</strong> ${text}</span>`;
};

export const createMostReadItem = (news, index) => {
    return `
        <div class="most-read-item" data-id="${news.id}" style="cursor: pointer;">
            <span class="number">${index + 1}</span>
            <p style="font-size: 0.95rem; font-weight: 600;">${news.title}</p>
        </div>
    `;
};
