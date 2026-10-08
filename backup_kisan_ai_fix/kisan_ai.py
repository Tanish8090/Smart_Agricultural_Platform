#!/usr/bin/env python3
"""
Smart Agriculture Platform (SAP) — Real Gemini AI Kisan Bot Assistant
Connects user queries directly to Google Gemini API with bilingual support,
farm context awareness (crop, location, weather, soil), multi-turn memory,
and dynamic model fallback.
"""

import os
import sys
import json
import ssl
import urllib.request
import urllib.error

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_gemini_api_key():
    """Retrieve GEMINI_API_KEY safely from environment or .env files."""
    key = os.environ.get('GEMINI_API_KEY', '')
    if key and key.strip():
        return key.strip()

    search_paths = [
        os.path.join(BASE_DIR, '.env'),
        os.path.join(BASE_DIR, 'final sap project', 'final sap project', '.env')
    ]
    for p in search_paths:
        if os.path.isfile(p):
            try:
                with open(p, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith('GEMINI_API_KEY='):
                            val = line.split('=', 1)[1].strip().strip('"').strip("'")
                            if val:
                                return val
            except Exception:
                pass
    return ''

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
1. If the user asks in Hindi or Hinglish (e.g., "Aalu ugane ka pura tarika batao", "गेहूं में यूरिया कब डालें", "patte peele ho rahe hain", "fasal me keede"):
   - Respond in natural, clear, respectful Hindi using Devanagari script.
   - Do NOT respond in Roman script / Hinglish.
2. If the user asks in English (e.g., "Which fertilizer should I use for wheat?", "How often should I irrigate potato?"):
   - Respond in clear, helpful English. Do NOT translate English questions into Hindi.
3. Answer the user's ACTUAL question directly and comprehensively. Provide structured, step-by-step guidance with bold headers and bullet points.
4. Do NOT reply with generic "Ask me questions like..." or list sample questions, unless the user explicitly asks what questions they can ask.
5. If farm context (crop, location, weather, soil) is provided, use it factually. Do NOT fabricate missing details (e.g. do not invent local weather if not provided).
"""

def generate_kisan_chat_response(
    message: str,
    context: dict = None,
    history: list = None,
    image_bytes: bytes = None,
    mime_type: str = 'image/jpeg',
    language: str = None
):
    """
    Process incoming chat query and generate a dynamic response using Google Gemini API.
    """
    context = context or {}
    history = history or []
    message = (message or '').strip()

    # Detect language intent: Hindi characters or Hinglish keywords
    has_devanagari = any('\u0900' <= ch <= '\u097f' for ch in message)
    is_hindi_hinglish = has_devanagari or (str(language).lower() in ('hi', 'hindi'))
    if not is_hindi_hinglish and message:
        hinglish_words = {
            'kya', 'kaise', 'kab', 'batao', 'kare', 'karein', 'kheti', 'mitti',
            'fasal', 'paani', 'pani', 'ugane', 'patte', 'peele', 'tarika', 'me',
            'mein', 'hai', 'hain', 'ho', 'rahe', 'rokn', 'upay', 'khad', 'keede'
        }
        words = set(message.lower().split())
        if len(words.intersection(hinglish_words)) >= 2:
            is_hindi_hinglish = True

    key = get_gemini_api_key()
    if not key:
        print("[Kisan Bot Error] GEMINI_API_KEY is not configured in environment or .env", file=sys.stderr)
        err_msg = (
            'AI किसान बॉट वर्तमान में अनुपलब्ध है। कृपया अपना इंटरनेट कनेक्शन जांचें और पुनः प्रयास करें।'
            if is_hindi_hinglish else
            'AI Kisan Bot is temporarily unavailable. Please check your internet connection and try again.'
        )
        return {
            'status': 'error',
            'error': 'API_KEY_NOT_CONFIGURED',
            'reply': err_msg,
            'message': err_msg,
            'response': err_msg
        }

    # Extract contextual farm details
    crop = context.get('crop') or 'General Crop'
    location = context.get('location') or context.get('locationData')
    weather = context.get('weather')
    soil = context.get('soil') or context.get('soilType')

    context_lines = []
    if crop and crop != 'General Crop':
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
        cur = weather.get('current') if isinstance(weather.get('current'), dict) else weather
        if cur.get('temp') or cur.get('temperature'):
            w_parts.append(f"Temperature: {cur.get('temp') or cur.get('temperature')}°C")
        if cur.get('weather_desc') or cur.get('condition') or cur.get('description'):
            w_parts.append(f"Condition: {cur.get('weather_desc') or cur.get('condition') or cur.get('description')}")
        if cur.get('humidity'):
            w_parts.append(f"Humidity: {cur.get('humidity')}%")
        if w_parts:
            context_lines.append(f"Live Weather: {', '.join(w_parts)}")
    if soil:
        context_lines.append(f"Soil Type: {soil}")

    full_system = SYSTEM_PROMPT
    if context_lines:
        full_system += "\n\nCurrent Farm Context:\n" + "\n".join(f"- {line}" for line in context_lines)

    # Multi-turn conversation contents
    contents = []
    if history and isinstance(history, list):
        for h in history[-8:]:
            role = 'model' if h.get('role') in ('assistant', 'bot', 'model') else 'user'
            text_val = h.get('content') or h.get('text') or ''
            if text_val:
                contents.append({'role': role, 'parts': [{'text': text_val}]})

    current_parts = []
    if image_bytes:
        import base64
        b64_img = base64.b64encode(image_bytes).decode('utf-8')
        current_parts.append({
            'inline_data': {
                'mime_type': mime_type,
                'data': b64_img
            }
        })

    user_text = message if message else (
        ("कृपया इस पत्ती का विश्लेषण करें और उपचार बताएं।" if is_hindi_hinglish else "Please analyze this crop leaf and recommend treatment.")
        if image_bytes else
        ("नमस्ते! आप मेरी खेती में क्या मदद कर सकते हैं?" if is_hindi_hinglish else "Hello! How can you help with my farming?")
    )
    current_parts.append({'text': user_text})

    contents.append({'role': 'user', 'parts': current_parts})

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

    # Model resolution with resilient fallback
    model_pref = os.environ.get('GEMINI_MODEL', 'gemini-3.8-flash')
    model_candidates = [model_pref, 'gemini-3.1-flash-lite', 'gemini-3.6-flash', 'gemini-3.5-flash-lite', 'gemini-flash-latest']
    seen = set()
    candidate_models = [m for m in model_candidates if not (m in seen or seen.add(m))]

    # Temporary development logging
    print(f"[POST /api/chat] message received: {message[:120]}", flush=True)

    last_error = None
    for model_name in candidate_models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={key}"
        req = urllib.request.Request(
            url,
            data=req_data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        print(f"[POST /api/chat] Gemini request sent (model: {model_name})", flush=True)
        try:
            with urllib.request.urlopen(req, timeout=14, context=ctx) as resp:
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
                        'message': response_text,
                        'response': response_text,
                        'model': model_name
                    }
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode('utf-8', errors='replace')[:120]
            last_error = f"HTTP {e.code}: {err_msg}"
            print(f"[POST /api/chat] Model {model_name} HTTP {e.code}: {err_msg}", flush=True)
            continue
        except Exception as e:
            last_error = str(e)
            print(f"[POST /api/chat] Model {model_name} Error: {e}", flush=True)
            continue

    # All model attempts failed - return requested friendly error (NEVER fake advice)
    fallback_text = (
        'AI किसान बॉट वर्तमान में अनुपलब्ध है। कृपया अपना इंटरनेट कनेक्शन जांचें और पुनः प्रयास करें।'
        if is_hindi_hinglish else
        'AI Kisan Bot is temporarily unavailable. Please check your internet connection and try again.'
    )
    return {
        'status': 'error',
        'error': last_error or 'GEMINI_CALL_FAILED',
        'reply': fallback_text,
        'message': fallback_text,
        'response': fallback_text
    }
