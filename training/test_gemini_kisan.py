import os
import sys
import json
import ssl
import urllib.request
import urllib.error

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# 1. Load GEMINI_API_KEY from environment or .env files
key = os.environ.get('GEMINI_API_KEY', '')
if not key:
    for env_path in ['.env', 'final sap project/final sap project/.env']:
        if os.path.exists(env_path):
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('GEMINI_API_KEY='):
                        key = line.split('=', 1)[1].strip().strip('"').strip("'")
                        break
        if key:
            break

print("GEMINI_API_KEY loaded:", bool(key), "Length:", len(key), flush=True)

model_pref = os.environ.get('GEMINI_MODEL', 'gemini-3.8-flash')
MODELS = [model_pref, 'gemini-3.6-flash', 'gemini-3.1-flash-lite', 'gemini-flash-latest']

seen = set()
CANDIDATE_MODELS = [m for m in MODELS if not (m in seen or seen.add(m))]

SYSTEM_PROMPT = """You are AI Kisan Assistant, a knowledgeable, practical, and trusted agricultural advisor for Indian farmers.

Your core expertise covers:
- Crop cultivation from sowing to harvesting (land preparation, seed selection, seed treatment, sowing time, spacing, earthing up, harvesting, storage)
- Balanced fertilization and nutrient management (NPK, Urea, DAP, MOP, micronutrients, FYM, organic fertilizers)
- Irrigation scheduling and water management
- Plant protection: Pest, insect, and disease diagnosis, organic remedies, and approved chemical sprays
- Soil management, soil health, and pH adjustments
- Weather-informed farming decisions
- General agricultural and farm management practices

Language and Script Rules:
1. If the user asks in Hindi or Hinglish (e.g., "Aalu ugane ka pura tarika batao", "गेहूं में यूरिया कब डालें", "patte peele ho rahe hain"):
   - Respond in natural, clear, respectful Hindi using Devanagari script.
   - Do NOT respond in Roman script / Hinglish.
2. If the user asks in English (e.g., "Which fertilizer should I use for wheat?", "How often should I irrigate potato?"):
   - Respond in clear, helpful English. Do NOT translate English questions into Hindi.
3. Answer the user's ACTUAL question directly and comprehensively. Provide structured, step-by-step guidance with bold headers and bullet points.
4. Do NOT reply with generic "Ask me questions like..." or list sample questions, unless the user explicitly asks what questions they can ask.
5. If farm context (crop, location, weather, soil) is provided, use it factually. Do NOT fabricate missing details (e.g. do not invent local weather if not provided).
"""

