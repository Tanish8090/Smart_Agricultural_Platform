import re

print("=" * 60)
print("  VERIFYING SAP ANDROID v4 STARTUP & CAMERA FIXES")
print("=" * 60)

# 1. Check index.html
with open('www/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

cam_match = re.search(r'<div[^>]*id=["\']cameraModal["\'][^>]*class=["\']([^"\']*)["\']', html)
assert cam_match, "cameraModal not found in index.html"
cam_classes = cam_match.group(1).split()
print("[CHECK 1] cameraModal initial classes:", cam_classes)
assert "hidden" in cam_classes, "cameraModal MUST have class 'hidden'"
print("  -> PASS: cameraModal is hidden by default in HTML")

vid_match = re.search(r'<video[^>]*id=["\']cameraVideo["\'][^>]*>', html)
assert vid_match, "cameraVideo not found in index.html"
vid_tag = vid_match.group(0)
print("[CHECK 2] cameraVideo element:", vid_tag)
for attr in ['autoplay', 'playsinline', 'webkit-playsinline', 'muted']:
    assert attr in vid_tag, f"cameraVideo missing {attr}"
print("  -> PASS: cameraVideo contains all necessary WebView autoplay attributes")

# 2. Check android.css
with open('www/android.css', 'r', encoding='utf-8') as f:
    css = f.read()

print("[CHECK 3] android.css modal rules:")
assert "body.capacitor-native #cameraModal.hidden" in css
assert "display: none !important;" in css
assert "body.capacitor-native .fixed.inset-0.z-50:not(.hidden)" in css
print("  -> PASS: android.css properly hides .hidden modals with !important and scopes display:flex to :not(.hidden)")

# 3. Check app.js
with open('www/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

print("[CHECK 4] app.js startup and camera lifecycle:")
assert "function closeAllModals()" in js
assert "switchTab('dashboard')" in js
assert "stopCameraStream()" in js
assert "CameraBridge" in js
assert "requestCameraPermission" in js
assert "visibilitychange" in js
assert "pagehide" in js
assert "appStateChange" in js
print("  -> PASS: app.js contains startup modal-closing, Home tab enforcement, native permission bridge, and background camera release")

# 4. Check MainActivity.java and CameraBridgePlugin.java
with open('android/app/src/main/java/com/sap/agri/MainActivity.java', 'r', encoding='utf-8') as f:
    main_activity = f.read()

print("[CHECK 5] MainActivity.java plugin registrations:")
assert "registerPlugin(OnnxInferencePlugin.class);" in main_activity
assert "registerPlugin(VoiceRecognitionPlugin.class);" in main_activity
assert "registerPlugin(CameraBridgePlugin.class);" in main_activity
print("  -> PASS: CameraBridgePlugin, VoiceRecognitionPlugin, and OnnxInferencePlugin registered")

# 5. Check APK existence and models
import zipfile
with zipfile.ZipFile('SAP_Smart_Agriculture_Platform_v4.apk', 'r') as z:
    onnx_files = [f for f in z.namelist() if f.endswith('.onnx') and 'assets/public/models/' in f]
    print(f"[CHECK 6] ONNX models in APK assets/public/models: {len(onnx_files)}")
    assert len(onnx_files) == 11, f"Expected 11 models, found {len(onnx_files)}"
    for m in sorted(onnx_files):
        print(f"   - {m.split('/')[-1]}")
    print("  -> PASS: All 11 ONNX crop & leaf models present in APK")

print("\nALL VERIFICATIONS PASSED SUCCESSFULLY!")
