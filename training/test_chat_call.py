import sys
sys.path.insert(0, '.')
import legacy_helpers

res = legacy_helpers.generate_kisan_chat_response("Hello, what is the best fertilizer for wheat?")
print("Result status:", res.get('status'))
print("Engine:", res.get('engine'))
print("Reply snippet:", str(res.get('reply'))[:200])
