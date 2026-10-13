import os
import re
import markdown
from playwright.sync_api import sync_playwright
import pypdf
import shutil

VAULT_MD = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Брошюра — Новый Органон Сознания (Почему Внутренний Ток — не 1001-я школа психологии, а объективный закон природы).md"
OUTPUT_HTML = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\novum_organum_brochure.html"
OUTPUT_PDF = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\IC Library\Брошюра — Новый Органон Сознания (Почему Внутренний Ток — не 1001-я школа психологии, а объективный закон природы).pdf"
VAULT_PDF = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Брошюра — Новый Органон Сознания (Почему Внутренний Ток — не 1001-я школа психологии, а объективный закон природы).pdf"

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

# Preprocess Mermaid diagram blocks BEFORE markdown parser
def replace_mermaid(match):
    diagram = match.group(1).strip()
    return f'<div class="mermaid-wrap"><pre class="mermaid">\n{diagram}\n</pre></div>'

processed_md = re.sub(r"```mermaid([\s\S]*?)```", replace_mermaid, processed_md)

# Preprocess Chapters/Parts to inject chapter-break classes
processed_md = re.sub(r"^(## ЧАСТЬ [^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
processed_md = re.sub(r"^(## 🛠️ Дашборд[^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
processed_md = re.sub(r"^(## Резюме[^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)

# Convert Markdown to HTML
md_extensions = ['tables', 'fenced_code', 'def_list', 'nl2br']
html_body = markdown.markdown(processed_md, extensions=md_extensions)

# Wrap tables in responsive containers
html_body = html_body.replace("<table>", '<div class="table-wrapper"><table>')
html_body = html_body.replace("</table>", '</table></div>')

FULL_HTML = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Новый Органон Сознания — Владимир Аньянов</title>
<!-- KaTeX for beautiful math formulas rendering -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js" 
  onload="renderMathInElement(document.body, {{
    delimiters: [
      {{left: '$$', right: '$$', display: true}},
      {{left: '$', right: '$', display: false}}
    ],
    throwOnError: false
  }});">
</script>

<!-- Mermaid for diagrams rendering -->
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
  mermaid.initialize({{
    startOnLoad: true,
    theme: 'neutral',
    themeVariables: {{
      fontFamily: 'Plus Jakarta Sans, sans-serif',
      fontSize: '11px',
      primaryColor: '#f0fff4',
      primaryBorderColor: '#38a169',
      primaryTextColor: '#1e293b',
      lineColor: '#64748b'
    }}
  }});
</script>

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
    font-size: 10pt;
    line-height: 1.62;
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
    margin-top: 10mm;
  }}

  .cover-emblem {{
    width: 68px;
    height: 68px;
    margin-bottom: 7mm;
    color: #c2410c;
  }}

  .cover-author {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 12pt;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #575047;
    margin-bottom: 8mm;
    font-weight: 600;
  }}

  .cover-title {{
    font-family: 'Cinzel', serif;
    font-size: 23pt;
    font-weight: 700;
    line-height: 1.2;
    letter-spacing: 0.04em;
    color: #1c1917;
    margin-bottom: 6mm;
  }}

  .cover-subtitle {{
    font-family: 'Lora', serif;
    font-size: 10.5pt;
    font-style: italic;
    color: #6c6358;
    max-width: 150mm;
    line-height: 1.5;
  }}

  .cover-footer {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 8pt;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #a8a29e;
    width: 100%;
    display: flex;
    justify-content: space-between;
    border-top: 1px solid #e7e5e4;
    padding-top: 5mm;
  }}

  /* FRONTISPIECE */
  .frontispiece {{
    page-break-after: always;
    height: 100vh;
    min-height: 250mm;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 20mm;
  }}

  .frontispiece-quote {{
    font-family: 'Lora', serif;
    font-size: 12pt;
    font-style: italic;
    line-height: 1.7;
    color: #334155;
    max-width: 135mm;
    margin-bottom: 6mm;
  }}

  .frontispiece-author {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 9.5pt;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #64748b;
    font-weight: 600;
  }}

  /* TYPOGRAPHY */
  h1 {{
    font-family: 'Cinzel', serif;
    font-size: 18pt;
    font-weight: 700;
    line-height: 1.25;
    color: #0f172a;
    margin-top: 0;
    margin-bottom: 3mm;
    letter-spacing: 0.03em;
  }}

  h2 {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 12.5pt;
    font-weight: 700;
    color: #1e293b;
    margin-top: 7mm;
    margin-bottom: 3mm;
    letter-spacing: -0.01em;
    border-bottom: 1px solid #f1f5f9;
    padding-bottom: 1.5mm;
  }}

  h3 {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 10.5pt;
    font-weight: 600;
    color: #334155;
    margin-top: 5mm;
    margin-bottom: 2mm;
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

  /* BLOCKQUOTES AS FORMULAS */
  blockquote {{
    margin: 4mm 0;
    padding: 3mm 5mm;
    border-left: 3px solid #c2410c;
    background-color: #fff7ed;
    color: #9a3412;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 10pt;
    font-weight: 600;
    border-radius: 0 4px 4px 0;
  }}

  /* TABLES */
  .table-wrapper {{
    margin: 5mm 0;
    overflow-x: auto;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 8.5pt;
    font-family: 'Plus Jakarta Sans', sans-serif;
  }}

  th, td {{
    padding: 2.2mm 3mm;
    text-align: left;
    border-bottom: 1px solid #e2e8f0;
  }}

  th {{
    background-color: #f8fafc;
    font-weight: 600;
    color: #334155;
    border-top: 1px solid #cbd5e1;
    border-bottom: 2px solid #cbd5e1;
  }}

  /* CODE & ASCII DIAGRAMS */
  pre {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 6.8pt;
    line-height: 1.32;
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    padding: 3.5mm;
    overflow-x: auto;
    margin: 4mm 0;
    color: #1e293b;
  }}

  code {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.2pt;
    background-color: #f1f5f9;
    padding: 0.5mm 1.5mm;
    border-radius: 3px;
    color: #0f172a;
  }}

  pre code {{
    background: none;
    padding: 0;
    font-size: inherit;
  }}

  /* MERMAID WRAPPER */
  .mermaid-wrap {{
    margin: 5mm 0;
    padding: 4mm;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
    display: flex;
    justify-content: center;
    page-break-inside: avoid;
  }}

  .mermaid {{
    text-align: center;
    background: transparent !important;
  }}

  /* CALLOUTS */
  .callout {{
    margin: 4.5mm 0;
    padding: 3.5mm 4.5mm;
    border-radius: 5px;
    border-left: 4px solid #94a3b8;
    background-color: #f8fafc;
    page-break-inside: avoid;
  }}

  .callout-quote {{
    border-left-color: #c2410c;
    background-color: #fff7ed;
  }}

  .callout-quote .callout-title {{
    color: #9a3412;
  }}

  .callout-info {{
    border-left-color: #0284c7;
    background-color: #f0f9ff;
  }}

  .callout-info .callout-title {{
    color: #0369a1;
  }}

  .callout-important {{
    border-left-color: #0284c7;
    background-color: #f0f9ff;
  }}

  .callout-important .callout-title {{
    color: #0369a1;
  }}

  .callout-title {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 8.5pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.15em;
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
    margin: 5mm 0;
  }}

  ul, ol {{
    margin-top: 0;
    margin-bottom: 3.5mm;
    padding-left: 5mm;
  }}

  li {{
    margin-bottom: 1.2mm;
  }}

  /* KATEX ADJUSTMENTS */
  .katex {{
    font-size: 1.05em !important;
  }}
  .katex-display {{
    margin: 3.5mm 0 !important;
    overflow-x: auto;
    overflow-y: hidden;
  }}
