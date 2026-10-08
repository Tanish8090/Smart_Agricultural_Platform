import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. Update index.html to add id="chatTypingText"
index_paths = [
    'final sap project/final sap project/index.html',
    'final sap project/final sap project/final sap project/index.html',
    'final sap project/index.html'
]

for p in index_paths:
    with open(p, 'r', encoding='utf-8') as f:
        html = f.read()

    # Add id="chatTypingText"
    html = re.sub(
        r'<span class="text-xs" data-lang-en="AI Kisan is thinking"[^>]*>.*?</span>',
        '<span id="chatTypingText" class="text-xs" data-lang-en="AI Kisan is thinking..." data-lang-hi="उत्तर तैयार किया जा रहा है...">AI Kisan is thinking...</span>',
        html
    )

    with open(p, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Updated typing indicator in {p}")

# 2. Update translations.js to call renderChatSuggestedChips()
trans_paths = [
    'translations.js',
    'final sap project/translations.js',
    'final sap project/final sap project/translations.js',
    'final sap project/final sap project/final sap project/translations.js'
]

for p in trans_paths:
    with open(p, 'r', encoding='utf-8') as f:
        tcode = f.read()

    if 'renderChatSuggestedChips' not in tcode:
        tcode = tcode.replace(
            "if (typeof updateLocationHeroUI === 'function') updateLocationHeroUI();",
            "if (typeof updateLocationHeroUI === 'function') updateLocationHeroUI();\n  if (typeof renderChatSuggestedChips === 'function') renderChatSuggestedChips();"
        )
        with open(p, 'w', encoding='utf-8') as f:
            f.write(tcode)
        print(f"Added renderChatSuggestedChips to {p}")
    else:
        print(f"renderChatSuggestedChips already in {p}")

print("Index and Translations updated!")
