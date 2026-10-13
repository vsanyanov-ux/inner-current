import os
import sys

scan_dirs = ["/var/www", "/app", "/opt", "/root", "/etc/nginx"]
targets = ["суперкостюм", "Инструкция к твоему", "суперкостюму"]

print("Starting scan for keywords:", targets)
found = 0
for base in scan_dirs:
    if not os.path.exists(base):
        continue
    for root, dirs, files in os.walk(base):
        for f in files:
            p = os.path.join(root, f)
            try:
                if os.path.getsize(p) > 20 * 1024 * 1024:
                    continue
                with open(p, "r", encoding="utf-8", errors="ignore") as fh:
                    content = fh.read()
                    for t in targets:
                        if t in content:
                            print(f"[MATCH] '{t}' found in: {p}")
                            found += 1
                            break
            except Exception as e:
                pass

print(f"Scan complete. Total matches: {found}")
