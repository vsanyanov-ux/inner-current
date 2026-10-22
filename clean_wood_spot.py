import cv2
import numpy as np

# Загружаем afisha_fonarik_faceless_final.jpg
path = r"C:\Users\vanya\.gemini\antigravity\brain\595d7ab7-6eb8-4a63-a314-66f392e88f80\afisha_fonarik_faceless_final.jpg"
img = cv2.imread(path)

# Участок с темным овалом на столе: Y: 940..980, X: 420..500
# Берем чистые доски правее: Y: 940..980, X: 510..590
wood_src = img[940:980, 510:590]

# Создаем эллиптическую маску
mask = np.zeros((40, 80), dtype=np.float32)
cv2.ellipse(mask, (40, 20), (35, 16), 0, 0, 360, 1.0, -1)
mask = cv2.GaussianBlur(mask, (15, 15), 0)
mask_3ch = np.dstack([mask, mask, mask])

roi = img[940:980, 420:500].astype(np.float32)
img[940:980, 420:500] = np.clip(roi * (1.0 - mask_3ch) + wood_src.astype(np.float32) * mask_3ch, 0, 255).astype(np.uint8)

# Смягчаем световое пятно на столе
spot = img[930:990, 410:510]
img[930:990, 410:510] = cv2.bilateralFilter(spot, 9, 40, 40)

out = r"C:\Users\vanya\.gemini\antigravity\brain\595d7ab7-6eb8-4a63-a314-66f392e88f80\afisha_fonarik_faceless_master.jpg"
cv2.imwrite(out, img)
print("Master ready:", out)
