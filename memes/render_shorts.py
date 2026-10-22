import asyncio
import os
from playwright.async_api import async_playwright

async def render():
    html_path = os.path.abspath("memes/meme_car_shorts_9_16.html")
    output_png = os.path.abspath("memes/meme_01_car_shorts_9_16.png")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        # Viewport strictly 1080x1920 (9:16)
        page = await browser.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
        await page.goto(f"file:///{html_path.replace(os.sep, '/')}", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        await page.screenshot(path=output_png, quality=95, type="jpeg")
        await browser.close()
        print(f"Rendered 9:16 Shorts successfully to {output_png}")

if __name__ == "__main__":
    asyncio.run(render())
