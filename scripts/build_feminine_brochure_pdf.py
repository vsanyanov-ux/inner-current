import os
import re
import shutil
import markdown
from playwright.sync_api import sync_playwright
import pypdf

VAULT_MD = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Брошюра — Женственность и внутренний ток (Касание жизни, руки в масле и преодоление пассивности).md"
OUTPUT_HTML = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\feminine_brochure.html"
OUTPUT_PDF = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\IC Library\Брошюра — Женственность и внутренний ток (Касание жизни, руки в масле и преодоление пассивности).pdf"
VAULT_PDF = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Брошюра — Женственность и внутренний ток (Касание жизни, руки в масле и преодоление пассивности).pdf"

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

# Preprocess Chapters to inject page-break classes
processed_md = re.sub(r"^(## Часть I\.[^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
processed_md = re.sub(r"^(## Часть III\.[^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
processed_md = re.sub(r"^(## Часть V\.[^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
processed_md = re.sub(r"^(## Часть VI\.[^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
processed_md = re.sub(r"^(## Часть VII\.[^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
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
<title>Женственность и внутренний ток — Владимир Аньянов</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js" onload="renderMathInElement(document.body, {{delimiters: [{{left: '$$', right: '$$', display: true}}, {{left: '$', right: '$', display: false}}]}});"></script>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700;800&family=Lora:ital,wght@0,400;0,500;0,600;1,400;1,500;1,600&family=JetBrains+Mono:wght@400;500&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

  @page {{
    size: A4;
    margin: 22mm 18mm 22mm 18mm;
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

  h1, h2, h3, h4 {{
    font-family: 'Cinzel', serif;
    color: #0f172a;
    letter-spacing: -0.01em;
  }}

  h1 {{
    font-size: 20pt;
    text-align: center;
    margin-top: 15mm;
    margin-bottom: 6mm;
    font-weight: 700;
    line-height: 1.25;
    color: #be185d;
  }}

  .subtitle {{
    text-align: center;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 11pt;
    font-weight: 500;
    color: #475569;
    margin-bottom: 12mm;
    line-height: 1.4;
  }}

  h2 {{
    font-size: 13.5pt;
    margin-top: 10mm;
    margin-bottom: 4mm;
    border-bottom: 1px solid #fce7f3;
    padding-bottom: 2mm;
    font-weight: 700;
    color: #9d174d;
  }}

  h3 {{
    font-size: 11pt;
    margin-top: 6mm;
    margin-bottom: 2.5mm;
    font-weight: 600;
    color: #0f172a;
  }}

  p {{
    margin-top: 0;
    margin-bottom: 3.5mm;
    text-align: justify;
    text-justify: inter-word;
  }}

  .chapter-break {{
    page-break-before: always;
  }}

  /* FRONTISPIECE COVER */
  .frontispiece {{
    page-break-after: always;
    text-align: center;
    padding-top: 42mm;
  }}

  .frontispiece-badge {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 9pt;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #db2777;
    margin-bottom: 10mm;
  }}

  .frontispiece-title {{
    font-family: 'Cinzel', serif;
    font-size: 26pt;
    font-weight: 700;
    color: #0f172a;
    line-height: 1.22;
    margin-bottom: 6mm;
  }}

  .frontispiece-subtitle {{
    font-family: 'Lora', serif;
    font-style: italic;
    font-size: 13pt;
    color: #475569;
    max-width: 145mm;
    margin: 0 auto 20mm auto;
    line-height: 1.5;
  }}

  .frontispiece-divider {{
    width: 60mm;
    height: 1px;
    background: linear-gradient(to right, transparent, #db2777, transparent);
    margin: 0 auto 24mm auto;
  }}

  .frontispiece-author {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 11pt;
    font-weight: 600;
    letter-spacing: 0.08em;
    color: #1e293b;
    margin-top: 45mm;
  }}

  /* DEDICATION PAGE */
  .dedication-page {{
    page-break-after: always;
    text-align: center;
    padding: 45mm 15mm 0 15mm;
  }}

  .dedication-card {{
    border: 1px solid #fbcfe8;
    background: #fffdfa;
    border-radius: 8px;
    padding: 18mm 16mm;
    box-shadow: 0 4px 20px rgba(219, 39, 119, 0.05);
    max-width: 130mm;
    margin: 0 auto;
    position: relative;
  }}

  .dedication-card::before {{
    content: "✦";
    position: absolute;
    top: -9px;
    left: 50%;
    transform: translateX(-50%);
    background: #fffdfa;
    padding: 0 8px;
    color: #db2777;
    font-size: 11pt;
  }}

  .dedication-badge {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 8.5pt;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #be185d;
    margin-bottom: 6mm;
  }}

  .dedication-text {{
    font-family: 'Lora', serif;
    font-style: italic;
    font-size: 11.5pt;
    line-height: 1.85;
    color: #334155;
    margin-bottom: 7mm;
  }}

  .dedication-highlight {{
    color: #9d174d;
    font-weight: 600;
    font-style: normal;
    font-family: 'Cinzel', serif;
    font-size: 13pt;
    display: block;
    margin-bottom: 4mm;
  }}

  .dedication-signature {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 9.5pt;
    font-weight: 600;
    color: #64748b;
    letter-spacing: 0.05em;
  }}

  /* CALLOUTS */
  blockquote, .callout {{
    margin: 5mm 0;
    padding: 4mm 6mm;
    border-radius: 5px;
    font-size: 10pt;
    line-height: 1.55;
  }}

  .callout-quote {{
    border-left: 3.5px solid #db2777;
    background: #fdf2f8;
    color: #831843;
    font-style: italic;
  }}

  .callout-tip {{
    border-left: 3.5px solid #10b981;
    background: #ecfdf5;
    color: #064e3b;
  }}

  .callout-important, .callout-warning {{
    border-left: 3.5px solid #f59e0b;
    background: #fffbeb;
    color: #78350f;
  }}

  .callout-title {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 700;
    font-size: 9.5pt;
    margin-bottom: 2mm;
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }}

  /* CODE & SCHEMATICS */
  pre {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.2pt;
    line-height: 1.35;
    background: #0f172a;
    color: #f1f5f9;
    padding: 4.5mm 5.5mm;
    border-radius: 6px;
    overflow-x: hidden;
    white-space: pre;
    margin: 5mm 0;
    border: 1px solid #1e293b;
  }}

  code {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5pt;
    background: #fdf2f8;
    color: #9d174d;
    padding: 0.8mm 1.6mm;
    border-radius: 3px;
  }}

  pre code {{
    background: transparent;
    color: inherit;
    padding: 0;
  }}

  /* TABLES */
  table {{
    width: 100%;
    border-collapse: collapse;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 8pt;
    line-height: 1.4;
    margin: 4mm 0;
  }}

  th, td {{
    padding: 2.2mm 3mm;
    border: 1px solid #e2e8f0;
    text-align: left;
    vertical-align: top;
  }}

  th {{
    background: #fdf2f8;
    color: #831843;
    font-weight: 600;
  }}

  ul, ol {{
    margin-top: 0;
    margin-bottom: 3.5mm;
    padding-left: 6mm;
  }}

  li {{
    margin-bottom: 1.5mm;
  }}

  hr {{
    border: 0;
    height: 1px;
    background: #fce7f3;
    margin: 6mm 0;
  }}
</style>
</head>
<body>

<!-- FRONTISPIECE COVER -->
<div class="frontispiece">
  <div class="frontispiece-badge">⚡ Inner Current • Мастер-Брошюра • Выпуск 2026</div>
  <div class="frontispiece-title">Женственность и внутренний ток</div>
  <div class="frontispiece-subtitle">Касание жизни, руки в масле и преодоление холостого хода пассивности: Манифест соматической реабилитации живой женщины</div>
  <div class="frontispiece-divider"></div>
  <div class="frontispiece-author">Владимир Аньянов</div>
</div>

<!-- DEDICATION PAGE -->
<div class="dedication-page">
  <div class="dedication-card">
    <div class="dedication-badge">Посвящение</div>
    <span class="dedication-highlight">Анне</span>
    <div class="dedication-text">
      Женщине, чьё сердце отказалось быть фарфоровой декорацией на чужой полке.<br><br>
      Той, кто помнит свист ветра в визоре шлема, терпкий запах нагретого мотора и первозданную силу шершавой коры векового дуба.<br><br>
      Той, кто имеет смелость касаться этой реальности всеми десятью пальцами — преодолевая гравитацию и чужие страхи, но не предавая своей кошачьей нежности, королевской грации и способности беззаветно любить.<br><br>
      Пусть твой соматический ток никогда не встречает сомнений.<br>
      <strong>Свети на полную мощность.</strong>
    </div>
    <div class="dedication-signature">— Владимир Аньянов</div>
  </div>
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
      <span>Владимир Аньянов • Женственность и внутренний ток</span>
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

# Copy to vault
shutil.copy2(OUTPUT_PDF, VAULT_PDF)

reader = pypdf.PdfReader(OUTPUT_PDF)
print(f"SUCCESS: Generated PDF! Total Pages: {len(reader.pages)}, Size: {os.path.getsize(OUTPUT_PDF) / 1024:.1f} KB")
