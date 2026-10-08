import urllib.request
import json
import time

pins = [
    ('208001', 'Uttar Pradesh'),
    ('462001', 'Madhya Pradesh'),
    ('400001', 'Maharashtra'),
    ('141001', 'Punjab'),
    ('800001', 'Bihar'),
    ('302001', 'Rajasthan'),
    ('560001', 'Karnataka'),
    ('700001', 'West Bengal'),
]

print(f"Testing {len(pins)} PINs across states...")
for pin, expected_state in pins:
    url = f"https://api.postalpincode.in/pincode/{pin}"
    req = urllib.request.Request(url, headers={'User-Agent': 'SAP-Test/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=5) as res:
            data = json.loads(res.read().decode('utf-8'))
            if data and data[0].get('Status') == 'Success':
                po = data[0]['PostOffice'][0]
                actual_state = po.get('State')
                po_name = po.get('Name')
                district = po.get('District')
                match = (expected_state.lower() in actual_state.lower())
                status = "PASS" if match else "STATE_MISMATCH"
                print(f"[{status}] PIN {pin} -> PO: {po_name}, District: {district}, State: {actual_state}")
            else:
                print(f"[FAIL] PIN {pin} returned non-success")
    except Exception as e:
        print(f"[ERROR] PIN {pin}: {e}")
    time.sleep(0.3)
