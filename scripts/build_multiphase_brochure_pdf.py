import os
import sys
import re
import markdown
from playwright.sync_api import sync_playwright

if sys.stdout:
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr:
    sys.stderr.reconfigure(encoding='utf-8')

SOURCE_MD = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Брошюра — Многофазный мир (Электродинамика планетарного согласия).md"
OUTPUT_HTML = r"C:\Users\vanya\Antigravity Projects\Apps\Inner Current\multiphase_brochure.html"
OUTPUT_PDF = r"C:\Users\vanya\Antigravity Projects\Apps\Inner Current\Брошюра — Многофазный мир (Электродинамика планетарного согласия).pdf"

with open(SOURCE_MD, "r", encoding="utf-8") as f:
    raw_md = f.read()

# Strip YAML frontmatter
raw_md = re.sub(r'^---[\s\S]*?---\s*', '', raw_md)

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

# Clean up initial H1/H2 since cover handles it
html_body = re.sub(r'<h1>МНОГОФАЗНЫЙ МИР:.*?</h1>\s*<h2>.*?</h2>', '', html_body, flags=re.DOTALL)

HTML_TEMPLATE = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Многофазный мир: Электродинамика планетарного согласия</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700;900&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Lora:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
<style>
  @page {{
    size: A4;
    margin: 0;
  }}

  * {{
    box-sizing: border-box;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}

  body {{
    margin: 0;
    padding: 0;
    font-family: 'Inter', sans-serif;
    font-size: 9.5pt;
    line-height: 1.55;
    color: #1e293b;
    background: #ffffff;
  }}

  /* COVER STYLING */
  .cover-page {{
    width: 210mm;
    height: 297mm;
    page-break-after: always;
    background: radial-gradient(circle at 50% 25%, #1e293b 0%, #0f172a 50%, #020617 100%);
    color: #ffffff;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 22mm 20mm 18mm 20mm;
    position: relative;
    overflow: hidden;
  }}

  .cover-page::before {{
    content: "";
    position: absolute;
    top: -80px;
    right: -80px;
    width: 320px;
    height: 320px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(56, 189, 248, 0.15) 0%, transparent 70%);
    pointer-events: none;
  }}

  .cover-page::after {{
    content: "";
    position: absolute;
    bottom: -60px;
    left: -60px;
    width: 280px;
    height: 280px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(245, 158, 11, 0.12) 0%, transparent 70%);
    pointer-events: none;
  }}

  .cover-series {{
    font-family: 'Cinzel', serif;
    font-size: 8.5pt;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #38bdf8;
    border-bottom: 1px solid rgba(56, 189, 248, 0.3);
    padding-bottom: 3.5mm;
  }}

  .cover-hero {{
    margin: auto 0;
    text-align: center;
  }}

  .cover-emblem {{
    width: 64px;
    height: 64px;
    margin: 0 auto 6mm auto;
    stroke: #38bdf8;
    filter: drop-shadow(0 0 12px rgba(56, 189, 248, 0.6));
  }}

  .cover-author {{
    font-family: 'Cinzel', serif;
    font-size: 11pt;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #94a3b8;
    margin-bottom: 4mm;
  }}

  .cover-title {{
    font-family: 'Cinzel', serif;
    font-size: 26pt;
    font-weight: 900;
    letter-spacing: 2px;
    line-height: 1.15;
    color: #ffffff;
    text-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
  }}

  .cover-divider {{
    width: 50mm;
    height: 2px;
    background: linear-gradient(90deg, transparent, #38bdf8, #f59e0b, transparent);
    margin: 6mm auto;
  }}

  .cover-subtitle {{
    font-family: 'Inter', sans-serif;
    font-size: 11.5pt;
    font-weight: 300;
    line-height: 1.45;
    color: #cbd5e1;
    max-width: 155mm;
    margin: 0 auto;
  }}

  .cover-quote {{
    background: rgba(30, 41, 59, 0.7);
    border-left: 3px solid #38bdf8;
    border-right: 1px solid rgba(255, 255, 255, 0.05);
    border-top: 1px solid rgba(255, 255, 255, 0.05);
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 4px;
    padding: 4mm 5mm;
    font-family: 'Lora', serif;
    font-style: italic;
    font-size: 9pt;
    line-height: 1.5;
    color: #e2e8f0;
    backdrop-filter: blur(8px);
  }}

  .cover-footer {{
    display: flex;
    justify-content: space-between;
    font-size: 7.5pt;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #64748b;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding-top: 3mm;
  }}

  /* CONTENT STYLING */
  .content {{
    padding: 16mm 18mm 16mm 18mm;
  }}

  h1, h2, h3, h4 {{
    font-family: 'Cinzel', serif;
    color: #0f172a;
    page-break-after: avoid;
  }}

  h1 {{
    font-size: 15pt;
    font-weight: 700;
    margin-top: 6mm;
    margin-bottom: 3.5mm;
    padding-bottom: 2mm;
    border-bottom: 1.5px solid #0f172a;
    letter-spacing: 0.5px;
  }}

  h2 {{
    font-size: 12pt;
    font-weight: 700;
    margin-top: 5mm;
    margin-bottom: 2.5mm;
    color: #1e3a8a;
  }}

  h3 {{
    font-size: 10pt;
    font-weight: 600;
    margin-top: 3.5mm;
    margin-bottom: 1.5mm;
    color: #0369a1;
  }}

  p {{
    margin-top: 0;
    margin-bottom: 2.5mm;
    text-align: justify;
  }}

  pre {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.2pt;
    line-height: 1.35;
    background: #0f172a;
    color: #e2e8f0;
    border-radius: 4px;
    padding: 3mm 3.5mm;
    margin: 3.5mm 0;
    white-space: pre;
    overflow-x: auto;
    page-break-inside: avoid;
    box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
    border: 1px solid #1e293b;
  }}

  code {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.8pt;
    background: #f1f5f9;
    color: #0f172a;
    padding: 0.5mm 1.5mm;
    border-radius: 3px;
  }}

  .math-inline {{
    font-family: 'Lora', serif;
    font-style: italic;
    color: #0284c7;
    font-size: 9.5pt;
  }}

  .math-display {{
    text-align: center;
    font-family: 'Lora', serif;
    font-style: italic;
    font-size: 10.5pt;
    color: #0369a1;
    margin: 3mm 0;
    padding: 2mm;
    background: #f8fafc;
    border-radius: 4px;
    border: 1px solid #e2e8f0;
  }}

  /* CALLOUTS */
  .callout {{
    margin: 3.5mm 0;
    padding: 3.5mm 4mm;
    border-radius: 4px;
    font-size: 9pt;
    line-height: 1.5;
    page-break-inside: avoid;
  }}

  .callout-quote {{
    background: #f0fdf4;
    border-left: 3.5px solid #10b981;
    color: #064e3b;
  }}

  .callout-quote .callout-title {{
    font-weight: 700;
    color: #047857;
    margin-bottom: 1.5mm;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 8pt;
    margin: 3.5mm 0;
    page-break-inside: avoid;
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
  }}

  tr:nth-child(even) td {{
    background: #f8fafc;
  }}

  hr {{
    border: none;
    height: 1px;
    background: #cbd5e1;
    margin: 4.5mm 0;
  }}

  ul, ol {{
    margin-top: 0;
    margin-bottom: 2.5mm;
    padding-left: 5mm;
  }}

  li {{
    margin-bottom: 1.2mm;
  }}

  blockquote {{
    margin: 3mm 0;
    padding: 2.5mm 4mm;
    background: #f8fafc;
    border-left: 3px solid #64748b;
    font-style: italic;
    color: #334155;
  }}
