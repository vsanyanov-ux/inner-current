import os
import re
import sys
import shutil
import markdown
from playwright.sync_api import sync_playwright
import pypdf

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

VAULT_DIR = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki"
LIB2_DIR = r"C:\Users\vanya\Antigravity Projects\Apps\Inner Current\IC Library\Золотая семерка 2.0"
LIB_DIR = r"C:\Users\vanya\Antigravity Projects\Apps\Inner Current\IC Library"
LOCAL_BUILD_DIR = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\pdf_build"
DIST_DIR = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\dist_site\books"
PUB_DIR = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\public\books"

os.makedirs(LOCAL_BUILD_DIR, exist_ok=True)
os.makedirs(LIB2_DIR, exist_ok=True)
os.makedirs(DIST_DIR, exist_ok=True)
os.makedirs(PUB_DIR, exist_ok=True)

KATEX_SCRIPTS = r"""
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"></script>
<script>
  window.addEventListener('load', () => {
    if (typeof renderMathInElement !== 'undefined') {
      renderMathInElement(document.body, {
        delimiters: [
          {left: '$$', right: '$$', display: true},
          {left: '\\[', right: '\\]', display: true},
          {left: '\\(', right: '\\)', display: false},
          {left: '$', right: '$', display: false}
        ],
        throwOnError: false
      });
    }
    window.katexDone = true;
  });
</script>
"""

