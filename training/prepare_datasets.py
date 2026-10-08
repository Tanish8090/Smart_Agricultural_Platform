import os
import sys
import shutil
import hashlib
import random
import json
import io
import urllib.request
from collections import defaultdict, Counter
from PIL import Image, ImageEnhance, ImageFilter

sys.stdout.reconfigure(encoding='utf-8')

RANDOM_SEED = 42
random.seed(RANDOM_SEED)

TARGET_CROPS = {
    "wheat": {
        "classes": {
            "Wheat___Yellow_rust": {"source_dir": "data_raw/archive (1)/Wheat Disease Dataset/YellowRust"},
            "Wheat___healthy": {"source_dir": "data_raw/archive (1)/Wheat Disease Dataset/Healthy"}
        },
        "excluded": {
            "BrownRust": "Excluded - target model focuses specifically on Yellow Rust and Healthy",
            "Mildew": "Excluded - Powdery Mildew is distinct fungal disease not in target classes",
            "Septoria": "Excluded - Septoria tritici blotch is not in target classes"
        }
    },
    "cotton": {
        "classes": {
            "Cotton___Bacterial_blight": {"source_dir": "data_raw/archive (2)/Augmented Dataset/Bacterial Blight"},
            "Cotton___healthy": {"source_dir": "data_raw/archive (2)/Augmented Dataset/Healthy Leaf"}
        },
        "excluded": {
            "Curl Virus": "Excluded - Cotton leaf curl virus not in target classes",
            "Herbicide Growth Damage": "Excluded - Physiological/chemical injury not in target classes",
            "Leaf Hopper Jassids": "Excluded - Insect pest damage not in target classes",
            "Leaf Redding": "Excluded - Nutritional/physiological stress not in target classes",
            "Leaf Variegation": "Excluded - Variegation condition not in target classes"
        }
    },
    "sugarcane": {
        "classes": {
            "Sugarcane___Red_rot": {"source_dir": "data_raw/archive (3)/Sugarcane_leafs/RedRot"},
            "Sugarcane___healthy": {"source_dir": "data_raw/archive (3)/Sugarcane_leafs/Healthy"}
        },
        "excluded": {
            "BacterialBlights": "Excluded - Bacterial blight not in target classes",
            "Mosaic": "Excluded - Mosaic virus not in target classes",
            "Rust": "Excluded - Sugarcane rust not in target classes",
            "Yellow": "Excluded - Yellow leaf syndrome not in target classes"
        }
    },
    "potato": {
        "classes": {
            "Potato___Late_blight": {"source_dir": "data_raw/archive (4)/Late Blight"},
            "Potato___healthy": {"source_dir": "data_raw/archive (4)/Healthy"}
        },
        "excluded": {}
    },
    "rice": {
        "classes": {
            "Rice___Blast": {"parquet_sources": [
                ("data_raw/huggingface/rice_leaf_disease_classification/data", ["Leaf_Blast"]),
                ("data_raw/huggingface/rice_leaf_disease_classification_india/data", ["Blast"])
            ]},
            "Rice___healthy": {"parquet_sources": [
                ("data_raw/huggingface/rice_leaf_disease_classification/data", ["Healthy_Rice_Leaf"])
            ]}
        },
        "excluded": {
            "Bacterial_Leaf_Blight": "Excluded - Bacterial blight not in target classes",
            "Brown_Spot": "Excluded - Brown spot not in target classes",
            "Leaf_Scald": "Excluded - Leaf scald not in target classes",
            "Sheath_Blight": "Excluded - Sheath blight not in target classes",
            "Tungro": "Excluded - Tungro virus not in target classes"
        }
    },
    "soybean": {
        "classes": {
            "Soybean___Rust": {"parquet_sources": [
                ("data_raw/huggingface/MH_SoyaHealthVision_disease_classification_leaf/data", ["Rust"])
            ]},
            "Soybean___healthy": {"parquet_sources": [
                ("data_raw/huggingface/MH_SoyaHealthVision_disease_classification_leaf/data", ["Healthy"])
            ]}
        },
        "excluded": {
            "Caterpillar_Semilooper_Pest": "Excluded - Insect pest damage not in target classes",
            "Frog_Leaf_Eye": "Excluded - Frog eye leaf spot not in target classes",
            "Mosaic": "Excluded - Soybean mosaic virus not in target classes",
            "Spectoria_Brown_Spot": "Excluded - Brown spot not in target classes",
            "SoyNet_Disease": "Excluded - Generic mixed disease class in SoyNet cannot be safely mapped to Rust"
        }
    }
}

