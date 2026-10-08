import sys
import json
import urllib.request

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

base = 'https://scheme-benchmark-tuning-robot.trycloudflare.com'
questions = [
    'Hello bhai',
    'Aalu ki kheti kaise karte hain?',
    'Wheat me yellow leaves kyu hain?',
    'What is soil pH?',
    'Soybean me pani ki problem hai kya karu?'
]

print(f"Connecting to live HTTPS backend: {base}\n")

for i, q in enumerate(questions, 1):
    payload = json.dumps({'message': q, 'history': []}).encode('utf-8')
    req = urllib.request.Request(
        f'{base}/api/chat',
        data=payload,
        headers={'Content-Type': 'application/json', 'User-Agent': 'SAP-Android-App'}
    )
    try:
        res = urllib.request.urlopen(req, timeout=30)
        data = json.loads(res.read().decode('utf-8'))
        reply = data.get('reply', '')
        print(f"✓ Test {i} [{q}]")
        print(f"  HTTP: {res.status} | Status: {data.get('status')} | Model: {data.get('model')} | Chars: {len(reply)}")
        print(f"  Answer: {reply[:120].strip()}...\n")
    except Exception as e:
        print(f"✗ Test {i} [{q}] Failed: {e}\n")
