import fs from 'node:fs';
import path from 'node:path';
import { marked } from 'marked';
import katex from 'katex';

const SOURCE_MD = path.resolve('wiki/Inner Current (Feynman Primer — Happiness Architecture in Plain Words for the Unprepared Reader).md');
const OUT_HTML = path.resolve('docs/primer.html');

function processMarkdown(rawMd) {
  // Strip YAML frontmatter
  let md = rawMd.replace(/^---[\s\S]*?---\n/, '');

  // 1. Process Obsidian Callouts
  md = md.replace(/^>\s*\[!([a-zA-Z0-9_-]+)\][ \t]*(.*)$/gm, (match, type, title) => {
    const cleanType = type.toLowerCase();
    const typeLabel = cleanType === 'quote' ? 'Цитата' : cleanType.toUpperCase();
    const titleText = title && title.trim() ? title.trim() : typeLabel;
    return `> <div class="callout-header"><span class="callout-badge">${typeLabel}</span> <strong>${titleText}</strong></div>\n>`;
  });

  // 2. Process Obsidian Wiki-links: [[Link|Alias]] -> Alias, [[Link]] -> Link
  md = md.replace(/\[\[(?:[^|\]]*\|)?([^\]]+)\]\]/g, '$1');

  // 3. Pre-process Math formulas via KaTeX
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

marked.use({
  renderer: {
    code(token) {
      if (token.lang === 'mermaid') {
        return `\n\n<div class="mermaid-diagram-wrap"><pre class="mermaid">${token.text}</pre></div>\n\n`;
      }
      return false;
    }
  }
});

