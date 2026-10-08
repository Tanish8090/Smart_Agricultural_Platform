import os
import sys
import json
import torch
import numpy as np
from PIL import Image
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix, classification_report
from ultralytics import YOLO

sys.stdout.reconfigure(encoding='utf-8')

def evaluate_crop_model(crop_name):
    print("\n" + "=" * 60)
    print(f"EVALUATING MODEL FOR: {crop_name.upper()}")
    print("=" * 60)

    model_path = os.path.join('models', crop_name, 'best.pt')
    if not os.path.exists(model_path):
        # Fallback to runs/
        runs_p = os.path.join('runs', 'crop_models', crop_name, 'weights', 'best.pt')
        if os.path.exists(runs_p):
            model_path = runs_p
        else:
            print(f"[ERROR] Model weights not found for {crop_name}: {model_path}")
            return None

    test_dir = os.path.join('datasets', crop_name, 'test')
    if not os.path.exists(test_dir):
        print(f"[ERROR] Test directory not found: {test_dir}")
        return None

    classes = sorted([d for d in os.listdir(test_dir) if os.path.isdir(os.path.join(test_dir, d))])
    class_to_idx = {c: i for i, c in enumerate(classes)}

    y_true = []
    y_pred = []
    confidences = []

    print(f"Loading weights from: {model_path}")
    model = YOLO(model_path)

    test_images = []
    for cls in classes:
        cls_dir = os.path.join(test_dir, cls)
        for f in os.listdir(cls_dir):
            if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                test_images.append((os.path.join(cls_dir, f), cls))

    if not test_images:
        print(f"[ERROR] No test images found in {test_dir}")
        return None

    print(f"Evaluating {len(test_images)} test images across classes: {classes}")

    for img_path, true_cls in test_images:
        try:
            results = model.predict(img_path, verbose=False, imgsz=224)
            top1_idx = int(results[0].probs.top1)
            pred_cls = results[0].names[top1_idx]
            conf = float(results[0].probs.top1conf)

            y_true.append(true_cls)
            y_pred.append(pred_cls)
            confidences.append(conf)
        except Exception as e:
            print(f"Error predicting {img_path}: {e}")
            continue

    if not y_true:
        print("[ERROR] Evaluation produced no valid predictions.")
        return None

    # Compute metrics
    acc = accuracy_score(y_true, y_pred)
    prec, rec, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='weighted', zero_division=0)
    cm = confusion_matrix(y_true, y_pred, labels=classes)
    report_txt = classification_report(y_true, y_pred, labels=classes, zero_division=0)
    report_dict = classification_report(y_true, y_pred, labels=classes, output_dict=True, zero_division=0)

    eval_dir = os.path.join('runs', 'crop_models', crop_name, 'evaluation')
    os.makedirs(eval_dir, exist_ok=True)

    metrics = {
        "crop": crop_name,
        "classes": classes,
        "test_samples": len(y_true),
        "accuracy": round(float(acc), 4),
        "precision_weighted": round(float(prec), 4),
        "recall_weighted": round(float(rec), 4),
        "f1_weighted": round(float(f1), 4),
        "mean_confidence": round(float(np.mean(confidences)), 4),
        "confusion_matrix": cm.tolist(),
        "per_class": {c: report_dict.get(c, {}) for c in classes},
        "evaluation_notes": "Validation scores on small/controlled test datasets do NOT imply equal real-world diagnostic performance."
    }

    # Save files
    with open(os.path.join(eval_dir, 'metrics.json'), 'w', encoding='utf-8') as f:
        json.dump(metrics, f, indent=2)

    with open(os.path.join(eval_dir, 'classification_report.txt'), 'w', encoding='utf-8') as f:
        f.write(report_txt)

    # Save summary markdown
    summary_md = f"""# Model Evaluation: {crop_name.upper()}

- **Test Images**: {len(y_true)}
- **Classes**: {', '.join(classes)}
- **Accuracy**: {acc * 100:.2f}%
- **Precision (Weighted)**: {prec * 100:.2f}%
- **Recall (Weighted)**: {rec * 100:.2f}%
- **F1-Score (Weighted)**: {f1 * 100:.2f}%
- **Mean Confidence**: {np.mean(confidences) * 100:.2f}%

## Classification Report
```
{report_txt}
```

## Confusion Matrix
Classes: {classes}
```json
{json.dumps(cm.tolist())}
```

> **Note**: Prototype evaluation metrics. High test score on controlled datasets does not guarantee identical field performance under varied lighting, occlusions, and camera variations.
"""
    with open(os.path.join(eval_dir, 'evaluation_summary.md'), 'w', encoding='utf-8') as f:
        f.write(summary_md)

    print(f"\n[RESULTS] {crop_name.upper()}:")
    print(f"  Accuracy:  {acc * 100:.2f}%")
    print(f"  Precision: {prec * 100:.2f}%")
    print(f"  Recall:    {rec * 100:.2f}%")
    print(f"  F1 Score:  {f1 * 100:.2f}%")
    print(f"  Saved evaluation artifacts to: {eval_dir}")

    return metrics

def evaluate_all():
    summary = {}
    crops = ['wheat', 'cotton', 'sugarcane', 'potato', 'rice', 'soybean', 'not_a_leaf']
    for c in crops:
        res = evaluate_crop_model(c)
        if res:
            summary[c] = res

    # Save global evaluation summary
    os.makedirs('runs', exist_ok=True)
    with open(os.path.join('runs', 'all_evaluations.json'), 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)

    return summary

if __name__ == '__main__':
    crop = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if crop == 'all':
        evaluate_all()
    else:
        evaluate_crop_model(crop)
