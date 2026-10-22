import os
import re
import shutil
import markdown
from playwright.sync_api import sync_playwright
import pypdf

VAULT_MD = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Brochure — The Georgism of Consciousness (Attention as Land, Tanden as Labor and the Ego-Rentier).md"
OUTPUT_HTML = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\georgism_of_consciousness.html"
OUTPUT_PDF = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\IC Library\The Georgism of Consciousness — Vladimir Anyanov.pdf"
VAULT_PDF = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\The Georgism of Consciousness — Vladimir Anyanov.pdf"
PUBLIC_PDF = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\public\books\the_georgism_of_consciousness.pdf"
DIST_PDF = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\dist_site\books\the_georgism_of_consciousness.pdf"

ROOT_DIR = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current"
KATEX_CSS = os.path.abspath(os.path.join(ROOT_DIR, "node_modules", "katex", "dist", "katex.min.css")).replace("\\", "/")
KATEX_JS = os.path.abspath(os.path.join(ROOT_DIR, "node_modules", "katex", "dist", "katex.min.js")).replace("\\", "/")
KATEX_AUTO = os.path.abspath(os.path.join(ROOT_DIR, "node_modules", "katex", "dist", "contrib", "auto-render.min.js")).replace("\\", "/")

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

# Preprocess Sections to inject chapter-break classes
processed_md = re.sub(r"^(## Part [^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)

# Convert Markdown to HTML
md_extensions = ['tables', 'fenced_code', 'codehilite', 'def_list', 'nl2br']
html_body = markdown.markdown(processed_md, extensions=md_extensions)

# Wrap tables in responsive containers
html_body = html_body.replace("<table>", '<div class="table-wrapper"><table>')
html_body = html_body.replace("</table>", '</table></div>')

# Wrap display math in container for centering and convert to \[...\]
html_body = re.sub(r"\$\$(.*?)\$\$", r'<div class="math-display">\\[\1\\]</div>', html_body, flags=re.DOTALL)
html_body = re.sub(r"\$([^\$\n]+?)\$", r'<span class="math-inline">\\(\1\\)</span>', html_body)

FULL_HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>The Georgism of Consciousness — Vladimir Anyanov</title>
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
  }});
