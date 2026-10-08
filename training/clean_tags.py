import re
import sys

# Ensure utf-8 output
sys.stdout.reconfigure(encoding='utf-8')

paths = [
    'final sap project/final sap project/index.html',
    'final sap project/final sap project/final sap project/index.html',
    'final sap project/index.html'
]

for p in paths:
    with open(p, 'r', encoding='utf-8') as f:
        html = f.read()

    # Clean double nested spans
    # e.g.: <span data-lang-en="Dashboard" data-lang-hi="डैशबोर्ड"><span data-lang-en="Dashboard" data-lang-hi="डैशबोर्ड">Dashboard</span></span>
    def clean_nested(m):
        full = m.group(0)
        # get inner content
        inner_m = re.search(r'>([^<]+)</span></span>$', full)
        if inner_m:
            text = inner_m.group(1)
            # extract en and hi from first tag
            en_m = re.search(r'data-lang-en="([^"]+)"', full)
            hi_m = re.search(r'data-lang-hi="([^"]+)"', full)
            en = en_m.group(1) if en_m else text
            hi = hi_m.group(1) if hi_m else text
            return f'<span data-lang-en="{en}" data-lang-hi="{hi}">{text}</span>'
        return full

    html = re.sub(r'<span\s+data-lang-en="[^"]+"\s+data-lang-hi="[^"]+">\s*<span\s+data-lang-en="[^"]+"\s+data-lang-hi="[^"]+">.*?</span>\s*</span>', clean_nested, html)

    with open(p, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Cleaned nested tags in {p}")
