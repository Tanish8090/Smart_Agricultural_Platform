import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('final sap project/final sap project/index.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

print("--- SELECT ELEMENTS IN INDEX.HTML ---")
for m in re.finditer(r'<select[^>]*id=["\']([^"\']+)["\'][^>]*>', html):
    print("Found select id:", m.group(1), "->", m.group(0))

print("\n--- ELEMENTS WITH 'crop' IN ID OR CLASS ---")
for m in re.finditer(r'id=["\']([^"\']*crop[^"\']*)["\']', html, re.IGNORECASE):
    print("Found crop id:", m.group(1))

print("\n--- DISEASE SCANNER CARD SURROUNDINGS ---")
for m in re.finditer(r'<section[^>]*id=["\']([^"\']*(?:disease|scan)[^"\']*)["\'][^>]*>', html, re.IGNORECASE):
    print("Found scanner section:", m.group(0))

# Search for crop selector in app.js
with open('final sap project/final sap project/app.js', 'r', encoding='utf-8', errors='ignore') as f:
    js = f.read()

print("\n--- CROP SELECTOR IN APP.JS ---")
for line in js.splitlines():
    if any(k in line.lower() for k in ['cropselect', 'selectedcrop', 'crop_name', 'state.crop', 'fertcrop']):
        print("JS:", line.strip()[:100])
