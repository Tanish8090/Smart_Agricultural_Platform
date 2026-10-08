# SAP Smart Agriculture Platform — Android v4 Bug Fix & Test Report

**Artifact**: `SAP_Smart_Agriculture_Platform_v4.apk`  
**Size**: ~197.34 MB (206,925,100 bytes)  
**Date**: October 1, 2026  
**Build Target**: Android 14 / API 34 (Compiled with JDK 17, Capacitor 7.0)  
**ADB Status**: No real Android physical device or emulator connected (`adb devices` returned 0 attached devices). In strict adherence to project instructions, all tests requiring live physical screen touch/mic/camera hardware are explicitly labeled **NOT VERIFIED (No ADB Device Connected)**, while code-level, asset, and automated verification tests are labeled **VERIFIED**.

---

## 1. Root Cause Analysis

### 1.1 Automatic Camera Modal Opening on App Startup
* **Root Cause**: In `www/android.css`, the modal rule was defined as:
  ```css
  body.capacitor-native .fixed.inset-0.z-50 {
    z-index: 70 !important;
    display: flex !important;
    ...
  }
  ```
  In `www/index.html`, all modal overlays—including the Live Camera modal (`#cameraModal`)—are marked with:
  ```html
  <div id="cameraModal" class="hidden fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4">
  ```
  Because the CSS selector `body.capacitor-native .fixed.inset-0.z-50` specified `display: flex !important;`, it had higher specificity and an `!important` flag that completely overrode Tailwind's `.hidden` (`display: none;`).
  As soon as the app initialized on Android and executed `document.body.classList.add('capacitor-native')`, `#cameraModal` (being the last modal in DOM order) was forced to `display: flex !important` on startup, before any user action occurred and before the Home dashboard could be viewed.

### 1.2 Black/Grey Camera Preview with Large Play Icon
* **Root Cause**:
  1. **Uninitialized Video Element**: Because `#cameraModal` was opened on startup purely by the CSS override rather than via `openCameraModal()`, `cameraVideo.srcObject` was `null`. In Android Chromium WebView, an HTML5 `<video>` element with no active stream or poster renders by default as a dark grey rectangle with a large media play icon in the center.
  2. **Missing Video Autoplay Attributes**: The `<video id="cameraVideo">` tag lacked the `muted` attribute, and `video.muted = true` was never set in JavaScript. In modern Chromium/WebView autoplay policies, any media stream without `muted` is treated as unmuted audio/video and is automatically blocked from playing without a direct user tap on the video element, remaining paused with a play icon.
  3. **Lack of Explicit `.play()` Invocation**: In JavaScript, `video.srcObject = cameraStream` was assigned without waiting for `onloadedmetadata` and without explicitly invoking `await video.play()`.
  4. **Unconstrained WebRTC Fallbacks**: `facingMode: cameraFacing` without fallback handling threw unhandled constraint errors on devices that do not support fixed resolution requests (`1280x720`).

---

## 2. Code Changes Implemented

### 2.1 Modal CSS & Hidden State Scoping (`www/android.css`)
- Replaced unconditional `display: flex !important` with scoped `:not(.hidden)` selectors and explicit `display: none !important` for all hidden modals:
  ```css
  body.capacitor-native .hidden,
  body.capacitor-native .fixed.inset-0.z-50.hidden,
  body.capacitor-native #cameraModal.hidden,
  body.capacitor-native #pincodeModal.hidden,
  body.capacitor-native #farmContextModal.hidden,
  body.capacitor-native #mandiDetailModal.hidden {
    display: none !important;
  }

  body.capacitor-native .fixed.inset-0.z-50:not(.hidden) {
    z-index: 70 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 16px !important;
    padding-top: max(16px, env(safe-area-inset-top)) !important;
    padding-bottom: max(16px, env(safe-area-inset-bottom)) !important;
  }

  body.capacitor-native #cameraModal:not(.hidden) {
    display: flex !important;
  }
  ```
- Styled `#cameraVideo` to fit cleanly inside the preview frame with `max-height: 42dvh !important; object-fit: cover !important; width: 100% !important; height: 100% !important; background-color: #020617 !important;`.

