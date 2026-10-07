import os
import re
import shutil
import markdown
from playwright.sync_api import sync_playwright
import pypdf

VAULT_MD = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\懐中電灯の原理 (ひきこもり脱出のための意識回路設計と身体的アプローチ).md"
OUTPUT_HTML = r"C:\Users\vanya\Antigravity Projects\Apps\Inner Current\japanese_hikikomori_pamphlet.html"
OUTPUT_PDF = r"C:\Users\vanya\Antigravity Projects\Apps\Inner Current\IC Library\懐中電灯の原理 — ひきこもり脱出の回路設計 (Vladimir Anyanov).pdf"
VAULT_PDF = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\懐中電灯の原理 — ひきこもり脱出の回路設計 (Vladimir Anyanov).pdf"

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

# Preprocess Chapters to inject page-break classes
processed_md = re.sub(r"^(## 第[^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
processed_md = re.sub(r"^(## 7つの原則[^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)

# Convert Markdown to HTML
md_extensions = ['tables', 'fenced_code', 'codehilite', 'def_list', 'nl2br']
html_body = markdown.markdown(processed_md, extensions=md_extensions)

# Wrap tables in responsive containers
html_body = html_body.replace("<table>", '<div class="table-wrapper"><table>')
html_body = html_body.replace("</table>", '</table></div>')

FULL_HTML = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<title>懐中電灯の原理 — ウラジーミル・アニャノフ</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js" onload="renderMathInElement(document.body, {{delimiters: [{{left: '$$', right: '$$', display: true}}, {{left: '$', right: '$', display: false}}]}});"></script>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Noto+Serif+JP:wght@400;600;700&family=Noto+Sans+JP:wght@300;400;500;700&family=JetBrains+Mono:wght@400;500&family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');

  @page {{
    size: A4;
    margin: 20mm 18mm 20mm 18mm;
  }}

  * {{
    box-sizing: border-box;
  }}

  body {{
    font-family: 'Noto Sans JP', 'Noto Serif JP', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 10pt;
    line-height: 1.75;
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
    border: 1px solid #cbd5e1;
    background: linear-gradient(150deg, #f8fafc 0%, #f1f5f9 45%, #e2e8f0 100%);
    position: relative;
    box-sizing: border-box;
  }}

  .cover-series {{
    font-family: 'Plus Jakarta Sans', 'Noto Sans JP', sans-serif;
    font-size: 8.5pt;
    font-weight: 700;
    letter-spacing: 0.2em;
    color: #0369a1;
    border-bottom: 2px solid #0284c7;
    padding-bottom: 3mm;
    display: inline-block;
  }}

  .cover-hero {{
    margin: auto 0;
  }}

  .cover-emblem {{
    width: 22mm;
    height: 22mm;
    color: #0284c7;
    margin-bottom: 8mm;
  }}

  .cover-author {{
    font-family: 'Noto Sans JP', sans-serif;
    font-size: 11pt;
    font-weight: 600;
    letter-spacing: 0.1em;
    color: #334155;
    margin-bottom: 4mm;
  }}

  .cover-title {{
    font-family: 'Noto Serif JP', serif;
    font-size: 26pt;
    font-weight: 700;
    line-height: 1.25;
    color: #0f172a;
    letter-spacing: 0.02em;
    margin-bottom: 6mm;
  }}

  .cover-subtitle {{
    font-family: 'Noto Sans JP', sans-serif;
    font-size: 11pt;
    font-weight: 400;
    line-height: 1.6;
    color: #0369a1;
    max-width: 95%;
    border-left: 3px solid #0284c7;
    padding-left: 5mm;
  }}

  .cover-footer {{
    font-family: 'Plus Jakarta Sans', 'Noto Sans JP', sans-serif;
    font-size: 8.5pt;
    color: #64748b;
    border-top: 1px solid #cbd5e1;
    padding-top: 4mm;
    display: flex;
    justify-content: space-between;
  }}

  /* FRONTISPIECE */
  .frontispiece {{
    page-break-after: always;
    min-height: 75vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 20mm 15mm;
  }}

  .frontispiece-quote {{
    font-family: 'Noto Serif JP', serif;
    font-size: 12.5pt;
    line-height: 1.9;
    color: #1e293b;
    max-width: 90%;
    margin-bottom: 8mm;
    position: relative;
  }}

  .frontispiece-quote::before {{
    content: "“";
    font-family: 'Cinzel', serif;
    font-size: 40pt;
    color: #38bdf8;
    position: absolute;
    top: -20px;
    left: -25px;
    opacity: 0.5;
  }}

  .frontispiece-author {{
    font-family: 'Noto Sans JP', sans-serif;
    font-weight: 700;
    font-size: 10pt;
    letter-spacing: 0.15em;
    color: #0284c7;
  }}

  /* TYPOGRAPHY */
  h1, h2, h3, h4 {{
    font-family: 'Noto Serif JP', serif;
    color: #0f172a;
  }}

  h1 {{
    font-size: 18pt;
    text-align: center;
    margin-top: 8mm;
    margin-bottom: 4mm;
    font-weight: 700;
    line-height: 1.3;
    color: #0369a1;
  }}

  h2 {{
    font-size: 13pt;
    margin-top: 8mm;
    margin-bottom: 3.5mm;
    padding-bottom: 2mm;
    border-bottom: 1px solid #cbd5e1;
    color: #0369a1;
    page-break-after: avoid;
  }}

  h3 {{
    font-size: 10.5pt;
    font-family: 'Noto Sans JP', sans-serif;
    font-weight: 700;
    color: #1e293b;
    margin-top: 5mm;
    margin-bottom: 2.5mm;
    page-break-after: avoid;
  }}

  p {{
    margin-top: 0;
    margin-bottom: 3.5mm;
    text-align: justify;
  }}

  strong {{
    font-weight: 700;
    color: #0f172a;
  }}

  /* CALLOUTS */
  .callout {{
    margin: 5mm 0;
    padding: 4mm 5mm;
    border-radius: 2mm;
    background: #f0f9ff;
    border-left: 4px solid #0284c7;
    page-break-inside: avoid;
  }}

  .callout-title {{
    font-family: 'Noto Sans JP', sans-serif;
    font-weight: 700;
    font-size: 9.5pt;
    color: #0369a1;
    margin-bottom: 2mm;
    letter-spacing: 0.05em;
  }}

  .callout-body p:last-child {{
    margin-bottom: 0;
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
    line-height: 1.5;
  }}

  th {{
    background: #f1f5f9;
    color: #0f172a;
    font-family: 'Noto Sans JP', sans-serif;
    font-weight: 700;
    text-align: left;
    padding: 2.5mm 3mm;
    border-bottom: 2px solid #cbd5e1;
  }}

  td {{
    padding: 2.5mm 3mm;
    border-bottom: 1px solid #e2e8f0;
    vertical-align: top;
  }}

  tr:nth-child(even) td {{
    background: #f8fafc;
  }}

  /* PRE & CODE */
  pre {{
    font-family: 'JetBrains Mono', 'Noto Sans JP', monospace;
    font-size: 7.8pt;
    line-height: 1.45;
    background: #0f172a;
    color: #f8fafc;
    padding: 4mm;
    border-radius: 2mm;
    overflow-x: auto;
    page-break-inside: avoid;
    margin: 4mm 0;
    border: 1px solid #1e293b;
  }}

  code {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.5pt;
    background: #f1f5f9;
    color: #0369a1;
    padding: 1px 4px;
    border-radius: 1mm;
  }}

  pre code {{
    background: transparent;
    color: inherit;
    padding: 0;
  }}

  .chapter-break {{
    page-break-before: always;
  }}

  hr {{
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 5mm 0;
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

<!-- COVER PAGE -->
<div class="cover-page">
  <div class="cover-series">インナーカーレント・ライブラリー • 特別支援ガイド</div>
  <div class="cover-hero">
    <svg class="cover-emblem" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
      <path d="M12 2v8"></path>
      <path d="m4.93 10.93 1.41 1.41"></path>
      <path d="M2 18h2"></path>
      <path d="M20 18h2"></path>
      <path d="m19.07 10.93-1.41 1.41"></path>
      <path d="M22 22H2"></path>
      <path d="m8 22 4-10 4 10"></path>
    </svg>
    <div class="cover-author">ウラジーミル・アニャノフ（Vladimir Anyanov）</div>
    <div class="cover-title">懐中電灯の原理</div>
    <div class="cover-subtitle">ひきこもり脱出のための意識回路設計と身体的アプローチ<br>— 部屋が暗いのはあなたがダメだからではない。光の向きを1ミリ外に向ける60秒プロトコル</div>
  </div>
  <div class="cover-footer">
    <span>Inner Current Project • 意識の電磁気学</span>
    <span>2026年</span>
  </div>
</div>

<!-- FRONTISPIECE -->
<div class="frontispiece">
  <div class="frontispiece-quote">
    「部屋が暗いのは、あなたがダメな人間だからではありません。懐中電灯の光が、内側の機械に向けて曲がってしまっているだけです。心の中をいくら照らしても、答えは見つかりません。光を外の小さな現実に向けるだけで、内側の火事は止まります。」
  </div>
  <div class="frontispiece-author">ウラジーミル・アニャノフ</div>
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
print("Launching browser for Japanese PDF render...")
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"file:///{OUTPUT_HTML.replace(os.sep, '/')}", wait_until="networkidle")
    
    header_template = """
    <div style="font-family: 'Noto Sans JP', sans-serif; font-size: 7.5pt; color: #0369a1; width: 100%; display: flex; justify-content: space-between; padding: 0 18mm;">
      <span>ウラジーミル・アニャノフ • 懐中電灯の原理（ひきこもり支援ガイド）</span>
      <span>Inner Current Library</span>
    </div>
    """
    
    footer_template = """
    <div style="font-family: 'Noto Sans JP', sans-serif; font-size: 8pt; color: #64748b; width: 100%; display: flex; justify-content: center; padding: 0 18mm;">
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
        margin={"top": "18mm", "bottom": "18mm", "left": "18mm", "right": "18mm"}
    )
    browser.close()

# Copy to vault
shutil.copy2(OUTPUT_PDF, VAULT_PDF)

reader = pypdf.PdfReader(OUTPUT_PDF)
print(f"SUCCESS: Generated Japanese Pamphlet PDF! Total Pages: {len(reader.pages)}, Size: {os.path.getsize(OUTPUT_PDF) / 1024:.1f} KB")
