import cv2
import numpy as np

# Загружаем кроп
img = cv2.imread('crop_beam_torso.jpg')
h, w = img.shape[:2]

# 1. Ликвидируем свечение нижнего фонарика (y: 215..260, x: 120..180) и сам фонарик с рукой (y: 215..355, x: 100..200)
# Берем чистую темную кофту слева (x: 40..95) и справа (x: 205..260)
torso_left = img[215:355, 40:95]
torso_right = img[215:355, 205:260]

torso_w = 100
torso_h = 355 - 215 # 140

patch_left = cv2.resize(torso_left, (torso_w // 2, torso_h))
patch_right = cv2.resize(torso_right, (torso_w // 2, torso_h))
torso_combined = np.hstack([patch_left, patch_right])

# Добавляем шум ткани
noise = np.random.normal(0, 3, torso_combined.shape).astype(np.float32)
torso_combined = np.clip(torso_combined.astype(np.float32) + noise, 0, 255).astype(np.uint8)

# Мягкая маска для вставки кофты
mask = np.zeros((torso_h, torso_w), dtype=np.float32)
cv2.ellipse(mask, (torso_w // 2, torso_h // 2), (torso_w // 2 - 5, torso_h // 2 - 5), 0, 0, 360, 1.0, -1)
mask = cv2.GaussianBlur(mask, (25, 25), 0)
mask_3ch = np.dstack([mask, mask, mask])

roi = img[215:355, 100:200].astype(np.float32)
img[215:355, 100:200] = np.clip(roi * (1.0 - mask_3ch) + torso_combined.astype(np.float32) * mask_3ch, 0, 255).astype(np.uint8)

# 2. Восстанавливаем деревянные доски стола на месте основания фонарика (y: 338..375, x: 120..180)
# Доски стола имеют вертикальную структуру. Берем полосу досок стола справа от фонарика (x: 185..245)
table_source = img[338:375, 185:245]
table_mask = np.zeros((37, 60), dtype=np.float32)
cv2.ellipse(table_mask, (30, 18), (25, 15), 0, 0, 360, 1.0, -1)
table_mask = cv2.GaussianBlur(table_mask, (15, 15), 0)
table_mask_3ch = np.dstack([table_mask, table_mask, table_mask])

table_roi = img[338:375, 120:180].astype(np.float32)
img[338:375, 120:180] = np.clip(table_roi * (1.0 - table_mask_3ch) + table_source.astype(np.float32) * table_mask_3ch, 0, 255).astype(np.uint8)

# 3. Накладываем идеальный направленный конус света от верхнего фонарика прямо на стол!
# Верхний луч расширяется от центра x=148
light_layer = img.copy().astype(np.float32)
for y in range(0, 365):
    # Конус света расширяется сверху вниз
    half_w = 32 + (y / 365.0) * 88
    for x in range(int(148 - half_w), int(148 + half_w)):
        if 0 <= x < w:
            dist = abs(x - 148) / half_w
            # Плавный профиль освещенности
            alpha = (1.0 - dist**1.7) * 0.48 * (1.0 - (y / 450.0) * 0.25)
            # Теплый золотисто-янтарный луч (BGR: 140, 210, 255)
            gold = np.array([135, 205, 255], dtype=np.float32)
            light_layer[y, x] = light_layer[y, x] * (1.0 - alpha) + gold * alpha

result = np.clip(light_layer, 0, 255).astype(np.uint8)

# Сохраняем результат
cv2.imwrite('crop_clean_result.jpg', result)
print('Perfect blend saved.')
