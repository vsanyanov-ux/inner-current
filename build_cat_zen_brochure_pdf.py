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
    "md_path": r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Брошюра — Кошачий дзэн и сверхпроводимость (Хайку, мурлыкание и ток).md",
    "output_html": r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\cat_zen_brochure.html",
    "output_pdf": r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\IC Library\Брошюра — Кошачий дзэн и сверхпроводимость (Хайку, мурлыкание и ток).pdf",
    "vault_pdf": r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Брошюра — Кошачий дзэн и сверхпроводимость (Хайку, мурлыкание и ток).pdf",
    "series": "Inner Current • Электродинамика Состояния • Манифест",
    "title": "КОШАЧИЙ ДЗЭН И<br>СВЕРХПРОВОДИМОСТЬ",
    "subtitle": "Хайку, мурлыкание и ток: почему внутренний ток не сухой механизм, а физика чувственного экстаза, и как кошачий сон раскрывает тайну Тандэна",
    "header_title": "Владимир Аньянов • Кошачий дзэн и сверхпроводимость",
    "quote": "«Самая большая ошибка ума — вообразить, что электродинамика Внутреннего тока суха, механистична и бесчувственна. Схемотехника и закон Ома нужны нам не для того, чтобы превратить человека в бесстрастный кремниевый процессор, а для того, чтобы убрать паразитный омический шум и защитить тончайшую струну чувственности от выгорания. Внутренний ток — это не холодный монастырский изолятор; это предельная жажда и сочность жизни, способность до слез чувствовать музыку, поэзию, аромат мокрой хвои и утренний рассвет. Кот, растянувшийся на залитом солнцем полу, не читал ни одной сутры, но его сопротивление строго равно нулю, а мурлыкание на частоте 25–50 Гц — это чистый резонанс живого проводника с космическим полем».",
    "gradient": "linear-gradient(145deg, #0b132b 0%, #1c2541 50%, #0a0e1a 100%)",
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
    processed_md = re.sub(r"^(## ⚡ Экспресс-протокол[^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
    processed_md = re.sub(r"^(## 📜 Резюме[^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)

    # Convert Markdown to HTML
    md_extensions = ['tables', 'fenced_code', 'codehilite', 'def_list', 'nl2br']
    html_body = markdown.markdown(processed_md, extensions=md_extensions)

    full_html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>{b_info['header_title']}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400;1,600&family=JetBrains+Mono:wght@400;500;600&family=Lora:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
  <style>
    @page {{
      size: A4;
      margin: 0;
    }}
    *, *::before, *::after {{
      box-sizing: border-box;
    }}
    body {{
      margin: 0;
      padding: 0;
      font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
      font-size: 10pt;
      line-height: 1.65;
      color: #1e293b;
      background-color: #ffffff;
      -webkit-font-smoothing: antialiased;
    }}
    .cover-page {{
      width: 210mm;
      height: 297mm;
      page-break-after: always;
      background: {b_info['gradient']};
      color: #ffffff;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 26mm 22mm;
      position: relative;
      overflow: hidden;
    }}
    .cover-top {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid rgba(255, 255, 255, 0.15);
      padding-bottom: 8mm;
    }}
    .cover-series {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 8.5pt;
      letter-spacing: 0.22em;
      text-transform: uppercase;
      color: {b_info['accent']};
      font-weight: 600;
    }}
    .cover-badge {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 8pt;
      padding: 3px 10px;
      border-radius: 9999px;
      background: rgba(245, 158, 11, 0.15);
      border: 1px solid rgba(245, 158, 11, 0.35);
      color: {b_info['accent']};
      font-weight: 600;
    }}
    .cover-center {{
      margin-top: auto;
      margin-bottom: auto;
    }}
    .cover-icon {{
      width: 56px;
      height: 56px;
      margin-bottom: 8mm;
      filter: drop-shadow(0 0 16px rgba(245, 158, 11, 0.5));
    }}
    .cover-author {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 13pt;
      font-weight: 600;
      color: #94a3b8;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      margin-bottom: 6mm;
    }}
    .cover-title {{
      font-family: 'Cinzel', serif;
      font-size: 32pt;
      font-weight: 800;
      line-height: 1.1;
      letter-spacing: -0.02em;
      color: #ffffff;
      margin-bottom: 7mm;
      text-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }}
    .cover-subtitle {{
      font-family: 'Lora', serif;
      font-style: italic;
      font-size: 13pt;
      line-height: 1.5;
      color: #cbd5e1;
      max-width: 155mm;
    }}
    .cover-footer {{
      border-top: 1px solid rgba(255, 255, 255, 0.15);
      padding-top: 8mm;
      display: flex;
      justify-content: space-between;
      font-family: 'JetBrains Mono', monospace;
      font-size: 8pt;
      color: #64748b;
      letter-spacing: 0.05em;
    }}
    .frontispiece {{
      width: 210mm;
      height: 297mm;
      page-break-after: always;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding: 35mm 28mm;
      background: #fafaf9;
      text-align: center;
    }}
    .frontispiece-quote {{
      font-family: 'Lora', serif;
      font-size: 13pt;
      line-height: 1.8;
      color: #334155;
      font-style: italic;
      max-width: 145mm;
      margin-bottom: 12mm;
      position: relative;
    }}
    .frontispiece-author {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 10pt;
      font-weight: 700;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      color: #0f172a;
    }}
    .main-content {{
      padding: 22mm 20mm;
    }}
    h1 {{
      font-family: 'Cinzel', serif;
      font-size: 21pt;
      font-weight: 800;
      color: #0f172a;
      line-height: 1.25;
      margin-top: 0;
      margin-bottom: 4mm;
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 4mm;
    }}
    h2 {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 13.5pt;
      font-weight: 700;
      color: #0f172a;
      margin-top: 8mm;
      margin-bottom: 4mm;
      letter-spacing: -0.01em;
    }}
    h3 {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-size: 11pt;
      font-weight: 700;
      color: #1e293b;
      margin-top: 6mm;
      margin-bottom: 2.5mm;
    }}
    p {{
      margin-top: 0;
      margin-bottom: 3.5mm;
      text-align: justify;
    }}
    pre {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 7.2pt;
      line-height: 1.35;
      background: #0f172a;
      color: #e2e8f0;
      padding: 5mm;
      border-radius: 3mm;
      overflow-x: auto;
      margin: 5mm 0;
      border: 1px solid #334155;
    }}
    code {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 8.5pt;
      background: #f1f5f9;
      color: #0f172a;
      padding: 1px 4px;
      border-radius: 2px;
    }}
    pre code {{
      background: transparent;
      color: inherit;
      padding: 0;
    }}
    .callout {{
      border-left: 4px solid #f59e0b;
      background: #fffbeb;
      padding: 4mm 5mm;
      border-radius: 0 3mm 3mm 0;
      margin: 5mm 0;
    }}
    .callout-quote {{
      border-left-color: #f59e0b;
      background: #fefce8;
    }}
    .callout-title {{
      font-family: 'Plus Jakarta Sans', sans-serif;
      font-weight: 700;
      font-size: 10pt;
      color: #78350f;
      margin-bottom: 2mm;
    }}
    .callout-body {{
      font-size: 9.5pt;
      color: #451a03;
    }}
    blockquote {{
      border-left: 3px solid #cbd5e1;
      margin: 4mm 0;
      padding-left: 5mm;
      color: #475569;
      font-style: italic;
    }}
    ul, ol {{
      margin-top: 0;
      margin-bottom: 4mm;
      padding-left: 6mm;
    }}
    li {{
      margin-bottom: 2mm;
    }}
    .chapter-break {{
      page-break-before: always;
    }}
    hr {{
      border: none;
      border-top: 1px solid #e2e8f0;
      margin: 6mm 0;
    }}
  </style>
</head>
<body>

<!-- COVER -->
<div class="cover-page">
  <div class="cover-top">
    <div class="cover-series">{b_info['series']}</div>
    <div class="cover-badge">⚡ Master Brochure</div>
  </div>
  <div class="cover-center">
    <svg class="cover-icon" viewBox="0 0 24 24" fill="none" stroke="{b_info['accent']}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
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

    # Copy to Obsidian Vault for immediate access
    shutil.copy2(b_info["output_pdf"], b_info["vault_pdf"])

    reader = pypdf.PdfReader(b_info["output_pdf"])
    print(f"SUCCESS: Generated PDF {b_info['output_pdf']}! Total Pages: {len(reader.pages)}, Size: {os.path.getsize(b_info['output_pdf']) / 1024:.1f} KB")

if __name__ == "__main__":
    build_pdf()
