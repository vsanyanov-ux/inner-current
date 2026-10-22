import os
import sys
import re
import shutil
import markdown
from playwright.sync_api import sync_playwright
import pypdf

if sys.stdout:
    sys.stdout.reconfigure(encoding='utf-8')

b_info = {
    "md_path": r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Брошюра — 2500 лет сборки фонарика вслепую (История западной философии от досократиков до Ницше в свете контурной электродинамики).md",
    "output_html": r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\philosophy_2500_brochure.html",
    "output_pdf": r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\IC Library\Брошюра — 2500 лет сборки фонарика вслепую (История западной философии от досократиков до Ницше в свете контурной электродинамики).pdf",
    "vault_pdf": r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Брошюра — 2500 лет сборки фонарика вслепую (История западной философии от досократиков до Ницше в свете контурной электродинамики).pdf",
    "series": "Inner Current • Электродинамика Состояния • Манифест",
    "title": "2500 ЛЕТ СБОРКИ<br>ФОНАРИКА ВСЛЕПУЮ",
    "subtitle": "История западной философии от досократиков до Ницше в свете контурной электродинамики: как титаны мысли нащупывали контур, чего они пугались и в чём состоял их общий слепой изъян",
    "header_title": "Владимир Аньянов • 2500 лет сборки фонарика вслепую",
    "quote": "«История западной философии на протяжении двух с половиной тысячелетий — это не свалка абстрактных мнений, а драматическая летопись сборки карманного фонарика вслепую. Платон проклял медь проводов ради невидимого света; Стоики пытались гасить ожоги напряжением челюстей; Спиноза начертил поле, но оставил его на бумаге; Декарт разрубил кабель топором дуализма; Кант заперся в будке рассудка; Шопенгауэр нашел аккумулятор, но испугался искр и предложил разбить его аскезой; а Ницше воспел силу тока, но сжег проводку на собственном раскаленном эго. Внутренний ток не спорит ни с кем из них. Он просто кладет на стол принципиальную схему, соединяет клеммы реактора с лампочкой, сбрасывает сопротивление в ноль Ом — и включает свет.»",
    "gradient": "linear-gradient(145deg, #090d16 0%, #1e1b4b 50%, #2e1065 100%)",
    "accent": "#c084fc"
}

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

