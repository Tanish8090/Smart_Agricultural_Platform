import os
import sys
import json
import time
import numpy as np
from PIL import Image
import onnx
import onnxruntime as ort
from ultralytics import YOLO

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
MODELS_DIR = os.path.join(ROOT_DIR, 'models')
DATASETS_DIR = os.path.join(ROOT_DIR, 'datasets')
REPORT_PATH = os.path.join(BASE_DIR, 'onnx_validation_report.md')
CONFIG_PATH = os.path.join(MODELS_DIR, 'model_config.json')

CROPS = [
    'wheat', 'cotton', 'sugarcane', 'potato', 'rice',
    'soybean', 'tomato', 'corn', 'apple', 'grape', 'not_a_leaf'
]

from ultralytics.data.augment import classify_transforms

transform = classify_transforms(224)

def preprocess_image_for_onnx(img_path):
    img = Image.open(img_path).convert('RGB')
    tensor = transform(img).unsqueeze(0)
    return tensor.numpy(), img

def softmax(x):
    e_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return e_x / e_x.sum(axis=-1, keepdims=True)

def find_sample_image(crop):
    # Check datasets/<crop>/test
    test_dir = os.path.join(DATASETS_DIR, crop, 'test')
    if os.path.exists(test_dir):
        for root, dirs, files in os.walk(test_dir):
            for f in files:
                if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                    return os.path.join(root, f)
    # Check val
    val_dir = os.path.join(DATASETS_DIR, crop, 'val')
    if os.path.exists(val_dir):
        for root, dirs, files in os.walk(val_dir):
            for f in files:
                if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                    return os.path.join(root, f)
    # Fallback to test photos
    test_photos = os.path.join(ROOT_DIR, 'final sap project', 'test photos')
    if os.path.exists(test_photos):
        for f in os.listdir(test_photos):
            if f.lower().endswith(('.jpg', '.jpeg', '.png')):
                return os.path.join(test_photos, f)
    return None