function build() {
  const rawMd = fs.readFileSync(SOURCE_MD, 'utf-8');
  const processed = processMarkdown(rawMd);
  const bodyHtml = marked.parse(processed);

  const html = `<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>Архитектура счастья простыми словами — Праймер Фейнмана</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    @page {
      size: A4;
      margin: 22mm 20mm 24mm 20mm;
      @top-right {
        content: "Архитектура счастья простыми словами";
        font-family: 'Inter', sans-serif;
        font-size: 8pt;
        color: #999;
        font-weight: 500;
        letter-spacing: 0.04em;
      }
      @bottom-left {
        content: "Праймер Фейнмана • Физика внутреннего контура";
        font-family: 'Inter', sans-serif;
        font-size: 7.5pt;
        color: #aaa;
        letter-spacing: 0.03em;
      }
      @bottom-right {
        content: counter(page);
        font-family: 'Inter', sans-serif;
        font-size: 8.5pt;
        color: #666;
        font-weight: 500;
      }
    }

    @page :first {
      margin: 0;
      @top-right { content: none; }
      @bottom-left { content: none; }
      @bottom-right { content: none; }
    }

    * {
      box-sizing: border-box;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }

    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      font-size: 10.5pt;
      line-height: 1.65;
      color: #1e242b;
      background: #ffffff;
      margin: 0;
      padding: 0;
    }

    /* Cover Page */
    .cover-page {
      page-break-after: always;
      height: 100vh;
      min-height: 297mm;
      padding: 35mm 25mm 30mm 25mm;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      background: linear-gradient(175deg, #0e141d 0%, #161f2c 60%, #1c2738 100%);
      color: #ffffff;
      position: relative;
      overflow: hidden;
    }

    .cover-page::before {
      content: "";
      position: absolute;
      top: -120px;
      right: -120px;
      width: 450px;
      height: 450px;
      background: radial-gradient(circle, rgba(212, 175, 55, 0.15) 0%, rgba(212, 175, 55, 0) 70%);
      border-radius: 50%;
      pointer-events: none;
    }

    .cover-top {
      position: relative;
      z-index: 2;
    }

    .cover-pill {
      display: inline-block;
      font-family: 'JetBrains Mono', monospace;
      font-size: 8.5pt;
      letter-spacing: 0.25em;
      text-transform: uppercase;
      color: #dfb755;
      background: rgba(223, 183, 85, 0.12);
      border: 1px solid rgba(223, 183, 85, 0.3);
      padding: 6px 14px;
      border-radius: 20px;
      margin-bottom: 25px;
    }

    .cover-title {
      font-family: 'Cormorant Garamond', Georgia, serif;
      font-size: 38pt;
      font-weight: 700;
      line-height: 1.15;
      letter-spacing: -0.02em;
      color: #ffffff;
      margin: 0 0 16px 0;
    }

    .cover-title span {
      color: #dfb755;
      display: block;
    }

    .cover-subtitle {
      font-size: 13pt;
      font-weight: 300;
      color: #a4b3c6;
      line-height: 1.5;
      max-width: 90%;
      margin: 0 0 25px 0;
    }

    .cover-middle {
      position: relative;
      z-index: 2;
      border-left: 2px solid #dfb755;
      padding-left: 20px;
      margin: 20px 0;
    }

    .cover-epigraph {
      font-family: 'Cormorant Garamond', serif;
      font-style: italic;
      font-size: 14pt;
      line-height: 1.5;
      color: #e2e8f0;
      margin-bottom: 8px;
    }

    .cover-author {
      font-family: 'Inter', sans-serif;
      font-size: 9.5pt;
      font-weight: 600;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: #dfb755;
    }

    .cover-bottom {
      position: relative;
      z-index: 2;
      border-top: 1px solid rgba(255, 255, 255, 0.12);
      padding-top: 20px;
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      font-size: 9pt;
      color: #798da3;
    }

    .cover-specs {
      font-family: 'JetBrains Mono', monospace;
      font-size: 8pt;
      line-height: 1.6;
    }

    /* Content Typography */
    .content-container {
      padding: 0;
    }

    h1 {
      font-family: 'Cormorant Garamond', serif;
      font-size: 24pt;
      font-weight: 700;
      color: #0f172a;
      line-height: 1.25;
      margin-top: 0;
      margin-bottom: 12px;
      display: none; /* Already on cover */
    }

    h2 {
      font-family: 'Cormorant Garamond', serif;
      font-size: 17pt;
      font-weight: 700;
      color: #0e1c2f;
      line-height: 1.3;
      margin-top: 28px;
      margin-bottom: 12px;
      padding-bottom: 6px;
      border-bottom: 1.5px solid #eaeef4;
      break-after: avoid;
    }

    h3 {
      font-family: 'Inter', sans-serif;
      font-size: 11.5pt;
      font-weight: 700;
      color: #1e293b;
      margin-top: 18px;
      margin-bottom: 8px;
      break-after: avoid;
    }

    p {
      margin-top: 0;
      margin-bottom: 12px;
      text-align: justify;
      hyphens: auto;
    }

    strong {
      color: #0f172a;
      font-weight: 600;
    }

    /* Blockquotes / Callouts */
    blockquote {
      margin: 16px 0;
      padding: 12px 18px;
      background: #f8fafc;
      border-left: 3.5px solid #c59b27;
      border-radius: 0 8px 8px 0;
      font-size: 10pt;
      color: #334155;
    }

    blockquote p {
      margin-bottom: 6px;
    }

    blockquote p:last-child {
      margin-bottom: 0;
    }

    .callout-header {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 6px;
      font-size: 9.5pt;
      color: #8c6b12;
    }

    .callout-badge {
      font-family: 'JetBrains Mono', monospace;
      font-size: 7.5pt;
      text-transform: uppercase;
      padding: 2px 7px;
      background: #f1e5c3;
      color: #8c6b12;
      border-radius: 4px;
      font-weight: 600;
    }

    /* Tables */
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 18px 0;
      font-size: 9.5pt;
      line-height: 1.5;
    }

    th {
      background: #f1f5f9;
      color: #0f172a;
      font-weight: 600;
      text-align: left;
      padding: 9px 12px;
      border: 1px solid #cbd5e1;
      font-size: 9pt;
      letter-spacing: 0.02em;
    }

    td {
      padding: 9px 12px;
      border: 1px solid #e2e8f0;
      vertical-align: top;
    }

    tr:nth-child(even) td {
      background: #fafcff;
    }

    /* Code blocks / ASCII */
    pre {
      font-family: 'JetBrains Mono', monospace;
      font-size: 8pt;
      background: #0f172a;
      color: #e2e8f0;
      padding: 12px 16px;
      border-radius: 6px;
      overflow-x: auto;
      line-height: 1.45;
      margin: 16px 0;
    }

    code {
      font-family: 'JetBrains Mono', monospace;
      font-size: 8.5pt;
      background: #f1f5f9;
      color: #0f172a;
      padding: 2px 5px;
      border-radius: 4px;
    }

    pre code {
      background: none;
      color: inherit;
      padding: 0;
    }

    /* Math */
    .math-block {
      text-align: center;
      margin: 14px 0;
      padding: 8px 0;
      overflow-x: auto;
    }

    /* Mermaid */
    .mermaid-diagram-wrap {
      text-align: center;
      margin: 18px 0;
      padding: 14px 10px;
      background: #fafbfd;
      border: 1px solid #e2e8f0;
      border-radius: 8px;
      break-inside: avoid;
    }

    .mermaid {
      display: flex;
      justify-content: center;
    }

    .mermaid svg {
      max-width: 100% !important;
      height: auto !important;
    }

    /* Lists */
    ul, ol {
      margin-top: 0;
      margin-bottom: 12px;
      padding-left: 22px;
    }

    li {
      margin-bottom: 5px;
    }

    hr {
      border: 0;
      height: 1px;
      background: #e2e8f0;
      margin: 22px 0;
    }

    /* Chapter breaks */
    .chapter-break {
      page-break-before: always;
    }
  </style>
</head>
<body>

  <!-- Cover Page -->
  <div class="cover-page">
    <div class="cover-top">
      <div class="cover-pill">Первые Принципы • Канон Фейнмана</div>
      <div class="cover-title">
        Архитектура счастья
        <span>простыми словами</span>
      </div>
      <div class="cover-subtitle">
        Базовые понятия контурной физики человека на основе книги «Внутренний ток». Полное руководство без академического тумана, мистики и снисходительности.
      </div>
    </div>

    <div class="cover-middle">
      <div class="cover-epigraph">
        «Если вы не можете объяснить идею простыми словами обычному человеку или десятилетнему ребенку — значит, вы сами глубоко её не понимаете или прячете ложь за птичьим языком.»
      </div>
      <div class="cover-author">Ричард Фейнман • Лауреат Нобелевской премии по физике</div>
    </div>

    <div class="cover-bottom">
      <div>
        <strong>Контурная электродинамика сознания</strong><br>
        Модель карманного фонарика, шланг без заломов и 10-секундный ремонт
      </div>
      <div class="cover-specs">
        Издание 2026<br>
        Open Source Protocol • Self-Hosted Node
      </div>
    </div>
  </div>

  <!-- Main Content -->
  <div class="content-container">
    ${bodyHtml}
  </div>

  <script>
    mermaid.initialize({
      startOnLoad: true,
      theme: 'neutral',
      fontFamily: 'Inter, sans-serif',
      fontSize: 12,
      flowchart: { curve: 'basis' }
    });
  </script>
</body>
</html>`;

  fs.writeFileSync(OUT_HTML, html, 'utf-8');
  console.log(`✅ Generated HTML: ${OUT_HTML} (${Buffer.byteLength(html, 'utf-8')} bytes)`);
}

build();
