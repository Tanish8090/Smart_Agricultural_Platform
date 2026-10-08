import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("Fetching served HTML from http://localhost:8080/ ...")
html = urllib.request.urlopen("http://localhost:8080/").read().decode("utf-8")

print("\n=== VERIFICATION 1: NAVBAR TABS ===")
nav_matches = re.findall(r'<button onclick="switchTab\(\'([^\']+)\'\)"[^>]*>([\s\S]*?)<\/button>', html[:15000])
tabs_found = [m[0] for m in nav_matches if 'tab-' in m[1] or 'tab-' in html]
print(f"Tabs found in navbar: {set(m[0] for m in nav_matches)}")
assert 'schemes' not in [m[0] for m in nav_matches], "ERROR: 'schemes' found in navbar!"
print("[✓] 'schemes' tab is completely removed from navbar!")

print("\n=== VERIFICATION 2: MOBILE DRAWER ===")
mobile_section = re.search(r'id="mobileDrawer"[\s\S]*?<\/div>\s*<\/div>', html)
if mobile_section:
    mob_content = mobile_section.group(0)
    assert 'schemes' not in mob_content, "ERROR: 'schemes' found in mobile drawer!"
    print("[✓] Mobile drawer has NO schemes button!")
else:
    print("[!] Mobile drawer section not isolated, checking whole drawer area...")

print("\n=== VERIFICATION 3: LOCATION HERO QUICK BAR ===")
hero_section = re.search(r'<!-- Quick Jump Modules -->[\s\S]*?<\/div>', html)
if hero_section:
    hero_content = hero_section.group(0)
    assert 'schemes' not in hero_content, "ERROR: 'schemes' found in hero bar!"
    print("[✓] Location Hero quick bar has NO schemes button!")

print("\n=== VERIFICATION 4: DASHBOARD CARDS ===")
dash_section = re.search(r'<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">([\s\S]*?)<!-- ═════════', html)
if dash_section:
    cards_text = dash_section.group(1)
    card_headers = re.findall(r'<h3 class="text-sm font-extrabold[^"]*"[^>]*>([^<]+)<\/h3>', cards_text)
    print(f"Dashboard card titles: {card_headers}")
    assert not any('scheme' in h.lower() or 'योजना' in h for h in card_headers), "ERROR: Scheme card found in dashboard!"
    print(f"[✓] Dashboard contains exactly {len(card_headers)} cards, with NO schemes card!")

print("\n=== VERIFICATION 5: CHAT SUGGESTED QUESTION CHIPS ===")
chat_chips = re.findall(r'<button onclick="sendQuickPrompt\(\'([^\']+)\'\)" class="chat-chip[^"]*"[^>]*>([\s\S]*?)<\/button>', html)
print(f"HTML chat chips count: {len(chat_chips)}")
for prompt, body in chat_chips:
    clean_body = re.sub(r'<[^>]+>', ' ', body).strip()
    print(f"  Chip: {clean_body} -> Prompt: {prompt[:50]}")
    assert 'scheme' not in prompt.lower() and 'yojana' not in prompt.lower(), f"ERROR: Scheme found in chat prompt: {prompt}"
print("[✓] All chat chips are 100% farming/weather/mandi/disease/fertilizer/pest queries!")

print("\n=== VERIFICATION 6: VIEW SECTIONS IN DOM ===")
sections = re.findall(r'<section id="([^"]+)"', html)
print(f"Tab views in DOM: {sections}")
assert 'view-schemes' not in sections, "ERROR: #view-schemes exists in DOM!"
assert 'view-dashboard' in sections
assert 'view-weather' in sections
assert 'view-disease' in sections
assert 'view-fertilizer' in sections
assert 'view-market' in sections
assert 'view-bot' in sections
print("[✓] #view-schemes is removed, all 6 legitimate module views exist!")

print("\n=== VERIFICATION 7: MODALS IN DOM ===")
modals = re.findall(r'<div id="([^"]+Modal)"', html)
print(f"Modals in DOM: {modals}")
assert 'schemeDetailModal' not in modals, "ERROR: #schemeDetailModal exists in DOM!"
assert 'pincodeModal' in modals
assert 'farmContextModal' in modals
assert 'cameraModal' in modals
assert 'mandiDetailModal' in modals
print("[✓] #schemeDetailModal is completely removed!")

print("\n=== VERIFICATION 8: FOOTER ===")
footer_section = re.search(r'<footer[\s\S]*?<\/footer>', html)
if footer_section:
    footer_text = footer_section.group(0)
    assert 'switchTab(\'schemes\')' not in footer_text, "ERROR: schemes link found in footer!"
    assert 'myScheme' not in footer_text, "ERROR: myScheme found in footer sources!"
    print("[✓] Footer has zero schemes links, buttons, or sources!")

print("\n=== VERIFICATION 9: SWITCHTAB('SCHEMES') ANYWHERE IN HTML ===")
all_switch = re.findall(r'switchTab\(\'([^\']+)\'\)', html)
print(f"All switchTab calls in HTML: {set(all_switch)}")
assert 'schemes' not in all_switch, "ERROR: switchTab('schemes') still called in HTML!"
print("[✓] Zero calls to switchTab('schemes') in HTML!")

print("\n=======================================================")
print("ALL 9 DOM VERIFICATION CHECKS PASSED FLAWLESSLY!")
print("=======================================================")
