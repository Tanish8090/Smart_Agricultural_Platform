import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

for repo in ["dpdl-benchmark/plant_village", "GVJahnavi/PlantVillage_dataset", "Project-AgML/apple_leaf_disease_classification", "Project-AgML/grape_leaf_disease_classification"]:
    url = f"https://datasets-server.huggingface.co/info?dataset={repo}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            dataset_info = data.get('dataset_info', {})
            # get default config
            for cfg, info in dataset_info.items():
                features = info.get('features', {})
                label_names = features.get('label', {}).get('names', [])
                print(f"=== {repo} ({cfg}) ===")
                print(f"Num classes: {len(label_names)}")
                for name in label_names:
                    if any(c in name.lower() for c in ['potato', 'tomato', 'corn', 'apple', 'grape']):
                        print(f"  {name}")
    except Exception as e:
        print(f"Error {repo}: {e}")
