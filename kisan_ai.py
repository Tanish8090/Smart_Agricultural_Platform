#!/usr/bin/env python3
"""
Smart Agriculture Platform (SAP) — Real Gemini AI Kisan Bot Assistant
Connects farmer queries directly to the official Google Gemini API with:
- True conversational intelligence for all agricultural and farm management topics
- Bilingual understanding (Hindi, English, Hinglish) with natural Devanagari Hindi responses
- Fact-grounded farm context (crop, growth stage, soil, location, weather) without fabrication
- Multi-turn conversation history
- Official google-genai SDK support with resilient REST fallback
- Strict adherence to real AI responses with zero keyword-matching or hardcoded canned answers
"""

import os
import sys
import json
import ssl
import urllib.request
import urllib.error
import warnings
from typing import Any, Dict, List, Optional

# Suppress non-critical SDK advisory warnings
warnings.filterwarnings("ignore")

# Ensure UTF-8 output
reconfigure_stdout = getattr(sys.stdout, 'reconfigure', None)
if callable(reconfigure_stdout):
    reconfigure_stdout(encoding='utf-8', errors='replace')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Try importing official Google GenAI SDK
try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None

# System instruction configuring Gemini as a GENERAL AI ASSISTANT with deep AGRICULTURE expertise
SYSTEM_INSTRUCTION = """You are AI Kisan Assistant, an intelligent, versatile AI assistant with specialized, deep expertise in Indian agriculture as well as broad general knowledge.

CORE CAPABILITIES & DIRECTIVES:
1. ANSWER ANY USER QUESTION: You are NOT restricted to agriculture. You must answer ANY question the user asks — whether about general knowledge, daily life, science, technology, language, study tips, math, coding, jokes, or casual conversation.
   - Examples of non-farming queries to answer naturally: "Hello", "Who are you?", "What is AI?", "Explain photosynthesis", "Give me a study timetable", "How can I improve my English?", "Tell me a joke", "Explain this in simple words", etc.
   - NEVER refuse or reject a question merely because it is not about agriculture.
   - NEVER say: "I can only answer agriculture questions", "I am only an agricultural assistant", or "Ask me about crops". Always respond helpfully.

2. AGRICULTURE EXPERTISE:
   When the question relates to farming, crops, soil, or agriculture, provide detailed, practical, farmer-friendly guidance covering:
   - Crop cultivation & farming practices (wheat, rice, potato, tomato, cotton, sugarcane, maize, soybean, mustard, etc.)
   - Sowing techniques, seed rate & seed treatment
   - Irrigation scheduling & water management
   - Fertilizers & plant nutrition (Urea, DAP, MOP, NPK ratios, zinc, biofertilizers, vermicompost, farmyard manure)
   - Soil health, soil pH, soil types & organic carbon management
   - Pest identification, disease diagnosis, symptoms, organic remedies & chemical treatments (with safe dosages)
   - Crop growth stages, harvesting, post-harvest handling & storage
   - Weather impact on crops and timely agricultural advisories

3. LANGUAGE & SCRIPT RULES:
   - Hindi or Hinglish query (e.g., "Aalu ki kheti kaise kare?", "गेहूं में पीली पत्तियां क्यों हो रही हैं?") → Respond naturally in fluent, grammatically correct Hindi using Devanagari script.
   - English query (e.g., "What is AI?", "How to improve English?") → Respond in clear, natural English.
   - Mixed-language query → Respond naturally in the language most appropriate and comfortable for the user.
   - Do NOT use robotic or hardcoded translations.

4. CONVERSATIONAL CONTEXT & FOLLOW-UP QUESTIONS:
   - Understand recent conversational context and pronouns across follow-up questions.
   - Example: If the user previously mentioned "I am growing potato" and later asks "When should I water it?", understand that "it" refers to potato.
   - Maintain continuity across multi-turn exchanges.

5. RESPONSE STRUCTURE & LENGTH:
   - Do NOT artificially restrict answers to a single sentence or a tiny snippet.
   - For complex questions: Provide a well-structured, easy-to-read answer using headings, numbered steps, bullet points, or clear paragraphs.
   - For simple questions: Provide a concise, direct answer without unnecessary fluff.

6. GROUNDING & LIVE INFORMATION:
   - Use the provided farm profile (selected crop, growth stage, soil, location, weather) only when that information is actually available and relevant.
   - NEVER invent or fabricate missing data, live weather conditions, or live mandi market prices.
   - If the user asks for live data (e.g., "What is today's mandi price?" or "What's the weather today?") and verified live data is not in the provided context, clearly state that current live market prices or real-time data are currently unavailable, while still answering general aspects (such as standard price trends, official sources like e-NAM, or seasonal weather guidance).

7. HANDLING UNCERTAIN OR INSUFFICIENT QUERIES:
   - Do not dismiss vague questions with a cold "I don't know" or refusal.
   - If a problem is described with insufficient detail (e.g., "मेरी फसल खराब हो रही है"), explain the common potential causes, note what is uncertain, and politely ask for more details (e.g., crop name, observed symptoms, or a leaf photo).
"""


