import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('final sap project/final sap project/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Look for scanner sample chips or preset buttons
presets = re.findall(r'<button[^>]*onclick="[^"]*(?:Sample|Crop|selectCrop)[^"]*"[^>]*>([\s\S]*?)<\/button>', html)
print(f"Sample / Preset Crop Buttons: {len(presets)}")
for p in presets[:10]:
    clean = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', p)).strip()
    print("  Preset:", clean)

# Check all occurrences of 'Wheat', 'Mustard', 'Chickpea', 'Corn', 'Maize', 'Soybean', 'Soyabean' in select tags
select_blocks = re.findall(r'<select[\s\S]*?<\/select>', html)
print(f"\nTotal select elements: {len(select_blocks)}")
for idx, sb in enumerate(select_blocks):
    m_id = re.search(r'id="([^"]*)"', sb)
    id_str = m_id.group(1) if m_id else f"select_{idx}"
    opt_vals = re.findall(r'value="([^"]*)"', sb)
    if any(v in ['Wheat', 'Rice', 'Cotton', 'Auto'] for v in opt_vals):
        print(f"Crop Select #{id_str}: {opt_vals}")
