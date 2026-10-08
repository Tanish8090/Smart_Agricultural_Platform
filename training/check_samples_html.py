import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('final sap project/final sap project/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

m = re.search(r'<!-- Sample Test Leaves Carousel \/ Grid -->[\s\S]*?<\/div>\s*<\/div>', html)
if not m:
    m = re.search(r'loadSamplePhoto[\s\S]*?<\/div>\s*<\/div>', html)

if m:
    print(m.group(0)[:1500])
else:
    # search for loadSample
    for line in html.split('\n'):
        if 'loadSample' in line or 'test photos' in line:
            print(line.strip())