</style>
</head>
<body>

<!-- COVER -->
<div class="cover-page">
  <div class="cover-series">Контурная Электродинамика Цивилизаций • Манифест 2026</div>

  <div class="cover-hero">
    <svg class="cover-emblem" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2">
      <circle cx="12" cy="12" r="10"/>
      <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
      <circle cx="12" cy="12" r="3"/>
    </svg>
    <div class="cover-author">Владимир Аньянов</div>
    <div class="cover-title">МНОГОФАЗНЫЙ МИР</div>
    <div class="cover-divider"></div>
    <div class="cover-subtitle">Электродинамика планетарного согласия:<br>Почему однополярный мир сгорел, в чём смертельная ловушка 1914 года и как теория Внутреннего тока превращает войну хищников в безыскровую энергосеть цивилизаций</div>
  </div>

  <div class="cover-quote">
    «Строить многополярный мир без принципиальной схемы электродинамики — всё равно что собирать термоядерный реактор методами кузнечного молота.<br>
    Настоящий многополярный мир — это многофазная сеть Николы Теслы: суверенные генераторы с гальванической развязкой, создающие единое вращающееся поле созидания».
  </div>

  <div class="cover-footer">
    <span>LLM Wiki Publications • Октябрь 2026</span>
    <span>Inner Current Edition</span>
  </div>
</div>

<!-- CONTENT -->
<div class="content">
{html_body}
</div>

</body>
</html>
"""

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(HTML_TEMPLATE)
print(f"Saved HTML to: {OUTPUT_HTML}")

# Generate PDF with Playwright
print("Launching Chromium via Playwright to generate PDF...")
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"file:///{os.path.abspath(OUTPUT_HTML).replace(os.sep, '/')}")
    page.wait_for_timeout(1500)
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
