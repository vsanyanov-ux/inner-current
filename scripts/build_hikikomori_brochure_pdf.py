import os
import re
import shutil
import markdown
from playwright.sync_api import sync_playwright
import pypdf

VAULT_MD = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Брошюра — Хикикомори и физика фонарика (Электродинамика запертого сознания, парадокс японского стыда и размыкание контура изоляции).md"
OUTPUT_HTML = r"C:\Users\vanya\Antigravity Projects\Apps\Inner Current\hikikomori_brochure.html"
OUTPUT_PDF = r"C:\Users\vanya\Antigravity Projects\Apps\Inner Current\IC Library\Брошюра — Хикикомори и физика фонарика (Электродинамика запертого сознания, парадокс японского стыда и размыкание контура изоляции).pdf"
VAULT_PDF = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Брошюра — Хикикомори и физика фонарика (Электродинамика запертого сознания, парадокс японского стыда и размыкание контура изоляции).pdf"

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
<title>Хикикомори и физика фонарика — Владимир Аньянов</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js" onload="renderMathInElement(document.body, {{delimiters: [{{left: '$$', right: '$$', display: true}}, {{left: '$', right: '$', display: false}}]}});"></script>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Lora:ital,wght@0,400;0,500;0,600;1,400;1,500&family=JetBrains+Mono:wght@400;500&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Noto+Sans+JP:wght@400;500;700&display=swap');

  @page {{
    size: A4;
    margin: 22mm 18mm 22mm 18mm;
  }}

  * {{
    box-sizing: border-box;
  }}

  body {{
    font-family: 'Lora', 'Noto Sans JP', Georgia, serif;
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
    border: 1px solid #bfdbfe;
    background: linear-gradient(145deg, #f0fdf4 0%, #eff6ff 40%, #e0f2fe 100%);
    position: relative;
    box-sizing: border-box;
  }}

  .cover-series {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 8.5pt;
    font-weight: 700;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #0369a1;
    border-bottom: 2px solid #0284c7;
    padding-bottom: 3mm;
    display: inline-block;
  }}

  .cover-hero {{
    margin: auto 0;
  }}

  .cover-emblem {{
    width: 24mm;
    height: 24mm;
    color: #0284c7;
    margin-bottom: 8mm;
  }}

  .cover-author {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 12pt;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #0c4a6e;
    margin-bottom: 5mm;
  }}

  .cover-title {{
    font-family: 'Cinzel', serif;
    font-size: 24pt;
    font-weight: 700;
    line-height: 1.18;
    color: #082f49;
    letter-spacing: -0.01em;
    margin-bottom: 6mm;
  }}

  .cover-subtitle {{
    font-family: 'Lora', serif;
    font-size: 11pt;
    font-style: italic;
    line-height: 1.5;
    color: #0369a1;
    max-width: 95%;
    border-left: 3px solid #0284c7;
    padding-left: 5mm;
  }}

  .cover-footer {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 8.5pt;
    color: #075985;
    border-top: 1px solid #bae6fd;
    padding-top: 4mm;
    display: flex;
    justify-content: space-between;
  }}

  /* FRONTISPIECE */
  .frontispiece {{
    page-break-after: always;
    min-height: 80vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 20mm 15mm;
  }}

  .frontispiece-quote {{
    font-size: 12pt;
    font-style: italic;
    line-height: 1.7;
    color: #1e293b;
    max-width: 88%;
    margin-bottom: 8mm;
    position: relative;
  }}

  .frontispiece-quote::before {{
    content: "“";
    font-family: 'Cinzel', serif;
    font-size: 40pt;
    color: #7dd3fc;
    position: absolute;
    top: -20px;
    left: -25px;
    opacity: 0.6;
  }}

  .frontispiece-author {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 700;
    font-size: 10pt;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #0284c7;
  }}

  /* TYPOGRAPHY */
  h1, h2, h3, h4 {{
    font-family: 'Cinzel', serif;
    color: #0f172a;
    letter-spacing: -0.01em;
  }}

  h1 {{
    font-size: 18pt;
    text-align: center;
    margin-top: 10mm;
    margin-bottom: 5mm;
    font-weight: 700;
    line-height: 1.25;
    color: #0369a1;
  }}

  h2 {{
    font-size: 13pt;
    margin-top: 9mm;
    margin-bottom: 4mm;
    padding-bottom: 2mm;
    border-bottom: 1px solid #bae6fd;
    color: #0369a1;
    page-break-after: avoid;
  }}

  h3 {{
    font-size: 11pt;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 700;
    color: #1e293b;
    margin-top: 6mm;
    margin-bottom: 3mm;
    page-break-after: avoid;
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

  /* CALLOUTS */
  .callout {{
    margin: 5mm 0;
    padding: 4mm 5mm;
    border-radius: 2mm;
    background: #f0f9ff;
    border-left: 4px solid #0284c7;
    page-break-inside: avoid;
  }}

  .callout-title {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 700;
    font-size: 9.5pt;
    color: #0369a1;
    margin-bottom: 2mm;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }}

  .callout-body p:last-child {{
    margin-bottom: 0;
  }}

  /* TABLES */
  .table-wrapper {{
    margin: 5mm 0;
    page-break-inside: avoid;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 9pt;
    line-height: 1.45;
  }}

  th {{
    background: #f0f9ff;
    color: #0369a1;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 700;
    text-align: left;
    padding: 3mm;
    border-bottom: 2px solid #bae6fd;
  }}

  td {{
    padding: 3mm;
    border-bottom: 1px solid #e2e8f0;
    vertical-align: top;
  }}

  tr:nth-child(even) td {{
    background: #f8fafc;
  }}

  /* PRE & CODE */
  pre {{
    font-family: 'JetBrains Mono', 'Noto Sans JP', monospace;
    font-size: 8pt;
    line-height: 1.4;
    background: #0f172a;
    color: #f8fafc;
    padding: 4mm;
    border-radius: 2mm;
    overflow-x: auto;
    page-break-inside: avoid;
    margin: 5mm 0;
    border: 1px solid #1e293b;
  }}

  code {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5pt;
    background: #f1f5f9;
    color: #0369a1;
    padding: 1px 4px;
    border-radius: 1mm;
  }}

  pre code {{
    background: transparent;
    color: inherit;
    padding: 0;
  }}

  /* PAGE BREAKS */
  .chapter-break {{
    page-break-before: always;
  }}

  hr {{
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 6mm 0;
  }}

  ul, ol {{
    margin-top: 0;
    margin-bottom: 4mm;
    padding-left: 6mm;
  }}

  li {{
    margin-bottom: 1.5mm;
  }}
