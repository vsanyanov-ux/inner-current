import os
import re
import shutil
import sys
import markdown
from playwright.sync_api import sync_playwright
import pypdf

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current"
VAULT_MD = r"C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\02_Wiki\Inner Current (Master Protocol Whitepaper — Dual Circuit and Superconductivity).md"

OUTPUT_HTML_PRINT = os.path.join(ROOT_DIR, "master_whitepaper_print.html")
OUTPUT_PDF_LIBRARY = os.path.join(ROOT_DIR, "IC Library", "Владимир Аньянов — Внутренний ток (Master Protocol Whitepaper — Двухконтурная электродинамика человека).pdf")
DIST_PDF = os.path.join(ROOT_DIR, "dist_site", "books", "whitepaper.pdf")
PUB_PDF = os.path.join(ROOT_DIR, "public", "books", "whitepaper.pdf")
DIST_READER_HTML = os.path.join(ROOT_DIR, "dist_site", "books", "whitepaper.html")
SITE_WHITEPAPER_HTML = os.path.join(ROOT_DIR, "dist_site", "whitepaper.html")

with open(VAULT_MD, "r", encoding="utf-8") as f:
    raw_md = f.read()

# Strip YAML frontmatter
raw_md = re.sub(r"^---.*?---\s*", "", raw_md, flags=re.DOTALL)

# Extract Mermaid diagrams before markdown processing so codehilite doesn't corrupt them
mermaid_blocks = {}
def extract_mermaid(match):
    idx = len(mermaid_blocks)
    key = f"MERMAIDPLACEHOLDER{idx}END"
    mermaid_blocks[key] = match.group(1).strip()
    return f"\n\n{key}\n\n"

processed_md = re.sub(r"```mermaid\s*\n([\s\S]*?)\n```", extract_mermaid, raw_md)

# Preprocess Callouts (> [!quote] etc.)
def replace_callout(match):
    ctype = match.group(1).lower()
    content = match.group(2)
    lines = [re.sub(r"^>\s?", "", line) for line in content.strip().split("\n")]
    title = lines[0].strip() if lines else ""
    body_lines = lines[1:] if len(lines) > 1 else []
    body_text = "\n".join(body_lines).strip()
    body_html = markdown.markdown(body_text, extensions=['tables', 'fenced_code', 'codehilite', 'def_list', 'nl2br'])
    
    icon = "⚡"
    if "quote" in ctype: icon = "📜"
    elif "important" in ctype or "warning" in ctype: icon = "⚠️"
    elif "tip" in ctype: icon = "💡"
    elif "info" in ctype: icon = "ℹ️"
    
    title_html = f'<div class="callout-title"><span>{icon}</span> <span>{title}</span></div>' if title else ""
    return f'<div class="callout callout-{ctype}">{title_html}<div class="callout-body">{body_html}</div></div>'

processed_md = re.sub(r"^>\s*\[!(\w+)\]([^\n]*(?:\n>[^\n]*)*)", replace_callout, processed_md, flags=re.MULTILINE)

# Preprocess Sections to inject page-break classes for print
print_md = re.sub(r"^(## (?:[1-9]|10)\. [^\n]+)", r'<div class="chapter-break"></div>\n\1', processed_md, flags=re.MULTILINE)
print_md = re.sub(r"^(## ⚡ Аннотация[^\n]+)", r'<div class="chapter-break"></div>\n\1', print_md, flags=re.MULTILINE)
print_md = re.sub(r"^(## 📚 Литература[^\n]+)", r'<div class="chapter-break"></div>\n\1', print_md, flags=re.MULTILINE)

# Convert Markdown to HTML
md_extensions = ['tables', 'fenced_code', 'codehilite', 'def_list', 'nl2br']
print_body = markdown.markdown(print_md, extensions=md_extensions)
web_body = markdown.markdown(processed_md, extensions=md_extensions)

# Restore Mermaid blocks into HTML
for key, mcode in mermaid_blocks.items():
    print_replacement = f'<div class="mermaid-print-block"><div class="mermaid">\n{mcode}\n</div></div>'
    web_replacement = f'<div class="mermaid-web-block my-10 p-4 sm:p-6 rounded-2xl bg-slate-900/80 border border-slate-800 shadow-xl overflow-x-auto"><div class="mermaid flex justify-center min-w-[320px]">\n{mcode}\n</div></div>'
    
    # markdown may wrap ___MERMAID_BLOCK_X___ in <p>___MERMAID_BLOCK_X___</p>
    print_body = re.sub(rf'<p>\s*{re.escape(key)}\s*</p>', print_replacement, print_body)
    print_body = print_body.replace(key, print_replacement)
    
    web_body = re.sub(rf'<p>\s*{re.escape(key)}\s*</p>', web_replacement, web_body)
    web_body = web_body.replace(key, web_replacement)

