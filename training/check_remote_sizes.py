import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "https://huggingface.co/api/datasets/GVJahnavi/PlantVillage_dataset"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        for s in data.get('siblings', []):
            print(f"{s.get('rfilename')}: {s.get('size', 0) / 1024 / 1024:.2f} MB")
except Exception as e:
    print("Error:", e)
