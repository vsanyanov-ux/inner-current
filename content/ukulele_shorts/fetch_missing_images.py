import urllib.request
import urllib.parse
import os
import time

OUTPUT_DIR = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\content\ukulele_shorts\exports"
os.makedirs(OUTPUT_DIR, exist_ok=True)

PROMPTS = [
    (
        "scene5_keyframe.jpg",
        "Vertical 9:16, Pixar Disney 3D animation style. A charismatic 30yo male presenter with styled pompadour hair and van dyke beard, wearing tailored navy blue blazer over white shirt. He exhales in deep serene relief. His lower abdomen gently glows with a warm golden core of radiant light labeled ТАНДЭН. His hands are completely relaxed, touching the ukulele strings feather-light. Dazzling golden musical light waves fill the cozy studio. Enlightened peaceful Pixar smile, 8k."
    ),
    (
        "scene6_keyframe.jpg",
        "Vertical 9:16, Pixar Disney 3D animation style. The charismatic 30yo male presenter in navy blue blazer and white shirt stands holding a wooden soprano ukulele, smiling charismatically and winking at camera. Beside him floats a big glossy 3D YouTube subscribe button labeled ПОДПИСАТЬСЯ with a golden bell icon, under a glowing neon sign ВНУТРЕННИЙ ТОК. Warm cinematic studio lighting, celebratory golden confetti, Pixar Disney style, 8k."
    )
]

def fetch(filename, prompt):
    target = os.path.join(OUTPUT_DIR, filename)
    print(f"Downloading {filename}...")
    encoded = urllib.parse.quote(prompt)
    seed = int(time.time()) + hash(filename) % 10000
    # Standard free endpoint without model param
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=768&height=1344&nologo=true&seed={seed}"
    
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    )
    with urllib.request.urlopen(req, timeout=90) as response:
        data = response.read()
        with open(target, "wb") as f:
            f.write(data)
    print(f"Saved: {target} ({len(data)} bytes)")

for fname, prompt in PROMPTS:
    try:
        fetch(fname, prompt)
        time.sleep(2)
    except Exception as e:
        print(f"Error fetching {fname}: {e}")
