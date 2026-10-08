# Final Model Class Audit Report

**Audit Date:** 2026-09-29  
**Status:** ALL MODELS VERIFIED & VALIDATED  
**Requirement:** Strict alignment with required class configurations without extra/unrelated classes.

---

## 1. Class Configuration Summary Table

| Crop / Target | Required Count | Actual PT Count | Actual ONNX Count | ONNX Output Shape | Extra Classes | Missing Classes | Audit Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Wheat** | 2 | 2 | 2 | `[1, 2]` | None | None | **PASS** |
| **Cotton** | 2 | 2 | 2 | `[1, 2]` | None | None | **PASS** |
| **Sugarcane** | 2 | 2 | 2 | `[1, 2]` | None | None | **PASS** |
| **Potato** | 3 | 3 | 3 | `[1, 3]` | None | None | **PASS** |
| **Rice** | 3 | 3 | 3 | `[1, 3]` | None | None | **PASS** |
| **Soybean** | 2 | 2 | 2 | `[1, 2]` | None | None | **PASS** |
| **Tomato** | 3 | 3 | 3 | `[1, 3]` | None | None | **PASS** |
| **Corn** | 3 | 3 | 3 | `[1, 3]` | None | None | **PASS** |
| **Apple** | 2 | 2 | 2 | `[1, 2]` | None | None | **PASS** |
| **Grape** | 2 | 2 | 2 | `[1, 2]` | None | None | **PASS** |
| **Not_A_Leaf** | 1 (Binary) | 2 | 2 | `[1, 2]` | None | None | **PASS** |

---

## 2. Detailed Per-Model Class Audit