# Wrap tables
print_body = print_body.replace("<table>", '<div class="table-wrapper"><table>')
print_body = print_body.replace("</table>", '</table></div>')
web_body = web_body.replace("<table>", '<div class="overflow-x-auto my-6 border border-slate-800 rounded-xl"><table class="min-w-full divide-y divide-slate-800 text-sm">')
web_body = web_body.replace("</table>", '</table></div>')

# PRINT HTML (Optimized for Playwright A4 PDF generation)
PRINT_HTML = f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Внутренний ток — Master Protocol Whitepaper | Владимир Аньянов</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js" onload="renderMathInElement(document.body, {{delimiters: [{{left: '$$', right: '$$', display: true}}, {{left: '$', right: '$', display: false}}]}});"></script>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
  mermaid.initialize({{
    startOnLoad: true,
    theme: 'neutral',
    themeVariables: {{
      fontFamily: 'Plus Jakarta Sans, sans-serif',
      fontSize: '9.5pt',
      primaryColor: '#f8fafc',
      primaryTextColor: '#0f172a',
      primaryBorderColor: '#d97706',
      lineColor: '#2563eb',
      secondaryColor: '#f1f5f9',
      tertiaryColor: '#ffffff'
    }},
    securityLevel: 'loose'
  }});
</script>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Lora:ital,wght@0,400;0,500;0,600;1,400;1,500&family=JetBrains+Mono:wght@400;500;600&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

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
    padding: 24mm 16mm 20mm 16mm;
    border: 1px solid #e2e8f0;
    background: linear-gradient(145deg, #f8fafc 0%, #f1f5f9 100%);
    position: relative;
    box-sizing: border-box;
  }}

  .cover-series {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 8pt;
    font-weight: 700;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #d97706;
    border-bottom: 2px solid #f59e0b;
    padding-bottom: 3mm;
    display: inline-block;
  }}

  .cover-hero {{
    margin: auto 0;
  }}

  .cover-emblem {{
    width: 26mm;
    height: 26mm;
    color: #d97706;
    margin-bottom: 8mm;
  }}

  .cover-author {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 11pt;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 5mm;
  }}

  .cover-title {{
    font-family: 'Cinzel', serif;
    font-size: 24pt;
    font-weight: 800;
    line-height: 1.15;
    color: #0f172a;
    letter-spacing: -0.01em;
    margin-bottom: 6mm;
  }}

  .cover-subtitle {{
    font-family: 'Lora', serif;
    font-size: 11pt;
    font-style: italic;
    line-height: 1.5;
    color: #334155;
    max-width: 90%;
    border-left: 3px solid #f59e0b;
    padding-left: 5mm;
  }}

  .cover-footer {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 8pt;
    color: #64748b;
    border-top: 1px solid #cbd5e1;
    padding-top: 4mm;
    display: flex;
    justify-content: space-between;
  }}

  /* HEADINGS */
  h1 {{
    font-family: 'Cinzel', serif;
    font-size: 18pt;
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
    font-size: 13pt;
    font-weight: 600;
    color: #1e293b;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 2mm;
    margin-top: 8mm;
    margin-bottom: 4mm;
  }}

  h3 {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 10.5pt;
    font-weight: 600;
    color: #334155;
    margin-top: 5mm;
    margin-bottom: 2.5mm;
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
    font-size: 9pt;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #b45309;
    margin-bottom: 2mm;
  }}

  pre {{
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.2pt;
    line-height: 1.35;
    background: #0f172a;
    color: #f8fafc;
    padding: 4mm 5mm;
    border-radius: 6px;
    overflow-x: auto;
    margin: 4.5mm 0;
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

  .table-wrapper {{
    margin: 5mm 0;
    overflow-x: auto;
  }}

  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 8.5pt;
  }}

  th, td {{
    border: 1px solid #cbd5e1;
    padding: 2.5mm 3.5mm;
    text-align: left;
  }}

  th {{
    background: #f1f5f9;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 600;
    color: #0f172a;
  }}

  .mermaid-print-block {{
    margin: 6mm 0;
    text-align: center;
    page-break-inside: avoid;
    break-inside: avoid;
  }}

  .mermaid-print-block .mermaid {{
    display: flex;
    justify-content: center;
    width: 100%;
  }}

  .mermaid-print-block .mermaid svg {{
    max-width: 100%;
    height: auto;
    max-height: 190mm;
    margin: 0 auto;
    display: block;
  }}
