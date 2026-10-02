import os
import re
import markdown
from playwright.sync_api import sync_playwright
import pypdf

VAULT_MD = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Книга — Укулеле Бытия (Акустическая физика счастливой жизни).md"
OUTPUT_HTML = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\ukulele_book.html"
OUTPUT_PDF = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\Укулеле Бытия — Владимир Аньянов.pdf"

with open(VAULT_MD, "r", encoding="utf-8") as f:
    raw_md = f.read()

# Preprocess Callouts (> [!quote] etc.)
def replace_callout(match):
    ctype = match.group(1).lower()
    content = match.group(2)
    # clean leading '> '
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

# Beautify math inline and display
html_body = re.sub(r"\$\$(.*?)\$\$", r'<div class="math-display">\1</div>', html_body, flags=re.DOTALL)
html_body = re.sub(r"\$([^\$\n]+)\$", r'<span class="math-inline">\1</span>', html_body)

FULL_HTML = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Укулеле Бытия — Владимир Аньянов</title>
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
    font-size: 32pt;
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
    font-size: 14pt;
    font-style: italic;
    color: #615a51;
    max-width: 480px;
    margin: 0 auto 8mm auto;
    line-height: 1.45;
  }}

  .cover-tagline {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 9.5pt;
    color: #7d756a;
    max-width: 440px;
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
    max-width: 520px;
    font-size: 13pt;
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
    line-height: 1;
  }}

  .frontispiece-author {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 10pt;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: #8c8275;
    font-weight: 600;
    margin-top: 8mm;
  }}

  /* HEADINGS */
  h1, h2, h3, h4 {{
    color: #1a1816;
    font-family: 'Lora', serif;
    font-weight: 600;
  }}

  .part-header {{
    page-break-before: always;
    padding-top: 25mm;
    margin-bottom: 12mm;
    border-bottom: 2px solid #bfa15f;
    padding-bottom: 6mm;
  }}

  .part-header h1 {{
    font-family: 'Cinzel', serif;
    font-size: 20pt;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: #1a1816;
    margin: 0;
  }}

  .chapter-break {{
    page-break-before: always;
    height: 1px;
  }}

  h2 {{
    font-size: 15pt;
    margin-top: 10mm;
    margin-bottom: 4mm;
    color: #1e1b18;
    border-bottom: 1px solid #eee9e0;
    padding-bottom: 2mm;
  }}

  h3 {{
    font-size: 12.5pt;
    margin-top: 6mm;
    margin-bottom: 2.5mm;
    color: #332d26;
  }}

  h4 {{
    font-size: 11pt;
    margin-top: 4mm;
    margin-bottom: 2mm;
    color: #554d42;
  }}

  p {{
    margin: 0 0 3.5mm 0;
    text-align: justify;
    hyphens: auto;
  }}

  strong {{
    font-weight: 600;
    color: #111;
  }}

  em {{
    font-style: italic;
  }}

  /* CALLOUTS */
  .callout {{
    margin: 5mm 0;
    padding: 4mm 5mm;
    border-radius: 4px;
    background: #faf7f2;
    border: 1px solid #ebd9b5;
    border-left: 4px solid #bfa15f;
    break-inside: avoid;
    font-size: 10.5pt;
    line-height: 1.6;
  }}

  .callout p:last-child {{
    margin-bottom: 0;
  }}

  /* DIAGRAMS / PRE / CODE */
  pre {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5pt;
    line-height: 1.45;
    background-color: #f7f6f3;
    border: 1px solid #e2ddd5;
    border-radius: 4px;
    padding: 4mm 5mm;
    margin: 5mm 0;
    overflow-x: hidden;
    white-space: pre;
    break-inside: avoid;
    color: #2b2723;
  }}

  code {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 9pt;
    background-color: #f2efe9;
    padding: 1px 4px;
    border-radius: 3px;
    color: #5a2e16;
  }}

  pre code {{
    background: transparent;
    padding: 0;
    color: inherit;
  }}

  /* TABLES */
  .table-wrapper {{
    margin: 5mm 0;
    break-inside: avoid;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 9.5pt;
    line-height: 1.5;
    margin: 0;
  }}

  th, td {{
    padding: 2.5mm 3.5mm;
    border: 1px solid #ded8ce;
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

  /* TOC STYLING */
  h2#_1, h2:first-of-type {{
    /* Table of contents header */
    font-family: 'Cinzel', serif;
    letter-spacing: 0.05em;
  }}
</style>
</head>
<body>

<!-- COVER PAGE -->
<div class="cover-page">
  <div class="cover-series">Серия «Внутренний ток» • Канон Кансо</div>
  
  <div class="cover-hero">
    <svg class="cover-emblem" viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="1.8">
      <circle cx="50" cy="50" r="45" stroke-dasharray="3 3"/>
      <!-- Ukulele stylized silhouette -->
      <path d="M 50 15 L 50 42 M 45 42 Q 35 48 35 58 Q 35 68 45 74 Q 32 82 32 90 Q 32 98 50 98 Q 68 98 68 90 Q 68 82 55 74 Q 65 68 65 58 Q 65 48 55 42 Z" stroke="currentColor" stroke-width="1.8" fill="none"/>
      <circle cx="50" cy="62" r="6" fill="#bfa15f" stroke="none"/>
      <line x1="48" y1="20" x2="48" y2="88" stroke="#bfa15f" stroke-width="0.8"/>
      <line x1="49.5" y1="20" x2="49.5" y2="88" stroke="#bfa15f" stroke-width="1.2"/>
      <line x1="50.5" y1="20" x2="50.5" y2="88" stroke="#bfa15f" stroke-width="0.9"/>
      <line x1="52" y1="20" x2="52" y2="88" stroke="#bfa15f" stroke-width="0.7"/>
    </svg>
    <div class="cover-author">Владимир Аньянов</div>
    <h1 class="cover-title">УКУЛЕЛЕ БЫТИЯ</h1>
    <div class="cover-divider"></div>
    <div class="cover-subtitle">Простая акустика счастливой жизни</div>
    <div class="cover-tagline">
      Как 400 граммов дерева, четыре струны и пустота внутри корпуса объясняют гармонию человека, природу эго и искусство жить без фальши
    </div>
  </div>

  <div class="cover-footer">
    Волгодонск 2026
  </div>
</div>

<!-- FRONTISPIECE EPIGRAPH -->
<div class="frontispiece">
  <div class="frontispiece-quote">
    «Человек устроен не как сложная неприступная крепость и не как жертвенный механизм. Человек устроен как укулеле: четыреста граммов дерева, четыре струны и чистая пустота внутри корпуса. Когда струна живота настроена точно, а пальцы ума не сжимают гриф мёртвой хваткой контроля, радость рождается сама собой от малейшего прикосновения жизни. Счастье — это не консерваторский диплом. Счастье — это чистый строй твоего инструмента прямо здесь и сейчас.»
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
    
    header_template = """
    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 8pt; color: #a19a91; width: 100%; display: flex; justify-content: space-between; padding: 0 18mm;">
      <span>Владимир Аньянов • Укулеле Бытия</span>
      <span>Канон Кансо</span>
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
print(f"SUCCESS: Generated PDF! Total Pages: {len(reader.pages)}, Size: {os.path.getsize(OUTPUT_PDF) / 1024:.1f} KB")
