import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('final sap project/final sap project/translations.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'diseaseCropSelect' in line or 'headerCropSelect' in line or 'fertCropSelect' in line or 'modalCropSelect' in line:
        print(f"Line {i+1}: {line.strip()[:100]}")
