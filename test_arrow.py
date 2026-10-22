from playwright.sync_api import sync_playwright

html = """<!DOCTYPE html>
<html>
<head>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js"></script>
</head>
<body>
<p id="math">$$\\mathcal{H} = \\frac{P_{\\text{load}}}{P_{\\text{total}}} = 1 - \\frac{R_{\\text{ego}}}{R_{\\text{total}}} \\xrightarrow{R_{\\text{ego}} \\to 0} 1.0$$</p>
<script>
document.addEventListener("DOMContentLoaded", () => {
    renderMathInElement(document.body, {
        delimiters: [{left: "$$", right: "$$", display: true}]
    });
});
</script>
</body>
</html>"""

with open("test_arrow.html", "w", encoding="utf-8") as f:
    f.write(html)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(r"file:///c:/Users/vanya/Antigravity Projects/Apps/Inner Current/test_arrow.html", wait_until="networkidle")
    page.wait_for_timeout(1000)
    has_error = page.evaluate("() => document.querySelector('.katex-error') !== null")
    has_katex = page.evaluate("() => document.querySelector('.katex') !== null")
    inner = page.evaluate("() => document.querySelector('#math').innerText")
    print("Has KaTeX error:", has_error)
    print("Has KaTeX:", has_katex)
    print("Inner text:", repr(inner))
    browser.close()