</style>
</head>
<body>

<!-- COVER PAGE -->
<div class="cover-page">
  <div class="cover-series">Inner Current • Master Protocol Whitepaper • 2026</div>
  <div class="cover-hero">
    <svg class="cover-emblem" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
      <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"></path>
    </svg>
    <div class="cover-author">Владимир Аньянов</div>
    <div class="cover-title">ВНУТРЕННИЙ ТОК</div>
    <div class="cover-subtitle">Открытый протокол суверенной электродинамики человека и двухконтурной сверхпроводимости: каскад открытых диссипативных систем (Пригожин 1977 — Аньянов 2026), Proof-of-Action, закон потерь Джоуля — Ленца и закон лампочки.</div>
  </div>
  <div class="cover-footer">
    <span>Архитектура Внутреннего Тока • Спецификация стандарта</span>
    <span>Октябрь 2026</span>
  </div>
</div>

<!-- CONTENT -->
{print_body}

</body>
</html>
"""

with open(OUTPUT_HTML_PRINT, "w", encoding="utf-8") as f:
    f.write(PRINT_HTML)

print("Compiling PDF with Playwright...")
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"file:///{OUTPUT_HTML_PRINT.replace(os.sep, '/')}")
    # Wait for Mermaid and KaTeX
    try:
        page.wait_for_selector('.mermaid svg', timeout=15000)
    except Exception as e:
        print(f"Warning waiting for mermaid: {e}")
    page.wait_for_timeout(3500)
    
    page.pdf(
        path=OUTPUT_PDF_LIBRARY,
        format="A4",
        margin={"top": "22mm", "bottom": "22mm", "left": "18mm", "right": "18mm"},
        print_background=True,
        display_header_footer=True,
        header_template='<div style="font-size: 7.5pt; font-family: sans-serif; color: #94a3b8; width: 100%; text-align: right; padding-right: 18mm;">Владимир Аньянов • Внутренний ток (Master Protocol Whitepaper)</div>',
        footer_template='<div style="font-size: 7.5pt; font-family: sans-serif; color: #94a3b8; width: 100%; text-align: center;"><span class="pageNumber"></span> / <span class="totalPages"></span></div>'
    )
    browser.close()

# Copy PDF to target destinations
os.makedirs(os.path.dirname(DIST_PDF), exist_ok=True)
os.makedirs(os.path.dirname(PUB_PDF), exist_ok=True)
shutil.copy2(OUTPUT_PDF_LIBRARY, DIST_PDF)
shutil.copy2(OUTPUT_PDF_LIBRARY, PUB_PDF)
print(f"PDF successfully built and copied to:\n- {DIST_PDF}\n- {PUB_PDF}\n- {OUTPUT_PDF_LIBRARY}")

# NOW GENERATE STANDALONE WEB PAGE: dist_site/whitepaper.html
WEB_PAGE_HTML = f"""<!DOCTYPE html>
<html lang="ru" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Белая книга: Внутренний ток — Открытый протокол суверенной электродинамики | innercurrent.ru</title>
  <meta name="description" content="Официальная Белая книга (Master Protocol Whitepaper) системы 'Внутренний ток': двухконтурная электродинамика человека, Proof-of-Action, закон Джоуля-Ленца, теорема лампочки и режим сверхпроводимости.">
  
  <!-- Favicon -->
  <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>⚡</text></svg>">

  <!-- Fonts & Math -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Lora:ital,wght@0,400;0,500;0,600;1,400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js" onload="renderMathInElement(document.body, {{delimiters: [{{left: '$$', right: '$$', display: true}}, {{left: '$', right: '$', display: false}}]}});"></script>

  <!-- Mermaid Diagrams -->
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <script>
    mermaid.initialize({{
      startOnLoad: true,
      theme: 'dark',
      themeVariables: {{
        darkMode: true,
        background: '#090d16',
        mainBkg: '#0f172a',
        nodeBorder: '#f59e0b',
        textColor: '#f8fafc',
        lineColor: '#38bdf8',
        secondaryColor: '#1e293b',
        tertiaryColor: '#0f172a',
        fontFamily: 'Inter, system-ui, sans-serif',
        fontSize: '13px'
      }},
      securityLevel: 'loose'
    }});
  </script>

  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          fontFamily: {{
            sans: ['Inter', 'system-ui', 'sans-serif'],
            serif: ['Lora', 'Georgia', 'serif'],
            display: ['Cinzel', 'serif'],
            mono: ['JetBrains Mono', 'monospace'],
          }},
          colors: {{
            slate: {{
              850: '#111827',
              900: '#090d16',
              950: '#030712',
            }}
          }}
        }}
      }}
    }}
  </script>

  <style>
    body {{
      background-color: #030712;
      color: #f1f5f9;
      -webkit-font-smoothing: antialiased;
    }}
    .prose h1, .prose h2, .prose h3 {{
      font-family: 'Cinzel', serif;
      color: #f8fafc;
    }}
    .prose p, .prose li {{
      font-family: 'Lora', Georgia, serif;
      color: #cbd5e1;
      line-height: 1.8;
      font-size: 1.05rem;
    }}
    .prose strong {{
      color: #f8fafc;
    }}
    .prose blockquote {{
      border-left: 4px solid #f59e0b;
      background: rgba(245, 158, 11, 0.05);
      border-radius: 0 0.75rem 0.75rem 0;
      padding: 1rem 1.25rem;
      color: #fef3c7;
      font-style: italic;
    }}
    .callout {{
      border-left: 4px solid #f59e0b;
      background: rgba(245, 158, 11, 0.07);
      border-radius: 0 0.75rem 0.75rem 0;
      padding: 1.25rem;
      margin: 1.5rem 0;
    }}
    .callout-title {{
      font-family: 'Inter', sans-serif;
      font-weight: 700;
      text-transform: uppercase;
      font-size: 0.85rem;
      letter-spacing: 0.05em;
      color: #fbbf24;
      margin-bottom: 0.5rem;
    }}
    pre {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.82rem;
      line-height: 1.45;
      background: #090d16;
      border: 1px solid #1e293b;
      color: #38bdf8;
      padding: 1.25rem;
      border-radius: 0.75rem;
      overflow-x: auto;
      margin: 1.5rem 0;
    }}
    code {{
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.9em;
      background: #1e293b;
      color: #fbbf24;
      padding: 0.15rem 0.35rem;
      border-radius: 0.25rem;
    }}
    pre code {{
      background: transparent;
      color: inherit;
      padding: 0;
    }}
    .mermaid-web-block {{
      page-break-inside: avoid;
      break-inside: avoid;
    }}
    .mermaid-web-block .mermaid {{
      display: flex;
      justify-content: center;
      width: 100%;
    }}
    .mermaid-web-block .mermaid svg {{
      max-width: 100%;
      height: auto;
      display: block;
      margin: 0 auto;
    }}
  </style>
