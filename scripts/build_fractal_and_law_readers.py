import os
import re
import sys
import markdown

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current"
LIB_DIR = os.path.join(ROOT_DIR, "IC Library", "Золотая семерка 2.0")
DIST_BOOKS = os.path.join(ROOT_DIR, "dist_site", "books")
PUB_BOOKS = os.path.join(ROOT_DIR, "public", "books")

def replace_callout(match):
    ctype = match.group(1).lower()
    content = match.group(2)
    lines = [re.sub(r"^>\s?", "", line) for line in content.strip().split("\n")]
    title = lines[0].strip() if lines else ""
    body_lines = lines[1:] if len(lines) > 1 else []
    body_text = "\n".join(body_lines).strip()
    body_html = markdown.markdown(body_text, extensions=['tables', 'fenced_code', 'codehilite', 'def_list', 'nl2br'])
    
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
        
    title_html = f'<div class="callout-title" style="font-family: \'Plus Jakarta Sans\', sans-serif; font-size: 9pt; font-weight: 700; text-transform: uppercase; letter-spacing: 0.12em; color: {accent_color}; margin-bottom: 8px; display: flex; align-items: center; gap: 6px;"><span>{icon}</span> <span>{title}</span></div>' if title else ""
    return f'<div class="callout callout-{ctype}">{title_html}<div class="callout-body">{body_html}</div></div>'

def replace_mermaid(match):
    diagram = match.group(1).strip()
    return f'<div class="mermaid-wrap"><pre class="mermaid">\n{diagram}\n</pre></div>'

