import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('final sap project/final sap project/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's add data-lang-en and data-lang-hi to these specific headers and sections
ADDITIONAL_TRANSLATIONS = [
    # Forecast header
    (r'<h3 class="font-extrabold text-slate-800 dark:text-slate-100 text-sm">5-7 Day Weather Forecast</h3>',
     '<h3 class="font-extrabold text-slate-800 dark:text-slate-100 text-sm" data-lang-en="5-7 Day Weather Forecast" data-lang-hi="5-7 दिवसीय मौसम पूर्वानुमान">5-7 Day Weather Forecast</h3>'),
    
    # Mandi header
    (r'<h3 class="text-base font-extrabold text-slate-900 dark:text-white">Detailed Mandi Market Cards</h3>',
     '<h3 class="text-base font-extrabold text-slate-900 dark:text-white" data-lang-en="Detailed Mandi Market Cards" data-lang-hi="विस्तृत मंडी भाव कार्ड">Detailed Mandi Market Cards</h3>'),

    # Schemes header
    (r'<h3 class="text-base font-extrabold text-slate-900 dark:text-white">Available Government Schemes</h3>',
     '<h3 class="text-base font-extrabold text-slate-900 dark:text-white" data-lang-en="Available Government Schemes" data-lang-hi="उपलब्ध सरकारी योजनाएं">Available Government Schemes</h3>'),

    # Footer headers
    (r'<h4 class="font-extrabold text-white text-xs uppercase tracking-wider">Platform Modules</h4>',
     '<h4 class="font-extrabold text-white text-xs uppercase tracking-wider" data-lang-en="Platform Modules" data-lang-hi="प्लेटफॉर्म मॉड्यूल">Platform Modules</h4>'),
    
    (r'<h4 class="font-extrabold text-white text-xs uppercase tracking-wider">Verified Sources</h4>',
     '<h4 class="font-extrabold text-white text-xs uppercase tracking-wider" data-lang-en="Verified Sources" data-lang-hi="प्रमाणित स्रोत">Verified Sources</h4>'),

    # AI Kisan Bot header
    (r'<h2 class="text-lg font-extrabold text-slate-900 dark:text-white">AI Kisan Assistant</h2>',
     '<h2 class="text-lg font-extrabold text-slate-900 dark:text-white" data-lang-en="AI Kisan Assistant" data-lang-hi="एआई किसान सहायक">AI Kisan Assistant</h2>'),

    # Disclaimer
    (r'<span>⚠ Advisory Disclaimer</span>',
     '<span data-lang-en="⚠ Advisory Disclaimer" data-lang-hi="⚠ सलाह अस्वीकरण">⚠ Advisory Disclaimer</span>'),
    (r'<p class="leading-relaxed">\s*AI recommendations and market information are decision-support tools\. Verify critical agricultural decisions with local agricultural authorities and official sources\.\s*</p>',
     '<p class="leading-relaxed" data-lang-en="AI recommendations and market information are decision-support tools. Verify critical agricultural decisions with local agricultural authorities and official sources." data-lang-hi="एआई सिफारिशें और बाजार जानकारी निर्णय-समर्थन उपकरण हैं। महत्वपूर्ण कृषि निर्णयों को स्थानीय कृषि अधिकारियों और आधिकारिक स्रोतों से सत्यापित करें।">AI recommendations and market information are decision-support tools. Verify critical agricultural decisions with local agricultural authorities and official sources.</p>'),

    # Weather IMD Advisory card
    (r'<span class="text-xs font-bold text-amber-900 dark:text-amber-200 uppercase tracking-wide">Agri-Weather Advisory</span>',
     '<span class="text-xs font-bold text-amber-900 dark:text-amber-200 uppercase tracking-wide" data-lang-en="Agri-Weather Advisory" data-lang-hi="कृषि-मौसम सलाह">Agri-Weather Advisory</span>'),

    # Spray conditions
    (r'<span class="font-bold text-slate-700 dark:text-slate-300">Pesticide / Spray Window</span>',
     '<span class="font-bold text-slate-700 dark:text-slate-300" data-lang-en="Pesticide / Spray Window" data-lang-hi="कीटनाशक / छिड़काव अनुकूलता">Pesticide / Spray Window</span>'),

    # Mandi filters
    (r'<label class="text-xs font-semibold text-slate-600 dark:text-slate-400 block mb-1">Select Crop</label>',
     '<label class="text-xs font-semibold text-slate-600 dark:text-slate-400 block mb-1" data-lang-en="Select Crop" data-lang-hi="फसल चुनें">Select Crop</label>'),
    (r'<label class="text-xs font-semibold text-slate-600 dark:text-slate-400 block mb-1">Search Radius</label>',
     '<label class="text-xs font-semibold text-slate-600 dark:text-slate-400 block mb-1" data-lang-en="Search Radius" data-lang-hi="खोज दायरा">Search Radius</label>'),
    (r'<label class="text-xs font-semibold text-slate-600 dark:text-slate-400 block mb-1">Sort By</label>',
     '<label class="text-xs font-semibold text-slate-600 dark:text-slate-400 block mb-1" data-lang-en="Sort By" data-lang-hi="क्रमबद्ध करें">Sort By</label>')
]

for pat, repl in ADDITIONAL_TRANSLATIONS:
    html = re.sub(pat, repl, html)

paths = [
    'final sap project/final sap project/index.html',
    'final sap project/final sap project/final sap project/index.html',
    'final sap project/index.html'
]
for p in paths:
    with open(p, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Updated {p}")

print("Added additional section and header translations!")
