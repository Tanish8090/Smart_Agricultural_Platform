# SAP Smart Agriculture Platform — Android v3 Verification & Test Report

**Artifact**: `SAP_Smart_Agriculture_Platform_v3.apk`  
**Size**: ~197.36 MB (206,948,917 bytes)  
**Date**: October 1, 2026  
**Build Target**: Android 14 / API 34 (Compiled with JDK 17, Capacitor 6.0)  
**ADB Status**: No real Android physical device connected (`adb devices` returned 0 attached devices). In strict adherence to **Rule 42**, all tests requiring live physical screen touch/mic hardware are explicitly labeled **NOT VERIFIED (No ADB Device Connected)**, while code-level, network, and offline logic tests are labeled **VERIFIED**.

---

## 1. Executive Summary & Verification Matrix

The v3 build incorporates Android-specific viewport & scrolling fixes, safe-area inset management, native Android `SpeechRecognizer` integration via `VoiceRecognitionPlugin.java`, dynamic Open-Meteo weather intelligence with active farm coordinate synchronization, generic Indian postal PIN resolution (combining local SQLite/JSON caches, official India Post API, and OpenStreetMap Nominatim), soft-keyboard viewport adjustments (`android:windowSoftInputMode="adjustResize"`), and internal modal scrolling.

The desktop/web application (`localhost:8080`) remains **100% untouched and isolated**.

