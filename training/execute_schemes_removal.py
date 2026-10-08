import re
import sys
import shutil

sys.stdout.reconfigure(encoding='utf-8')

print("Starting removal of Government Schemes feature...")

# -----------------------------------------------------------------------------
# 1. Update index.html
# -----------------------------------------------------------------------------
index_path = 'final sap project/final sap project/index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

original_html_len = len(html)

# 1.1 Remove top navbar tab
nav_btn_pattern = r'(\s*<button onclick="switchTab\(\'schemes\'\)" id="tab-schemes"[^>]*>[\s\S]*?<\/button>)'
html, count1 = re.subn(nav_btn_pattern, '', html, count=1)
print(f"1.1 Top navbar tab removed: {count1 == 1}")

# 1.2 Remove mobile drawer button
mobile_btn_pattern = r'(\s*<button onclick="switchTab\(\'schemes\'\); toggleMobileMenu\(\)"[^>]*>[\s\S]*?<\/button>)'
html, count2 = re.subn(mobile_btn_pattern, '', html, count=1)
print(f"1.2 Mobile menu button removed: {count2 == 1}")

# 1.3 Remove hero quick bar button
hero_btn_pattern = r'(\s*<button onclick="switchTab\(\'schemes\'\)" class="bg-white\/10[^>]*>[\s\S]*?<\/button>)'
html, count3 = re.subn(hero_btn_pattern, '', html, count=1)
print(f"1.3 Hero quick bar button removed: {count3 == 1}")

# 1.4 Remove Dashboard Card 5 (Government Schemes & Subsidies Widget)
card5_pattern = r'(\s*<!-- 5\. Government Schemes & Subsidies Widget -->[\s\S]*?<\/button>\s*<\/div>)'
html, count4 = re.subn(card5_pattern, '', html, count=1)
print(f"1.4 Dashboard Card 5 removed: {count4 == 1}")

# 1.5 Update Card 6 subsidy prompt to pest control prompt
card6_sub_pattern = r'<button onclick="sendQuickPrompt\(\'मुझे ट्रैक्टर और कृषि यंत्रों पर 50% सब्सिडी कैसे मिलेगी\?\'\)"[^>]*>[\s\S]*?<\/button>'
replacement_prompt = '''<button onclick="sendQuickPrompt('फसल में कीट लगने पर कौन सी दवा डालें?')" class="text-left text-[11px] font-semibold bg-violet-50/60 dark:bg-violet-950/40 hover:bg-violet-100 text-violet-800 dark:text-violet-200 px-3 py-1.5 rounded-xl border border-violet-200 dark:border-violet-800 transition truncate">
                  🐛 फसल में कीट लगने पर रोकथाम कैसे करें?
                </button>'''
html, count5 = re.subn(card6_sub_pattern, replacement_prompt, html, count=1)
print(f"1.5 Card 6 prompt updated: {count5 == 1}")

# 1.6 Remove Chat suggested chip in HTML
chat_chip_pattern = r'(\s*<button onclick="sendQuickPrompt\(\'What government agriculture schemes can I apply for\?\'\)"[^>]*>[\s\S]*?<\/button>)'
html, count6 = re.subn(chat_chip_pattern, '', html, count=1)
print(f"1.6 Chat chip in HTML removed: {count6 == 1}")

# 1.7 Remove Schemes view section (#view-schemes) and Scheme Details Modal (#schemeDetailModal)
view_modal_pattern = r'(\s*<!-- ═+\s*GOVERNMENT SCHEMES MODULE \(#view-schemes\)[\s\S]*?<\/div>\s*<\/div>\s*)(?=\s*<!-- ═+\s*MANDI MARKET DETAILS)'
html, count7 = re.subn(view_modal_pattern, '\n\n', html, count=1)
print(f"1.7 Schemes view and modal removed: {count7 == 1}")

# 1.8 Remove Footer icon button
footer_icon_pattern = r'(\s*<button onclick="switchTab\(\'schemes\'\)" title="Govt Schemes"[^>]*>[\s\S]*?<\/button>)'
html, count8 = re.subn(footer_icon_pattern, '', html, count=1)
print(f"1.8 Footer icon removed: {count8 == 1}")

# 1.9 Remove Footer module list item
footer_mod_pattern = r'(\s*<li><button onclick="switchTab\(\'schemes\'\)"[^>]*>[\s\S]*?<\/button><\/li>)'
html, count9 = re.subn(footer_mod_pattern, '', html, count=1)
print(f"1.9 Footer module item removed: {count9 == 1}")

# 1.10 Remove Footer verified source
footer_source_pattern = r'(\s*<div>\s*<span class="font-bold text-white block">Schemes<\/span>\s*<span>myScheme\.gov\.in \/ official government portals<\/span>\s*<\/div>)'
html, count10 = re.subn(footer_source_pattern, '', html, count=1)
print(f"1.10 Footer source removed: {count10 == 1}")

# 1.11 Update Footer description text
footer_desc_pattern = r', and welfare schemes\.'
html, count11 = re.subn(footer_desc_pattern, '.', html)
print(f"1.11 Footer description updated: {count11 == 2}") # en attribute and text content

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"index.html saved ({original_html_len} -> {len(html)} bytes)")


# -----------------------------------------------------------------------------
# 2. Update app.js
# -----------------------------------------------------------------------------
app_path = 'final sap project/final sap project/app.js'
with open(app_path, 'r', encoding='utf-8') as f:
    js = f.read()

original_js_len = len(js)