def render_book_reader(md_filename, out_html_name, book_title, book_sub, badge_text, pdf_name):
    md_path = os.path.join(LIB_DIR, md_filename)
    with open(md_path, "r", encoding="utf-8") as f:
        raw_md = f.read()

    # Strip YAML frontmatter
    raw_md = re.sub(r"^---[\s\S]*?---\n", "", raw_md)
    # Strip Obsidian WikiLinks
    raw_md = re.sub(r"\[\[(?:[^|\]]*\\?\|)?([^\]]+)\]\]", r"\1", raw_md)

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

    # Preprocess mermaid
    processed_md = re.sub(r"```mermaid([\s\S]*?)```", replace_mermaid, processed_md)

    # Convert to HTML
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

    template = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{book_title} — Владимир Аньянов</title>
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
    background: rgba(11, 19, 41, 0.92);
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
    max-width: 860px;
    margin: 0 auto;
    padding: 40px 24px 100px;
  }}

  .book-cover {{
    background: linear-gradient(180deg, rgba(245, 158, 11, 0.08) 0%, rgba(11, 19, 41, 0.6) 100%);
    border: 1px solid rgba(245, 158, 11, 0.25);
    border-radius: 20px;
    padding: 48px 36px;
    margin-bottom: 50px;
    text-align: center;
    box-shadow: 0 20px 40px -15px rgba(0,0,0,0.5);
  }}

  .cover-badge {{
    display: inline-block;
    padding: 4px 12px;
    border-radius: 999px;
    background: rgba(245, 158, 11, 0.15);
    border: 1px solid rgba(245, 158, 11, 0.35);
    color: var(--accent);
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 16px;
  }}

  .cover-title {{
    font-family: 'Cinzel', serif;
    font-size: 34px;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.25;
    margin: 0 0 14px;
    text-shadow: 0 2px 20px rgba(245, 158, 11, 0.2);
  }}

  .cover-sub {{
    font-family: 'Lora', serif;
    font-size: 18px;
    color: #cbd5e1;
    font-style: italic;
    max-width: 700px;
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

  article {{
    font-family: 'Lora', serif;
    font-size: 18px;
    color: #e2e8f0;
    line-height: 1.95;
  }}

  article h1, article h2, article h3, article h4 {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #ffffff;
    font-weight: 700;
    margin-top: 2.2em;
    margin-bottom: 0.8em;
    line-height: 1.35;
  }}

  article h1 {{
    font-size: 28px;
    border-bottom: 1px solid var(--border);
    padding-bottom: 12px;
    color: var(--accent-light);
  }}

  article h2 {{
    font-size: 23px;
    color: #f8fafc;
  }}

  article h3 {{
    font-size: 19px;
    color: #38bdf8;
  }}

  article p {{
    margin: 1.2em 0;
  }}

  article strong {{
    color: #ffffff;
    font-weight: 600;
  }}

  article a {{
    color: var(--accent);
    text-decoration: underline;
    text-underline-offset: 3px;
  }}

  article hr {{
    border: none;
    border-top: 1px solid var(--border);
    margin: 40px 0;
  }}

  article blockquote {{
    border-left: 3px solid var(--accent);
    padding: 12px 20px;
    margin: 24px 0;
    background: rgba(245, 158, 11, 0.05);
    border-radius: 0 10px 10px 0;
    color: #cbd5e1;
    font-style: italic;
  }}

  .callout {{
    margin: 24px 0;
    padding: 18px 22px;
    border-radius: 12px;
    border: 1px solid var(--border);
    background: rgba(15, 23, 42, 0.8);
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

  .callout-body p {{ margin: 0.6em 0; font-size: 16px; }}

  .table-wrapper {{
    overflow-x: auto;
    margin: 24px 0;
    border-radius: 10px;
    border: 1px solid var(--border);
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 15px;
  }}

  th, td {{
    padding: 12px 16px;
    border-bottom: 1px solid var(--border);
    text-align: left;
  }}

  th {{
    background: #0f172a;
    color: var(--accent);
    font-weight: 700;
  }}

  td {{ background: #070d1d; }}

  code {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 14.5px;
    padding: 2px 6px;
    background: #1e293b;
    border-radius: 5px;
    color: #fcd34d;
  }}

  pre {{
    background: #090e1a;
    border: 1px solid var(--border);
    padding: 16px 20px;
    border-radius: 10px;
    overflow-x: auto;
  }}

  pre code {{
    background: transparent;
    padding: 0;
    color: #e2e8f0;
  }}

  .math-display {{
    overflow-x: auto;
    padding: 12px 0;
    text-align: center;
  }}

  .mermaid-wrap {{
    margin: 24px 0;
    padding: 20px;
    background: #070d1d;
    border: 1px solid var(--border);
    border-radius: 12px;
    text-align: center;
  }}
</style>
</head>
<body>

<div id="read-progress"></div>

<header class="top-bar">
  <a href="/" class="top-brand">
    <span>⚡</span>
    <span>Внутренний ток • Ридер</span>
  </a>
  <div class="top-actions">
    <a href="/" class="btn-action">
      <span>🔙</span> В библиотеку
    </a>
    <a href="{pdf_name}" download class="btn-action btn-accent">
      <span>📥</span> Скачать PDF
    </a>
  </div>
</header>

<main class="container">

  <div class="book-cover">
    <div class="cover-badge">{badge_text}</div>
    <h1 class="cover-title">{book_title}</h1>
    <div class="cover-sub">{book_sub}</div>
    <div class="cover-meta">
      <strong>Владимир Аньянов</strong> • Каноническая мастер-рукопись • 2026
    </div>
  </div>

  <article id="book-content">
{html_body}
  </article>

</main>

<script>
  window.addEventListener('scroll', () => {{
    const winScroll = document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (winScroll / height) * 100;
    document.getElementById('read-progress').style.width = scrolled + '%';
  }});
</script>

</body>
</html>
"""
    out_dist = os.path.join(DIST_BOOKS, out_html_name)
    out_pub = os.path.join(PUB_BOOKS, out_html_name)
    with open(out_dist, "w", encoding="utf-8") as f:
        f.write(template)
    with open(out_pub, "w", encoding="utf-8") as f:
        f.write(template)
    print(f"Generated reader: {out_html_name} ({len(template)} bytes)")

# 1. Book 02: Четверичный фрактал цепи
render_book_reader(
    md_filename="02 — Владимир Аньянов — Четверичный фрактал цепи (Архитектурный инвариант природы — от клетки и фонарика до Биткоина и общества).md",
    out_html_name="quaternary_fractal.html",
    book_title="Четверичный фрактал цепи",
    book_sub="Архитектурный инвариант природы: от клетки и фонарика до Биткоина и общества",
    badge_text="Библиотека «Внутренний ток» • Золотая Семёрка 2.0 • Книга 2 (Стены)",
    pdf_name="02_quaternary_fractal.pdf"
)

# 2. Book 03: Универсальный закон потоковых систем
render_book_reader(
    md_filename="03 — Владимир Аньянов — Универсальный закон потоковых систем (Термодинамика негэнтропии, открытые системы и КПД бытия).md",
    out_html_name="universal_law.html",
    book_title="Универсальный закон потоковых систем",
    book_sub="Термодинамика негэнтропии, открытые системы и КПД бытия",
    badge_text="Библиотека «Внутренний ток» • Золотая Семёрка 2.0 • Книга 3 (Крыша)",
    pdf_name="03_universal_law.pdf"
)

# 3. Book 04: Тайна карманного фонарика (Детский праймер)
for primer_html in ["primer_flashlight.html", "primer.html"]:
    render_book_reader(
        md_filename="04 — Владимир Аньянов — Тайна карманного фонарика (Внутренний ток для детей и подростков — как устроена твоя суперсила).md",
        out_html_name=primer_html,
        book_title="Тайна карманного фонарика",
        book_sub="Внутренний ток для детей и подростков — как устроена твоя суперсила",
        badge_text="Библиотека «Внутренний ток» • Золотая Семёрка 2.0 • Книга 4 (Детский праймер)",
        pdf_name="04_flashlight_primer.pdf"
    )

# 4. Book 05: Полевой мануал оператора
render_book_reader(
    md_filename="05 — Владимир Аньянов — Полевой мануал оператора (Карманная аптечка первой помощи — 30-секундный протокол соматической отладки).md",
    out_html_name="field_manual.html",
    book_title="Полевой мануал оператора",
    book_sub="Карманная аптечка первой помощи — 30-секундный протокол соматической отладки",
    badge_text="Библиотека «Внутренний ток» • Золотая Семёрка 2.0 • Книга 5 (Аптечка 30 сек)",
    pdf_name="05_field_manual.pdf"
)

# 5. Book 06: Укулеле Бытия
render_book_reader(
    md_filename="06 — Владимир Аньянов — Укулеле Бытия (Акустическая физика счастливой жизни — материя, звук и резонанс Мусин).md",
    out_html_name="ukulele.html",
    book_title="Укулеле Бытия",
    book_sub="Акустическая физика счастливой жизни — материя, звук и резонанс Мусин",
    badge_text="Библиотека «Внутренний ток» • Золотая Семёрка 2.0 • Книга 6 (Акустический монизм)",
    pdf_name="06_ukulele.pdf"
)

# 6. Book 07: Великий Синтез
render_book_reader(
    md_filename="07 — Владимир Аньянов — Великий Синтез (Революции материи, трагедия духа и электродинамика человека).md",
    out_html_name="great_synthesis.html",
    book_title="Великий Синтез",
    book_sub="Революции материи, трагедия духа и электродинамика человека",
    badge_text="Библиотека «Внутренний ток» • Золотая Семёрка 2.0 • Книга 7 (Макроистория • Master Edition 2.0)",
    pdf_name="07_great_synthesis.pdf"
)
