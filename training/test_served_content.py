import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("Fetching http://localhost:8080/ ...")
res = urllib.request.urlopen('http://localhost:8080/')
html = res.read().decode('utf-8')
print('HTTP / status:', res.status, 'HTML length:', len(html))

keywords = ['Government Schemes', 'Govt Schemes', 'Government Scheme', 'सरकारी योजनाएं', 'सरकारी योजना', 'view-schemes', 'tab-schemes', 'schemeDetailModal']
for kw in keywords:
    matches = len(re.findall(re.escape(kw), html, re.IGNORECASE))
    print(f'Keyword in served HTML "{kw}": {matches}')

print("\nFetching http://localhost:8080/app.js ...")
res_js = urllib.request.urlopen('http://localhost:8080/app.js')
js = res_js.read().decode('utf-8')
print('HTTP /app.js status:', res_js.status, 'JS length:', len(js))
for kw in keywords:
    matches = len(re.findall(re.escape(kw), js, re.IGNORECASE))
    print(f'Keyword in served JS "{kw}": {matches}')

print("\nFetching http://localhost:8080/translations.js ...")
res_tr = urllib.request.urlopen('http://localhost:8080/translations.js')
tr = res_tr.read().decode('utf-8')
print('HTTP /translations.js status:', res_tr.status, 'Translations length:', len(tr))
for kw in keywords:
    matches = len(re.findall(re.escape(kw), tr, re.IGNORECASE))
    print(f'Keyword in served translations "{kw}": {matches}')
