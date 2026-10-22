import os
import re
import shutil
import sys
import markdown
from playwright.sync_api import sync_playwright
import pypdf

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current"
VAULT_DIR = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki"
IC_LIB_DIR = os.path.join(ROOT_DIR, "IC Library")
DIST_BOOKS_DIR = os.path.join(ROOT_DIR, "dist_site", "books")
PUB_BOOKS_DIR = os.path.join(ROOT_DIR, "public", "books")

KATEX_CSS = os.path.abspath(os.path.join(ROOT_DIR, "node_modules", "katex", "dist", "katex.min.css")).replace("\\", "/")
KATEX_JS = os.path.abspath(os.path.join(ROOT_DIR, "node_modules", "katex", "dist", "katex.min.js")).replace("\\", "/")
KATEX_AUTO = os.path.abspath(os.path.join(ROOT_DIR, "node_modules", "katex", "dist", "contrib", "auto-render.min.js")).replace("\\", "/")

def replace_callout(match):
    ctype = match.group(1).lower()
    content = match.group(2)
    lines = [re.sub(r"^>\s?", "", line) for line in content.strip().split("\n")]
    title = lines[0].strip() if lines else ""
    body_lines = lines[1:] if len(lines) > 1 else []
    body_text = "\n".join(body_lines).strip()
    
    # Ensure blank lines before lists inside callouts
    body_text = re.sub(r"([^\n])\n([ \t]*[\*\-][ \t]+)", r"\1\n\n\2", body_text)
    body_text = re.sub(r"([^\n])\n([ \t]*\d+\.[ \t]+)", r"\1\n\n\2", body_text)
    
    body_html = markdown.markdown(body_text, extensions=['tables', 'fenced_code', 'codehilite', 'def_list'])
    
    icon = "⚡"
    if "quote" in ctype: icon = "📜"
    elif "important" in ctype or "warning" in ctype: icon = "⚠️"
    elif "tip" in ctype: icon = "💡"
    elif "info" in ctype: icon = "ℹ️"
    
    title_html = f'<div class="callout-title"><span>{icon}</span> <span>{title}</span></div>' if title else ""
    return f'<div class="callout callout-{ctype}">{title_html}<div class="callout-body">{body_html}</div></div>'

