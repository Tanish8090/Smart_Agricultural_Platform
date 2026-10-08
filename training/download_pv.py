import os
import sys
from huggingface_hub import snapshot_download

sys.stdout.reconfigure(encoding='utf-8')

local_dir = os.path.join("data_raw", "huggingface", "PlantVillage_dataset")
os.makedirs(local_dir, exist_ok=True)

print(f"Downloading GVJahnavi/PlantVillage_dataset to {local_dir}...")
path = snapshot_download(
    repo_id="GVJahnavi/PlantVillage_dataset",
    repo_type="dataset",
    local_dir=local_dir,
    local_dir_use_symlinks=False,
    max_workers=4
)
print(f"Download complete: {path}")

# List files
for root, dirs, files in os.walk(local_dir):
    for f in files:
        fp = os.path.join(root, f)
        print(f"  {f} ({os.path.getsize(fp) / 1024 / 1024:.2f} MB)")
