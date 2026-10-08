import os
import sys
import json
from ultralytics import YOLO

sys.stdout.reconfigure(encoding='utf-8')

REQUIRED_SPECS = {
    "Wheat": {
        "dir": "models/wheat",
        "classes": ["Wheat___Yellow_rust", "Wheat___healthy"]
    },
    "Cotton": {
        "dir": "models/cotton",
        "classes": ["Cotton___Bacterial_blight", "Cotton___healthy"]
    },
    "Sugarcane": {
        "dir": "models/sugarcane",
        "classes": ["Sugarcane___Red_rot", "Sugarcane___healthy"]
    },
    "Potato": {
        "dir": "models/potato",
        "classes": ["Potato___Early_blight", "Potato___Late_blight", "Potato___healthy"]
    },
    "Rice": {
        "dir": "models/rice",
        "classes": ["Rice___Blast", "Rice___Brown_spot", "Rice___healthy"]
    },
    "Soybean": {
        "dir": "models/soybean",
        "classes": ["Soybean___Rust", "Soybean___healthy"]
    },
    "Tomato": {
        "dir": "models/tomato",
        "classes": ["Tomato___Early_blight", "Tomato___Late_blight", "Tomato___healthy"]
    },
    "Corn": {
        "dir": "models/corn",
        "classes": ["Corn___Common_rust", "Corn___Leaf_blight", "Corn___healthy"]
    },
    "Apple": {
        "dir": "models/apple",
        "classes": ["Apple___Scab", "Apple___healthy"]
    },
    "Grape": {
        "dir": "models/grape",
        "classes": ["Grape___Black_rot", "Grape___healthy"]
    },
    "Not_A_Leaf": {
        "dir": "models/not_a_leaf",
        "classes": ["Not_A_Leaf", "Plant_Leaf"]
    }
}

def verify():
    results = []
    all_passed = True

    print("=" * 80)
    print("VERIFYING ALL SAP CROP & REJECTION MODELS")
    print("=" * 80)

    for crop, spec in REQUIRED_SPECS.items():
        model_path = os.path.join(spec["dir"], "best.pt")
        meta_path = os.path.join(spec["dir"], "metadata.json")

        exists = os.path.exists(model_path)
        loadable = False
        classes_correct = False
        actual_classes = []
        error_msg = ""

        if exists:
            try:
                model = YOLO(model_path)
                loadable = True
                if hasattr(model, 'names') and isinstance(model.names, dict):
                    actual_classes = list(model.names.values())
                elif hasattr(model, 'names') and isinstance(model.names, list):
                    actual_classes = model.names
                
                # Check class match (independent of order, or exact match)
                expected_set = set(spec["classes"])
                actual_set = set(actual_classes)

                if expected_set == actual_set:
                    classes_correct = True
                else:
                    diff_missing = expected_set - actual_set
                    diff_extra = actual_set - expected_set
                    error_msg = f"Missing: {diff_missing}, Extra: {diff_extra}"
            except Exception as e:
                loadable = False
                error_msg = str(e)
        else:
            error_msg = "best.pt not found"

        status = "PASSED" if (exists and loadable and classes_correct) else "FAILED"
        if status == "FAILED":
            all_passed = False

        results.append({
            "crop": crop,
            "exists": "YES" if exists else "NO",
            "classes_correct": "YES" if classes_correct else "NO",
            "loadable": "YES" if loadable else "NO",
            "status": status,
            "actual_classes": actual_classes,
            "expected_classes": spec["classes"],
            "error": error_msg
        })

        print(f"[{'PASS' if status == 'PASSED' else 'FAIL'}] {crop:12}: Exists={results[-1]['exists']}, Loadable={results[-1]['loadable']}, Classes={results[-1]['classes_correct']} | Actual: {actual_classes}")
        if error_msg:
            print(f"       Note: {error_msg}")

    print("=" * 80)
    print(f"Overall Result: {'ALL MODELS PASSED' if all_passed else 'SOME MODELS FAILED'}")
    print("=" * 80)

    # Generate Markdown Report
    report_content = [
        "# SAP Crop Disease System — Model Validation Report",
        "",
        f"**Date**: {os.popen('date /t').read().strip() if os.name == 'nt' else ''}",
        f"**Overall Status**: {'ALL CHECKS PASSED (11/11)' if all_passed else 'INCOMPLETE'}",
        "",
        "## Summary Validation Table",
        "",
        "| Crop | Model Exists | Classes Correct | Loadable | Status |",
        "| :--- | :---: | :---: | :---: | :---: |"
    ]

    for r in results:
        report_content.append(f"| **{r['crop']}** | {r['exists']} | {r['classes_correct']} | {r['loadable']} | **{r['status']}** |")

    report_content.extend([
        "",
        "## Detailed Model Class Verification",
        ""
    ])

    for r in results:
        report_content.append(f"### {r['crop']}")
        report_content.append(f"- **Model Path**: `{REQUIRED_SPECS[r['crop']]['dir']}/best.pt`")
        report_content.append(f"- **Expected Classes**: `{r['expected_classes']}`")
        report_content.append(f"- **Actual Classes**: `{r['actual_classes']}`")
        report_content.append(f"- **Status**: `{r['status']}`")
        if r['error']:
            report_content.append(f"- **Notes**: {r['error']}")
        report_content.append("")

    report_path = "training/model_validation_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_content))

    print(f"\n[✓] Validation report written to {report_path}")
    return all_passed

if __name__ == "__main__":
    verify()