def build_pdf_from_md(md_path, html_title, brochure_badge, brochure_h1, brochure_sub, author_meta, out_pdf_name, lang="ru", web_pdf_name="manifesto.pdf"):
    print(f"\n=======================================================")
    print(f"Building PDF for: {out_pdf_name}")
    print(f"Source MD: {md_path}")
    print(f"=======================================================")

    with open(md_path, "r", encoding="utf-8") as f:
        raw_md = f.read()

    # Strip YAML frontmatter
    raw_md = re.sub(r"^---.*?---\s*", "", raw_md, flags=re.DOTALL)

    # Strip redundant leading Markdown titles if present (already rendered by brochure header)
    raw_md = re.sub(r"^\s*#\s+[^\n]+\n+", "", raw_md)
    raw_md = re.sub(r"^\s*###?\s+[^\n]+\n+", "", raw_md)
    raw_md = re.sub(r"^\s*---\s*\n+", "", raw_md)

    # Ensure blank line before bullet lists and numbered lists so markdown parses them properly
    raw_md = re.sub(r"([^\n])\n([ \t]*[\*\-][ \t]+)", r"\1\n\n\2", raw_md)
    raw_md = re.sub(r"([^\n])\n([ \t]*\d+\.[ \t]+)", r"\1\n\n\2", raw_md)

    # Process Callouts
    processed_md = re.sub(r"^>\s*\[!(\w+)\]([^\n]*(?:\n>[^\n]*)*)", replace_callout, raw_md, flags=re.MULTILINE)

    # Preprocess Headers to inject page-break classes
    # Break before Schema, Parts, Practical algorithm, and Summary Axioms
    processed_md = re.sub(r"^(## 📐 [^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
    processed_md = re.sub(r"^(## (?:Часть|Part|Parte) [^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
    processed_md = re.sub(r"^(## (?:Часть III|Part III|Parte III) [^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
    processed_md = re.sub(r"^(## (?:Часть V|Part V|Parte V) [^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
    processed_md = re.sub(r"^(## (?:Часть VII|Part VII|Parte VII) [^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
    processed_md = re.sub(r"^(## ⚡ [^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)

    # Convert Markdown to HTML (WITHOUT nl2br so lists and paragraphs parse canonically)
    md_extensions = ['tables', 'fenced_code', 'codehilite', 'def_list']
    html_body = markdown.markdown(processed_md, extensions=md_extensions)

    # Wrap tables
    html_body = html_body.replace("<table>", '<div class="table-wrapper"><table>')
    html_body = html_body.replace("</table>", '</table></div>')

    # Wrap display math in container for centering and convert to \[...\]
    html_body = re.sub(r"\$\$(.*?)\$\$", r'<div class="math-display">\\[\1\\]</div>', html_body, flags=re.DOTALL)
    html_body = re.sub(r"\$([^\$\n]+?)\$", r'<span class="math-inline">\\(\1\\)</span>', html_body)

    # HTML document
    full_html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<title>{html_title}</title>
<link rel="stylesheet" href="file:///{KATEX_CSS}">
<script src="file:///{KATEX_JS}"></script>
<script src="file:///{KATEX_AUTO}"></script>
<script>
  window.addEventListener('DOMContentLoaded', () => {{
    if (typeof renderMathInElement !== 'undefined') {{
      renderMathInElement(document.body, {{
        delimiters: [
          {{left: '\\\\[', right: '\\\\]', display: true}},
          {{left: '\\\\(', right: '\\\\)', display: false}},
          {{left: '$$', right: '$$', display: true}},
          {{left: '$', right: '$', display: false}}
        ],
        throwOnError: false
      }});
    }}
    window.katexDone = true;
  }});
</script>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Lora:ital,wght@0,400;0,500;0,600;1,400;1,500&family=JetBrains+Mono:wght@400;500;600&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

  @page {{
    size: A4;
    margin: 20mm 18mm 20mm 18mm;
    @bottom-center {{
      content: counter(page);
      font-family: 'JetBrains Mono', monospace;
      font-size: 8.5pt;
      color: #94a3b8;
    }}
  }}

  * {{
    box-sizing: border-box;
  }}

  body {{
    font-family: 'Lora', Georgia, serif;
    font-size: 10pt;
    line-height: 1.65;
    color: #1e293b;
    background: #ffffff;
    margin: 0;
    padding: 0;
  }}

  h1, h2, h3, h4 {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #0f172a;
    line-height: 1.3;
  }}

  h1 {{
    font-family: 'Cinzel', serif;
    font-size: 24pt;
    font-weight: 800;
    text-align: center;
    color: #0f172a;
    margin-top: 15pt;
    margin-bottom: 8pt;
    letter-spacing: 0.02em;
  }}

  .brochure-badge {{
    text-align: center;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 8pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: #d97706;
    margin-bottom: 8pt;
  }}

  .brochure-meta {{
    text-align: center;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 9pt;
    color: #64748b;
    margin-bottom: 22pt;
    border-bottom: 1.5pt solid #e2e8f0;
    padding-bottom: 12pt;
  }}

  h2 {{
    font-size: 14pt;
    margin-top: 18pt;
    margin-bottom: 8pt;
    border-bottom: 1pt solid #e2e8f0;
    padding-bottom: 4pt;
    color: #0f172a;
  }}

  h3 {{
    font-size: 11pt;
    margin-top: 14pt;
    margin-bottom: 6pt;
    color: #b45309;
  }}

  h4 {{
    font-size: 10pt;
    margin-top: 10pt;
    margin-bottom: 4pt;
    color: #334155;
  }}

  p {{
    margin-top: 0;
    margin-bottom: 8pt;
    text-align: left;
    line-height: 1.65;
  }}

  strong {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 700;
    color: #0f172a;
  }}

  code {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5pt;
    background: #f1f5f9;
    padding: 1pt 3pt;
    border-radius: 3pt;
    color: #0f172a;
  }}

  pre {{
    background: #090d16;
    color: #f8fafc;
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.2pt;
    line-height: 1.35;
    padding: 10pt 12pt;
    border-radius: 6pt;
    border: 1pt solid #1e293b;
    overflow-x: auto;
    margin: 12pt 0;
    white-space: pre;
  }}

  pre code {{
    background: transparent;
    color: #f8fafc;
    padding: 0;
    font-size: inherit;
  }}

  .callout {{
    margin: 12pt 0;
    padding: 10pt 14pt;
    border-radius: 6pt;
    border-left: 3.5pt solid #d97706;
    background: #fffbeb;
  }}

  .callout-title {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 8.5pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #b45309;
    margin-bottom: 4pt;
    display: flex;
    align-items: center;
    gap: 6px;
  }}

  .callout-body p {{
    margin-bottom: 4pt;
    font-size: 9.5pt;
    line-height: 1.6;
  }}

  .callout-body p:last-child {{
    margin-bottom: 0;
  }}

  .chapter-break {{
    page-break-before: always;
  }}

  .table-wrapper {{
    margin: 12pt 0;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 9pt;
  }}

  th, td {{
    padding: 6pt 8pt;
    border-bottom: 1pt solid #e2e8f0;
    text-align: left;
  }}

  th {{
    background: #f8fafc;
    color: #0f172a;
    font-weight: 700;
  }}

  .math-display {{
    text-align: center;
    margin: 12pt 0;
  }}

  .katex {{
    font-size: 1.05em !important;
  }}

  .katex-display {{
    margin: 8pt 0 !important;
    text-align: center;
  }}

  ul, ol {{
    margin-top: 4pt;
    margin-bottom: 10pt;
    padding-left: 20pt;
  }}

  li {{
    margin-bottom: 4pt;
    line-height: 1.6;
    text-align: left;
  }}

  hr {{
    border: none;
    border-top: 1pt solid #e2e8f0;
    margin: 16pt 0;
  }}
</style>
</head>
<body>

  <div class="brochure-badge">{brochure_badge}</div>
  <h1>{brochure_h1}</h1>
  <div style="text-align:center; font-family:'Lora',serif; font-size:11.5pt; font-style:italic; color:#475569; margin-bottom:10pt; line-height: 1.4;">
    {brochure_sub}
  </div>
  <div class="brochure-meta">
    {author_meta}
  </div>

  {html_body}

</body>
</html>
"""

    temp_html_path = os.path.join(ROOT_DIR, f"temp_{out_pdf_name}.html")
    with open(temp_html_path, "w", encoding="utf-8") as f:
        f.write(full_html)

    target_pdf_library = os.path.join(IC_LIB_DIR, out_pdf_name)
    target_pdf_vault = os.path.join(VAULT_DIR, out_pdf_name)
    target_pdf_dist = os.path.join(DIST_BOOKS_DIR, web_pdf_name)
    target_pdf_pub = os.path.join(PUB_BOOKS_DIR, web_pdf_name)

    print("Rendering PDF via Playwright with local KaTeX engine...")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file:///{os.path.abspath(temp_html_path).replace(os.sep, '/')}", wait_until="networkidle")
        page.wait_for_function("() => window.katexDone === true")
        page.wait_for_timeout(500)
        
        # Verify KaTeX rendered count
        katex_count = page.evaluate("() => document.querySelectorAll('.katex').length")
        print(f"Verified KaTeX rendered formulas: {katex_count}")

        page.pdf(
            path=target_pdf_library,
            format="A4",
            print_background=True,
            margin={"top": "20mm", "bottom": "20mm", "left": "18mm", "right": "18mm"}
        )
        browser.close()

    # Clean up temp HTML
    if os.path.exists(temp_html_path):
        os.remove(temp_html_path)

    reader = pypdf.PdfReader(target_pdf_library)
    pages_count = len(reader.pages)
    print(f"Generated: {target_pdf_library} ({pages_count} pages, {os.path.getsize(target_pdf_library):,} bytes)")

    # Sync to Vault
    shutil.copy2(target_pdf_library, target_pdf_vault)
    print(f"Synced to Vault: {target_pdf_vault}")

    # Sync to dist_site and public
    shutil.copy2(target_pdf_library, target_pdf_dist)
    shutil.copy2(target_pdf_library, target_pdf_pub)
    print(f"Synced to web dist: {target_pdf_dist}")

    return target_pdf_library, pages_count

def main():
    os.makedirs(IC_LIB_DIR, exist_ok=True)
    os.makedirs(DIST_BOOKS_DIR, exist_ok=True)
    os.makedirs(PUB_BOOKS_DIR, exist_ok=True)

    # 1. Russian Manifesto PDF
    ru_md = os.path.join(VAULT_DIR, "Брошюра — Манифест Внутреннего Тока (Электродинамика сознания).md")
    build_pdf_from_md(
        md_path=ru_md,
        html_title="Манифест Внутреннего Тока — Владимир Аньянов",
        brochure_badge="Библиотека «Внутренний ток» • Манифест Суверенного Человека • Специальный выпуск",
        brochure_h1="Манифест Внутреннего Тока",
        brochure_sub="Электродинамика сознания: почему мы выгораем, как устроен человек на самом деле и почему в лампочке нет батарейки",
        author_meta="Автор: <strong>Владимир Аньянов</strong> • Мастер-манифест и схема Дзен-Фонарика • innercurrent.ru",
        out_pdf_name="Брошюра — Манифест Внутреннего Тока (Электродинамика сознания).pdf",
        lang="ru",
        web_pdf_name="manifesto.pdf"
    )

    # 2. English Manifesto PDF
    en_md = os.path.join(VAULT_DIR, "Brochure — The Inner Current Manifesto (Consciousness Electrodynamics).md")
    if os.path.exists(en_md):
        build_pdf_from_md(
            md_path=en_md,
            html_title="The Inner Current Manifesto — Vladimir Anyanov",
            brochure_badge="Inner Current Library • Sovereign Circuit Manifesto • Special Edition",
            brochure_h1="The Inner Current Manifesto",
            brochure_sub="Consciousness Electrodynamics: Why We Burn Out, How Human Beings Are Actually Wired, and Why There Is No Battery Inside the Lightbulb",
            author_meta="Author: <strong>Vladimir Anyanov</strong> • Master Manifesto & Zen Flashlight Circuit • innercurrent.ru/en",
            out_pdf_name="The Inner Current Manifesto — Vladimir Anyanov.pdf",
            lang="en",
            web_pdf_name="manifesto_en.pdf"
        )
        # Also copy with canonical brochure name in IC Library & Vault
        en_lib_brochure = os.path.join(IC_LIB_DIR, "Brochure — The Inner Current Manifesto (Consciousness Electrodynamics).pdf")
        shutil.copy2(os.path.join(IC_LIB_DIR, "The Inner Current Manifesto — Vladimir Anyanov.pdf"), en_lib_brochure)
        en_vault_brochure = os.path.join(VAULT_DIR, "Brochure — The Inner Current Manifesto (Consciousness Electrodynamics).pdf")
        shutil.copy2(os.path.join(IC_LIB_DIR, "The Inner Current Manifesto — Vladimir Anyanov.pdf"), en_vault_brochure)
        print(f"Also created canonical brochure alias: {en_lib_brochure}")

    # 3. Italian Manifesto PDF
    it_md = os.path.join(VAULT_DIR, "Brochure — Il Manifesto della Corrente Interiore (Elettrodinamica della coscienza).md")
    if os.path.exists(it_md):
        build_pdf_from_md(
            md_path=it_md,
            html_title="Il Manifesto della Corrente Interiore — Vladimir Anyanov",
            brochure_badge="Biblioteca «La Corrente Interiore» • Manifesto dell'Essere Umano Sovrano • Edizione Speciale",
            brochure_h1="Il Manifesto della Corrente Interiore",
            brochure_sub="Elettrodinamica della coscienza: perché ci bruciamo nel burnout, come è fatto veramente l'essere umano e perché nella lampadina non c'è alcuna batteria",
            author_meta="Autore: <strong>Vladimir Anyanov</strong> • Manifesto Maestro e Schema della Torcia Zen • innercurrent.ru",
            out_pdf_name="Il Manifesto della Corrente Interiore — Vladimir Anyanov.pdf",
            lang="it",
            web_pdf_name="manifesto_it.pdf"
        )
        # Also copy with canonical brochure name in IC Library & Vault
        it_lib_brochure = os.path.join(IC_LIB_DIR, "Brochure — Il Manifesto della Corrente Interiore (Elettrodinamica della coscienza).pdf")
        shutil.copy2(os.path.join(IC_LIB_DIR, "Il Manifesto della Corrente Interiore — Vladimir Anyanov.pdf"), it_lib_brochure)
        it_vault_brochure = os.path.join(VAULT_DIR, "Brochure — Il Manifesto della Corrente Interiore (Elettrodinamica della coscienza).pdf")
        shutil.copy2(os.path.join(IC_LIB_DIR, "Il Manifesto della Corrente Interiore — Vladimir Anyanov.pdf"), it_vault_brochure)
        print(f"Also created canonical Italian brochure alias: {it_lib_brochure}")

if __name__ == "__main__":
    main()
