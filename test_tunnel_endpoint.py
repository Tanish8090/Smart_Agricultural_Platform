import urllib.request
import json
import ssl
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ctx = ssl._create_unverified_context()
tunnel_url = 'https://rotary-registry-harder-copies.trycloudflare.com'

test_prompts = [
    "Hello bhai",
    "Aalu ugane ka pura tarika batao",
    "Soybean ki kheti kaise karu?",
    "Meri fasal ke patte peele ho rahe hain"
]

print("=================================================================")
print(f"VERIFYING 4 PROMPTS VIA LIVE HTTPS ENDPOINT: {tunnel_url}")
print("=================================================================\n")

results = []
for i, prompt in enumerate(test_prompts, 1):
    print(f"--- [TEST {i}/4] Prompt: {prompt} ---")
    payload = json.dumps({
        'message': prompt,
        'language': 'hi',
        'crop': 'Potato' if 'aalu' in prompt.lower() else ('Soybean' if 'soybean' in prompt.lower() else 'Wheat'),
        'location': 'Kanpur, Uttar Pradesh'
    }).encode('utf-8')

    req = urllib.request.Request(
        f'{tunnel_url}/api/chat',
        data=payload,
        headers={'Content-Type': 'application/json', 'User-Agent': 'SAP-Android-App'},
        method='POST'
    )
    with urllib.request.urlopen(req, timeout=35, context=ctx) as r:
        data = json.loads(r.read().decode('utf-8'))
        reply = data.get('reply', '')
        print(f"HTTP Status: {r.status} | API Status: {data.get('status')} | Chars: {len(reply)}")
        print(f"Reply Sample:\n{reply[:250]}...\n")
        results.append({
            'prompt': prompt,
            'reply': reply,
            'chars': len(reply)
        })

with open("android_https_test_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("All 4 live HTTPS tests completed successfully!")
