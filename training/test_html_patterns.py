import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('final sap project/final sap project/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Top Navbar button
nav_btn_pattern = r'(\s*<button onclick="switchTab\(\'schemes\'\)" id="tab-schemes"[^>]*>[\s\S]*?<\/button>)'
m1 = re.search(nav_btn_pattern, html)
print("1. Nav btn found:", bool(m1))

# 2. Mobile menu button
mobile_btn_pattern = r'(\s*<button onclick="switchTab\(\'schemes\'\); toggleMobileMenu\(\)"[^>]*>[\s\S]*?<\/button>)'
m2 = re.search(mobile_btn_pattern, html)
print("2. Mobile btn found:", bool(m2))

# 3. Hero quick bar button
hero_btn_pattern = r'(\s*<button onclick="switchTab\(\'schemes\'\)" class="bg-white\/10[^>]*>[\s\S]*?<\/button>)'
m3 = re.search(hero_btn_pattern, html)
print("3. Hero btn found:", bool(m3))

# 4. Dashboard Card 5
card5_pattern = r'(\s*<!-- 5\. Government Schemes & Subsidies Widget -->[\s\S]*?<\/button>\s*<\/div>)'
m4 = re.search(card5_pattern, html)
print("4. Card 5 found:", bool(m4))

# 5. Dashboard Card 6 subsidy prompt
card6_sub_pattern = r'<button onclick="sendQuickPrompt\(\'मुझे ट्रैक्टर और कृषि यंत्रों पर 50% सब्सिडी कैसे मिलेगी\?\'\)"[^>]*>[\s\S]*?<\/button>'
m5 = re.search(card6_sub_pattern, html)
print("5. Card 6 subsidy prompt found:", bool(m5))

# 6. Chat suggested chip in HTML
chat_chip_pattern = r'(\s*<button onclick="sendQuickPrompt\(\'What government agriculture schemes can I apply for\?\'\)"[^>]*>[\s\S]*?<\/button>)'
m6 = re.search(chat_chip_pattern, html)
print("6. Chat chip in HTML found:", bool(m6))

# 7. Schemes view and modal
view_modal_pattern = r'(\s*<!-- ═+\s*GOVERNMENT SCHEMES MODULE \(#view-schemes\)[\s\S]*?<\/div>\s*<\/div>\s*)(?=\s*<!-- ═+\s*MANDI MARKET DETAILS)'
m7 = re.search(view_modal_pattern, html)
print("7. Schemes view & modal found:", bool(m7))

# 8. Footer icon button
footer_icon_pattern = r'(\s*<button onclick="switchTab\(\'schemes\'\)" title="Govt Schemes"[^>]*>[\s\S]*?<\/button>)'
m8 = re.search(footer_icon_pattern, html)
print("8. Footer icon found:", bool(m8))

# 9. Footer module list item
footer_mod_pattern = r'(\s*<li><button onclick="switchTab\(\'schemes\'\)"[^>]*>[\s\S]*?<\/button><\/li>)'
m9 = re.search(footer_mod_pattern, html)
print("9. Footer module item found:", bool(m9))

# 10. Footer verified source
footer_source_pattern = r'(\s*<div>\s*<span class="font-bold text-white block">Schemes<\/span>\s*<span>myScheme\.gov\.in \/ official government portals<\/span>\s*<\/div>)'
m10 = re.search(footer_source_pattern, html)
print("10. Footer source found:", bool(m10))

# 11. Footer description text
footer_desc_pattern = r', and welfare schemes\.'
m11 = re.search(footer_desc_pattern, html)
print("11. Footer desc found:", bool(m11))
