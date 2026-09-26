import fs from 'node:fs';
import path from 'node:path';
import { marked } from 'marked';
import katex from 'katex';

const EDITIONS = [
  {
    lang: 'ru',
    sourceFile: path.resolve('book_outline.md'),
    outDir: path.resolve('public/book'),
    htmlFile: path.resolve('public/book/index.html'),
    title: 'Внутренний ток: Архитектура счастья — Владимир Аньянов',
    brandTitle: '⚡ ВНУТРЕННИЙ ТОК',
    brandPill: 'Книга (Полное издание)',
    heroTitle: 'Внутренний ток',
    heroSubtitle: 'Архитектура счастья: Инженерное руководство по электродинамике сознания',
    heroAuthor: 'Владимир Аньянов',
    fig1Caption: 'Рис. 1. Топология сверхпроводимости человека-оператора: ламинарный поток при R → 0',
    fig2Caption: 'Рис. 2. Принципиальная схема паразитного шунта эго и тепловые потери Джоуля-Ленца (Q = I²·Re·t)',
    tocTitle: 'Оглавление книги',
    searchPlaceholder: 'Поиск по главам и понятиям...',
    themeLabel: '🌓 Тема',
    pdfLabel: '📄 Скачать PDF',
    appLabel: '🚀 В тренажер',
    appUrl: '../index.html'
  },
  {
    lang: 'en',
    sourceFile: path.resolve('book_outline_en.md'),
    outDir: path.resolve('public/book/en'),
    htmlFile: path.resolve('public/book/en/index.html'),
    title: 'Inner Current: The Architecture of Happiness — Vladimir Anyanov',
    brandTitle: '⚡ INNER CURRENT',
    brandPill: 'Book (Complete Edition)',
    heroTitle: 'Inner Current',
    heroSubtitle: 'The Architecture of Happiness: An Engineering Guide to Consciousness Electrodynamics',
    heroAuthor: 'Vladimir Anyanov',
    fig1Caption: 'Fig. 1. Operator superconductivity topology: laminar flow at R → 0',
    fig2Caption: 'Fig. 2. Schematic of parasitic ego shunt and Joule-Lenz thermal losses (Q = I²·Re·t)',
    tocTitle: 'Table of Contents',
    searchPlaceholder: 'Search chapters and concepts...',
    themeLabel: '🌓 Theme',
    pdfLabel: '📄 Download PDF',
    appLabel: '🚀 Open App',
    appUrl: '../../index.html'
  },
  {
    lang: 'it',
    sourceFile: path.resolve('book_outline_it.md'),
    outDir: path.resolve('public/book/it'),
    htmlFile: path.resolve('public/book/it/index.html'),
    title: 'La Corrente Interiore: L\'Architettura della Felicità — Vladimir Anyanov',
    brandTitle: '⚡ LA CORRENTE INTERIORE',
    brandPill: 'Libro (Edizione Completa)',
    heroTitle: 'La Corrente Interiore',
    heroSubtitle: 'L\'Architettura della Felicità: Guida ingegneristica all\'elettrodinamica della coscienza',
    heroAuthor: 'Vladimir Anyanov',
    fig1Caption: 'Fig. 1. Topologia della superconduttività dell\'operatore: flusso laminare a R → 0',
    fig2Caption: 'Fig. 2. Schema di principio dello shunt parassita dell\'ego e perdite termiche di Joule-Lenz (Q = I²·Re·t)',
    tocTitle: 'Indice del Libro',
    searchPlaceholder: 'Cerca tra capitoli e concetti...',
    themeLabel: '🌓 Tema',
    pdfLabel: '📄 Scarica PDF',
    appLabel: '🚀 Apri App',
    appUrl: '../../index.html'
  }
];

