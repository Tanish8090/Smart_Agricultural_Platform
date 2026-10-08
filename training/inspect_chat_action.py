import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('final sap project/final sap project/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(3000, 3120):
    if i < len(lines):
        print(f"{i+1}: {lines[i]}", end='')