# Book definitions
BOOKS = [
    {
        "id": "01_canon",
        "title": "Внутренний ток: Архитектура Человека",
        "subtitle": "Канон Сверхпроводимости 3.1: Прикладная соматическая электродинамика, схемотехника карманного фонарика и полный потенциал открытия И. Пригожина",
        "series": "Библиотека «Золотая Семёрка 2.0» — Книга 1 (Канон 3.1)",
        "author": "Владимир Аньянов",
        "edition": "Master Edition 3.1 (Superconductivity Canon)",
        "md_source": os.path.join(LIB2_DIR, "01 — Владимир Аньянов — Внутренний ток (Архитектура Человека — Канон Сверхпроводимости).md"),
        "pdf_name_lib": "01 — Владимир Аньянов — Внутренний ток (Архитектура Человека — Канон Сверхпроводимости).pdf",
        "pdf_name_vault": "Книга — Внутренний ток (Архитектура Человека — Канон Сверхпроводимости).pdf",
        "site_slugs": ["01_canon_superconductivity.pdf"],
        "emblem": """<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M50 10 L50 90 M25 35 L75 35 M35 65 L65 65"/><circle cx="50" cy="50" r="35"/></svg>"""
    },
    {
        "id": "01",
        "title": "Внутренний ток",
        "subtitle": "Архитектура человека — схемотехника фонарика и соматическая сверхпроводимость",
        "series": "Библиотека «Золотая Семёрка 2.0» — Книга 1 (Фундамент)",
        "author": "Владимир Аньянов",
        "edition": "Master Edition 2.0 (Somatic Foundation N=1)",
        "md_source": os.path.join(LIB2_DIR, "01 — Владимир Аньянов — Внутренний ток (Архитектура человека — схемотехника фонарика и соматическая сверхпроводимость).md"),
        "pdf_name_lib": "01 — Владимир Аньянов — Внутренний ток (Архитектура человека — схемотехника фонарика и соматическая сверхпроводимость).pdf",
        "pdf_name_vault": "Книга — Внутренний ток (Архитектура человека — схемотехника фонарика и соматическая сверхпроводимость).pdf",
        "site_slugs": ["01_inner_current.pdf", "inner_current.pdf"],
        "emblem": """<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M50 10 L50 90 M25 35 L75 35 M35 65 L65 65"/><circle cx="50" cy="50" r="35"/></svg>"""
    },
    {
        "id": "02",
        "title": "Четверичный фрактал цепи",
        "subtitle": "Архитектурный инвариант природы — от клетки и фонарика до Биткоина и общества",
        "series": "Библиотека «Золотая Семёрка 2.0» — Книга 2 (Стены)",
        "author": "Владимир Аньянов",
        "edition": "First Edition 1.0 (Topological Architecture)",
        "md_source": os.path.join(LIB2_DIR, "02 — Владимир Аньянов — Четверичный фрактал цепи (Архитектурный инвариант природы — от клетки и фонарика до Биткоина и общества).md"),
        "pdf_name_lib": "02 — Владимир Аньянов — Четверичный фрактал цепи (Архитектурный инвариант природы — от клетки и фонарика до Биткоина и общества).pdf",
        "pdf_name_vault": "Книга — Четверичный фрактал цепи (Архитектурный инвариант природы — от клетки и фонарика до Биткоина и общества).pdf",
        "site_slugs": ["02_quaternary_fractal.pdf", "quaternary_fractal.pdf"],
        "emblem": """<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="20" y="20" width="60" height="60" rx="8"/><circle cx="20" cy="20" r="6" fill="currentColor"/><circle cx="80" cy="20" r="6" fill="currentColor"/><circle cx="80" cy="80" r="6" fill="currentColor"/><circle cx="20" cy="80" r="6" fill="currentColor"/><path d="M20 20 L80 20 L80 80 L20 80 Z"/></svg>"""
    },
    {
        "id": "03",
        "title": "Универсальный закон потоковых систем",
        "subtitle": "Термодинамика негэнтропии, открытые системы и КПД бытия",
        "series": "Библиотека «Золотая Семёрка 2.0» — Книга 3 (Крыша)",
        "author": "Владимир Аньянов",
        "edition": "First Edition 1.0 (Cosmological Foundation)",
        "md_source": os.path.join(LIB2_DIR, "03 — Владимир Аньянов — Универсальный закон потоковых систем (Термодинамика негэнтропии, открытые системы и КПД бытия).md"),
        "pdf_name_lib": "03 — Владимир Аньянов — Универсальный закон потоковых систем (Термодинамика негэнтропии, открытые системы и КПД бытия).pdf",
        "pdf_name_vault": "Книга — Универсальный закон потоковых систем (Термодинамика негэнтропии, открытые системы и КПД бытия).pdf",
        "site_slugs": ["03_universal_law.pdf", "universal_law.pdf"],
        "emblem": """<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="50" cy="50" r="42"/><path d="M50 15 L50 85 M15 50 L85 50"/><circle cx="50" cy="50" r="18" fill="currentColor" fill-opacity="0.15"/></svg>"""
    },
    {
        "id": "04",
        "title": "Тайна карманного фонарика",
        "subtitle": "Внутренний ток для детей и подростков — как устроена твоя суперсила",
        "series": "Библиотека «Золотая Семёрка 2.0» — Книга 4 (Детский праймер)",
        "author": "Владимир Аньянов",
        "edition": "Primer Edition 1.0 (Youth Guide)",
        "md_source": os.path.join(LIB2_DIR, "04 — Владимир Аньянов — Тайна карманного фонарика (Внутренний ток для детей и подростков — как устроена твоя суперсила).md"),
        "pdf_name_lib": "04 — Владимир Аньянов — Тайна карманного фонарика (Внутренний ток для детей и подростков — как устроена твоя суперсила).pdf",
        "pdf_name_vault": "Книга-праймер — Тайна карманного фонарика (Внутренний ток для детей — Система Аньянова).pdf",
        "site_slugs": ["04_flashlight_primer.pdf", "primer_flashlight.pdf", "primer.pdf"],
        "emblem": """<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M35 25 L65 25 L60 50 L40 50 Z M40 50 L40 85 L60 85 L60 50"/><circle cx="50" cy="20" r="10" fill="currentColor" fill-opacity="0.2"/></svg>"""
    },
    {
        "id": "05",
        "title": "Полевой мануал оператора",
        "subtitle": "Карманная аптечка первой помощи — 30-секундный протокол соматической отладки",
        "series": "Библиотека «Золотая Семёрка 2.0» — Книга 5 (Аварийный пульт)",
        "author": "Владимир Аньянов",
        "edition": "Operator Field Manual 2.0",
        "md_source": os.path.join(LIB2_DIR, "05 — Владимир Аньянов — Полевой мануал оператора (Карманная аптечка первой помощи — 30-секундный протокол соматической отладки).md"),
        "pdf_name_lib": "05 — Владимир Аньянов — Полевой мануал оператора (Карманная аптечка первой помощи — 30-секундный протокол соматической отладки).pdf",
        "pdf_name_vault": "Книга — Внутренний ток (Полевой мануал отладки).pdf",
        "site_slugs": ["05_field_manual.pdf", "field_manual.pdf"],
        "emblem": """<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="25" y="25" width="50" height="50" rx="10"/><path d="M50 35 L50 65 M35 50 L65 50" stroke-width="4"/></svg>"""
    },
    {
        "id": "06",
        "title": "Укулеле Бытия",
        "subtitle": "Акустическая физика счастливой жизни — материя, звук и резонанс Мусин",
        "series": "Библиотека «Золотая Семёрка 2.0» — Книга 6 (Чувственный монизм)",
        "author": "Владимир Аньянов",
        "edition": "Acoustic Edition 1.0",
        "md_source": os.path.join(LIB2_DIR, "06 — Владимир Аньянов — Укулеле Бытия (Акустическая физика счастливой жизни — материя, звук и резонанс Мусин).md"),
        "pdf_name_lib": "06 — Владимир Аньянов — Укулеле Бытия (Акустическая физика счастливой жизни — материя, звук и резонанс Мусин).pdf",
        "pdf_name_vault": "Книга — Укулеле Бытия (Акустическая физика счастливой жизни).pdf",
        "site_slugs": ["06_ukulele.pdf", "ukulele.pdf"],
        "emblem": """<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2.5"><ellipse cx="50" cy="65" rx="25" ry="22"/><ellipse cx="50" cy="40" rx="18" ry="14"/><circle cx="50" cy="55" r="8" fill="currentColor" fill-opacity="0.2"/><path d="M46 26 L46 10 L54 10 L54 26"/></svg>"""
    },
    {
        "id": "07",
        "title": "Великий Синтез",
        "subtitle": "Революции материи, трагедия духа и электродинамика человека",
        "series": "Библиотека «Золотая Семёрка 2.0» — Книга 7 (Макроистория)",
        "author": "Владимир Аньянов",
        "edition": "Master Edition 2.0 (Post-Universal Flow Law Synthesis)",
        "md_source": os.path.join(LIB2_DIR, "07 — Владимир Аньянов — Великий Синтез (Революции материи, трагедия духа и электродинамика человека).md"),
        "pdf_name_lib": "07 — Владимир Аньянов — Великий Синтез (Революции материи, трагедия духа и электродинамика человека).pdf",
        "pdf_name_vault": "Книга — Великий Синтез (Революции материи, трагедия духа и электродинамика человека).pdf",
        "site_slugs": ["07_great_synthesis.pdf", "great_synthesis.pdf"],
        "emblem": """<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2"><circle cx="50" cy="50" r="44"/><path d="M50 15 L50 85 M15 50 L85 50"/><circle cx="50" cy="50" r="28" stroke-dasharray="3 3"/><circle cx="50" cy="50" r="6" fill="currentColor"/></svg>"""
    },
    {
        "id": "08_copernicus",
        "title": "Коперник Сознания",
        "subtitle": "Анатомия эго и физика внутренней свободы",
        "series": "Библиотека «Внутренний ток» — Специальное издание",
        "author": "Владимир Аньянов",
        "edition": "Master Edition 1.0 (Copernican Revolution)",
        "md_source": os.path.join(VAULT_DIR, "Книга — Коперник Сознания (Анатомия эго и физика внутренней свободы).md"),
        "pdf_name_lib": None,
        "pdf_name_vault": "Книга — Коперник Сознания (Анатомия эго и физика внутренней свободы).pdf",
        "site_slugs": ["copernicus.pdf"],
        "emblem": """<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="50" cy="50" r="14" fill="currentColor"/><circle cx="50" cy="50" r="28" stroke-dasharray="4 4"/><circle cx="50" cy="50" r="42"/><circle cx="80" cy="50" r="5" fill="currentColor"/></svg>"""
    },
    {
        "id": "09_triptych",
        "title": "Триптих Сверхпроводимости",
        "subtitle": "Леванте, Versace и Внутренний ток: Акустико-ольфакторная онтология фазового перехода",
        "series": "Библиотека «Внутренний ток» — Философский триптих",
        "author": "Владимир Аньянов",
        "edition": "Italian Triptych Edition 1.0",
        "md_source": os.path.join(VAULT_DIR, "Книга — Триптих Сверхпроводимости (Леванте и Внутренний ток).md"),
        "pdf_name_lib": None,
        "pdf_name_vault": "Книга — Триптих Сверхпроводимости (Леванте и Внутренний ток).pdf",
        "site_slugs": ["Триптих Сверхпроводимости — Леванте и Внутренний ток.pdf"],
        "emblem": """<svg viewBox="0 0 100 100" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M20 80 L50 20 L80 80 Z"/><circle cx="50" cy="55" r="10" fill="currentColor" fill-opacity="0.2"/></svg>"""
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
    title_html = f'<div class="callout-title" style="font-family: \'Plus Jakarta Sans\', sans-serif; font-size: 8.5pt; font-weight: 700; text-transform: uppercase; letter-spacing: 0.15em; color: #8c8275; margin-bottom: 3mm;">{title}</div>' if title else ""
    return f'<div class="callout callout-{ctype}">{title_html}<div class="callout-body">{body_html}</div></div>'

def build_pdf_for_book(book, browser):
    md_path = book["md_source"]
    if not os.path.exists(md_path):
        print(f"ERROR: File not found: {md_path}")
        return False
    
    print(f"\n=======================================================")
    print(f"Building PDF for: {book['id']} - {book['title']}")
    print(f"Source: {md_path}")
    
    with open(md_path, "r", encoding="utf-8") as f:
        raw_md = f.read()
    
    # Strip frontmatter
    raw_md = re.sub(r"^---.*?---\s*", "", raw_md, flags=re.DOTALL)
    # Strip Obsidian WikiLinks [[target|label]] or [[target\|label]] -> label
    raw_md = re.sub(r"\[\[(?:[^|\]]*\\?\|)?([^\]]+)\]\]", r"\1", raw_md)
    
    # 0. Protect math blocks from Markdown corruption (underscores -> <em>, asterisks, etc.)
    math_stash = []
    def stash_display(m):
        idx = len(math_stash)
        math_stash.append(('display', m.group(1).strip()))
        return f"KATEXDISPLAYMATHPLACEHOLDER{idx}KATEX"

    def stash_inline(m):
        idx = len(math_stash)
        math_stash.append(('inline', m.group(1).strip()))
        return f"KATEXINLINEMATHPLACEHOLDER{idx}KATEX"

    processed_md = re.sub(r"\$\$(.*?)\$\$", stash_display, raw_md, flags=re.DOTALL)
    processed_md = re.sub(r"(?<!\\)\$([^\$\n]+?)(?<!\\)\$", stash_inline, processed_md)

    # Preprocess Callouts
    processed_md = re.sub(r"^>\s*\[!(\w+)\]([^\n]*(?:\n>[^\n]*)*)", replace_callout, processed_md, flags=re.MULTILINE)
    
    # Preprocess Parts and Chapters
    processed_md = re.sub(r"^(# Часть [^\n]+)", r'<div class="part-header">\1</div>', processed_md, flags=re.MULTILINE)
    processed_md = re.sub(r"^(## Часть [^\n]+)", r'<div class="part-header">\1</div>', processed_md, flags=re.MULTILINE)
    processed_md = re.sub(r"^(## Глава [^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
    processed_md = re.sub(r"^(### Глава [^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
    processed_md = re.sub(r"^(# Заключение[^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
    processed_md = re.sub(r"^(## Заключение[^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
    
    # Convert Markdown to HTML
    md_extensions = ['tables', 'fenced_code', 'codehilite', 'def_list', 'nl2br']
    html_body = markdown.markdown(processed_md, extensions=md_extensions)
    
    # Remove initial H1 title and subtitle if matched
    html_body = re.sub(r"<h1>.*?</h1>\s*<h2>.*?</h2>", "", html_body, count=1, flags=re.DOTALL)
    
    # Wrap tables
    html_body = html_body.replace("<table>", '<div class="table-wrapper"><table>')
    html_body = html_body.replace("</table>", '</table></div>')
    
    # Restore math placeholders into clean KaTeX containers
    for i, (mtype, content) in enumerate(math_stash):
        if mtype == 'display':
            placeholder = f"KATEXDISPLAYMATHPLACEHOLDER{i}KATEX"
            replacement = f'<div class="math-display">\\[{content}\\]</div>'
            html_body = re.sub(rf'<p>\s*{re.escape(placeholder)}\s*</p>', lambda m, r=replacement: r, html_body)
            html_body = html_body.replace(placeholder, replacement)
        else:
            placeholder = f"KATEXINLINEMATHPLACEHOLDER{i}KATEX"
            replacement = f'<span class="math-inline">\\({content}\\)</span>'
            html_body = html_body.replace(placeholder, replacement)
    
    title = book["title"]
    subtitle = book["subtitle"]
    series = book["series"]
    author = book["author"]
    edition = book["edition"]
    emblem_svg = book["emblem"]
    
    full_html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>{title} — {author}</title>
{KATEX_SCRIPTS}
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@500;700&family=Lora:ital,wght@0,400;0,500;0,600;1,400;1,500&family=JetBrains+Mono:wght@400;500&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

  @page {{
    size: A4;
    margin: 22mm 18mm 22mm 18mm;
  }}

  * {{
    box-sizing: border-box;
  }}

  body {{
    font-family: 'Lora', 'Georgia', serif;
    font-size: 10.8pt;
    line-height: 1.68;
    color: #24292f;
    background-color: #ffffff;
    margin: 0;
    padding: 0;
    text-rendering: optimizeLegibility;
    -webkit-font-smoothing: antialiased;
  }}

  /* COVER PAGE */
  .cover-page {{
    page-break-after: always;
    height: 100vh;
    min-height: 250mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    text-align: center;
    padding: 28mm 15mm 20mm 15mm;
    background: radial-gradient(circle at 50% 30%, #ffffff 0%, #faf8f5 100%);
    border: 1px solid #eae5df;
    position: relative;
  }}

  .cover-series {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 8.5pt;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #8c8275;
    font-weight: 600;
  }}

  .cover-hero {{
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 12mm;
  }}

  .cover-emblem {{
    width: 68px;
    height: 68px;
    margin-bottom: 8mm;
    color: #bfa15f;
  }}

  .cover-author {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 13pt;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #4a453e;
    font-weight: 500;
    margin-bottom: 6mm;
  }}

  .cover-title {{
    font-family: 'Cinzel', 'Lora', serif;
    font-size: 26pt;
    font-weight: 700;
    line-height: 1.18;
    color: #1a1816;
    letter-spacing: 0.03em;
    margin: 0 0 5mm 0;
  }}

  .cover-divider {{
    width: 60px;
    height: 2px;
    background: #bfa15f;
    margin: 4mm 0 6mm 0;
  }}

  .cover-subtitle {{
    font-family: 'Lora', serif;
    font-size: 12.5pt;
    font-style: italic;
    color: #615a51;
    max-width: 540px;
    line-height: 1.5;
    margin: 0 auto;
  }}

  .cover-footer {{
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 3mm;
  }}

  .cover-edition {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 8.5pt;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #8c8275;
    font-weight: 600;
  }}

  .cover-year {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 8.5pt;
    color: #a8a196;
    letter-spacing: 0.08em;
  }}

  /* PART & CHAPTER HEADERS */
  .part-header {{
    page-break-before: always;
    margin-top: 25mm;
    margin-bottom: 15mm;
    text-align: center;
  }}

  .part-header h1, .part-header h2 {{
    font-family: 'Cinzel', serif;
    font-size: 20pt;
    font-weight: 700;
    color: #8b6e32;
    letter-spacing: 0.08em;
    border-bottom: 2px solid #e5ded5;
    padding-bottom: 6mm;
    margin: 0;
  }}

  .chapter-break {{
    page-break-before: always;
    height: 0;
  }}

  h1, h2, h3, h4 {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #1a1816;
    font-weight: 600;
    break-after: avoid;
  }}

  h1 {{
    font-size: 18pt;
    margin-top: 10mm;
    margin-bottom: 4mm;
    letter-spacing: -0.01em;
  }}

  h2 {{
    font-size: 14pt;
    margin-top: 8mm;
    margin-bottom: 3.5mm;
    color: #2b2723;
    border-bottom: 1px solid #f0ebe4;
    padding-bottom: 2mm;
  }}

  h3 {{
    font-size: 11.5pt;
    font-weight: 700;
    margin-top: 6mm;
    margin-bottom: 2mm;
    color: #4a453e;
  }}

  p {{
    margin-top: 0;
    margin-bottom: 3.5mm;
    text-align: justify;
    hyphens: auto;
  }}

  strong {{
    font-weight: 600;
    color: #1a1816;
  }}

  em {{
    font-style: italic;
  }}

  hr {{
    border: 0;
    height: 1px;
    background: #e5ded5;
    margin: 8mm 0;
  }}

  /* CALLOUTS */
  .callout {{
    margin: 5mm 0;
    padding: 4mm 5mm;
    border-left: 3px solid #bfa15f;
    background-color: #faf8f5;
    border-radius: 0 4px 4px 0;
    font-size: 10.2pt;
    break-inside: avoid;
  }}

  .callout-quote {{
    border-left-color: #bfa15f;
    background-color: #fcfbf9;
    font-style: normal;
  }}

  .callout-important, .callout-warning {{
    border-left-color: #c95d3b;
    background-color: #fff9f7;
  }}

  .callout-info, .callout-tip {{
    border-left-color: #4a7c8c;
    background-color: #f5f9fa;
  }}

  /* ASCII / CODE BLOCKS */
  pre {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.8pt;
    line-height: 1.35;
    background: #1e1e1e;
    color: #e6e6e6;
    padding: 3.5mm 4mm;
    border-radius: 4px;
    overflow-x: auto;
    margin: 4mm 0;
    break-inside: avoid;
    white-space: pre;
  }}

  code {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.8pt;
    background: #f4f0ea;
    color: #7a3e26;
    padding: 1px 4px;
    border-radius: 3px;
  }}

  pre code {{
    background: transparent;
    color: inherit;
    padding: 0;
  }}

  /* TABLES */
  .table-wrapper {{
    margin: 5mm 0;
    overflow-x: auto;
    break-inside: avoid;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 9pt;
    line-height: 1.45;
  }}

  th, td {{
    padding: 2.5mm 3.5mm;
    border: 1px solid #e0d9cf;
    text-align: left;
  }}

  th {{
    background-color: #f7f4ee;
    font-weight: 600;
    color: #38332c;
  }}

  tr:nth-child(even) td {{
    background-color: #faf8f5;
  }}

  /* MATH DISPLAY */
  .math-display {{
    font-family: 'Lora', 'Georgia', serif;
    font-style: italic;
    text-align: center;
    margin: 4mm 0;
    padding: 2.5mm 0;
    background: #faf8f5;
    border-radius: 4px;
    font-size: 11pt;
    break-inside: avoid;
    color: #1a1816;
  }}

  .math-inline {{
    font-family: 'Lora', 'Georgia', serif;
    font-style: italic;
  }}

  ul, ol {{
    margin-top: 0;
    margin-bottom: 3.5mm;
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
  <div class="cover-series">{series}</div>
  <div class="cover-hero">
    <div class="cover-emblem">{emblem_svg}</div>
    <div class="cover-author">{author}</div>
    <div class="cover-title">{title}</div>
    <div class="cover-divider"></div>
    <div class="cover-subtitle">{subtitle}</div>
  </div>
  <div class="cover-footer">
    <div class="cover-edition">{edition}</div>
    <div class="cover-year">2026 • Библиотека «Внутренний ток»</div>
  </div>
</div>

<!-- BODY CONTENT -->
<div class="book-body">
{html_body}
</div>

</body>
</html>"""

    html_temp_path = os.path.join(LOCAL_BUILD_DIR, f"temp_{book['id']}.html")
    with open(html_temp_path, "w", encoding="utf-8") as f:
        f.write(full_html)
    
    local_pdf_path = os.path.join(LOCAL_BUILD_DIR, f"{book['id']}_output.pdf")
    
    page = browser.new_page()
    page.goto("file:///" + html_temp_path.replace("\\", "/"), wait_until="networkidle")
    page.wait_for_function("() => window.katexDone === true")
    page.wait_for_timeout(800)
    
    header_template = f"""
    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 7.5pt; color: #8c8275; width: 100%; display: flex; justify-content: space-between; padding: 0 18mm; border-bottom: 0.5px solid #eae5df; padding-bottom: 2mm;">
      <span>{author} • {title}</span>
      <span>{edition}</span>
    </div>
    """
    
    footer_template = """
    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 8.5pt; color: #827b72; width: 100%; display: flex; justify-content: center; padding: 0 18mm;">
      <span class="pageNumber"></span>
    </div>
    """
    
    page.pdf(
        path=local_pdf_path,
        format="A4",
        print_background=True,
        display_header_footer=True,
        header_template=header_template,
        footer_template=footer_template,
        margin={"top": "20mm", "bottom": "20mm", "left": "18mm", "right": "18mm"}
    )
    page.close()
    
    reader = pypdf.PdfReader(local_pdf_path)
    pages = len(reader.pages)
    size_kb = os.path.getsize(local_pdf_path) / 1024
    print(f"SUCCESS: Generated {book['title']} ({pages} pages, {size_kb:.1f} KB)")
    
    # Copy to Vault if defined
    if book.get("pdf_name_vault"):
        target_vault = os.path.join(VAULT_DIR, book["pdf_name_vault"])
        shutil.copyfile(local_pdf_path, target_vault)
        print(f"-> Copied to Obsidian Vault: {book['pdf_name_vault']}")
    
    # Copy to Golden Seven 2.0 if defined
    if book.get("pdf_name_lib"):
        target_lib = os.path.join(LIB2_DIR, book["pdf_name_lib"])
        shutil.copyfile(local_pdf_path, target_lib)
        print(f"-> Copied to Golden Seven 2.0: {book['pdf_name_lib']}")

    # Copy to dist_site and public books
    for dest_dir in [DIST_DIR, PUB_DIR]:
        os.makedirs(dest_dir, exist_ok=True)
        if book.get("pdf_name_lib"):
            shutil.copyfile(local_pdf_path, os.path.join(dest_dir, book["pdf_name_lib"]))
        for slug in book.get("site_slugs", []):
            shutil.copyfile(local_pdf_path, os.path.join(dest_dir, slug))
    print(f"-> Copied to dist_site & public: {book.get('site_slugs', [])}")
        
    return True

def main():
    target_ids = sys.argv[1:]
    to_build = BOOKS
    if target_ids:
        to_build = [b for b in BOOKS if b["id"] in target_ids]
        print(f"Targeting specific books: {target_ids}")
    else:
        print("Starting master PDF compilation for ALL books...")
        
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for b in to_build:
            build_pdf_for_book(b, browser)
        browser.close()
    print("\nTARGET BOOKS SUCCESSFULLY COMPILED INTO PDF!")

if __name__ == "__main__":
    main()
