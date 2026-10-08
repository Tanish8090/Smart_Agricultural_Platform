import html.parser
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

class TranslationAuditor(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.tag_stack = []
        self.untranslated = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        has_trans = 'data-lang-en' in attr_dict or 'data-i18n' in attr_dict
        parent_has_trans = any(t.get('has_trans', False) for t in self.tag_stack)
        tag_info = {
            'tag': tag,
            'id': attr_dict.get('id', ''),
            'attrs': attr_dict,
            'has_trans': has_trans or parent_has_trans
        }
        self.tag_stack.append(tag_info)

    def handle_endtag(self, tag):
        if self.tag_stack:
            self.tag_stack.pop()

    def handle_data(self, data):
        text = data.strip()
        if not text or len(text) <= 2:
            return
        if re.match(r'^[0-9\.\,\:\%\-\+\/\°C\s\(\)]+$', text):
            return
        if self.tag_stack:
            curr = self.tag_stack[-1]
            if curr['tag'] in ['script', 'style']:
                return
            if not curr['has_trans']:
                self.untranslated.append((curr['tag'], curr['id'], text))

with open('final sap project/final sap project/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

auditor = TranslationAuditor()
auditor.feed(content)

print(f"Total untranslated text occurrences: {len(auditor.untranslated)}")
unique_texts = {}
for t, id_val, txt in auditor.untranslated:
    if txt not in unique_texts:
        unique_texts[txt] = (t, id_val)

print(f"Total unique texts: {len(unique_texts)}")
for txt, (t, id_val) in list(unique_texts.items())[:60]:
    print(f"<{t} id='{id_val}'>: {repr(txt)}")