def generate_chat_response(message, crop=None, location=None, weather=None, soil=None, history=None):
    history = history or []
    
    # Detect language intent: Hindi characters or Hinglish keywords
    has_devanagari = any('\u0900' <= ch <= '\u097f' for ch in message)
    is_hindi_hinglish = has_devanagari
    if not is_hindi_hinglish:
        hinglish_words = {'kya', 'kaise', 'kab', 'batao', 'kare', 'karein', 'kheti', 'mitti', 'fasal', 'paani', 'pani', 'ugane', 'patte', 'peele', 'tarika', 'me', 'mein', 'hai', 'hain', 'ho', 'rahe', 'rokn', 'upay'}
        words = set(message.lower().split())
        if len(words.intersection(hinglish_words)) >= 2:
            is_hindi_hinglish = True

    # Assemble context block
    context_lines = []
    if crop:
        context_lines.append(f"Selected Crop: {crop}")
    if location:
        if isinstance(location, dict):
            loc_str = f"{location.get('city', '')} {location.get('district', '')} {location.get('state', '')} {location.get('pincode', '')}".strip()
            if loc_str:
                context_lines.append(f"Location: {loc_str}")
        else:
            context_lines.append(f"Location: {location}")
    if weather and isinstance(weather, dict):
        w_parts = []
        if weather.get('temperature'):
            w_parts.append(f"Temperature: {weather.get('temperature')}°C")
        if weather.get('condition'):
            w_parts.append(f"Condition: {weather.get('condition')}")
        if weather.get('humidity'):
            w_parts.append(f"Humidity: {weather.get('humidity')}%")
        if w_parts:
            context_lines.append(f"Live Weather: {', '.join(w_parts)}")
    if soil:
        context_lines.append(f"Soil Type: {soil}")

    full_system = SYSTEM_PROMPT
    if context_lines:
        full_system += "\n\nCurrent Farm Context:\n" + "\n".join(f"- {line}" for line in context_lines)

    # Format multi-turn conversation
    contents = []
    for h in history[-8:]:
        role = 'model' if h.get('role') in ('assistant', 'bot', 'model') else 'user'
        text_val = h.get('content') or h.get('text') or ''
        if text_val:
            contents.append({'role': role, 'parts': [{'text': text_val}]})

    # Current user message
    contents.append({'role': 'user', 'parts': [{'text': message}]})

    payload = {
        'system_instruction': {
            'parts': [{'text': full_system}]
        },
        'contents': contents,
        'generationConfig': {
            'temperature': 0.3,
            'maxOutputTokens': 2048
        }
    }

    req_data = json.dumps(payload).encode('utf-8')
    ctx = ssl._create_unverified_context()

    print(f"\n[POST /api/chat] message received: {message}", flush=True)

    for model_name in CANDIDATE_MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={key}"
        req = urllib.request.Request(
            url,
            data=req_data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        print(f"[POST /api/chat] Gemini request sent (model: {model_name})", flush=True)
        try:
            with urllib.request.urlopen(req, timeout=12, context=ctx) as resp:
                res_json = json.loads(resp.read().decode('utf-8'))
                candidates = res_json.get('candidates', [])
                if candidates:
                    parts = candidates[0].get('content', {}).get('parts', [])
                    text_parts = [p['text'] for p in parts if 'text' in p and not p.get('thought', False)]
                    if not text_parts and parts:
                        text_parts = [parts[-1].get('text', '')]
                    response_text = ''.join(text_parts).strip()
                    print(f"[POST /api/chat] Gemini response received ({len(response_text)} chars, model: {model_name})", flush=True)
                    return {
                        'status': 'success',
                        'reply': response_text,
                        'model': model_name
                    }
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode('utf-8', errors='replace')[:120]
            print(f"[POST /api/chat] Model {model_name} HTTP {e.code}: {err_msg}", flush=True)
            continue
        except Exception as e:
            print(f"[POST /api/chat] Model {model_name} Error: {e}", flush=True)
            continue

    return {
        'status': 'error',
        'reply': 'AI किसान बॉट वर्तमान में अनुपलब्ध है। कृपया अपना इंटरनेट कनेक्शन जांचें और पुनः प्रयास करें।' if is_hindi_hinglish else 'AI Kisan Bot is temporarily unavailable. Please check your internet connection and try again.'
    }

test_questions = [
    ("Aalu ugane ka mujhe pura tarika batao", "Potato"),
    ("गेहूं में पीली पत्तियां क्यों हो रही हैं?", "Wheat"),
    ("Tomato me early blight kaise control kare?", "Tomato"),
    ("Which fertilizer should I use for wheat?", "Wheat"),
    ("How often should I irrigate potato?", "Potato")
]

print("="*60, flush=True)
print("STARTING 5 KISAN BOT TEST QUESTIONS", flush=True)
print("="*60, flush=True)

for i, (q, crop) in enumerate(test_questions, 1):
    print(f"\n--- TEST #{i}: '{q}' (Crop: {crop}) ---", flush=True)
    res = generate_chat_response(q, crop=crop, location={"city": "Kanpur", "state": "Uttar Pradesh"})
    if res['status'] == 'success':
        print(f"SUCCESS [Model: {res.get('model')}]:", flush=True)
        reply = res['reply']
        print(reply[:250] + " ...\n... " + reply[-100:], flush=True)
    else:
        print("FAILED:", res['reply'], flush=True)
