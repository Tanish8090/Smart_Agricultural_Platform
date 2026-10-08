import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('final sap project/final sap project/translations.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines in translations.js: {len(lines)}")

# Find where crops are listed
for i, line in enumerate(lines):
    if 'crops:' in line or 'cropList' in line or 'cropOptions' in line or 'wheat:' in line.lower():
        print(f"Line {i+1}: {line.strip()[:100]}")

# Find DISEASE_TRANSLATIONS
for i, line in enumerate(lines):
    if 'DISEASE_TRANSLATIONS' in line or 'disease_info' in line or 'Potato___' in line:
        print(f"Line {i+1}: {line.strip()[:100]}")
        break
