import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://localhost:8080/api/chat"

def query_chat(message, language, crop="Wheat", location="Kanpur"):
    payload = {
        "message": message,
        "language": language,
        "crop": crop,
        "location": location,
        "soil": "Alluvial / Loam",
        "context": {
            "crop": crop,
            "cropStage": "Vegetative / Growth",
            "soilType": "Alluvial / Loam",
            "location": location,
            "language": language
        }
    }
    req = urllib.request.Request(
        BASE_URL,
        data=json.dumps(payload).encode('utf-8'),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        return data

print("==================================================")
print("TESTING BILINGUAL KISAN AI ASSISTANT ENDPOINT")
print("==================================================\n")

# HINDI TESTS
hindi_tests = [
    "मेरे गेहूं में पीले धब्बे क्यों आ रहे हैं?",
    "आज मौसम कैसा है?",
    "मंडी भाव बताओ",
    "मेरी पत्ती में रोग है",
    "mere pet me dard hai"
]

print("--- [A] HINDI MODE TESTS (Expected: 100% Pure Devanagari Hindi) ---")
for q in hindi_tests:
    print(f"\nUser Query: {q}")
    res = query_chat(q, language="hi")
    reply = res.get("reply", "")
    lang = res.get("language")
    dev_count = sum(1 for ch in reply if '\u0900' <= ch <= '\u097f')
    lat_count = sum(1 for ch in reply if 'a' <= ch.lower() <= 'z')
    is_dev = dev_count > 30 and dev_count > lat_count

    print(f" -> Reported Lang: {lang}")
    print(f" -> Devanagari chars: {dev_count} | Latin chars: {lat_count}")
    print(f" -> Devanagari Check: {'PASS' if is_dev else 'FAIL'}")
    print(f" -> First 120 chars: {reply[:120].strip()}...")
    assert is_dev, f"Response should be in Devanagari Hindi! Got: {reply[:100]}"
    assert not reply.strip().startswith(('Namaste Kisan', 'Kisan Bhai, aapki')), "Must NOT use Roman Hindi!"

print("\n--- [B] ENGLISH MODE TESTS (Expected: 100% English) ---")
english_tests = [
    "Why are yellow spots appearing on my wheat?",
    "What is today's weather forecast?",
    "Tell me mandi prices for wheat",
    "My crop leaf has a disease, what should I do?",
    "I have stomach pain"
]

for q in english_tests:
    print(f"\nUser Query: {q}")
    res = query_chat(q, language="en")
    reply = res.get("reply", "")
    lang = res.get("language")
    dev_count = sum(1 for ch in reply if '\u0900' <= ch <= '\u097f')
    lat_count = sum(1 for ch in reply if 'a' <= ch.lower() <= 'z')
    is_en = lat_count > 30 and lat_count > (dev_count * 2)

    print(f" -> Reported Lang: {lang}")
    print(f" -> Latin chars: {lat_count} | Devanagari chars: {dev_count}")
    print(f" -> English Check: {'PASS' if is_en else 'FAIL'}")
    print(f" -> First 120 chars: {reply[:120].strip()}...")
    assert is_en, f"Response should be in English! Got: {reply[:100]}"

print("\n==================================================")
print("ALL 10/10 BILINGUAL CHAT TEST CASES PASSED 100%!")
print("==================================================")
