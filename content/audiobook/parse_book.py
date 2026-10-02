import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('book_outline.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect headings
lines = text.split('\n')
headings = []
for idx, line in enumerate(lines):
    if line.startswith('## ') or line.startswith('### Глава') or line.startswith('### ЧАСТЬ'):
        headings.append((idx + 1, line))

print(f"Total lines: {len(lines)}")
print(f"Found {len(headings)} main headings:")
for line_num, h in headings:
    print(f"L{line_num:04d}: {h}")
