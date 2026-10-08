#!/usr/bin/env python3
"""
Comprehensive Automated Test Suite for AI Kisan Bot
Tests all 8 required agricultural queries + edge cases against both local and HTTPS tunnel endpoints.
"""

import sys
import json
import urllib.request
import urllib.error
import ssl

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

TEST_PROMPTS = [
    {
        "id": 1,
        "query": "Hello bhai",
        "expected_lang": "Hindi (Devanagari)",
        "context": {"crop": "Wheat", "location": "Kanpur, Uttar Pradesh"}
    },
    {
        "id": 2,
        "query": "Yah batao Aalu kheti kaise karte hain",
        "expected_lang": "Hindi (Devanagari)",
        "context": {"crop": "Potato", "location": "Kanpur, Uttar Pradesh"}
    },
    {
        "id": 3,
        "query": "Meri soybean ki kheti mein pani ki samasya hai, kya karun?",
        "expected_lang": "Hindi (Devanagari)",
        "context": {"crop": "Soybean", "location": "Indore, Madhya Pradesh"}
    },
    {
        "id": 4,
        "query": "गेहूं में पीली पत्तियां क्यों हो रही हैं?",
        "expected_lang": "Hindi (Devanagari)",
        "context": {"crop": "Wheat", "location": "Karnal, Haryana"}
    },
    {
        "id": 5,
        "query": "What fertilizer information should I consider for wheat?",
        "expected_lang": "English",
        "context": {"crop": "Wheat", "location": "Punjab, India"}
    },
    {
        "id": 6,
        "query": "How should I irrigate potato?",
        "expected_lang": "English",
        "context": {"crop": "Potato", "location": "Agra, Uttar Pradesh"}
    },
    {
        "id": 7,
        "query": "Tomato ke patton par daag hain, kya karun?",
        "expected_lang": "Hindi (Devanagari)",
        "context": {"crop": "Tomato", "location": "Nashik, Maharashtra"}
    },
    {
        "id": 8,
        "query": "What is soil pH?",
        "expected_lang": "English",
        "context": {"crop": "General"}
    }
]

def run_tests(base_url: str):
    print("=" * 70)
    print(f"RUNNING KISAN BOT TEST SUITE AGAINST: {base_url}")
    print("=" * 70)

    ctx = ssl._create_unverified_context()
    results = []

    for item in TEST_PROMPTS:
        q_id = item["id"]
        query = item["query"]
        expected_lang = item["expected_lang"]
        context = item["context"]

        payload = json.dumps({
            "message": query,
            "crop": context.get("crop", "Wheat"),
            "location": context.get("location", "Kanpur, UP"),
            "context": context
        }).encode("utf-8")

        req = urllib.request.Request(
            f"{base_url}/api/chat",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                status = resp.status
                reply = data.get("reply") or data.get("response") or data.get("message") or ""
                model = data.get("model", "unknown")

                # Language verification
                dev_chars = sum(1 for c in reply if '\u0900' <= c <= '\u097f')
                eng_chars = sum(1 for c in reply if 'a' <= c.lower() <= 'z')
                detected_script = "Devanagari Hindi" if dev_chars > 20 else "English"

                is_pass = status == 200 and data.get("status") == "success" and len(reply) > 50

                print(f"\n[Test #{q_id}] Query: \"{query}\"")
                print(f"  HTTP: {status} | Status: {data.get('status')} | Model: {model}")
                print(f"  Reply Length: {len(reply)} chars | Script: {detected_script}")
                print(f"  Preview: {reply[:130].replace(chr(10), ' ')}...")
                print(f"  Result: {'PASS' if is_pass else 'FAIL'}")

                results.append({
                    "id": q_id,
                    "query": query,
                    "status": status,
                    "api_status": data.get("status"),
                    "model": model,
                    "reply_length": len(reply),
                    "detected_script": detected_script,
                    "reply_preview": reply[:200],
                    "pass": is_pass
                })
        except Exception as e:
            print(f"\n[Test #{q_id}] Query: \"{query}\" -> ERROR: {e}")
            results.append({
                "id": q_id,
                "query": query,
                "error": str(e),
                "pass": False
            })

    # Edge cases
    print("\n--- Testing Edge Cases ---")

    # Edge Case 1: Empty message
    try:
        empty_req = urllib.request.Request(
            f"{base_url}/api/chat",
            data=json.dumps({"message": ""}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(empty_req, timeout=10, context=ctx) as r:
                print("  [Edge 1] Empty message returned HTTP 200 (Expected 400)")
        except urllib.error.HTTPError as e:
            print(f"  [Edge 1] Empty message returned HTTP {e.code} (Correctly rejected empty input)")
    except Exception as e:
        print(f"  [Edge 1] Error: {e}")

    # Edge Case 2: Unexpected query
    try:
        unseen_req = urllib.request.Request(
            f"{base_url}/api/chat",
            data=json.dumps({"message": "Can I grow dragon fruit in Bundelkhand red soil?"}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(unseen_req, timeout=30, context=ctx) as r:
            data = json.loads(r.read().decode("utf-8"))
            unseen_reply = data.get("reply") or data.get("response") or ""
            print(f"  [Edge 2] Unexpected agriculture question answered: {len(unseen_reply)} chars (Model: {data.get('model')})")
    except Exception as e:
        print(f"  [Edge 2] Error: {e}")

    return results

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8080"
    res = run_tests(url)
    with open("kisan_test_results.json", "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=2)
    print("\nAll tests completed and saved to kisan_test_results.json!")
