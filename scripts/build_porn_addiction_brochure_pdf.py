import os
import re
import shutil
import markdown
from playwright.sync_api import sync_playwright
import pypdf

VAULT_MD = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Брошюра — Порно-зависимость и внутренний ток (Дофаминовое короткое замыкание, обрыв живого контура и банкротство силы воли).md"
OUTPUT_HTML = r"C:\Users\vanya\Antigravity Projects\Apps\Inner Current\porn_addiction_brochure.html"
OUTPUT_PDF = r"C:\Users\vanya\Antigravity Projects\Apps\Inner Current\IC Library\Брошюра — Порно-зависимость и внутренний ток (Дофаминовое короткое замыкание, обрыв живого контура и банкротство силы воли).pdf"
VAULT_PDF = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Брошюра — Порно-зависимость и внутренний ток (Дофаминовое короткое замыкание, обрыв живого контура и банкротство силы воли).pdf"

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
    title_html = f'<div class="callout-title">{title}</div>' if title else ""
    return f'<div class="callout callout-{ctype}">{title_html}<div class="callout-body">{body_html}</div></div>'

processed_md = re.sub(r"^>\s*\[!(\w+)\]([^\n]*(?:\n>[^\n]*)*)", replace_callout, raw_md, flags=re.MULTILINE)

# Preprocess Parts to inject page-break classes
processed_md = re.sub(r"^(## Часть [^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
processed_md = re.sub(r"^(## 🛠 Практический алгоритм[^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
processed_md = re.sub(r"^(## Резюме[^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)

# Convert Markdown to HTML
md_extensions = ['tables', 'fenced_code', 'codehilite', 'def_list', 'nl2br']
html_body = markdown.markdown(processed_md, extensions=md_extensions)

# Wrap tables in responsive containers
html_body = html_body.replace("<table>", '<div class="table-wrapper"><table>')
html_body = html_body.replace("</table>", '</table></div>')

FULL_HTML = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Порно-зависимость и внутренний ток — Владимир Аньянов</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js" onload="renderMathInElement(document.body, {{delimiters: [{{left: '$$', right: '$$', display: true}}, {{left: '$', right: '$', display: false}}]}});"></script>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Lora:ital,wght@0,400;0,500;0,600;1,400;1,500&family=JetBrains+Mono:wght@400;500&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

  @page {{
    size: A4;
    margin: 22mm 18mm 22mm 18mm;
  }}

  * {{
    box-sizing: border-box;
  }}

  body {{
    font-family: 'Lora', Georgia, serif;
    font-size: 10.5pt;
    line-height: 1.65;
    color: #1e293b;
    background: #ffffff;
    margin: 0;
    padding: 0;
  }}

  /* COVER STYLING */
  .cover-page {{
    page-break-after: always;
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 25mm 15mm 20mm 15mm;
    border: 1px solid #fecdd3;
    background: linear-gradient(145deg, #fff1f2 0%, #ffe4e6 40%, #fecdd3 100%);
    position: relative;
    box-sizing: border-box;
  }}

  .cover-series {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 8.5pt;
    font-weight: 700;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #be123c;
    border-bottom: 2px solid #e11d48;
    padding-bottom: 3mm;
    display: inline-block;
  }}

  .cover-hero {{
    margin: auto 0;
  }}

  .cover-emblem {{
    width: 24mm;
    height: 24mm;
    color: #e11d48;
    margin-bottom: 8mm;
  }}

  .cover-author {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 12pt;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #881337;
    margin-bottom: 5mm;
  }}

  .cover-title {{
    font-family: 'Cinzel', serif;
    font-size: 26pt;
    font-weight: 700;
    line-height: 1.15;
    color: #4c0519;
    letter-spacing: -0.01em;
    margin-bottom: 6mm;
  }}

  .cover-subtitle {{
    font-family: 'Lora', serif;
    font-size: 11.5pt;
    font-style: italic;
    line-height: 1.5;
    color: #9f1239;
    max-width: 92%;
    border-left: 3px solid #e11d48;
    padding-left: 5mm;
  }}

  .cover-footer {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 8.5pt;
    color: #be123c;
    border-top: 1px solid #fda4af;
    padding-top: 4mm;
    display: flex;
    justify-content: space-between;
  }}

  /* FRONTISPIECE */
  .frontispiece {{
    page-break-after: always;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
    padding: 30mm 20mm;
    text-align: center;
    box-sizing: border-box;
  }}

  .frontispiece-quote {{
    font-family: 'Lora', Georgia, serif;
    font-size: 13pt;
    font-style: italic;
    line-height: 1.8;
    color: #334155;
    max-width: 580px;
    margin-bottom: 12mm;
    position: relative;
  }}

  .frontispiece-quote::before {{
    content: "«";
    font-family: 'Cinzel', serif;
    font-size: 50pt;
    color: #fda4af;
    position: absolute;
    top: -30px;
    left: -35px;
    opacity: 0.6;
  }}

  .frontispiece-author {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 10pt;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #be123c;
  }}

  /* TYPOGRAPHY */
  h1 {{
    font-family: 'Cinzel', serif;
    font-size: 18pt;
    font-weight: 700;
    color: #4c0519;
    margin-top: 0;
    margin-bottom: 4mm;
    line-height: 1.25;
    border-bottom: 1.5px solid #fda4af;
    padding-bottom: 3mm;
  }}

  h2 {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 13pt;
    font-weight: 700;
    color: #881337;
    margin-top: 8mm;
    margin-bottom: 3mm;
    line-height: 1.35;
    letter-spacing: -0.01em;
  }}

  h3 {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 11pt;
    font-weight: 600;
    color: #9f1239;
    margin-top: 5mm;
    margin-bottom: 2mm;
  }}

  p {{
    margin-top: 0;
    margin-bottom: 3.5mm;
    text-align: justify;
    text-justify: inter-word;
  }}

  strong {{
    font-weight: 600;
    color: #0f172a;
  }}

  em {{
    font-style: italic;
  }}

  .chapter-break {{
    page-break-before: always;
  }}

  /* CODE & ASCII */
  pre {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.2pt;
    line-height: 1.35;
    background: #fff1f2;
    color: #881337;
    border: 1px solid #fecdd3;
    border-radius: 4px;
    padding: 3.5mm 4mm;
    margin: 4mm 0;
    white-space: pre;
    overflow-x: hidden;
    page-break-inside: avoid;
  }}

  code {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5pt;
    background: #ffe4e6;
    color: #9f1239;
    padding: 0.5mm 1.5mm;
    border-radius: 3px;
  }}

  pre code {{
    background: transparent;
    color: inherit;
    padding: 0;
  }}

  /* CALLOUTS */
  .callout {{
    margin: 4mm 0;
    padding: 3.5mm 4.5mm;
    border-left: 4px solid #be123c;
    background: #fff1f2;
    border-radius: 0 4px 4px 0;
    page-break-inside: avoid;
  }}

  .callout-title {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 9.5pt;
    font-weight: 700;
    color: #9f1239;
    margin-bottom: 1.5mm;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }}

  .callout-body p:last-child {{
    margin-bottom: 0;
  }}

  .callout-quote {{
    border-left-color: #be123c;
    background: #fff1f2;
  }}

  .callout-info {{
    border-left-color: #0284c7;
    background: #f0f9ff;
  }}

  /* TABLES */
  .table-wrapper {{
    margin: 4mm 0;
    page-break-inside: avoid;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 8.2pt;
    line-height: 1.45;
  }}

  th {{
    background: #881337;
    color: #ffffff;
    font-weight: 600;
    text-align: left;
    padding: 2.5mm 3mm;
    border: 1px solid #9f1239;
  }}

  td {{
    padding: 2.5mm 3mm;
    border: 1px solid #fecdd3;
    background: #ffffff;
    vertical-align: top;
  }}

  tr:nth-child(even) td {{
    background: #fff1f2;
  }}

  /* LISTS */
  ul, ol {{
    margin-top: 1mm;
    margin-bottom: 3.5mm;
    padding-left: 5mm;
  }}

  li {{
    margin-bottom: 1.5mm;
  }}

  hr {{
    border: 0;
    height: 1px;
    background: #fecdd3;
    margin: 6mm 0;
  }}
