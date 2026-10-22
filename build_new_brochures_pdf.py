import os
import re
import shutil
import markdown
from playwright.sync_api import sync_playwright
import pypdf

BROCHURES = [
    {
        "md_path": r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Брошюра — Синдром Кокосового Рафа (Почему люди путают счастье с удовольствием, иллюзия Пяти Сцен и трагедия починки исправной лампочки).md",
        "output_html": r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\coconut_raff_brochure.html",
        "output_pdf": r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\IC Library\Брошюра — Синдром Кокосового Рафа (Почему люди путают счастье с удовольствием, иллюзия Пяти Сцен и трагедия починки исправной лампочки).pdf",
        "vault_pdf": r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Брошюра — Синдром Кокосового Рафа (Почему люди путают счастье с удовольствием, иллюзия Пяти Сцен и трагедия починки исправной лампочки).pdf",
        "series": "Inner Current • Электродинамика Состояния • Манифест",
        "title": "СИНДРОМ КОКОСОВОГО<br>РАФА",
        "subtitle": "Почему люди путают счастье с удовольствием, иллюзия Пяти Сцен и трагедия починки исправной лампочки: манифест деконструкции гедонистической слепоты",
        "header_title": "Владимир Аньянов • Синдром Кокосового Рафа",
        "quote": "«Удовольствия — это всего лишь электроприборы. Это тостеры, кофемашины, неоновые вывески и пылесосы бытия. А счастье — это электрическое напряжение в домашней сети. Если на входе в дом выбило пробки и сопротивление эго взлетело в бесконечность ($R_{\\text{ego}} \\to \\infty$), сколько бы дорогих тостеров вы ни втыкали в розетки, внутри останется мёртвая тьма, а хлеб будет холодным и сырым. Трагедия человечества в том, что оно веками полирует тостеры и чинит молотком абсолютно исправные лампочки, не понимая, что в доме просто отключен ток.»",
        "gradient": "linear-gradient(145deg, #18120c 0%, #451a03 50%, #1c1917 100%)",
        "accent": "#f59e0b"
    },
    {
        "md_path": r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Брошюра — Костыльный цех метафизики (Четыре псевдо-инженера цивилизации, иллюзия очищающего страдания и почему для счастья не нужны философские протезы).md",
        "output_html": r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\metaphysics_crutch_factory_brochure.html",
        "output_pdf": r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\IC Library\Брошюра — Костыльный цех метафизики (Четыре псевдо-инженера цивилизации, иллюзия очищающего страдания и почему для счастья не нужны философские протезы).pdf",
        "vault_pdf": r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Брошюра — Костыльный цех метафизики (Четыре псевдо-инженера цивилизации, иллюзия очищающего страдания и почему для счастья не нужны философские протезы).pdf",
        "series": "Inner Current • Электродинамика Состояния • Манифест",
        "title": "КОСТЫЛЬНЫЙ ЦЕХ<br>МЕТАФИЗИКИ",
        "subtitle": "Четыре псевдо-инженера цивилизации, иллюзия очищающего страдания и почему для счастья не нужны философские протезы: манифест депосреднизации духа",
        "header_title": "Владимир Аньянов • Костыльный цех метафизики",
        "quote": "«Десять тысяч лет цивилизация не имела принципиальной электрической схемы человека. Когда у проводника раскалялись контакты и дымила проводка, к аварийному щитку сбегались четыре кустарных мастера: Священник, Астролог, Философ и Психолог. Ни один из них не понимал законов Кирхгофа и формулы Джоуля — Ленца. Они врезали в замкнутую цепь кадила, хрустальные шары, фолианты схоластики и терапевтические индульгенции, объявив аварийный ожог нихрома „очищающим страданием“. Но когда на стол ложится строгая принципиальная схема контура, вор пойман за руку: эго — это банальный нихромовый реостат. А при нулевом сопротивлении ($R \\to 0$) вся мировая метафизика превращается в ненужный костыльный склад перед лицом прямого действия, живой симфонии, объятий любимой и удара теннисной ракетки.»",
        "gradient": "linear-gradient(145deg, #090d16 0%, #1e1b4b 50%, #0f172a 100%)",
        "accent": "#38bdf8"
    }
]

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

def generate_brochure_pdf(b_info, browser):
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
    processed_md = re.sub(r"^(## 🛠️ Практический алгоритм[^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
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
    font-size: 10.5pt;
    line-height: 1.65;
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
    font-size: 11.5pt;
    font-style: italic;
    line-height: 1.8;
    color: #334155;
    max-width: 520px;
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
    color: #0284c7;
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
    border-bottom: 2px solid #0284c7;
    padding-bottom: 3mm;
  }}

  h2 {{
    font-family: 'Cinzel', serif;
    font-size: 13.5pt;
    font-weight: 600;
    color: #1e293b;
    margin-top: 8mm;
    margin-bottom: 3mm;
    border-left: 3px solid #0284c7;
    padding-left: 3mm;
  }}

  h3 {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 11pt;
    font-weight: 600;
    color: #334155;
    margin-top: 5mm;
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
    font-size: 7.6pt;
    line-height: 1.42;
    padding: 4mm;
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
    margin: 5mm 0;
    padding: 4mm 5mm;
    border-radius: 4px;
    background: #f8fafc;
    border-left: 4px solid #94a3b8;
  }}

  .callout-quote {{
    border-left-color: #0284c7;
    background: #f0f9ff;
  }}

  .callout-info {{
    border-left-color: #0ea5e9;
    background: #f0fdf4;
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

  .callout-body {{
    font-size: 9.5pt;
    line-height: 1.6;
    color: #334155;
  }}

  .chapter-break {{
    page-break-before: always;
  }}

  /* TABLES */
  .table-wrapper {{
    margin: 5mm 0;
    overflow-x: auto;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 8.5pt;
    line-height: 1.45;
  }}

  th, td {{
    border: 1px solid #cbd5e1;
    padding: 2.5mm 3mm;
    text-align: left;
  }}

  th {{
    background: #f1f5f9;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 600;
    color: #0f172a;
  }}

  hr {{
    border: none;
    border-top: 1px solid #e2e8f0;
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

    # Also copy to Obsidian Vault for immediate access
    shutil.copy2(b_info["output_pdf"], b_info["vault_pdf"])

    reader = pypdf.PdfReader(b_info["output_pdf"])
    print(f"SUCCESS: Generated PDF {b_info['output_pdf']}! Total Pages: {len(reader.pages)}, Size: {os.path.getsize(b_info['output_pdf']) / 1024:.1f} KB")

def main():
    print("Launching Chromium via Playwright...")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for b_info in BROCHURES:
            generate_brochure_pdf(b_info, browser)
        browser.close()
    print("\nAll brochures converted to PDF successfully!")

if __name__ == "__main__":
    main()
