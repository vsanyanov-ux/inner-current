import os
import re
import markdown
from playwright.sync_api import sync_playwright

SOURCE_MD = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\wiki\Книга — Коперник Сознания (Анатомия эго и физика внутренней свободы).md"
OUTPUT_HTML = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\public\books\copernicus.html"
OUTPUT_PDF = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\public\books\copernicus.pdf"

with open(SOURCE_MD, "r", encoding="utf-8") as f:
    raw_md = f.read()

# Strip YAML frontmatter if present
raw_md = re.sub(r"^---[\s\S]*?---\n", "", raw_md)

# Preprocess Callouts (> [!quote], > [!important], etc.)
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
        
    title_html = f'<div class="callout-title" style="font-family: \'Plus Jakarta Sans\', sans-serif; font-size: 9pt; font-weight: 700; text-transform: uppercase; letter-spacing: 0.12em; color: {accent_color}; margin-bottom: 8px; display: flex; items-center: center; gap: 6px;"><span>{icon}</span> <span>{title}</span></div>' if title else ""
    return f'<div class="callout callout-{ctype}">{title_html}<div class="callout-body">{body_html}</div></div>'

processed_md = re.sub(r"^>\s*\[!(\w+)\]([^\n]*(?:\n>[^\n]*)*)", replace_callout, raw_md, flags=re.MULTILINE)

# Preprocess Mermaid diagram blocks
def replace_mermaid(match):
    diagram = match.group(1).strip()
    return f'<div class="mermaid-wrap"><pre class="mermaid">\n{diagram}\n</pre></div>'

processed_md = re.sub(r"```mermaid([\s\S]*?)```", replace_mermaid, processed_md)

# Convert Markdown to HTML
md_extensions = ['tables', 'fenced_code', 'codehilite', 'def_list', 'nl2br']
html_body = markdown.markdown(processed_md, extensions=md_extensions)

# Wrap tables in responsive containers
html_body = html_body.replace("<table>", '<div class="table-wrapper"><table>')
html_body = html_body.replace("</table>", '</table></div>')

# Beautify math inline and display
html_body = re.sub(r"\$\$(.*?)\$\$", r'<div class="math-display">\[\1\]</div>', html_body, flags=re.DOTALL)
html_body = re.sub(r"\$([^\$\n]+)\$", r'<span class="math-inline">\(\1\)</span>', html_body)