</style>
</head>
<body>

<!-- COVER PAGE -->
<div class="cover-page">
  <div class="cover-header">
    <div class="cover-series">Мастер-Брошюра • Inner Current Series</div>
  </div>
  <div class="cover-hero">
    <svg class="cover-emblem" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
      <path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
    </svg>
    <div class="cover-author">Владимир Аньянов</div>
    <div class="cover-title">ПОРНО-ЗАВИСИМОСТЬ И<br>ВНУТРЕННИЙ ТОК</div>
    <div class="cover-subtitle">Дофаминовое короткое замыкание, обрыв живого контура и банкротство силы воли — Манифест депосреднизации сексуальности: почему NoFap гарантирует срыв и как вернуть сверхпроводимость жизни</div>
  </div>
  <div class="cover-footer">
    <span>Архитектура Счастья • Электродинамика Освобождения</span>
    <span>Ростов-на-Дону • 2026</span>
  </div>
</div>

<!-- FRONTISPIECE -->
<div class="frontispiece">
  <div class="frontispiece-quote">
    «Порно-зависимость — это не половой грех, не моральная грязь и не генетический порок. Это аварийное короткое замыкание дофаминового ядра на плоский стеклянный экран. Измученный омическим пожаром эго человек пытается выбить себе 10 секунд тишины Мусин в абсолютно разомкнутом контуре, где нет обратного провода реальности ($I_{{\\text{{return}}}} = 0$) и не действует закон взаимной индукции Фарадея ($M = 0$). Попытки бороться с этим стиснутыми зубами (NoFap), копанием в детских травмах или химическими таблетками обречены на крах, потому что они квадратично умножают нагрев вины ($Q = I^2 R t$). Срежь реостат стыда ($R \\to 0$) — и высоковольтная ЭДС жизни направится либо во взаимную индукцию живой любви, либо в пламя созидания.»
  </div>
  <div class="frontispiece-author">Владимир Аньянов</div>
</div>

<!-- CONTENT -->
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
    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 7.5pt; color: #9f1239; width: 100%; display: flex; justify-content: space-between; padding: 0 18mm;">
      <span>Владимир Аньянов • Порно-зависимость и внутренний ток</span>
      <span>Библиотека Inner Current</span>
    </div>
    """
    
    footer_template = """
    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 8pt; color: #881337; width: 100%; display: flex; justify-content: center; padding: 0 18mm;">
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

# Copy to vault
shutil.copy2(OUTPUT_PDF, VAULT_PDF)

reader = pypdf.PdfReader(OUTPUT_PDF)
print(f"SUCCESS: Generated PDF! Total Pages: {len(reader.pages)}, Size: {os.path.getsize(OUTPUT_PDF) / 1024:.1f} KB")
