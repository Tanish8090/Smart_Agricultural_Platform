import os
import sys
import zipfile
import tarfile
import json
from collections import defaultdict, Counter

sys.stdout.reconfigure(encoding='utf-8')

# Required directories
DIRS = [
    'data_raw',
    'data_processed',
    'datasets',
    'models',
    'training',
    'logs'
]

for d in DIRS:
    os.makedirs(d, exist_ok=True)
    print(f"[OK] Directory created/verified: {d}")

ARCHIVES_TO_EXTRACT = [
    'archive (1).zip',
    'archive (2).zip',
    'archive (3).zip',
    'archive (4).zip'
]

IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tiff'}
ANNOT_EXTS = {'.txt', '.xml', '.json'}

def extract_archive(archive_path, dest_dir):
    print(f"\n[*] Extracting: {archive_path} -> {dest_dir} ...")
    os.makedirs(dest_dir, exist_ok=True)
    if archive_path.lower().endswith('.zip'):
        with zipfile.ZipFile(archive_path, 'r') as z:
            z.extractall(dest_dir)
    elif archive_path.lower().endswith(('.tar.gz', '.tgz', '.tar')):
        with tarfile.open(archive_path, 'r:*') as t:
            t.extractall(dest_dir)
    print(f"[DONE] Extracted {archive_path}")

def extract_recursive(target_dir):
    """Scan target_dir for any nested archives and extract them."""
    extracted_any = True
    while extracted_any:
        extracted_any = False
        for root, dirs, files in os.walk(target_dir):
            for f in files:
                f_lower = f.lower()
                if f_lower.endswith(('.zip', '.tar.gz', '.tgz', '.tar')):
                    sub_archive = os.path.join(root, f)
                    sub_dest = os.path.splitext(sub_archive)[0]
                    if not os.path.exists(sub_dest) or len(os.listdir(sub_dest)) == 0:
                        extract_archive(sub_archive, sub_dest)
                        extracted_any = True

# Extract all dataset archives
for arc in ARCHIVES_TO_EXTRACT:
    if os.path.exists(arc):
        stem = os.path.splitext(os.path.basename(arc))[0]
        dest = os.path.join('data_raw', stem)
        # Check if already extracted
        if os.path.exists(dest) and len(os.listdir(dest)) > 0:
            print(f"[SKIP] Already extracted: {dest}")
        else:
            extract_archive(arc, dest)
            extract_recursive(dest)
    else:
        print(f"[WARN] Archive not found: {arc}")

# Generate DATASET_INVENTORY.json
print("\n[*] Analyzing extracted datasets in data_raw ...")
inventory = []

for item in sorted(os.listdir('data_raw')):
    item_path = os.path.join('data_raw', item)
    if not os.path.isdir(item_path):
        continue
    
    total_images = 0
    img_extensions = Counter()
    found_folders = []
    classes = set()
    has_train = False
    has_val = False
    has_test = False
    has_yolo_labels = False
    has_coco = False

    for root, dirs, files in os.walk(item_path):
        rel = os.path.relpath(root, item_path)
        parts = rel.replace('\\', '/').split('/')
        if 'train' in [p.lower() for p in parts]:
            has_train = True
        if any(v in [p.lower() for p in parts] for v in ['val', 'valid', 'validation']):
            has_val = True
        if 'test' in [p.lower() for p in parts]:
            has_test = True

        for d in dirs:
            if d not in ('train', 'val', 'valid', 'validation', 'test', '__MACOSX'):
                classes.add(d)

        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in IMAGE_EXTS:
                total_images += 1
                img_extensions[ext] += 1
                parent = os.path.basename(root)
                if parent not in ('train', 'val', 'valid', 'validation', 'test', item):
                    classes.add(parent)
            elif ext == '.txt' and 'label' in root.lower():
                has_yolo_labels = True
            elif ext == '.json' and ('annot' in f.lower() or 'coco' in f.lower()):
                has_coco = True

    # Detect annotation type
    if has_yolo_labels:
        annot_type = "YOLO_detection"
    elif has_coco:
        annot_type = "COCO_detection"
    else:
        annot_type = "Classification_folders"

    # Match original archive
    orig_archive = f"{item}.zip"
    if not os.path.exists(orig_archive):
        orig_archive = "N/A"

    entry = {
        "dataset_name": item,
        "original_archive": orig_archive,
        "number_of_images": total_images,
        "folders": [os.path.relpath(x[0], item_path).replace('\\', '/') for x in os.walk(item_path)][:10],
        "classes": sorted(list(classes)),
        "annotation_type": annot_type,
        "train_val_test_availability": {
            "has_train": has_train,
            "has_val": has_val,
            "has_test": has_test
        },
        "image_extensions": dict(img_extensions)
    }
    inventory.append(entry)

inventory_path = os.path.join('data_raw', 'DATASET_INVENTORY.json')
with open(inventory_path, 'w', encoding='utf-8') as f:
    json.dump(inventory, f, indent=2)

print(f"\n[SUCCESS] Saved inventory to {inventory_path}")
for entry in inventory:
    print(f"Dataset: {entry['dataset_name']} ({entry['original_archive']})")
    print(f"  Images: {entry['number_of_images']}")
    print(f"  Annotation: {entry['annotation_type']}")
    print(f"  Classes ({len(entry['classes'])}): {entry['classes'][:8]}")
    print(f"  Splits: Train={entry['train_val_test_availability']['has_train']}, Val={entry['train_val_test_availability']['has_val']}, Test={entry['train_val_test_availability']['has_test']}")
