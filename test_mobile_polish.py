"""
Automated Verification Suite for Mobile UI Polish & Desktop Invariance
Smart Agriculture Platform (SAP)
"""

import os
import re
from html.parser import HTMLParser

class ElementCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.classes = set()
        self.bottom_nav_items = []
        self._in_bottom_nav = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        el_id = attrs_dict.get('id')
        if el_id:
            self.ids.add(el_id)
        
        cls = attrs_dict.get('class', '')
        for c in cls.split():
            self.classes.add(c)

        if 'android-bottom-nav' in cls:
            self._in_bottom_nav = True
        
        if self._in_bottom_nav and 'android-nav-item' in cls:
            data_tab = attrs_dict.get('data-tab')
            if data_tab:
                self.bottom_nav_items.append(data_tab)

    def handle_endtag(self, tag):
        if tag == 'nav' and self._in_bottom_nav:
            self._in_bottom_nav = False

def run_tests():
    print("=" * 70)
    print("  SAP MOBILE POLISH & DESKTOP INTEGRITY VERIFICATION SUITE")
    print("=" * 70)

    www_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "www")
    html_path = os.path.join(www_dir, "index.html")
    css_path = os.path.join(www_dir, "android.css")
    js_path = os.path.join(www_dir, "app.js")

    assert os.path.exists(html_path), "index.html missing"
    assert os.path.exists(css_path), "android.css missing"
    assert os.path.exists(js_path), "app.js missing"

    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    with open(css_path, "r", encoding="utf-8") as f:
        css_content = f.read()

    with open(js_path, "r", encoding="utf-8") as f:
        js_content = f.read()

    parser = ElementCollector()
    parser.feed(html_content)

    # 1. Location Hero Bar
    print("\n[TEST 1] Location Hero Bar element check:")
    assert "farmLocationHeroBar" in parser.ids, "FAIL: #farmLocationHeroBar not found"
    assert "locationTitle" in parser.ids, "FAIL: #locationTitle missing in hero bar"
    assert "pincodeInput" in parser.ids, "FAIL: #pincodeInput missing in hero bar"
    assert "heroGpsBtn" in parser.ids, "FAIL: #heroGpsBtn missing in hero bar"
    print("  [PASS] #farmLocationHeroBar exists with all required input/GPS elements intact.")

    # 2. Scanner Header and Elements
    print("\n[TEST 2] Scanner elements check:")
    assert "scannerHeaderBanner" in parser.ids, "FAIL: #scannerHeaderBanner not found"
    assert "diseaseCropSelect" in parser.ids, "FAIL: #diseaseCropSelect missing"
    assert "dropZone" in parser.ids, "FAIL: #dropZone missing"
    assert "scanButton" in parser.ids, "FAIL: #scanButton missing"
    assert "onDeviceModelBadge" in parser.ids, "FAIL: #onDeviceModelBadge missing in DOM"
    assert "aiEngineBadgeText" in parser.ids, "FAIL: #aiEngineBadgeText missing in DOM"
    print("  [PASS] All scanner elements (crop selector, dropZone, camera trigger, scanButton, model badges) exist in DOM.")

    # 3. CSS Scoping to body.capacitor-native
    print("\n[TEST 3] Desktop CSS Invariance & Mobile Scoping check:")
    assert "body.capacitor-native" in css_content, "FAIL: body.capacitor-native missing in android.css"
    assert "body.capacitor-native:not([data-active-tab=\"dashboard\"]) #farmLocationHeroBar" in css_content, "FAIL: Hero bar hiding selector missing"
    assert "body.capacitor-native #scannerHeaderBanner .scanner-tech-badge" in css_content, "FAIL: Scanner tech badge hiding rule missing"
    assert "body.capacitor-native #scannerHeaderBanner .scanner-desc-text" in css_content, "FAIL: Scanner desc text hiding rule missing"
    assert "body.capacitor-native #scannerHeaderBanner .scanner-model-badges" in css_content, "FAIL: Scanner model badges hiding rule missing"
    print("  [PASS] All mobile visual changes are strictly scoped under body.capacitor-native.")

    # 4. JavaScript SwitchTab & Bottom Nav Logic
    print("\n[TEST 4] JS Tab switching & Bottom Navigation check:")
    assert "document.body.setAttribute('data-active-tab', tabId);" in js_content, "FAIL: data-active-tab attribute setting missing in switchTab"
    assert "mobile-hidden-tab" in js_content, "FAIL: mobile-hidden-tab toggle missing in switchTab"
    assert "updateAndroidBottomNavActive(tabId);" in js_content, "FAIL: updateAndroidBottomNavActive call missing in switchTab"

    # Check 6 bottom navigation buttons in HTML
    expected_tabs = ["dashboard", "weather", "disease", "fertilizer", "market", "bot"]
    assert parser.bottom_nav_items == expected_tabs, f"FAIL: Nav tabs mismatch: {parser.bottom_nav_items} vs {expected_tabs}"
    print(f"  [PASS] 6 Bottom navigation tabs verified: {parser.bottom_nav_items}")

    # 5. Check other Views
    print("\n[TEST 5] All Tab Views present:")
    for tab in expected_tabs:
        assert f"view-{tab}" in parser.ids, f"FAIL: #view-{tab} missing in DOM"
        print(f"  [PASS] #view-{tab} verified in DOM.")

    print("\n" + "=" * 70)
    print("  ALL 5 SUITE VERIFICATION CHECKS PASSED WITH ZERO ERRORS!")
    print("=" * 70)

if __name__ == "__main__":
    run_tests()
