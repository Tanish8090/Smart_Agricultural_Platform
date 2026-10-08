import os
import sys
import json
import base64
import glob
import urllib.request
import urllib.error

sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = 'http://localhost:8080'
CROPS = ['wheat', 'cotton', 'sugarcane', 'potato', 'rice', 'soybean', 'tomato', 'corn', 'apple', 'grape']

def run_tests():
    report = {
        "disease_scanner": {},
        "not_a_leaf": {},
        "pincodes": {},
        "weather": {},
        "chatbot": {}
    }

    print("=================================================================")
    print("      SMART AGRICULTURE PLATFORM — COMPREHENSIVE TEST RUN        ")
    print("=================================================================\n")

    # 1. Disease Scanner on 10 crops
    print("[1] Testing Local Disease Scanner on All 10 Crops + Not A Leaf...")
    for crop in CROPS:
        # Find a test image for this crop
        pattern = f"datasets/{crop}/test/*/*.jpg"
        images = glob.glob(pattern)
        if not images:
            pattern = f"datasets/{crop}/test/*/*.JPG"
            images = glob.glob(pattern)
        if not images:
            print(f"  [-] {crop.upper()}: No sample test image found matching {pattern}")
            report["disease_scanner"][crop] = {"status": "FAIL", "reason": "No test image found"}
            continue

        sample_path = images[0]
        actual_class = os.path.basename(os.path.dirname(sample_path))
        with open(sample_path, 'rb') as f:
            b64_img = base64.b64encode(f.read()).decode('utf-8')

        payload = json.dumps({
            "crop": crop,
            "image": "data:image/jpeg;base64," + b64_img
        }).encode('utf-8')

        req = urllib.request.Request(
            f"{BASE_URL}/api/disease/analyze",
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as res:
                data = json.loads(res.read().decode('utf-8'))
                pred = data.get("prediction")
                conf = data.get("confidence", 0.0)
                is_leaf = data.get("is_leaf", False)
                print(f"  [+] {crop.upper():10s}: Class={actual_class} -> Pred={pred} (Conf={conf:.2%}, is_leaf={is_leaf})")
                report["disease_scanner"][crop] = {
                    "status": "PASS",
                    "actual_class": actual_class,
                    "prediction": pred,
                    "confidence": conf,
                    "is_leaf": is_leaf
                }
        except Exception as e:
            print(f"  [!] {crop.upper()}: Error during inference: {e}")
            report["disease_scanner"][crop] = {"status": "FAIL", "error": str(e)}

    # Not A Leaf Test
    nal_images = glob.glob("datasets/not_a_leaf/test/*/*.jpg") + glob.glob("datasets/not_a_leaf/test/*/*.JPG")
    if nal_images:
        nal_path = nal_images[0]
        with open(nal_path, 'rb') as f:
            b64_nal = base64.b64encode(f.read()).decode('utf-8')
        payload = json.dumps({
            "crop": "wheat",
            "image": "data:image/jpeg;base64," + b64_nal
        }).encode('utf-8')
        req = urllib.request.Request(
            f"{BASE_URL}/api/disease/analyze",
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as res:
                data = json.loads(res.read().decode('utf-8'))
                pred = data.get("prediction")
                conf = data.get("confidence", 0.0)
                is_leaf = data.get("is_leaf", True)
                passed = (pred == "Not_A_Leaf" or is_leaf == False)
                print(f"  [+] NOT_A_LEAF: Pred={pred} (Conf={conf:.2%}, is_leaf={is_leaf}) -> Gatekeeper passed: {passed}")
                report["not_a_leaf"] = {
                    "status": "PASS" if passed else "FAIL",
                    "prediction": pred,
                    "confidence": conf,
                    "is_leaf": is_leaf
                }
        except Exception as e:
            print(f"  [!] NOT_A_LEAF: Error: {e}")
            report["not_a_leaf"] = {"status": "FAIL", "error": str(e)}

    # 2. Weather & GPS Test
    print("\n[2] Testing Weather Resolution via Lat/Lon...")
    # Test coordinates for Kanpur (26.4499, 80.3319) and Pune (18.5204, 73.8567)
    test_coords = [
        {"city": "Kanpur", "lat": 26.4499, "lon": 80.3319},
        {"city": "Pune", "lat": 18.5204, "lon": 73.8567}
    ]
    for tc in test_coords:
        try:
            url = f"{BASE_URL}/api/weather?lat={tc['lat']}&lon={tc['lon']}&crop=Wheat"
            with urllib.request.urlopen(url, timeout=10) as res:
                data = json.loads(res.read().decode('utf-8'))
                status = data.get("status")
                cur = data.get("current", {})
                temp = cur.get("temp")
                cond = cur.get("condition")
                humidity = cur.get("humidity")
                print(f"  [+] {tc['city']} Weather: Status={status}, Temp={temp}°C, Condition='{cond}', Humidity={humidity}%")
                report["weather"][tc["city"]] = {
                    "status": "PASS" if status == "success" else "FAIL",
                    "temp": temp,
                    "condition": cond,
                    "humidity": humidity
                }
        except Exception as e:
            print(f"  [!] {tc['city']} Weather: Error: {e}")
            report["weather"][tc["city"]] = {"status": "FAIL", "error": str(e)}

    # 3. Indian PIN Code Geocoding Test
    print("\n[3] Testing Indian PIN Code Resolution...")
    test_pins = [
        ("208001", "Kanpur", True),
        ("110001", "New Delhi", True),
        ("500001", "Hyderabad", True),
        ("462001", "Bhopal", True),
        ("000000", "Invalid PIN", False),
        ("999999", "Unassigned PIN", False)
    ]
    for pin, expected_label, should_succeed in test_pins:
        try:
            url = f"{BASE_URL}/api/geocode?pincode={pin}"
            with urllib.request.urlopen(url, timeout=10) as res:
                data = json.loads(res.read().decode('utf-8'))
                status = data.get("status")
                city = data.get("city")
                state = data.get("state")
                lat = data.get("lat")
                lon = data.get("lon")
                if status == "success":
                    print(f"  [+] PIN {pin} ({expected_label}): Resolved -> City={city}, State={state}, Coords=({lat}, {lon})")
                    report["pincodes"][pin] = {"status": "PASS", "city": city, "state": state, "lat": lat, "lon": lon}
                else:
                    print(f"  [-] PIN {pin} ({expected_label}): Service returned status={status}")
                    report["pincodes"][pin] = {"status": "PASS" if not should_succeed else "FAIL", "data": data}
        except urllib.error.HTTPError as he:
            if not should_succeed:
                print(f"  [+] PIN {pin} correctly rejected with HTTP {he.code}")
                report["pincodes"][pin] = {"status": "PASS", "expected_rejection": True, "code": he.code}
            else:
                print(f"  [!] PIN {pin} HTTP error: {he.code}")
                report["pincodes"][pin] = {"status": "FAIL", "code": he.code}
        except Exception as e:
            print(f"  [!] PIN {pin} Error: {e}")
            report["pincodes"][pin] = {"status": "FAIL", "error": str(e)}

    # 4. AI Kisan Bot Test
    print("\n[4] Testing AI Kisan Bot Endpoint (/api/chat)...")
    # A. English query
    try:
        chat_payload = json.dumps({
            "message": "What is the recommended fertilizer for wheat at CRI stage in Kanpur?",
            "crop": "Wheat",
            "location": "Kanpur",
            "soil": "Alluvial",
            "language": "en"
        }).encode('utf-8')
        req = urllib.request.Request(
            f"{BASE_URL}/api/chat",
            data=chat_payload,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=15) as res:
            data = json.loads(res.read().decode('utf-8'))
            status = data.get("status")
            reply = data.get("reply", "")
            print(f"  [+] Chatbot (EN): Status={status}, Reply snippet='{reply[:90]}...'")
            report["chatbot"]["en"] = {"status": "PASS", "response_status": status, "reply_snippet": reply[:120]}
    except Exception as e:
        print(f"  [!] Chatbot (EN) error: {e}")
        report["chatbot"]["en"] = {"status": "FAIL", "error": str(e)}

    # B. Hindi query (natural Devanagari)
    try:
        chat_payload_hi = json.dumps({
            "message": "गेहूं में पीला रतुआ रोग के क्या लक्षण और जैविक उपचार हैं?",
            "crop": "Wheat",
            "location": "Kanpur",
            "soil": "Alluvial",
            "language": "hi"
        }).encode('utf-8')
        req = urllib.request.Request(
            f"{BASE_URL}/api/chat",
            data=chat_payload_hi,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=15) as res:
            data = json.loads(res.read().decode('utf-8'))
            status = data.get("status")
            reply = data.get("reply", "")
            print(f"  [+] Chatbot (HI): Status={status}, Reply snippet='{reply[:90]}...'")
            report["chatbot"]["hi"] = {"status": "PASS", "response_status": status, "reply_snippet": reply[:120]}
    except Exception as e:
        print(f"  [!] Chatbot (HI) error: {e}")
        report["chatbot"]["hi"] = {"status": "FAIL", "error": str(e)}

    print("\n=================================================================")
    print("                    AUTOMATED TESTS COMPLETED                    ")
    print("=================================================================\n")

    with open("training/test_results.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    run_tests()
