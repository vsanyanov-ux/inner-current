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
VAULT_MD = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Брошюра — Двухконтурный человек (Тело Пригожина, Дух Аньянова и физика счастья).md"
OUTPUT_HTML = os.path.join(ROOT_DIR, "dual_circuit_brochure.html")
OUTPUT_PDF = os.path.join(ROOT_DIR, "IC Library", "Брошюра — Двухконтурный человек (Тело Пригожина, Дух Аньянова и физика счастья).pdf")
VAULT_PDF = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Брошюра — Двухконтурный человек (Тело Пригожина, Дух Аньянова и физика счастья).pdf"
DIST_PDF = os.path.join(ROOT_DIR, "dist_site", "books", "dual_circuit.pdf")
DIST_HTML = os.path.join(ROOT_DIR, "dist_site", "books", "dual_circuit.html")
PUB_PDF = os.path.join(ROOT_DIR, "public", "books", "dual_circuit.pdf")
PUB_HTML = os.path.join(ROOT_DIR, "public", "books", "dual_circuit.html")

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
processed_md = re.sub(r"^(### ЧАСТЬ [^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
processed_md = re.sub(r"^(### ДАШБОРД ОПЕРАТОРА[^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
processed_md = re.sub(r"^(### Резюме[^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)

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
<title>Двухконтурный человек: Тело Пригожина, Дух Аньянова и физика счастья — Владимир Аньянов</title>
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
    font-size: 23pt;
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
    color: #d97706;
    margin-bottom: 8pt;
  }}

  .brochure-meta {{
    text-align: center;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 9pt;
    color: #64748b;
    margin-bottom: 22pt;
    border-bottom: 1.5pt solid #e2e8f0;
    padding-bottom: 12pt;
  }}

  h2 {{
    font-size: 15pt;
    margin-top: 18pt;
    margin-bottom: 8pt;
    border-bottom: 1pt solid #e2e8f0;
    padding-bottom: 4pt;
    color: #0f172a;
  }}

  h3 {{
    font-size: 12pt;
    margin-top: 16pt;
    margin-bottom: 6pt;
    color: #b45309;
  }}

  h4 {{
    font-size: 10.5pt;
    margin-top: 12pt;
    margin-bottom: 4pt;
    color: #334155;
  }}

  p {{
    margin-top: 0;
    margin-bottom: 8pt;
    text-align: justify;
  }}

  strong {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 700;
    color: #0f172a;
  }}

  code {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 9pt;
    background: #f1f5f9;
    padding: 1pt 3pt;
    border-radius: 3pt;
    color: #0f172a;
  }}

  pre {{
    background: #0f172a;
    color: #f8fafc;
    font-family: 'JetBrains Mono', monospace;
    font-size: 8pt;
    line-height: 1.45;
    padding: 10pt 12pt;
    border-radius: 6pt;
    overflow-x: auto;
    margin: 12pt 0;
  }}

  pre code {{
    background: transparent;
    color: #f8fafc;
    padding: 0;
  }}

  .callout {{
    margin: 12pt 0;
    padding: 10pt 14pt;
    border-radius: 6pt;
    border-left: 3.5pt solid #d97706;
    background: #fffbeb;
  }}

  .callout-title {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 8.5pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #b45309;
    margin-bottom: 4pt;
  }}

  .callout-body p {{
    margin-bottom: 4pt;
    font-size: 10pt;
  }}

  .chapter-break {{
    page-break-before: always;
  }}

  .table-wrapper {{
    margin: 12pt 0;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 9pt;
  }}

  th, td {{
    padding: 6pt 8pt;
    border-bottom: 1pt solid #e2e8f0;
    text-align: left;
  }}

  th {{
    background: #f8fafc;
    color: #0f172a;
    font-weight: 700;
  }}

  .math-display {{
    text-align: center;
    margin: 10pt 0;
  }}
</style>
</head>
<body>

  <div class="brochure-badge">Библиотека «Внутренний ток» • Специальный выпуск • Манифест</div>
  <h1>Двухконтурный человек</h1>
  <div style="text-align:center; font-family:'Lora',serif; font-size:12pt; font-style:italic; color:#475569; margin-bottom:10pt;">
    Тело Пригожина, Дух Аньянова и физика счастья: как Нобелевская премия 1977 года объяснила соматический контур 2026-го
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
    # Wait for KaTeX
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
shutil.copy2(OUTPUT_PDF, DIST_PDF)
shutil.copy2(OUTPUT_PDF, PUB_PDF)
print(f"Synced PDF to Vault: {VAULT_PDF}")
print(f"Synced PDF to dist_site: {DIST_PDF}")

# Also build interactive dark-mode Web Reader for the brochure
sys.path.insert(0, os.path.dirname(__file__))
from build_fractal_and_law_readers import render_book_reader
render_book_reader(
    md_filename="Брошюра — Двухконтурный человек (Тело Пригожина, Дух Аньянова и физика счастья).md",
    out_html_name="dual_circuit.html",
    book_title="Двухконтурный человек",
    book_sub="Тело Пригожина, Дух Аньянова и физика счастья: почему идеальное тело не гарантирует счастья и как устроен второй вихрь внимания",
    badge_text="Библиотека «Внутренний ток» • Манифест • Специальный выпуск",
    pdf_name="dual_circuit.pdf"
)
print("Dual Circuit Web Reader built successfully!")
