import os
import sys

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current"
TARGET_FILES = [
    os.path.join(ROOT_DIR, "public", "index.html"),
    os.path.join(ROOT_DIR, "dist_site", "index.html"),
    os.path.join(ROOT_DIR, "scripts", "update_index_golden_seven.py"),
    os.path.join(ROOT_DIR, "scripts", "build_new_book1_reader.py"),
]

# Map of full substring replacements (order matters: longer/specific matches first)
REPLACEMENTS = [
    # Full LaTeX blocks
    (r"$\mathcal{H} = P_{\text{load}} / P_{\text{total}}$", "H = P_load / P_total"),
    (r"$\mathcal{H} = P_{\\text{load}} / P_{\\text{total}}$", "H = P_load / P_total"),
    (r"($R_{\text{ego}} \to 0$)", "(R_ego → 0)"),
    (r"($R_{\\text{ego}} \\to 0$)", "(R_ego → 0)"),
    (r"$R_{\text{ego}} \to 0$", "R_ego → 0"),
    (r"$R_{\\text{ego}} \\to 0$", "R_ego → 0"),
    (r"Ленц $Q = I^2 R t$", "закон Джоуля — Ленца Q = I²·R·t"),
    (r"($Q = I^2 R t$)", "(Q = I²·R·t)"),
    (r"$Q = I^2 R t$", "Q = I²·R·t"),
    (r"Источник $\to$ Проводник $\to$ Нагрузка $\to$ Обратный провод", "Источник → Проводник → Нагрузка → Обратный провод"),
    (r"Источник $\\to$ Проводник $\\to$ Нагрузка $\\to$ Обратный провод", "Источник → Проводник → Нагрузка → Обратный провод"),
    (r"($N=1$)", "(N=1)"),
    (r"$N=1$", "N=1"),
    (r"($C_4$)", "(C₄)"),
    (r"$C_4$", "C₄"),
    (r"$\to$", "→"),
    (r"$\\to$", "→"),
]

for file_path in TARGET_FILES:
    if not os.path.exists(file_path):
        print(f"Skipping missing file: {file_path}")
        continue
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    changed = False
    for old, new in REPLACEMENTS:
        if old in content:
            content = content.replace(old, new)
            changed = True

    if changed:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Successfully cleaned: {file_path}")
    else:
        print(f"No changes needed: {file_path}")

print("All replacements done!")
