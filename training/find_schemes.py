import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

keywords = ['Government Schemes', 'Govt Schemes', 'Government Scheme', 'सरकारी योजनाएं', 'सरकारी योजना', 'view-schemes', 'tab-schemes', 'scheme']

files_to_check = [
    'final sap project/final sap project/index.html',
    'final sap project/final sap project/app.js',
    'final sap project/final sap project/translations.js'
]

for file_path in files_to_check:
    print(f"\n=== Checking {file_path} ===")
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        for kw in ['Government Schemes', 'Govt Schemes', 'Government Scheme', 'सरकारी योजनाएं', 'सरकारी योजना', 'view-schemes', 'tab-schemes']:
            if kw.lower() in line.lower():
                print(f"Line {i+1}: {line.strip()[:100]}")
                break
