import os
import glob
from PIL import Image
from ultralytics import YOLO
import numpy as np

m = YOLO('models/not_a_leaf/best.pt')

# Test random image with colored stripes
stripes = np.zeros((224, 224, 3), dtype=np.uint8)
stripes[:, :74, 0] = 255 # red
stripes[:, 74:148, 1] = 255 # green
stripes[:, 148:, 2] = 255 # blue
img = Image.fromarray(stripes)
res = m.predict(img, imgsz=224, verbose=False)
idx = int(res[0].probs.top1)
print(f"Colored stripes: {m.names[idx]}, conf: {float(res[0].probs.top1conf):.4f}")

# Look for non-leaf training/test images in dataset
nl_files = glob.glob('**/Not_A_Leaf/*.*', recursive=True) + glob.glob('**/not_a_leaf/*.*', recursive=True)
print(f"Found {len(nl_files)} not_a_leaf files in workspace.")
for f in nl_files[:5]:
    if f.endswith('.jpg') or f.endswith('.png'):
        res = m.predict(f, imgsz=224, verbose=False)
        idx = int(res[0].probs.top1)
        print(f"File {f}: {m.names[idx]}, conf: {float(res[0].probs.top1conf):.4f}")
