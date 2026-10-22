import asyncio
import os
from playwright.async_api import async_playwright

async def render():
    html_path = os.path.abspath("memes/meme_02_relationship_card.html")
    output_png = os.path.abspath("memes/meme_02_relationship_final.png")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=2)
        await page.goto(f"file:///{html_path.replace(os.sep, '/')}", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        await page.screenshot(path=output_png, quality=95, type="jpeg")
        await browser.close()
        print(f"Rendered Meme 02 Card successfully to {output_png}")

if __name__ == "__main__":
    asyncio.run(render())
