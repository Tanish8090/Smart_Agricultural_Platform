import cv2
import numpy as np
from PIL import Image
from ultralytics import YOLO

m = YOLO('models/not_a_leaf/best.pt')
noise_img = Image.fromarray(np.zeros((224, 224, 3), dtype=np.uint8))
res = m.predict(noise_img, imgsz=224, verbose=False)
top1_idx = int(res[0].probs.top1)
pred_class = m.names[top1_idx]
conf = float(res[0].probs.top1conf)
print(f"Prediction for black image: {pred_class}, conf: {conf}")
for idx, c in enumerate(res[0].probs.data):
    print(f" - {m.names[idx]}: {float(c):.4f}")