### 2.2 Native Camera Bridge Plugin (`CameraBridgePlugin.java`)
- Created [CameraBridgePlugin.java](file:///c:/Users/Tanish/OneDrive/Desktop/SAP%202/android/app/src/main/java/com/sap/agri/CameraBridgePlugin.java) implementing Capacitor's `@CapacitorPlugin` permission architecture.
- Added runtime permission checks (`checkCameraPermission`), runtime requests (`requestCameraPermission`), and camera hardware inspection (`isCameraAvailable` via Android `CameraManager`).
- Registered `CameraBridgePlugin.class` in [MainActivity.java](file:///c:/Users/Tanish/OneDrive/Desktop/SAP%202/android/app/src/main/java/com/sap/agri/MainActivity.java).

### 2.3 Video Element Attributes (`www/index.html`)
- Updated `<video id="cameraVideo">` with:
  ```html
  <video id="cameraVideo" autoplay playsinline webkit-playsinline muted disablePictureInPicture class="w-full h-full object-cover"></video>
  ```

### 2.4 Application Logic & Camera Lifecycle (`www/app.js`)
- **Startup Protection**: Added `closeAllModals()` and `switchTab('dashboard')` inside `DOMContentLoaded` and `checkCapacitorNative()`. Added guard flag `capacitorInitialized` to prevent repeated or duplicate initialization events.
- **Progressive Camera Stream Resolution**: Implemented `getCameraStream(facing)` with a 4-tier fallback:
  1. High-resolution rear/front (`facingMode: { ideal: facing }, width: { ideal: 1280 }, height: { ideal: 720 }`)
  2. Standard ideal facing (`facingMode: { ideal: facing }`)
  3. String facing mode (`facingMode: facing`)
  4. Universal video fallback (`video: true`)
- **Stream Playback**: Configured `video.muted = true`, `video.playsInline = true`, waited for `onloadedmetadata`, and explicitly called `video.play()` with retry logic.
- **Camera Switching**: `switchCameraFacing()` toggles between `'environment'` (rear) and `'user'` (front), displaying a localized toast notification (e.g., *"पिछला कैमरा (Rear)"* / *"Rear Camera"*), stops the existing stream, and restarts with the new facing mode.
- **Photo Capture & Immediate AI Scan**: `captureCameraPhoto()` verifies frame dimensions, draws to canvas, extracts high-quality JPEG base64, immediately stops the camera stream and closes the modal, populates the preview card, and automatically initiates `analyzePlantDisease()` on the local ONNX inference engine.
- **Hardware Release on Backgrounding**: Added listeners for `visibilitychange`, `pagehide`, and Capacitor `appStateChange` to stop all camera tracks immediately when the app or tab is backgrounded.

---

## 3. Verification Matrix

| # | Test Item | Expected Behavior | Actual Behavior / Verified Result | Status |
|---|-----------|-------------------|-----------------------------------|--------|
| **1** | **App Startup View** | App launches directly to Home screen (`view-dashboard`). | Verified in `training/verify_v4_camera_fixes.py`: `switchTab('dashboard')` and `closeAllModals()` run on launch. | **VERIFIED** *(Code Logic)* / **NOT VERIFIED** *(Device Screen)* |
| **2** | **Camera Modal on Startup** | Camera modal remains completely closed on launch. | Verified: `#cameraModal` has class `hidden`, and `android.css` enforces `display: none !important;`. | **VERIFIED** *(Code & CSS)* / **NOT VERIFIED** *(Device Screen)* |
| **3** | **Explicit Trigger Only** | Camera opens only when user clicks "Launch Camera" / "Live Camera". | Verified: `openCameraModal()` is only wired to the Leaf Scanner card (`#dropZone` sibling) and camera flip. | **VERIFIED** *(Event Triggers)* |
| **4** | **Runtime Permission Bridge** | Native camera permission requested before stream start. | Verified: `CameraBridgePlugin.java` handles `Manifest.permission.CAMERA` at runtime; localized toasts shown on denial. | **VERIFIED** *(Plugin & Manifest)* / **NOT VERIFIED** *(Device Dialog)* |
| **5** | **Rear Camera by Default** | `cameraFacing` defaults to `'environment'`. | Verified: `let cameraFacing = 'environment';` passed to `getCameraStream({ ideal: 'environment' })`. | **VERIFIED** *(Logic)* / **NOT VERIFIED** *(Device Camera)* |
| **6** | **Camera Flip Toggle** | `switchCameraFacing()` toggles front/rear cameras. | Verified: Flips between `'environment'` and `'user'`, restarts stream cleanly without modal reload. | **VERIFIED** *(Logic)* / **NOT VERIFIED** *(Device Camera)* |
| **7** | **Preview Fit & No Distortion** | Video fits 16:9 frame without stretching. | Verified: `object-fit: cover; aspect-video; max-height: 42dvh;` applied in `android.css`. | **VERIFIED** *(CSS)* / **NOT VERIFIED** *(Device Screen)* |
| **8** | **Take Photo & Scan Pipeline** | Captures snapshot and immediately runs local ONNX disease diagnosis. | Verified: `captureCameraPhoto()` draws video frame to canvas, closes camera, and triggers `analyzePlantDisease()`. | **VERIFIED** *(Pipeline)* / **NOT VERIFIED** *(Device Camera)* |
| **9** | **Camera Hardware Release** | Tracks stopped when modal closes or app backgrounds. | Verified: `stopCameraStream()` stops all tracks; bound to `visibilitychange`, `pagehide`, and `appStateChange`. | **VERIFIED** *(Lifecycle Listeners)* |
| **10** | **11 Local ONNX Models** | All 11 models present in APK bundle. | Verified in `verify_v4_camera_fixes.py`: All 11 ONNX files present in `assets/public/models/` and `assets/models/`. | **VERIFIED** *(APK Inspection)* |
| **11** | **Desktop Website Isolation** | Desktop website on `http://localhost:8080/` unchanged. | Verified: HTTP 200, HTML length 196,795 bytes, no bottom navigation, no modal display errors. | **VERIFIED** *(Server Response)* |

---

## 4. Model Verification in `SAP_Smart_Agriculture_Platform_v4.apk`

The final APK (`SAP_Smart_Agriculture_Platform_v4.apk`, 206,925,100 bytes) contains all 11 required local ONNX models:

1. `apple.onnx` (6,161,073 bytes) — Scab / Healthy
2. `corn.onnx` (6,166,224 bytes) — Common Rust / Leaf Blight / Healthy
3. `cotton.onnx` (6,161,086 bytes) — Bacterial Blight / Healthy
4. `grape.onnx` (6,161,076 bytes) — Black Rot / Healthy
5. `not_a_leaf.onnx` (6,161,069 bytes) — Non-crop Leaf & Background Rejection Model
6. `potato.onnx` (6,166,233 bytes) — Early Blight / Late Blight / Healthy
7. `rice.onnx` (6,166,217 bytes) — Blast / Brown Spot / Healthy
8. `soybean.onnx` (6,161,077 bytes) — Rust / Healthy
9. `sugarcane.onnx` (6,161,086 bytes) — Red Rot / Healthy
10. `tomato.onnx` (6,166,233 bytes) — Early Blight / Late Blight / Healthy
11. `wheat.onnx` (6,161,078 bytes) — Yellow Rust / Healthy
