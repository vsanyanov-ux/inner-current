import os
import sys
import re
import markdown
from playwright.sync_api import sync_playwright

if sys.stdout:
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr:
    sys.stderr.reconfigure(encoding='utf-8')

SOURCE_MD = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Книга — Великий Синтез (Революции материи, трагедия духа и электродинамика человека).md"
OUTPUT_HTML = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\great_synthesis_book.html"
OUTPUT_PDF = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\Книга — Великий Синтез (Революции материи, трагедия духа и электродинамика человека).pdf"
VAULT_PDF = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Книга — Великий Синтез (Революции материи, трагедия духа и электродинамика человека).pdf"

with open(SOURCE_MD, "r", encoding="utf-8") as f:
    raw_md = f.read()

# Strip YAML frontmatter if any
raw_md = re.sub(r"^---[\s\S]*?---\n", "", raw_md)

# Preprocess Obsidian Callouts (> [!quote], > [!tip], etc.)
def replace_callout(match):
    ctype = match.group(1).lower()
    content = match.group(2)
    lines = [re.sub(r"^>\s?", "", line) for line in content.strip().split("\n")]
    title = lines[0].strip() if lines else ""
    body_lines = lines[1:] if len(lines) > 1 else []
    body_text = "\n".join(body_lines).strip()
    body_html = markdown.markdown(body_text, extensions=['tables', 'fenced_code', 'nl2br'])
    title_html = f'<div class="callout-title">{title}</div>' if title else ""
    return f'<div class="callout callout-{ctype}">{title_html}<div class="callout-body">{body_html}</div></div>\n\n'

processed_md = re.sub(r"^>\s*\[!(\w+)\]([^\n]*(?:\n>[^\n]*)*)", replace_callout, raw_md, flags=re.MULTILINE)

# Remove the duplicated first H1 / H2 from markdown body since the Cover Page handles them
processed_md = re.sub(
    r"# Великий Синтез: Революции Материи, Трагедия Духа и Электродинамика Человека\s*\n+## [^\n]+\s*\n+\*\*Автор:\*\*[^\n]+\s*\n+\*\*Серия:\*\*[^\n]+\s*\n+\*\*Статус:\*\*[^\n]+\s*\n+\*\*Год создания:\*\*[^\n]+\s*\n+---\s*\n*",
    "",
    processed_md
)

# Convert Markdown to HTML
md_extensions = ['tables', 'fenced_code', 'nl2br', 'sane_lists']
html_body = markdown.markdown(processed_md, extensions=md_extensions)

# Mark Parts with page-breaks
html_body = re.sub(r'<h1>(Часть [I|V|X]+.*?|Заключение.*?)</h1>', r'<div class="part-page-break"></div><h1 class="part-title">\1</h1>', html_body)
html_body = re.sub(r'<h2>(Глава \d+.*?)</h2>', r'<div class="chapter-anchor"></div><h2 class="chapter-title">\1</h2>', html_body)

HTML_CONTENT = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Великий Синтез: Революции Материи, Трагедия Духа и Электродинамика Человека</title>

<!-- Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Lora:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">

<!-- KaTeX for pristine math rendering -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"
    onload="renderMathInElement(document.body, {{
        delimiters: [
            {{left: '$$', right: '$$', display: true}},
            {{left: '$', right: '$', display: false}}
        ],
        throwOnError: false
    }});"></script>

