import os
import re
import markdown

SOURCE_MD = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\wiki\Inner Current (Primer for a Smart 10-Year-Old — The Architecture of Happiness and External Magnetism).md"
OUTPUT_HTML = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\public\books\primer.html"

with open(SOURCE_MD, "r", encoding="utf-8") as f:
    raw_md = f.read()

# Strip YAML frontmatter
raw_md = re.sub(r"^---[\s\S]*?---\n", "", raw_md)

# Preprocess Callouts (> [!quote], > [!tip], > [!important] etc.)
def replace_callout(match):
    ctype = match.group(1).lower()
    content = match.group(2)
    lines = [re.sub(r"^>\s?", "", line) for line in content.strip().split("\n")]
    title = lines[0].strip() if lines else ""
    body_lines = lines[1:] if len(lines) > 1 else []
    body_text = "\n".join(body_lines).strip()
    body_html = markdown.markdown(body_text, extensions=['tables', 'fenced_code', 'codehilite', 'def_list', 'nl2br'])
    title_html = f'<div class="callout-title" style="font-family: \'Plus Jakarta Sans\', sans-serif; font-size: 8.5pt; font-weight: 700; text-transform: uppercase; letter-spacing: 0.15em; color: #38bdf8; margin-bottom: 3mm;">{title}</div>' if title else ""
    return f'<div class="callout callout-{ctype}">{title_html}<div class="callout-body">{body_html}</div></div>'

processed_md = re.sub(r"^>\s*\[!(\w+)\]([^\n]*(?:\n>[^\n]*)*)", replace_callout, raw_md, flags=re.MULTILINE)

# Preprocess Mermaid diagram blocks so mermaid can render them
def replace_mermaid(match):
    diagram = match.group(1).strip()
    return f'<div class="mermaid-wrap"><pre class="mermaid">\n{diagram}\n</pre></div>'

processed_md = re.sub(r"```mermaid([\s\S]*?)```", replace_mermaid, processed_md)

# Beautify math inline and display
processed_md = re.sub(r"\$\$(.*?)\$\$", r'<div class="math-display">\1</div>', processed_md, flags=re.DOTALL)
processed_md = re.sub(r"\$([^\$\n]+)\$", r'<span class="math-inline">\1</span>', processed_md)

# Convert Markdown to HTML
md_extensions = ['tables', 'fenced_code', 'codehilite', 'def_list', 'nl2br']
html_body = markdown.markdown(processed_md, extensions=md_extensions)

FULL_HTML = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Инструкция к твоему суперкостюму: Праймер по физике счастья — Владимир Аньянов</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
  mermaid.initialize({{ startOnLoad: true, theme: 'dark' }});
