import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

INPUT_IMG = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\content\ukulele_shorts\exports\scene1_keyframe.jpg"
OUTPUT_COVER = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\content\ukulele_shorts\exports\ukulele_viral_cover.jpg"

img = Image.open(INPUT_IMG).convert("RGBA")
W, H = img.size

# 1. Color and Contrast Pop for YouTube Feed
enhancer = ImageEnhance.Color(img)
img = enhancer.enhance(1.15)
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(1.10)

# Create an overlay for graphics
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

# Add subtle top vignette for text readability
for y in range(int(H * 0.35)):
    alpha = int(180 * (1 - y / (H * 0.35)) ** 1.5)
    draw.line([(0, y), (W, y)], fill=(0, 0, 15, alpha))

# Bottom subtle vignette
start_y = int(H * 0.82)
for y in range(start_y, H):
    prog = max(0.0, min(1.0, (y - start_y) / (H - start_y)))
    alpha = int(160 * (prog ** 1.5))
    draw.line([(0, y), (W, y)], fill=(0, 0, 15, alpha))

font_path_impact = r"C:\Windows\Fonts\impact.ttf"
font_path_arial = r"C:\Windows\Fonts\arialbd.ttf"

# Top Badge: "ТАЙНА 2500 ЛЕТ"
badge_font = ImageFont.truetype(font_path_arial, 36)
badge_text = "ТАЙНА 2500 ЛЕТ"
bbox = badge_font.getbbox(badge_text)
bw = bbox[2] - bbox[0]
bh = bbox[3] - bbox[1]
bx = (W - bw) // 2
by = 50

# Badge pill background
pad_x, pad_y = 24, 10
draw.rounded_rectangle(
    [bx - pad_x, by - pad_y, bx + bw + pad_x, by + bh + pad_y + 4],
    radius=20,
    fill=(255, 60, 0, 235),
    outline=(255, 230, 0, 255),
    width=3
)
draw.text((bx, by), badge_text, font=badge_font, fill=(255, 255, 255, 255))

# Main Hook above the hair/forehead
title_font = ImageFont.truetype(font_path_impact, 94)

def draw_3d_text(draw, x, y, text, font, fill_color, stroke_color=(0, 0, 0), stroke_w=10, shadow_offset=8):
    for sx in range(shadow_offset // 2, shadow_offset + 1):
        for sy in range(shadow_offset // 2, shadow_offset + 1):
            draw.text((x + sx, y + sy), text, font=font, fill=(0, 0, 0, 230))
    draw.text((x, y), text, font=font, fill=fill_color, stroke_width=stroke_w, stroke_fill=stroke_color)

text1 = "СКОЛЬКО"
bbox1 = title_font.getbbox(text1)
w1 = bbox1[2] - bbox1[0]
x1 = (W - w1) // 2
y1 = 125

text2 = "ВЕСИТ ДУША?"
bbox2 = title_font.getbbox(text2)
w2 = bbox2[2] - bbox2[0]
x2 = (W - w2) // 2
y2 = y1 + 95

draw_3d_text(draw, x1, y1, text1, title_font, fill_color=(255, 255, 255), stroke_color=(0, 0, 0), stroke_w=12, shadow_offset=10)
draw_3d_text(draw, x2, y2, text2, title_font, fill_color=(255, 235, 0), stroke_color=(0, 0, 0), stroke_w=12, shadow_offset=12)

# Callout near the digital scale display (Bottom right of the scale)
callout_font = ImageFont.truetype(font_path_arial, 52)
callout_text = "400 ГРАММ?!"
c_bbox = callout_font.getbbox(callout_text)
cw = c_bbox[2] - c_bbox[0]
ch = c_bbox[3] - c_bbox[1]
cx = (W - cw) // 2
cy = H - 180

# Callout banner
draw.rounded_rectangle(
    [cx - 30, cy - 16, cx + cw + 30, cy + ch + 18],
    radius=20,
    fill=(0, 0, 0, 220),
    outline=(0, 215, 255, 255),
    width=5
)
draw.text((cx, cy), callout_text, font=callout_font, fill=(0, 235, 255, 255))

# Composite overlay
final_img = Image.alpha_composite(img, overlay)
final_img = final_img.convert("RGB")
final_img.save(OUTPUT_COVER, "JPEG", quality=95)
print(f"Viral cover created: {OUTPUT_COVER}")
