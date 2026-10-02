import os
import re
import markdown

SOURCE_MD = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Книга — Внутренний ток (Полевой мануал отладки).md"
OUTPUT_HTML = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\public\books\field_manual.html"

with open(SOURCE_MD, "r", encoding="utf-8") as f:
    raw_md = f.read()

# Preprocess Callouts (> [!quote], > [!important] etc.)
def replace_callout(match):
    ctype = match.group(1).lower()
    content = match.group(2)
    lines = [re.sub(r"^>\s?", "", line) for line in content.strip().split("\n")]
    title = lines[0].strip() if lines else ""
    body_lines = lines[1:] if len(lines) > 1 else []
    body_text = "\n".join(body_lines).strip()
    body_html = markdown.markdown(body_text, extensions=['tables', 'fenced_code', 'codehilite', 'def_list', 'nl2br'])
    title_html = f'<div class="callout-title" style="font-family: \'Plus Jakarta Sans\', sans-serif; font-size: 8.5pt; font-weight: 700; text-transform: uppercase; letter-spacing: 0.15em; color: #b45309; margin-bottom: 3mm;">{title}</div>' if title else ""
    return f'<div class="callout callout-{ctype}">{title_html}<div class="callout-body">{body_html}</div></div>'

processed_md = re.sub(r"^>\s*\[!(\w+)\]([^\n]*(?:\n>[^\n]*)*)", replace_callout, raw_md, flags=re.MULTILINE)

# Preprocess Parts and Chapters
processed_md = re.sub(r"^(## Часть [^\n]+)", r'<div class="part-header">\1</div>', processed_md, flags=re.MULTILINE)
processed_md = re.sub(r"^(### Глава [^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)

# Convert Markdown to HTML
md_extensions = ['tables', 'fenced_code', 'codehilite', 'def_list', 'nl2br']
html_body = markdown.markdown(processed_md, extensions=md_extensions)

# Wrap tables
html_body = html_body.replace("<table>", '<div class="table-wrapper"><table>')
html_body = html_body.replace("</table>", '</table></div>')

# Beautify math inline and display
html_body = re.sub(r"\$\$(.*?)\$\$", r'<div class="math-display">\1</div>', html_body, flags=re.DOTALL)
html_body = re.sub(r"\$([^\$\n]+)\$", r'<span class="math-inline">\1</span>', html_body)

FULL_HTML = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Внутренний ток: Полевой мануал отладки — Владимир Аньянов</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Lora:ital,wght@0,400;0,500;0,600;1,400;1,500&family=JetBrains+Mono:wght@400;500&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

  :root {{
    --bg-page: #030712;
    --bg-card: #0f172a;
    --text-main: #f1f5f9;
    --text-muted: #94a3b8;
    --accent: #f59e0b;
    --accent-light: #fbbf24;
    --border: #1e293b;
  }}

  * {{
    box-sizing: border-box;
  }}

  body {{
    background: var(--bg-page);
    color: var(--text-main);
    font-family: 'Lora', serif;
    font-size: 17px;
    line-height: 1.8;
    margin: 0;
    padding: 0;
    -webkit-font-smoothing: antialiased;
  }}

  /* Top sticky action bar */
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

  .top-actions {{
    display: flex;
    gap: 12px;
  }}

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
    color: #030712;
    border: none;
  }}

  .btn-accent:hover {{
    background: var(--accent-light);
  }}

  /* Main Reader Layout */
  .container {{
    max-width: 820px;
    margin: 40px auto 80px auto;
    padding: 0 24px;
  }}

  /* Cover Header */
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

  .book-cover::before {{
    content: '';
    position: absolute;
    top: -50px;
    left: 50%;
    transform: translateX(-50%);
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(245, 158, 11, 0.15) 0%, transparent 70%);
    pointer-events: none;
  }}

  .cover-badge {{
    display: inline-block;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--accent);
    background: rgba(245, 158, 11, 0.1);
    border: 1px solid rgba(245, 158, 11, 0.3);
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
    background: linear-gradient(135deg, #fef3c7 0%, #f59e0b 100%);
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

  /* Typography */
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

  p {{
    margin: 1.4em 0;
  }}

  strong {{
    color: #fff;
    font-weight: 600;
  }}

  em {{
    color: #cbd5e1;
  }}

  ul, ol {{
    padding-left: 28px;
    margin: 1.4em 0;
  }}

  li {{
    margin-bottom: 0.6em;
  }}

  /* Callouts */
  .callout {{
    margin: 28px 0;
    padding: 20px 24px;
    border-radius: 16px;
    background: #0f172a;
    border-left: 4px solid var(--accent);
    border: 1px solid #1e293b;
    border-left-width: 5px;
    border-left-color: var(--accent);
  }}

  .callout-important {{
    border-left-color: #ef4444;
    background: rgba(239, 68, 68, 0.05);
  }}

  .callout-quote {{
    border-left-color: #f59e0b;
    background: rgba(245, 158, 11, 0.05);
    font-style: italic;
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

  /* Table */
  .table-wrapper {{
    overflow-x: auto;
    margin: 24px 0;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 14px;
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

  /* Footer */
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
    <div class="cover-badge">Полевой гид • Аптечка скорой помощи</div>
    <h1 class="cover-title">Внутренний ток:<br>Полевой мануал отладки</h1>
    <div class="cover-sub">Практическая инженерия человека: как починить себя, когда горит проводка</div>
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

print("Generated:", OUTPUT_HTML)
