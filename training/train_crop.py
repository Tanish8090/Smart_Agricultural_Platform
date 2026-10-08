import os
import sys
import shutil
import json
import torch
from ultralytics import YOLO

sys.stdout.reconfigure(encoding='utf-8')

def detect_device():
    if getattr(torch.backends, 'mps', None) and torch.backends.mps.is_available():
        print("[DEVICE] Apple MPS detected.")
        return "mps"
    elif torch.cuda.is_available():
        print(f"[DEVICE] CUDA detected: {torch.cuda.get_device_name(0)}")
        return 0
    else:
        print("[DEVICE] CPU detected.")
        return "cpu"

def train_crop_model(crop_name, epochs=30, imgsz=224, initial_batch=32):
    print("\n" + "=" * 60)
    print(f"TRAINING MODEL FOR: {crop_name.upper()}")
    print("=" * 60)

    dataset_dir = os.path.abspath(os.path.join('datasets', crop_name))
    if not os.path.exists(dataset_dir):
        print(f"[ERROR] Dataset directory not found: {dataset_dir}")
        return False, "DATASET_NOT_FOUND"

    train_dir = os.path.join(dataset_dir, 'train')
    val_dir = os.path.join(dataset_dir, 'val')
    test_dir = os.path.join(dataset_dir, 'test')

    classes = sorted([d for d in os.listdir(train_dir) if os.path.isdir(os.path.join(train_dir, d))])
    if len(classes) < 2:
        print(f"[ERROR] Crop {crop_name} must have at least 2 classes, found: {classes}")
        return False, "INSUFFICIENT_CLASSES"

    train_count = sum(len(os.listdir(os.path.join(train_dir, c))) for c in classes)
    val_count = sum(len(os.listdir(os.path.join(val_dir, c))) for c in classes)
    test_count = sum(len(os.listdir(os.path.join(test_dir, c))) for c in classes)

    print(f"Classes ({len(classes)}): {classes}")
    print(f"Images: Train={train_count}, Val={val_count}, Test={test_count}")

    device = detect_device()
    runs_crop_dir = os.path.abspath(os.path.join('runs', 'crop_models', crop_name))
    os.makedirs(runs_crop_dir, exist_ok=True)

    batch_size = initial_batch
    trained_ok = False
    train_results = None

    while batch_size >= 4 and not trained_ok:
        try:
            print(f"\n[*] Starting training with batch_size={batch_size}, epochs={epochs}, imgsz={imgsz} on device={device}...")
            model = YOLO('yolo11n-cls.pt')
            train_results = model.train(
                data=dataset_dir,
                epochs=epochs,
                imgsz=imgsz,
                batch=batch_size,
                device=device,
                patience=5,
                project=os.path.abspath(os.path.join('runs', 'crop_models')),
                name=crop_name,
                exist_ok=True,
                verbose=True,
                workers=2,
                plots=True
            )
            trained_ok = True
        except (torch.cuda.OutOfMemoryError, RuntimeError) as e:
            if 'out of memory' in str(e).lower() and batch_size > 4:
                batch_size = batch_size // 2
                print(f"[WARN] Memory error, reducing batch size to {batch_size} and retrying...")
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
            else:
                print(f"[ERROR] Training failed for {crop_name}: {e}")
                return False, str(e)
        except Exception as e:
            print(f"[ERROR] Unexpected training error for {crop_name}: {e}")
            return False, str(e)

    if not trained_ok:
        return False, "TRAINING_FAILED_AFTER_RETRIES"

    # Save to models/<crop_name>/best.pt
    model_dest_dir = os.path.join('models', crop_name)
    os.makedirs(model_dest_dir, exist_ok=True)
    target_best_pt = os.path.join(model_dest_dir, 'best.pt')

    # Backup if best.pt exists
    if os.path.exists(target_best_pt):
        backup_pt = os.path.join(model_dest_dir, 'best.pt.bak')
        shutil.copy2(target_best_pt, backup_pt)
        print(f"[BACKUP] Created backup of existing weights: {backup_pt}")

    # Locate trained weights
    candidate_weights = [
        os.path.join('runs', 'crop_models', crop_name, 'weights', 'best.pt'),
        os.path.join('runs', 'crop_models', crop_name, 'train', 'weights', 'best.pt')
    ]
    saved_weights = None
    for cw in candidate_weights:
        if os.path.exists(cw):
            shutil.copy2(cw, target_best_pt)
            saved_weights = target_best_pt
            print(f"[SUCCESS] Copied best weights to {target_best_pt}")
            break

    if not saved_weights:
        print(f"[WARN] Could not find best.pt in runs/crop_models/{crop_name}/weights/")

    # Generate metadata.json
    metadata = {
        "crop": crop_name,
        "model_type": "classification",
        "classes": classes,
        "weights": "best.pt",
        "image_size": imgsz,
        "epochs": epochs,
        "dataset_version": "1.0.0",
        "training_device": str(device),
        "train_images": train_count,
        "val_images": val_count,
        "test_images": test_count,
        "batch_size": batch_size
    }
    metadata_path = os.path.join(model_dest_dir, 'metadata.json')
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    print(f"[METADATA] Saved {metadata_path}")

    return True, metadata

if __name__ == '__main__':
    crop = sys.argv[1] if len(sys.argv) > 1 else 'wheat'
    ep = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    train_crop_model(crop, epochs=ep)
