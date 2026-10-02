import os
import sys
import re
import markdown
from playwright.sync_api import sync_playwright

if sys.stdout:
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr:
    sys.stderr.reconfigure(encoding='utf-8')

OUTPUT_HTML = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\triptych_brochure.html"
OUTPUT_PDF = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\Триптих Сверхпроводимости — Леванте и Внутренний ток.pdf"
VAULT_MD = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Книга — Триптих Сверхпроводимости (Леванте и Внутренний ток).md"
LOCAL_MD = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\wiki\Книга — Триптих Сверхпроводимости (Леванте и Внутренний ток).md"

with open(VAULT_MD, "r", encoding="utf-8") as f:
    BROCHURE_MD = f.read()

with open(LOCAL_MD, "w", encoding="utf-8") as f:
    f.write(BROCHURE_MD)
print(f"Synced Markdown to Repo: {LOCAL_MD}")

# Convert Markdown to HTML
html_body = markdown.markdown(BROCHURE_MD, extensions=['extra', 'tables'])

# Clean up Mermaid blocks into styled visual containers or diagrams
def replace_mermaid(match):
    content = match.group(1).strip()
    return f'<div class="mermaid-box"><pre><code>{content}</code></pre></div>'

html_body = re.sub(r'<pre><code class="language-mermaid">(.*?)</code></pre>', replace_mermaid, html_body, flags=re.DOTALL)

# Add page break markers before major sections
html_body = re.sub(r'<h1>(.*?)</h1>', r'<div class="act-break"></div><h1>\1</h1>', html_body)

FULL_HTML = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>Триптих Сверхпроводимости — Леванте и Внутренний ток</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Lora:ital,wght@0,400;0,500;0,600;1,400&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

  @page {{
    size: A4;
    margin: 18mm 16mm 18mm 16mm;
    @bottom-center {{
      content: counter(page);
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 8pt;
      color: #94a3b8;
    }}
  }}

  @page:first {{
    margin: 0;
    @bottom-center {{
      content: none;
    }}
  }}

  * {{
    box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }}

  body {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 9.5pt;
    line-height: 1.55;
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
    background: radial-gradient(circle, rgba(0, 180, 216, 0.18) 0%, rgba(3, 7, 18, 0) 70%);
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

  .cover-emblem {{
    width: 68px;
    height: 68px;
    margin: 0 auto 8mm auto;
    color: #00b4d8;
    opacity: 0.9;
  }}

  .cover-author {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 11pt;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #94a3b8;
    margin-bottom: 5mm;
  }}

  .cover-title {{
    font-family: 'Cinzel', serif;
    font-size: 26pt;
    font-weight: 800;
    line-height: 1.15;
    letter-spacing: 2px;
    color: #f8fafc;
    margin-bottom: 5mm;
    text-shadow: 0 4px 20px rgba(0, 180, 216, 0.3);
  }}

  .cover-divider {{
    width: 80px;
    height: 2px;
    background: linear-gradient(90deg, transparent, #00b4d8, transparent);
    margin: 5mm auto;
  }}

  .cover-subtitle {{
    font-family: 'Lora', serif;
    font-size: 12.5pt;
    font-style: italic;
    color: #cbd5e1;
    max-width: 480px;
    margin: 0 auto;
    line-height: 1.45;
  }}

  .cover-quote {{
    font-family: 'Lora', serif;
    font-style: italic;
    font-size: 9.5pt;
    color: #64748b;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding-top: 6mm;
    margin-top: 10mm;
    line-height: 1.5;
  }}

  .cover-footer {{
    font-size: 8pt;
    letter-spacing: 2px;
    color: #475569;
    text-transform: uppercase;
  }}

  /* CONTENT STYLING */
  .content {{
    padding: 0;
  }}

  .act-break {{
    page-break-before: always;
  }}

  h1 {{
    font-family: 'Cinzel', serif;
    font-size: 15pt;
    font-weight: 700;
    color: #0a192f;
    letter-spacing: 0.5px;
    border-bottom: 2px solid #0077b6;
    padding-bottom: 2.5mm;
    margin-top: 0;
    margin-bottom: 4mm;
  }}

  h2 {{
    font-family: 'Cinzel', serif;
    font-size: 11.5pt;
    font-weight: 600;
    color: #0077b6;
    margin-top: 4.5mm;
    margin-bottom: 2.5mm;
  }}

  h3 {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 10pt;
    font-weight: 700;
    color: #1e293b;
    margin-top: 3.5mm;
    margin-bottom: 1.5mm;
  }}

  p {{
    margin-top: 0;
    margin-bottom: 3mm;
    text-align: justify;
  }}

  blockquote {{
    font-family: 'Lora', serif;
    font-style: italic;
    font-size: 9.5pt;
    background: #f0fdf4;
    border-left: 3px solid #00b4d8;
    margin: 3.5mm 0;
    padding: 3mm 4mm;
    color: #0f172a;
    border-radius: 0 4px 4px 0;
  }}

  blockquote p {{
    margin-bottom: 1.5mm;
  }}
  blockquote p:last-child {{
    margin-bottom: 0;
  }}

  pre {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.8pt;
    line-height: 1.4;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    padding: 3mm 4mm;
    margin: 3.5mm 0;
    white-space: pre-wrap;
    word-break: break-word;
    color: #334155;
  }}

  code {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 8pt;
    background: #f1f5f9;
    padding: 0.5mm 1.5mm;
    border-radius: 3px;
    color: #0f172a;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 8pt;
    margin: 3.5mm 0;
  }}

  th, td {{
    border: 1px solid #cbd5e1;
    padding: 2mm 2.5mm;
    text-align: left;
    vertical-align: top;
  }}

  th {{
    background: #0f172a;
    color: #ffffff;
    font-family: 'Cinzel', serif;
    font-weight: 600;
    font-size: 7.5pt;
    letter-spacing: 0.5px;
  }}

  tr:nth-child(even) td {{
    background: #f8fafc;
  }}

  .mermaid-box pre {{
    background: #f1f5f9;
    border: 1px dashed #94a3b8;
    font-size: 7.5pt;
    color: #1e293b;
    padding: 3mm;
  }}

  hr {{
    border: none;
    height: 1px;
    background: #e2e8f0;
    margin: 5mm 0;
  }}

  .math-display {{
    text-align: center;
    font-family: 'Lora', serif;
    font-style: italic;
    font-size: 11pt;
    color: #0077b6;
    margin: 3.5mm 0;
    padding: 2.5mm;
    background: #f8fafc;
    border-radius: 4px;
    border: 1px solid #e2e8f0;
  }}

  ul, ol {{
    margin: 1.5mm 0 3mm 0;
    padding-left: 5mm;
  }}

  li {{
    margin-bottom: 1.5mm;
  }}
