import os
import re
import sys
import shutil
import markdown
from playwright.sync_api import sync_playwright
import pypdf

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

VAULT_MD = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Книга — Великий Синтез (Революции материи, трагедия духа и электродинамика человека).md"
OUTPUT_HTML = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\great_synthesis_book.html"
OUTPUT_PDF = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\Книга — Великий Синтез (Революции материи, трагедия духа и электродинамика человека).pdf"
PDF_VAULT = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Книга — Великий Синтез (Революции материи, трагедия духа и электродинамика человека).pdf"
PDF_LIB = r"C:\Users\vanya\Antigravity Projects\Apps\Inner Current\IC Library\Золотая семерка\v2 Великий Синтез (Революции материи, трагедия духа и электродинамика человека).pdf"
PDF_LIB_2 = r"C:\Users\vanya\Antigravity Projects\Apps\Inner Current\IC Library\Золотая семерка 2.0\07 — Владимир Аньянов — Великий Синтез (Революции материи, трагедия духа и электродинамика человека).pdf"

with open(VAULT_MD, "r", encoding="utf-8") as f:
    raw_md = f.read()

# Strip frontmatter
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
    title_html = f'<div class="callout-title" style="font-family: \'Plus Jakarta Sans\', sans-serif; font-size: 8.5pt; font-weight: 700; text-transform: uppercase; letter-spacing: 0.15em; color: #8c8275; margin-bottom: 3mm;">{title}</div>' if title else ""
    return f'<div class="callout callout-{ctype}">{title_html}<div class="callout-body">{body_html}</div></div>'

processed_md = re.sub(r"^>\s*\[!(\w+)\]([^\n]*(?:\n>[^\n]*)*)", replace_callout, raw_md, flags=re.MULTILINE)

