import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('disease_analyzer.py', 'r', encoding='utf-8') as f:
    code = f.read()

m = re.search(r'AGRONOMIC_KNOWLEDGE = \{([\s\S]*?)\n\}', code)
if m:
    keys = re.findall(r'"([^"]+)": \{', m.group(1))
    print(f"Keys in AGRONOMIC_KNOWLEDGE ({len(keys)}):")
    for k in keys:
        print(f"  {k}")
