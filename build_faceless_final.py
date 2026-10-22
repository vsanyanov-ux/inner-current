import cv2
import numpy as np

# Загружаем полноразмерный исходный постер
src_path = r"C:\Users\vanya\.gemini\antigravity\brain\595d7ab7-6eb8-4a63-a314-66f392e88f80\afisha_fonarik_ru_1791828964068.jpg"
full_img = cv2.imread(src_path)
H, W = full_img.shape[:2]

# В полноразмерном изображении область кропа была: Y: 600..1050, X: 300..600
# Координаты смещения: off_y = 600, off_x = 300
off_y = 600
off_x = 300

img = full_img[off_y:off_y+450, off_x:off_x+300].copy()
h, w = img.shape[:2]

# 1. Тень от фонарика на деревянном столе: y: 345..378, x: 100..195
# Доски стола: берем чистые доски правее тени (x: 195..255)
clean_wood = img[345:378, 195:255]
clean_wood_resized = cv2.resize(clean_wood, (95, 33))

# Мягкая маска для тени на столе
t_mask = np.zeros((33, 95), dtype=np.float32)
cv2.ellipse(t_mask, (47, 16), (42, 14), 0, 0, 360, 1.0, -1)
t_mask = cv2.GaussianBlur(t_mask, (15, 15), 0)
t_mask_3ch = np.dstack([t_mask, t_mask, t_mask])

table_area = img[345:378, 100:195].astype(np.float32)
img[345:378, 100:195] = np.clip(table_area * (1.0 - t_mask_3ch) + clean_wood_resized.astype(np.float32) * t_mask_3ch, 0, 255).astype(np.uint8)

# 2. Торс человека в темно-серой кофте: y: 215..355, x: 95..205
torso_left = img[215:355, 35:95]
torso_right = img[215:355, 205:265]
torso_w = 110
torso_h = 140

patch_left = cv2.resize(torso_left, (torso_w // 2, torso_h))
patch_right = cv2.resize(torso_right, (torso_w // 2, torso_h))
torso_combined = np.hstack([patch_left, patch_right])

# Размываем вертикальный шов посередине
torso_combined = cv2.GaussianBlur(torso_combined, (25, 5), 0)
# Добавляем шум ткани
noise = np.random.normal(0, 2.5, torso_combined.shape).astype(np.float32)
torso_combined = np.clip(torso_combined.astype(np.float32) + noise, 0, 255).astype(np.uint8)

mask = np.zeros((torso_h, torso_w), dtype=np.float32)
cv2.ellipse(mask, (torso_w // 2, torso_h // 2), (torso_w // 2 - 4, torso_h // 2 - 4), 0, 0, 360, 1.0, -1)
mask = cv2.GaussianBlur(mask, (25, 25), 0)
mask_3ch = np.dstack([mask, mask, mask])

roi = img[215:355, 95:205].astype(np.float32)
img[215:355, 95:205] = np.clip(roi * (1.0 - mask_3ch) + torso_combined.astype(np.float32) * mask_3ch, 0, 255).astype(np.uint8)

# 3. Направленный мягкий конус света от верхнего фонарика над головой
# Верхний луч идет непрерывно сверху вниз, плавно расширяясь
light_layer = img.copy().astype(np.float32)
for y in range(0, 375):
    half_w = 32 + (y / 375.0) * 88
    for x in range(int(148 - half_w), int(148 + half_w)):
        if 0 <= x < w:
            dist = abs(x - 148) / half_w
            alpha = (1.0 - dist**1.6) * 0.44 * (1.0 - (y / 450.0) * 0.22)
            gold = np.array([135, 205, 255], dtype=np.float32)
            light_layer[y, x] = light_layer[y, x] * (1.0 - alpha) + gold * alpha

img_final = np.clip(light_layer, 0, 255).astype(np.uint8)

# Вставляем отретушированный кроп обратно в полноразмерный постер
full_img[off_y:off_y+450, off_x:off_x+300] = img_final

# Сохраняем финальный шедевр
out_full = r"C:\Users\vanya\.gemini\antigravity\brain\595d7ab7-6eb8-4a63-a314-66f392e88f80\afisha_fonarik_faceless_final.jpg"
cv2.imwrite(out_full, full_img)
print("Saved final full poster:", out_full)
