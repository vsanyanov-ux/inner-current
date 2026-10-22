import cv2
import numpy as np

# 1. Загружаем фотографию спикера
src_path = r"C:\Users\vanya\.gemini\antigravity\brain\595d7ab7-6eb8-4a63-a314-66f392e88f80\.user_uploaded\media_1791828744136_3f4d95f3.jpg"
src = cv2.imread(src_path)
h, w = src.shape[:2] # 1024 x 682

# Создаем вертикальный холст пропорций А4: 1414 x 1000
canvas_h, canvas_w = 1414, 1000
canvas = np.zeros((canvas_h, canvas_w, 3), dtype=np.uint8)

# Масштабируем фото спикера так, чтобы он сидел за столом в нижней/центральной части композиции
target_w = 1000
target_h = int(h * (target_w / w))
resized_src = cv2.resize(src, (target_w, target_h))

# Позиционируем в нижней части (стол на уровне y ~ 1100..1414, голова на уровне y ~ 500..750)
y_offset = canvas_h - target_h + 80
if y_offset < 0:
    crop_top = -y_offset
    resized_src = resized_src[crop_top:crop_top+canvas_h]
    y_offset = 0

canvas[y_offset:y_offset+resized_src.shape[0], :target_w] = resized_src

# 2. Создаем ночной атмосферный приглушенный полумрак (moody cafe)
# Затемняем всю сцену, уводя в благородный теплый графит
dark_base = canvas.astype(np.float32) * 0.32
# Добавляем синевато-угольный оттенок теней
dark_base[:, :, 0] += 12 # Blue channel
dark_base[:, :, 1] += 8
dark_base[:, :, 2] += 6
canvas = np.clip(dark_base, 0, 255).astype(np.uint8)

# 3. Лицо полностью уводим в глубокую тень (не видно лица)
# Координаты лица на холсте: X ~ 440..560, Y ~ 470..620
face_mask = np.zeros((canvas_h, canvas_w), dtype=np.float32)
cv2.ellipse(face_mask, (500, 530), (70, 95), 0, 0, 360, 1.0, -1)
face_mask = cv2.GaussianBlur(face_mask, (55, 55), 0)
face_mask_3ch = np.dstack([face_mask]*3)

# Сильно затемняем область лица до глубокого силуэта
canvas = np.clip(canvas.astype(np.float32) * (1.0 - face_mask_3ch * 0.78), 0, 255).astype(np.uint8)

# 4. Рисуем стильный металлический карманный фонарик НАД ГОЛОВОЙ (Y ~ 380..440, X ~ 485..515)
# Фонарик направлен вниз
fl_cx, fl_cy = 500, 410

# Корпус фонарика (черно-титановый цилиндр с насечками и золотым кольцом)
cv2.rectangle(canvas, (fl_cx - 14, fl_cy - 48), (fl_cx + 14, fl_cy - 8), (40, 42, 48), -1)
cv2.rectangle(canvas, (fl_cx - 15, fl_cy - 48), (fl_cx + 15, fl_cy - 42), (60, 65, 75), -1)
# Рельефные насечки рукоятки
for y_rib in range(fl_cy - 40, fl_cy - 12, 5):
    cv2.line(canvas, (fl_cx - 14, y_rib), (fl_cx + 14, y_rib), (25, 27, 30), 1)
# Золотое кольцо на ободке
cv2.rectangle(canvas, (fl_cx - 16, fl_cy - 8), (fl_cx + 16, fl_cy - 3), (40, 160, 220), -1)
# Безель и линза
cv2.rectangle(canvas, (fl_cx - 18, fl_cy - 3), (fl_cx + 18, fl_cy + 4), (70, 75, 85), -1)

# 5. Ослепительно яркий источник света из линзы фонарика
cv2.circle(canvas, (fl_cx, fl_cy + 3), 16, (200, 245, 255), -1)
cv2.circle(canvas, (fl_cx, fl_cy + 3), 8, (255, 255, 255), -1)

# Свечение линзы
glow_lens = np.zeros((canvas_h, canvas_w, 3), dtype=np.float32)
cv2.circle(glow_lens, (fl_cx, fl_cy + 3), 90, (80, 180, 255), -1)
cv2.circle(glow_lens, (fl_cx, fl_cy + 3), 45, (160, 220, 255), -1)
glow_lens = cv2.GaussianBlur(glow_lens, (91, 91), 0)
canvas = np.clip(canvas.astype(np.float32) + glow_lens, 0, 255).astype(np.uint8)

# 6. Объемный кинематографичный конус света (Volumetric Light Cone) от фонарика вниз на стол!
beam_layer = np.zeros((canvas_h, canvas_w, 3), dtype=np.float32)
start_y = fl_cy + 4
end_y = canvas_h

for y in range(start_y, end_y):
    t = (y - start_y) / float(end_y - start_y)
    # Конус расширяется от 18px до 420px
    half_width = 18 + t * 400
    
    # Центр луча
    cx = fl_cx
    x0 = int(cx - half_width)
    x1 = int(cx + half_width)
    
    if x1 > x0:
        # Профиль интенсивности по горизонтали
        xs = np.arange(max(0, x0), min(canvas_w, x1))
        dists = np.abs(xs - cx) / half_width
        # Профиль Гаусса
        intensity = np.exp(-2.2 * (dists ** 2)) * (0.65 - t * 0.22)
        
        # Теплый золотистый цвет (BGR: 120, 205, 255)
        for i, x in enumerate(xs):
            b_val = intensity[i]
            beam_layer[y, x, 0] += 110 * b_val # B
            beam_layer[y, x, 1] += 195 * b_val # G
            beam_layer[y, x, 2] += 255 * b_val # R

# Размываем световой луч для бархатистости
beam_layer = cv2.GaussianBlur(beam_layer, (35, 35), 0)

# Вторичное освещение на столе и сложенных руках (в нижней части y > 950)
table_bounce = np.zeros((canvas_h, canvas_w, 3), dtype=np.float32)
cv2.ellipse(table_bounce, (500, 1180), (320, 160), 0, 0, 360, (90, 180, 245), -1)
table_bounce = cv2.GaussianBlur(table_bounce, (121, 121), 0)

# Смешиваем свет с полотном
final_art = canvas.astype(np.float32) + beam_layer * 0.95 + table_bounce * 0.55

# 7. Добавляем летающие золотые пылинки в луче света
np.random.seed(42)
num_particles = 220
for _ in range(num_particles):
    py = np.random.randint(fl_cy + 20, canvas_h - 100)
    t = (py - fl_cy) / float(canvas_h - fl_cy)
    hw = 18 + t * 380
    px = int(fl_cx + np.random.normal(0, hw * 0.45))
    if 0 <= px < canvas_w:
        p_size = np.random.choice([1, 2, 3], p=[0.7, 0.25, 0.05])
        p_brightness = np.random.uniform(150, 255)
        color = (int(p_brightness * 0.7), int(p_brightness * 0.9), int(p_brightness))
        cv2.circle(final_art, (px, py), p_size, color, -1)

final_art = np.clip(final_art, 0, 255).astype(np.uint8)

# 8. Верхний градиент под типографику заголовка
top_gradient = np.zeros((canvas_h, canvas_w, 3), dtype=np.float32)
for y in range(0, 380):
    factor = 1.0 - (y / 380.0)
    final_art[y, :] = np.clip(final_art[y, :].astype(np.float32) * (1.0 - factor * 0.85), 0, 255).astype(np.uint8)

out_path = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\faceless_flashlight_v3.jpg"
cv2.imwrite(out_path, final_art)
print("Saved faceless_flashlight_v3.jpg successfully!")
