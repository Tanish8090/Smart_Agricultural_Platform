import pyarrow.parquet as pq
import json
import sys
import os
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

for name in ['rice_leaf_disease_classification', 'rice_leaf_disease_classification_india']:
    p = f'data_raw/huggingface/{name}/data'
    if os.path.exists(p):
        for f in os.listdir(p):
            if f.endswith('.parquet'):
                t = pq.read_table(os.path.join(p, f))
                meta = json.loads(t.schema.metadata.get(b'huggingface', b'{}'))
                names = meta.get('info', {}).get('features', {}).get('label', {}).get('names', [])
                counts = Counter(t['label'].to_pylist())
                print(f"=== {name} / {f} ===")
                for idx, cname in enumerate(names):
                    print(f"  {cname}: {counts[idx]}")
