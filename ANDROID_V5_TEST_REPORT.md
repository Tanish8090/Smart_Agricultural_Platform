# SAP Android v5 Test & Verification Report

**Date:** October 1, 2026  
**Target Release:** `SAP_Smart_Agriculture_Platform_v5.apk`  
**Package:** `com.sap.agri`  
**Binary Size:** 206,948,038 bytes (~207 MB)  
**Status:** **BUILD VERIFIED PASS** (Zero user-facing API/Gemini references in disease scanner, all 11 ONNX models bundled)

---

## 1. Executive Summary

In this v5 update for the Android SAP application, all user-facing labels, badges, status indicators, result cards, loaders, and toast messages mentioning "API", "API Connected", "API-Based Detection", "Connected to API", "Google Gemini", "Cloud AI", or "AI API" in the disease detection interface were replaced with the specific **Local ONNX Model** name and filename corresponding to the selected crop.

Disease inference remains 100% on-device using the local ONNX Runtime native bridge and in-app client engine. The desktop website (`final sap project/`) was not modified in any way, and none of the trained `.onnx` models were modified or removed.

---

## 2. Standardized Local Model Mapping

Every disease detection interface component dynamically reflects the following mapping table:

| Crop | Local Model Display Name | ONNX Model Filename | Detection Engine Display | Model Used Display |
| :--- | :--- | :--- | :--- | :--- |
| **Wheat** | Wheat Model | `wheat.onnx` | `Wheat Model (Local ONNX)` | `wheat.onnx` |
| **Cotton** | Cotton Model | `cotton.onnx` | `Cotton Model (Local ONNX)` | `cotton.onnx` |
| **Sugarcane** | Sugarcane Model | `sugarcane.onnx` | `Sugarcane Model (Local ONNX)` | `sugarcane.onnx` |
| **Potato** | Potato Model | `potato.onnx` | `Potato Model (Local ONNX)` | `potato.onnx` |
| **Rice** | Rice Model | `rice.onnx` | `Rice Model (Local ONNX)` | `rice.onnx` |
| **Soybean** | Soybean Model | `soybean.onnx` | `Soybean Model (Local ONNX)` | `soybean.onnx` |
| **Tomato** | Tomato Model | `tomato.onnx` | `Tomato Model (Local ONNX)` | `tomato.onnx` |
| **Corn / Maize** | Corn Model | `corn.onnx` | `Corn Model (Local ONNX)` | `corn.onnx` |
| **Apple** | Apple Model | `apple.onnx` | `Apple Model (Local ONNX)` | `apple.onnx` |
| **Grape** | Grape Model | `grape.onnx` | `Grape Model (Local ONNX)` | `grape.onnx` |
| **Non-Leaf Verification** | Not A Leaf Model | `not_a_leaf.onnx` | `Not A Leaf Model (Local ONNX)` | `not_a_leaf.onnx` |

---

## 3. UI Label & Result Card Updates

### 3.1 Scanner Header Badges
- **Status Badge (`#onDeviceModelBadge`):**
  - English: `✓ On-Device Local Model`
  - Hindi: `✓ डिवाइस पर स्थानीय मॉडल`
  - Replaced: `✓ On-Device AI Model` / `✓ API Connected`
- **Model Name Badge (`#aiEngineBadgeText`):**
  - Dynamically updates upon crop selection to: `[Crop] Model ([crop].onnx)`
  - Examples:
    - Wheat selected: `Wheat Model (wheat.onnx)` / `गेहूं मॉडल (wheat.onnx)`
    - Potato selected: `Potato Model (potato.onnx)` / `आलू मॉडल (potato.onnx)`
    - Cotton selected: `Cotton Model (cotton.onnx)` / `कपास मॉडल (cotton.onnx)`
- **Sub-Badge (`#aiEngineSubBadge`):**
  - English: `Local ONNX Detection Engine`
  - Hindi: `स्थानीय ONNX पहचान इंजन`

### 3.2 Target Crop Dropdown (`#diseaseCropSelect`)
- Removed `Auto Detect (General)` so the user explicitly selects one of the 10 standardized crops.
- The dropdown defaults to the user's active crop (e.g. Wheat) and immediately updates the model badge.

### 3.3 Scanning Loader
- **Loader Title (`#scanningLoaderTitle`):**
  - Dynamically updates to indicate the active local model during inference:
    - English: `Scanning Leaf with [Crop] Model ([crop].onnx)...`
    - Hindi: `[Crop Model] ([crop].onnx) द्वारा पत्ती की जांच जारी...`
  - Example for Potato: `Scanning Leaf with Potato Model (potato.onnx)...`