</script>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Lora:ital,wght@0,400;0,500;0,600;1,400;1,500&family=JetBrains+Mono:wght@400;500&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

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

  /* COVER STYLING */
  .cover-page {{
    page-break-after: always;
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 24mm 16mm 20mm 16mm;
    border: 1px solid #e2e8f0;
    background: radial-gradient(circle at 80% 20%, rgba(245, 158, 11, 0.08) 0%, transparent 60%),
                linear-gradient(145deg, #f8fafc 0%, #f1f5f9 100%);
    position: relative;
    box-sizing: border-box;
  }}

  .cover-series {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 8.5pt;
    font-weight: 800;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #b45309;
    border-bottom: 2px solid #f59e0b;
    padding-bottom: 3.5mm;
    display: inline-block;
  }}

  .cover-hero {{
    margin: auto 0;
  }}

  .cover-emblem {{
    width: 58px;
    height: 58px;
    margin-bottom: 6mm;
    color: #f59e0b;
  }}

  .cover-author {{
    font-family: 'Cinzel', serif;
    font-size: 13pt;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #64748b;
    margin-bottom: 4mm;
  }}

  .cover-title {{
    font-family: 'Cinzel', serif;
    font-size: 26pt;
    font-weight: 700;
    line-height: 1.18;
    color: #0f172a;
    letter-spacing: -0.01em;
    margin-bottom: 6mm;
  }}

  .cover-subtitle {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 11pt;
    font-weight: 400;
    line-height: 1.55;
    color: #475569;
    max-width: 92%;
    border-left: 3px solid #f59e0b;
    padding-left: 5mm;
  }}

  .cover-footer {{
    display: flex;
    justify-content: space-between;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 8pt;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #94a3b8;
    border-top: 1px solid #cbd5e1;
    padding-top: 4mm;
  }}

  /* FRONTISPIECE */
  .frontispiece {{
    page-break-after: always;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    min-height: 80vh;
    padding: 0 14mm;
    text-align: center;
  }}

  .frontispiece-quote {{
    font-family: 'Lora', Georgia, serif;
    font-size: 13pt;
    font-style: italic;
    line-height: 1.8;
    color: #334155;
    margin-bottom: 7mm;
    position: relative;
  }}

  .frontispiece-quote::before {{
    content: "“";
    font-family: 'Cinzel', serif;
    font-size: 50pt;
    color: #f59e0b;
    opacity: 0.35;
    position: absolute;
    top: -24px;
    left: -28px;
  }}

  .frontispiece-author {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 9pt;
    font-weight: 700;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: #b45309;
  }}

  /* HEADINGS */
  h1 {{
    font-family: 'Cinzel', serif;
    font-size: 20pt;
    font-weight: 700;
    color: #0f172a;
    line-height: 1.3;
    margin-top: 0;
    margin-bottom: 5mm;
    border-bottom: 2px solid #e2e8f0;
    padding-bottom: 3mm;
  }}

  h2 {{
    font-family: 'Cinzel', serif;
    font-size: 14pt;
    font-weight: 700;
    color: #0f172a;
    margin-top: 8mm;
    margin-bottom: 3.5mm;
    border-bottom: 1px solid #f1f5f9;
    padding-bottom: 2mm;
  }}

  h3 {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 11pt;
    font-weight: 700;
    color: #1e293b;
    margin-top: 5mm;
    margin-bottom: 2.5mm;
  }}

  p {{
    margin-top: 0;
    margin-bottom: 3.5mm;
    text-align: justify;
  }}

  .chapter-break {{
    page-break-before: always;
  }}

  /* CALLOUTS */
  .callout {{
    margin: 5mm 0;
    padding: 4mm 5mm;
    border-radius: 6px;
    border-left: 4px solid #f59e0b;
    background: #fffbeb;
    page-break-inside: avoid;
  }}

  .callout-quote {{
    border-left-color: #f59e0b;
    background: #fffbeb;
  }}

  .callout-title {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 9pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #92400e;
    margin-bottom: 2mm;
  }}

  .callout-body {{
    font-size: 10pt;
    line-height: 1.6;
    color: #78350f;
  }}

  /* CODE & ASCII DIAGRAMS */
  pre {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.8pt;
    line-height: 1.4;
    background: #0f172a;
    color: #e2e8f0;
    padding: 4mm 5mm;
    border-radius: 6px;
    overflow-x: auto;
    page-break-inside: avoid;
    margin: 4mm 0;
    border: 1px solid #1e293b;
  }}

  code {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 8.8pt;
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

  /* LISTS */
  ul, ol {{
    margin-top: 0;
    margin-bottom: 3.5mm;
    padding-left: 6mm;
  }}

  li {{
    margin-bottom: 1.8mm;
    text-align: justify;
  }}

  /* BLOCKQUOTE */
  blockquote {{
    margin: 4mm 0;
    padding: 3mm 5mm;
    border-left: 3px solid #cbd5e1;
    color: #475569;
    font-style: italic;
    background: #f8fafc;
    border-radius: 0 4px 4px 0;
    page-break-inside: avoid;
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
  <div class="cover-series">Inner Current • Classical Synthesis • 2026</div>
  <div class="cover-hero">
    <svg class="cover-emblem" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
      <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"></path>
    </svg>
    <div class="cover-author">Vladimir Anyanov</div>
    <div class="cover-title">THE GEORGISM OF<br>CONSCIOUSNESS</div>
    <div class="cover-subtitle">The Historical Paradox of Progress and the Triad of Mind: Attention as Land, Tanden as Labor, Gyo as Manifest Action, and the Expropriation of the Ego-Rentier</div>
  </div>
  <div class="cover-footer">
    <span>Inner Current Architecture • Epistemology of Direct Flow</span>
    <span>2026</span>
  </div>
</div>

<!-- FRONTISPIECE -->
<div class="frontispiece">
  <div class="frontispiece-quote">
    "Creators do not suffer from a deficit of vitality; their physical core is capable of moving mountains. Creators are dying because they have become indentured serfs upon their own territory: their entire attention has been monopolized by a speculative Ego-Rentier, demanding an extortionate toll of anxiety for every heartbeat of real life."
  </div>
  <div class="frontispiece-author">Vladimir Anyanov • 2026</div>
</div>

<!-- CONTENT -->
{html_body}

</body>
</html>
"""

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(FULL_HTML)

print(f"Generated HTML: {OUTPUT_HTML}")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"file:///{OUTPUT_HTML.replace(os.sep, '/')}", wait_until="networkidle")
    
    header_template = """
    <div style="font-family: 'Plus Jakarta Sans', sans-serif; font-size: 7.5pt; color: #94a3b8; width: 100%; display: flex; justify-content: space-between; padding: 0 18mm;">
      <span>Vladimir Anyanov • The Georgism of Consciousness (Attention as Land, Tanden as Labor, Gyo and the Ego-Rentier)</span>
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

# Synchronize across destinations
shutil.copy2(OUTPUT_PDF, VAULT_PDF)
for d in [PUBLIC_PDF, DIST_PDF]:
    os.makedirs(os.path.dirname(d), exist_ok=True)
    shutil.copy2(OUTPUT_PDF, d)

reader = pypdf.PdfReader(OUTPUT_PDF)
print(f"SUCCESS: Generated PDF! Total Pages: {len(reader.pages)}, Size: {os.path.getsize(OUTPUT_PDF) / 1024:.1f} KB")