</style>
</head>
<body>

<!-- COVER -->
<div class="cover-page">
  <div class="cover-series">Контурная Электродинамика Сознания</div>
  
  <div class="cover-hero">
    <svg class="cover-emblem" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2">
      <circle cx="12" cy="12" r="10"/>
      <path d="M12 2v20M2 12h20M7 7l10 10M17 7L7 17"/>
    </svg>
    <div class="cover-author">Владимир Аньянов</div>
    <div class="cover-title">ТРИПТИХ<br>СВЕРХПРОВОДИМОСТИ</div>
    <div class="cover-divider"></div>
    <div class="cover-subtitle">Леванте, Versace и Внутренний ток:<br>Акустико-ольфакторная онтология фазового перехода</div>
  </div>

  <div class="cover-quote">
    «Схемы объясняют ток рассудку. Музыка и аромат включают его прямо в теле за 150 миллисекунд.<br>
    Итальянский триптих Клаудии Лагона и триада Versace, объясняющие физику человеческого счастья».
  </div>

  <div class="cover-footer">LLM Wiki Publications • 2026</div>
</div>

<!-- CONTENT -->
<div class="content">
{html_body}
</div>

</body>
</html>
"""

# Remove the duplicated first H1 title from html_body since cover handles it
FULL_HTML = FULL_HTML.replace('<div class="act-break"></div><h1>ТРИПТИХ СВЕРХПРОВОДИМОСТИ</h1>\n<h2>Леванте, Versace и Внутренний ток: Акустико-ольфакторная онтология фазового перехода</h2>\n<p><strong>Автор:</strong> Владимир Аньянов<br />\n<strong>Музыкально-онтологический фокус:</strong> Claudia Lagona (Levante)<br />\n<strong>Ольфакторный консилиенс:</strong> Серия Versace Pour Homme (Classic, Dylan Blue, Oud Noir)</p>\n<hr />', '')

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(FULL_HTML)
print(f"Saved HTML: {OUTPUT_HTML}")

# Generate PDF with Playwright
print("Launching Playwright to render PDF...")
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"file:///{os.path.abspath(OUTPUT_HTML).replace(os.sep, '/')}")
    page.wait_for_timeout(1000)
    page.pdf(
        path=OUTPUT_PDF,
        format="A4",
        print_background=True,
        margin={"top": "0mm", "bottom": "0mm", "left": "0mm", "right": "0mm"}
    )
    browser.close()

print(f"SUCCESS! Rendered PDF at: {OUTPUT_PDF}")
size_kb = os.path.getsize(OUTPUT_PDF) / 1024
print(f"PDF Size: {size_kb:.1f} KB")