# Preprocess Parts and Chapters to inject page-break classes
processed_md = re.sub(r"^(# Часть [^\n]+)", r'<div class="part-header">\1</div>', processed_md, flags=re.MULTILINE)
processed_md = re.sub(r"^(## Глава [^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
processed_md = re.sub(r"^(# Заключение[^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)

# Convert Markdown to HTML
md_extensions = ['tables', 'fenced_code', 'codehilite', 'def_list', 'nl2br']
html_body = markdown.markdown(processed_md, extensions=md_extensions)

# Remove the initial H1 title and subtitle from body (since they are in the cover)
html_body = re.sub(r"<h1>.*?</h1>\s*<h2>.*?</h2>", "", html_body, count=1, flags=re.DOTALL)

# Wrap tables in responsive containers
html_body = html_body.replace("<table>", '<div class="table-wrapper"><table>')
html_body = html_body.replace("</table>", '</table></div>')

# Beautify math inline and display while preserving clean delimiters for KaTeX
html_body = re.sub(r"\$\$(.*?)\$\$", r'<div class="math-display">\\[\1\\]</div>', html_body, flags=re.DOTALL)
html_body = re.sub(r"(?<!\\)\$([^\$\n]+?)(?<!\\)\$", r'<span class="math-inline">\\(\1\\)</span>', html_body)

KATEX_SCRIPTS = r"""
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"></script>
<script>
  window.addEventListener('load', () => {
    if (typeof renderMathInElement !== 'undefined') {
      renderMathInElement(document.body, {
        delimiters: [
          {left: '$$', right: '$$', display: true},
          {left: '\\[', right: '\\]', display: true},
          {left: '\\(', right: '\\)', display: false},
          {left: '$', right: '$', display: false}
        ],
        throwOnError: false
      });
    }
    window.katexDone = true;
  });
</script>
"""

FULL_HTML = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Великий Синтез: Революции Материи, Трагедия Духа и Электродинамика Человека</title>
{KATEX_SCRIPTS}
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=Lora:ital,wght@0,400;0,500;0,600;1,400;1,500&family=JetBrains+Mono:wght@400;500&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

  @page {{
    size: A4;
    margin: 22mm 18mm 22mm 18mm;
  }}

  * {{
    box-sizing: border-box;
  }}

  body {{
    font-family: 'Lora', 'Georgia', serif;
    font-size: 11pt;
    line-height: 1.68;
    color: #24292f;
    background-color: #ffffff;
    margin: 0;
    padding: 0;
    text-rendering: optimizeLegibility;
    -webkit-font-smoothing: antialiased;
  }}

  /* COVER PAGE */
  .cover-page {{
    page-break-after: always;
    height: 100vh;
    min-height: 250mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    text-align: center;
    padding: 30mm 15mm 20mm 15mm;
    background: radial-gradient(circle at 50% 30%, #ffffff 0%, #faf8f5 100%);
    border: 1px solid #eae5df;
    position: relative;
  }}

  .cover-series {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 8.5pt;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #8c8275;
    font-weight: 600;
  }}

  .cover-hero {{
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 15mm;
  }}

  .cover-emblem {{
    width: 68px;
    height: 68px;
    margin-bottom: 8mm;
    color: #bfa15f;
  }}

  .cover-author {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 13pt;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #4a453e;
    font-weight: 500;
    margin-bottom: 6mm;
  }}

  .cover-title {{
    font-family: 'Cinzel', 'Lora', serif;
    font-size: 28pt;
    font-weight: 700;
    line-height: 1.15;
    color: #1a1816;
    letter-spacing: 0.04em;
    margin: 0 0 5mm 0;
  }}

  .cover-divider {{
    width: 60px;
    height: 2px;
    background: #bfa15f;
    margin: 4mm 0 6mm 0;
  }}

  .cover-subtitle {{
    font-family: 'Lora', serif;
    font-size: 13pt;
    font-style: italic;
    color: #615a51;
    max-width: 520px;
    margin: 0 auto 8mm auto;
    line-height: 1.45;
  }}

  .cover-tagline {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 9.5pt;
    color: #7d756a;
    max-width: 480px;
    line-height: 1.55;
    font-weight: 400;
  }}

  .cover-footer {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 8.5pt;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #999083;
  }}

  /* EPIGRAPH / FRONTISPIECE */
  .frontispiece {{
    page-break-after: always;
    min-height: 240mm;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 40mm 15mm;
  }}

  .frontispiece-quote {{
    max-width: 540px;
    font-size: 12.5pt;
    font-style: italic;
    line-height: 1.75;
    color: #3d3730;
    text-align: center;
    position: relative;
    padding: 0 10mm;
  }}

  .frontispiece-quote::before {{
    content: "“";
    font-family: 'Cinzel', serif;
    font-size: 50pt;
    position: absolute;
    top: -25px;
    left: -10px;
    color: #dfd7cc;
  }}

  .frontispiece-author {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 9.5pt;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #8c8275;
    margin-top: 8mm;
    font-weight: 600;
  }}

  /* HEADINGS & BREAKS */
  .part-header {{
    page-break-before: always;
    margin-top: 15mm;
    margin-bottom: 10mm;
    border-bottom: 2px solid #1a1816;
    padding-bottom: 4mm;
  }}

  .part-header h1 {{
    font-family: 'Cinzel', serif;
    font-size: 20pt;
    color: #1a1816;
    letter-spacing: 0.05em;
    margin: 0;
  }}

  .chapter-break {{
    page-break-before: always;
  }}

  h2 {{
    font-family: 'Lora', serif;
    font-size: 15pt;
    font-weight: 600;
    color: #1a1816;
    margin-top: 8mm;
    margin-bottom: 4mm;
    line-height: 1.35;
    break-after: avoid;
  }}

  h3 {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 12pt;
    font-weight: 600;
    color: #3a352f;
    margin-top: 6mm;
    margin-bottom: 3mm;
    break-after: avoid;
  }}

  p {{
    margin: 0 0 3.5mm 0;
    text-align: justify;
    hyphens: auto;
  }}

  strong {{
    font-weight: 600;
    color: #141210;
  }}

  em {{
    font-style: italic;
  }}

  /* CALLOUTS */
  .callout {{
    margin: 5mm 0 6mm 0;
    padding: 4mm 5mm;
    background: #fbf9f6;
    border-left: 3px solid #bfa15f;
    border-radius: 2px;
    break-inside: avoid;
  }}

  .callout-quote {{
    border-left-color: #bfa15f;
    background: #faf7f2;
  }}

  .callout-body p:last-child {{
    margin-bottom: 0;
  }}

  /* CODE & DIAGRAMS */
  pre {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.5pt;
    line-height: 1.35;
    background-color: #f7f5f2;
    border: 1px solid #e5dfd7;
    border-radius: 4px;
    padding: 3.5mm 4mm;
    margin: 4mm 0 5mm 0;
    overflow-x: auto;
    color: #2b2723;
    break-inside: avoid;
  }}

  code {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5pt;
    background-color: #f3efe9;
    padding: 1px 4px;
    border-radius: 3px;
    color: #2b2723;
  }}

  /* TABLES */
  .table-wrapper {{
    margin: 4mm 0 6mm 0;
    break-inside: avoid;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 8.5pt;
    line-height: 1.45;
  }}

  th, td {{
    border: 1px solid #dfd8cf;
    padding: 2.2mm 2.8mm;
    text-align: left;
    vertical-align: top;
  }}

  th {{
    background-color: #f5f1eb;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 600;
    color: #332d26;
  }}

  tr:nth-child(even) td {{
    background-color: #fbf9f6;
  }}

  /* BLOCKQUOTES */
  blockquote {{
    margin: 4mm 0 4mm 5mm;
    padding-left: 4mm;
    border-left: 3px solid #bfa15f;
    color: #4a453e;
    font-style: italic;
    break-inside: avoid;
  }}

  /* MATH STYLING */
  .math-display {{
    font-family: 'Lora', serif;
    font-style: italic;
    text-align: center;
    margin: 3.5mm 0;
    padding: 2mm;
    background: #fbf9f5;
    border-radius: 4px;
    color: #2b2723;
    break-inside: avoid;
  }}

  .math-inline {{
    font-family: 'Lora', serif;
    font-style: italic;
    color: #2b2723;
  }}

  /* HR / DIVIDERS */
  hr {{
    border: 0;
    height: 1px;
    background: #e2ddd5;
    margin: 8mm 0;
  }}

  /* LISTS */
  ul, ol {{
    margin: 2mm 0 4mm 0;
    padding-left: 6mm;
  }}

  li {{
    margin-bottom: 1.8mm;
    text-align: justify;
  }}
