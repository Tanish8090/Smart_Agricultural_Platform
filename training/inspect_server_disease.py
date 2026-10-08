import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines in server.py: {len(lines)}")

for i, line in enumerate(lines):
    if '/api/disease' in line or 'crop_models' in line or 'CROP_MODELS' in line or 'predict' in line or 'not_ready' in line:
        print(f"Line {i+1}: {line.strip()[:100]}")