</script>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Lora:ital,wght@0,400;0,500;0,600;1,400;1,500&family=JetBrains+Mono:wght@400;500&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

  :root {{
    --bg-page: #020617;
    --bg-card: #0f172a;
    --text-main: #f1f5f9;
    --text-muted: #94a3b8;
    --accent: #38bdf8;
    --accent-light: #7dd3fc;
    --border: #1e293b;
  }}

  * {{ box-sizing: border-box; }}

  body {{
    background: var(--bg-page);
    color: var(--text-main);
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 17px;
    line-height: 1.8;
    margin: 0;
    padding: 0;
    -webkit-font-smoothing: antialiased;
  }}

  .top-bar {{
    position: sticky;
    top: 0;
    z-index: 50;
    background: rgba(15, 23, 42, 0.85);
    backdrop-filter: blur(12px);
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

  .top-actions {{ display: flex; gap: 12px; }}

  .btn-action {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 13px;
    font-weight: 600;
    padding: 8px 16px;
    border-radius: 10px;
    border: 1px solid var(--border);
    background: #1e293b;
    color: #e2e8f0;
    cursor: pointer;
    text-decoration: none;
    transition: all 0.2s;
  }}

  .btn-action:hover {{
    background: #334155;
    border-color: var(--accent);
  }}

  .btn-accent {{
    background: var(--accent);
    color: #020617;
    border: none;
  }}

  .btn-accent:hover {{ background: var(--accent-light); }}

  .container {{
    max-width: 820px;
    margin: 40px auto 80px auto;
    padding: 0 24px;
  }}

  .book-cover {{
    background: linear-gradient(180deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
    border: 1px solid #334155;
    border-radius: 24px;
    padding: 60px 40px;
    text-align: center;
    margin-bottom: 60px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    position: relative;
    overflow: hidden;
  }}

  .cover-badge {{
    display: inline-block;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--accent);
    background: rgba(56, 189, 248, 0.1);
    border: 1px solid rgba(56, 189, 248, 0.3);
    padding: 6px 14px;
    border-radius: 9999px;
    margin-bottom: 24px;
  }}

  .cover-title {{
    font-family: 'Cinzel', serif;
    font-size: 38px;
    font-weight: 800;
    line-height: 1.2;
    margin: 0 0 16px 0;
    background: linear-gradient(135deg, #e0f2fe 0%, #38bdf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }}

  .cover-sub {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 18px;
    color: #cbd5e1;
    max-width: 600px;
    margin: 0 auto 24px auto;
    line-height: 1.5;
  }}

  .cover-meta {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 13px;
    color: var(--text-muted);
  }}

  h1, h2, h3, h4 {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #f8fafc;
    line-height: 1.3;
  }}

  h1 {{
    font-size: 28px;
    margin-top: 48px;
    border-bottom: 1px solid var(--border);
    padding-bottom: 12px;
  }}

  h2 {{
    font-size: 24px;
    margin-top: 44px;
    color: var(--accent-light);
  }}

  h3 {{
    font-size: 20px;
    margin-top: 36px;
    color: #e2e8f0;
  }}

  p {{ margin: 1.4em 0; }}
  strong {{ color: #fff; font-weight: 700; }}
  em {{ color: #cbd5e1; }}
  ul, ol {{ padding-left: 28px; margin: 1.4em 0; }}
  li {{ margin-bottom: 0.6em; }}

  /* Callouts */
  .callout {{
    margin: 28px 0;
    padding: 20px 24px;
    border-radius: 16px;
    background: #0f172a;
    border: 1px solid #1e293b;
    border-left: 5px solid var(--accent);
  }}

  .callout-quote {{
    border-left-color: #38bdf8;
    background: rgba(56, 189, 248, 0.05);
    font-style: italic;
  }}

  /* Mermaid Diagrams */
  .mermaid-wrap {{
    background: #090d16;
    border: 1px solid #1e293b;
    border-radius: 16px;
    padding: 20px;
    margin: 30px 0;
    display: flex;
    justify-content: center;
    overflow-x: auto;
  }}

  /* Math */
  .math-display {{
    background: #090d16;
    border: 1px solid #1e293b;
    padding: 16px;
    border-radius: 12px;
    margin: 20px 0;
    text-align: center;
    font-family: 'JetBrains Mono', monospace;
    color: #38bdf8;
    overflow-x: auto;
  }}

  .math-inline {{
    font-family: 'JetBrains Mono', monospace;
    background: rgba(56, 189, 248, 0.1);
    color: #38bdf8;
    padding: 2px 6px;
    border-radius: 6px;
    font-size: 0.9em;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 14px;
    margin: 24px 0;
  }}

  th, td {{
    padding: 12px 16px;
    border: 1px solid #1e293b;
    text-align: left;
  }}

  th {{
    background: #1e293b;
    color: #f1f5f9;
    font-weight: 600;
  }}

  hr {{
    border: 0;
    height: 1px;
    background: #1e293b;
    margin: 48px 0;
  }}

  footer {{
    text-align: center;
    padding: 40px 0;
    border-top: 1px solid var(--border);
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 13px;
    color: var(--text-muted);
  }}
</style>
</head>
<body>

<div class="top-bar">
  <a href="../index.html" class="top-brand">
    <span>⚡</span>
    <span>Inner Current • Библиотека</span>
  </a>
  <div class="top-actions">
    <button onclick="window.print()" class="btn-action">🖨️ Печать</button>
    <a href="../index.html" class="btn-action btn-accent">Вернуться на сайт ➔</a>
  </div>
</div>

<div class="container">
  <div class="book-cover">
    <div class="cover-badge">Праймер для детей и подростков • Возраст 10+</div>
    <h1 class="cover-title">Инструкция к твоему<br>суперкостюму</h1>
    <div class="cover-sub">Праймер по физике счастья и невидимой суперсиле для умных подростков, будущих изобретателей и капитанов своей жизни</div>
    <div class="cover-meta">Автор: Владимир Аньянов • Серия «Внутренний ток» • 2026</div>
  </div>

  <div class="book-content">
    {html_body}
  </div>

  <footer>
    © 2026 Владимир Аньянов. Все права защищены. Библиотека «Внутренний ток».
  </footer>
</div>

</body>
</html>
"""

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(FULL_HTML)

print("Generated Happiness Architecture Primer:", OUTPUT_HTML)
