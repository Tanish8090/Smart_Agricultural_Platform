import os
import sys
import shutil
import hashlib
import random
import json
import io
from collections import Counter
from PIL import Image, ImageEnhance
import pyarrow.parquet as pq

sys.stdout.reconfigure(encoding='utf-8')

RANDOM_SEED = 42
random.seed(RANDOM_SEED)

def get_bytes_md5(data):
    return hashlib.md5(data).hexdigest()

def augment_image(pil_img):
    transforms = [
        lambda img: img.transpose(Image.FLIP_LEFT_RIGHT),
        lambda img: img.transpose(Image.FLIP_TOP_BOTTOM),
        lambda img: img.rotate(90, expand=False),
        lambda img: img.rotate(180, expand=False),
        lambda img: img.rotate(270, expand=False),
        lambda img: ImageEnhance.Brightness(img).enhance(random.uniform(0.88, 1.12)),
        lambda img: ImageEnhance.Contrast(img).enhance(random.uniform(0.88, 1.12)),
    ]
    fn = random.choice(transforms)
    return fn(pil_img)

def extract_from_parquet_files(files_and_targets, max_per_class=350):
    """
    files_and_targets: list of (parquet_file, target_class_to_source_labels_map)
    returns: dict of {target_class: [PIL.Image]}
    """
    class_images = {k: [] for item in files_and_targets for k in item[1].keys()}
    seen_hashes = {k: set() for k in class_images.keys()}

    for p_file, target_map in files_and_targets:
        if not os.path.exists(p_file):
            print(f"[!] Warning: Parquet file not found: {p_file}")
            continue

        print(f"Reading {p_file} ...")
        table = pq.read_table(p_file)
        meta = json.loads(table.schema.metadata.get(b'huggingface', b'{}'))
        names = meta.get('info', {}).get('features', {}).get('label', {}).get('names', [])
        name_to_idx = {name: i for i, name in enumerate(names)}

        # Map target class to label indices
        target_to_indices = {}
        for tgt_cls, src_labels in target_map.items():
            indices = set()
            for sl in src_labels:
                if sl in name_to_idx:
                    indices.add(name_to_idx[sl])
            target_to_indices[tgt_cls] = indices

        # Process rows in table
        img_col = table['image']
        lbl_col = table['label']

        for row_idx in range(len(table)):
            lbl_val = lbl_col[row_idx].as_py()
            for tgt_cls, idx_set in target_to_indices.items():
                if lbl_val in idx_set:
                    if len(class_images[tgt_cls]) >= max_per_class:
                        continue
                    item = img_col[row_idx].as_py()
                    b = item.get('bytes') if isinstance(item, dict) else item
                    if b:
                        h = get_bytes_md5(b)
                        if h not in seen_hashes[tgt_cls]:
                            seen_hashes[tgt_cls].add(h)
                            try:
                                img = Image.open(io.BytesIO(b)).convert('RGB')
                                class_images[tgt_cls].append(img)
                            except Exception as e:
                                pass

    for k, v in class_images.items():
        print(f"  Extracted {len(v)} images for target class '{k}'")
    return class_images

