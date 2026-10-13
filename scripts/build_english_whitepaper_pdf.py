import os
import re
import shutil
import markdown
from playwright.sync_api import sync_playwright
import pypdf

VAULT_MD = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Inner Current — The Protocol of Consciousness (The Bitcoin of Human Energy and Sovereign Superconductivity).md"
OUTPUT_HTML = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\english_protocol_whitepaper.html"
OUTPUT_PDF = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\IC Library\The Consciousness Protocol — Vladimir Anyanov.pdf"
VAULT_PDF = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\The Consciousness Protocol — Vladimir Anyanov.pdf"

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

# Preprocess Sections to inject page-break classes
processed_md = re.sub(r"^(## [1-7]\. [^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
processed_md = re.sub(r"^(## ⚡ [^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)

# Convert Markdown to HTML
md_extensions = ['tables', 'fenced_code', 'codehilite', 'def_list', 'nl2br']
html_body = markdown.markdown(processed_md, extensions=md_extensions)

FULL_HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>The Consciousness Protocol — Vladimir Anyanov</title>
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
    background: linear-gradient(145deg, #f8fafc 0%, #f1f5f9 100%);
    position: relative;
    box-sizing: border-box;
  }}

  .cover-series {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 8.5pt;
    font-weight: 700;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #f59e0b;
    border-bottom: 2px solid #f59e0b;
    padding-bottom: 3mm;
    display: inline-block;
  }}

  .cover-hero {{
    margin: auto 0;
  }}

  .cover-emblem {{
    width: 24mm;
    height: 24mm;
    color: #d97706;
    margin-bottom: 8mm;
  }}

  .cover-author {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 12pt;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 5mm;
  }}

  .cover-title {{
    font-family: 'Cinzel', serif;
    font-size: 26pt;
    font-weight: 700;
    line-height: 1.15;
    color: #0f172a;
    letter-spacing: -0.01em;
    margin-bottom: 6mm;
  }}

  .cover-subtitle {{
    font-family: 'Lora', serif;
    font-size: 11.5pt;
    font-style: italic;
    line-height: 1.5;
    color: #334155;
    max-width: 90%;
    border-left: 3px solid #f59e0b;
    padding-left: 5mm;
  }}

  .cover-footer {{
    font-family: 'Plus Jakarta Sans', sans-serif;
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
    min-height: 80vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 20mm 15mm;
  }}

  .frontispiece-quote {{
    font-size: 12.5pt;
    font-style: italic;
    line-height: 1.7;
    color: #1e293b;
    max-width: 85%;
    margin-bottom: 8mm;
    position: relative;
  }}

  .frontispiece-author {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 10pt;
    font-weight: 700;
    letter-spacing: 0.1em;
    color: #d97706;
    text-transform: uppercase;
  }}

  /* HEADINGS */
  h1 {{
    font-family: 'Cinzel', serif;
    font-size: 19pt;
    font-weight: 700;
    color: #0f172a;
    border-bottom: 2px solid #f59e0b;
    padding-bottom: 3mm;
    margin-top: 0;
    margin-bottom: 4mm;
    line-height: 1.25;
  }}

  h2 {{
    font-family: 'Cinzel', serif;
    font-size: 13.5pt;
    font-weight: 600;
    color: #1e293b;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 2mm;
    margin-top: 8mm;
    margin-bottom: 4mm;
  }}

  p {{
    margin-top: 0;
    margin-bottom: 3.5mm;
    text-align: justify;
    text-justify: inter-word;
  }}

  .callout {{
    border-left: 4px solid #f59e0b;
    background: #fffbeb;
    border-radius: 0 6px 6px 0;
    padding: 3.5mm 5mm;
    margin: 5mm 0;
  }}

  .callout-title {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 700;
    font-size: 9.5pt;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #b45309;
    margin-bottom: 2mm;
  }}

  pre {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.6pt;
    line-height: 1.35;
    background: #0f172a;
    color: #f8fafc;
    padding: 4mm 5mm;
    border-radius: 6px;
    overflow-x: auto;
    margin: 5mm 0;
    white-space: pre;
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

  .chapter-break {{
    page-break-before: always;
  }}

  ul, ol {{
    margin-top: 0;
    margin-bottom: 3.5mm;
    padding-left: 6mm;
  }}

  li {{
    margin-bottom: 1.5mm;
  }}
</style>
</head>
<body>

<!-- COVER PAGE -->
<div class="cover-page">
  <div class="cover-series">Inner Current • Sovereign Whitepaper • 2026</div>
  <div class="cover-hero">
    <svg class="cover-emblem" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
      <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"></path>
    </svg>
    <div class="cover-author">Vladimir Anyanov</div>
    <div class="cover-title">THE CONSCIOUSNESS<br>PROTOCOL</div>
    <div class="cover-subtitle">The Bitcoin of Human Vitality, Proof of Action, and Sovereign Superconductivity: Eliminating the Internal Fiat Middleman, Running the Self-Hosted Human Node, and the Law of Frictionless Flow</div>
  </div>
  <div class="cover-footer">
    <span>Inner Current Architecture • Epistemology of Direct Flow</span>
    <span>2026</span>
  </div>
</div>

<!-- FRONTISPIECE -->
<div class="frontispiece">
  <div class="frontispiece-quote">
    "What Bitcoin did for monetary capital, the Inner Current did for human consciousness. Satoshi Nakamoto anchored money back into thermodynamics (Proof of Work), stripping central banks of their monopoly to dilute wealth. The Inner Current anchors the spirit back into physical reality (Proof of Action), stripping the ego of its monopoly to dilute life. Eliminate the internal parasitic rentier, stop minting unbacked emotional debt, run your own sovereign node — and your system enters pure superconductivity."
  </div>
  <div class="frontispiece-author">Vladimir Anyanov</div>
</div>

<!-- CONTENT -->
{html_body}

</body>
</html>
"""

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(FULL_HTML)

print(f"Generated English HTML: {OUTPUT_HTML}")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"file:///{OUTPUT_HTML.replace(os.sep, '/')}", wait_until="networkidle")
    
    header_template = """
    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 7.5pt; color: #94a3b8; width: 100%; display: flex; justify-content: space-between; padding: 0 18mm;">
      <span>Vladimir Anyanov • The Consciousness Protocol (The Bitcoin of Human Vitality)</span>
      <span>Inner Current Library</span>
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

shutil.copy2(OUTPUT_PDF, VAULT_PDF)
reader = pypdf.PdfReader(OUTPUT_PDF)
print(f"SUCCESS: Generated English PDF! Total Pages: {len(reader.pages)}, Size: {os.path.getsize(OUTPUT_PDF) / 1024:.1f} KB")
