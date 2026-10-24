# -*- coding: utf-8 -*-
"""
Build HTML reader for New Book 1:
«Внутренний ток: Архитектура Человека (Канон Сверхпроводимости 3.0)»
Generates:
1. dist_site/books/01_inner_current.html & public/books/01_inner_current.html
2. dist_site/book/index.html & public/book/index.html
3. Updates dist_site/index.html & public/index.html book 1 card
"""
import os
import re
import sys
import shutil
import markdown

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current"
LIB_DIR = os.path.join(ROOT_DIR, "IC Library", "Золотая семерка 2.0")
SRC_MD = os.path.join(LIB_DIR, "01 — Владимир Аньянов — Внутренний ток (Архитектура Человека — Канон Сверхпроводимости).md")

DIST_DIR = os.path.join(ROOT_DIR, "dist_site")
PUBLIC_DIR = os.path.join(ROOT_DIR, "public")

with open(SRC_MD, "r", encoding="utf-8") as f:
    raw_md = f.read()

# Strip frontmatter
raw_md = re.sub(r"^---[\s\S]*?---\n", "", raw_md)
# Strip Obsidian WikiLinks
raw_md = re.sub(r"\[\[(?:[^|\]]*\\?\|)?([^\]]+)\]\]", r"\1", raw_md)

def replace_callout(match):
    ctype = match.group(1).lower()
    content = match.group(2)
    lines = [re.sub(r"^>\s?", "", line) for line in content.strip().split("\n")]
    title = lines[0].strip() if lines else ""
    body_lines = lines[1:] if len(lines) > 1 else []
    body_text = "\n".join(body_lines).strip()
    body_html = markdown.markdown(body_text, extensions=['tables', 'fenced_code', 'nl2br'])
    
    icon = "⚡"
    accent_color = "#f59e0b"
    if "quote" in ctype:
        icon = "📜"
        accent_color = "#38bdf8"
    elif "important" in ctype or "warning" in ctype:
        icon = "⚠️"
        accent_color = "#f43f5e"
    elif "tip" in ctype:
        icon = "💡"
        accent_color = "#10b981"
    elif "info" in ctype:
        icon = "ℹ️"
        accent_color = "#60a5fa"
        
    title_html = f'<div class="callout-title" style="font-family: \'Plus Jakarta Sans\', sans-serif; font-size: 10pt; font-weight: 700; text-transform: uppercase; letter-spacing: 0.12em; color: {accent_color}; margin-bottom: 8px; display: flex; align-items: center; gap: 6px;"><span>{icon}</span> <span>{title}</span></div>' if title else ""
    return f'<div class="callout callout-{ctype}">{title_html}<div class="callout-body">{body_html}</div></div>'

def replace_mermaid(match):
    diagram = match.group(1).strip()
    return f'<div class="mermaid-wrap"><pre class="mermaid">\n{diagram}\n</pre></div>'

# Protect math blocks and inline formulas before markdown parsing
math_blocks = []
def save_block(m):
    idx = len(math_blocks)
    math_blocks.append(m.group(1))
    return f"@@MATH_BLOCK_{idx}@@"

processed_md = re.sub(r"\$\$(.*?)\$\$", save_block, raw_md, flags=re.DOTALL)

math_inlines = []
def save_inline(m):
    idx = len(math_inlines)
    math_inlines.append(m.group(1))
    return f"@@MATH_INLINE_{idx}@@"

processed_md = re.sub(r"\$([^\$\n]+)\$", save_inline, processed_md)

# Preprocess callouts
processed_md = re.sub(r"^>\s*\[!(\w+)\]([^\n]*(?:\n>[^\n]*)*)", replace_callout, processed_md, flags=re.MULTILINE)
processed_md = re.sub(r"```mermaid([\s\S]*?)```", replace_mermaid, processed_md)