<style>
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

  html, body {{
    margin: 0;
    padding: 0;
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    font-size: 9.6pt;
    line-height: 1.62;
    color: #1e293b;
    background: #ffffff;
  }}

  /* ==========================================
     COVER PAGE: WHITE BACKGROUND (ТИТУЛ С БЕЛЫМ ФОНОМ)
     ========================================== */
  .cover-page {{
    width: 210mm;
    height: 297mm;
    page-break-after: always;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background: #ffffff;
    padding: 22mm 20mm 20mm 20mm;
    position: relative;
    box-sizing: border-box;
    border: 1px solid #ffffff;
  }}

  /* Architectural geometric hairline border */
  .cover-frame {{
    position: absolute;
    top: 12mm;
    left: 12mm;
    right: 12mm;
    bottom: 12mm;
    border: 1px solid #e2e8f0;
    pointer-events: none;
  }}

  .cover-frame::before {{
    content: "";
    position: absolute;
    top: 3mm;
    left: 3mm;
    right: 3mm;
    bottom: 3mm;
    border: 0.5px solid #cbd5e1;
  }}

  .cover-corner-tl, .cover-corner-tr, .cover-corner-bl, .cover-corner-br {{
    position: absolute;
    width: 10px;
    height: 10px;
    border-color: #0284c7;
    pointer-events: none;
  }}
  .cover-corner-tl {{ top: 10mm; left: 10mm; border-top: 2px solid #0284c7; border-left: 2px solid #0284c7; }}
  .cover-corner-tr {{ top: 10mm; right: 10mm; border-top: 2px solid #0284c7; border-right: 2px solid #0284c7; }}
  .cover-corner-bl {{ bottom: 10mm; left: 10mm; border-bottom: 2px solid #0284c7; border-left: 2px solid #0284c7; }}
  .cover-corner-br {{ bottom: 10mm; right: 10mm; border-bottom: 2px solid #0284c7; border-right: 2px solid #0284c7; }}

  .cover-top {{
    text-align: center;
    padding-top: 10mm;
    z-index: 10;
  }}

  .cover-series-badge {{
    display: inline-block;
    font-family: 'Cinzel', serif;
    font-size: 8pt;
    font-weight: 700;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #0284c7;
    background: #f0f9ff;
    border: 1px solid #bae6fd;
    padding: 4px 14px;
    border-radius: 20px;
    margin-bottom: 8mm;
  }}

  .cover-author {{
    font-family: 'Cinzel', serif;
    font-size: 13pt;
    font-weight: 700;
    letter-spacing: 5px;
    text-transform: uppercase;
    color: #334155;
    margin: 0;
  }}

  .cover-center {{
    text-align: center;
    padding: 0 4mm;
    z-index: 10;
    margin: auto 0;
  }}

  .cover-emblem {{
    width: 72px;
    height: 72px;
    margin: 0 auto 8mm auto;
  }}

  .cover-title {{
    font-family: 'Cinzel', serif;
    font-size: 32pt;
    font-weight: 900;
    letter-spacing: 2px;
    color: #0f172a;
    line-height: 1.15;
    margin: 0 0 5mm 0;
    text-transform: uppercase;
  }}

  .cover-subtitle {{
    font-family: 'Lora', Georgia, serif;
    font-size: 13.5pt;
    font-weight: 500;
    font-style: italic;
    color: #0284c7;
    line-height: 1.45;
    margin: 0 0 7mm 0;
  }}

  .cover-divider {{
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 7mm auto;
    width: 60%;
  }}

  .cover-divider-line {{
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, transparent, #cbd5e1, transparent);
  }}

  .cover-divider-symbol {{
    padding: 0 12px;
    color: #0284c7;
    font-size: 11pt;
  }}

  .cover-tagline {{
    font-size: 10pt;
    color: #475569;
    max-width: 145mm;
    margin: 0 auto;
    line-height: 1.6;
    font-weight: 400;
  }}

  .cover-bottom {{
    text-align: center;
    padding-bottom: 8mm;
    z-index: 10;
  }}

  .cover-quote-box {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-left: 3px solid #0284c7;
    padding: 4mm 6mm;
    border-radius: 4px;
    max-width: 145mm;
    margin: 0 auto 6mm auto;
    text-align: left;
  }}

  .cover-quote-text {{
    font-family: 'Lora', serif;
    font-style: italic;
    font-size: 8.8pt;
    color: #334155;
    line-height: 1.5;
    margin: 0;
  }}

  .cover-meta {{
    font-size: 7.5pt;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #94a3b8;
    line-height: 1.6;
  }}

  /* ==========================================
     INTERIOR CONTENT STYLING
     ========================================== */
  .book-content {{
    padding: 0;
  }}

  .part-page-break {{
    page-break-before: always;
  }}

  .part-title {{
    font-family: 'Cinzel', serif;
    font-size: 18pt;
    font-weight: 800;
    color: #0f172a;
    border-bottom: 2px solid #0284c7;
    padding-bottom: 3mm;
    margin-top: 10mm;
    margin-bottom: 6mm;
    text-transform: uppercase;
    letter-spacing: 1px;
    break-after: avoid;
  }}

  .chapter-title {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 12.5pt;
    font-weight: 700;
    color: #0369a1;
    margin-top: 8mm;
    margin-bottom: 3.5mm;
    break-after: avoid;
  }}

  h3 {{
    font-size: 10.5pt;
    font-weight: 700;
    color: #1e293b;
    margin-top: 5mm;
    margin-bottom: 2.5mm;
    break-after: avoid;
  }}

  p {{
    margin: 0 0 3.5mm 0;
    text-align: justify;
    text-justify: inter-word;
    hyphens: auto;
  }}

  strong {{
    color: #0f172a;
    font-weight: 600;
  }}

  em {{
    font-family: 'Lora', Georgia, serif;
  }}

  hr {{
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 6mm 0;
  }}

  /* Lists */
  ul, ol {{
    margin: 0 0 4mm 0;
    padding-left: 6mm;
  }}

  li {{
    margin-bottom: 1.5mm;
  }}

  /* Callouts */
  .callout {{
    margin: 5mm 0;
    padding: 4mm 5mm;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-left: 4px solid #0284c7;
    border-radius: 4px;
    break-inside: avoid;
  }}

  .callout-quote {{
    background: #f0fdf4;
    border-color: #bbf7d0;
    border-left-color: #16a34a;
  }}

  .callout-title {{
    font-family: 'Cinzel', serif;
    font-size: 9pt;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: #166534;
    margin-bottom: 2mm;
  }}

  .callout-body p:last-child {{
    margin-bottom: 0;
  }}

  /* Code / Preformatted ASCII diagrams */
  pre {{
    font-family: 'JetBrains Mono', Consolas, monospace;
    font-size: 7.8pt;
    line-height: 1.35;
    background: #f8fafc;
    color: #0f172a;
    border: 1px solid #e2e8f0;
    border-left: 3px solid #0284c7;
    padding: 3.5mm 4mm;
    border-radius: 4px;
    overflow-x: auto;
    margin: 4mm 0;
    break-inside: avoid;
    white-space: pre;
  }}

  code {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5pt;
    background: #f1f5f9;
    padding: 1px 4px;
    border-radius: 3px;
    color: #0369a1;
  }}

  pre code {{
    background: transparent;
    padding: 0;
    color: inherit;
    font-size: inherit;
  }}

  /* Tables */
  table {{
    width: 100%;
    border-collapse: collapse;
    margin: 5mm 0;
    font-size: 8.8pt;
    break-inside: avoid;
  }}

  th, td {{
    border: 1px solid #cbd5e1;
    padding: 2.5mm 3.5mm;
    text-align: left;
    vertical-align: top;
  }}

  th {{
    background: #f1f5f9;
    color: #0f172a;
    font-weight: 700;
  }}

  tr:nth-child(even) td {{
    background: #f8fafc;
  }}

  /* Math */
  .katex {{
    font-size: 1.05em !important;
  }}

  .katex-display {{
    margin: 4mm 0 !important;
    padding: 2mm 0;
  }}

</style>
</head>
<body>

<!-- ==========================================
     TITLE / COVER PAGE (WHITE BACKGROUND)
     ========================================== -->
<div class="cover-page">
  <div class="cover-frame"></div>
  <div class="cover-corner-tl"></div>
  <div class="cover-corner-tr"></div>
  <div class="cover-corner-bl"></div>
  <div class="cover-corner-br"></div>

  <div class="cover-top">
    <div class="cover-series-badge">Библиотека «Внутренний ток» • Мастер-рукопись</div>
    <div class="cover-author">Владимир Аньянов</div>
  </div>

  <div class="cover-center">
    <!-- Minimalist Vector Emblem of Closed Circuit & Superconductivity -->
    <svg class="cover-emblem" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="50" cy="50" r="44" stroke="#e2e8f0" stroke-width="2"/>
      <circle cx="50" cy="50" r="38" stroke="#0284c7" stroke-width="2.5" stroke-dasharray="8 4"/>
      <circle cx="50" cy="50" r="24" stroke="#0f172a" stroke-width="2"/>
      <circle cx="50" cy="50" r="10" fill="#0284c7"/>
      <!-- Cardinal Axis Circuit Keys -->
      <line x1="50" y1="2" x2="50" y2="12" stroke="#0284c7" stroke-width="3"/>
      <line x1="50" y1="88" x2="50" y2="98" stroke="#0284c7" stroke-width="3"/>
      <line x1="2" y1="50" x2="12" y2="50" stroke="#0284c7" stroke-width="3"/>
      <line x1="88" y1="50" x2="98" y2="50" stroke="#0284c7" stroke-width="3"/>
      <!-- Energy Radiance Ray -->
      <path d="M50 40 L53 47 L60 50 L53 53 L50 60 L47 53 L40 50 L47 47 Z" fill="#ffffff"/>
    </svg>

    <h1 class="cover-title">ВЕЛИКИЙ СИНТЕЗ</h1>
    <div class="cover-subtitle">Революции Материи, Трагедия Духа и Электродинамика Человека</div>

    <div class="cover-divider">
      <div class="cover-divider-line"></div>
      <div class="cover-divider-symbol">⚡</div>
      <div class="cover-divider-line"></div>
    </div>

    <div class="cover-tagline">
      Как наука покорила вещество, почему десять тысяч лет поисков не спасли душу и как замкнутый контур соединил две половины бытия
    </div>
  </div>

  <div class="cover-bottom">
    <div class="cover-quote-box">
      <p class="cover-quote-text">
        «Счастье оказалось не наградой на небесах и не генетической лотереей, а режимом сверхпроводимости замкнутого контура. Великий Синтез свершился: дух и материя соединились в одном строгом уравнении жизни.»
      </p>
    </div>
    <div class="cover-meta">
      Каноническая мастер-рукопись • Издание 2026<br>
      DOI: 10.5281/zenodo.22958926 • Creative Commons CC BY 4.0
    </div>
  </div>
</div>

<!-- ==========================================
     BOOK INTERIOR
     ========================================== -->
<div class="book-content">
{html_body}
</div>

</body>
</html>
"""

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)
print(f"Saved compiled HTML to: {OUTPUT_HTML}")

# Generate PDF via Playwright Chromium
print("Launching Chromium to render PDF...")
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"file:///{os.path.abspath(OUTPUT_HTML).replace(os.sep, '/')}", wait_until="networkidle")
    # Wait for KaTeX to finish rendering
    page.wait_for_timeout(2000)
    page.pdf(
        path=OUTPUT_PDF,
        format="A4",
        print_background=True,
        display_header_footer=False,
        margin={"top": "0mm", "bottom": "0mm", "left": "0mm", "right": "0mm"}
    )
    browser.close()

print(f"SUCCESS! Rendered PDF at: {OUTPUT_PDF}")
size_kb = os.path.getsize(OUTPUT_PDF) / 1024
print(f"PDF Size: {size_kb:.1f} KB")

# Copy to Obsidian Vault and public site directory as well
import shutil
shutil.copyfile(OUTPUT_PDF, VAULT_PDF)
print(f"Synced PDF to Obsidian Vault: {VAULT_PDF}")
PUBLIC_PDF = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\public\books\great_synthesis.pdf"
shutil.copyfile(OUTPUT_PDF, PUBLIC_PDF)
print(f"Synced PDF to Public site: {PUBLIC_PDF}")

