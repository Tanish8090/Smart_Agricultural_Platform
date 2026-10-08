# Smart Agriculture Platform (SAP) — Gemini AI Kisan Bot Setup & Architecture

## 1. Architecture Overview

The SAP AI Kisan Bot strictly follows a secure, server-mediated architecture:

```
[Android APK / Desktop Web UI]
               │
               ▼  HTTP POST /api/chat
    [SAP Local Backend: server.py]
               │
               ▼  Google GenAI SDK / Official Gemini REST API
        [Gemini 2.5 Flash]
               │
               ▼  Grounded Response (Hindi Devanagari / English)
    [SAP Local Backend: server.py]
               │
               ▼  JSON { "status": "success", "reply": "...", "intent": "..." }
[Chat UI: Speech Synthesis & Rendering]
```

### Critical Security Principles
- **No Client-Side Secrets:** `GEMINI_API_KEY` is **NEVER** embedded in `app.js`, `index.html`, Capacitor assets, or the compiled Android `.apk`.
- **Environment Isolation:** The backend reads `GEMINI_API_KEY` strictly from the server environment / `.env` file via `python-dotenv` or `os.environ`.
- **No Hallucinated Offline Responses:** If the API key is not configured, the backend returns a clear, helpful `config_error` message instructing the operator how to set their key in `.env`. It does **not** silently invent fake facts.

---

## 2. API Key Configuration

1. In the project root, create a `.env` file (copy from `.env.example`):
   ```bash
   cp .env.example .env
   ```

2. Open `.env` and add your Google Gemini API key:
   ```env
   # Server Port
   PORT=8080

   # Google Gemini API Key (Obtain from https://aistudio.google.com/)
   GEMINI_API_KEY=AIzaSyYourActualKeyHere

   # OpenWeatherMap API Key (Optional — Open-Meteo is used as automatic zero-cost fallback)
   OWM_API_KEY=
   ```

3. Ensure `.env` is ignored by Git:
   ```gitignore
   .env
   .env.local
   *.apk
   ```

---

## 3. Supported Models

The backend (`legacy_helpers.py` / `server.py`) queries currently active, official Gemini models with graceful fallbacks:

| Priority | Model Identifier | Purpose |
|---|---|---|
| 1 (Primary) | `gemini-2.5-flash` | High-speed, multimodal, up-to-date reasoning |
| 2 (Fallback 1) | `gemini-2.0-flash` | Ultra-fast low latency fallback |
| 3 (Fallback 2) | `gemini-1.5-flash` | Standard established production model |
| 4 (Fallback 3) | `gemini-1.5-pro` | Complex multi-turn agronomic reasoning |

---

## 4. Running the Backend Server

To start the backend server with your environment variables:

```bash
# Windows PowerShell
python server.py

# Or with uvicorn directly
uvicorn server:app --host 0.0.0.0 --port 8080
```

Verify the chat endpoint:
```bash
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What fertilizer is best for wheat?", "crop": "Wheat", "language": "en"}'
```

---

## 5. Bilingual Support (Hindi & English)

- When `language: "hi"` is sent, the system instructions compel Gemini to respond in natural, polite Hindi using **Devanagari script** (not Latin transliteration / Hinglish).
- The prompt incorporates the farmer's crop, district/city, weather, and soil type context directly into the prompt to provide tailored, grounded agricultural advice.
