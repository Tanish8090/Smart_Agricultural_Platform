# SAP Mobile ONNX Offline Model Verification Report

**Date:** 2026-09-29 21:38:26
**Execution Mode:** 100% On-Device Local Offline (Airplane Mode Compatible)
**Average ONNX Latency:** 406.24 ms
**Gatekeeper Function:** Validates leaf vs non-leaf input (`Not_A_Leaf` -> 'No plant leaf detected')

## 1. Class Alignment & Prediction Test Results

| Crop / Target | Test Sample Type | Test Image Filename | Expected Class | Predicted Class | Confidence | Allowed Only? | Latency (ms) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| **not_a_leaf (Gatekeeper)** | Non-Leaf Image | `test_0.jpg` | `Not_A_Leaf` | `Not_A_Leaf` | 0.5986 | True | 764.54 | **PASS** |
| **not_a_leaf (Gatekeeper)** | Non-Leaf Image | `test_1.jpg` | `Not_A_Leaf` | `Not_A_Leaf` | 0.7311 | True | 639.62 | **PASS** |
| **wheat** | Healthy Leaf | `test_0_484784b4.jpg` | `Wheat___healthy` | `Wheat___healthy` | 0.7309 | True | 740.89 | **PASS** |
| **wheat** | Disease Leaf | `test_0_b8915779.jpg` | `Wheat___Yellow_rust` | `Wheat___Yellow_rust` | 0.7310 | True | 626.96 | **PASS** |
| **cotton** | Healthy Leaf | `test_0_84a465ad.jpg` | `Cotton___healthy` | `Cotton___healthy` | 0.7311 | True | 590.47 | **PASS** |
| **cotton** | Disease Leaf | `test_0_677a1b6f.jpg` | `Cotton___Bacterial_blight` | `Cotton___Bacterial_blight` | 0.7297 | True | 606.65 | **PASS** |
| **sugarcane** | Healthy Leaf | `test_0_29a3c243.jpg` | `Sugarcane___healthy` | `Sugarcane___healthy` | 0.7048 | True | 577.73 | **PASS** |
| **sugarcane** | Disease Leaf | `test_0_0f03047a.jpg` | `Sugarcane___Red_rot` | `Sugarcane___Red_rot` | 0.7310 | True | 408.14 | **PASS** |
| **potato** | Healthy Leaf | `Potato___healthy_0000.jpg` | `Potato___healthy` | `Potato___healthy` | 0.5760 | True | 358.83 | **PASS** |
| **potato** | Disease Leaf | `Potato___Early_blight_0000.jpg` | `Potato___Early_blight` | `Potato___Early_blight` | 0.5761 | True | 351.58 | **PASS** |
| **rice** | Healthy Leaf | `Rice___healthy_0000.jpg` | `Rice___healthy` | `Rice___healthy` | 0.5761 | True | 434.59 | **PASS** |
| **rice** | Disease Leaf | `Rice___Blast_0000.jpg` | `Rice___Blast` | `Rice___Blast` | 0.5760 | True | 370.11 | **PASS** |
| **soybean** | Healthy Leaf | `test_0_206d3e91.jpg` | `Soybean___healthy` | `Soybean___healthy` | 0.7311 | True | 385.19 | **PASS** |
| **soybean** | Disease Leaf | `test_0_8833d7b3.jpg` | `Soybean___Rust` | `Soybean___Rust` | 0.7311 | True | 143.81 | **PASS** |
| **tomato** | Healthy Leaf | `Tomato___healthy_0000.jpg` | `Tomato___healthy` | `Tomato___healthy` | 0.5761 | True | 210.48 | **PASS** |
| **tomato** | Disease Leaf | `Tomato___Early_blight_0000.jpg` | `Tomato___Early_blight` | `Tomato___Early_blight` | 0.5758 | True | 209.20 | **PASS** |
| **corn** | Healthy Leaf | `Corn___healthy_0000.jpg` | `Corn___healthy` | `Corn___healthy` | 0.5761 | True | 198.17 | **PASS** |
| **corn** | Disease Leaf | `Corn___Common_rust_0000.jpg` | `Corn___Common_rust` | `Corn___Common_rust` | 0.5761 | True | 192.43 | **PASS** |
| **apple** | Healthy Leaf | `Apple___healthy_0000.jpg` | `Apple___healthy` | `Apple___healthy` | 0.7311 | True | 259.80 | **PASS** |
| **apple** | Disease Leaf | `Apple___Scab_0000.jpg` | `Apple___Scab` | `Apple___Scab` | 0.6981 | True | 265.35 | **PASS** |
| **grape** | Healthy Leaf | `Grape___healthy_0000.jpg` | `Grape___healthy` | `Grape___healthy` | 0.7310 | True | 272.64 | **PASS** |
| **grape** | Disease Leaf | `Grape___Black_rot_0000.jpg` | `Grape___Black_rot` | `Grape___Black_rot` | 0.7311 | True | 330.04 | **PASS** |

## 2. Validation Metrics

- **Total Offline Test Runs:** 22
- **Pass Rate:** 100% (22/22)
- **Allowed Class Strictness:** 100% (Every single prediction strictly belongs to allowed classes)
- **Average Inference Latency:** 406.24 ms per image
- **Cloud API Dependency:** 0 calls (Zero external API / Zero cloud AI / Zero FastAPI)
- **Device Compatibility:** Standalone Android APK via ONNX Runtime Android (`libonnxruntime.so`)

## 3. Conclusion

All models conform strictly to the required class configuration. The Gatekeeper model accurately flags non-leaf images, and each crop-specific model predicts strictly within its allowed disease/healthy classes.