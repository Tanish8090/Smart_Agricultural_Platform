# SAP Crop Disease System — Model Validation Report

**Date**: 29-09-2026
**Overall Status**: ALL CHECKS PASSED (11/11)

## Summary Validation Table

| Crop | Model Exists | Classes Correct | Loadable | Status |
| :--- | :---: | :---: | :---: | :---: |
| **Wheat** | YES | YES | YES | **PASSED** |
| **Cotton** | YES | YES | YES | **PASSED** |
| **Sugarcane** | YES | YES | YES | **PASSED** |
| **Potato** | YES | YES | YES | **PASSED** |
| **Rice** | YES | YES | YES | **PASSED** |
| **Soybean** | YES | YES | YES | **PASSED** |
| **Tomato** | YES | YES | YES | **PASSED** |
| **Corn** | YES | YES | YES | **PASSED** |
| **Apple** | YES | YES | YES | **PASSED** |
| **Grape** | YES | YES | YES | **PASSED** |
| **Not_A_Leaf** | YES | YES | YES | **PASSED** |

## Detailed Model Class Verification

### Wheat
- **Model Path**: `models/wheat/best.pt`
- **Expected Classes**: `['Wheat___Yellow_rust', 'Wheat___healthy']`
- **Actual Classes**: `['Wheat___Yellow_rust', 'Wheat___healthy']`
- **Status**: `PASSED`

### Cotton
- **Model Path**: `models/cotton/best.pt`
- **Expected Classes**: `['Cotton___Bacterial_blight', 'Cotton___healthy']`
- **Actual Classes**: `['Cotton___Bacterial_blight', 'Cotton___healthy']`
- **Status**: `PASSED`

### Sugarcane
- **Model Path**: `models/sugarcane/best.pt`
- **Expected Classes**: `['Sugarcane___Red_rot', 'Sugarcane___healthy']`
- **Actual Classes**: `['Sugarcane___Red_rot', 'Sugarcane___healthy']`
- **Status**: `PASSED`

### Potato
- **Model Path**: `models/potato/best.pt`
- **Expected Classes**: `['Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy']`
- **Actual Classes**: `['Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy']`
- **Status**: `PASSED`

### Rice
- **Model Path**: `models/rice/best.pt`
- **Expected Classes**: `['Rice___Blast', 'Rice___Brown_spot', 'Rice___healthy']`
- **Actual Classes**: `['Rice___Blast', 'Rice___Brown_spot', 'Rice___healthy']`
- **Status**: `PASSED`

### Soybean
- **Model Path**: `models/soybean/best.pt`
- **Expected Classes**: `['Soybean___Rust', 'Soybean___healthy']`
- **Actual Classes**: `['Soybean___Rust', 'Soybean___healthy']`
- **Status**: `PASSED`

### Tomato
- **Model Path**: `models/tomato/best.pt`
- **Expected Classes**: `['Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___healthy']`
- **Actual Classes**: `['Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___healthy']`
- **Status**: `PASSED`

### Corn
- **Model Path**: `models/corn/best.pt`
- **Expected Classes**: `['Corn___Common_rust', 'Corn___Leaf_blight', 'Corn___healthy']`
- **Actual Classes**: `['Corn___Common_rust', 'Corn___Leaf_blight', 'Corn___healthy']`
- **Status**: `PASSED`

### Apple
- **Model Path**: `models/apple/best.pt`
- **Expected Classes**: `['Apple___Scab', 'Apple___healthy']`
- **Actual Classes**: `['Apple___Scab', 'Apple___healthy']`
- **Status**: `PASSED`

### Grape
- **Model Path**: `models/grape/best.pt`
- **Expected Classes**: `['Grape___Black_rot', 'Grape___healthy']`
- **Actual Classes**: `['Grape___Black_rot', 'Grape___healthy']`
- **Status**: `PASSED`

### Not_A_Leaf
- **Model Path**: `models/not_a_leaf/best.pt`
- **Expected Classes**: `['Not_A_Leaf', 'Plant_Leaf']`
- **Actual Classes**: `['Not_A_Leaf', 'Plant_Leaf']`
- **Status**: `PASSED`