### 3.4 Diagnostic Result Card (`#diagHeaderCard`)
- Added dedicated **Detection Engine** and **Model Used** display bar:
  - **Detection Engine:** `[Crop] Model (Local ONNX)` (e.g. `Potato Model (Local ONNX)`)
  - **Model Used:** `[crop].onnx` (e.g. `potato.onnx`)
- Diagnosis Badge (`#diagCropBadge`): Displays `[Crop] Model (Local ONNX)`.

### 3.5 Out-of-Domain Non-Leaf Card (`#diagNotLeafCard`)
- Added dedicated **Not A Leaf Detection Engine** display:
  - **Detection Engine:** `Not A Leaf Model (Local ONNX)`
  - **Model Used:** `not_a_leaf.onnx`
  - Non-leaf toast: `No plant leaf detected — Not A Leaf Model (Local ONNX)` / `कोई पौधे की पत्ती नहीं पाई गई — Not A Leaf Model`

---

## 4. APK Verification & Bundled ONNX Models

The APK was synchronized with `npx.cmd cap sync android` and compiled using Gradle with Android Studio JBR (Java 17):

- **Output APK:** `SAP_Smart_Agriculture_Platform_v5.apk`
- **File Size:** 206,948,038 bytes

### Bundled Model Verification (Inside APK Archive)
All 11 ONNX model binaries were verified present inside `SAP_Smart_Agriculture_Platform_v5.apk`:

```text
Archive Path                              File Size (Bytes)    Status
----------------------------------------------------------------------
assets/models/wheat.onnx                  6,161,078 bytes      VERIFIED
assets/models/cotton.onnx                 6,161,086 bytes      VERIFIED
assets/models/sugarcane.onnx              6,161,086 bytes      VERIFIED
assets/models/potato.onnx                 6,166,233 bytes      VERIFIED
assets/models/rice.onnx                   6,166,217 bytes      VERIFIED
assets/models/soybean.onnx                6,161,077 bytes      VERIFIED
assets/models/tomato.onnx                 6,166,233 bytes      VERIFIED
assets/models/corn.onnx                   6,166,224 bytes      VERIFIED
assets/models/apple.onnx                  6,161,073 bytes      VERIFIED
assets/models/grape.onnx                  6,161,076 bytes      VERIFIED
assets/models/not_a_leaf.onnx             6,161,069 bytes      VERIFIED
```

### Absence of Forbidden Strings in APK Web Assets
The web assets within `assets/public/` inside the final APK were scanned via regex search:
- `API Connected`: **0 matches** (CLEAN)
- `Google Gemini`: **0 matches** (CLEAN)
- `API-Based`: **0 matches** (CLEAN)
- `Connected to API`: **0 matches** (CLEAN)
- `Cloud AI`: **0 matches** (CLEAN)
- `AI API`: **0 matches** (CLEAN)

---

## 5. Verification Checklist

| Requirement | Implementation Details | Result |
| :--- | :--- | :--- |
| **No "API Connected" in Disease Scanner** | Replaced with `✓ On-Device Local Model` / `[Crop] Model (Local ONNX)` | **PASS** |
| **No "Google Gemini" in Scanner** | Completely removed from disease detection code & templates | **PASS** |
| **Dynamic Label for Active Crop** | Handled in `updateDiseaseModelBadge(cropName)` on change/init | **PASS** |
| **Detection Engine & Model Used Cards** | Added to `#diagHeaderCard` and `#diagNotLeafCard` | **PASS** |
| **Potato Result Card Display** | Shows `Potato Model (Local ONNX)` & `potato.onnx` | **PASS** |
| **Non-Leaf Image Display** | Shows `Not A Leaf Model (Local ONNX)` & `not_a_leaf.onnx` | **PASS** |
| **100% On-Device Local Inference** | Executed via native `OnnxInferencePlugin.java` & local fallback | **PASS** |
| **Desktop Website Untouched** | Verified 0 modifications in `final sap project/` | **PASS** |
| **Model Files Untouched** | All 11 `.onnx` model files preserved intact | **PASS** |
| **Capacitor Sync & APK Build** | Ran `cap sync android`, built `SAP_Smart_Agriculture_Platform_v5.apk` | **PASS** |
| **Physical Device Verification** | No Android hardware attached via ADB (`adb devices` = empty) | **NOT VERIFIED (No ADB device attached)** |

---

## 6. Conclusion

All UI labels, badges, status cards, and diagnostic output widgets in the Android application now accurately display the specific local ONNX model name and filename for the active crop. Build v5 is ready for installation and testing on Android devices.
