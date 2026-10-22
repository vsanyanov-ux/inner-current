import cv2
import numpy as np

# 1. Загружаем уютный интерьер антикафе
# Используем качественный фон антикафе с кирпичом и лампочками
cafe_bg = cv2.imread(r"C:\Users\vanya\.gemini\antigravity\brain\595d7ab7-6eb8-4a63-a314-66f392e88f80\clean_cafe_flashlight_1791829450612.jpg")
# Убираем фонарик с переднего плана этого фона с помощью размытия/кропа стола
# Размер фона: 1200 x 896
bg_h, bg_w = cafe_bg.shape[:2]

# Целевой размер А4 постера: 1414 x 1000
canvas_h, canvas_w = 1414, 1000
bg_resized = cv2.resize(cafe_bg, (canvas_w, canvas_h))

# Затемняем фон, чтобы создать кинематографичную ночную атмосферу
bg_dark = (bg_resized.astype(np.float32) * 0.45).astype(np.uint8)

# Добавляем уютное теплое вечернее виньетирование
vignette = np.zeros((canvas_h, canvas_w), dtype=np.float32)
cv2.ellipse(vignette, (canvas_w // 2, canvas_h // 2), (canvas_w // 2 + 100, canvas_h // 2 + 100), 0, 0, 360, 1.0, -1)
vignette = cv2.GaussianBlur(vignette, (151, 151), 0)
vignette_3ch = np.dstack([vignette]*3)
bg_dark = np.clip(bg_dark.astype(np.float32) * (0.4 + 0.6 * vignette_3ch), 0, 255).astype(np.uint8)

# 2. Создаем деревянный стол на переднем плане (Y: 960..1414)
# Берем красивую деревянную текстуру стола
table_y = 960
for y in range(table_y, canvas_h):
    t = (y - table_y) / float(canvas_h - table_y)
    # Теплый деревянный тон стола
    wood_tone = np.array([25, 45, 65], dtype=np.float32) * (1.2 - t * 0.3)
    bg_dark[y, :] = np.clip(bg_dark[y, :].astype(np.float32) * 0.5 + wood_tone, 0, 255).astype(np.uint8)

# 3. Вырезаем чистый силуэт человека, сидящего за столом (из фото спикера)
speaker_img = cv2.imread(r"C:\Users\vanya\.gemini\antigravity\brain\595d7ab7-6eb8-4a63-a314-66f392e88f80\.user_uploaded\media_1791828744136_3f4d95f3.jpg")
sh, sw = speaker_img.shape[:2]

# Подгоняем размер спикера под масштаб постера
target_sw = 800
target_sh = int(sh * (target_sw / sw))
sp_resized = cv2.resize(speaker_img, (target_sw, target_sh))

# Преобразуем человека в глубокий силуэт (контражур), где лица не видно
# Создаем маску тела человека: голова, плечи, сложенные на столе руки
gray_sp = cv2.cvtColor(sp_resized, cv2.COLOR_BGR2GRAY)
# Маска человека
person_mask = np.zeros((target_sh, target_sw), dtype=np.uint8)
# Голова: эллипс
cv2.ellipse(person_mask, (400, 340), (120, 160), 0, 0, 360, 255, -1)
# Плечи и торс
pts_torso = np.array([[120, target_sh], [220, 480], [400, 450], [580, 480], [680, target_sh]], dtype=np.int32)
cv2.fillPoly(person_mask, [pts_torso], 255)
# Сложенные на столе руки
cv2.ellipse(person_mask, (400, 850), (220, 130), 0, 0, 360, 255, -1)

# Сглаживаем маску
person_mask = cv2.GaussianBlur(person_mask, (31, 31), 0)
person_mask_f = person_mask.astype(np.float32) / 255.0
person_mask_3ch = np.dstack([person_mask_f]*3)

# Позиционируем человека по центру холста
pos_x = (canvas_w - target_sw) // 2
pos_y = canvas_h - target_sh + 40

# Вставляем человека как темный силуэт (noir silhouette)
# Тело темное (BGR: 14, 16, 20), лица не видно
silhouette_color = np.zeros_like(sp_resized, dtype=np.float32)
silhouette_color[:] = [14, 16, 20]

# Добавляем легкий контурный свет (rim light) по краям силуэта
edges = cv2.Canny(person_mask, 50, 150)
edges_blur = cv2.GaussianBlur(edges, (15, 15), 0).astype(np.float32) / 255.0
edges_3ch = np.dstack([edges_blur]*3)
rim_light = edges_3ch * np.array([90, 175, 245], dtype=np.float32) # теплый золотой ободок

silhouette_final = silhouette_color + rim_light
silhouette_final = np.clip(silhouette_final, 0, 255).astype(np.uint8)

# Обрезаем человека по границе холста снизу
actual_h = min(target_sh, canvas_h - pos_y)
person_mask_3ch = person_mask_3ch[:actual_h]
silhouette_final = silhouette_final[:actual_h]

# Накладываем силуэт на фон
bg_roi = bg_dark[pos_y:pos_y+actual_h, pos_x:pos_x+target_sw].astype(np.float32)
blended_roi = bg_roi * (1.0 - person_mask_3ch) + silhouette_final.astype(np.float32) * person_mask_3ch
bg_dark[pos_y:pos_y+actual_h, pos_x:pos_x+target_sw] = np.clip(blended_roi, 0, 255).astype(np.uint8)

# 4. РИСУЕМ ФОНАРИК НАД ГОЛОВОЙ (чистый векторный рендер высокого разрешения)
# Центр фонарика над головой человека:
fl_x = canvas_w // 2 # 500
fl_y = pos_y + 190   # прямо над головой

# Металлический корпус фонарика
# Цилиндр фонарика (черно-титановый с золотым кольцом)
cv2.rectangle(bg_dark, (fl_x - 16, fl_y - 65), (fl_x + 16, fl_y - 12), (30, 32, 38), -1)
# Ребра охлаждения/насечки
for ry in range(fl_y - 58, fl_y - 16, 6):
    cv2.line(bg_dark, (fl_x - 16, ry), (fl_x + 16, ry), (18, 19, 22), 2)
# Золотое кольцо
cv2.rectangle(bg_dark, (fl_x - 18, fl_y - 12), (fl_x + 18, fl_y - 5), (45, 175, 235), -1)
# Безель и линза
cv2.rectangle(bg_dark, (fl_x - 20, fl_y - 5), (fl_x + 20, fl_y + 4), (60, 65, 75), -1)
# Линза (ярко-белое ядро)
cv2.circle(bg_dark, (fl_x, fl_y + 4), 16, (220, 245, 255), -1)
cv2.circle(bg_dark, (fl_x, fl_y + 4), 8, (255, 255, 255), -1)

# 5. КИНЕМАТОГРАФИЧНЫЙ КОНУС СВЕТА ВНИЗ НА СТОЛ
beam = np.zeros((canvas_h, canvas_w, 3), dtype=np.float32)
for y in range(fl_y + 5, canvas_h):
    t = (y - (fl_y + 5)) / float(canvas_h - fl_y)
    half_w = 20 + t * 440
    xs = np.arange(max(0, int(fl_x - half_w)), min(canvas_w, int(fl_x + half_w)))
    if len(xs) > 0:
        dists = np.abs(xs - fl_x) / half_w
        intensity = np.exp(-2.5 * (dists ** 2)) * (0.75 - t * 0.28)
        for i, x in enumerate(xs):
            b_val = intensity[i]
            beam[y, x, 0] += 110 * b_val # Blue
            beam[y, x, 1] += 195 * b_val # Green
            beam[y, x, 2] += 255 * b_val # Red

beam = cv2.GaussianBlur(beam, (41, 41), 0)

# Яркое световое пятно на столе
table_spot = np.zeros((canvas_h, canvas_w, 3), dtype=np.float32)
cv2.ellipse(table_spot, (fl_x, 1180), (360, 180), 0, 0, 360, (110, 195, 255), -1)
table_spot = cv2.GaussianBlur(table_spot, (121, 121), 0)

# Смешиваем свет с постером
bg_with_light = bg_dark.astype(np.float32) + beam * 0.95 + table_spot * 0.65

# 6. Золотые частицы в луче
np.random.seed(108)
for _ in range(180):
    py = np.random.randint(fl_y + 30, canvas_h - 120)
    t = (py - fl_y) / float(canvas_h - fl_y)
    hw = 20 + t * 400
    px = int(fl_x + np.random.normal(0, hw * 0.42))
    if 0 <= px < canvas_w:
        size = np.random.choice([1, 2, 3], p=[0.75, 0.2, 0.05])
        bright = np.random.uniform(160, 255)
        color = (int(bright * 0.65), int(bright * 0.88), int(bright))
        cv2.circle(bg_with_light, (px, py), size, color, -1)

# 7. Затемнение верха под крупную чистую типографику
top_shade = np.zeros((canvas_h, canvas_w, 3), dtype=np.float32)
for y in range(0, 420):
    factor = 1.0 - (y / 420.0)
    bg_with_light[y, :] = bg_with_light[y, :] * (1.0 - factor * 0.88)

poster_clean = np.clip(bg_with_light, 0, 255).astype(np.uint8)

# Сохраняем чистый фон
out_poster = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\clean_faceless_scene.jpg"
cv2.imwrite(out_poster, poster_clean)
print("Saved clean_faceless_scene.jpg successfully!")
