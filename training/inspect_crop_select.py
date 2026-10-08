import re, sys
sys.stdout.reconfigure(encoding='utf-8')
html = open('www/index.html', encoding='utf-8').read()
m = re.search(r'<select[^>]*id=["\']diseaseCropSelect["\'][^>]*>(.*?)</select>', html, re.DOTALL)
if m:
    print("Found diseaseCropSelect options:")
    for opt in re.findall(r'<option[^>]*>.*?</option>', m.group(1)):
        print("  ", opt)
else:
    print("diseaseCropSelect NOT FOUND")
