# Crop Disease AI Pipeline — Training & Evaluation Summary

**Execution Date**: 2026-09-29 00:48:29  
**Active Device**: `0`  
**Architecture**: Ultralytics YOLO Classification (`yolo11n-cls.pt`)  
**Input Image Size**: 224x224  
**Epochs**: 30 (with patience=5 early stopping)  
**Total Training Time**: 12.47 minutes  

---

## 1. Discovered and Downloaded Datasets

### Local Archives Extracted:
- `archive (1).zip` -> Wheat Disease Dataset (999 images: Yellow Rust, Healthy, Brown Rust, Mildew, Septoria)
- `archive (2).zip` -> Cotton Augmented Dataset (7000 images: Bacterial Blight, Healthy Leaf, etc.)
- `archive (3).zip` -> Sugarcane Leafs Dataset (19926 images: Red Rot, Healthy, Mosaic, etc.)
- `archive (4).zip` -> Potato Late Blight Dataset (430 images: Late Blight, Healthy)

### Hugging Face Datasets Downloaded:
- `Project-AgML/rice_leaf_disease_classification` -> 3 Parquet files (~1.0 GB)
- `Project-AgML/rice_leaf_disease_classification_india` -> 1 Parquet file (~200 MB)
- `Project-AgML/MH_SoyaHealthVision_disease_classification_leaf` -> 13 Parquet files (~6.1 GB, 2782 images: Rust, Healthy, etc.)
- `Project-AgML/SoyNet_leaf_health_classification` -> Verified snapshot

---

## 2. Crop Mapping & Class Balancing

| Crop | Class | Train | Val | Test | Total |
|---|---|---|---|---|---|
| wheat | Wheat___Yellow_rust | 167 | 35 | 37 | 239 |
| wheat | Wheat___healthy | 167 | 18 | 19 | 204 |
| cotton | Cotton___Bacterial_blight | 631 | 134 | 135 | 900 |
| cotton | Cotton___healthy | 631 | 135 | 136 | 902 |
| sugarcane | Sugarcane___Red_rot | 840 | 180 | 180 | 1200 |
| sugarcane | Sugarcane___healthy | 819 | 175 | 177 | 1171 |
| potato | Potato___Late_blight | 253 | 10 | 11 | 274 |
| potato | Potato___healthy | 253 | 54 | 55 | 362 |
| rice | Rice___Blast | 1105 | 236 | 238 | 1579 |
| rice | Rice___healthy | 800 | 97 | 99 | 996 |
| soybean | Soybean___Rust | 596 | 127 | 129 | 852 |
| soybean | Soybean___healthy | 596 | 30 | 32 | 658 |
| not_a_leaf | Not_A_Leaf | 200 | 3 | 3 | 206 |
| not_a_leaf | Plant_Leaf | 175 | 37 | 38 | 250 |

---

## 3. Trained Crop Models & Test Metrics

| Crop | Weights Path | Test Accuracy | Precision | Recall | F1 Score | Test Samples |
|---|---|---|---|---|---|---|
| **WHEAT** | `models/wheat/best.pt` | 94.64% | 94.64% | 94.64% | 94.61% | 56 |
| **COTTON** | `models/cotton/best.pt` | 100.00% | 100.00% | 100.00% | 100.00% | 271 |
| **SUGARCANE** | `models/sugarcane/best.pt` | 91.32% | 91.32% | 91.32% | 91.32% | 357 |
| **POTATO** | `models/potato/best.pt` | 98.48% | 98.61% | 98.48% | 98.51% | 66 |
| **RICE** | `models/rice/best.pt` | 100.00% | 100.00% | 100.00% | 100.00% | 337 |
| **SOYBEAN** | `models/soybean/best.pt` | 100.00% | 100.00% | 100.00% | 100.00% | 161 |
| **NOT_A_LEAF** | `models/not_a_leaf/best.pt` | 100.00% | 100.00% | 100.00% | 100.00% | 41 |

---

## 4. Crops Marked as DATASET_NOT_READY (Rule 22)

The following crops did not have datasets in local archives or specified Hugging Face repositories:
- **TOMATO**: DATASET_NOT_READY: No local archive or HF repository present in workspace for Tomato Early Blight & Healthy
- **CORN**: DATASET_NOT_READY: No local archive or HF repository present in workspace for Corn Common Rust & Healthy
- **APPLE**: DATASET_NOT_READY: No local archive or HF repository present in workspace for Apple Scab & Healthy
- **GRAPE**: DATASET_NOT_READY: No local archive or HF repository present in workspace for Grape Downy Mildew & Healthy

Per strict Rule 22, no fake images or synthetic labels were invented for missing crops.

---

## 5. Important Quality, Safety & Out-Of-Domain Warnings

1. **Not_A_Leaf Model**:
   - The Not_A_Leaf collection is small. High training accuracy does **NOT** guarantee real-world invariance across all unconstrained out-of-domain objects.
   - Thresholds are configurable in `models/model_config.json`.
2. **Realistic Expectations**:
   - Validation and test scores on clean, controlled benchmark datasets (e.g. lab/leaf backgrounds) are typically higher than noisy field conditions with shadows, multi-leaf overlaps, or severe camera blur.
   - This platform is a prototype decision-support tool, not a medical-style diagnosis system.

---
