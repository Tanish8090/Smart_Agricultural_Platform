import sys
sys.path.insert(0, '.')
import legacy_helpers

print("=== 1. Testing Hindi Farming Question ===")
res_hi = legacy_helpers.generate_kisan_chat_response(
    message="मेरे गेहूं में पीले धब्बे क्यों आ रहे हैं?",
    language="hi",
    context={"crop": "Wheat", "location": "Kanpur"}
)
print("Language:", res_hi.get("language"))
print("Reply snippet:\n", res_hi.get("reply")[:300])

print("\n=== 2. Testing Hindi Off-Topic / Medical Question ===")
res_unrelated = legacy_helpers.generate_kisan_chat_response(
    message="mere pet me dard hai",
    language="hi",
    context={"crop": "Wheat", "location": "Kanpur"}
)
print("Language:", res_unrelated.get("language"))
print("Reply snippet:\n", res_unrelated.get("reply")[:300])

print("\n=== 3. Testing English Question ===")
res_en = legacy_helpers.generate_kisan_chat_response(
    message="Why are yellow spots appearing on my wheat leaves?",
    language="en",
    context={"crop": "Wheat", "location": "Kanpur"}
)
print("Language:", res_en.get("language"))
print("Reply snippet:\n", res_en.get("reply")[:300])
