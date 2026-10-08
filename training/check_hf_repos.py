import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

repos = [
    "mohanty/PlantVillage",
    "dpdl-benchmark/plant_village",
    "GVJahnavi/PlantVillage_dataset",
    "PVS5665/PlantVillage",
    "Project-AgML/tomato_leaf_disease_classification",
    "Project-AgML/corn_leaf_disease_classification",
    "Project-AgML/apple_leaf_disease_classification",
    "Project-AgML/grape_leaf_disease_classification"
]

for repo in repos:
    url = f"https://huggingface.co/api/datasets/{repo}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print(f"[FOUND] {repo} (id: {data.get('id')})")
            # check siblings
            siblings = [s['rfilename'] for s in data.get('siblings', [])]
            parquet_files = [s for s in siblings if s.endswith('.parquet')]
            print(f"   total files: {len(siblings)}, parquet: {len(parquet_files)}")
            if parquet_files:
                print(f"   sample parquet: {parquet_files[:3]}")
    except Exception as e:
        print(f"[NOT FOUND] {repo}: {e}")
