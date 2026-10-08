import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('final sap project/final sap project/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
for i in range(max(0, len(lines)-35), len(lines)):
    print(f"{i+1}: {lines[i]}", end='')