MISSING_CROPS = {
    "tomato": "DATASET_NOT_READY: No local archive or HF repository present in workspace for Tomato Early Blight & Healthy",
    "corn": "DATASET_NOT_READY: No local archive or HF repository present in workspace for Corn Common Rust & Healthy",
    "apple": "DATASET_NOT_READY: No local archive or HF repository present in workspace for Apple Scab & Healthy",
    "grape": "DATASET_NOT_READY: No local archive or HF repository present in workspace for Grape Downy Mildew & Healthy"
}

def get_file_md5(file_path):
    h = hashlib.md5()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def get_bytes_md5(data):
    return hashlib.md5(data).hexdigest()

def augment_image(pil_img):
    """Generate subtle, realistic agricultural image augmentations."""
    transforms = [
        lambda img: img.transpose(Image.FLIP_LEFT_RIGHT),
        lambda img: img.transpose(Image.FLIP_TOP_BOTTOM),
        lambda img: img.rotate(90, expand=False),
        lambda img: img.rotate(180, expand=False),
        lambda img: img.rotate(270, expand=False),
        lambda img: ImageEnhance.Brightness(img).enhance(random.uniform(0.85, 1.15)),
        lambda img: ImageEnhance.Contrast(img).enhance(random.uniform(0.85, 1.15)),
    ]
    fn = random.choice(transforms)
    return fn(pil_img)

def extract_parquet_images(parquet_dir, target_label_names, max_samples=1200):
    """Read parquet files and extract images for specified label names."""
    import pyarrow.parquet as pq
    results = [] # list of (md5, pil_image)
    seen_hashes = set()
    
    if not os.path.exists(parquet_dir):
        return results

    p_files = sorted([os.path.join(parquet_dir, f) for f in os.listdir(parquet_dir) if f.endswith('.parquet')])
    for p_file in p_files:
        if len(results) >= max_samples:
            break
        try:
            table = pq.read_table(p_file)
            meta = json.loads(table.schema.metadata.get(b'huggingface', b'{}'))
            label_names = meta.get('info', {}).get('features', {}).get('label', {}).get('names', [])
            if not label_names and 'label' in table.column_names:
                # check if label column has string names directly
                pass

            target_indices = [i for i, name in enumerate(label_names) if name in target_label_names]
            
            img_col = table.column('image')
            lbl_col = table.column('label') if 'label' in table.column_names else None

            for i in range(len(table)):
                if len(results) >= max_samples:
                    break
                lbl = lbl_col[i].as_py() if lbl_col else None
                if target_indices and lbl not in target_indices:
                    continue
                
                cell = img_col[i].as_py()
                img_bytes = cell['bytes'] if isinstance(cell, dict) and 'bytes' in cell else cell
                if not img_bytes:
                    continue
                
                h = get_bytes_md5(img_bytes)
                if h in seen_hashes:
                    continue
                seen_hashes.add(h)

                try:
                    im = Image.open(io.BytesIO(img_bytes))
                    if im.mode != 'RGB':
                        im = im.convert('RGB')
                    im.verify() # check integrity
                    # Reopen after verify
                    im = Image.open(io.BytesIO(img_bytes)).convert('RGB')
                    results.append((h, im))
                except Exception:
                    continue
        except Exception as e:
            print(f"Error reading {p_file}: {e}")
            continue

    return results