def save_and_split_dataset(crop_name, class_images, min_per_class=150):
    dest_dir = os.path.join('datasets', crop_name)
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    for split in ['train', 'val', 'test']:
        for cls_name in class_images.keys():
            os.makedirs(os.path.join(dest_dir, split, cls_name), exist_ok=True)

    summary = {}

    for cls_name, images in class_images.items():
        # If below min_per_class, augment
        if len(images) < min_per_class and len(images) > 0:
            print(f"  [Augmenting] Class '{cls_name}' has {len(images)} images, augmenting to {min_per_class}...")
            orig_imgs = list(images)
            while len(images) < min_per_class:
                chosen = random.choice(orig_imgs)
                images.append(augment_image(chosen.copy()))

        random.shuffle(images)
        n = len(images)
        n_train = int(n * 0.70)
        n_val = int(n * 0.20)
        n_test = n - n_train - n_val

        splits = {
            'train': images[:n_train],
            'val': images[n_train:n_train+n_val],
            'test': images[n_train+n_val:]
        }

        for split_name, split_imgs in splits.items():
            split_dir = os.path.join(dest_dir, split_name, cls_name)
            for i, img in enumerate(split_imgs):
                fpath = os.path.join(split_dir, f"{cls_name}_{i:04d}.jpg")
                img.save(fpath, 'JPEG', quality=95)

        summary[cls_name] = {
            'total': n,
            'train': len(splits['train']),
            'val': len(splits['val']),
            'test': len(splits['test'])
        }

    report_path = os.path.join(dest_dir, 'dataset_report.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump({'crop': crop_name, 'classes': list(class_images.keys()), 'summary': summary}, f, indent=2)
    print(f"[✓] Saved {crop_name} dataset ({summary})")

def main():
    print("=" * 60)
    print("PREPARING STANDARDIZED DATASETS FOR ALL TARGET CROPS")
    print("=" * 60)

    pv_dir = 'data_raw/huggingface/PlantVillage_dataset/data'
    pv_files = [os.path.join(pv_dir, f) for f in os.listdir(pv_dir) if f.endswith('.parquet')]

    # 1. POTATO
    print("\n--- [1] POTATO ---")
    potato_targets = {
        'Potato___Early_blight': ['Potato___Early_blight'],
        'Potato___Late_blight': ['Potato___Late_blight'],
        'Potato___healthy': ['Potato___healthy']
    }
    potato_images = extract_from_parquet_files([(f, potato_targets) for f in pv_files], max_per_class=350)
    # Also add images from data_raw/archive (4) if needed
    for sub, cls in [('Healthy', 'Potato___healthy'), ('Late Blight', 'Potato___Late_blight')]:
        dir4 = os.path.join('data_raw/archive (4)', sub)
        if os.path.exists(dir4):
            for fname in os.listdir(dir4):
                if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
                    if len(potato_images[cls]) < 350:
                        try:
                            im = Image.open(os.path.join(dir4, fname)).convert('RGB')
                            potato_images[cls].append(im)
                        except Exception:
                            pass
    save_and_split_dataset('potato', potato_images)

    # 2. RICE
    print("\n--- [2] RICE ---")
    rice_files_targets = []
    r_dir1 = 'data_raw/huggingface/rice_leaf_disease_classification/data'
    if os.path.exists(r_dir1):
        for f in os.listdir(r_dir1):
            if f.endswith('.parquet'):
                rice_files_targets.append((
                    os.path.join(r_dir1, f),
                    {
                        'Rice___Blast': ['Leaf_Blast'],
                        'Rice___Brown_spot': ['Brown_Spot'],
                        'Rice___healthy': ['Healthy_Rice_Leaf']
                    }
                ))
    r_dir2 = 'data_raw/huggingface/rice_leaf_disease_classification_india/data'
    if os.path.exists(r_dir2):
        for f in os.listdir(r_dir2):
            if f.endswith('.parquet'):
                rice_files_targets.append((
                    os.path.join(r_dir2, f),
                    {
                        'Rice___Blast': ['Blast'],
                        'Rice___Brown_spot': ['Brownspot']
                    }
                ))
    rice_images = extract_from_parquet_files(rice_files_targets, max_per_class=350)
    save_and_split_dataset('rice', rice_images)

    # 3. TOMATO
    print("\n--- [3] TOMATO ---")
    tomato_targets = {
        'Tomato___Early_blight': ['Tomato___Early_blight'],
        'Tomato___Late_blight': ['Tomato___Late_blight'],
        'Tomato___healthy': ['Tomato___healthy']
    }
    tomato_images = extract_from_parquet_files([(f, tomato_targets) for f in pv_files], max_per_class=350)
    save_and_split_dataset('tomato', tomato_images)

    # 4. CORN
    print("\n--- [4] CORN ---")
    corn_targets = {
        'Corn___Common_rust': ['Corn_(maize)___Common_rust_'],
        'Corn___Leaf_blight': ['Corn_(maize)___Northern_Leaf_Blight'],
        'Corn___healthy': ['Corn_(maize)___healthy']
    }
    corn_images = extract_from_parquet_files([(f, corn_targets) for f in pv_files], max_per_class=350)
    save_and_split_dataset('corn', corn_images)

    # 5. APPLE
    print("\n--- [5] APPLE ---")
    apple_targets = {
        'Apple___Scab': ['Apple__Apple_scab'],
        'Apple___healthy': ['Apple___healthy']
    }
    apple_images = extract_from_parquet_files([(f, apple_targets) for f in pv_files], max_per_class=350)
    save_and_split_dataset('apple', apple_images)

    # 6. GRAPE
    print("\n--- [6] GRAPE ---")
    grape_targets = {
        'Grape___Black_rot': ['Grape___Black_rot'],
        'Grape___healthy': ['Grape___healthy']
    }
    grape_images = extract_from_parquet_files([(f, grape_targets) for f in pv_files], max_per_class=350)
    save_and_split_dataset('grape', grape_images)

    print("\n=======================================================")
    print("ALL 6 NEW/UPDATED DATASETS PREPARED SUCCESSFULLY!")
    print("=======================================================")

if __name__ == '__main__':
    main()