</style>
</head>
<body>

<!-- COVER PAGE -->
<div class="cover-page">
  <div class="cover-series">Серия «Внутренний ток» • Библиотека «Золотая Семёрка»</div>
  
  <div class="cover-hero">
    <svg class="cover-emblem" viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="1.8">
      <circle cx="50" cy="50" r="45" stroke-dasharray="3 3"/>
      <!-- Lightning and Circuit Icon -->
      <path d="M 50 18 L 38 52 L 48 52 L 44 82 L 62 46 L 52 46 Z" stroke="#bfa15f" stroke-width="1.5" fill="#faf6ed"/>
      <circle cx="50" cy="50" r="32" stroke="currentColor" stroke-width="1.2"/>
    </svg>
    <div class="cover-author">Владимир Аньянов</div>
    <h1 class="cover-title">ВЕЛИКИЙ СИНТЕЗ</h1>
    <div class="cover-divider"></div>
    <div class="cover-subtitle">Революции Материи, Трагедия Духа и Электродинамика Человека</div>
    <div class="cover-tagline">
      Как наука покорила вещество, почему десять тысяч лет поисков не спасли душу и как Универсальный закон потоковых систем соединил две половины бытия
    </div>
  </div>

  <div class="cover-footer">
    Master Edition 2.0 • Волгодонск 2026
  </div>
</div>

<!-- FRONTISPIECE EPIGRAPH -->
<div class="frontispiece">
  <div class="frontispiece-quote">
    «Человечество совершило величайший подвиг: оно исследовало край наблюдаемой Вселенной, расщепило атомное ядро и научило кремний мыслить. Но оставшись наедине с собой в ночной тишине, создатель космических станций испытывает тот же палеолитический страх, что и кроманьонец у костра. Стоило развернуть объективные законы термодинамики открытых систем, негэнтропии и электродинамики внутрь человека — и раскол исчез. Счастье оказалось не наградой на небесах, а режимом сверхпроводимости открытого контура. Великий Синтез свершился: дух и материя соединились в одном строгом уравнении жизни.»
  </div>
  <div class="frontispiece-author">Владимир Аньянов</div>
</div>

<!-- BOOK CONTENT -->
{html_body}

</body>
</html>
"""

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(FULL_HTML)

print(f"Generated HTML: {OUTPUT_HTML} (size: {os.path.getsize(OUTPUT_HTML)} bytes)")

# RENDER PDF VIA PLAYWRIGHT
print("Launching browser for PDF render...")
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"file:///{OUTPUT_HTML.replace(os.sep, '/')}", wait_until="networkidle")
    page.wait_for_function("() => window.katexDone === true")
    page.wait_for_timeout(1000)
    
    header_template = """
    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 8pt; color: #a19a91; width: 100%; display: flex; justify-content: space-between; padding: 0 18mm;">
      <span>Владимир Аньянов • Великий Синтез</span>
      <span>Master Edition 2.0</span>
    </div>
    """
    
    footer_template = """
    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 8.5pt; color: #827b72; width: 100%; display: flex; justify-content: center; padding: 0 18mm;">
      <span class="pageNumber"></span>
    </div>
    """
    
    page.pdf(
        path=OUTPUT_PDF,
        format="A4",
        print_background=True,
        display_header_footer=True,
        header_template=header_template,
        footer_template=footer_template,
        margin={"top": "20mm", "bottom": "20mm", "left": "18mm", "right": "18mm"}
    )
    browser.close()

reader = pypdf.PdfReader(OUTPUT_PDF)
print(f"SUCCESS: Generated primary PDF! Total Pages: {len(reader.pages)}, Size: {os.path.getsize(OUTPUT_PDF) / 1024:.1f} KB")

# Copy to Vault and IC Library
shutil.copyfile(OUTPUT_PDF, PDF_VAULT)
print("Copied PDF to Obsidian Vault:", PDF_VAULT)

shutil.copyfile(OUTPUT_PDF, PDF_LIB)
print("Copied PDF to IC Library Golden Seven:", PDF_LIB)

shutil.copyfile(OUTPUT_PDF, PDF_LIB_2)
print("Copied PDF to IC Library Golden Seven 2.0:", PDF_LIB_2)
