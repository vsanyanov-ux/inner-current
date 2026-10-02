import os
import sys
import re
import markdown
from playwright.sync_api import sync_playwright

if sys.stdout:
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr:
    sys.stderr.reconfigure(encoding='utf-8')

SOURCE_MD = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Inner Current (Italian Triptych of Superconductivity — Olfactory-Acoustic Neocortex Bypass, The Versace Triad, Levante and Tanden Grounding).md"
OUTPUT_HTML = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\article_183_triptych.html"
OUTPUT_PDF = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\IC Library\183. Итальянский триптих сверхпроводимости — Ольфакторно-акустический байпас неокортекса (Триада Versace и Леванте).pdf"
ROOT_PDF = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\183. Итальянский триптих сверхпроводимости — Ольфакторно-акустический байпас неокортекса (Триада Versace и Леванте).pdf"
PUBLIC_PDF = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\public\books\183. Итальянский триптих сверхпроводимости.pdf"

with open(SOURCE_MD, "r", encoding="utf-8") as f:
    raw_md = f.read()

# Strip YAML frontmatter
raw_md = re.sub(r'^---[\s\S]*?---\s*', '', raw_md)

# Remove navigation links at top
raw_md = re.sub(r'\[К оглавлению\].*?\n', '', raw_md)

# Process Obsidian callouts
def process_callouts(text):
    pattern = r'> \[!(\w+)\]\s*([^\n]*)\n((?:>.*\n?)*)'
    def replace_callout(m):
        c_type = m.group(1).lower()
        title = m.group(2).strip()
        body = m.group(3)
        body = re.sub(r'^>\s?', '', body, flags=re.MULTILINE)
        title_html = f'<div class="callout-title">{title}</div>' if title else ''
        return f'<div class="callout callout-{c_type}">{title_html}\n{body}\n</div>\n'
    return re.sub(pattern, replace_callout, text)

processed_md = process_callouts(raw_md)

# Convert math expressions to styled spans
processed_md = re.sub(r'\$\$([\s\S]*?)\$\$', r'<div class="math-display">\1</div>', processed_md)
processed_md = re.sub(r'\$([^\$\n]+?)\$', r'<span class="math-inline">\1</span>', processed_md)

# Convert Markdown to HTML
html_body = markdown.markdown(processed_md, extensions=['extra', 'tables', 'fenced_code', 'nl2br'])

# Clean up initial H1 since cover handles it
html_body = re.sub(r'<h1>183\..*?</h1>', '', html_body, count=1)

# Clean up Mermaid blocks into styled visual containers
def replace_mermaid(match):
    content = match.group(1).strip()
    return f'<div class="mermaid-box"><pre><code>{content}</code></pre></div>'

html_body = re.sub(r'<pre><code class="language-mermaid">(.*?)</code></pre>', replace_mermaid, html_body, flags=re.DOTALL)

# Add page break markers before major sections
html_body = re.sub(r'<h2>(.*?)</h2>', r'<div class="section-break"></div><h2>\1</h2>', html_body)