# Convert markdown
md_extensions = ['tables', 'fenced_code', 'codehilite', 'def_list', 'nl2br']
html_body = markdown.markdown(processed_md, extensions=md_extensions)

# Responsive tables
html_body = html_body.replace("<table>", '<div class="table-wrapper"><table>')
html_body = html_body.replace("</table>", '</table></div>')

# Restore math blocks and inlines
for idx, b in enumerate(math_blocks):
    html_body = html_body.replace(f"@@MATH_BLOCK_{idx}@@", f'<div class="math-display">\\[{b.strip()}\\]</div>')
    html_body = re.sub(rf'<p>\s*(<div class="math-display">.*?</div>)\s*</p>', r'\1', html_body, flags=re.DOTALL)

for idx, i in enumerate(math_inlines):
    html_body = html_body.replace(f"@@MATH_INLINE_{idx}@@", f'<span class="math-inline">\\({i}\\)</span>')

# Generate Table of Contents from headings
headings = re.findall(r'<h([23])(?:\s+id="([^"]*)")?>(.*?)</h\1>', html_body)
toc_items = []
heading_counter = 0

def add_heading_id(match):
    global heading_counter
    level = match.group(1)
    title = match.group(2)
    heading_counter += 1
    slug = f"sec-{heading_counter}"
    clean_title = re.sub(r'<[^>]+>', '', title)
    toc_items.append((level, slug, clean_title))
    return f'<h{level} id="{slug}">{title}</h{level}>'

html_body = re.sub(r'<h([23])>(.*?)</h\1>', add_heading_id, html_body)

toc_html = '<div class="toc-wrap"><div class="toc-title"><span>🧭</span> Навигация по главам</div><ul class="toc-list">'
for level, slug, title in toc_items:
    indent = "toc-l2" if level == "2" else "toc-l3"
    toc_html += f'<li class="{indent}"><a href="#{slug}">{title}</a></li>'
toc_html += '</ul></div>'

# HTML Template
html_content = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Внутренний ток: Архитектура Человека (Канон Сверхпроводимости 3.0) — Владимир Аньянов</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"></script>
<script>
  document.addEventListener("DOMContentLoaded", function() {{
    function initKaTeX() {{
      if (typeof renderMathInElement === 'function') {{
        renderMathInElement(document.body, {{
          delimiters: [
            {{left: '$$', right: '$$', display: true}},
            {{left: '\\\\[', right: '\\\\]', display: true}},
            {{left: '\\\\(', right: '\\\\)', display: false}},
            {{left: '$', right: '$', display: false}}
          ],
          throwOnError: false
        }});
      }} else {{
        setTimeout(initKaTeX, 50);
      }}
    }}
    initKaTeX();
  }});
</script>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
  mermaid.initialize({{ startOnLoad: true, theme: 'dark' }});
