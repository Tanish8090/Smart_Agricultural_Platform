import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('final sap project/final sap project/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. schemesState declaration
schemes_state_pat = r'(\/\/\s*───\s*Government Schemes State\s*───+[\s\S]*?selectedScheme:\s*null,\s*\};\s*)'
m1 = re.search(schemes_state_pat, js)
print("1. schemesState in app.js:", bool(m1))
