import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('final sap project/final sap project/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('id="diseaseResultContainer"')
if start != -1:
    end = html.find('<!-- Tab 4: Fertilizer Advisor Tab -->', start)
    if end == -1:
        end = start + 5000
    diag_html = html[start:end]
    print("Found diseaseResultContainer (length:", len(diag_html), ")")
    # write to a temporary file to inspect cleanly
    with open('training/diag_section.html', 'w', encoding='utf-8') as df:
        df.write(diag_html)
    print("Saved to training/diag_section.html")
