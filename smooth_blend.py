import cv2
import numpy as np

img_path = r"C:\Users\vanya\.gemini\antigravity\brain\595d7ab7-6eb8-4a63-a314-66f392e88f80\afisha_fonarik_ru_1791828964068.jpg"
img = cv2.imread(img_path)
h, w = img.shape[:2]

# Диапазон руки и фонарика: Y от 790 до 960, X от 365 до 535
x1, x2 = 365, 535
y1, y2 = 790, 960
box_w = x2 - x1
box_h = y2 - y1

# Берем чистый вертикальный фрагмент конуса света выше рук (Y: 620..770, X: 415..585)
clean_beam = img[620:770, 415:585]
beam_patch = cv2.resize(clean_beam, (box_w, box_h), interpolation=cv2.INTER_CUBIC)

# Создаем плавную маску
mask = np.zeros((box_h, box_w), dtype=np.float32)
cv2.ellipse(mask, (box_w // 2, box_h // 2), (box_w // 2 - 10, box_h // 2 - 10), 0, 0, 360, 1.0, -1)
mask = cv2.GaussianBlur(mask, (35, 35), 0)
mask_3ch = np.dstack([mask, mask, mask])

# Смешиваем
roi = img[y1:y2, x1:x2].astype(np.float32)
blended = roi * (1.0 - mask_3ch) + beam_patch.astype(np.float32) * mask_3ch

img_out = img.copy()
img_out[y1:y2, x1:x2] = np.clip(blended, 0, 255).astype(np.uint8)

# Смягчаем переход у столешницы (Y: 930..980, X: 400..510)
# На столе должен лежать ровный теплый свет от падающего луча
table_light = cv2.GaussianBlur(img_out[930:980, 400:510], (21, 21), 0)
img_out[930:980, 400:510] = cv2.addWeighted(img_out[930:980, 400:510], 0.3, table_light, 0.7, 0)

out_file = r"C:\Users\vanya\.gemini\antigravity\brain\595d7ab7-6eb8-4a63-a314-66f392e88f80\afisha_fonarik_final.jpg"
cv2.imwrite(out_file, img_out)
print("Saved final to:", out_file)
