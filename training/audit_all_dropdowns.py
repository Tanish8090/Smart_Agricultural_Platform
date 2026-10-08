import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

html_path = "final sap project/final sap project/index.html"
with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

pattern = re.compile(r'<select([^>]*)>([\s\S]*?)</select>', re.IGNORECASE)
matches = pattern.findall(content)

print(f"Total <select> elements found in {html_path}: {len(matches)}")
print("=" * 80)

for attrs, body in matches:
    id_match = re.search(r'id=["\']([^"\']+)["\']', attrs)
    sel_id = id_match.group(1) if id_match else "NO_ID"
    options = re.findall(r'<option[^>]*value=["\']([^"\']*)["\'][^>]*>(.*?)</option>', body, re.DOTALL)
    is_crop = any(v in ['Wheat', 'Potato', 'Rice', 'Cotton', 'Sugarcane', 'Soybean', 'Tomato', 'Corn', 'Apple', 'Grape'] for v, _ in options)
    print(f"ID: #{sel_id:<22} | Crop Selector: {is_crop!s:<5} | Options: {len(options)}")
    if is_crop:
        print("   Values:", [v for v, _ in options])

print("\n" + "=" * 80)

