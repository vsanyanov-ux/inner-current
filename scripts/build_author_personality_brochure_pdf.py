import os
import re
import shutil
import markdown
from playwright.sync_api import sync_playwright
import pypdf

VAULT_MD = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Брошюра — Личность автора (Хоккейный Мусин, этический нерв Толстого и Дзен-радиотехника — почему контур замкнулся в одной точке).md"
OUTPUT_HTML = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\author_personality_brochure.html"
OUTPUT_PDF = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\IC Library\Брошюра — Личность автора (Хоккейный Мусин, этический нерв Толстого и Дзен-радиотехника — почему контур замкнулся в одной точке).pdf"
VAULT_PDF = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Брошюра — Личность автора (Хоккейный Мусин, этический нерв Толстого и Дзен-радиотехника — почему контур замкнулся в одной точке).pdf"

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
processed_md = re.sub(r"^(## 🛠️ Практический экспресс-дашборд[^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
processed_md = re.sub(r"^(## 📜 Резюме[^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
processed_md = re.sub(r"^(## 🔗 Связанные[^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)

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
<title>Личность автора — Владимир Аньянов</title>
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
    border: 1px solid #fed7aa;
    background: linear-gradient(145deg, #fffbeb 0%, #fef3c7 40%, #ffedd5 100%);
    position: relative;
    box-sizing: border-box;
  }}

  .cover-series {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 8.5pt;
    font-weight: 700;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #c2410c;
    border-bottom: 2px solid #ea580c;
    padding-bottom: 3mm;
    display: inline-block;
  }}

  .cover-hero {{
    margin: auto 0;
  }}

  .cover-emblem {{
    width: 24mm;
    height: 24mm;
    color: #ea580c;
    margin-bottom: 8mm;
  }}

  .cover-author {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 12pt;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #78350f;
    margin-bottom: 5mm;
  }}

  .cover-title {{
    font-family: 'Cinzel', serif;
    font-size: 26pt;
    font-weight: 700;
    line-height: 1.15;
    color: #431407;
    letter-spacing: -0.01em;
    margin-bottom: 6mm;
  }}

  .cover-subtitle {{
    font-family: 'Lora', serif;
    font-size: 11pt;
    font-style: italic;
    line-height: 1.5;
    color: #7c2d12;
    max-width: 95%;
    border-left: 3px solid #ea580c;
    padding-left: 5mm;
  }}

  .cover-footer {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 8.5pt;
    color: #9a3412;
    border-top: 1px solid #fdba74;
    padding-top: 4mm;
    display: flex;
    justify-content: space-between;
  }}

  /* FRONTISPIECE */
  .frontispiece {{
    page-break-after: always;
    min-height: 80vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 20mm 15mm;
  }}

  .frontispiece-quote {{
    font-size: 11.5pt;
    font-style: italic;
    line-height: 1.7;
    color: #1e293b;
    max-width: 90%;
    margin-bottom: 8mm;
    position: relative;
    text-align: justify;
    text-justify: inter-word;
  }}

  .frontispiece-quote::before {{
    content: "“";
    font-family: 'Cinzel', serif;
    font-size: 40pt;
    color: #fdba74;
    position: absolute;
    top: -20px;
    left: -25px;
    opacity: 0.6;
  }}

  .frontispiece-author {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 700;
    font-size: 10pt;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #c2410c;
  }}

  /* TYPOGRAPHY */
  h1, h2, h3, h4 {{
    font-family: 'Cinzel', serif;
    color: #0f172a;
    letter-spacing: -0.01em;
  }}

  h1 {{
    font-size: 18pt;
    text-align: center;
    margin-top: 10mm;
    margin-bottom: 4mm;
    font-weight: 700;
    line-height: 1.25;
    color: #c2410c;
  }}

  h2 {{
    font-size: 12.5pt;
    margin-top: 9mm;
    margin-bottom: 4mm;
    padding-bottom: 2mm;
    border-bottom: 1px solid #fdba74;
    color: #9a3412;
    page-break-after: avoid;
  }}

  h3 {{
    font-size: 10.5pt;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 700;
    color: #1e293b;
    margin-top: 6mm;
    margin-bottom: 3mm;
    page-break-after: avoid;
  }}

  p {{
    margin-top: 0;
    margin-bottom: 3.5mm;
    text-align: justify;
    text-justify: inter-word;
  }}

  strong {{
    font-weight: 600;
    color: #0f172a;
  }}

  /* CALLOUTS */
  .callout {{
    margin: 5mm 0;
    padding: 4mm 5mm;
    border-radius: 2mm;
    background: #fff7ed;
    border-left: 4px solid #ea580c;
    page-break-inside: avoid;
  }}

  .callout-title {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 700;
    font-size: 9.5pt;
    color: #9a3412;
    margin-bottom: 2mm;
    display: flex;
    align-items: center;
  }}

  .callout-body {{
    font-size: 9.8pt;
    line-height: 1.55;
    color: #431407;
  }}

  .callout-body p:last-child {{
    margin-bottom: 0;
  }}

  .callout-quote {{
    background: #fdf2f8;
    border-left-color: #be185d;
  }}
  .callout-quote .callout-title {{
    color: #9d174d;
  }}

  .callout-info {{
    background: #f0fdf4;
    border-left-color: #16a34a;
  }}
  .callout-info .callout-title {{
    color: #15803d;
  }}

  /* MONOSPACE & CODE */
  code {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5pt;
    background: #f1f5f9;
    padding: 1px 4px;
    border-radius: 3px;
    color: #0f172a;
  }}

  pre {{
    background: #0f172a;
    color: #f8fafc;
    padding: 4mm 5mm;
    border-radius: 2mm;
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.2pt;
    line-height: 1.4;
    overflow-x: auto;
    margin: 5mm 0;
    border-left: 4px solid #ea580c;
    page-break-inside: avoid;
    white-space: pre;
  }}

  pre code {{
    background: transparent;
    color: inherit;
    padding: 0;
  }}

  /* TABLES */
  .table-wrapper {{
    margin: 5mm 0;
    page-break-inside: avoid;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 8.5pt;
    line-height: 1.45;
  }}

  th {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 700;
    background: #ffedd5;
    color: #9a3412;
    text-align: left;
    padding: 2.5mm 3mm;
    border: 1px solid #fed7aa;
  }}

  td {{
    padding: 2.5mm 3mm;
    border: 1px solid #fed7aa;
    vertical-align: top;
  }}

  ul, ol {{
    margin-top: 0;
    margin-bottom: 3.5mm;
    padding-left: 6mm;
  }}

  li {{
    margin-bottom: 1.5mm;
  }}

  .chapter-break {{
    page-break-before: always;
  }}