def get_gemini_api_key() -> str:
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


def get_gemini_model_preference() -> str:
    """Retrieve GEMINI_MODEL configuration from environment or .env file."""
    model = os.environ.get('GEMINI_MODEL', '').strip()
    if model:
        return model

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
                        if line.startswith('GEMINI_MODEL='):
                            val = line.split('=', 1)[1].strip().strip('"').strip("'")
                            if val:
                                return val
            except Exception:
                pass
    return 'gemini-3.8-flash'


def build_system_instruction_with_context(context: Optional[dict] = None) -> str:
    """
    Build the final system instruction incorporating available farm context.
    Strictly avoids fabricating information if fields are missing or empty.
    """
    context = context or {}
    context_blocks = []

    crop = str(context.get('crop') or '').strip()
    if crop and crop.lower() not in ('general', 'general crop', 'unknown', 'auto'):
        context_blocks.append(f"Selected Crop: {crop}")

    crop_stage = str(context.get('crop_stage') or context.get('cropStage') or '').strip()
    if crop_stage and crop_stage.lower() not in ('unknown', 'not specified'):
        context_blocks.append(f"Crop Growth Stage: {crop_stage}")

    soil = str(context.get('soil') or context.get('soilType') or '').strip()
    if soil and soil.lower() not in ('unknown', 'not specified'):
        context_blocks.append(f"Soil Details: {soil}")

    location = context.get('location') or context.get('locationData')
    if location:
        if isinstance(location, dict):
            parts = [
                location.get('village', ''),
                location.get('block', ''),
                location.get('district', '') or location.get('city', ''),
                location.get('state', ''),
                str(location.get('pincode', '')).strip()
            ]
            loc_str = ', '.join([p for p in parts if p and p not in ('GPS', 'City', 'Farm Location')])
            if loc_str:
                context_blocks.append(f"Farmer Location: {loc_str}")
        elif isinstance(location, str) and location.strip():
            context_blocks.append(f"Farmer Location: {location.strip()}")

    weather = context.get('weather')
    if weather and isinstance(weather, dict):
        cur_candidate = weather.get('current')
        cur = cur_candidate if isinstance(cur_candidate, dict) else weather
        w_parts = []
        temp = cur.get('temp') or cur.get('temperature')
        if temp is not None:
            w_parts.append(f"Temperature: {temp}°C")
        desc = cur.get('weather_desc') or cur.get('condition') or cur.get('description') or cur.get('weather_main')
        if desc:
            w_parts.append(f"Condition: {desc}")
        hum = cur.get('humidity')
        if hum is not None:
            w_parts.append(f"Humidity: {hum}%")
        if w_parts:
            context_blocks.append(f"Current Verified Weather: {', '.join(w_parts)}")

    symptoms = str(context.get('symptoms') or '').strip()
    if symptoms:
        context_blocks.append(f"Reported Plant Symptoms: {symptoms}")

    if context_blocks:
        return SYSTEM_INSTRUCTION + "\n\nAvailable Verified Farm Context (use only what is relevant; never fabricate missing values):\n" + "\n".join(f"- {b}" for b in context_blocks)
    return SYSTEM_INSTRUCTION


