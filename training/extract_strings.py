import html.parser
import re
import json

class TextExtractor(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.tag_stack = []
        self.texts = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        has_trans = 'data-lang-en' in attr_dict or 'data-i18n' in attr_dict
        parent_has_trans = any(t.get('has_trans', False) for t in self.tag_stack)
        self.tag_stack.append({
            'tag': tag,
            'id': attr_dict.get('id', ''),
            'has_trans': has_trans or parent_has_trans
        })

    def handle_endtag(self, tag):
        if self.tag_stack:
            self.tag_stack.pop()

    def handle_data(self, data):
        text = data.strip()
        if not text or len(text) <= 2:
            return
        if re.match(r'^[0-9\.\,\:\%\-\+\/\°C\s\(\)\₹\▲\▼]+$', text):
            return
        if self.tag_stack:
            curr = self.tag_stack[-1]
            if curr['tag'] in ['script', 'style']:
                return
            if not curr['has_trans']:
                self.texts.append(text)

with open('final sap project/final sap project/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

extractor = TextExtractor()
extractor.feed(content)

unique_texts = sorted(list(set(extractor.texts)))
print(f"Total unique texts to translate: {len(unique_texts)}")
with open('training/untranslated_strings.json', 'w', encoding='utf-8') as f:
    json.dump(unique_texts, f, ensure_ascii=False, indent=2)

print("Saved untranslated_strings.json")
