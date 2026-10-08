import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('www/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('id="cameraModal"')
if pos != -1:
    end_pos = text.find('</div>\n  </div>', pos)
    print(text[pos-50:end_pos+50])
