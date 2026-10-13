import os
import re
import shutil
import markdown
from playwright.sync_api import sync_playwright
import pypdf

VAULT_MD = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Брошюра — Электродинамика любви (Взаимная индукция двух суверенных генераторов, гальваническая развязка и преодоление аварии созависимости).md"
OUTPUT_HTML = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\love_brochure.html"
OUTPUT_PDF = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\IC Library\Брошюра — Электродинамика любви (Взаимная индукция двух суверенных генераторов, гальваническая развязка и преодоление аварии созависимости).pdf"
VAULT_PDF = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Брошюра — Электродинамика любви (Взаимная индукция двух суверенных генераторов, гальваническая развязка и преодоление аварии созависимости).pdf"

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
processed_md = re.sub(r"^(## ⏱️ Практический алгоритм[^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
processed_md = re.sub(r"^(## ⚡ Резюме[^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)

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
<title>Электродинамика любви — Владимир Аньянов</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js" onload="renderMathInElement(document.body, {{delimiters: [{{left: '$$', right: '$$', display: true}}, {{left: '$', right: '$', display: false}}]}});"></script>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Lora:ital,wght@0,400;0,500;0,600;1,400;1,500&family=JetBrains+Mono:wght@400;500&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

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
    color: #db2777;
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
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 2mm;
    font-weight: 700;
    color: #be185d;
  }}

  h3 {{
    font-size: 11.5pt;
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

  .frontispiece {{
    page-break-after: always;
    text-align: center;
    padding-top: 40mm;
  }}

  .frontispiece-badge {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 9pt;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #db2777;
    margin-bottom: 8mm;
  }}

  .frontispiece-title {{
    font-family: 'Cinzel', serif;
    font-size: 26pt;
    font-weight: 700;
    color: #0f172a;
    line-height: 1.2;
    margin-bottom: 6mm;
  }}

  .frontispiece-subtitle {{
    font-family: 'Lora', serif;
    font-style: italic;
    font-size: 13pt;
    color: #475569;
    max-width: 140mm;
    margin: 0 auto 20mm auto;
    line-height: 1.5;
  }}

  .frontispiece-author {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 11pt;
    font-weight: 600;
    letter-spacing: 0.05em;
    color: #1e293b;
    margin-top: 40mm;
  }}

  blockquote, .callout {{
    margin: 5mm 0;
    padding: 4mm 6mm;
    border-radius: 4px;
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
    font-size: 10pt;
    margin-bottom: 2mm;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }}

  pre {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.5pt;
    line-height: 1.35;
    background: #0f172a;
    color: #e2e8f0;
    padding: 4mm 5mm;
    border-radius: 6px;
    overflow-x: hidden;
    white-space: pre;
    margin: 5mm 0;
  }}

  code {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5pt;
    background: #f1f5f9;
    color: #0f172a;
    padding: 0.8mm 1.6mm;
    border-radius: 3px;
  }}

  pre code {{
    background: transparent;
    color: inherit;
    padding: 0;
  }}

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
    border: 1px solid #cbd5e1;
    text-align: left;
    vertical-align: top;
  }}

  th {{
    background: #f8fafc;
    color: #0f172a;
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
    background: #e2e8f0;
    margin: 6mm 0;
  }}
</style>
</head>
<body>

<!-- FRONTISPIECE COVER -->
<div class="frontispiece">
  <div class="frontispiece-badge">⚡ Inner Current • Мастер-Брошюра • Выпуск 2026</div>
  <div class="frontispiece-title">Электродинамика любви</div>
  <div class="frontispiece-subtitle">Взаимная индукция двух суверенных генераторов, гальваническая развязка и преодоление аварии созависимости</div>
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
      <span>Владимир Аньянов • Электродинамика любви</span>
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