</style>
</head>
<body>

<!-- COVER PAGE -->
<div class="cover-page">
  <div class="cover-series">Брошюры Внутреннего Тока • Манифест Оператора</div>
  <div class="cover-hero">
    <div class="cover-author">Владимир Аньянов</div>
    <div class="cover-title">ЛИЧНОСТЬ АВТОРА</div>
    <div class="cover-subtitle">Кизляр, библиотека им. Чехова, 15 лет толстовства (20–35 лет), Радиотех vs Культурология, отказ от военной службы, Хоккейный Мусин в Волгодонске и Дзен-инженерия — почему контур замкнулся в одной точке</div>
  </div>
  <div class="cover-footer">
    <span>Архитектура Счастья • Электродинамика Созидания</span>
    <span>Ростов-на-Дону • 2026</span>
  </div>
</div>

<!-- FRONTISPIECE -->
<div class="frontispiece">
  <div class="frontispiece-quote">
    «Россия была высоковольтным полигоном, где нихромовая спираль духа накалилась добела, но одного географического напряжения мало — нужен был конкретный кристалл, в котором сойдутся лучи. Если бы автор жил в сытом мегаполисе, его внимание растворилось бы в амбициях, ресторанах и развлечениях. Если бы он остался в тишине монастыря, мир получил бы молчание. Если бы он был психологом, он создал бы очередную секту платных консультаций. Контур Внутреннего тока замкнулся ровно потому, что в одной биографии сплавились несовместимые стихии: детство в Кизляре на стыке мусульманского и русского миров, открывшее множественность путей жизни; русская классика в 14 лет, внедрившая вопрос о правде и счастье; несостоявшийся побег в культурологию и суровая родовая колея Таганрогского радиотеха, давшая математический аппарат электродинамики; студенческое потрясение в библиотеке им. Чехова и пятнадцать лет толстовства (20–35 лет) с открытием жизни ради духа по трактату „О жизни“; бескомпромиссный отказ от военной службы под угрозой тюрьмы, доказавший верность принципам до конца; английский язык, ставший окном в глобальный мир из провинции; возвращение в атомный Волгодонск, где слово „реактор“ витает в воздухе; десять лет яростного хоккея на роликах, вбившего кинетический Мусин (не-ум) в кости; балконный фрезер асфальтовой шайбы; инвестиции после ретритов Ситы; освобождающий переворот Ошо, разбивший тюрьму христианской морали и вернувший радость жизни и Дзен; лазерный диагноз Менячихина „ты духовностью чинишь несчастье“; беговая дорожка и внезапный щелчок фонарика. Жизнь не потратила ни одного дня впустую: она методично ковала прибор».
  </div>
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

# Ensure IC Library directory exists
os.makedirs(os.path.dirname(OUTPUT_PDF), exist_ok=True)

# RENDER PDF VIA PLAYWRIGHT
print("Launching browser for PDF render...")
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"file:///{OUTPUT_HTML.replace(os.sep, '/')}", wait_until="networkidle")
    
    header_template = """
    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 7.5pt; color: #9a3412; width: 100%; display: flex; justify-content: space-between; padding: 0 18mm;">
      <span>Владимир Аньянов • Личность автора</span>
      <span>Библиотека Inner Current</span>
    </div>
    """
    
    footer_template = """
    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 8pt; color: #78350f; width: 100%; display: flex; justify-content: center; padding: 0 18mm;">
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
