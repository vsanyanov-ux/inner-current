import os
import sys
import re
import shutil
import markdown
from playwright.sync_api import sync_playwright
import pypdf

if sys.stdout:
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

b_info = {
    "md_path": r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Брошюра — Радиоприёмник сознания (Детерминированная настройка счастья).md",
    "output_html": r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\radio_receiver_brochure.html",
    "output_pdf": r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\IC Library\Брошюра — Радиоприёмник сознания (Детерминированная настройка счастья).pdf",
    "vault_pdf": r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Брошюра — Радиоприёмник сознания (Детерминированная настройка счастья).pdf",
    "series": "Inner Current • Электродинамика Состояния • Манифест",
    "title": "РАДИОПРИЁМНИК<br>СОЗНАНИЯ",
    "subtitle": "От племенного забивания гвоздей корпусом к заводской инструкции 101,5 FM: почему счастье это не цель, а акустический резонанс, и как настроить прибор 10 раз из 10",
    "header_title": "Владимир Аньянов • Радиоприёмник сознания",
    "quote": "«Внутренний ток — это вообще не про \"поиск счастья\". Всё человечество тысячелетиями вело себя в отношении собственной психики в точности как австралийский абориген, которому в руки попал сложнейший всеволновый радиоприёмник. Не зная про электричество, радиоволны и колебательные контуры, он использовал его как мог: забивал тяжелым корпусом колышки в землю, сидел на нём у костра, молился на шипение динамика или десятилетиями исследовал структуру статического треска, объявляя его жестоким роком бытия. Внутренний ток впервые дал заводскую инструкцию к аппарату. Счастье — это не дар небес, не награда за страдания и не философская тайна. Счастье — это симфония Моцарта, которая с неизбежностью физического закона льётся из динамика, когда ты перестал колотить прибором по камням, включил питание и выставил верньер шкалы ровно на 101,5 FM. Это строгая технология: делай раз, делай два — и ты получаешь чистый звук десять раз из десяти».",
    "gradient": "linear-gradient(145deg, #18120c 0%, #3f1a07 50%, #1c1917 100%)",
    "accent": "#f59e0b"
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

def build_pdf():
    print(f"\n========================================================")
    print(f"Processing: {b_info['header_title']}")
    print(f"========================================================")
    
    with open(b_info["md_path"], "r", encoding="utf-8") as f:
        raw_md = f.read()

    # Strip YAML frontmatter
    raw_md = re.sub(r"^---.*?---\s*", "", raw_md, flags=re.DOTALL)

    # Preprocess Callouts
    processed_md = re.sub(r"^>\s*\[!(\w+)\]([^\n]*(?:\n>[^\n]*)*)", replace_callout, raw_md, flags=re.MULTILINE)

    # Preprocess Parts to inject page-break classes
    processed_md = re.sub(r"^(## Часть [^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
    processed_md = re.sub(r"^(## 🧭 Бортовой дашборд[^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
    processed_md = re.sub(r"^(## ⚡ Резюме[^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)

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
    font-size: 10.2pt;
    line-height: 1.62;
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
    color: #cbd5e1;
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
    color: #94a3b8;
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
    font-size: 11.2pt;
    font-style: italic;
    line-height: 1.8;
    color: #334155;
    max-width: 520px;
    margin-bottom: 8mm;
    position: relative;
  }}

  .frontispiece-author {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 9.5pt;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #d97706;
  }}

  /* TYPOGRAPHY */
  h1 {{
    font-family: 'Cinzel', serif;
    font-size: 19pt;
    font-weight: 700;
    color: #0f172a;
    line-height: 1.3;
    margin-top: 0;
    margin-bottom: 4mm;
    border-bottom: 2px solid #d97706;
    padding-bottom: 3mm;
  }}

  h2 {{
    font-family: 'Cinzel', serif;
    font-size: 13pt;
    font-weight: 600;
    color: #1e293b;
    margin-top: 7mm;
    margin-bottom: 3mm;
    border-left: 3px solid #d97706;
    padding-left: 3mm;
  }}

  h3 {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 10.5pt;
    font-weight: 600;
    color: #334155;
    margin-top: 4.5mm;
    margin-bottom: 2mm;
  }}

  p {{
    margin-top: 0;
    margin-bottom: 3.5mm;
    text-align: justify;
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
    border-left: 3px solid #cbd5e1;
    margin: 4mm 0;
    padding-left: 4mm;
    font-style: italic;
    color: #475569;
  }}

  pre {{
    background: #0f172a;
    color: #f8fafc;
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.2pt;
    line-height: 1.38;
    padding: 3.5mm;
    border-radius: 4px;
    overflow-x: auto;
    margin: 4mm 0;
  }}

  code {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5pt;
    background: #f1f5f9;
    color: #0f172a;
    padding: 1px 4px;
    border-radius: 3px;
  }}

  pre code {{
    background: transparent;
    color: inherit;
    padding: 0;
  }}

  /* CALLOUTS */
  .callout {{
    margin: 4.5mm 0;
    padding: 3.5mm 4.5mm;
    border-radius: 4px;
    background: #f8fafc;
    border-left: 4px solid #94a3b8;
  }}

  .callout-quote {{
    border-left-color: #d97706;
    background: #fffbeb;
  }}

  .callout-info {{
    border-left-color: #0ea5e9;
    background: #f0fdf4;
  }}

  .callout-important {{
    border-left-color: #dc2626;
    background: #fef2f2;
  }}

  .callout-title {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 700;
    font-size: 9.5pt;
    color: #0f172a;
    margin-bottom: 2mm;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }}

  /* TABLES */
  .table-wrapper {{
    margin: 4mm 0;
    overflow-x: auto;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 8pt;
    line-height: 1.45;
  }}

  th, td {{
    padding: 5px 8px;
    border: 1px solid #cbd5e1;
    text-align: left;
    vertical-align: top;
  }}

  th {{
    background: #0f172a;
    color: #ffffff;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }}

  tr:nth-child(even) {{
    background: #f8fafc;
  }}

  .chapter-break {{
    page-break-before: always;
  }}
</style>
</head>
<body>

<!-- COVER PAGE -->
<div class="cover-page">
  <div>
    <div class="cover-series">{b_info['series']}</div>
  </div>
  <div class="cover-hero">
    <svg class="cover-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
      <path d="M4.9 19.1C1 15.2 1 8.8 4.9 4.9"/>
      <path d="M7.8 16.2c-2.3-2.3-2.3-6.1 0-8.5"/>
      <circle cx="12" cy="12" r="2"/>
      <path d="M16.2 7.8c2.3 2.3 2.3 6.1 0 8.5"/>
      <path d="M19.1 4.9C23 8.8 23 15.1 19.1 19"/>
    </svg>
    <div class="cover-author">Владимир Аньянов</div>
    <div class="cover-title">{b_info['title']}</div>
    <div class="cover-subtitle">{b_info['subtitle']}</div>
  </div>
  <div class="cover-footer">
    <span>Библиотека Inner Current</span>
    <span>Октябрь 2026</span>
    <span>Master Protocol • Edition 1.0</span>
  </div>
</div>

<!-- FRONTISPIECE -->
<div class="frontispiece">
  <div class="frontispiece-quote">
    {b_info['quote']}
  </div>
  <div class="frontispiece-author">Владимир Аньянов</div>
</div>

<!-- MAIN CONTENT -->
<div class="main-content">
  {html_body}
</div>

</body>
</html>
"""

    with open(b_info["output_html"], "w", encoding="utf-8") as f:
        f.write(full_html)

    print(f"Generated HTML: {b_info['output_html']}")

    os.makedirs(os.path.dirname(b_info["output_pdf"]), exist_ok=True)

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

    # Also copy to Obsidian Vault for immediate access
    shutil.copy2(b_info["output_pdf"], b_info["vault_pdf"])

    reader = pypdf.PdfReader(b_info["output_pdf"])
    print(f"SUCCESS: Generated PDF {b_info['output_pdf']}! Total Pages: {len(reader.pages)}, Size: {os.path.getsize(b_info['output_pdf']) / 1024:.1f} KB")

if __name__ == "__main__":
    build_pdf()
