import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

for crop in ['potato', 'rice', 'tomato', 'corn', 'apple', 'grape']:
    m_path = os.path.join('models', crop, 'best.pt')
    meta_path = os.path.join('models', crop, 'metadata.json')
    if os.path.exists(m_path):
        size = os.path.getsize(m_path) / 1024 / 1024
        classes = None
        if os.path.exists(meta_path):
            import json
            with open(meta_path, 'r', encoding='utf-8') as f:
                classes = json.load(f).get('classes')
        print(f"[✓] {crop:10s}: best.pt ready ({size:.2f} MB), classes={classes}")
    else:
        print(f"[-] {crop:10s}: training / pending...")
