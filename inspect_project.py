import os
import sys
import glob
import zipfile
import json
from collections import defaultdict, Counter

reconfigure_stdout = getattr(sys.stdout, 'reconfigure', None)
if callable(reconfigure_stdout):
    reconfigure_stdout(encoding='utf-8')

print("=" * 60)
print("PROJECT AND DATASET INSPECTION")
print("=" * 60)

# 1. Python Environment
print("\n--- 1. PYTHON ENVIRONMENT ---")
print("sys.executable:", sys.executable)
print("sys.version:", sys.version)

try:
    import torch
    print("torch:", torch.__version__)
    print("torch.cuda.is_available():", torch.cuda.is_available())
    mps_avail = getattr(torch.backends, 'mps', None) and torch.backends.mps.is_available()
    print("torch.backends.mps.is_available():", mps_avail)
except ImportError:
    print("torch: NOT INSTALLED")

try:
    import ultralytics
    print("ultralytics:", ultralytics.__version__)
except ImportError:
    print("ultralytics: NOT INSTALLED")

# 2. Archives Scan
print("\n--- 2. ARCHIVES SCAN ---")
archives = []
for root, dirs, files in os.walk('.'):
    # Avoid scanning inside extracted dirs if any
    for f in files:
        if f.lower().endswith(('.zip', '.rar', '.7z', '.tar', '.tar.gz', '.tgz')):
            archives.append(os.path.join(root, f))

for a in archives:
    size_mb = os.path.getsize(a) / (1024 * 1024)
    print(f"Archive: {a} ({size_mb:.2f} MB)")
    if a.lower().endswith('.zip'):
        try:
            with zipfile.ZipFile(a, 'r') as z:
                names = [n for n in z.namelist() if not n.endswith('/')]
                img_exts = Counter(os.path.splitext(n)[1].lower() for n in names)
                # Check top folders
                top_folders = Counter(n.split('/')[0] for n in names if '/' in n)
                # Check annotations (.txt, .xml, .json)
                annot_exts = [ext for ext in img_exts if ext in ('.txt', '.xml', '.json')]
                print(f"   Files: {len(names)} | Images: {sum(v for k, v in img_exts.items() if k in ('.jpg', '.jpeg', '.png', '.bmp', '.webp'))}")
                print(f"   Extensions: {dict(img_exts)}")
                print(f"   Top Folders: {dict(top_folders)}")
                if annot_exts:
                    print(f"   Annotation files found: {annot_exts}")
        except Exception as e:
            print(f"   Error reading zip: {e}")

# 3. Existing Dataset Directories, Models, Runs
print("\n--- 3. EXISTING DIRECTORIES & ARTIFACTS ---")
check_dirs = ['dataset', 'datasets', 'models', 'runs', 'data_raw', 'data_processed', 'training', 'logs']
for d in check_dirs:
    exists = os.path.exists(d)
    print(f"Directory '{d}': {'EXISTS' if exists else 'NOT FOUND'}")
    if exists:
        subitems = os.listdir(d)
        print(f"   Contents: {subitems[:10]}")

# 4. Existing Models
print("\n--- 4. EXISTING MODEL FILES ---")
model_files = []
for root, dirs, files in os.walk('.'):
    for f in files:
        if f.lower().endswith(('.pt', '.onnx', '.tflite', '.h5', '.engine', '.bin')):
            model_files.append(os.path.join(root, f))
if model_files:
    for m in model_files:
        print("Model found:", m)
else:
    print("No model files (.pt, .onnx, etc.) found in workspace.")

# 5. Existing Scripts
print("\n--- 5. EXISTING SCRIPTS ---")
scripts = []
for root, dirs, files in os.walk('.'):
    if '__MACOSX' in root or '.git' in root:
        continue
    for f in files:
        if f.lower().endswith(('.py', '.js', '.sh', '.bat')):
            scripts.append(os.path.join(root, f))
for s in scripts:
    print("Script:", s)

# 6. Test Photos & Sample Data
print("\n--- 6. TEST PHOTOS & SAMPLE DATA ---")
for root, dirs, files in os.walk('.'):
    if '__MACOSX' in root:
        continue
    for f in files:
        if f.lower().endswith(('.jpg', '.jpeg', '.png')) and ('test' in root.lower() or 'sample' in root.lower() or 'photo' in root.lower()):
            print("Sample photo:", os.path.join(root, f))

print("\n" + "=" * 60)
print("END OF INSPECTION")
print("=" * 60)
