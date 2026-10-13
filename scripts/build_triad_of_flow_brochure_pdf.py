import os
import re
import markdown
from playwright.sync_api import sync_playwright
import pypdf
import shutil

VAULT_MD = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Брошюра — Триада потока (Универсальный закон систем, четверичный фрактал и соматика Внутреннего тока).md"
OUTPUT_HTML = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\triad_of_flow_brochure.html"
# Clean file name without forbidden or problematic characters (only safe characters: Russian letters, spaces, hyphens, brackets):
PDF_NAME = "Брошюра — Триада потока (Универсальный закон систем, четверичный фрактал и соматика Внутреннего тока).pdf"
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

# Preprocess Mermaid diagram blocks BEFORE markdown parser
def replace_mermaid(match):
    diagram = match.group(1).strip()
    return f'<div class="mermaid-wrap"><pre class="mermaid">\n{diagram}\n</pre></div>'

processed_md = re.sub(r"```mermaid([\s\S]*?)```", replace_mermaid, processed_md)

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
<title>Триада потока — Владимир Аньянов</title>
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
    font-size: 28pt;
    font-weight: 700;
    line-height: 1.25;
    color: #0f172a;
    letter-spacing: 0.03em;
    margin-bottom: 16px;
  }}

  .cover-author {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 13pt;
    font-weight: 600;
    color: #334155;
    letter-spacing: 0.08em;
    margin-bottom: 24px;
    text-transform: uppercase;
  }}

  .cover-subtitle {{
    font-family: 'Lora', Georgia, serif;
    font-size: 11pt;
    font-style: italic;
    color: #64748b;
    max-width: 580px;
    margin: 0 auto;
    line-height: 1.6;
  }}

  .cover-footer {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 8.5pt;
    color: #94a3b8;
    display: flex;
    justify-content: space-between;
    border-top: 1px solid #e2e8f0;
    padding-top: 14px;
    letter-spacing: 0.05em;
  }}

  /* FRONTISPIECE */
  .frontispiece {{
    page-break-after: always;
    height: 90vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 0 25mm;
    text-align: center;
  }}

  .frontispiece-quote {{
    font-family: 'Lora', Georgia, serif;
    font-size: 12.5pt;
    font-style: italic;
    line-height: 1.8;
    color: #334155;
    margin-bottom: 20px;
  }}

  .frontispiece-author {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 9.5pt;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #0d9488;
  }}

  /* CHAPTER BREAK */
  .chapter-break {{
    page-break-before: always;
  }}

  h1, h2, h3, h4 {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #0f172a;
    font-weight: 700;
    line-height: 1.3;
  }}

  h1 {{
    font-size: 20pt;
    margin-top: 0;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 2px solid #0d9488;
    letter-spacing: -0.01em;
  }}

  h2 {{
    font-size: 15pt;
    margin-top: 28px;
    margin-bottom: 12px;
    color: #0f172a;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 6px;
  }}

  h3 {{
    font-size: 12.5pt;
    margin-top: 22px;
    margin-bottom: 10px;
    color: #0d9488;
  }}

  p {{
    margin-top: 0;
    margin-bottom: 12px;
    text-align: justify;
    text-justify: inter-word;
  }}

  ul, ol {{
    margin-top: 0;
    margin-bottom: 14px;
    padding-left: 22px;
  }}

  li {{
    margin-bottom: 6px;
  }}

  strong {{
    font-weight: 600;
    color: #0f172a;
  }}

  /* CALLOUTS */
  .callout {{
    margin: 16px 0;
    padding: 14px 18px;
    border-radius: 6px;
    background: #f8fafc;
    border-left: 4px solid #94a3b8;
  }}

  .callout-quote {{
    background: #f0fdfa;
    border-left-color: #0d9488;
    font-style: italic;
  }}

  .callout-title {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 700;
    font-size: 9.5pt;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 6px;
    color: #0d9488;
  }}

  .callout-body p:last-child {{
    margin-bottom: 0;
  }}

  /* PRE & ASCII */
  pre {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.8pt;
    line-height: 1.35;
    background: #0f172a;
    color: #e2e8f0;
    padding: 12px 14px;
    border-radius: 6px;
    overflow-x: auto;
    margin: 14px 0;
  }}

  code {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5pt;
    background: #f1f5f9;
    padding: 2px 5px;
    border-radius: 3px;
    color: #0f172a;
  }}

  pre code {{
    background: transparent;
    padding: 0;
    color: inherit;
  }}

  /* TABLES */
  .table-wrapper {{
    margin: 16px 0;
    overflow-x: auto;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 9pt;
    line-height: 1.45;
  }}

  th, td {{
    padding: 8px 10px;
    border: 1px solid #cbd5e1;
    text-align: left;
  }}

  th {{
    background: #f1f5f9;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 700;
    color: #0f172a;
  }}

  tr:nth-child(even) td {{
    background: #f8fafc;
  }}

  hr {{
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 24px 0;
  }}
</style>
</head>
<body>

<!-- COVER -->
<div class="cover-page">
  <div class="cover-badge">Манифест и мастер-рукопись • 2026</div>
  <div class="cover-center">
    <div class="cover-title">Триада Потока</div>
    <div class="cover-author">Владимир Аньянов</div>
    <div class="cover-subtitle">Универсальный закон потоковых систем, четверичный фрактал цепи и прикладная соматика Внутреннего тока: Сквозная вертикаль от космической термодинамики к карманному фонарику счастья</div>
  </div>
  <div class="cover-footer">
    <span>Архитектура Счастья • Контурная Электродинамика</span>
    <span>Ростов-на-Дону • 2026</span>
  </div>
</div>

<!-- FRONTISPIECE -->
<div class="frontispiece">
  <div class="frontispiece-quote">«Внутренний ток, который изначально казался лишь инструментом избавления от личной душевной боли, оказался соматической дверью в фундаментальную физику Вселенной. Закон потоков объясняет, ПОЧЕМУ жизнь преодолевает энтропию. Четверичный фрактал задаёт чертёж, ИЗ КАКИХ УЗЛОВ состоит любой устойчивый контур. А Внутренний ток даёт человеку в руки простой соматический пульт, позволяя за тридцать секунд включить режим чистой сверхпроводимости прямо посреди бурь повседневного мира.»</div>
  <div class="frontispiece-author">Владимир Аньянов</div>
</div>

<!-- CONTENT -->
{html_body}

</body>
</html>
"""

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(FULL_HTML)

print("Generated clean HTML for brochure!")

# RENDER PDF VIA PLAYWRIGHT
print("Launching browser for PDF render...")
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"file:///{OUTPUT_HTML.replace(os.sep, '/')}", wait_until="networkidle")
    
    # Wait for KaTeX and Mermaid rendering
    page.wait_for_timeout(3000)
    
    header_template = """
    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 7.5pt; color: #94a3b8; width: 100%; display: flex; justify-content: space-between; padding: 0 18mm;">
      <span>Владимир Аньянов • Триада Потока</span>
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
