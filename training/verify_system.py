#!/usr/bin/env python3
import urllib.request
import json
import base64
import os
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

available_crops = ['wheat', 'cotton', 'sugarcane', 'potato', 'rice', 'soybean']
nl_path = 'data_raw/not_a_leaf/asset_bus.jpg'
with open(nl_path, 'rb') as f:
    b64_bus = base64.b64encode(f.read()).decode('utf-8')

for crop in available_crops:
    print(f"\n{'='*20} VERIFICATION SUITE: {crop.upper()} {'='*20}")
    td = f'datasets/{crop}/test'
    classes = sorted(os.listdir(td))
    healthy_cls = [c for c in classes if 'healthy' in c.lower()][0]
    disease_cls = [c for c in classes if 'healthy' not in c.lower()][0]

    # 1. Healthy Image
    h_files = [f for f in os.listdir(f'{td}/{healthy_cls}') if f.endswith(('.jpg', '.png'))]
    with open(f'{td}/{healthy_cls}/{h_files[0]}', 'rb') as f:
        b64_h = base64.b64encode(f.read()).decode('utf-8')
    payload_h = json.dumps({'image': b64_h, 'crop': crop.capitalize()}).encode('utf-8')
    req_h = urllib.request.Request('http://localhost:8080/api/disease/analyze', data=payload_h, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req_h, timeout=15) as r:
        res_h = json.loads(r.read().decode('utf-8'))
    print(f"  [1. HEALTHY]  Pred: {res_h.get('prediction')} | Conf: {res_h.get('confidence')} | Area: {res_h.get('affected_area_percent')}% | Overlay: {bool(res_h.get('highlight_image'))}")

    # 2. Diseased Image
    d_files = [f for f in os.listdir(f'{td}/{disease_cls}') if f.endswith(('.jpg', '.png'))]
    with open(f'{td}/{disease_cls}/{d_files[0]}', 'rb') as f:
        b64_d = base64.b64encode(f.read()).decode('utf-8')
    payload_d = json.dumps({'image': b64_d, 'crop': crop.capitalize()}).encode('utf-8')
    req_d = urllib.request.Request('http://localhost:8080/api/disease/analyze', data=payload_d, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req_d, timeout=15) as r:
        res_d = json.loads(r.read().decode('utf-8'))
    print(f"  [2. DISEASED] Pred: {res_d.get('prediction')} | Conf: {res_d.get('confidence')} | Area: {res_d.get('affected_area_percent')}% | Overlay: {bool(res_d.get('highlight_image'))}")

    # 3. Unrelated Non-Leaf Image
    payload_nl = json.dumps({'image': b64_bus, 'crop': crop.capitalize()}).encode('utf-8')
    req_nl = urllib.request.Request('http://localhost:8080/api/disease/analyze', data=payload_nl, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req_nl, timeout=15) as r:
        res_nl = json.loads(r.read().decode('utf-8'))
    print(f"  [3. NON-LEAF] IsLeaf: {res_nl.get('is_leaf')} | Pred: {res_nl.get('prediction')} | Msg: \"{res_nl.get('message')}\"")

print("\n" + "="*60)
print("ALL LIVE ENDPOINT TESTS COMPLETED SUCCESSFULLY!")
print("="*60)