def generate_pdf():
    print(f"Reading markdown: {b_info['md_path']}")
    with open(b_info["md_path"], "r", encoding="utf-8") as f:
        raw_md = f.read()

    # Strip YAML frontmatter
    raw_md = re.sub(r"^---.*?---\s*", "", raw_md, flags=re.DOTALL)

    # Preprocess Callouts
    processed_md = re.sub(r"^>\s*\[!(\w+)\]([^\n]*(?:\n>[^\n]*)*)", replace_callout, raw_md, flags=re.MULTILINE)

    # Preprocess Chapters/Parts for page breaks
    processed_md = re.sub(r"^(## ⚡ ЧАСТЬ [^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
    processed_md = re.sub(r"^(## 📊 СВОДНЫЙ АУДИТ[^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
    processed_md = re.sub(r"^(## 🛠️ Практический алгоритм[^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
    processed_md = re.sub(r"^(## ⚡ Семь аксиом[^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)

    # Convert Markdown to HTML
    md_extensions = ['tables', 'fenced_code', 'codehilite', 'def_list', 'nl2br']
    html_body = markdown.markdown(processed_md, extensions=md_extensions)

    # Wrap tables in responsive containers
    html_body = html_body.replace("<table>", '<div class="table-wrapper"><table>')
    html_body = html_body.replace("</table>", '</table></div>')

    full_html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>{b_info['header_title']}</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js" onload="renderMathInElement(document.body, {{delimiters: [{{left: '$$', right: '$$', display: true}}, {{left: '$', right: '$', display: false}}]}});"></script>
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
    font-size: 10pt;
    line-height: 1.6;
    color: #1e293b;
    background: #ffffff;
    margin: 0;
    padding: 0;
  }}

  /* COVER STYLING */
  .cover-page {{
    page-break-after: always;
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 25mm 15mm 20mm 15mm;
    border: 1px solid #e2e8f0;
    background: {b_info['gradient']};
    color: #f8fafc;
    position: relative;
    box-sizing: border-box;
  }}

  .cover-series {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 8.5pt;
    font-weight: 700;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: {b_info['accent']};
    border-bottom: 2px solid {b_info['accent']};
    padding-bottom: 3mm;
    display: inline-block;
  }}

  .cover-hero {{
    text-align: center;
    margin: auto 0;
  }}

  .cover-icon {{
    width: 68px;
    height: 68px;
    margin: 0 auto 8mm auto;
    stroke: {b_info['accent']};
  }}

  .cover-author {{
    font-family: 'Cinzel', serif;
    font-size: 14pt;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #94a3b8;
    margin-bottom: 6mm;
  }}

  .cover-title {{
    font-family: 'Cinzel', serif;
    font-size: 26pt;
    font-weight: 700;
    letter-spacing: 0.05em;
    line-height: 1.25;
    color: #ffffff;
    margin-bottom: 6mm;
    text-shadow: 0 4px 14px rgba(0,0,0,0.5);
  }}

  .cover-subtitle {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 10.5pt;
    font-weight: 300;
    line-height: 1.6;
    color: #cbd5e1;
    max-width: 530px;
    margin: 0 auto;
  }}

  .cover-footer {{
    display: flex;
    justify-content: space-between;
    border-top: 1px solid #334155;
    padding-top: 4mm;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 8pt;
    letter-spacing: 0.1em;
    color: #64748b;
    text-transform: uppercase;
  }}

  /* FRONTISPIECE */
  .frontispiece {{
    page-break-after: always;
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 30mm 20mm;
    text-align: center;
    background: #ffffff;
  }}

  .frontispiece-quote {{
    font-size: 11pt;
    font-style: italic;
    line-height: 1.8;
    color: #334155;
    max-width: 530px;
    margin-bottom: 8mm;
    position: relative;
  }}

  .frontispiece-quote::before {{
    content: "«";
    font-size: 40pt;
    color: #cbd5e1;
    position: absolute;
    top: -25px;
    left: -20px;
    font-family: Georgia, serif;
  }}

  .frontispiece-author {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 9.5pt;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #0f172a;
  }}

  .chapter-break {{
    page-break-before: always;
    height: 0;
  }}

  h1 {{
    font-family: 'Cinzel', serif;
    font-size: 20pt;
    font-weight: 700;
    color: #0f172a;
    border-bottom: 2px solid #0f172a;
    padding-bottom: 3mm;
    margin-top: 0;
    margin-bottom: 5mm;
  }}

  h2 {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 13pt;
    font-weight: 700;
    color: #1e1b4b;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 2mm;
    margin-top: 7mm;
    margin-bottom: 4mm;
    page-break-after: avoid;
  }}

  h3 {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 11pt;
    font-weight: 600;
    color: #334155;
    margin-top: 5mm;
    margin-bottom: 2mm;
    page-break-after: avoid;
  }}

  p {{
    margin-top: 0;
    margin-bottom: 3.5mm;
    text-align: justify;
    text-justify: inter-word;
  }}

  ul, ol {{
    margin-top: 0;
    margin-bottom: 4mm;
    padding-left: 6mm;
  }}

  li {{
    margin-bottom: 1.5mm;
  }}

  blockquote {{
    border-left: 3px solid {b_info['accent']};
    background: #f8fafc;
    margin: 4mm 0;
    padding: 3mm 5mm;
    font-style: italic;
    color: #334155;
  }}

  pre {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.5pt;
    line-height: 1.4;
    background: #0f172a;
    color: #e2e8f0;
    padding: 4mm;
    border-radius: 4px;
    overflow-x: auto;
    margin: 4mm 0;
    page-break-inside: avoid;
  }}

  code {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5pt;
    background: #f1f5f9;
    color: #0f172a;
    padding: 1px 3px;
    border-radius: 2px;
  }}

  pre code {{
    background: transparent;
    color: inherit;
    padding: 0;
  }}

  /* CALLOUTS */
  .callout {{
    border-left: 3.5px solid #64748b;
    background: #f8fafc;
    border-radius: 0 4px 4px 0;
    margin: 5mm 0;
    padding: 3.5mm 5mm;
    page-break-inside: avoid;
  }}

  .callout-title {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 9.5pt;
    font-weight: 700;
    margin-bottom: 2mm;
    color: #0f172a;
  }}

  .callout-quote {{
    border-left-color: {b_info['accent']};
    background: #faf5ff;
  }}

  .callout-quote .callout-title {{
    color: #6b21a8;
  }}

  .callout-tip {{
    border-left-color: #10b981;
    background: #f0fdf4;
  }}

  .callout-tip .callout-title {{
    color: #047857;
  }}

  .callout-info {{
    border-left-color: #0284c7;
    background: #f0f9ff;
  }}

  .callout-info .callout-title {{
    color: #0369a1;
  }}

  /* TABLES */
  .table-wrapper {{
    width: 100%;
    overflow-x: auto;
    margin: 5mm 0;
    page-break-inside: avoid;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 8pt;
    line-height: 1.4;
  }}

  th, td {{
    border: 1px solid #cbd5e1;
    padding: 2mm 2.5mm;
    text-align: left;
    vertical-align: top;
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
    border: 0;
    height: 1px;
    background: #e2e8f0;
    margin: 6mm 0;
  }}
