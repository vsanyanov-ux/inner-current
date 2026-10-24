import os
import re
import shutil
import sys
import markdown
from playwright.sync_api import sync_playwright
import pypdf

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current"
VAULT_MD = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Брошюра — Оживление Вселенной (От энтропийного пессимизма к созидательному току бытия).md"
OUTPUT_HTML = os.path.join(ROOT_DIR, "living_universe_brochure.html")
OUTPUT_PDF = os.path.join(ROOT_DIR, "IC Library", "Брошюра — Оживление Вселенной (От энтропийного пессимизма к созидательному току бытия).pdf")
VAULT_PDF = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Брошюра — Оживление Вселенной (От энтропийного пессимизма к созидательному току бытия).pdf"
DIST_PDF = os.path.join(ROOT_DIR, "dist_site", "books", "living_universe.pdf")
PUB_PDF = os.path.join(ROOT_DIR, "public", "books", "living_universe.pdf")

with open(VAULT_MD, "r", encoding="utf-8") as f:
    raw_md = f.read()

# Strip YAML frontmatter
raw_md = re.sub(r"^---.*?---\s*", "", raw_md, flags=re.DOTALL)

# Preprocess Callouts (> [!quote] etc.)
def replace_callout(match):
    ctype = match.group(1).lower()
    content = match.group(2)
    lines = [re.sub(r"^>\s?", "", line) for line in content.strip().split("\n")]
    title = lines[0].strip() if lines else ""
    body_lines = lines[1:] if len(lines) > 1 else []
    body_text = "\n".join(body_lines).strip()
    body_html = markdown.markdown(body_text, extensions=['tables', 'fenced_code', 'codehilite', 'def_list', 'nl2br'])
    
    icon = "⚡"
    if "quote" in ctype: icon = "📜"
    elif "important" in ctype or "warning" in ctype: icon = "⚠️"
    elif "tip" in ctype: icon = "💡"
    elif "info" in ctype: icon = "ℹ️"
    
    title_html = f'<div class="callout-title"><span>{icon}</span> <span>{title}</span></div>' if title else ""
    return f'<div class="callout callout-{ctype}">{title_html}<div class="callout-body">{body_html}</div></div>'

processed_md = re.sub(r"^>\s*\[!(\w+)\]([^\n]*(?:\n>[^\n]*)*)", replace_callout, raw_md, flags=re.MULTILINE)

# Preprocess Parts to inject page-break classes
processed_md = re.sub(r"^(## Часть [^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)

# Convert Markdown to HTML
md_extensions = ['tables', 'fenced_code', 'codehilite', 'def_list', 'nl2br']
html_body = markdown.markdown(processed_md, extensions=md_extensions)

# Wrap tables in responsive containers
html_body = html_body.replace("<table>", '<div class="table-wrapper"><table>')
html_body = html_body.replace("</table>", '</table></div>')

# Beautify math inline and display
html_body = re.sub(r"\$\$(.*?)\$\$", r'<div class="math-display">\[\1\]</div>', html_body, flags=re.DOTALL)
html_body = re.sub(r"\$([^\$\n]+)\$", r'<span class="math-inline">\(\1\)</span>', html_body)

PDF_HTML_TEMPLATE = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Оживление Вселенной: От энтропийного пессимизма к созидательному току бытия — Владимир Аньянов</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js" onload="renderMathInElement(document.body);"></script>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Lora:ital,wght@0,400;0,500;0,600;1,400;1,500&family=JetBrains+Mono:wght@400;500&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

  @page {{
    size: A4;
    margin: 20mm 18mm 20mm 18mm;
    @bottom-center {{
      content: counter(page);
      font-family: 'JetBrains Mono', monospace;
      font-size: 8.5pt;
      color: #94a3b8;
    }}
  }}

  body {{
    font-family: 'Lora', serif;
    font-size: 10.5pt;
    line-height: 1.7;
    color: #1e293b;
    background: #ffffff;
    margin: 0;
    padding: 0;
  }}

  h1, h2, h3, h4 {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #0f172a;
    line-height: 1.3;
  }}

  h1 {{
    font-family: 'Cinzel', serif;
    font-size: 22pt;
    font-weight: 800;
    text-align: center;
    color: #0f172a;
    margin-top: 15pt;
    margin-bottom: 8pt;
    letter-spacing: 0.02em;
  }}

  .brochure-badge {{
    text-align: center;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 8pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: #0284c7;
    margin-bottom: 6pt;
  }}

  .brochure-meta {{
    text-align: center;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 9pt;
    color: #64748b;
    margin-bottom: 20pt;
    padding-bottom: 12pt;
    border-bottom: 1px solid #e2e8f0;
  }}

  h2 {{
    font-size: 13pt;
    font-weight: 700;
    border-bottom: 1.5px solid #0284c7;
    padding-bottom: 4pt;
    margin-top: 20pt;
    margin-bottom: 10pt;
    color: #0369a1;
  }}

  h3 {{
    font-size: 11pt;
    font-weight: 600;
    margin-top: 14pt;
    margin-bottom: 6pt;
  }}

  p {{
    margin-top: 0;
    margin-bottom: 10pt;
    text-align: justify;
  }}

  blockquote {{
    margin: 12pt 0;
    padding: 8pt 14pt;
    background: #f8fafc;
    border-left: 3px solid #0284c7;
    font-style: italic;
    color: #334155;
  }}

  pre {{
    background: #0f172a;
    color: #f8fafc;
    padding: 10pt 12pt;
    border-radius: 6px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 8pt;
    line-height: 1.45;
    overflow-x: auto;
    margin: 12pt 0;
  }}

  code {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5pt;
    background: #f1f5f9;
    padding: 1.5pt 3.5pt;
    border-radius: 3px;
    color: #0f172a;
  }}

  pre code {{
    background: transparent;
    padding: 0;
    color: inherit;
  }}

  .table-wrapper {{
    overflow-x: auto;
    margin: 12pt 0;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 9pt;
    font-family: 'Plus Jakarta Sans', sans-serif;
  }}

  th, td {{
    padding: 6pt 9pt;
    border: 1px solid #cbd5e1;
    text-align: left;
  }}

  th {{
    background: #f1f5f9;
    font-weight: 600;
    color: #0f172a;
  }}

  .callout {{
    margin: 12pt 0;
    padding: 10pt 14pt;
    border-radius: 6px;
    background: #f8fafc;
    border-left: 4px solid #0284c7;
  }}

  .callout-quote {{
    border-left-color: #0284c7;
    background: #f0f9ff;
  }}

  .callout-title {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 700;
    font-size: 9.5pt;
    margin-bottom: 5pt;
    color: #0369a1;
    display: flex;
    align-items: center;
    gap: 6px;
  }}

  .callout-body p:last-child {{
    margin-bottom: 0;
  }}

  .chapter-break {{
    page-break-before: always;
  }}

  .math-display {{
    text-align: center;
    margin: 10pt 0;
  }}
