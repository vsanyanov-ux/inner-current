# -*- coding: utf-8 -*-
"""
Injects /assets/tracker.js before </body> into all HTML pages in public/ and dist_site/
"""
import os
import sys

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

TRACKER_TAG = '<script src="/assets/tracker.js" defer></script>'

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_DIRS = [
    os.path.join(ROOT_DIR, 'public'),
    os.path.join(ROOT_DIR, 'dist_site')
]

EXCLUDE_FILES = {'admin.html'}

def inject_in_dir(directory):
    if not os.path.exists(directory):
        return
    count = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.html') and file.lower() not in EXCLUDE_FILES:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    if 'tracker.js' in content:
                        continue

                    if '</body>' in content:
                        new_content = content.replace('</body>', f'  {TRACKER_TAG}\n</body>')
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        count += 1
                        rel = os.path.relpath(file_path, ROOT_DIR)
                        print(f"  [+] Injected tracker into: {rel}")
                except Exception as e:
                    print(f"  [!] Error processing {file_path}: {e}")
    print(f"Total updated in {os.path.basename(directory)}: {count} files.")

if __name__ == '__main__':
    print("=== ⚡ Injecting High-Precision Telemetry Tracker ===")
    for d in TARGET_DIRS:
        inject_in_dir(d)
    print("=== ✅ Tracker Injection Complete! ===")