function processMarkdown(rawMd) {
  let md = rawMd;

  // 1. Process Obsidian Callouts:
  // > [!quote] Title
  // > Content
  md = md.replace(/^>\s*\[!([a-zA-Z0-9_-]+)\][ \t]*(.*)$/gm, (match, type, title) => {
    if (title && title.trim()) {
      return `> **${title.trim()}**\n>`;
    }
    return '>';
  });

  // 2. Process Obsidian Wiki-links in tables or text:
  // [[02_Wiki/Inner Current (Title)\|Alias]] -> Alias
  // [[02_Wiki/Inner Current (Title)|Alias]] -> Alias
  // [[Title]] -> Title
  md = md.replace(/\[\[(?:[^|\]]*\|)?([^\]]+)\]\]/g, '$1');

  // 3. Pre-process Math formulas via KaTeX before markdown parsing:
  // Block math: $$ ... $$
  md = md.replace(/\$\$([\s\S]+?)\$\$/g, (match, formula) => {
    try {
      const rendered = katex.renderToString(formula.trim(), {
        displayMode: true,
        throwOnError: false
      });
      return `\n\n<div class="math-block">${rendered}</div>\n\n`;
    } catch (e) {
      return match;
    }
  });

  // Inline math: $ ... $
  md = md.replace(/(?<!\\)\$([^\$\n]+?)(?<!\\)\$/g, (match, formula) => {
    try {
      const rendered = katex.renderToString(formula.trim(), {
        displayMode: false,
        throwOnError: false
      });
      return rendered;
    } catch (e) {
      return match;
    }
  });

  return md;
}

// Configure marked renderer for Mermaid diagrams
marked.use({
  renderer: {
    code(token) {
      if (token.lang === 'mermaid') {
        const encoded = encodeURIComponent(token.text);
        return `\n\n<div class="mermaid-diagram" data-diagram="${encoded}"><pre class="mermaid">${token.text}</pre></div>\n\n`;
      }
      return false;
    }
  }
});