</style>
</head>
<body>

<!-- COVER PAGE -->
<div class="cover-page">
  <div class="cover-series">{b_info['series']}</div>
  <div class="cover-hero">
    <svg class="cover-icon" viewBox="0 0 24 24" fill="none" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
      <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"></path>
    </svg>
    <div class="cover-author">Владимир Аньянов</div>
    <div class="cover-title">{b_info['title']}</div>
    <div class="cover-subtitle">{b_info['subtitle']}</div>
  </div>
  <div class="cover-footer">
    <span>Архитектура Счастья • Дзен-Инженерия</span>
    <span>Ростов-на-Дону • 2026</span>
  </div>
</div>

<!-- FRONTISPIECE -->
<div class="frontispiece">
  <div class="frontispiece-quote">
    {b_info['quote']}
  </div>
  <div class="frontispiece-author">Владимир Аньянов</div>
</div>

<!-- CONTENT -->
{html_body}

</body>
</html>
"""

    with open(b_info["output_html"], "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"Generated HTML: {b_info['output_html']}")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file:///{b_info['output_html'].replace(os.sep, '/')}", wait_until="networkidle")

        header_template = f"""
        <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 7.5pt; color: #94a3b8; width: 100%; display: flex; justify-content: space-between; padding: 0 18mm;">
          <span>{b_info['header_title']}</span>
          <span>Библиотека Inner Current</span>
        </div>
        """

        footer_template = """
        <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 8pt; color: #64748b; width: 100%; display: flex; justify-content: center; padding: 0 18mm;">
          <span class="pageNumber"></span>
        </div>
        """

        page.pdf(
            path=b_info["output_pdf"],
            format="A4",
            print_background=True,
            display_header_footer=True,
            header_template=header_template,
            footer_template=footer_template,
            margin={"top": "20mm", "bottom": "20mm", "left": "18mm", "right": "18mm"}
        )
        page.close()
        browser.close()

    shutil.copy2(b_info["output_pdf"], b_info["vault_pdf"])
    reader = pypdf.PdfReader(b_info["output_pdf"])
    print(f"SUCCESS! Generated PDF: {b_info['output_pdf']} | Pages: {len(reader.pages)}, Size: {os.path.getsize(b_info['output_pdf']) / 1024:.1f} KB")

if __name__ == "__main__":
    generate_pdf()