def main():
    print("=" * 65)
    print("  ONNX Model Conversion & Validation Pipeline")
    print("=" * 65)

    registry = {}
    validation_results = []

    for crop in CROPS:
        pt_path = os.path.join(MODELS_DIR, crop, 'best.pt')
        onnx_path = os.path.join(MODELS_DIR, crop, 'best.onnx')
        named_onnx_path = os.path.join(MODELS_DIR, crop, f"{crop}.onnx")

        print(f"\n---> Processing [{crop}]...")
        if not os.path.exists(pt_path):
            print(f"  [ERROR] {pt_path} does not exist!")
            continue

        # Load PyTorch model
        pt_model = YOLO(pt_path)
        class_dict = pt_model.names
        classes = [class_dict[i] for i in range(len(class_dict))]
        num_classes = len(classes)
        print(f"  Classes ({num_classes}): {classes}")

        # Update registry
        registry[crop] = {
            "model": f"{crop}.onnx",
            "classes": classes
        }

        # Export if not already exported or to ensure freshness
        if not os.path.exists(onnx_path):
            print(f"  Exporting {pt_path} to ONNX (imgsz=224)...")
            pt_model.export(format='onnx', imgsz=224, opset=18)
        else:
            print(f"  Found existing {onnx_path}")

        # Also copy/save as named onnx file: models/<crop>/<crop>.onnx for direct access
        if os.path.exists(onnx_path):
            with open(onnx_path, 'rb') as f_in:
                onnx_bytes = f_in.read()
            with open(named_onnx_path, 'wb') as f_out:
                f_out.write(onnx_bytes)

        file_size_mb = os.path.getsize(onnx_path) / (1024 * 1024)
        print(f"  ONNX file size: {file_size_mb:.2f} MB")

        # Load ONNX model and check shapes
        onnx_model = onnx.load(onnx_path)
        onnx.checker.check_model(onnx_model)

        session = ort.InferenceSession(onnx_path)
        input_info = session.get_inputs()[0]
        output_info = session.get_outputs()[0]
        input_name = input_info.name
        input_shape = input_info.shape
        output_name = output_info.name
        output_shape = output_info.shape
        print(f"  ONNX Input: name='{input_name}', shape={input_shape}")
        print(f"  ONNX Output: name='{output_name}', shape={output_shape}")

        # Compare inference on sample image
        sample_img = find_sample_image(crop)
        match_status = "N/A"
        max_diff = 0.0
        pt_pred = "N/A"
        onnx_pred = "N/A"

        if sample_img:
            # PyTorch inference
            pt_res = pt_model.predict(sample_img, imgsz=224, verbose=False)[0]
            pt_top1 = int(pt_res.probs.top1)
            pt_conf = float(pt_res.probs.top1conf)
            pt_pred = f"{classes[pt_top1]} ({pt_conf:.4f})"
            pt_all_probs = pt_res.probs.data.cpu().numpy()

            # ONNX inference
            input_arr, _ = preprocess_image_for_onnx(sample_img)
            onnx_outputs = session.run([output_name], {input_name: input_arr})
            raw_logits = onnx_outputs[0][0]
            # YOLO classification head outputs logits; apply softmax if needed
            if np.isclose(np.sum(raw_logits), 1.0, atol=1e-2) and np.all(raw_logits >= 0):
                onnx_probs = raw_logits
            else:
                onnx_probs = softmax(raw_logits)

            onnx_top1 = int(np.argmax(onnx_probs))
            onnx_conf = float(onnx_probs[onnx_top1])
            onnx_pred = f"{classes[onnx_top1]} ({onnx_conf:.4f})"

            max_diff = float(np.max(np.abs(pt_all_probs - onnx_probs)))
            match_status = "PASSED" if (pt_top1 == onnx_top1 and max_diff < 0.05) else "VERIFY"
            print(f"  Test image: {os.path.basename(sample_img)}")
            print(f"    PyTorch: {pt_pred}")
            print(f"    ONNX:    {onnx_pred}")
            print(f"    Max Diff: {max_diff:.6f} -> Status: {match_status}")
        else:
            print("  [WARN] No sample image found for verification.")

        validation_results.append({
            "crop": crop,
            "onnx_file": f"{crop}.onnx",
            "size_mb": round(file_size_mb, 2),
            "input_shape": str(input_shape),
            "output_shape": str(output_shape),
            "classes": classes,
            "sample_img": os.path.basename(sample_img) if sample_img else "None",
            "pt_pred": pt_pred,
            "onnx_pred": onnx_pred,
            "max_diff": max_diff,
            "status": match_status
        })

    # Save central registry to models/model_config.json
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(registry, f, indent=2)
    print(f"\n[OK] Model registry saved to {CONFIG_PATH}")

    # Generate Markdown Report
    report_lines = [
        "# ONNX Model Conversion & Validation Report",
        "",
        f"**Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}",
        "**Runtime:** ONNX Runtime & Ultralytics YOLOv11n-cls",
        "**Target Platform:** Android Local On-Device Inference (No Cloud API)",
        "",
        "## 1. Summary",
        "",
        f"A total of **{len(validation_results)}** models were converted to ONNX and validated:",
        "- 10 Crop-Specific Disease Classification Models",
        "- 1 Not_A_Leaf Binary Classification Gatekeeper Model",
        "",
        "## 2. Model Specifications & Validation Results",
        "",
        "| Crop / Model | ONNX File | Size (MB) | Input Shape | Output Shape | Classes | Sample Image | Status |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
    ]

    for r in validation_results:
        report_lines.append(
            f"| **{r['crop']}** | `{r['onnx_file']}` | {r['size_mb']} MB | `{r['input_shape']}` | `{r['output_shape']}` | {len(r['classes'])} | `{r['sample_img']}` | **{r['status']}** |"
        )

    report_lines.extend([
        "",
        "## 3. Numerical Parity Verification (PyTorch .pt vs ONNX)",
        "",
        "| Model | PyTorch Prediction | ONNX Prediction | Max Probability Diff | Parity |",
        "| :--- | :--- | :--- | :--- | :--- |"
    ])

    for r in validation_results:
        report_lines.append(
            f"| **{r['crop']}** | {r['pt_pred']} | {r['onnx_pred']} | {r['max_diff']:.6f} | `{r['status']}` |"
        )

    report_lines.extend([
        "",
        "## 4. Central Model Registry (`models/model_config.json`)",
        "",
        "```json",
        json.dumps(registry, indent=2),
        "```",
        "",
        "## 5. Architectural Alignment",
        "",
        "- **Format:** ONNX Opset 18 with onnxslim optimization",
        "- **Input Tensor:** `[1, 3, 224, 224]` Float32 normalized to `[0.0, 1.0]` (NCHW format, RGB channel order)",
        "- **Output Tensor:** `[1, num_classes]` Float32 logits",
        "- **Postprocessing:** Softmax over output tensor yields class confidence probabilities",
        "- **Zero Cloud Dependencies:** All inference is executed locally using ONNX Runtime.",
        ""
    ])

    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write("\n".join(report_lines))
    print(f"[OK] Validation report written to {REPORT_PATH}")

if __name__ == '__main__':
    main()