### WHEAT
- **PyTorch Model:** [models/wheat/best.pt](file:///c:/Users/Tanish/OneDrive/Desktop/SAP%202/models/wheat/best.pt)
- **ONNX Model:** [models/wheat/best.onnx](file:///c:/Users/Tanish/OneDrive/Desktop/SAP%202/models/wheat/best.onnx)
- **Required Classes (2):** `['Wheat___Yellow_rust', 'Wheat___healthy']`
- **PyTorch Classes (2):** `['Wheat___Yellow_rust', 'Wheat___healthy']`
- **ONNX Classes (2):** `['Wheat___Yellow_rust', 'Wheat___healthy']`
- **ONNX Tensor Dimension:** `[1, 2]`
- **Extra Classes:** None
- **Missing Classes:** None
- **Verdict:** **PASS**

### COTTON
- **PyTorch Model:** [models/cotton/best.pt](file:///c:/Users/Tanish/OneDrive/Desktop/SAP%202/models/cotton/best.pt)
- **ONNX Model:** [models/cotton/best.onnx](file:///c:/Users/Tanish/OneDrive/Desktop/SAP%202/models/cotton/best.onnx)
- **Required Classes (2):** `['Cotton___Bacterial_blight', 'Cotton___healthy']`
- **PyTorch Classes (2):** `['Cotton___Bacterial_blight', 'Cotton___healthy']`
- **ONNX Classes (2):** `['Cotton___Bacterial_blight', 'Cotton___healthy']`
- **ONNX Tensor Dimension:** `[1, 2]`
- **Extra Classes:** None
- **Missing Classes:** None
- **Verdict:** **PASS**

### SUGARCANE
- **PyTorch Model:** [models/sugarcane/best.pt](file:///c:/Users/Tanish/OneDrive/Desktop/SAP%202/models/sugarcane/best.pt)
- **ONNX Model:** [models/sugarcane/best.onnx](file:///c:/Users/Tanish/OneDrive/Desktop/SAP%202/models/sugarcane/best.onnx)
- **Required Classes (2):** `['Sugarcane___Red_rot', 'Sugarcane___healthy']`
- **PyTorch Classes (2):** `['Sugarcane___Red_rot', 'Sugarcane___healthy']`
- **ONNX Classes (2):** `['Sugarcane___Red_rot', 'Sugarcane___healthy']`
- **ONNX Tensor Dimension:** `[1, 2]`
- **Extra Classes:** None
- **Missing Classes:** None
- **Verdict:** **PASS**

### POTATO
- **PyTorch Model:** [models/potato/best.pt](file:///c:/Users/Tanish/OneDrive/Desktop/SAP%202/models/potato/best.pt)
- **ONNX Model:** [models/potato/best.onnx](file:///c:/Users/Tanish/OneDrive/Desktop/SAP%202/models/potato/best.onnx)
- **Required Classes (3):** `['Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy']`
- **PyTorch Classes (3):** `['Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy']`
- **ONNX Classes (3):** `['Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy']`
- **ONNX Tensor Dimension:** `[1, 3]`
- **Extra Classes:** None
- **Missing Classes:** None
- **Verdict:** **PASS**

### RICE
- **PyTorch Model:** [models/rice/best.pt](file:///c:/Users/Tanish/OneDrive/Desktop/SAP%202/models/rice/best.pt)
- **ONNX Model:** [models/rice/best.onnx](file:///c:/Users/Tanish/OneDrive/Desktop/SAP%202/models/rice/best.onnx)
- **Required Classes (3):** `['Rice___Blast', 'Rice___Brown_spot', 'Rice___healthy']`
- **PyTorch Classes (3):** `['Rice___Blast', 'Rice___Brown_spot', 'Rice___healthy']`
- **ONNX Classes (3):** `['Rice___Blast', 'Rice___Brown_spot', 'Rice___healthy']`
- **ONNX Tensor Dimension:** `[1, 3]`
- **Extra Classes:** None
- **Missing Classes:** None
- **Verdict:** **PASS**

### SOYBEAN
- **PyTorch Model:** [models/soybean/best.pt](file:///c:/Users/Tanish/OneDrive/Desktop/SAP%202/models/soybean/best.pt)
- **ONNX Model:** [models/soybean/best.onnx](file:///c:/Users/Tanish/OneDrive/Desktop/SAP%202/models/soybean/best.onnx)
- **Required Classes (2):** `['Soybean___Rust', 'Soybean___healthy']`
- **PyTorch Classes (2):** `['Soybean___Rust', 'Soybean___healthy']`
- **ONNX Classes (2):** `['Soybean___Rust', 'Soybean___healthy']`
- **ONNX Tensor Dimension:** `[1, 2]`
- **Extra Classes:** None
- **Missing Classes:** None
- **Verdict:** **PASS**

### TOMATO
- **PyTorch Model:** [models/tomato/best.pt](file:///c:/Users/Tanish/OneDrive/Desktop/SAP%202/models/tomato/best.pt)
- **ONNX Model:** [models/tomato/best.onnx](file:///c:/Users/Tanish/OneDrive/Desktop/SAP%202/models/tomato/best.onnx)
- **Required Classes (3):** `['Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___healthy']`
- **PyTorch Classes (3):** `['Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___healthy']`
- **ONNX Classes (3):** `['Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___healthy']`
- **ONNX Tensor Dimension:** `[1, 3]`
- **Extra Classes:** None
- **Missing Classes:** None
- **Verdict:** **PASS**

### CORN
- **PyTorch Model:** [models/corn/best.pt](file:///c:/Users/Tanish/OneDrive/Desktop/SAP%202/models/corn/best.pt)
- **ONNX Model:** [models/corn/best.onnx](file:///c:/Users/Tanish/OneDrive/Desktop/SAP%202/models/corn/best.onnx)
- **Required Classes (3):** `['Corn___Common_rust', 'Corn___Leaf_blight', 'Corn___healthy']`
- **PyTorch Classes (3):** `['Corn___Common_rust', 'Corn___Leaf_blight', 'Corn___healthy']`
- **ONNX Classes (3):** `['Corn___Common_rust', 'Corn___Leaf_blight', 'Corn___healthy']`
- **ONNX Tensor Dimension:** `[1, 3]`
- **Extra Classes:** None
- **Missing Classes:** None
- **Verdict:** **PASS**

### APPLE
- **PyTorch Model:** [models/apple/best.pt](file:///c:/Users/Tanish/OneDrive/Desktop/SAP%202/models/apple/best.pt)
- **ONNX Model:** [models/apple/best.onnx](file:///c:/Users/Tanish/OneDrive/Desktop/SAP%202/models/apple/best.onnx)
- **Required Classes (2):** `['Apple___Scab', 'Apple___healthy']`
- **PyTorch Classes (2):** `['Apple___Scab', 'Apple___healthy']`
- **ONNX Classes (2):** `['Apple___Scab', 'Apple___healthy']`
- **ONNX Tensor Dimension:** `[1, 2]`
- **Extra Classes:** None
- **Missing Classes:** None
- **Verdict:** **PASS**

### GRAPE
- **PyTorch Model:** [models/grape/best.pt](file:///c:/Users/Tanish/OneDrive/Desktop/SAP%202/models/grape/best.pt)
- **ONNX Model:** [models/grape/best.onnx](file:///c:/Users/Tanish/OneDrive/Desktop/SAP%202/models/grape/best.onnx)
- **Required Classes (2):** `['Grape___Black_rot', 'Grape___healthy']`
- **PyTorch Classes (2):** `['Grape___Black_rot', 'Grape___healthy']`
- **ONNX Classes (2):** `['Grape___Black_rot', 'Grape___healthy']`
- **ONNX Tensor Dimension:** `[1, 2]`
- **Extra Classes:** None
- **Missing Classes:** None
- **Verdict:** **PASS**

### NOT_A_LEAF (Gatekeeper)
- **PyTorch Model:** [models/not_a_leaf/best.pt](file:///c:/Users/Tanish/OneDrive/Desktop/SAP%202/models/not_a_leaf/best.pt)
- **ONNX Model:** [models/not_a_leaf/best.onnx](file:///c:/Users/Tanish/OneDrive/Desktop/SAP%202/models/not_a_leaf/best.onnx)
- **Target Class:** `Not_A_Leaf` (Binary Classifier against `Plant_Leaf`)
- **PyTorch Classes (2):** `['Not_A_Leaf', 'Plant_Leaf']`
- **ONNX Classes (2):** `['Not_A_Leaf', 'Plant_Leaf']`
- **ONNX Tensor Dimension:** `[1, 2]`
- **Function:** Rejects non-leaf images with confidence > 0.50 before routing to crop models.
- **Verdict:** **PASS**

---

## 3. Retraining Verification

No retraining is required because:
1. Every model's PyTorch `.pt` file has already been trained with the exact specified linear classification head and exact target classes.
2. Every `.onnx` model has been exported directly from `best.pt` with identical output dimensions:
   - Wheat = 2
   - Cotton = 2
   - Sugarcane = 2
   - Potato = 3
   - Rice = 3
   - Soybean = 2
   - Tomato = 3
   - Corn = 3
   - Apple = 2
   - Grape = 2
   - Not_A_Leaf = 2 (Binary Classifier)
3. Zero extra classes exist in either PyTorch weights or ONNX computational graphs.
