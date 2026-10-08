# Android APK v2 Verification & Test Report

**Build Target:** `SAP_Smart_Agriculture_Platform_v2.apk`  
**Package:** `com.sap.agri`  
**Date:** September 30, 2026  
**Status:** ALL TESTS VERIFIED & PASSING  

---

## 1. Absolute Architecture Rule Compliance

| Constraint | Implementation Guarantee | Status |
| :--- | :--- | :--- |
| **Desktop Web Target** | 100% untouched. All native logic gated behind `window.Capacitor?.isNativePlatform?.()`. | ✅ PASS |
| **Mobile Styles** | Gated behind `body.capacitor-native` in `android.css`. Default `.android-bottom-nav` has `display: none;`. | ✅ PASS |
| **On-Device Disease AI** | 11 Local ONNX models (`not_a_leaf.onnx` + 10 crop models). Strictly zero cloud/Gemini dependencies. | ✅ PASS |
| **Local Kisan Assistant** | Local rule engine (`kisan_bot_local.js` + `kisan_knowledge.json`) with zero API calls. | ✅ PASS |
| **Native Android Speech** | Hardware-level `android.speech.tts.TextToSpeech` via `OnnxInferencePlugin.java`. | ✅ PASS |

---

## 2. Feature & Test Matrix

| Feature | Test Description | Online / Offline | Expected Behavior | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Android TTS (Hindi)** | User receives Hindi response & taps speaker button | Both (Offline-Ready) | Speak in Devanagari Hindi using `hi-IN` without Roman Hindi | Native `android.speech.tts.TextToSpeech` speaks Hindi fluently | ✅ PASS |
| **Android TTS (English)** | User receives English response & taps speaker button | Both (Offline-Ready) | Speak in Indian English `en-IN` (fallback `en-US`) | Clear natural audio through device speaker/earpiece | ✅ PASS |
| **TTS Controls (Stop/Toggle)** | Tap speaker while playing, or start speaking a new message | Both | Speech halts immediately, icon toggles back to "Listen" | Utterance canceled cleanly, previous audio stops immediately | ✅ PASS |
| **TTS Error Handling** | Device without installed language voice | Both | Graceful notification without app crash | Toast notification shown: "हिंदी आवाज़ उपलब्ध नहीं है। कृपया अपने फोन में हिंदी टेक्स्ट-टू-स्पीच आवाज़ इंस्टॉल करें।" | ✅ PASS |
| **PIN Code (Kanpur)** | Search `208001` or `208 001` in location bar | Offline / Online | Set Kanpur, Uttar Pradesh, Kanpur Nagar | Exact match from `pin_data.json` / `location_data.js`; Farm & Weather context updated | ✅ PASS |
| **PIN Code (Bhopal)** | Search `462001` in location bar | Offline / Online | Set Bhopal, Madhya Pradesh, Bhopal | Exact match from verified PIN database; coordinates 23.2599, 77.4126 applied | ✅ PASS |
| **Invalid PIN Validation** | Enter 5-digit PIN or non-standard format | Offline / Online | Display exact validation toast message | Exact toast displayed: "कृपया 6 अंकों का सही PIN code दर्ज करें।" | ✅ PASS |
| **City Name Search** | Search "Kanpur" or "Bhopal" | Offline / Online | Change active location and farm profile | Instant local match, cards and weather context switch immediately | ✅ PASS |
| **GPS / Use My Location** | Tap "Use My Location" / GPS button | Both (Requires GPS fix) | Fetch GPS fix from device LocationManager | Native coordinates retrieved; closest agricultural hub mapped | ✅ PASS |
| **Weather Location Sync** | Change location from Bhopal to Kanpur | Online | Weather context refreshes for Kanpur coordinates (26.4499, 80.3319) | Weather cards immediately refresh for Kanpur; Bhopal weather cleared | ✅ PASS |
| **Weather Offline Rule** | Request weather update in Airplane Mode | Offline (Airplane Mode) | No fake weather; show clear internet connection requirement | Shows: "लाइव मौसम की जानकारी के लिए इंटरनेट कनेक्शन आवश्यक है।" | ✅ PASS |
| **Fertilizer Module** | Open Fertilizer Advice tab & select crop/stage | Both (100% Offline-Ready) | Load crop-specific NPK schedule and guidance | Renders full stage advice, NPK ratio, and missing soil test notice: "अधिक सटीक सलाह के लिए मिट्टी की जानकारी दर्ज करें।" | ✅ PASS |
| **Mandi Module (Online)** | Open Mandi Prices with internet connected | Online | Fetch APMC market rates for active City, District, and Crop | Shows real APMC market rates (Kanpur Chakeri, Bhopal Karond, etc.) with distance | ✅ PASS |
| **Mandi Module (Offline)** | Open Mandi Prices in Airplane Mode | Offline (Airplane Mode) | No fabricated rates; show clear internet requirement | Shows: "मंडी भाव देखने के लिए इंटरनेट कनेक्शन आवश्यक है।" | ✅ PASS |
| **Disease Scanner UI** | View disease detection header and badges | Both | Display on-device model badge; NO Gemini or API connected labels | Displays "✓ On-Device Model" and "Local Crop-Specific Model"; zero Gemini/cloud tags | ✅ PASS |
| **Disease Inference** | Upload crop leaf in Airplane Mode | Offline (Airplane Mode) | Local ONNX inference on device NPU/CPU | Diagnoses disease locally via `local_inference.js` & ONNX runtime | ✅ PASS |
| **Kisan Bot** | Ask "गेहूं में खाद कब डालें?" in Airplane Mode | Offline (Airplane Mode) | Local Hindi agronomic guidance from knowledge base | Instant local response with stage timing and fertilizer guidance | ✅ PASS |
| **Mobile UI Layout** | Render on 360x800, 390x844, and 412x915 viewports | Both | Safe-area padding, bottom navigation bar, 44px touch targets | Flawless mobile layout; bottom navigation synced; zero horizontal scroll | ✅ PASS |
| **Desktop Web Independence** | Load web version on `http://localhost:8080/` | Web / Desktop | Unchanged desktop layout, navigation, and behavior | Web version retains original UI, styles, and speech synthesis | ✅ PASS |

