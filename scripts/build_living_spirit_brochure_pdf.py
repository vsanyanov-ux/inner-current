import os
import re
import markdown
from playwright.sync_api import sync_playwright
import pypdf
import shutil

VAULT_MD = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Брошюра — Инженерия живого духа (Секстет инвариантного опыта, схемотехника уюта и преодоление великого раскола физиков и лириков).md"
OUTPUT_HTML = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\living_spirit_brochure.html"
PDF_NAME = "Брошюра — Инженерия живого духа (Секстет инвариантного опыта, схемотехника уюта и преодоление великого раскола физиков и лириков).pdf"
OUTPUT_PDF = os.path.join(r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\IC Library", PDF_NAME)
VAULT_PDF = os.path.join(r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki", PDF_NAME)

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

# Preprocess Chapters/Parts to inject chapter-break classes
processed_md = re.sub(r"^(### Часть [^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)

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
<title>Инженерия живого духа — Владимир Аньянов</title>
<!-- KaTeX for math formulas -->
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
    line-height: 1.68;
    color: #1e293b;
    background: #ffffff;
    margin: 0;
    padding: 0;
  }}

  /* COVER PAGE */
  .cover-page {{
    page-break-after: always;
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 30mm 15mm 20mm 15mm;
    text-align: center;
    border: 1px solid rgba(226, 232, 240, 0.8);
    background: radial-gradient(circle at 50% 30%, #fbfcfe 0%, #f1f5f9 100%);
    position: relative;
    border-radius: 8px;
  }}

  .cover-badge {{
    display: inline-block;
    align-self: center;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 8.5pt;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #0d9488;
    background: rgba(13, 148, 136, 0.08);
    padding: 6px 16px;
    border-radius: 20px;
    border: 1px solid rgba(13, 148, 136, 0.2);
  }}

  .cover-center {{
    margin-top: auto;
    margin-bottom: auto;
  }}

  .cover-title {{
    font-family: 'Cinzel', serif;
    font-size: 27pt;
    font-weight: 700;
    line-height: 1.25;
    color: #0f172a;
    letter-spacing: 0.03em;
    margin-bottom: 16px;
  }}

  .cover-subtitle {{
    font-family: 'Lora', serif;
    font-size: 12.5pt;
    font-style: italic;
    color: #475569;
    max-width: 580px;
    margin: 0 auto 30px auto;
    line-height: 1.5;
  }}

  .cover-author {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 13pt;
    font-weight: 600;
    color: #334155;
    letter-spacing: 0.08em;
  }}

  .cover-author-title {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 8.5pt;
    color: #64748b;
    margin-top: 4px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
  }}

  .cover-footer {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 8pt;
    color: #94a3b8;
    letter-spacing: 0.05em;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid #e2e8f0;
    padding-top: 15px;
  }}

  /* FRONTISPIECE */
  .frontispiece {{
    page-break-after: always;
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 40mm 25mm;
  }}

  .frontispiece-quote {{
    font-family: 'Lora', serif;
    font-size: 12.5pt;
    font-style: italic;
    line-height: 1.8;
    color: #334155;
    max-width: 560px;
    position: relative;
  }}

  .frontispiece-quote::before {{
    content: "«";
    font-size: 40pt;
    color: #cbd5e1;
    position: absolute;
    left: -35px;
    top: -20px;
    font-family: 'Cinzel', serif;
  }}

  .frontispiece-author {{
    margin-top: 25px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 9.5pt;
    font-weight: 600;
    color: #0d9488;
    letter-spacing: 0.1em;
    text-transform: uppercase;
  }}

  /* HEADINGS */
  h1 {{
    font-family: 'Cinzel', serif;
    font-size: 20pt;
    font-weight: 700;
    color: #0f172a;
    border-bottom: 2px solid #0d9488;
    padding-bottom: 8px;
    margin-top: 0;
    margin-bottom: 20px;
    page-break-after: avoid;
  }}

  h2 {{
    font-family: 'Cinzel', serif;
    font-size: 14pt;
    font-weight: 600;
    color: #1e293b;
    margin-top: 28px;
    margin-bottom: 12px;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 4px;
    page-break-after: avoid;
  }}

  h3 {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 12pt;
    font-weight: 700;
    color: #0f766e;
    margin-top: 24px;
    margin-bottom: 10px;
    page-break-after: avoid;
  }}

  p {{
    margin: 0 0 12px 0;
    text-align: justify;
  }}

  ul, ol {{
    margin: 0 0 14px 0;
    padding-left: 24px;
  }}

  li {{
    margin-bottom: 6px;
  }}

  blockquote {{
    margin: 16px 0;
    padding: 12px 20px;
    background: #f8fafc;
    border-left: 4px solid #0d9488;
    font-style: italic;
    color: #334155;
    border-radius: 0 6px 6px 0;
  }}

  /* CALLOUTS */
  .callout {{
    margin: 18px 0;
    padding: 14px 18px;
    border-radius: 8px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-left: 4px solid #0d9488;
    page-break-inside: avoid;
  }}

  .callout-quote {{
    border-left-color: #0d9488;
    background: #f0fdfa;
  }}

  .callout-title {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 9.5pt;
    font-weight: 700;
    color: #0f766e;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 8px;
  }}

  /* CODE & ASCII DIAGRAMS */
  pre {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5pt;
    line-height: 1.45;
    background: #0f172a;
    color: #e2e8f0;
    padding: 14px 16px;
    border-radius: 6px;
    overflow-x: auto;
    page-break-inside: avoid;
    margin: 16px 0;
  }}

  code {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5pt;
  }}

  p code, li code {{
    background: #f1f5f9;
    color: #0f766e;
    padding: 2px 5px;
    border-radius: 4px;
    border: 1px solid #e2e8f0;
  }}

  /* TABLES */
  .table-wrapper {{
    margin: 16px 0;
    page-break-inside: avoid;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 9pt;
  }}

  th {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 600;
    background: #f1f5f9;
    color: #1e293b;
    border: 1px solid #cbd5e1;
    padding: 8px 10px;
    text-align: left;
  }}

  td {{
    border: 1px solid #e2e8f0;
    padding: 8px 10px;
    vertical-align: top;
  }}

  tr:nth-child(even) td {{
    background: #f8fafc;
  }}

  .chapter-break {{
    page-break-before: always;
  }}