# 2.1 Remove schemesState declaration
schemes_state_pat = r'(\/\/\s*───\s*Government Schemes State\s*───+[\s\S]*?selectedScheme:\s*null,\s*\};\s*)'
js, count2_1 = re.subn(schemes_state_pat, '', js, count=1)
print(f"2.1 schemesState removed: {count2_1 == 1}")

# 2.2 Remove switchTab schemes branch
switch_tab_pat = r'(\s*\}\s*else if\s*\(\s*tabId\s*===\s*\'schemes\'\s*\)\s*\{[\s\S]*?initSchemesTab\(\);\s*\}\s*\})'
js, count2_2 = re.subn(switch_tab_pat, '', js, count=1)
print(f"2.2 switchTab schemes removed: {count2_2 == 1}")

# 2.3 Remove Schemes engine block
schemes_engine_pat = r'(\/\/\s*═+\s*\n\/\/\s*GOVERNMENT SCHEMES ENGINE \(TAB 5\)[\s\S]*?)(?=\/\/\s*───\s*AI Disease Scanner Frontend Engine \(Tab 2\))'
js, count2_3 = re.subn(schemes_engine_pat, '', js, count=1)
print(f"2.3 Schemes engine removed: {count2_3 == 1}")

# 2.4 Remove CHAT_SUGGESTED_CHIPS schemes item
chat_chips_schemes_pat = r'(\s*,\s*\{\s*icon:\s*\'🏛\',\s*enLabel:\s*\'Govt schemes\',\s*hiLabel:\s*\'सरकारी योजनाएं\',\s*enPrompt:\s*\'[^\']*\',\s*hiPrompt:\s*\'[^\']*\'\s*\})'
js, count2_4 = re.subn(chat_chips_schemes_pat, '', js, count=1)
print(f"2.4 CHAT_SUGGESTED_CHIPS schemes item removed: {count2_4 == 1}")

# 2.5 Remove Chat message scheme action button
chat_action_pat = r'(\s*if\s*\(\s*msg\.intent\s*===\s*\'scheme\'[\s\S]*?<\/button>\s*`;\s*\})'
js, count2_5 = re.subn(chat_action_pat, '', js, count=1)
print(f"2.5 Chat scheme action button removed: {count2_5 == 1}")

# 2.6 Remove closeSchemeDetailModal() in escape listener
escape_pat = r'(\s*closeSchemeDetailModal\(\);)'
js, count2_6 = re.subn(escape_pat, '', js, count=1)
print(f"2.6 closeSchemeDetailModal() removed: {count2_6 == 1}")

# 2.7 Remove 'schemeDetailModal', in modal click list
modal_click_pat = r"('schemeDetailModal',\s*)"
js, count2_7 = re.subn(modal_click_pat, '', js, count=1)
print(f"2.7 schemeDetailModal in modal click list removed: {count2_7 == 1}")

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(js)
print(f"app.js saved ({original_js_len} -> {len(js)} bytes)")


# -----------------------------------------------------------------------------
# 3. Update translations.js
# -----------------------------------------------------------------------------
trans_path = 'final sap project/final sap project/translations.js'
with open(trans_path, 'r', encoding='utf-8') as f:
    tjs = f.read()

original_tjs_len = len(tjs)

# 3.1 Remove English governmentSchemes key
en_key_pat = r'(\s*governmentSchemes:\s*\'Government Schemes\',)'
tjs, count3_1 = re.subn(en_key_pat, '', tjs, count=1)
print(f"3.1 en governmentSchemes key removed: {count3_1 == 1}")

# 3.2 Remove English schemes module section
en_mod_pat = r'(\s*\/\/\s*Schemes Module[\s\S]*?stateGovt:\s*\'State Govt\',)'
tjs, count3_2 = re.subn(en_mod_pat, '', tjs, count=1)
print(f"3.2 en schemes module removed: {count3_2 == 1}")

# 3.3 Remove Hindi governmentSchemes key
hi_key_pat = r'(\s*governmentSchemes:\s*\'सरकारी योजनाएं\',)'
tjs, count3_3 = re.subn(hi_key_pat, '', tjs, count=1)
print(f"3.3 hi governmentSchemes key removed: {count3_3 == 1}")

# 3.4 Remove Hindi schemes module section
hi_mod_pat = r'(\s*\/\/\s*Schemes Module[\s\S]*?stateGovt:\s*\'राज्य सरकार\',)'
tjs, count3_4 = re.subn(hi_mod_pat, '', tjs, count=1)
print(f"3.4 hi schemes module removed: {count3_4 == 1}")

# 3.5 Remove schemeSearchInput in applyTranslations
input_pat = r'(\s*const schemeSearchInput = document\.getElementById\(\'schemeSearchInput\'\);[\s\S]*?schemeSearchInput\.placeholder = t\(\'searchSchemesPlaceholder\'\);\s*\})'
tjs, count3_5 = re.subn(input_pat, '', tjs, count=1)
print(f"3.5 schemeSearchInput removed from translations.js: {count3_5 == 1}")

with open(trans_path, 'w', encoding='utf-8') as f:
    f.write(tjs)
print(f"translations.js saved ({original_tjs_len} -> {len(tjs)} bytes)")


# -----------------------------------------------------------------------------
# 4. Sync to mirrored directories
# -----------------------------------------------------------------------------
targets = [
    'final sap project',
    'final sap project/final sap project/final sap project'
]

for tgt in targets:
    shutil.copyfile(index_path, f"{tgt}/index.html")
    shutil.copyfile(app_path, f"{tgt}/app.js")
    shutil.copyfile(trans_path, f"{tgt}/translations.js")
    print(f"Synced changes to {tgt}/")

shutil.copyfile(trans_path, "translations.js")
print("Synced translations.js to root directory")

print("All modifications successfully completed!")
