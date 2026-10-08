# Android Build & Compilation Guide — Smart Agriculture Platform (SAP)

This document provides reproducible, step-by-step instructions to compile and assemble the Android APK for the Smart Agriculture Platform.

---

## 1. Prerequisites

Ensure the following SDKs and runtimes are installed on your workstation:

1. **Node.js**: v18.x or v20.x+ (`node --version`, `npm --version`)
2. **Java Development Kit (JDK)**: **OpenJDK 17 LTS** (Crucial: Android Gradle Plugin 8.7+ and Capacitor 7 require JDK 17 compatibility).
   - In this workspace, OpenJDK 17 is available at:
     ```
     C:\Users\Tanish\.jdks\jdk-17
     ```
3. **Android SDK**: API Level 35 (`compileSdk 35`, `targetSdk 35`, `minSdk 23`).
   - Android SDK location:
     ```
     C:\Users\Tanish\AppData\Local\Android\Sdk
     ```

---

## 2. Web Asset & Plugin Synchronization

Before building the native APK, compile/prepare web assets in `www/` and synchronize them with Capacitor:

```bash
# From workspace root:
npx cap sync android
```

This step performs:
- Copies web assets (`www/`) to `android/app/src/main/assets/public/`
- Copies all 11 local ONNX model files to `android/app/src/main/assets/public/models/`
- Links Capacitor Android plugins (`@capacitor/app`, `CameraBridge`, `OnnxInference`, `VoiceRecognition`)

---

## 3. Assembling the Android Debug APK

To compile the native Android application using the Gradle wrapper:

### Windows (PowerShell / Command Prompt):
```cmd
set JAVA_HOME=C:\Users\Tanish\.jdks\jdk-17
set PATH=%JAVA_HOME%\bin;%PATH%
cd android
gradlew.bat assembleDebug
```

### Linux / macOS:
```bash
export JAVA_HOME=/path/to/jdk-17
export PATH=$JAVA_HOME/bin:$PATH
cd android
./gradlew assembleDebug
```

---

## 4. Output APK Location

Upon successful build completion (`BUILD SUCCESSFUL`), the generated APK will be located at:
```
android/app/build/outputs/apk/debug/app-debug.apk
```

For distribution and QA testing, copy the APK to the root workspace with the designated release name:
```bash
copy android\app\build\outputs\apk\debug\app-debug.apk SAP_Smart_Agriculture_Platform_FINAL.apk
```

---

## 5. Installing the APK on a Device / Emulator

### Via Android Debug Bridge (ADB):
```bash
# Ensure device/emulator is connected
adb devices

# Install APK onto device
adb install -r SAP_Smart_Agriculture_Platform_FINAL.apk

# Launch Main Activity
adb shell am start -n com.sap.agri/.MainActivity
```

---

## 6. Built-in Native Capabilities & Permissions

The compiled APK includes native plugins configured in `com.sap.agri`:
- **`OnnxInferencePlugin`**: Native Microsoft ONNX Runtime (`ai.onnxruntime:onnxruntime-android:1.18.0`) executing on-device inference for all 10 crops and `Not_A_Leaf` gatekeeper model.
- **`CameraBridgePlugin`**: Android Camera2 integration handling permissions, lens selection (front/rear), and real-time scanning.
- **`VoiceRecognitionPlugin`**: Native Android `SpeechRecognizer` with bilingual English and Hindi speech recognition.
- **Hardware Back Button**: Handled via Capacitor App plugin + `MainActivity.onBackPressed()` override to safely dismiss modals, navigate back to Dashboard, or exit the application cleanly.