FULL_HTML = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>183. Итальянский триптих сверхпроводимости — Триада Versace и Леванте</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Lora:ital,wght@0,400;0,500;0,600;1,400&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

  @page {{
    size: A4;
    margin: 18mm 16mm 18mm 16mm;
    @top-left {{
      content: "Внутренний ток • Статья 183";
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 7.5pt;
      color: #94a3b8;
      letter-spacing: 1px;
      text-transform: uppercase;
    }}
    @top-right {{
      content: "Итальянский триптих сверхпроводимости";
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 7.5pt;
      color: #94a3b8;
      letter-spacing: 1px;
    }}
    @bottom-center {{
      content: counter(page);
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 8pt;
      color: #94a3b8;
    }}
  }}

  @page:first {{
    margin: 0;
    @top-left {{ content: none; }}
    @top-right {{ content: none; }}
    @bottom-center {{ content: none; }}
  }}

  * {{
    box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }}

  body {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 9.5pt;
    line-height: 1.6;
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
    background: radial-gradient(circle at 50% 25%, #0f172a 0%, #030712 100%);
    color: #ffffff;
    padding: 30mm 24mm 24mm 24mm;
    text-align: center;
    position: relative;
    overflow: hidden;
  }}

  .cover-page::before {{
    content: "";
    position: absolute;
    top: -150px;
    left: 50%;
    transform: translateX(-50%);
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba(0, 180, 216, 0.22) 0%, rgba(3, 7, 18, 0) 70%);
    border-radius: 50%;
    pointer-events: none;
  }}

  .cover-series {{
    font-family: 'Cinzel', serif;
    font-size: 10pt;
    letter-spacing: 5px;
    text-transform: uppercase;
    color: #00b4d8;
    font-weight: 700;
  }}

  .cover-hero {{
    margin: auto 0;
  }}

  .cover-badge {{
    display: inline-block;
    padding: 6px 16px;
    background: rgba(0, 180, 216, 0.12);
    border: 1px solid rgba(0, 180, 216, 0.35);
    border-radius: 20px;
    font-size: 8.5pt;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #38bdf8;
    margin-bottom: 8mm;
  }}

  .cover-title {{
    font-family: 'Cinzel', serif;
    font-size: 24pt;
    font-weight: 800;
    line-height: 1.2;
    letter-spacing: 2px;
    color: #f8fafc;
    margin-bottom: 6mm;
    text-shadow: 0 4px 20px rgba(0, 180, 216, 0.3);
  }}

  .cover-divider {{
    width: 80px;
    height: 2px;
    background: linear-gradient(90deg, transparent, #00b4d8, transparent);
    margin: 6mm auto;
  }}

  .cover-subtitle {{
    font-family: 'Lora', serif;
    font-size: 13pt;
    font-style: italic;
    color: #94a3b8;
    max-width: 520px;
    margin: 0 auto 8mm auto;
    line-height: 1.5;
  }}

  .cover-triad-pills {{
    display: flex;
    justify-content: center;
    gap: 12px;
    margin-top: 6mm;
  }}

  .cover-pill {{
    padding: 8px 14px;
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 8px;
    font-size: 8pt;
    color: #cbd5e1;
    text-align: left;
    line-height: 1.4;
  }}

  .cover-pill strong {{
    display: block;
    color: #38bdf8;
    font-size: 8.5pt;
  }}

  .cover-footer {{
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding-top: 6mm;
    display: flex;
    justify-content: space-between;
    font-size: 8.5pt;
    color: #64748b;
  }}

  .cover-footer-author {{
    color: #94a3b8;
    font-weight: 600;
    letter-spacing: 1px;
  }}

  /* CONTENT STYLING */
  .content-container {{
    padding-top: 4mm;
  }}

  h1 {{
    font-family: 'Cinzel', serif;
    font-size: 18pt;
    font-weight: 800;
    color: #0f172a;
    border-bottom: 2px solid #00b4d8;
    padding-bottom: 3mm;
    margin-top: 0;
    margin-bottom: 6mm;
    letter-spacing: 1px;
  }}

  h2 {{
    font-family: 'Cinzel', serif;
    font-size: 13pt;
    font-weight: 700;
    color: #0f172a;
    border-left: 3px solid #00b4d8;
    padding-left: 8px;
    margin-top: 8mm;
    margin-bottom: 4mm;
    letter-spacing: 0.5px;
  }}

  h3 {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 10.5pt;
    font-weight: 700;
    color: #0284c7;
    margin-top: 5mm;
    margin-bottom: 2mm;
  }}

  p {{
    margin-top: 0;
    margin-bottom: 3mm;
    text-align: justify;
  }}

  /* CALLOUT BOXES */
  .callout {{
    border-left: 3px solid #0284c7;
    background: #f8fafc;
    padding: 10px 14px;
    margin: 4mm 0;
    border-radius: 0 6px 6px 0;
    font-size: 9.5pt;
  }}

  .callout-quote {{
    border-left-color: #00b4d8;
    background: #f0f9ff;
    font-family: 'Lora', serif;
    font-style: italic;
  }}

  .callout-title {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 700;
    font-size: 8.5pt;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #0369a1;
    margin-bottom: 4px;
  }}

  /* TABLES */
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 5mm 0;
    font-size: 8.5pt;
    page-break-inside: avoid;
  }}

  th {{
    background: #0f172a;
    color: #ffffff;
    font-weight: 600;
    text-align: left;
    padding: 7px 10px;
    border: 1px solid #1e293b;
    font-size: 8pt;
    letter-spacing: 0.5px;
  }}

  td {{
    padding: 7px 10px;
    border: 1px solid #cbd5e1;
    vertical-align: top;
    line-height: 1.45;
  }}

  tr:nth-child(even) {{
    background: #f8fafc;
  }}

  /* CODE AND ASCII DIAGRAMS */
  pre {{
    background: #0f172a;
    color: #f8fafc;
    padding: 10px 14px;
    border-radius: 6px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 8pt;
    line-height: 1.4;
    overflow-x: auto;
    margin: 4mm 0;
    border: 1px solid #1e293b;
    page-break-inside: avoid;
  }}

  code {{
    font-family: 'JetBrains Mono', monospace;
  }}

  p code, li code {{
    background: #f1f5f9;
    color: #0284c7;
    padding: 2px 5px;
    border-radius: 4px;
    font-size: 8.5pt;
    border: 1px solid #e2e8f0;
  }}

  /* MERMAID / SCHEME BOX */
  .mermaid-box {{
    background: #0f172a;
    border: 1px solid #00b4d8;
    border-radius: 8px;
    margin: 5mm 0;
    padding: 4px;
    page-break-inside: avoid;
  }}

  .mermaid-box pre {{
    margin: 0;
    background: transparent;
    border: none;
    color: #38bdf8;
  }}

  /* MATH SPANS */
  .math-inline {{
    font-family: 'Lora', serif;
    font-style: italic;
    color: #0f172a;
  }}

  .math-display {{
    text-align: center;
    font-family: 'Lora', serif;
    font-size: 11pt;
    padding: 4mm;
    margin: 4mm 0;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 6px;
  }}

  blockquote {{
    border-left: 3px solid #00b4d8;
    margin: 3mm 0;
    padding: 4px 14px;
    background: #f0fdfa;
    color: #0f172a;
    font-family: 'Lora', serif;
    font-size: 9.5pt;
  }}

  ul, ol {{
    margin-top: 0;
    margin-bottom: 3mm;
    padding-left: 20px;
  }}

  li {{
    margin-bottom: 1.5mm;
  }}

  hr {{
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 6mm 0;
  }}

  .section-break {{
    margin-top: 8mm;
  }}