</style>
</head>
<body>

<!-- COVER -->
<div class="cover-page">
  <div class="cover-badge">Библиотека Inner Current • Секстет Инвариантного Опыта</div>
  <div class="cover-center">
    <div class="cover-title">ИНЖЕНЕРИЯ ЖИВОГО ДУХА</div>
    <div class="cover-subtitle">Схемотехника уюта, эмерджентный свет и преодоление великого раскола физиков и лириков</div>
    <div class="cover-author">Владимир Аньянов</div>
    <div class="cover-author-title">Основатель теории Внутреннего тока</div>
  </div>
  <div class="cover-footer">
    <span>Inner Current Publishing • Электродинамика Состояния</span>
    <span>Ростов-на-Дону • 2026</span>
  </div>
</div>

<!-- FRONTISPIECE -->
<div class="frontispiece">
  <div class="frontispiece-quote">«Логика строит провода, но Ток зажигает Сердце. Четыреста лет мир жил в расколе между физиками, считавшими человека куском мяса, и лириками, дрожавшими над душой как над неприкосновенной сказкой. Внутренний ток соединил их в один нерушимый контур: законы электродинамики оказались законами самого Духа, защищающими нежность, вечер на диване и свет любви.»</div>
  <div class="frontispiece-author">Владимир Аньянов</div>
</div>

<!-- CONTENT -->
{html_body}

</body>
</html>
"""

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(FULL_HTML)

print("HTML generated successfully! Starting Playwright PDF render...")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"file:///{OUTPUT_HTML.replace(os.sep, '/')}", wait_until="networkidle")
    
    # Wait for KaTeX formulas rendering
    page.wait_for_timeout(3000)
    
    header_template = """
    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 7.5pt; color: #94a3b8; width: 100%; display: flex; justify-content: space-between; padding: 0 18mm;">
      <span>Владимир Аньянов • Инженерия живого духа</span>
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
print(f"SUCCESS: Generated PDF in IC Library! Pages: {len(reader.pages)}, Size: {os.path.getsize(OUTPUT_PDF) / 1024:.1f} KB")

# Copy to Vault
shutil.copy2(OUTPUT_PDF, VAULT_PDF)
print("Copied PDF to Obsidian Vault successfully!")
