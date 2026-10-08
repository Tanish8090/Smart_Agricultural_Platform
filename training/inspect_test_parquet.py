import os
import sys
import json
import pyarrow.parquet as pq
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

parquet_file = 'data_raw/huggingface/PlantVillage_dataset/data/test-00000-of-00001.parquet'
if os.path.exists(parquet_file):
    table = pq.read_table(parquet_file)
    print("Table columns:", table.column_names)
    print("Total rows in test set:", len(table))
    meta = json.loads(table.schema.metadata.get(b'huggingface', b'{}'))
    label_names = meta.get('info', {}).get('features', {}).get('label', {}).get('names', [])
    labels = table['label'].to_pylist()
    counts = Counter(labels)
    for idx, name in enumerate(label_names):
        if any(c in name.lower() for c in ['potato', 'tomato', 'corn', 'apple', 'grape']):
            print(f"  [{idx}] {name}: {counts[idx]} test samples")
else:
    print(f"{parquet_file} does not exist yet")
