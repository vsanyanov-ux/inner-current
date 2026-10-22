import os
import re
import markdown
from playwright.sync_api import sync_playwright
import pypdf

VAULT_MD = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Брошюра — Схемотехника просветления (Сверхпроводимость как глагол, аппаратный замок Будды и физика Everyman).md"
OUTPUT_HTML = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\enlightenment_brochure.html"
OUTPUT_PDF = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\IC Library\Брошюра — Схемотехника просветления (Сверхпроводимость как глагол, аппаратный замок Будды и физика Everyman).pdf"

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
processed_md = re.sub(r"^(## ЧАСТЬ [^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
processed_md = re.sub(r"^(## РЕЗЮМЕ[^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)

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
<title>Схемотехника просветления — Владимир Аньянов</title>
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
    font-family: 'Lora', 'Georgia', serif;
    font-size: 10.5pt;
    line-height: 1.65;
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
    padding: 35mm 15mm 25mm 15mm;
    background: radial-gradient(circle at 50% 30%, #ffffff 0%, #faf8f5 100%);
    border: 1px solid #eae5df;
    position: relative;
  }}

  .cover-series {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 8.5pt;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: #8c8275;
    font-weight: 700;
  }}

  .cover-hero {{
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 15mm;
  }}

  .cover-emblem {{
    width: 72px;
    height: 72px;
    margin-bottom: 8mm;
    color: #0284c7;
  }}

  .cover-author {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 13pt;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #575047;
    margin-bottom: 12mm;
    font-weight: 600;
  }}

  .cover-title {{
    font-family: 'Cinzel', serif;
    font-size: 26pt;
    font-weight: 700;
    line-height: 1.22;
    color: #1a1816;
    margin: 0 0 7mm 0;
    letter-spacing: 0.04em;
  }}

  .cover-subtitle {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 11pt;
    line-height: 1.55;
    color: #6e6458;
    max-width: 145mm;
    margin: 0 auto;
    font-weight: 400;
  }}

  .cover-footer {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 8pt;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #a89f91;
    font-weight: 600;
    display: flex;
    flex-direction: column;
    gap: 2mm;
  }}

  /* FRONTISPIECE */
  .frontispiece {{
    page-break-after: always;
    min-height: 240mm;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 30mm 20mm;
    text-align: center;
  }}

  .frontispiece-quote {{
    font-family: 'Lora', serif;
    font-style: italic;
    font-size: 12.5pt;
    line-height: 1.75;
    color: #3b352e;
    max-width: 135mm;
    margin-bottom: 8mm;
  }}

  .frontispiece-author {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 9.5pt;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #8c8275;
    font-weight: 700;
  }}

  /* TYPOGRAPHY */
  h1 {{
    font-family: 'Cinzel', serif;
    font-size: 18pt;
    font-weight: 700;
    color: #1a1816;
    margin-top: 10mm;
    margin-bottom: 5mm;
    line-height: 1.3;
    border-bottom: 2px solid #0284c7;
    padding-bottom: 3mm;
  }}

  h2 {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 13pt;
    font-weight: 700;
    color: #1e293b;
    margin-top: 8mm;
    margin-bottom: 3.5mm;
    line-height: 1.35;
    letter-spacing: 0.02em;
  }}

  h3 {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 11pt;
    font-weight: 600;
    color: #334155;
    margin-top: 6mm;
    margin-bottom: 2.5mm;
  }}

  p {{
    margin-top: 0;
    margin-bottom: 3.5mm;
    text-align: justify;
  }}

  strong {{
    font-weight: 600;
    color: #0f172a;
  }}

  /* ASCII & CODE BLOCKS */
  pre {{
    background-color: #f8fafc;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    padding: 3.5mm 4mm;
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.8pt;
    line-height: 1.38;
    color: #0f172a;
    overflow-x: auto;
    page-break-inside: avoid;
    margin: 4mm 0 5mm 0;
  }}

  code {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5pt;
    background-color: #f1f5f9;
    padding: 0.5mm 1.5mm;
    border-radius: 3px;
    color: #0369a1;
  }}

  /* TABLES */
  .table-wrapper {{
    margin: 4mm 0 6mm 0;
    page-break-inside: avoid;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 8.8pt;
    font-family: 'Plus Jakarta Sans', sans-serif;
    line-height: 1.45;
  }}

  th {{
    background-color: #f1f5f9;
    color: #1e293b;
    font-weight: 700;
    text-align: left;
    padding: 2.5mm 3mm;
    border: 1px solid #cbd5e1;
  }}

  td {{
    padding: 2.5mm 3mm;
    border: 1px solid #e2e8f0;
    vertical-align: top;
  }}

  tr:nth-child(even) td {{
    background-color: #f8fafc;
  }}

  /* CALLOUTS */
  .callout {{
    margin: 5mm 0;
    padding: 4mm 5mm;
    border-left: 4px solid #0284c7;
    background-color: #f0f9ff;
    border-radius: 0 4px 4px 0;
    page-break-inside: avoid;
  }}

  .callout-quote {{
    border-left-color: #0284c7;
    background: #f8fafc;
    font-style: italic;
  }}

  .callout-title {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 8.5pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: #0369a1;
    margin-bottom: 2mm;
  }}

  .callout-body p:last-child {{
    margin-bottom: 0;
  }}

  /* CHAPTER BREAK */
  .chapter-break {{
    page-break-before: always;
  }}

  hr {{
    border: 0;
    height: 1px;
    background: #e2e8f0;
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
  <div class="cover-series">Манифест Контурной Электродинамики • Библиотека Inner Current</div>
  <div class="cover-hero">
    <svg class="cover-emblem" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="12" cy="12" r="10"></circle>
      <polygon points="13 2 9 14 15 14 11 22"></polygon>
    </svg>
    <div class="cover-author">Владимир Аньянов</div>
    <div class="cover-title">СХЕМОТЕХНИКА<br>ПРОСВЕТЛЕНИЯ</div>
    <div class="cover-subtitle">Сверхпроводимость как глагол, аппаратный замок Будды и физика Everyman: почему напор струи на автомойке равен дереву Бодхи</div>
  </div>
  <div class="cover-footer">
    <span>Архитектура Счастья • Дзен-Инженерия</span>
    <span>Ростов-на-Дону • 2026</span>
  </div>
</div>

<!-- FRONTISPIECE -->
<div class="frontispiece">
  <div class="frontispiece-quote">
    «Человечество три тысячи лет блуждало в потёмках восточной схоластики, потому что попало в грамматический капкан: люди искали просветление как существительное — отдельный статус, трофей или тайный параллельный контур. Но принципиальная схема Вселенной едина. Просветление — это глагол: быть сверхпроводящим в каждую секунду времени ($R \to 0, I > 0$). Стоя на автомойке со шлангом высокого давления и не думая ни о прошлом, ни о будущем, человек находится в абсолютном равенстве с Буддой под деревом Бодхи. Разница — лишь в топологии переключателя: у Everyman эго шунтируется динамически, а у Будды посадочный слот под эго аппаратно демонтирован навсегда.»
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
    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 7.5pt; color: #94a3b8; width: 100%; display: flex; justify-content: space-between; padding: 0 18mm;">
      <span>Владимир Аньянов • Схемотехника просветления</span>
      <span>Библиотека Inner Current</span>
    </div>
    """
    
    footer_template = """
    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 8pt; color: #64748b; width: 100%; display: flex; justify-content: center; padding: 0 18mm;">
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