</head>
<body class="selection:bg-amber-500 selection:text-slate-950 min-h-screen flex flex-col">

  <!-- TOP STICKY NAVBAR -->
  <nav class="sticky top-0 z-50 bg-slate-950/85 backdrop-blur-md border-b border-slate-800/80">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
      <a href="index.html" class="flex items-center gap-3 group">
        <div class="w-8 h-8 rounded-lg bg-gradient-to-tr from-amber-500 to-amber-300 text-slate-950 font-black text-lg flex items-center justify-center shadow-lg shadow-amber-500/20 group-hover:scale-105 transition">
          ⚡
        </div>
        <div>
          <div class="font-display font-bold text-sm tracking-wide text-slate-100 group-hover:text-amber-300 transition">
            INNER CURRENT
          </div>
          <div class="text-[9px] uppercase font-mono tracking-widest text-slate-400 font-semibold">
            Master Protocol Whitepaper
          </div>
        </div>
      </a>

      <div class="flex items-center gap-4 text-xs font-medium">
        <a href="index.html" class="text-slate-400 hover:text-slate-200 transition">Главная</a>
        <a href="manifesto.html" class="text-amber-400 hover:text-amber-300 transition flex items-center gap-1 font-semibold"><span>⚡</span> Манифест</a>
        <a href="books/whitepaper.pdf" download class="px-3.5 py-1.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold transition flex items-center gap-1.5 shadow-md shadow-amber-500/10">
          <span>📥</span> <span>Скачать PDF</span>
        </a>
      </div>
    </div>
  </nav>

  <!-- HERO HEADER -->
  <header class="py-16 sm:py-20 border-b border-slate-800/80 bg-gradient-to-b from-slate-900/50 via-slate-950 to-slate-950 relative overflow-hidden">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 relative z-10 text-center">
      <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs font-mono font-semibold tracking-wider uppercase mb-6">
        <span>⚡</span> Официальная спецификация протокола • 2026
      </div>
      <h1 class="text-3xl sm:text-5xl font-extrabold text-slate-100 tracking-tight leading-tight font-display mb-4">
        Белая книга: Внутренний ток
      </h1>
      <p class="text-lg sm:text-xl text-slate-300 max-w-2xl mx-auto font-serif italic mb-8">
        Открытый протокол суверенной электродинамики человека и двухконтурной сверхпроводимости
      </p>
      
      <div class="flex flex-wrap items-center justify-center gap-4 text-xs font-mono text-slate-400 mb-8">
        <div>Автор: <span class="text-slate-200 font-semibold">Владимир Аньянов</span></div>
        <div class="hidden sm:inline">•</div>
        <div>Версия: <span class="text-amber-400 font-semibold">Master Standard 2.0</span></div>
        <div class="hidden sm:inline">•</div>
        <div>Статус: <span class="text-emerald-400 font-semibold">Evergreen / Open-Source</span></div>
      </div>

      <div class="flex flex-wrap items-center justify-center gap-3">
        <a href="books/whitepaper.pdf" download class="px-5 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-sm transition flex items-center gap-2 shadow-lg shadow-amber-500/20">
          <span>📥</span> Скачать официальный White Paper (PDF)
        </a>
        <a href="manifesto.html" class="px-5 py-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 font-semibold text-sm transition flex items-center gap-2">
          <span>⚡</span> Читать народный Манифест
        </a>
      </div>
    </div>
  </header>

  <!-- MAIN ARTICLE -->
  <main class="flex-1 py-12 max-w-4xl mx-auto px-4 sm:px-6 w-full">
    <article class="prose prose-invert max-w-none">
      {web_body}
    </article>
  </main>

  <!-- FOOTER -->
  <footer class="border-t border-slate-800/80 bg-slate-950 py-12 mt-16 text-center text-xs font-mono text-slate-500">
    <div class="max-w-4xl mx-auto px-4 space-y-3">
      <div>© 2026 Владимир Аньянов • Архитектура Внутреннего Тока (Inner Current)</div>
      <div>Открытый протокол человеческого благополучия и суверенной сверхпроводимости.</div>
      <div class="pt-3">
        <a href="books/whitepaper.pdf" download class="text-amber-400 hover:underline">Скачать White Paper в PDF</a> • 
        <a href="manifesto.html" class="text-amber-400 hover:underline">Манифест</a> • 
        <a href="index.html" class="text-amber-400 hover:underline">Библиотека «Золотая Семёрка»</a>
      </div>
    </div>
  </footer>

</body>
</html>
"""

with open(SITE_WHITEPAPER_HTML, "w", encoding="utf-8") as f:
    f.write(WEB_PAGE_HTML)

with open(DIST_READER_HTML, "w", encoding="utf-8") as f:
    f.write(WEB_PAGE_HTML)

PUB_WHITEPAPER_HTML = os.path.join(ROOT_DIR, "public", "whitepaper.html")
PUB_READER_HTML = os.path.join(ROOT_DIR, "public", "books", "whitepaper.html")
os.makedirs(os.path.dirname(PUB_WHITEPAPER_HTML), exist_ok=True)
os.makedirs(os.path.dirname(PUB_READER_HTML), exist_ok=True)
shutil.copy2(SITE_WHITEPAPER_HTML, PUB_WHITEPAPER_HTML)
shutil.copy2(DIST_READER_HTML, PUB_READER_HTML)

print(f"Web whitepaper successfully created at:\n- {SITE_WHITEPAPER_HTML}\n- {DIST_READER_HTML}\n- {PUB_WHITEPAPER_HTML}\n- {PUB_READER_HTML}")
