import os
import re
import shutil
import markdown
from playwright.sync_api import sync_playwright
import pypdf

VAULT_MD = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Брошюра — Женственность и касание жизни (Руки в масле, скорость и преодоление пассивности).md"
OUTPUT_HTML = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\human_feminine_brochure.html"
OUTPUT_PDF = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\IC Library\Брошюра — Женственность и касание жизни (Руки в масле, скорость и преодоление пассивности).pdf"
VAULT_PDF = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Брошюра — Женственность и касание жизни (Руки в масле, скорость и преодоление пассивности).pdf"

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
    body_html = markdown.markdown(body_text, extensions=['nl2br'])
    title_html = f'<div class="callout-title">{title}</div>' if title else ""
    return f'<div class="callout callout-{ctype}">{title_html}<div class="callout-body">{body_html}</div></div>'

processed_md = re.sub(r"^>\s*\[!(\w+)\]([^\n]*(?:\n>[^\n]*)*)", replace_callout, raw_md, flags=re.MULTILINE)

# Preprocess Chapters to inject page-break classes
processed_md = re.sub(r"^(## Часть I\.[^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
processed_md = re.sub(r"^(## Часть III\.[^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
processed_md = re.sub(r"^(## Часть V\.[^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
processed_md = re.sub(r"^(## Часть VI\.[^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
processed_md = re.sub(r"^(## Часть VII\.[^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
processed_md = re.sub(r"^(## Семь истин[^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)

# Convert Markdown to HTML
html_body = markdown.markdown(processed_md, extensions=['nl2br'])

FULL_HTML = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Женственность и касание жизни — Владимир Аньянов</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700;800&family=Lora:ital,wght@0,400;0,500;0,600;1,400;1,500;1,600&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

  @page {{
    size: A4;
    margin: 24mm 20mm 24mm 20mm;
  }}

  body {{
    font-family: 'Lora', Georgia, serif;
    font-size: 11pt;
    line-height: 1.75;
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
    font-size: 21pt;
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
    font-size: 14pt;
    margin-top: 10mm;
    margin-bottom: 5mm;
    border-bottom: 1px solid #fce7f3;
    padding-bottom: 2.5mm;
    font-weight: 700;
    color: #9d174d;
  }}

  h3 {{
    font-size: 11.5pt;
    margin-top: 7mm;
    margin-bottom: 3mm;
    font-weight: 600;
    color: #0f172a;
  }}

  p {{
    margin-top: 0;
    margin-bottom: 4mm;
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
    padding-top: 45mm;
  }}

  .frontispiece-badge {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 9pt;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #db2777;
    margin-bottom: 12mm;
  }}

  .frontispiece-title {{
    font-family: 'Cinzel', serif;
    font-size: 27pt;
    font-weight: 700;
    color: #0f172a;
    line-height: 1.25;
    margin-bottom: 6mm;
  }}

  .frontispiece-subtitle {{
    font-family: 'Lora', serif;
    font-style: italic;
    font-size: 13.5pt;
    color: #475569;
    max-width: 145mm;
    margin: 0 auto 22mm auto;
    line-height: 1.5;
  }}

  .frontispiece-divider {{
    width: 60mm;
    height: 1.5px;
    background: linear-gradient(to right, transparent, #db2777, transparent);
    margin: 0 auto 26mm auto;
  }}

  .frontispiece-author {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 11.5pt;
    font-weight: 600;
    letter-spacing: 0.08em;
    color: #1e293b;
    margin-top: 45mm;
  }}

  /* DEDICATION PAGE */
  .dedication-page {{
    page-break-after: always;
    text-align: center;
    padding: 48mm 15mm 0 15mm;
  }}

  .dedication-card {{
    border: 1px solid #fbcfe8;
    background: #fffdfa;
    border-radius: 10px;
    padding: 20mm 18mm;
    box-shadow: 0 4px 25px rgba(219, 39, 119, 0.06);
    max-width: 130mm;
    margin: 0 auto;
    position: relative;
  }}

  .dedication-card::before {{
    content: "✦  ✦  ✦";
    position: absolute;
    top: -10px;
    left: 50%;
    transform: translateX(-50%);
    background: #fffdfa;
    padding: 0 12px;
    color: #db2777;
    font-size: 10pt;
    letter-spacing: 0.15em;
  }}

  .dedication-badge {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 9pt;
    font-weight: 600;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #be185d;
    margin-bottom: 6mm;
  }}

  .dedication-text {{
    font-family: 'Lora', serif;
    font-style: italic;
    font-size: 12pt;
    line-height: 1.85;
    color: #334155;
    margin-bottom: 8mm;
  }}

  .dedication-highlight {{
    color: #9d174d;
    font-weight: 600;
    font-style: normal;
    font-family: 'Cinzel', serif;
    font-size: 14pt;
    display: block;
    margin-bottom: 5mm;
  }}

  .dedication-signature {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 10pt;
    font-weight: 600;
    color: #64748b;
    letter-spacing: 0.05em;
  }}

  /* CALLOUTS */
  blockquote, .callout {{
    margin: 6mm 0;
    padding: 5mm 7mm;
    border-radius: 6px;
    font-size: 10.5pt;
    line-height: 1.6;
  }}

  .callout-quote {{
    border-left: 3.5px solid #db2777;
    background: #fff1f2;
    color: #881337;
    font-style: italic;
  }}

  .callout-title {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 700;
    font-size: 9.5pt;
    margin-bottom: 2.5mm;
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }}

  ol, ul {{
    margin-top: 0;
    margin-bottom: 4mm;
    padding-left: 7mm;
  }}

  li {{
    margin-bottom: 2.5mm;
  }}

  hr {{
    border: 0;
    height: 1px;
    background: #fce7f3;
    margin: 7mm 0;
  }}
</style>
</head>
<body>

<!-- FRONTISPIECE COVER -->
<div class="frontispiece">
  <div class="frontispiece-badge">🌸 Манифест Свободы и Силы • 2026</div>
  <div class="frontispiece-title">Женственность и касание жизни</div>
  <div class="frontispiece-subtitle">Руки в масле, скорость и преодоление пассивности: Книга о праве быть живой, смелой и любимой</div>
  <div class="frontispiece-divider"></div>
  <div class="frontispiece-author">Владимир Аньянов</div>
</div>

<!-- DEDICATION PAGE -->
<div class="dedication-page">
  <div class="dedication-card">
    <div class="dedication-badge">Посвящение</div>
    <span class="dedication-highlight">Анне</span>
    <div class="dedication-text">
      Женщине, чьё сердце отказалось быть фарфоровой куклой на чужой полке.<br><br>
      Той, кто помнит свист ветра в лицо, горячее дыхание мотора и шершавую силу коры векового дуба.<br><br>
      Той, кто имеет смелость касаться этой реальности всеми десятью пальцами — преодолевая гравитацию и чужие страхи, но не предавая своей кошачьей нежности, королевской грации и способности беззаветно любить.<br><br>
      Никогда не сомневайся в своей силе.<br>
      <strong>Живи на полную мощность.</strong>
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
    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 7.5pt; color: #94a3b8; width: 100%; display: flex; justify-content: space-between; padding: 0 20mm;">
      <span>Владимир Аньянов • Женственность и касание жизни</span>
      <span>Для Анны</span>
    </div>
    """
    
    footer_template = """
    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 8pt; color: #64748b; width: 100%; display: flex; justify-content: center; padding: 0 20mm;">
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
        margin={"top": "22mm", "bottom": "22mm", "left": "20mm", "right": "20mm"}
    )
    browser.close()

# Copy to vault
shutil.copy2(OUTPUT_PDF, VAULT_PDF)

reader = pypdf.PdfReader(OUTPUT_PDF)
print(f"SUCCESS: Generated PDF! Total Pages: {len(reader.pages)}, Size: {os.path.getsize(OUTPUT_PDF) / 1024:.1f} KB")
