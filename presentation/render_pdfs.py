import os
import base64
from playwright.sync_api import sync_playwright
import pypdf

DIR = os.path.dirname(os.path.abspath(__file__))

def encode_image(filename):
    path = os.path.join(DIR, filename)
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:image/jpeg;base64,{data}"

def render_pdf(html_name, pdf_name, image_var, image_file):
    html_path = os.path.join(DIR, html_name)
    pdf_path = os.path.join(DIR, pdf_name)
    
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    b64_img = encode_image(image_file)
    content = content.replace(f'src="{image_file}"', f'src="{b64_img}"')
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.set_content(content, wait_until="networkidle")
        page.pdf(
            path=pdf_path,
            format="A4",
            print_background=True,
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"}
        )
        browser.close()
    
    # Check page count
    reader = pypdf.PdfReader(pdf_path)
    page_count = len(reader.pages)
    print(f"Generated {pdf_name}: {page_count} page(s), size: {os.path.getsize(pdf_path)} bytes")

if __name__ == "__main__":
    render_pdf("inner_current_system_one_pager.html", "inner_current_system_one_pager.pdf", "image1", "image1.jpg")
    render_pdf("relationship_case_one_pager.html", "relationship_case_one_pager.pdf", "image2", "image2.jpg")