def generate_kisan_chat_response(
    message: str,
    context: Optional[dict] = None,
    history: Optional[list] = None,
    image_bytes: Optional[bytes] = None,
    mime_type: str = 'image/jpeg',
    language: Optional[str] = None
) -> dict:
    """
    Process incoming user query and generate a genuine Gemini AI response.
    Never uses hardcoded answers, static FAQs, or keyword matching.
    """
    message = (message or '').strip()
    if not message and not image_bytes:
        return {
            'status': 'error',
            'error': 'EMPTY_QUERY',
            'message': 'Please provide a question or attach an image.'
        }

    key = get_gemini_api_key()
    if not key:
        print("[Kisan Bot Backend Error] GEMINI_API_KEY is not configured in environment or .env", file=sys.stderr)
        return {
            'status': 'error',
            'error': 'API_KEY_NOT_CONFIGURED',
            'message': 'AI Kisan Bot is temporarily unavailable. Please check your internet connection and try again.'
        }

    system_instruction = build_system_instruction_with_context(context)

    # Format and sanitize multi-turn conversation history
    # Gemini requires strictly alternating user and model turns.
    sanitized_history = []
    if history and isinstance(history, list):
        for h in history[-8:]:
            if not isinstance(h, dict):
                continue
            role = 'model' if h.get('role') in ('assistant', 'bot', 'model') or h.get('sender') in ('assistant', 'bot', 'model') else 'user'
            text_val = h.get('content') or h.get('text') or h.get('message') or ''
            if not text_val and 'parts' in h and isinstance(h['parts'], list):
                part_texts = [p.get('text', '') for p in h['parts'] if isinstance(p, dict) and p.get('text')]
                text_val = ' '.join(part_texts)
            text_val = text_val.strip()
            if not text_val:
                continue

            # Ensure strictly alternating roles
            if sanitized_history and sanitized_history[-1]['role'] == role:
                sanitized_history[-1]['parts'][0]['text'] += "\n" + text_val
            else:
                sanitized_history.append({'role': role, 'parts': [{'text': text_val}]})

    # The incoming turn is always from 'user'.
    # Ensure the turn directly preceding the new user turn has role 'model'.
    if sanitized_history and sanitized_history[-1]['role'] == 'user':
        sanitized_history.pop()

    contents = list(sanitized_history)

    # Prepare current turn parts
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

    user_text = message if message else "कृपया इस फसल की पत्ती का विश्लेषण करें और मार्गदर्शन दें।"
    current_parts.append({'text': user_text})
    contents.append({'role': 'user', 'parts': current_parts})

    # Prepare candidate models based on verified availability
    preferred_model = get_gemini_model_preference()
    candidate_models = []
    if preferred_model:
        candidate_models.append(preferred_model)
    for m in ['gemini-3.8-flash', 'gemini-3.5-flash', 'gemini-3.5-flash-lite', 'gemini-flash-latest']:
        if m not in candidate_models:
            candidate_models.append(m)

    # Log incoming request safely (never log API keys)
    print(f"[POST /api/chat] User message received: {message[:100]}", flush=True)

    last_error = None
    for model_name in candidate_models:
        print(f"[POST /api/chat] Forwarding to Gemini API (model: {model_name})...", flush=True)

        # 1. Try official google-genai SDK first via Chat API
        if genai is not None and types is not None:
            try:
                client = genai.Client(api_key=key)

                # Format history for SDK
                sdk_history = []
                for turn in contents[:-1]:
                    turn_role = turn['role']
                    sdk_parts = []
                    for p in turn['parts']:
                        if 'text' in p:
                            sdk_parts.append(types.Part.from_text(text=p['text']))
                        elif 'inline_data' in p:
                            import base64
                            b_data = base64.b64decode(p['inline_data']['data'])
                            sdk_parts.append(types.Part.from_bytes(data=b_data, mime_type=p['inline_data']['mime_type']))
                    sdk_history.append(types.Content(role=turn_role, parts=sdk_parts))

                current_turn = contents[-1]
                current_sdk_parts = []
                for p in current_turn['parts']:
                    if 'text' in p:
                        current_sdk_parts.append(types.Part.from_text(text=p['text']))
                    elif 'inline_data' in p:
                        import base64
                        b_data = base64.b64decode(p['inline_data']['data'])
                        current_sdk_parts.append(types.Part.from_bytes(data=b_data, mime_type=p['inline_data']['mime_type']))

                config = types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.35,
                    max_output_tokens=2500
                )

                chat = client.chats.create(
                    model=model_name,
                    config=config,
                    history=sdk_history if sdk_history else None
                )
                resp = chat.send_message(current_sdk_parts)
                response_text = (resp.text or '').strip()
                if response_text:
                    print(f"[POST /api/chat] Real Gemini response received ({len(response_text)} chars, model: {model_name})", flush=True)
                    return {
                        'status': 'success',
                        'reply': response_text,
                        'response': response_text,
                        'message': response_text,
                        'model': model_name
                    }
            except Exception as e:
                err_str = str(e)
                last_error = f"SDK {model_name}: {err_str[:120]}"
                print(f"[POST /api/chat] Model {model_name} SDK error: {err_str[:120]}", flush=True)
                if '503' in err_str or '429' in err_str or '404' in err_str:
                    continue

        # 2. Resilient Direct REST fallback to official Gemini endpoint
        payload = {
            'system_instruction': {
                'parts': [{'text': system_instruction}]
            },
            'contents': contents,
            'generationConfig': {
                'temperature': 0.35,
                'maxOutputTokens': 2500
            }
        }
        req_data = json.dumps(payload).encode('utf-8')
        ctx = ssl._create_unverified_context()
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={key}"
        req = urllib.request.Request(
            url,
            data=req_data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        try:
            with urllib.request.urlopen(req, timeout=25, context=ctx) as resp:
                res_json = json.loads(resp.read().decode('utf-8'))
                candidates_out = res_json.get('candidates', [])
                if candidates_out:
                    parts = candidates_out[0].get('content', {}).get('parts', [])
                    text_parts = [p['text'] for p in parts if 'text' in p and not p.get('thought', False)]
                    if not text_parts and parts:
                        text_parts = [parts[-1].get('text', '')]
                    response_text = ''.join(text_parts).strip()
                    if response_text:
                        print(f"[POST /api/chat] Real Gemini REST response received ({len(response_text)} chars, model: {model_name})", flush=True)
                        return {
                            'status': 'success',
                            'reply': response_text,
                            'response': response_text,
                            'message': response_text,
                            'model': model_name
                        }
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode('utf-8', errors='replace')[:140]
            last_error = f"REST {model_name} HTTP {e.code}: {err_msg}"
            print(f"[POST /api/chat] Model {model_name} HTTP {e.code}: {err_msg}", flush=True)
            continue
        except Exception as e:
            last_error = str(e)
            print(f"[POST /api/chat] Model {model_name} REST error: {e}", flush=True)
            continue

    # All model attempts failed
    print(f"[POST /api/chat] All Gemini model attempts failed. Last error: {last_error}", file=sys.stderr)
    return {
        'status': 'error',
        'error': last_error or 'GEMINI_CALL_FAILED',
        'message': 'AI Kisan Bot is temporarily unavailable. Please check your internet connection and try again.'
    }