</style>
</head>
<body>

  <div class="brochure-badge">Библиотека «Внутренний ток» • Специальный выпуск • Манифест</div>
  <h1>Оживление Вселенной</h1>
  <div style="text-align:center; font-family:'Lora',serif; font-size:12pt; font-style:italic; color:#475569; margin-bottom:10pt;">
    От энтропийного пессимизма к созидательному току бытия: почему счастье — это оптический прибор живого космоса, а творчество — прямое проведение негэнтропии
  </div>
  <div class="brochure-meta">
    Автор: <strong>Владимир Аньянов</strong> • Мастер-манифест • Октябрь 2026
  </div>

  {html_body}

</body>
</html>
"""

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(PDF_HTML_TEMPLATE)
print(f"Written temp brochure HTML: {OUTPUT_HTML}")

# Generate PDF with Playwright
print("Compiling brochure PDF with Playwright...")
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"file:///{os.path.abspath(OUTPUT_HTML).replace(os.sep, '/')}", wait_until="networkidle")
    page.wait_for_timeout(2000)
    page.pdf(
        path=OUTPUT_PDF,
        format="A4",
        print_background=True,
        margin={"top": "20mm", "bottom": "20mm", "left": "18mm", "right": "18mm"}
    )
    browser.close()

reader = pypdf.PdfReader(OUTPUT_PDF)
print(f"PDF generated: {OUTPUT_PDF} ({len(reader.pages)} pages)")

# Sync PDF to Vault, dist_site, and public
shutil.copy2(OUTPUT_PDF, VAULT_PDF)
if os.path.exists(os.path.dirname(DIST_PDF)):
    shutil.copy2(OUTPUT_PDF, DIST_PDF)
if os.path.exists(os.path.dirname(PUB_PDF)):
    shutil.copy2(OUTPUT_PDF, PUB_PDF)
print(f"Synced PDF to Vault: {VAULT_PDF}")

# Sync HTML Reader for website
dist_html = os.path.join(ROOT_DIR, "dist_site", "books", "living_universe.html")
pub_html = os.path.join(ROOT_DIR, "public", "books", "living_universe.html")
shutil.copy2(OUTPUT_HTML, dist_html)
shutil.copy2(OUTPUT_HTML, pub_html)
print(f"Synced HTML reader to {dist_html} and {pub_html}")

if os.path.exists(OUTPUT_HTML):
    os.remove(OUTPUT_HTML)
print("Brochure build and sync completed successfully!")