def prepare_non_leaf_dataset():
    """Ensure non-leaf images exist and build datasets/not_a_leaf/"""
    print("\n" + "=" * 60)
    print("PREPARING NOT_A_LEAF DATASET")
    print("=" * 60)
    
    raw_not_leaf_dir = os.path.join('data_raw', 'not_a_leaf')
    os.makedirs(raw_not_leaf_dir, exist_ok=True)
    
    # 1. Collect non-leaf images
    urls = [
        # Building
        ("building_1.jpg", "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=400"),
        ("building_2.jpg", "https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=400"),
        # Bus
        ("bus_1.jpg", "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?w=400"),
        ("bus_2.jpg", "https://images.unsplash.com/photo-1570125909232-eb263c188f7e?w=400"),
        # Car
        ("car_1.jpg", "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=400"),
        ("car_2.jpg", "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=400"),
        # Person
        ("person_1.jpg", "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400"),
        ("person_2.jpg", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400"),
        # Bottle
        ("bottle_1.jpg", "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400"),
        ("bottle_2.jpg", "https://images.unsplash.com/photo-1523362628745-0c100150b504?w=400"),
        # Chair
        ("chair_1.jpg", "https://images.unsplash.com/photo-1567538096630-e0c55bd6374c?w=400"),
        ("chair_2.jpg", "https://images.unsplash.com/photo-1580481077191-23f721591f86?w=400"),
        # Laptop
        ("laptop_1.jpg", "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400"),
        ("laptop_2.jpg", "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400"),
        # Phone
        ("phone_1.jpg", "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400"),
        ("phone_2.jpg", "https://images.unsplash.com/photo-1580910051074-3eb694886505?w=400"),
        # Shoes
        ("shoes_1.jpg", "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400"),
        ("shoes_2.jpg", "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=400"),
        # Keyboard
        ("keyboard_1.jpg", "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400"),
        ("keyboard_2.jpg", "https://images.unsplash.com/photo-1541140532154-b024d705b909?w=400"),
    ]

    import ultralytics
    ultralytics_assets = os.path.join(os.path.dirname(ultralytics.__file__), 'assets')
    for asset_name in ['bus.jpg', 'zidane.jpg']:
        asset_path = os.path.join(ultralytics_assets, asset_name)
        if os.path.exists(asset_path):
            dest = os.path.join(raw_not_leaf_dir, f"asset_{asset_name}")
            shutil.copy2(asset_path, dest)

    headers = {'User-Agent': 'Mozilla/5.0'}
    for name, url in urls:
        p = os.path.join(raw_not_leaf_dir, name)
        if not os.path.exists(p) or os.path.getsize(p) == 0:
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=8) as resp:
                    with open(p, 'wb') as f:
                        f.write(resp.read())
            except Exception as e:
                pass

    non_leaf_imgs = []
    for f in os.listdir(raw_not_leaf_dir):
        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
            fp = os.path.join(raw_not_leaf_dir, f)
            try:
                im = Image.open(fp).convert('RGB')
                im.verify()
                im = Image.open(fp).convert('RGB')
                non_leaf_imgs.append(im)
            except Exception:
                continue

    print(f"Collected {len(non_leaf_imgs)} raw non-leaf images across all 10 categories.")
    print("WARNING: The Not_A_Leaf collection is small. Use augmentation; do NOT claim it is reliable merely because training accuracy is high.")

    # 2. Collect Plant_Leaf images from all available crop datasets
    leaf_imgs = []
    for crop in ['wheat', 'potato', 'cotton', 'rice', 'sugarcane', 'soybean']:
        crop_dir = os.path.join('datasets', crop, 'train')
        if os.path.exists(crop_dir):
            for cls in os.listdir(crop_dir):
                cls_p = os.path.join(crop_dir, cls)
                if os.path.isdir(cls_p):
                    for f in os.listdir(cls_p)[:35]:
                        try:
                            im = Image.open(os.path.join(cls_p, f)).convert('RGB')
                            leaf_imgs.append(im)
                        except Exception:
                            continue

    if not leaf_imgs:
        # Fallback to data_raw
        for r, _, files in os.walk('data_raw'):
            for f in files:
                if f.lower().endswith(('.jpg', '.png')) and ('healthy' in r.lower() or 'rust' in r.lower()):
                    try:
                        im = Image.open(os.path.join(r, f)).convert('RGB')
                        leaf_imgs.append(im)
                        if len(leaf_imgs) >= 150:
                            break
                    except Exception:
                        continue

    # Prepare datasets/not_a_leaf
    base_dir = os.path.join('datasets', 'not_a_leaf')
    shutil.rmtree(base_dir, ignore_errors=True)

    for split in ['train', 'val', 'test']:
        for cls in ['Not_A_Leaf', 'Plant_Leaf']:
            os.makedirs(os.path.join(base_dir, split, cls), exist_ok=True)

    # Split non_leaf
    random.shuffle(non_leaf_imgs)
    n = len(non_leaf_imgs)
    n_train = int(n * 0.7)
    n_val = int(n * 0.15)
    
    train_nl = non_leaf_imgs[:n_train]
    val_nl = non_leaf_imgs[n_train:n_train + n_val]
    test_nl = non_leaf_imgs[n_train + n_val:]

    # Save test & val as raw
    for i, im in enumerate(val_nl):
        im.save(os.path.join(base_dir, 'val', 'Not_A_Leaf', f'val_{i}.jpg'), 'JPEG')
    for i, im in enumerate(test_nl):
        im.save(os.path.join(base_dir, 'test', 'Not_A_Leaf', f'test_{i}.jpg'), 'JPEG')

    # Augment train non-leaf to ~200 samples
    idx = 0
    for im in train_nl:
        im.save(os.path.join(base_dir, 'train', 'Not_A_Leaf', f'train_{idx}.jpg'), 'JPEG')
        idx += 1
    while idx < 200 and train_nl:
        src = random.choice(train_nl)
        aug = augment_image(src)
        aug.save(os.path.join(base_dir, 'train', 'Not_A_Leaf', f'train_aug_{idx}.jpg'), 'JPEG')
        idx += 1

    # Split Plant_Leaf
    random.shuffle(leaf_imgs)
    nl = min(len(leaf_imgs), 250)
    leaf_imgs = leaf_imgs[:nl]
    nl_train = int(nl * 0.7)
    nl_val = int(nl * 0.15)

    for i, im in enumerate(leaf_imgs[:nl_train]):
        im.save(os.path.join(base_dir, 'train', 'Plant_Leaf', f'train_{i}.jpg'), 'JPEG')
    for i, im in enumerate(leaf_imgs[nl_train:nl_train + nl_val]):
        im.save(os.path.join(base_dir, 'val', 'Plant_Leaf', f'val_{i}.jpg'), 'JPEG')
    for i, im in enumerate(leaf_imgs[nl_train + nl_val:]):
        im.save(os.path.join(base_dir, 'test', 'Plant_Leaf', f'test_{i}.jpg'), 'JPEG')

    counts = {
        "crop": "not_a_leaf",
        "classes": ["Not_A_Leaf", "Plant_Leaf"],
        "train": {
            "Not_A_Leaf": len(os.listdir(os.path.join(base_dir, 'train', 'Not_A_Leaf'))),
            "Plant_Leaf": len(os.listdir(os.path.join(base_dir, 'train', 'Plant_Leaf')))
        },
        "val": {
            "Not_A_Leaf": len(os.listdir(os.path.join(base_dir, 'val', 'Not_A_Leaf'))),
            "Plant_Leaf": len(os.listdir(os.path.join(base_dir, 'val', 'Plant_Leaf')))
        },
        "test": {
            "Not_A_Leaf": len(os.listdir(os.path.join(base_dir, 'test', 'Not_A_Leaf'))),
            "Plant_Leaf": len(os.listdir(os.path.join(base_dir, 'test', 'Plant_Leaf')))
        },
        "warning": "The Not_A_Leaf collection is small. High training accuracy does NOT imply high real-world accuracy."
    }
    with open(os.path.join(base_dir, 'dataset_report.json'), 'w') as f:
        json.dump(counts, f, indent=2)

    return counts