</style>
</head>
<body>

<!-- COVER PAGE -->
<div class="cover-page">
  <div class="cover-series">Inner Current • Theoretical Monograph • 2026</div>
  
  <div class="cover-hero">
    <div class="cover-badge">Статья № 183 • Ольфакторно-акустический консилиенс</div>
    <div class="cover-title">Итальянский Триптих Сверхпроводимости</div>
    <div class="cover-divider"></div>
    <div class="cover-subtitle">Ольфакторно-акустический байпас неокортекса за 150 миллисекунд: Триада Versace, вокальный нерв Леванте и заземление Тандэн</div>
    
    <div class="cover-triad-pills">
      <div class="cover-pill">
        <strong>Узел I: Воздух / Свет</strong>
        Pour Homme Classic + «Leggera»
      </div>
      <div class="cover-pill">
        <strong>Узел II: Вода / Ток</strong>
        Dylan Blue + «Sono blu»
      </div>
      <div class="cover-pill">
        <strong>Узел III: Земля / Тандэн</strong>
        Oud Noir + «Magmamemoria»
      </div>
    </div>
  </div>
  
  <div class="cover-footer">
    <div class="cover-footer-author">Владимир Аньянов</div>
    <div>Санкт-Петербург — Милан — Катания, 2026</div>
  </div>
</div>

<!-- CONTENT CONTAINER -->
<div class="content-container">
{html_body}
</div>

</body>
</html>
"""

# Write HTML file
with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(FULL_HTML)
print(f"Saved HTML to: {OUTPUT_HTML}")

# Render to PDF using Playwright
print("Launching Playwright to render PDF...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(f"file:///{OUTPUT_HTML.replace(os.sep, '/')}", wait_until="networkidle")
    
    # Generate PDF
    os.makedirs(os.path.dirname(OUTPUT_PDF), exist_ok=True)
    page.pdf(
        path=OUTPUT_PDF,
        format="A4",
        print_background=True,
        margin={"top": "0mm", "bottom": "0mm", "left": "0mm", "right": "0mm"}
    )
    browser.close()

# Also copy to root and public/books
import shutil
shutil.copy2(OUTPUT_PDF, ROOT_PDF)
os.makedirs(os.path.dirname(PUBLIC_PDF), exist_ok=True)
shutil.copy2(OUTPUT_PDF, PUBLIC_PDF)

size_kb = os.path.getsize(OUTPUT_PDF) / 1024
print(f"SUCCESS! Rendered PDF at: {OUTPUT_PDF}")
print(f"PDF Size: {size_kb:.1f} KB")
print(f"Copied to: {ROOT_PDF}")
print(f"Copied to: {PUBLIC_PDF}")
