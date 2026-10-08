import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('final sap project/final sap project/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Look for buttons that don't have data-lang-en or data-i18n
buttons_without_lang = re.findall(r'<button(?![^>]*data-(?:lang-en|i18n))[^>]*>(.*?)</button>', html, re.DOTALL)
print(f"Total buttons without lang attributes: {len(buttons_without_lang)}")
for b in buttons_without_lang[:10]:
    clean = re.sub(r'<[^>]+>', ' ', b).strip()
    if clean:
        print(" - Button:", clean[:60])

# Look for h1, h2, h3, h4 without lang attributes
headers = re.findall(r'<(h[1-4])(?![^>]*data-(?:lang-en|i18n))[^>]*>(.*?)</\1>', html, re.DOTALL)
print(f"Total headers without lang attributes: {len(headers)}")
for tag, text in headers[:15]:
    clean = re.sub(r'<[^>]+>', ' ', text).strip()
    if clean:
        print(f" - {tag}:", clean[:60])