| # | Feature | Test Case | Expected Behavior | Actual Behavior / Result | Online / Offline | Status |
|---|---------|-----------|-------------------|--------------------------|------------------|--------|
| **A** | **App Launch** | Launch APK on device | App initializes splash, loads local assets from public bundle, checks native Capacitor environment, loads initial location from `localStorage`. | `MainActivity.java` initializes Capacitor Bridge, registers `OnnxInferencePlugin` and `VoiceRecognitionPlugin`, loads `public/index.html`. | Offline & Online | **NOT VERIFIED** *(Real device not connected)* |
| **B** | **Top Header** | Header visibility & layout | Top header remains visible; content is not obscured or clipped underneath notification bar. | CSS uses `env(safe-area-inset-top)` and `body.capacitor-native header` offset; WebView viewport set with `viewport-fit=cover`. | Offline & Online | **NOT VERIFIED** *(Real device not connected)* |
| **C** | **Bottom Navigation** | Navigation bar positioning & layout | 6-item bottom nav (Home, Weather, Scanner, Fertilizer, Mandi, Kisan Bot) fixed at bottom, respecting `env(safe-area-inset-bottom)`. | Scoped strictly to `body.capacitor-native .android-bottom-nav` with `display: flex !important`, `position: fixed`, and `z-index: 60`. Hidden on desktop. | Offline & Online | **NOT VERIFIED** *(Real device not connected)* |
| **D** | **Global Page Scroll** | Scrolling dashboard & views | Native touch scrolling enabled on body. Bottom content cards fully scrollable above fixed bottom navigation. | Removed `overflow: hidden` from body/html. Configured `overflow-y: auto !important; -webkit-overflow-scrolling: touch;`. Added `padding-bottom: calc(76px + env(safe-area-inset-bottom))` to content containers. | Offline & Online | **NOT VERIFIED** *(Real device not connected)* |
| **E** | **Scanner Scroll** | AI Disease Scanner view | Switching to Scanner tab scrolls smoothly to top of scanner section without random jumps or header overlap. | `switchTab('disease')` executes `window.scrollTo({ top: 0, behavior: 'smooth' })` and updates active nav button state. | Offline & Online | **NOT VERIFIED** *(Real device not connected)* |
| **F** | **Camera Modal** | Live camera leaf scanner modal | Modal centered, fits screen, internal scroll if height exceeds screen (`max-height: calc(100dvh - 32px)`), camera preview fits (`max-height: 40dvh`), capture/close buttons visible above bottom nav. | Scoped in `www/android.css` with `z-index: 70 !important` (above bottom nav `z-index: 60`). Video preview constrained and controls clearly accessible. | Offline & Online | **NOT VERIFIED** *(Real device not connected)* |
| **G** | **Weather Intelligence** | Live weather loading & refresh | Weather requests use active farm coordinates (`lat, lon`), bypasses unreachable localhost API on APK, queries Open-Meteo directly. No hardcoded Bhopal values. | Verified via `test_weather_resolution.py`: Kanpur (32.0°C), Bhopal (33.0°C), Indore (33.6°C), GPS/Pune (32.2°C) fetched distinct live data. | Online (Offline shows clear warning) | **VERIFIED** *(Data Service)* / **NOT VERIFIED** *(Device UI)* |
| **H** | **Generic PIN Resolution** | Any valid 6-digit Indian PIN code | Normalizes input, checks local database, and queries India Post API + Nominatim for live coordinates, post office, district, state. | Verified via `test_pin_resolution.py` across 8 states: UP (208001), MP (462001), MH (400001), PB (141001), BR (800001), RJ (302001), KA (560001), WB (700001). All resolved accurately. | Online (Offline falls back to local DB) | **VERIFIED** *(Resolution Logic)* / **NOT VERIFIED** *(Device UI)* |
| **I** | **GPS Location** | Geolocation detection | Acquires coordinates from device GPS, resolves nearest city/district, updates Active Farm Profile and triggers weather refresh. | Implemented via `navigator.geolocation.getCurrentPosition` with Nominatim reverse geocoding fallback. Saved to `localStorage.getItem('sap_farm_location')`. | Offline (GPS coords) / Online (Reverse geocode) | **NOT VERIFIED** *(Real device not connected)* |
| **J** | **Fertilizer Engine** | Crop & fertilizer advisor | Generates crop-, soil-, and stage-specific NPK advisory using local deterministic calculation engine. | 100% on-device fertilizer engine (`fertilizer_engine.js`) operates without cloud/AI reliance. | 100% Offline Capable | **VERIFIED** *(Engine Logic)* / **NOT VERIFIED** *(Device UI)* |
| **K** | **Mandi Prices** | Real agricultural market prices | Loads mandi prices for 10 core crops with distance sorting and search filtering. | Local mandi database (`mandi_data.js`) populated for key Indian agricultural markets and commodities. | 100% Offline Capable | **VERIFIED** *(Engine Logic)* / **NOT VERIFIED** *(Device UI)* |
| **L** | **Kisan Bot** | Offline Agricultural Assistant | Farmer chatbot generates authentic domain-specific answers for crops, pests, fertilizers, and irrigation without cloud/Gemini AI. | Verified via `test_chat_suite.py` & Node script: queries for wheat yellow rust and irrigation generate comprehensive, agronomy-backed advice. | 100% Offline Capable | **VERIFIED** *(Engine Logic)* / **NOT VERIFIED** *(Device UI)* |
| **M** | **Chatbot Voice Input** | Native Speech Recognition | Tapping mic button requests Android `RECORD_AUDIO` permission, starts `VoiceRecognitionPlugin`, updates UI to 🔴 "सुन रहा हूँ..." (HI) or 🔴 "Listening..." (EN), inserts transcript into `#chatMessageInput`. | Native Java plugin (`VoiceRecognitionPlugin.java`) bridges `android.speech.SpeechRecognizer`. UI updates with pulsing indicator. Errors and permissions handled gracefully. | Online (Native Speech Engine dependent) | **NOT VERIFIED** *(Real device not connected)* |
| **N** | **Chatbot Voice Output** | Native Text-to-Speech (TTS) | Tapping listen button or enabling auto-voice speaks message in selected language. | Existing native Android TTS bridge and Web Speech API synthesis intact with `hi-IN` and `en-IN` locales. | Offline Capable | **NOT VERIFIED** *(Real device not connected)* |
| **O** | **Hindi Language** | Full Hindi localized experience | UI, chatbot responses, voice input language (`hi-IN`), and weather alerts in authentic Devanagari Hindi. | Verified: Speech recognizer sets `hi-IN`; chatbot generates pure Devanagari Hindi (e.g. "🌾 गेहूं के मुख्य रोग व उपचार: पीला रतुआ..."). | Offline & Online | **VERIFIED** *(Logic)* / **NOT VERIFIED** *(Device UI)* |
| **P** | **English Language** | Full English localized experience | UI, chatbot responses, voice input language (`en-IN`/`en-US`), and weather alerts in clear English. | Verified: Speech recognizer sets `en-IN`; chatbot generates domain-rich English response. | Offline & Online | **VERIFIED** *(Logic)* / **NOT VERIFIED** *(Device UI)* |
| **Q** | **11 ONNX Disease Models** | Local AI leaf disease classification | 10 crop models (Wheat, Cotton, Sugarcane, Potato, Rice, Soybean, Tomato, Corn, Apple, Grape) + 1 Not_A_Leaf rejection model run on-device. | Verified: All 11 ONNX models bundled in `android/app/src/main/assets/public/models/` and executed locally via `OnnxInferencePlugin.java`. | 100% Offline Capable | **VERIFIED** *(Asset Bundle)* / **NOT VERIFIED** *(Device Inference)* |
| **R** | **Airplane Mode Test** | Offline disease diagnosis & bot | App functions without network connection: local disease inference and local Kisan Bot continue to operate. Weather & PIN display localized offline notices. | Zero network requests required for ONNX models or `kisan_bot_local.js`. Offline warnings formatted exactly as specified in requirements. | 100% Offline Capable | **VERIFIED** *(Offline Architecture)* / **NOT VERIFIED** *(Device Verification)* |

---

## 2. Detailed Technical Fixes Implemented

### 2.1 Viewport & Layout Architecture (`www/android.css`, `www/index.html`)
- **Viewport Meta**: `<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, viewport-fit=cover">`
- **Dynamic Viewport Height**: Replaced rigid `100vh` on mobile containers with `min-height: 100dvh` and fallback `min-height: 100vh`.
- **Safe-Area Insets**:
  ```css
  body.capacitor-native header {
    padding-top: max(8px, env(safe-area-inset-top)) !important;
  }
  body.capacitor-native .main-content-wrapper {
    padding-bottom: calc(76px + env(safe-area-inset-bottom)) !important;
  }
  ```
