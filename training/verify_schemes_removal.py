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

files_to_check = [
    'final sap project/final sap project/index.html',
    'final sap project/final sap project/app.js',
    'final sap project/final sap project/translations.js',
    'final sap project/final sap project/styles.css'
]

print("=== CHECK 1: STRICT KEYWORD SEARCH ===")
found_any = False
for fpath in files_to_check:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    for kw in keywords:
        matches = list(re.finditer(re.escape(kw), content, re.IGNORECASE))
        if matches:
            found_any = True
            print(f"[!] FOUND '{kw}' in {fpath}: {len(matches)} occurrences")
            for m in matches[:5]:
                start = max(0, m.start() - 30)
                end = min(len(content), m.end() + 30)
                print(f"    Snippet: ...{content[start:end].replace(chr(10), ' ')}...")

if not found_any:
    print("[✓] SUCCESS: Zero occurrences of any target keyword found in frontend source files!")

print("\n=== CHECK 2: GENERAL 'scheme' & 'योजना' AUDIT ===")
for fpath in files_to_check:
    print(f"\n--- Checking {fpath} ---")
    with open(fpath, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f):
            if re.search(r'scheme|योजना', line, re.IGNORECASE):
                print(f"Line {idx+1}: {line.strip()[:100]}")
