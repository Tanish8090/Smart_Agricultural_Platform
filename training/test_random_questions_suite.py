import urllib.request
import json
import sys
import time

# Ensure utf-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_URL = 'http://127.0.0.1:8080'

TEST_QUESTIONS = [
    ("1. Greeting (Hinglish)", "Hello bhai"),
    ("2. General Tech / AI", "What is AI?"),
    ("3. Identity", "Who are you?"),
    ("4. Science / Biology", "Explain photosynthesis in simple words."),
    ("5. Self-improvement / Language", "How can I improve my English?"),
    ("6. Crop Cultivation (Hinglish)", "Aalu ki kheti kaise kare?"),
    ("7. Crop Symptom (Hindi)", "गेहूं की पत्तियां पीली क्यों हो रही हैं?"),
    ("8. Soil Science", "What is soil pH?"),
    ("9. Fertilizer Guidance", "Give me fertilizer guidance for wheat."),
    ("10. Agronomy Practices", "Explain crop rotation."),
    ("11. Plant Care Problem", "What should I do if my plants are wilting?"),
    ("12. Completely Brand New Question", "Can quantum computers simulate complex molecular folding for drought-resistant enzymes?")
]

FORBIDDEN_PHRASES = [
    "i can only answer agriculture",
    "i can only answer agricultural",
    "i am only an agricultural",
    "ask me about crops",
    "only answer questions about farming",
    "केवल कृषि संबंधी"
]

print("==================================================================")
print("TESTING REAL GEMINI KISAN BOT ACROSS 12 DIVERSE QUESTIONS")
print(f"Target Endpoint: {BASE_URL}/api/chat")
print("==================================================================\n")

results = []
all_passed = True

for idx, (label, question) in enumerate(TEST_QUESTIONS, 1):
    print(f"[{idx}/12] Testing: {label}")
    print(f"      Question: \"{question}\"")
    
    payload = {
        "message": question,
        "context": {
            "crop": "Wheat",
            "soil": "Alluvial",
            "location": "Bhopal, MP"
        }
    }
    
    req = urllib.request.Request(
        f"{BASE_URL}/api/chat",
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    start_t = time.time()
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            elapsed = time.time() - start_t
            
            status = data.get('status')
            reply = data.get('reply') or data.get('response') or data.get('message') or ''
            model = data.get('model', 'gemini')
            
            # Checks
            is_success = (status == 'success')
            has_content = len(reply.strip()) > 30
            
            # Check for forbidden refusal phrases
            reply_lower = reply.lower()
            refusal_found = any(phrase in reply_lower for phrase in FORBIDDEN_PHRASES)
            
            if is_success and has_content and not refusal_found:
                print(f"      Status: PASS (HTTP 200, status='success', {len(reply)} chars, {elapsed:.1f}s, model={model})")
                first_lines = " ".join(reply.strip().splitlines()[:2])[:120]
                print(f"      Sample: {first_lines}...")
                results.append((label, True, f"{len(reply)} chars", model))
            else:
                all_passed = False
                err_details = f"is_success={is_success}, has_content={has_content}, refusal_found={refusal_found}"
                print(f"      Status: FAIL ({err_details})")
                print(f"      Reply: {reply[:200]}")
                results.append((label, False, err_details, model))
                
    except Exception as e:
        elapsed = time.time() - start_t
        all_passed = False
        print(f"      Status: ERROR ({e}) in {elapsed:.1f}s")
        results.append((label, False, str(e), "none"))
        
    print()

print("==================================================================")
print("TEST SUMMARY")
print("==================================================================")
for label, passed, detail, model in results:
    mark = "PASS" if passed else "FAIL"
    print(f"[{mark}] {label:35} -> {detail} ({model})")

print("==================================================================")
if all_passed:
    print("ALL 12 QUESTIONS PASSED REAL GEMINI GENERATION TEST!")
else:
    print("SOME QUESTIONS FAILED. CHECK LOGS ABOVE.")
    sys.exit(1)