- **Unrestricted Body Scroll**: Set `overflow-y: auto !important; -webkit-overflow-scrolling: touch;` on `body.capacitor-native`, removing any body-level scroll locks.
- **Modal Centering & Max Height**: Modals configured with `max-height: calc(100dvh - 24px) !important; overflow-y: auto !important; z-index: 70 !important;` so that they remain fully scrollable and above the fixed navigation bar (`z-index: 60`).

### 2.2 Native Android Speech Recognition Bridge
- **Plugin Implementation**: Created [VoiceRecognitionPlugin.java](file:///c:/Users/Tanish/OneDrive/Desktop/SAP%202/android/app/src/main/java/com/sap/agri/VoiceRecognitionPlugin.java) utilizing Android's native `SpeechRecognizer` and `RecognizerIntent`.
- **Runtime Permissions**: Configured `@Permission(alias = "microphone", strings = { Manifest.permission.RECORD_AUDIO })` with Capacitor's `requestPermissionForAlias` and `@PermissionCallback`.
- **Locale Routing**:
  - Hindi: `RecognizerIntent.EXTRA_LANGUAGE = "hi-IN"`
  - English: `RecognizerIntent.EXTRA_LANGUAGE = "en-IN"` (fallback `en-US`)
- **Registration**: Registered in [MainActivity.java](file:///c:/Users/Tanish/OneDrive/Desktop/SAP%202/android/app/src/main/java/com/sap/agri/MainActivity.java).
- **Soft Input Handling**: Added `android:windowSoftInputMode="adjustResize"` to [AndroidManifest.xml](file:///c:/Users/Tanish/OneDrive/Desktop/SAP%202/android/app/src/main/AndroidManifest.xml) and implemented `window.visualViewport` resize listener in JavaScript to keep the chat input bar and latest messages visible when the on-screen keyboard appears.

### 2.3 Dynamic Weather Engine (`www/app.js`)
- **No Hardcoded Bhopal Values**: Weather requests strictly read active farm profile coordinates: `const { lat, lon } = state.location`.
- **Direct Client Fetch in APK Mode**: In native APK mode where local backend (`localhost:8080`) is not running on the phone, requests automatically query Open-Meteo directly:
  `https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=...`
- **Cache Invalidation**: Force-refresh immediately flushes the cache key (`${lat.toFixed(3)},${lon.toFixed(3)},${crop}`).
- **Offline Resilience**: When `navigator.onLine === false`, the UI displays:
  - Hindi: *"लाइव मौसम की जानकारी के लिए इंटरनेट कनेक्शन आवश्यक है।"*
  - English: *"Live weather requires an internet connection."*

### 2.4 Generic Indian Postal PIN Code Lookup (`www/app.js`)
- **Normalization**: Strips internal and trailing whitespace (`"208 001"` -> `"208001"`).
- **Validation**: Regex check `/^\d{6}$/`. Rejects malformed PINs with localized error alerts.
- **Offline Fallback**: First checks local agricultural location database (`findLocationByPincode`). If offline and not in local cache, displays:
  - Hindi: *"यह PIN ऑफलाइन डेटाबेस में उपलब्ध नहीं है। इंटरनेट कनेक्शन मिलने पर दोबारा प्रयास करें।"*
  - English: *"This PIN is not available in the offline database. Connect to the internet and try again."*
- **Online Postal Resolution**: Queries official `https://api.postalpincode.in/pincode/${cleanPin}` to extract Post Office Name, District, and State, followed by OpenStreetMap Nominatim for exact latitude and longitude.
- **Tested & Verified Across 8 Indian States**:
  - **Uttar Pradesh**: PIN `208001` -> Kanpur Dehat / Kanpur Nagar
  - **Madhya Pradesh**: PIN `462001` -> Bhopal
  - **Maharashtra**: PIN `400001` -> Mumbai
  - **Punjab**: PIN `141001` -> Ludhiana
  - **Bihar**: PIN `800001` -> Patna
  - **Rajasthan**: PIN `302001` -> Jaipur
  - **Karnataka**: PIN `560001` -> Bengaluru
  - **West Bengal**: PIN `700001` -> Kolkata

### 2.5 Desktop Website Protection (`final sap project/`)
- All CSS modifications are strictly isolated to `www/android.css` and scoped under `body.capacitor-native`.
- The desktop portal running at `http://localhost:8080/` loads from `final sap project/` without any Android bottom navigation or mobile overrides.
- Verified on local server: HTTP 200 OK, full desktop layout intact.

---

## 3. Deployment Artifacts

1. **Production Debug APK**:
   - `SAP_Smart_Agriculture_Platform_v3.apk` (Workspace Root)
   - Size: `206,948,917 bytes`
2. **Capacitor Android Project**:
   - `android/app/build/outputs/apk/debug/app-debug.apk`
3. **Automated Verification Scripts**:
   - `training/test_pin_resolution.py` (Tests generic Indian PIN code resolution)
   - `training/test_weather_resolution.py` (Tests multi-city live Open-Meteo queries)
   - `training/test_chat_suite.py` (Tests offline bilingual Kisan Bot intelligence)