</script>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Lora:ital,wght@0,400;0,500;0,600;1,400;1,500&family=JetBrains+Mono:wght@400;500;600&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

  :root {{
    --bg-page: #020617;
    --bg-card: #0b1329;
    --text-main: #f1f5f9;
    --text-muted: #94a3b8;
    --accent: #f59e0b;
    --accent-light: #fcd34d;
    --sky: #38bdf8;
    --border: #1e293b;
  }}

  * {{ box-sizing: border-box; }}

  body {{
    background: var(--bg-page);
    color: var(--text-main);
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 17px;
    line-height: 1.85;
    margin: 0;
    padding: 0;
    -webkit-font-smoothing: antialiased;
  }}

  .top-bar {{
    position: sticky;
    top: 0;
    z-index: 50;
    background: rgba(11, 19, 41, 0.95);
    backdrop-filter: blur(14px);
    border-bottom: 1px solid var(--border);
    padding: 12px 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}

  .top-brand {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 14px;
    font-weight: 700;
    color: var(--accent);
    display: flex;
    align-items: center;
    gap: 8px;
    text-decoration: none;
  }}

  .top-actions {{ display: flex; gap: 10px; align-items: center; }}

  .btn-action {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 12.5px;
    font-weight: 600;
    padding: 7px 14px;
    border-radius: 9px;
    border: 1px solid var(--border);
    background: #1e293b;
    color: #e2e8f0;
    cursor: pointer;
    text-decoration: none;
    transition: all 0.2s;
    display: inline-flex;
    align-items: center;
    gap: 6px;
  }}

  .btn-action:hover {{
    background: #334155;
    border-color: var(--accent);
  }}

  .btn-accent {{
    background: var(--accent);
    color: #020617;
    border: none;
    font-weight: 700;
  }}

  .btn-accent:hover {{ background: var(--accent-light); }}

  #read-progress {{
    position: fixed;
    top: 0;
    left: 0;
    height: 3px;
    background: linear-gradient(90deg, #f59e0b, #38bdf8);
    width: 0%;
    z-index: 100;
    transition: width 0.1s;
  }}

  .container {{
    max-width: 880px;
    margin: 0 auto;
    padding: 40px 24px 100px;
  }}

  .book-cover {{
    background: linear-gradient(180deg, rgba(245, 158, 11, 0.12) 0%, rgba(11, 19, 41, 0.8) 100%);
    border: 1px solid rgba(245, 158, 11, 0.35);
    border-radius: 24px;
    padding: 48px 36px;
    margin-bottom: 40px;
    text-align: center;
    box-shadow: 0 20px 50px -15px rgba(245, 158, 11, 0.15);
  }}

  .cover-badge {{
    display: inline-block;
    padding: 5px 14px;
    border-radius: 999px;
    background: rgba(245, 158, 11, 0.18);
    border: 1px solid rgba(245, 158, 11, 0.4);
    color: var(--accent-light);
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 18px;
  }}

  .cover-title {{
    font-family: 'Cinzel', serif;
    font-size: 34px;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.25;
    margin: 0 0 14px;
    text-shadow: 0 2px 25px rgba(245, 158, 11, 0.25);
  }}

  .cover-sub {{
    font-family: 'Lora', serif;
    font-size: 18px;
    color: #cbd5e1;
    font-style: italic;
    max-width: 720px;
    margin: 0 auto 20px;
    line-height: 1.6;
  }}

  .cover-meta {{
    font-size: 13px;
    color: var(--text-muted);
    border-top: 1px solid rgba(255,255,255,0.1);
    padding-top: 18px;
    max-width: 500px;
    margin: 0 auto;
  }}

  .toc-wrap {{
    background: rgba(11, 19, 41, 0.7);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px 28px;
    margin-bottom: 40px;
  }}

  .toc-title {{
    font-size: 15px;
    font-weight: 700;
    color: var(--accent-light);
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 8px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }}

  .toc-list {{
    list-style: none;
    padding: 0;
    margin: 0;
  }}

  .toc-list li {{
    margin-bottom: 6px;
    line-height: 1.5;
  }}

  .toc-list li a {{
    color: #94a3b8;
    text-decoration: none;
    font-size: 14px;
    transition: color 0.15s;
  }}

  .toc-list li a:hover {{
    color: var(--accent);
  }}

  .toc-l2 {{ font-weight: 600; margin-top: 10px; color: #f1f5f9; }}
  .toc-l3 {{ padding-left: 18px; font-size: 13.5px; }}

  article {{
    font-family: 'Lora', serif;
    font-size: 18.5px;
    color: #e2e8f0;
    line-height: 1.95;
  }}

  article h1, article h2, article h3, article h4 {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #ffffff;
    font-weight: 700;
    margin-top: 2.2em;
    margin-bottom: 0.7em;
    line-height: 1.35;
  }}

  article h1 {{ font-size: 28px; border-bottom: 1px solid var(--border); padding-bottom: 10px; }}
  article h2 {{ font-size: 24px; color: var(--accent-light); }}
  article h3 {{ font-size: 20px; color: var(--sky); }}
  article h4 {{ font-size: 17px; color: #cbd5e1; }}

  article p {{ margin: 1.3em 0; }}

  article strong {{ color: #ffffff; font-weight: 600; }}

  article em {{ font-style: italic; color: #f8fafc; }}

  article blockquote {{
    border-left: 3px solid var(--accent);
    padding-left: 20px;
    margin: 1.8em 0;
    color: #cbd5e1;
    font-style: italic;
    background: rgba(245, 158, 11, 0.03);
    padding: 14px 20px;
    border-radius: 0 10px 10px 0;
  }}

  .callout {{
    border-radius: 14px;
    padding: 20px 24px;
    margin: 2em 0;
    border: 1px solid var(--border);
    background: #0f172a;
  }}

  .callout-quote {{
    border-color: rgba(56, 189, 248, 0.4);
    background: rgba(56, 189, 248, 0.05);
  }}

  .callout-important, .callout-warning {{
    border-color: rgba(244, 63, 94, 0.4);
    background: rgba(244, 63, 94, 0.05);
  }}

  .callout-tip {{
    border-color: rgba(16, 185, 129, 0.4);
    background: rgba(16, 185, 129, 0.05);
  }}

  .callout-info {{
    border-color: rgba(96, 165, 250, 0.4);
    background: rgba(96, 165, 250, 0.05);
  }}

  .table-wrapper {{
    overflow-x: auto;
    margin: 2em 0;
    border: 1px solid var(--border);
    border-radius: 12px;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 14px;
  }}

  th, td {{
    padding: 12px 16px;
    text-align: left;
    border-bottom: 1px solid var(--border);
  }}

  th {{
    background: #1e293b;
    color: var(--accent);
    font-weight: 700;
  }}

  tr:last-child td {{ border-bottom: none; }}
  tr:hover td {{ background: rgba(255,255,255,0.02); }}

  code {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 14px;
    background: #1e293b;
    padding: 2px 6px;
    border-radius: 5px;
    color: #fcd34d;
  }}

  pre {{
    background: #0b1329;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px;
    overflow-x: auto;
  }}

  pre code {{
    background: none;
    padding: 0;
    font-size: 13.5px;
    line-height: 1.6;
    color: #e2e8f0;
  }}

  .mermaid-wrap {{
    background: #0b1329;
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px;
    margin: 2em 0;
    display: flex;
    justify-content: center;
  }}

  .math-display {{
    margin: 1.5em 0;
    text-align: center;
    overflow-x: auto;
  }}

  hr {{
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 3em 0;
  }}

  .footer-nav {{
    border-top: 1px solid var(--border);
    padding-top: 30px;
    margin-top: 60px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 14px;
  }}

  @media (max-width: 640px) {{
    .container {{ padding: 24px 16px 80px; }}
    .book-cover {{ padding: 32px 20px; }}
    .cover-title {{ font-size: 26px; }}
    article {{ font-size: 17px; line-height: 1.8; }}
  }}
</style>
</head>
<body>

<div id="read-progress"></div>

<header class="top-bar">
  <a href="../index.html" class="top-brand">
    <span>⚡</span> <span>ВНУТРЕННИЙ ТОК</span>
  </a>
  <div class="top-actions">
    <a href="../index.html" class="btn-action">← Портал</a>
    <a href="../trainer.html" class="btn-action">🎛️ Тренажер</a>
    <a href="/books/01_inner_current.pdf" download class="btn-action btn-accent">📥 PDF</a>
  </div>
</header>

<main class="container">
  <div class="book-cover">
    <div class="cover-badge">Библиотека «Золотая Семёрка 2.0» • Книга 1 (Фундамент N=1)</div>
    <h1 class="cover-title">Внутренний ток: Архитектура Человека</h1>
    <p class="cover-sub">Канон Сверхпроводимости 3.1: Прикладная соматическая электродинамика, схемотехника карманного фонарика и полный потенциал открытия И. Пригожина (N=1)</p>
    <div class="cover-meta">
      <strong>Автор:</strong> Владимир Аньянов • <strong>Редакция:</strong> 3.1 (Синтез на базе 535+ исследований)
    </div>
  </div>

  {toc_html}

  <article>
    {html_body}
  </article>

  <div class="footer-nav">
    <a href="../index.html" class="btn-action">← На главную портала</a>
    <a href="../trainer.html" class="btn-action">Открыть интерактивный тренажер →</a>
  </div>
</main>

<script>
  window.addEventListener('scroll', () => {{
    const totalHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = (window.scrollY / totalHeight) * 100;
    document.getElementById('read-progress').style.width = progress + '%';
  }});
</script>

</body>
</html>
"""

# Save to public/book/index.html & dist_site/book/index.html
out_book_public = os.path.join(PUBLIC_DIR, "book", "index.html")
out_book_dist = os.path.join(DIST_DIR, "book", "index.html")
os.makedirs(os.path.dirname(out_book_public), exist_ok=True)
os.makedirs(os.path.dirname(out_book_dist), exist_ok=True)

with open(out_book_public, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"Saved: {out_book_public}")

with open(out_book_dist, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"Saved: {out_book_dist}")

# Also save to books/01_inner_current.html
out_books_dist = os.path.join(DIST_DIR, "books", "01_inner_current.html")
out_books_pub = os.path.join(PUBLIC_DIR, "books", "01_inner_current.html")
with open(out_books_dist, "w", encoding="utf-8") as f:
    f.write(html_content)
with open(out_books_pub, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"Saved: {out_books_dist}")

# 2. Update dist_site/index.html and public/index.html
def update_index(index_path):
    if not os.path.exists(index_path):
        return
    with open(index_path, "r", encoding="utf-8") as f:
        idx = f.read()

    # Update Book 1 card title & subtitle & description
    old_card_h3 = '<h3 class="text-lg font-bold text-slate-100 group-hover:text-amber-300 transition">\n              Внутренний ток (Архитектура человека)\n            </h3>'
    new_card_h3 = '<h3 class="text-lg font-bold text-slate-100 group-hover:text-amber-300 transition">\n              Внутренний ток: Архитектура Человека (Канон 3.0)\n            </h3>'
    
    old_card_sub = '<p class="text-xs text-amber-400/90 font-medium mt-1">\n              Схемотехника карманного фонарика и соматическая сверхпроводимость\n            </p>'
    new_card_sub = '<p class="text-xs text-amber-400 font-medium mt-1">\n              Канон Сверхпроводимости: соматика N=1, полный потенциал Пригожина и протокол Self-Hosted Human\n            </p>'
    
    old_card_desc_pattern = r'<p class="text-xs text-slate-300 leading-relaxed font-serif">\s*Фундаментальный труд соматической физики[\s\S]*?</p>'
    new_card_desc = '<p class="text-xs text-slate-300 leading-relaxed font-serif">\n            Новейший канон на базе 535+ исследований: Русский синтез (Толстой, Достоевский, закон Джоуля — Ленца Q = I²·R·t), 100% раскрытие потенциала И. Пригожина (1977 и 1997), триада «Труба, Зажигалка, Фонарик», онтология «Дух — Личность — Эго» и мастер-протокол «Тело — Мысль — Дело».\n          </p>'

    if old_card_h3 in idx:
        idx = idx.replace(old_card_h3, new_card_h3, 1)
    if old_card_sub in idx:
        idx = idx.replace(old_card_sub, new_card_sub, 1)
    idx = re.sub(old_card_desc_pattern, new_card_desc, idx, count=1)

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(idx)
    print(f"Updated index: {index_path}")

update_index(os.path.join(DIST_DIR, "index.html"))
update_index(os.path.join(PUBLIC_DIR, "index.html"))

print("=== All builds completed successfully! ===")
