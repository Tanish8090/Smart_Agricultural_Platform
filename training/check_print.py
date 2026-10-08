import re

with open('final sap project/final sap project/index.html', 'r', encoding='utf-8') as f:
    text = f.read()
    print("Print in index.html:")
    for m in re.finditer(r'print', text, re.IGNORECASE):
        start = max(0, m.start() - 40)
        end = min(len(text), m.end() + 40)
        print("...", text[start:end].replace('\n', ' '), "...")

with open('final sap project/final sap project/styles.css', 'r', encoding='utf-8') as f:
    text = f.read()
    print("\nPrint in styles.css:")
    for m in re.finditer(r'@media print', text):
        start = max(0, m.start() - 20)
        end = min(len(text), m.end() + 200)
        print("...", text[start:end].replace('\n', ' '), "...")
