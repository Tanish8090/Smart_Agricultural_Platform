import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('final sap project/final sap project/app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i in range(58, 77):
    print(f'{i+1}: {repr(lines[i])}')
