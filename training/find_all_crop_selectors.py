import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('final sap project/final sap project/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("=== SELECT ELEMENTS IN INDEX.HTML ===")
selects = re.findall(r'<select[^>]*id="([^"]*)"[^>]*>([\s\S]*?)<\/select>', html)
for sel_id, sel_body in selects:
    if any(c in sel_body.lower() for c in ['wheat', 'rice', 'cotton', 'potato', 'crop']):
        print(f"\nSelect ID: #{sel_id}")
        options = re.findall(r'<option[^>]*value="([^"]*)"[^>]*>([\s\S]*?)<\/option>', sel_body)
        for val, opt_text in options:
            clean_text = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', opt_text)).strip()
            print(f"   value='{val}': {clean_text}")

print("\n=== CROP ARRAYS / REFERENCES IN APP.JS ===")
with open('final sap project/final sap project/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Look for crop arrays or crop selector references
for m in re.finditer(r'(const|let|var)\s+([A-Za-z0-9_]*crop[A-Za-z0-9_]*)\s*=\s*(\[[^\]]*\]|\{[^\}]*\})', js, re.IGNORECASE):
    print(f"Match: {m.group(1)} {m.group(2)} = {m.group(3)[:100]}...")

# Look for populateCrop or updateCrop
for fn in ['populate', 'updateCrop', 'renderCrop', 'cropSelect']:
    matches = [line.strip() for line in js.split('\n') if fn.lower() in line.lower()]
    if matches:
        print(f"\nLines with '{fn}':")
        for line in matches[:5]:
            print(f"  {line[:100]}")