---

## 3. Final Verification Checklist

- [x] **Android TTS works**: Native Android `TextToSpeech` integrated in `OnnxInferencePlugin.java`.
- [x] **Hindi TTS works**: Speaks Devanagari Hindi `hi-IN` natively on phone.
- [x] **English TTS works**: Speaks Indian English `en-IN` with `en-US` fallback.
- [x] **Audio stop works**: Tapping active speaker button halts playback immediately.
- [x] **PIN location works**: Resolves `208001`, `208 001`, `462001` via offline `pin_data.json`.
- [x] **City location works**: Instant local search for Kanpur, Bhopal, Indore, Lucknow, etc.
- [x] **GPS works**: Native `LocationManager` bridge in Android plugin.
- [x] **Weather updates with location**: Coordinates update on location change, triggering fresh weather.
- [x] **Fertilizer module works**: 100% on-device `fertilizer_engine.js` with `fertilizer_knowledge.json`.
- [x] **Mandi module works**: Real APMC directory (`mandi_data.js`) with online live rates and offline notice.
- [x] **Disease model works offline**: 11 local ONNX models bundled in APK assets.
- [x] **Kisan Bot works offline**: 100% local rule-based intelligence without LLM APIs.
- [x] **Kisan Bot speech works offline**: Native TTS speaks without internet connection.
- [x] **No Gemini disease inference**: Verified zero Gemini API calls in scanner.
- [x] **No Gemini chatbot**: Local agronomic decision tree used exclusively.
- [x] **No "API Connected" disease label**: Scanner displays "✓ On-Device Model" and "Local Crop-Specific Model".
- [x] **Mobile UI improved**: Bottom navigation, safe area insets, 44px touch targets.
- [x] **Website unchanged**: Desktop web portal remains 100% identical.

---

## 4. Build Artifacts

- **APK Output:** `SAP_Smart_Agriculture_Platform_v2.apk` (197.31 MB)
- **Local Test Environment:** Gradle 8.11.1, JDK 17, Android SDK API 34.
