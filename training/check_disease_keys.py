import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('final sap project/final sap project/translations.js', 'r', encoding='utf-8') as f:
    content = f.read()

# find keys in DISEASE_TRANSLATIONS
m = re.search(r'const DISEASE_TRANSLATIONS = \{([\s\S]*?)\n\};', content)
if m:
    keys = re.findall(r"'([^']+)'\s*:", m.group(1))
    print(f"Total diseases in DISEASE_TRANSLATIONS: {len(keys)}")
    for k in keys:
        print(f"  {k}")
