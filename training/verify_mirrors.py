import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

keywords = [
    "Government Schemes",
    "Govt Schemes",
    "Government Scheme",
    "सरकारी योजनाएं",
    "सरकारी योजना",
    "view-schemes",
    "tab-schemes",
    "schemeDetailModal",
    "initSchemesTab"
]

all_files = [
    'final sap project/index.html',
    'final sap project/app.js',
    'final sap project/translations.js',
    'final sap project/final sap project/final sap project/index.html',
    'final sap project/final sap project/final sap project/app.js',
    'final sap project/final sap project/final sap project/translations.js',
    'translations.js'
]

found = False
for fpath in all_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    for kw in keywords:
        if kw.lower() in content.lower():
            found = True
            print(f"[!] Found '{kw}' in {fpath}")

if not found:
    print("[✓] ALL mirrored frontend directories are completely clean!")
