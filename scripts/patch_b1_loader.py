# -*- coding: utf-8 -*-
import os

with open('build_golden_seven_books.py', 'r', encoding='utf-8') as f:
    text = f.read()

replacement = """print("Syncing Book 1: Универсальный закон потоковых систем (Master Unabridged Edition)...")

# -------------------------------------------------------------
# BOOK 1: Универсальный закон потоковых систем
# -------------------------------------------------------------
b1_master_path = os.path.join(WIKI_DIR, "Книга — Универсальный закон потоковых систем (Термодинамика негэнтропии, открытые системы и КПД бытия).md")
if not os.path.exists(b1_master_path):
    b1_master_path = os.path.join(LIB_DIR, "03 — Владимир Аньянов — Универсальный закон потоковых систем (Термодинамика негэнтропии, открытые системы и КПД бытия).md")

with open(b1_master_path, "r", encoding="utf-8") as f:
    b1_content = f.read()

b1_path_wiki = os.path.join(WIKI_DIR, "Книга — Универсальный закон потоковых систем (Термодинамика негэнтропии, открытые системы и КПД бытия).md")
with open(b1_path_wiki, "w", encoding="utf-8") as f:
    f.write(b1_content)
print("Saved Book 1 to Wiki:", b1_path_wiki)

b1_path_lib = os.path.join(LIB_DIR, "01 — Владимир Аньянов — Универсальный закон потоковых систем (Термодинамика негэнтропии, открытые системы и КПД бытия).md")
with open(b1_path_lib, "w", encoding="utf-8") as f:
    f.write(b1_content)
print("Saved Book 1 to Library:", b1_path_lib)

b1_path_lib3 = os.path.join(LIB_DIR, "03 — Владимир Аньянов — Универсальный закон потоковых систем (Термодинамика негэнтропии, открытые системы и КПД бытия).md")
with open(b1_path_lib3, "w", encoding="utf-8") as f:
    f.write(b1_content)
print("Saved Book 1 (as 03) to Library:", b1_path_lib3)
"""

start_str = 'print("Assembling Book 1: Универсальный закон потоковых систем...")'
end_str = 'print("Saved Book 1 (as 03) to Library:", b1_path_lib3)\n'

idx_start = text.find(start_str)
idx_end = text.find(end_str) + len(end_str)

if idx_start != -1 and idx_end != -1:
    new_text = text[:idx_start] + replacement + text[idx_end:]
    with open('build_golden_seven_books.py', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("Successfully patched build_golden_seven_books.py!")
else:
    print(f"Could not find indices: start={idx_start}, end={idx_end}")
