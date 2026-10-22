from playwright.sync_api import sync_playwright

html = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"></script>
<script>
  window.addEventListener('DOMContentLoaded', () => {
    renderMathInElement(document.body, {
      delimiters: [
        {left: '$$', right: '$$', display: true},
        {left: '$', right: '$', display: false}
      ],
      throwOnError: false
    });
    window.katexDone = true;
  });
</script>
</head>
<body>
<p>Here is formula:</p>
<p>$$\mathcal{H} = \frac{P_{\text{load}}}{P_{\text{total}}} = 1 - \frac{R_{\text{ego}}}{R_{\text{total}}} \to 1.0$$</p>
<p>Inline: $R_{\text{ego}} \to 0$ and $Q = I^2 \cdot R_{\text{ego}} \cdot t$</p>
</body>
</html>"""

with open("test_render_katex.html", "w", encoding="utf-8") as f:
    f.write(html)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(r"file:///c:/Users/vanya/Antigravity Projects/Apps/Inner Current/test_render_katex.html", wait_until="networkidle")
    page.wait_for_function("() => window.katexDone === true")
    page.wait_for_timeout(1000)
    page.pdf(path="test_render_katex.pdf")
    
    # Check if katex-display or katex-html element exists in DOM
    has_katex = page.evaluate("() => document.querySelector('.katex') !== null")
    print("KaTeX element rendered in DOM:", has_katex)
    browser.close()
