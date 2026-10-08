import os
import sys
import json
import pyarrow.parquet as pq
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

dir_path = 'data_raw/huggingface/PlantVillage_dataset/data'
files = [f for f in os.listdir(dir_path) if f.endswith('.parquet')]
print(f"Parquet files currently ready: {files}")

total_counts = Counter()
label_names = []

for f in files:
    fp = os.path.join(dir_path, f)
    table = pq.read_table(fp)
    if not label_names:
        meta = json.loads(table.schema.metadata.get(b'huggingface', b'{}'))
        label_names = meta.get('info', {}).get('features', {}).get('label', {}).get('names', [])
    labels = table['label'].to_pylist()
    total_counts.update(labels)

print("\nReady Target Class Sample Counts in available files:")
for idx, name in enumerate(label_names):
    if any(c in name.lower() for c in ['potato', 'tomato', 'corn', 'apple', 'grape']):
        print(f"  [{idx:2d}] {name:50s}: {total_counts[idx]} samples")
