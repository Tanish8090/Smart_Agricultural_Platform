import re

with open('www/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

print("Modal elements found:")
for m in re.finditer(r'<div[^>]*id=["\']([^"\']*[Mm]odal[^"\']*)["\'][^>]*>', text):
    print(m.group(0)[:150])

print("\nCamera related elements:")
for m in re.finditer(r'<div[^>]*id=["\']([^"\']*[Cc]amera[^"\']*)["\'][^>]*>', text):
    print(m.group(0)[:150])