FULL_HTML = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Коперник Сознания: Анатомия эго и физика внутренней свободы — Владимир Аньянов</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js" onload="renderMathInElement(document.body);"></script>
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

  /* Top Navigation Bar */
  .top-bar {{
    position: sticky;
    top: 0;
    z-index: 50;
    background: rgba(11, 19, 41, 0.9);
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

  /* Progress bar */
  #read-progress {{
    position: fixed;
    top: 0;
    left: 0;
    height: 3px;
    background: linear-gradient(90deg, #f59e0b, #38bdf8);
    z-index: 100;
    width: 0%;
    transition: width 0.1s;
  }}

  .container {{
    max-width: 840px;
    margin: 40px auto 100px auto;
    padding: 0 24px;
  }}

  /* Book Cover Card */
  .book-cover {{
    background: linear-gradient(180deg, rgba(30, 41, 59, 0.75) 0%, rgba(15, 23, 42, 0.95) 100%);
    border: 1px solid #334155;
    border-radius: 24px;
    padding: 60px 40px;
    text-align: center;
    margin-bottom: 60px;
    box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.7);
    position: relative;
    overflow: hidden;
  }}

  .book-cover::before {{
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at center, rgba(245, 158, 11, 0.08) 0%, transparent 60%);
    pointer-events: none;
  }}

  .cover-badge {{
    display: inline-block;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--accent);
    background: rgba(245, 158, 11, 0.12);
    border: 1px solid rgba(245, 158, 11, 0.35);
    padding: 6px 16px;
    border-radius: 9999px;
    margin-bottom: 24px;
  }}

  .cover-title {{
    font-family: 'Cinzel', serif;
    font-size: 38px;
    font-weight: 900;
    line-height: 1.2;
    margin: 0 0 16px 0;
    background: linear-gradient(135deg, #fef3c7 0%, #f59e0b 60%, #38bdf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }}

  .cover-sub {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 18px;
    color: #cbd5e1;
    max-width: 650px;
    margin: 0 auto 24px auto;
    line-height: 1.55;
  }}

  .cover-meta {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 13.5px;
    color: var(--text-muted);
  }}

  /* Typography */
  h1, h2, h3, h4 {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #f8fafc;
    line-height: 1.35;
  }}

  h1 {{
    font-size: 30px;
    font-weight: 800;
    margin-top: 56px;
    padding-bottom: 12px;
    border-bottom: 1px solid var(--border);
    background: linear-gradient(90deg, #f8fafc, #cbd5e1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }}

  h2 {{
    font-size: 22px;
    font-weight: 700;
    margin-top: 40px;
    color: #e2e8f0;
    display: flex;
    align-items: center;
    gap: 8px;
  }}

  h3 {{
    font-size: 18px;
    font-weight: 600;
    margin-top: 28px;
    color: var(--accent-light);
  }}

  p {{
    margin: 18px 0;
    color: #cbd5e1;
  }}

  strong {{
    color: #f8fafc;
    font-weight: 700;
  }}

  blockquote {{
    margin: 28px 0;
    padding: 20px 26px;
    border-left: 4px solid var(--accent);
    background: rgba(245, 158, 11, 0.05);
    border-radius: 0 16px 16px 0;
    color: #e2e8f0;
    font-style: italic;
  }}

  /* Callouts */
  .callout {{
    margin: 28px 0;
    padding: 22px 26px;
    border-radius: 16px;
    background: #0f172a;
    border: 1px solid var(--border);
  }}

  .callout-quote {{
    border-left: 4px solid var(--sky);
    background: rgba(56, 189, 248, 0.06);
  }}

  .callout-body p:last-child {{
    margin-bottom: 0;
  }}

  /* Code / Pre / ASCII Blocks */
  pre {{
    background: #060b19;
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px;
    overflow-x: auto;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13.5px;
    line-height: 1.55;
    color: #93c5fd;
    margin: 24px 0;
  }}

  code {{
    font-family: 'JetBrains Mono', monospace;
    background: rgba(30, 41, 59, 0.8);
    padding: 2px 6px;
    border-radius: 6px;
    font-size: 14px;
    color: #fde68a;
  }}

  pre code {{
    background: transparent;
    padding: 0;
    color: inherit;
  }}

  /* Tables */
  .table-wrapper {{
    overflow-x: auto;
    margin: 28px 0;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 14.5px;
  }}

  th, td {{
    padding: 12px 16px;
    border: 1px solid var(--border);
    text-align: left;
  }}

  th {{
    background: #0f172a;
    color: #f8fafc;
    font-weight: 700;
  }}

  td {{
    background: rgba(15, 23, 42, 0.5);
    color: #cbd5e1;
  }}

  /* Mermaid Diagram Wrappers */
  .mermaid-wrap {{
    margin: 32px 0;
    padding: 24px;
    background: #090e1e;
    border: 1px solid #1e293b;
    border-radius: 16px;
    display: flex;
    justify-content: center;
    overflow-x: auto;
  }}

  .mermaid {{
    text-align: center;
  }}

  /* Math display */
  .math-display {{
    margin: 24px 0;
    padding: 16px;
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid var(--border);
    border-radius: 12px;
    text-align: center;
    font-size: 1.15em;
    overflow-x: auto;
  }}

  ul, ol {{
    padding-left: 24px;
    margin: 18px 0;
    color: #cbd5e1;
  }}

  li {{
    margin-bottom: 8px;
  }}

  hr {{
    border: none;
    border-top: 1px solid var(--border);
    margin: 48px 0;
  }}

  /* Print Styles */
  @media print {{
    .top-bar, #read-progress, .top-actions {{ display: none !important; }}
    body {{ background: #fff !important; color: #000 !important; font-size: 11pt; }}
    .container {{ max-width: 100% !important; margin: 0 !important; padding: 0 !important; }}
    .book-cover {{ border: 1px solid #ccc; background: none; box-shadow: none; page-break-after: always; }}
    .cover-title {{ -webkit-text-fill-color: #000 !important; color: #000 !important; font-size: 26pt; }}
    h1 {{ -webkit-text-fill-color: #000 !important; color: #000 !important; page-break-before: always; }}
    h2, h3, h4 {{ color: #000 !important; }}
    p, li, td {{ color: #111 !important; }}
    pre, code {{ background: #f4f4f4 !important; color: #000 !important; border: 1px solid #ddd !important; }}
    blockquote, .callout {{ border-left-color: #333 !important; background: #fafafa !important; color: #000 !important; }}
  }}
</style>
</head>
<body>

<div id="read-progress"></div>

<header class="top-bar">
  <a href="../index.html" class="top-brand">
    <span style="font-size: 18px;">⚡</span>
    <span>Inner Current • Золотой Сикстет</span>
  </a>
  <div class="top-actions">
    <a href="../index.html" class="btn-action">
      <span>←</span> На главную
    </a>
    <button onclick="window.print()" class="btn-action">
      <span>🖨️</span> Печать
    </button>
    <a href="copernicus.pdf" download class="btn-action btn-accent">
      <span>📥</span> Скачать PDF
    </a>
  </div>
</header>

<main class="container">

  <div class="book-cover">
    <div class="cover-badge">Библиотека «Внутренний ток» • Книга III</div>
    <h1 class="cover-title">Коперник Сознания</h1>
    <div class="cover-sub">Анатомия эго и физика внутренней свободы: почему сопротивление не может быть проводником и как вернуть Солнце в центр существа</div>
    <div class="cover-meta">
      <strong>Владимир Аньянов</strong> • Каноническая мастер-рукопись • 2026
    </div>
  </div>

  <article id="book-content">
{html_body}
  </article>

</main>

<script>
  // Scroll reading progress indicator
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

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(FULL_HTML)

print(f"Generated HTML reader: {OUTPUT_HTML}")

# Generate PDF with Playwright
try:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file:///{OUTPUT_HTML.replace(os.sep, '/')}")
        page.wait_for_timeout(2000) # wait for KaTeX and fonts to render
        page.pdf(
            path=OUTPUT_PDF,
            format="A4",
            print_background=True,
            margin={"top": "20mm", "bottom": "20mm", "left": "20mm", "right": "20mm"}
        )
        browser.close()
    print(f"Generated PDF: {OUTPUT_PDF}")
except Exception as e:
    print(f"PDF generation error: {e}")