</style>
</head>
<body>

<!-- COVER PAGE -->
<div class="cover-page">
  <div class="cover-series">Манифест Эпистемологической Демаркации • Библиотека Inner Current</div>
  <div class="cover-hero">
    <svg class="cover-emblem" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
      <circle cx="12" cy="12" r="10"></circle>
      <polygon points="13 2 9 14 15 14 11 22"></polygon>
    </svg>
    <div class="cover-author">Владимир Аньянов</div>
    <div class="cover-title">НОВЫЙ ОРГАНОН<br>СОЗНАНИЯ</div>
    <div class="cover-subtitle">Почему Внутренний Ток — не 1001-я школа психологии, а объективный закон природы: Масштабная инвариантность, консилиенция Уэвелла, критерий плодов Бэкона и физика прямого потока</div>
  </div>
  <div class="cover-footer">
    <span>Архитектура Счастья • Дзен-Инженерия</span>
    <span>Ростов-на-Дону • 2026</span>
  </div>
</div>

<!-- FRONTISPIECE -->
<div class="frontispiece">
  <div class="frontispiece-quote">«Психология сто тридцать лет вела себя как средневековая схоластика: выдумывала сотни птичьих терминов под каждый размер группы, бесконечно толковала "детские травмы" и продавала абонементы на сочувственное наблюдение горящей проводки. Но ложная модель не выдерживает смены масштаба. Внутренний ток — это не ещё одна терапевтическая школа и не разговорный жанр. Это Новый Органон науки о человеке: объективный закон электродинамики, который одинаково управляет соматикой одного тела, искрами пары, синергией команды и макроэкономикой цивилизаций. Таблице умножения и закону Ома не верят и в них не вступают — по ним просто безошибочно рассчитывают и замыкают ток жизни.»</div>
  <div class="frontispiece-author">Владимир Аньянов</div>
</div>

<!-- CONTENT -->
{html_body}

</body>
</html>
"""

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(FULL_HTML)

print("Generated HTML with KaTeX and Mermaid scripts!")

# RENDER PDF VIA PLAYWRIGHT
print("Launching browser for PDF render...")
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"file:///{OUTPUT_HTML.replace(os.sep, '/')}", wait_until="networkidle")
    
    # Wait for KaTeX and Mermaid to fully render in the DOM
    page.wait_for_timeout(3000)
    
    header_template = """
    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 7.5pt; color: #94a3b8; width: 100%; display: flex; justify-content: space-between; padding: 0 18mm;">
      <span>Владимир Аньянов • Новый Органон Сознания</span>
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
print(f"SUCCESS: Generated clean PDF in IC Library! Total Pages: {len(reader.pages)}, Size: {os.path.getsize(OUTPUT_PDF) / 1024:.1f} KB")

# Copy to Vault
shutil.copy2(OUTPUT_PDF, VAULT_PDF)
print("Copied PDF to Obsidian Vault successfully!")
