# ONNX Model Conversion & Validation Report

**Date:** 2026-09-29 20:17:21
**Runtime:** ONNX Runtime & Ultralytics YOLOv11n-cls
**Target Platform:** Android Local On-Device Inference (No Cloud API)

## 1. Summary

A total of **11** models were converted to ONNX and validated:
- 10 Crop-Specific Disease Classification Models
- 1 Not_A_Leaf Binary Classification Gatekeeper Model

## 2. Model Specifications & Validation Results

| Crop / Model | ONNX File | Size (MB) | Input Shape | Output Shape | Classes | Sample Image | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **wheat** | `wheat.onnx` | 5.88 MB | `[1, 3, 224, 224]` | `[1, 2]` | 2 | `test_0_484784b4.jpg` | **PASSED** |
| **cotton** | `cotton.onnx` | 5.88 MB | `[1, 3, 224, 224]` | `[1, 2]` | 2 | `test_0_677a1b6f.jpg` | **PASSED** |
| **sugarcane** | `sugarcane.onnx` | 5.88 MB | `[1, 3, 224, 224]` | `[1, 2]` | 2 | `test_0_29a3c243.jpg` | **PASSED** |
| **potato** | `potato.onnx` | 5.88 MB | `[1, 3, 224, 224]` | `[1, 3]` | 3 | `Potato___Early_blight_0000.jpg` | **PASSED** |
| **rice** | `rice.onnx` | 5.88 MB | `[1, 3, 224, 224]` | `[1, 3]` | 3 | `Rice___Blast_0000.jpg` | **PASSED** |
| **soybean** | `soybean.onnx` | 5.88 MB | `[1, 3, 224, 224]` | `[1, 2]` | 2 | `test_0_206d3e91.jpg` | **PASSED** |
| **tomato** | `tomato.onnx` | 5.88 MB | `[1, 3, 224, 224]` | `[1, 3]` | 3 | `Tomato___Early_blight_0000.jpg` | **PASSED** |
| **corn** | `corn.onnx` | 5.88 MB | `[1, 3, 224, 224]` | `[1, 3]` | 3 | `Corn___Common_rust_0000.jpg` | **PASSED** |
| **apple** | `apple.onnx` | 5.88 MB | `[1, 3, 224, 224]` | `[1, 2]` | 2 | `Apple___healthy_0000.jpg` | **PASSED** |
| **grape** | `grape.onnx` | 5.88 MB | `[1, 3, 224, 224]` | `[1, 2]` | 2 | `Grape___Black_rot_0000.jpg` | **PASSED** |
| **not_a_leaf** | `not_a_leaf.onnx` | 5.88 MB | `[1, 3, 224, 224]` | `[1, 2]` | 2 | `test_0.jpg` | **PASSED** |

## 3. Numerical Parity Verification (PyTorch .pt vs ONNX)

| Model | PyTorch Prediction | ONNX Prediction | Max Probability Diff | Parity |
| :--- | :--- | :--- | :--- | :--- |
| **wheat** | Wheat___healthy (0.9996) | Wheat___healthy (0.9996) | 0.000002 | `PASSED` |
| **cotton** | Cotton___Bacterial_blight (0.9967) | Cotton___Bacterial_blight (0.9967) | 0.000004 | `PASSED` |
| **sugarcane** | Sugarcane___healthy (0.9347) | Sugarcane___healthy (0.9352) | 0.000442 | `PASSED` |
| **potato** | Potato___Early_blight (1.0000) | Potato___Early_blight (1.0000) | 0.000000 | `PASSED` |
| **rice** | Rice___Blast (0.9996) | Rice___Blast (0.9996) | 0.000002 | `PASSED` |
| **soybean** | Soybean___healthy (1.0000) | Soybean___healthy (1.0000) | 0.000000 | `PASSED` |
| **tomato** | Tomato___Early_blight (0.9992) | Tomato___Early_blight (0.9992) | 0.000001 | `PASSED` |
| **corn** | Corn___Common_rust (1.0000) | Corn___Common_rust (1.0000) | 0.000000 | `PASSED` |
| **apple** | Apple___healthy (1.0000) | Apple___healthy (1.0000) | 0.000000 | `PASSED` |
| **grape** | Grape___Black_rot (1.0000) | Grape___Black_rot (1.0000) | 0.000000 | `PASSED` |
| **not_a_leaf** | Not_A_Leaf (0.7011) | Not_A_Leaf (0.6997) | 0.001355 | `PASSED` |

## 4. Central Model Registry (`models/model_config.json`)

```json
{
  "wheat": {
    "model": "wheat.onnx",
    "classes": [
      "Wheat___Yellow_rust",
      "Wheat___healthy"
    ]
  },
  "cotton": {
    "model": "cotton.onnx",
    "classes": [
      "Cotton___Bacterial_blight",
      "Cotton___healthy"
    ]
  },
  "sugarcane": {
    "model": "sugarcane.onnx",
    "classes": [
      "Sugarcane___Red_rot",
      "Sugarcane___healthy"
    ]
  },
  "potato": {
    "model": "potato.onnx",
    "classes": [
      "Potato___Early_blight",
      "Potato___Late_blight",
      "Potato___healthy"
    ]
  },
  "rice": {
    "model": "rice.onnx",
    "classes": [
      "Rice___Blast",
      "Rice___Brown_spot",
      "Rice___healthy"
    ]
  },
  "soybean": {
    "model": "soybean.onnx",
    "classes": [
      "Soybean___Rust",
      "Soybean___healthy"
    ]
  },
  "tomato": {
    "model": "tomato.onnx",
    "classes": [
      "Tomato___Early_blight",
      "Tomato___Late_blight",
      "Tomato___healthy"
    ]
  },
  "corn": {
    "model": "corn.onnx",
    "classes": [
      "Corn___Common_rust",
      "Corn___Leaf_blight",
      "Corn___healthy"
    ]
  },
  "apple": {
    "model": "apple.onnx",
    "classes": [
      "Apple___Scab",
      "Apple___healthy"
    ]
  },
  "grape": {
    "model": "grape.onnx",
    "classes": [
      "Grape___Black_rot",
      "Grape___healthy"
    ]
  },
  "not_a_leaf": {
    "model": "not_a_leaf.onnx",
    "classes": [
      "Not_A_Leaf",
      "Plant_Leaf"
    ]
  }
}
```

## 5. Architectural Alignment

- **Format:** ONNX Opset 18 with onnxslim optimization
- **Input Tensor:** `[1, 3, 224, 224]` Float32 normalized to `[0.0, 1.0]` (NCHW format, RGB channel order)
- **Output Tensor:** `[1, num_classes]` Float32 logits
- **Postprocessing:** Softmax over output tensor yields class confidence probabilities
- **Zero Cloud Dependencies:** All inference is executed locally using ONNX Runtime.