</style>
</head>
<body>

<!-- COVER PAGE -->
<div class="cover-page">
  <div class="cover-series">Манифест Депосреднизации Сознания • Серия Брошюр Inner Current</div>
  <div class="cover-hero">
    <svg class="cover-emblem" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
      <path d="M12 2v8"></path>
      <path d="m4.93 10.93 1.41 1.41"></path>
      <path d="M2 18h2"></path>
      <path d="M20 18h2"></path>
      <path d="m19.07 10.93-1.41 1.41"></path>
      <path d="M22 22H2"></path>
      <path d="m8 22 4-10 4 10"></path>
    </svg>
    <div class="cover-author">Владимир Аньянов</div>
    <div class="cover-title">ХИКИКОМОРИ И<br>ФИЗИКА ФОНАРИКА</div>
    <div class="cover-subtitle">Электродинамика запертого сознания, парадокс японского стыда и размыкание контура изоляции — Почему миллион людей заперлись в комнатах, в чём физика аварийного разворота луча внутрь ($Q = I^2 R t$) и как вернуть свет в реальность через 60-секундный протокол</div>
  </div>
  <div class="cover-footer">
    <span>Архитектура Счастья • Электродинамика Присутствия</span>
    <span>Ростов-на-Дону • 2026</span>
  </div>
</div>

<!-- FRONTISPIECE -->
<div class="frontispiece">
  <div class="frontispiece-quote">
    «Фонарик не сломан, если в комнате темно. Фонарик цел, его батарейка заряжена жизнью, но его оптическая головка вывернута внутрь собственного корпуса. Человек не может спастись, разглядывая расплавленные внутренности. Чтобы прекратить ад омического огня, достаточно направить один квант луча наружу — на холодную, простую вещь.»
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
    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 7.5pt; color: #0369a1; width: 100%; display: flex; justify-content: space-between; padding: 0 18mm;">
      <span>Владимир Аньянов • Хикикомори и физика фонарика</span>
      <span>Библиотека Inner Current</span>
    </div>
    """
    
    footer_template = """
    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 8pt; color: #0c4a6e; width: 100%; display: flex; justify-content: center; padding: 0 18mm;">
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