function buildEdition(edition) {
  if (!fs.existsSync(edition.sourceFile)) {
    console.log(`⚠️ Source file ${edition.sourceFile} does not exist yet. Skipping ${edition.lang}.`);
    return;
  }

  if (!fs.existsSync(edition.outDir)) {
    fs.mkdirSync(edition.outDir, { recursive: true });
  }

  const rawMarkdown = fs.readFileSync(edition.sourceFile, 'utf-8');
  const processedMarkdown = processMarkdown(rawMarkdown);
  const contentHtml = marked.parse(processedMarkdown);

  const assetPrefix = edition.lang === 'ru' ? '..' : '../..';
  const ruUrl = edition.lang === 'ru' ? 'index.html' : '../index.html';
  const enUrl = edition.lang === 'ru' ? 'en/index.html' : (edition.lang === 'en' ? 'index.html' : '../en/index.html');
  const itUrl = edition.lang === 'ru' ? 'it/index.html' : (edition.lang === 'it' ? 'index.html' : '../it/index.html');

  const template = `<!DOCTYPE html>
<html lang="${edition.lang}" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${edition.title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Fira+Code:wght@400;500;600&family=Inter:wght@300;400;500;600;700&family=Lora:ital,wght@0,400;0,500;0,600;1,400;1,500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>

  <style>
    :root {
      --bg: #090d16;
      --bg-card: #0f172a;
      --bg-card-subtle: #131c31;
      --border: #1e293b;
      --border-glow: rgba(56, 189, 248, 0.3);
      --text: #cbd5e1;
      --text-bright: #f8fafc;
      --text-muted: #64748b;
      --accent: #38bdf8;
      --accent-gold: #fbbf24;
      --accent-glow: rgba(56, 189, 248, 0.15);
      --font-body: 'Lora', Georgia, serif;
      --font-ui: 'Inter', system-ui, sans-serif;
      --font-mono: 'Fira Code', monospace;
      --font-display: 'Cinzel', serif;
      --reader-width: 780px;
      --font-size: 18px;
      --line-height: 1.85;
    }

    [data-theme="light"] {
      --bg: #f8fafc;
      --bg-card: #ffffff;
      --bg-card-subtle: #f1f5f9;
      --border: #e2e8f0;
      --border-glow: rgba(14, 165, 233, 0.3);
      --text: #334155;
      --text-bright: #0f172a;
      --text-muted: #64748b;
      --accent: #0284c7;
      --accent-gold: #d97706;
      --accent-glow: rgba(2, 132, 199, 0.1);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      background: var(--bg);
      color: var(--text);
      font-family: var(--font-body);
      font-size: var(--font-size);
      line-height: var(--line-height);
      overflow-x: hidden;
      transition: background 0.3s ease, color 0.3s ease;
    }

    /* Top Bar */
    .topbar {
      position: sticky;
      top: 0;
      z-index: 100;
      background: rgba(9, 13, 22, 0.85);
      backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--border);
      padding: 0.75rem 1.5rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-family: var(--font-ui);
    }
    [data-theme="light"] .topbar {
      background: rgba(248, 250, 252, 0.88);
    }

    .topbar-left {
      display: flex;
      align-items: center;
      gap: 1rem;
    }

    .brand-title {
      font-family: var(--font-display);
      font-weight: 700;
      font-size: 1.05rem;
      letter-spacing: 0.08em;
      color: var(--text-bright);
      text-decoration: none;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    .brand-pill {
      font-family: var(--font-mono);
      font-size: 0.7rem;
      padding: 0.2rem 0.5rem;
      border-radius: 999px;
      background: rgba(56, 189, 248, 0.15);
      color: var(--accent);
      border: 1px solid var(--border-glow);
    }

    .topbar-controls {
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }

    /* Language Switcher */
    .lang-switcher {
      display: flex;
      align-items: center;
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 2px;
      gap: 2px;
    }
    .lang-btn {
      padding: 0.35rem 0.55rem;
      font-size: 0.75rem;
      font-weight: 600;
      color: var(--text-muted);
      text-decoration: none;
      border-radius: 4px;
      transition: all 0.2s;
    }
    .lang-btn:hover {
      color: var(--text-bright);
      background: var(--bg-card-subtle);
    }
    .lang-btn.active {
      color: var(--accent);
      background: rgba(56, 189, 248, 0.15);
      border: 1px solid var(--border-glow);
    }

    .btn {
      font-family: var(--font-ui);
      background: var(--bg-card);
      border: 1px solid var(--border);
      color: var(--text);
      padding: 0.45rem 0.85rem;
      border-radius: 6px;
      cursor: pointer;
      font-size: 0.85rem;
      display: inline-flex;
      align-items: center;
      gap: 0.4rem;
      transition: all 0.2s;
      text-decoration: none;
    }
    .btn:hover {
      background: var(--bg-card-subtle);
      border-color: var(--accent);
      color: var(--text-bright);
    }
    .btn-primary {
      background: linear-gradient(135deg, #0284c7, #38bdf8);
      color: #fff;
      font-weight: 600;
      border: none;
    }
    .btn-primary:hover {
      box-shadow: 0 0 16px rgba(56, 189, 248, 0.4);
      color: #fff;
    }

    /* Layout */
    .app-layout {
      display: flex;
      min-height: calc(100vh - 56px);
    }

    /* Sidebar Navigation */
    .sidebar {
      width: 320px;
      background: var(--bg-card);
      border-right: 1px solid var(--border);
      overflow-y: auto;
      height: calc(100vh - 56px);
      position: sticky;
      top: 56px;
      padding: 1.25rem 1rem;
      font-family: var(--font-ui);
      flex-shrink: 0;
    }

    .sidebar-search {
      margin-bottom: 1.25rem;
    }
    .sidebar-search input {
      width: 100%;
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: 6px;
      padding: 0.55rem 0.75rem;
      color: var(--text-bright);
      font-size: 0.85rem;
      outline: none;
    }
    .sidebar-search input:focus {
      border-color: var(--accent);
      box-shadow: 0 0 0 2px var(--accent-glow);
    }

    .toc-title {
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: var(--text-muted);
      margin-bottom: 0.75rem;
      font-weight: 700;
    }

    .toc-list {
      list-style: none;
    }
    .toc-item {
      margin-bottom: 0.35rem;
    }
    .toc-link {
      display: block;
      color: var(--text);
      text-decoration: none;
      font-size: 0.85rem;
      padding: 0.35rem 0.6rem;
      border-radius: 5px;
      transition: background 0.15s, color 0.15s;
    }
    .toc-link:hover {
      background: var(--bg-card-subtle);
      color: var(--accent);
    }
    .toc-item.level-1 > .toc-link {
      font-weight: 700;
      color: var(--text-bright);
      margin-top: 0.75rem;
    }
    .toc-item.level-2 > .toc-link {
      padding-left: 1rem;
      color: var(--text);
    }
    .toc-item.level-3 > .toc-link {
      padding-left: 1.6rem;
      font-size: 0.8rem;
      color: var(--text-muted);
    }

    /* Main Reader Area */
    .reader-container {
      flex: 1;
      padding: 3rem 2rem 6rem;
      display: flex;
      justify-content: center;
      overflow-y: auto;
    }

    .reader-article {
      max-width: var(--reader-width);
      width: 100%;
    }

    /* Book Hero / Cover in Reader */
    .book-hero {
      text-align: center;
      padding: 2.5rem 1rem 4rem;
      border-bottom: 1px solid var(--border);
      margin-bottom: 3.5rem;
    }
    .book-hero-cover {
      max-width: 280px;
      border-radius: 12px;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6), 0 0 30px rgba(56, 189, 248, 0.2);
      margin-bottom: 2rem;
      border: 1px solid var(--border-glow);
    }
    .book-hero h1 {
      font-family: var(--font-display);
      font-size: 2.6rem;
      letter-spacing: 0.04em;
      color: var(--text-bright);
      margin-bottom: 0.5rem;
    }
    .book-hero-subtitle {
      font-family: var(--font-ui);
      font-size: 1.25rem;
      color: var(--accent-gold);
      margin-bottom: 1rem;
      font-weight: 500;
    }
    .book-hero-author {
      font-family: var(--font-ui);
      font-size: 1rem;
      color: var(--text-muted);
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }

    /* Typography inside manuscript */
    .reader-article h1, .reader-article h2, .reader-article h3, .reader-article h4 {
      color: var(--text-bright);
      font-weight: 700;
      line-height: 1.3;
      margin-top: 2.5em;
      margin-bottom: 0.8em;
      scroll-margin-top: 80px;
    }
    .reader-article h1 {
      font-family: var(--font-display);
      font-size: 2.1rem;
      border-bottom: 1px solid var(--border);
      padding-bottom: 0.4em;
    }
    .reader-article h2 {
      font-family: var(--font-ui);
      font-size: 1.55rem;
      color: var(--accent);
      border-left: 3px solid var(--accent);
      padding-left: 0.75rem;
    }
    .reader-article h3 {
      font-family: var(--font-ui);
      font-size: 1.25rem;
      color: var(--text-bright);
    }
    .reader-article p {
      margin-bottom: 1.5em;
      text-align: justify;
    }
    .reader-article strong {
      color: var(--text-bright);
      font-weight: 600;
    }
    .reader-article em {
      color: var(--accent-gold);
      font-style: italic;
    }

    .reader-article blockquote {
      border-left: 4px solid var(--accent-gold);
      background: var(--bg-card-subtle);
      padding: 1.25rem 1.75rem;
      margin: 2rem 0;
      border-radius: 0 8px 8px 0;
      font-style: italic;
      color: var(--text-bright);
    }

    .reader-article ul, .reader-article ol {
      margin: 1.25rem 0 1.75rem 1.8rem;
    }
    .reader-article li {
      margin-bottom: 0.5rem;
    }

    .reader-article code {
      font-family: var(--font-mono);
      background: var(--bg-card-subtle);
      color: var(--accent);
      padding: 0.15rem 0.4rem;
      border-radius: 4px;
      font-size: 0.9em;
      border: 1px solid var(--border);
    }

    .reader-article pre {
      background: #060910;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 1.25rem;
      overflow-x: auto;
      margin: 1.75rem 0;
    }
    .reader-article pre code {
      background: transparent;
      padding: 0;
      border: none;
      color: #94a3b8;
    }

    .reader-article table {
      width: 100%;
      border-collapse: collapse;
      margin: 2rem 0;
      font-family: var(--font-ui);
      font-size: 0.92rem;
    }
    .reader-article th, .reader-article td {
      border: 1px solid var(--border);
      padding: 0.75rem 1rem;
      text-align: left;
    }
    .reader-article th {
      background: var(--bg-card-subtle);
      color: var(--text-bright);
      font-weight: 600;
    }
    .reader-article tr:nth-child(even) {
      background: rgba(255, 255, 255, 0.02);
    }

    .reader-article hr {
      border: none;
      height: 1px;
      background: linear-gradient(90deg, transparent, var(--border), transparent);
      margin: 3.5rem 0;
    }

    .math-block {
      margin: 1.75rem 0;
      text-align: center;
      overflow-x: auto;
      padding: 0.5rem 0;
    }

    .katex {
      font-size: 1.15em !important;
      color: var(--accent) !important;
    }

    [data-theme="light"] .katex {
      color: var(--accent) !important;
    }

    .img-figure {
      margin: 2.5rem 0;
      text-align: center;
    }
    .img-figure img {
      max-width: 100%;
      border-radius: 8px;
      border: 1px solid var(--border);
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }
    .img-figure figcaption {
      font-family: var(--font-ui);
      font-size: 0.85rem;
      color: var(--text-muted);
      margin-top: 0.6rem;
    }

    .mermaid-diagram {
      margin: 2.5rem 0;
      padding: 1.5rem 1rem;
      background: var(--bg-card-subtle);
      border: 1px solid var(--border);
      border-radius: 12px;
      display: flex;
      justify-content: center;
      align-items: center;
      overflow-x: auto;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
      transition: background 0.3s ease, border-color 0.3s ease;
    }
    .mermaid-diagram svg {
      max-width: 100%;
      height: auto;
    }
    .mermaid-diagram pre.mermaid {
      background: transparent;
      border: none;
      padding: 0;
      margin: 0;
      color: var(--text-muted);
      font-size: 0.85rem;
    }

    /* Print styles */
    @media print {
      .topbar, .sidebar, .font-controls, .lang-switcher { display: none !important; }
      .reader-container { padding: 0 !important; width: 100% !important; }
      .reader-article { max-width: 100% !important; color: #111 !important; font-size: 11pt !important; }
      body { background: #fff !important; color: #111 !important; }
      h1, h2, h3 { color: #000 !important; page-break-after: avoid; }
      pre, blockquote { page-break-inside: avoid; border-color: #999; }
      .katex { color: #000 !important; }
    }

    @media (max-width: 860px) {
      .sidebar { display: none; }
      .reader-container { padding: 1.5rem 1rem; }
      .book-hero h1 { font-size: 2rem; }
    }
  </style>
</head>
<body>

  <!-- Top bar -->
  <header class="topbar">
    <div class="topbar-left">
      <a href="${edition.appUrl}" class="brand-title">
        <span>${edition.brandTitle}</span>
      </a>
      <span class="brand-pill">${edition.brandPill}</span>
    </div>
    <div class="topbar-controls">
      <!-- Language Switcher -->
      <nav class="lang-switcher" aria-label="Language selection">
        <a href="${ruUrl}" class="lang-btn ${edition.lang === 'ru' ? 'active' : ''}">🇷🇺 RU</a>
        <a href="${enUrl}" class="lang-btn ${edition.lang === 'en' ? 'active' : ''}">🇬🇧 EN</a>
        <a href="${itUrl}" class="lang-btn ${edition.lang === 'it' ? 'active' : ''}">🇮🇹 IT</a>
      </nav>

      <button class="btn" id="themeToggle" title="${edition.themeLabel}">${edition.themeLabel}</button>
      <button class="btn" id="fontIncBtn" title="A+">A+</button>
      <button class="btn" id="fontDecBtn" title="A-">A-</button>
      <button class="btn btn-primary" onclick="window.print()" title="${edition.pdfLabel}">${edition.pdfLabel}</button>
      <a href="${edition.appUrl}" class="btn">${edition.appLabel}</a>
    </div>
  </header>

  <div class="app-layout">
    <!-- Sidebar TOC -->
    <aside class="sidebar">
      <div class="sidebar-search">
        <input type="text" id="searchInput" placeholder="${edition.searchPlaceholder}">
      </div>
      <div class="toc-title">${edition.tocTitle}</div>
      <nav>
        <ul class="toc-list" id="tocList">
          <!-- Dynamically populated links -->
        </ul>
      </nav>
    </aside>

    <!-- Main Content -->
    <main class="reader-container">
      <article class="reader-article" id="articleBody">
        <header class="book-hero">
          <img src="${assetPrefix}/assets/book_cover.jpg" alt="${edition.heroTitle}" class="book-hero-cover">
          <h1>${edition.heroTitle}</h1>
          <div class="book-hero-subtitle">${edition.heroSubtitle}</div>
          <div class="book-hero-author">${edition.heroAuthor}</div>
        </header>

        <div class="img-figure">
          <img src="${assetPrefix}/assets/superconductivity_mushin.jpg" alt="Superconductivity Mushin">
          <figcaption>${edition.fig1Caption}</figcaption>
        </div>

        <div id="manuscriptContent">
          ${contentHtml}
        </div>

        <div class="img-figure">
          <img src="${assetPrefix}/assets/ego_shunt_circuit.jpg" alt="Ego Shunt Circuit">
          <figcaption>${edition.fig2Caption}</figcaption>
        </div>
      </article>
    </main>
  </div>

  <script>
    // Theme toggle
    const themeBtn = document.getElementById('themeToggle');
    themeBtn.addEventListener('click', () => {
      const html = document.documentElement;
      const current = html.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      html.setAttribute('data-theme', next);
      localStorage.setItem('inner-current-book-theme', next);
      renderMermaidDiagrams();
    });

    const savedTheme = localStorage.getItem('inner-current-book-theme');
    if (savedTheme) {
      document.documentElement.setAttribute('data-theme', savedTheme);
    }

    // Font size controls
    let currentFontSize = 18;
    document.getElementById('fontIncBtn').addEventListener('click', () => {
      if (currentFontSize < 26) {
        currentFontSize += 1;
        document.body.style.setProperty('--font-size', currentFontSize + 'px');
      }
    });
    document.getElementById('fontDecBtn').addEventListener('click', () => {
      if (currentFontSize > 14) {
        currentFontSize -= 1;
        document.body.style.setProperty('--font-size', currentFontSize + 'px');
      }
    });

    // Generate Dynamic TOC
    const article = document.getElementById('articleBody');
    const headings = article.querySelectorAll('h1, h2, h3');
    const tocList = document.getElementById('tocList');

    headings.forEach((h, idx) => {
      if (idx === 0) return; // Skip hero title
      if (!h.id) {
        h.id = 'heading-' + idx;
      }

      // Clone heading to extract clean TOC text without KaTeX duplicate MathML/annotations
      const clone = h.cloneNode(true);
      clone.querySelectorAll('.katex-mathml').forEach(el => el.remove());
      let text = clone.textContent || '';
      // Remove any emojis and pictographic special characters
      text = text.replace(/[\\p{Extended_Pictographic}\\u{1F300}-\\u{1FAFF}\\u{2600}-\\u{27BF}]/gu, '');
      // Remove invisible zero-width spaces generated by math formatters
      text = text.replace(/[\\u200B-\\u200D\\uFEFF]/g, '');
      // Normalize whitespace
      text = text.replace(/\\s+/g, ' ').trim();

      if (!text) return;

      const li = document.createElement('li');
      li.className = 'toc-item level-' + h.tagName.substring(1);
      const a = document.createElement('a');
      a.className = 'toc-link';
      a.href = '#' + h.id;
      a.textContent = text;
      li.appendChild(a);
      tocList.appendChild(li);
    });

    // Quick Search filter
    document.getElementById('searchInput').addEventListener('input', (e) => {
      const q = e.target.value.toLowerCase();
      const items = tocList.querySelectorAll('.toc-item');
      items.forEach(item => {
        const text = item.textContent.toLowerCase();
        item.style.display = text.includes(q) ? 'block' : 'none';
      });
    });

    // Mermaid dynamic renderer
    async function renderMermaidDiagrams() {
      if (typeof mermaid === 'undefined') return;
      const isLight = document.documentElement.getAttribute('data-theme') === 'light';
      try {
        mermaid.initialize({
          startOnLoad: false,
          theme: isLight ? 'default' : 'dark',
          securityLevel: 'loose',
          fontFamily: 'Inter, system-ui, sans-serif'
        });

        const containers = document.querySelectorAll('.mermaid-diagram');
        for (let i = 0; i < containers.length; i++) {
          const c = containers[i];
          const raw = decodeURIComponent(c.getAttribute('data-diagram') || '');
          if (!raw) continue;
          try {
            const id = 'mermaid-render-' + i + '-' + Date.now();
            const { svg } = await mermaid.render(id, raw);
            c.innerHTML = svg;
          } catch (err) {
            console.warn('Mermaid render error for diagram #' + i, err);
          }
        }
      } catch (e) {
        console.error('Mermaid initialization error:', e);
      }
    }

    // Initialize Mermaid on page load
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', renderMermaidDiagrams);
    } else {
      renderMermaidDiagrams();
    }
  </script>
</body>
</html>`;

  fs.writeFileSync(edition.htmlFile, template, 'utf-8');
  console.log(`✅ [${edition.lang.toUpperCase()}] Web Reader generated successfully at: ${edition.htmlFile}`);
}

console.log('🚀 Building all book editions (RU, EN, IT)...');
for (const ed of EDITIONS) {
  buildEdition(ed);
}
console.log('✨ Build process finished.');
