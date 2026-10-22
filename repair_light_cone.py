import cv2
import numpy as np

# Исходное изображение
img_path = r"C:\Users\vanya\.gemini\antigravity\brain\595d7ab7-6eb8-4a63-a314-66f392e88f80\afisha_fonarik_ru_1791828964068.jpg"
img = cv2.imread(img_path)
h, w = img.shape[:2]

# Центр источника света вверху
apex_x = 502
apex_y = 475

# Создаем копию изображения
clean = img.copy()

# Восстанавливаем деревянную поверхность стола на участке Y=915..1000, X=400..510
# Берем образец текстуры стола чуть левее (X=330..390) и правее (X=520..580)
table_sample_left = img[915:995, 330:390]
table_sample_right = img[915:995, 520:580]
table_blend = cv2.addWeighted(cv2.resize(table_sample_left, (110, 80)), 0.5, cv2.resize(table_sample_right, (110, 80)), 0.5, 0)
# Добавляем теплое освещение от луча
table_blend = np.clip(table_blend.astype(np.float32) * 1.15 + 10, 0, 255).astype(np.uint8)

# Вставляем деревянную поверхность стола
clean[915:995, 400:510] = cv2.GaussianBlur(table_blend, (5, 5), 0)

# Теперь моделируем естественный конус света от Y=720 до Y=925
# Внутри конуса свет идет непрерывно
# Фоновый цвет темного силуэта (одежды): около BGR [30, 28, 26]
bg_color = np.array([30, 28, 26], dtype=np.float32)

for y in range(720, 925):
    # Ширина конуса на высоте y
    t = (y - apex_y) / (925 - apex_y)
    # Полуширина конуса на высоте y
    half_w = int(60 + t * 140)
    
    # Центр луча
    cx = apex_x
    x_start = max(0, cx - half_w)
    x_end = min(w, cx + half_w)
    
    for x in range(350, 560):
        dist = abs(x - cx) / half_w
        if dist < 1.0:
            # Внутри конуса: мягкое затухание от центра к краям
            intensity = (1.0 - dist**1.5) * (1.0 - t * 0.4)
            # Цвет луча: золотисто-янтарный теплый свет
            beam_color = np.array([130, 205, 250], dtype=np.float32) * intensity + np.array([25, 35, 45], dtype=np.float32) * (1.0 - intensity)
            
            # Смешиваем с исходным
            alpha = 0.85 if (800 <= y <= 915 and 390 <= x <= 515) else 0.0
            if alpha > 0:
                clean[y, x] = np.clip(clean[y, x].astype(np.float32) * (1 - alpha) + beam_color * alpha, 0, 255).astype(np.uint8)
        else:
            if 800 <= y <= 915 and 370 <= x <= 530:
                # Вне конуса: силуэт темной одежды
                clean[y, x] = np.clip(bg_color + np.random.normal(0, 3, 3), 0, 255).astype(np.uint8)

# Финальное мягкое разглаживание швов
roi = clean[790:995, 360:540]
clean[790:995, 360:540] = cv2.bilateralFilter(roi, 9, 75, 75)

out_file = r"C:\Users\vanya\.gemini\antigravity\brain\595d7ab7-6eb8-4a63-a314-66f392e88f80\afisha_fonarik_clean.jpg"
cv2.imwrite(out_file, clean)
print("Saved cleanly to:", out_file)
