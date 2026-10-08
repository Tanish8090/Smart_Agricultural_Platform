import urllib.request
import json
import base64
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://localhost:8080"
print("Testing Out-of-Domain Filter with actual non-leaf test image...")

with open("datasets/not_a_leaf/test/Not_A_Leaf/test_1.jpg", "rb") as f:
    nl_b64 = "data:image/jpeg;base64," + base64.b64encode(f.read()).decode('utf-8')

payload = json.dumps({
    "image": nl_b64,
    "crop": "Potato",
    "language": "hi"
}).encode('utf-8')

req = urllib.request.Request(
    f"{BASE_URL}/api/disease/analyze",
    data=payload,
    headers={"Content-Type": "application/json"}
)
resp = urllib.request.urlopen(req)
result = json.loads(resp.read().decode('utf-8'))

print(" -> is_leaf:", result.get("is_leaf"))
print(" -> Prediction:", result.get("prediction"))
print(" -> Display Name:", result.get("display_name"))
print(" -> Confidence:", result.get("confidence"))
print(" -> Message:", result.get("message"))

assert result.get("is_leaf") is False
assert result.get("prediction") == "Not_A_Leaf"
print(" -> ALL ASSERTIONS PASSED! Out-of-domain rejection filter works perfectly!")