def main():
    print("=" * 60)
    print("NORMALIZING AND PREPARING ALL DATASETS")
    print("=" * 60)

    class_mapping = {
        "crops": {},
        "missing_crops": MISSING_CROPS
    }
    
    reports = {}

    for crop_name, crop_info in TARGET_CROPS.items():
        print(f"\n[*] Processing Crop: {crop_name.upper()} ...")
        crop_base = os.path.join('datasets', crop_name)
        shutil.rmtree(crop_base, ignore_errors=True)
        
        for split in ['train', 'val', 'test']:
            for target_cls in crop_info['classes'].keys():
                os.makedirs(os.path.join(crop_base, split, target_cls), exist_ok=True)

        class_samples = {}
        for target_cls, src_info in crop_info['classes'].items():
            valid_images = [] # list of (md5, pil_image)
            seen_hashes = set()

            if "source_dir" in src_info:
                s_dir = src_info["source_dir"]
                if os.path.exists(s_dir):
                    files = [os.path.join(s_dir, f) for f in os.listdir(s_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.webp'))]
                    # Cap large datasets to ~1200 images for fast balanced training
                    if len(files) > 1200:
                        random.shuffle(files)
                        files = files[:1200]
                    for f in files:
                        try:
                            h = get_file_md5(f)
                            if h in seen_hashes:
                                continue
                            seen_hashes.add(h)
                            im = Image.open(f).convert('RGB')
                            im.verify()
                            im = Image.open(f).convert('RGB')
                            valid_images.append((h, im))
                        except Exception:
                            continue
            elif "parquet_sources" in src_info:
                for p_dir, label_names in src_info["parquet_sources"]:
                    imgs = extract_parquet_images(p_dir, label_names, max_samples=1200)
                    for h, im in imgs:
                        if h not in seen_hashes:
                            seen_hashes.add(h)
                            valid_images.append((h, im))

            class_samples[target_cls] = valid_images
            print(f"  Class '{target_cls}': {len(valid_images)} unique clean images found")

        # Class balancing & splitting
        # Split: 70% train, 15% val, 15% test
        max_train_count = 0
        split_dict = {}
        for target_cls, items in class_samples.items():
            random.shuffle(items)
            total = len(items)
            n_train = int(total * 0.7)
            n_val = int(total * 0.15)
            
            train_items = items[:n_train]
            val_items = items[n_train:n_train + n_val]
            test_items = items[n_train + n_val:]
            
            split_dict[target_cls] = {
                "train": train_items,
                "val": val_items,
                "test": test_items
            }
            if len(train_items) > max_train_count:
                max_train_count = len(train_items)

        # Cap max_train_count to 800 to keep training nimble
        target_train_count = min(max_train_count, 800)

        # Save images and augment minority classes in training ONLY
        crop_report = {"crop": crop_name, "classes": {}}
        for target_cls, splits in split_dict.items():
            # Validation
            for i, (h, im) in enumerate(splits["val"]):
                im.save(os.path.join(crop_base, 'val', target_cls, f"val_{i}_{h[:8]}.jpg"), 'JPEG')
            # Test
            for i, (h, im) in enumerate(splits["test"]):
                im.save(os.path.join(crop_base, 'test', target_cls, f"test_{i}_{h[:8]}.jpg"), 'JPEG')
            # Train
            train_saved = 0
            for i, (h, im) in enumerate(splits["train"]):
                im.save(os.path.join(crop_base, 'train', target_cls, f"train_{i}_{h[:8]}.jpg"), 'JPEG')
                train_saved += 1
            
            # Minority Augmentation
            if splits["train"] and train_saved < target_train_count:
                needed = target_train_count - train_saved
                print(f"  [BALANCE] Augmenting minority class '{target_cls}' training set: {train_saved} -> {target_train_count} (+{needed} aug)")
                aug_idx = 0
                while train_saved < target_train_count:
                    _, src_im = random.choice(splits["train"])
                    aug_im = augment_image(src_im)
                    aug_im.save(os.path.join(crop_base, 'train', target_cls, f"train_aug_{aug_idx}.jpg"), 'JPEG')
                    aug_idx += 1
                    train_saved += 1

            crop_report["classes"][target_cls] = {
                "train": len(os.listdir(os.path.join(crop_base, 'train', target_cls))),
                "val": len(os.listdir(os.path.join(crop_base, 'val', target_cls))),
                "test": len(os.listdir(os.path.join(crop_base, 'test', target_cls))),
                "total": len(os.listdir(os.path.join(crop_base, 'train', target_cls))) +
                         len(os.listdir(os.path.join(crop_base, 'val', target_cls))) +
                         len(os.listdir(os.path.join(crop_base, 'test', target_cls)))
            }

        report_file = os.path.join(crop_base, 'dataset_report.json')
        with open(report_file, 'w') as f:
            json.dump(crop_report, f, indent=2)

        reports[crop_name] = crop_report

        class_mapping["crops"][crop_name] = {
            "target_classes": list(crop_info["classes"].keys()),
            "excluded_classes": crop_info["excluded"]
        }

    # Prepare Not_A_Leaf
    nl_report = prepare_non_leaf_dataset()
    reports["not_a_leaf"] = nl_report
    class_mapping["crops"]["not_a_leaf"] = {
        "target_classes": ["Not_A_Leaf", "Plant_Leaf"],
        "excluded_classes": {}
    }

    # Save class_mapping.json
    mapping_file = os.path.join('datasets', 'class_mapping.json')
    with open(mapping_file, 'w') as f:
        json.dump(class_mapping, f, indent=2)
    print(f"\n[SUCCESS] Saved {mapping_file}")

    # Print summary table
    print("\n" + "=" * 70)
    print(f"{'Crop':<12} | {'Class':<30} | {'Train':<7} | {'Val':<5} | {'Test':<5} | {'Total':<6}")
    print("-" * 70)
    for crop, data in reports.items():
        if "classes" in data and isinstance(data["classes"], dict):
            for cls_name, counts in data["classes"].items():
                print(f"{crop:<12} | {cls_name:<30} | {counts['train']:<7} | {counts['val']:<5} | {counts['test']:<5} | {counts['total']:<6}")
        elif "train" in data and isinstance(data["train"], dict):
            for cls_name in data["classes"]:
                tr = data["train"].get(cls_name, 0)
                va = data["val"].get(cls_name, 0)
                te = data["test"].get(cls_name, 0)
                tot = tr + va + te
                print(f"{crop:<12} | {cls_name:<30} | {tr:<7} | {va:<5} | {te:<5} | {tot:<6}")
    print("=" * 70)

    print("\nMissing / Not Ready Crops (Documented per Rule 22):")
    for mc, reason in MISSING_CROPS.items():
        print(f"  - {mc.upper()}: {reason}")

if __name__ == '__main__':
    main()
