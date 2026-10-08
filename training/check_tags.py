import re

with open('final sap project/final sap project/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Check for nested data-lang-en spans like <span data-lang-en=...><span data-lang-en=...>
nested = re.findall(r'(<span[^>]*data-lang-en[^>]*>\s*<span[^>]*data-lang-en[^>]*>.*?</span>\s*</span>)', content, re.DOTALL)
print(f"Nested data-lang-en spans: {len(nested)}")
if nested:
    print("Sample nested:", nested[0][:100])

# Check for data-lang-en containing <i
icons_inside = re.findall(r'(<[^>]*data-lang-en[^>]*>[^<]*<i\s+[^>]*>.*?</span>)', content, re.DOTALL)
print(f"Elements with data-lang-en containing <i>: {len(icons_inside)}")
if icons_inside:
    print("Sample with icon:", icons_inside[0][:100])
