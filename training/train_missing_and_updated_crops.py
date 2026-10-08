import os
import sys
import json
import time
import torch
from ultralytics import YOLO

sys.stdout.reconfigure(encoding='utf-8')

# Add training dir to path
sys.path.insert(0, os.path.abspath('training'))
from train_crop import train_crop_model, detect_device
from evaluate_models import evaluate_crop_model

CROPS_TO_TRAIN = ['potato', 'rice', 'tomato', 'corn', 'apple', 'grape']

def main():
    print("=" * 70)
    print("TRAINING REQUIRED MISSING & UPDATED CROP MODELS")
    print("=" * 70)

    device = detect_device()
    print(f"Device: {device}")

    results = {}
    eval_results = {}

    start_all = time.time()

    for crop in CROPS_TO_TRAIN:
        print(f"\n=======================================================")
        print(f"STARTING TRAINING FOR: {crop.upper()}")
        print(f"=======================================================")
        t0 = time.time()
        success, info = train_crop_model(crop, epochs=25, imgsz=224, initial_batch=32)
        dur = time.time() - t0
        if success:
            print(f"[✓] {crop.upper()} trained successfully in {dur:.1f}s")
            results[crop] = info
            try:
                ev = evaluate_crop_model(crop)
                if ev:
                    eval_results[crop] = ev
                    print(f"[✓] Test Evaluation {crop}: Acc={ev.get('accuracy', 0):.4f}, F1={ev.get('f1_weighted', 0):.4f}")
            except Exception as e:
                print(f"[!] Evaluation warning for {crop}: {e}")
        else:
            print(f"[✗] Failed to train {crop}: {info}")

    total_dur = time.time() - start_all
    print(f"\nTraining pipeline completed in {total_dur / 60:.2f} minutes.")

    # Update models/model_config.json
    all_10_crops = ['wheat', 'cotton', 'sugarcane', 'potato', 'rice', 'soybean', 'tomato', 'corn', 'apple', 'grape']
    crop_models_dict = {}
    for c in all_10_crops:
        mpath = os.path.abspath(os.path.join('models', c, 'best.pt')).replace('\\', '/')
        if os.path.exists(mpath):
            crop_models_dict[c] = mpath
        else:
            print(f"[!] Warning: Missing weights for {c} at {mpath}")

    model_config = {
        "device": str(device),
        "not_a_leaf_model": os.path.abspath('models/not_a_leaf/best.pt').replace('\\', '/'),
        "not_a_leaf_threshold": 0.50,
        "min_confidence_threshold": 0.40,
        "crop_models": crop_models_dict,
        "not_ready_crops": []
    }

    config_path = os.path.join('models', 'model_config.json')
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(model_config, f, indent=2)
    print(f"[CONFIG] Updated {config_path} with all 10 active crops!")

    # Summary
    print("\n=== SUMMARY OF TRAINED MODELS ===")
    for c in all_10_crops:
        meta_path = os.path.join('models', c, 'metadata.json')
        if os.path.exists(meta_path):
            with open(meta_path, 'r', encoding='utf-8') as f:
                meta = json.load(f)
            print(f"  {c:10s} -> Classes: {meta.get('classes')}")

if __name__ == '__main__':
    main()
