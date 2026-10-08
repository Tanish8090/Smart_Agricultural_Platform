import os
import sys
import json
import time
import subprocess
import torch

sys.stdout.reconfigure(encoding='utf-8')

from train_crop import train_crop_model, detect_device
from evaluate_models import evaluate_crop_model

AVAILABLE_CROPS = ['wheat', 'cotton', 'sugarcane', 'potato', 'rice', 'soybean', 'not_a_leaf']
MISSING_CROPS = {
    'tomato': 'DATASET_NOT_READY: No local archive or HF repository present in workspace for Tomato Early Blight & Healthy',
    'corn': 'DATASET_NOT_READY: No local archive or HF repository present in workspace for Corn Common Rust & Healthy',
    'apple': 'DATASET_NOT_READY: No local archive or HF repository present in workspace for Apple Scab & Healthy',
    'grape': 'DATASET_NOT_READY: No local archive or HF repository present in workspace for Grape Downy Mildew & Healthy'
}

def main():
    print("=" * 70)
    print("STARTING FULL END-TO-END MODEL TRAINING PIPELINE")
    print("=" * 70)

    device = detect_device()
    print(f"Active Device: {device}")

    # Results tracking
    trained_models = {}
    failed_models = {}
    evaluation_results = {}

    start_time = time.time()

    for crop in AVAILABLE_CROPS:
        print(f"\n>>> PROCESSING: {crop.upper()} <<<")
        try:
            # 30 epochs as requested in prompt, with early stopping
            success, info = train_crop_model(crop, epochs=30, imgsz=224, initial_batch=32)
            if success:
                trained_models[crop] = info
                print(f"[EVALUATING] Running test evaluation for {crop} ...")
                eval_metrics = evaluate_crop_model(crop)
                if eval_metrics:
                    evaluation_results[crop] = eval_metrics
            else:
                failed_models[crop] = info
        except Exception as e:
            print(f"[FAILED] Unexpected exception training {crop}: {e}")
            failed_models[crop] = str(e)
            continue

    total_duration = time.time() - start_time
    print("\n" + "=" * 70)
    print(f"ALL TRAINING COMPLETED IN {total_duration:.1f}s")
    print("=" * 70)

    # Build model_registry.json
    registry = {
        "device": str(device),
        "trained_models": {},
        "not_ready_crops": MISSING_CROPS,
        "evaluation_summary": {}
    }

    for crop, meta in trained_models.items():
        best_pt_path = os.path.abspath(os.path.join('models', crop, 'best.pt'))
        registry["trained_models"][crop] = {
            "status": "READY",
            "weights_path": best_pt_path.replace('\\', '/'),
            "model_type": meta.get("model_type", "classification"),
            "classes": meta.get("classes", []),
            "image_size": meta.get("image_size", 224),
            "epochs": meta.get("epochs", 30)
        }

    for crop, ev in evaluation_results.items():
        registry["evaluation_summary"][crop] = {
            "accuracy": ev.get("accuracy"),
            "precision": ev.get("precision_weighted"),
            "recall": ev.get("recall_weighted"),
            "f1": ev.get("f1_weighted"),
            "test_samples": ev.get("test_samples")
        }

    registry_path = os.path.join('training', 'model_registry.json')
    with open(registry_path, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2)
    print(f"[REGISTRY] Saved {registry_path}")

    # Also save models/model_config.json for inference engine
    models_config = {
        "device": str(device),
        "not_a_leaf_model": os.path.abspath('models/not_a_leaf/best.pt').replace('\\', '/'),
        "not_a_leaf_threshold": 0.50,
        "min_confidence_threshold": 0.40,
        "crop_models": {
            crop: os.path.abspath(os.path.join('models', crop, 'best.pt')).replace('\\', '/')
            for crop in trained_models.keys() if crop != 'not_a_leaf'
        },
        "not_ready_crops": list(MISSING_CROPS.keys())
    }
    with open(os.path.join('models', 'model_config.json'), 'w', encoding='utf-8') as f:
        json.dump(models_config, f, indent=2)
    print("[CONFIG] Saved models/model_config.json")

    # Generate training/TRAINING_SUMMARY.md
    summary_md = f"""# Crop Disease AI Pipeline — Training & Evaluation Summary

**Execution Date**: {time.strftime('%Y-%m-%d %H:%M:%S')}  
**Active Device**: `{device}`  
**Architecture**: Ultralytics YOLO Classification (`yolo11n-cls.pt`)  
**Input Image Size**: 224x224  
**Epochs**: 30 (with patience=5 early stopping)  
**Total Training Time**: {total_duration / 60:.2f} minutes  

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
"""
    for crop in AVAILABLE_CROPS:
        rep_p = os.path.join('datasets', crop, 'dataset_report.json')
        if os.path.exists(rep_p):
            with open(rep_p, 'r', encoding='utf-8') as rf:
                rdata = json.load(rf)
                if 'classes' in rdata and isinstance(rdata['classes'], dict):
                    for c_name, cnts in rdata['classes'].items():
                        summary_md += f"| {crop} | {c_name} | {cnts.get('train', 0)} | {cnts.get('val', 0)} | {cnts.get('test', 0)} | {cnts.get('total', 0)} |\n"
                elif 'classes' in rdata and isinstance(rdata['classes'], list):
                    for c_name in rdata['classes']:
                        tr = rdata.get('train', {}).get(c_name, 0)
                        va = rdata.get('val', {}).get(c_name, 0)
                        te = rdata.get('test', {}).get(c_name, 0)
                        summary_md += f"| {crop} | {c_name} | {tr} | {va} | {te} | {tr+va+te} |\n"

    summary_md += f"""
---

## 3. Trained Crop Models & Test Metrics

| Crop | Weights Path | Test Accuracy | Precision | Recall | F1 Score | Test Samples |
|---|---|---|---|---|---|---|
"""
    for crop in AVAILABLE_CROPS:
        ev = evaluation_results.get(crop, {})
        wpath = f"`models/{crop}/best.pt`"
        acc = f"{ev.get('accuracy', 0)*100:.2f}%" if ev else "N/A"
        prec = f"{ev.get('precision_weighted', 0)*100:.2f}%" if ev else "N/A"
        rec = f"{ev.get('recall_weighted', 0)*100:.2f}%" if ev else "N/A"
        f1 = f"{ev.get('f1_weighted', 0)*100:.2f}%" if ev else "N/A"
        samples = ev.get('test_samples', 0) if ev else "N/A"
        summary_md += f"| **{crop.upper()}** | {wpath} | {acc} | {prec} | {rec} | {f1} | {samples} |\n"

    summary_md += """
---

## 4. Crops Marked as DATASET_NOT_READY (Rule 22)

The following crops did not have datasets in local archives or specified Hugging Face repositories:
"""
    for mc, reason in MISSING_CROPS.items():
        summary_md += f"- **{mc.upper()}**: {reason}\n"

    summary_md += """
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
"""
    summary_path = os.path.join('training', 'TRAINING_SUMMARY.md')
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary_md)
    print(f"[SUMMARY] Saved {summary_path}")

    print("\n" + "=" * 70)
    print("FINAL SUMMARY REPORT:")
    print(f"Models successfully trained ({len(trained_models)}): {list(trained_models.keys())}")
    print(f"Models failed ({len(failed_models)}): {list(failed_models.keys())}")
    print(f"Models not ready ({len(MISSING_CROPS)}): {list(MISSING_CROPS.keys())}")
    print("=" * 70)

if __name__ == '__main__':
    main()
