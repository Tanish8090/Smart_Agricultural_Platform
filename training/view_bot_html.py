import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('www/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('id="view-bot"')
if pos != -1:
    end_pos = text.find('</section>', pos)
    print(text[pos:end_pos+10])
