import cv2
import numpy as np
from PIL import Image

# Загружаем изображение
img_path = r"C:\Users\vanya\.gemini\antigravity\brain\595d7ab7-6eb8-4a63-a314-66f392e88f80\afisha_fonarik_ru_1791828964068.jpg"
img = cv2.imread(img_path)
h, w = img.shape[:2]

# Создаем маску для удаления фонарика в руках
# Фонарик и рука находятся в диапазоне x: 375..525, y: 810..995
mask = np.zeros((h, w), dtype=np.uint8)

# Полигон/прямоугольник для руки и нижнего фонарика
pts = np.array([
    [400, 810],
    [496, 810],
    [525, 870],
    [520, 930],
    [500, 995],
    [395, 995],
    [375, 930],
    [375, 870]
], dtype=np.int32)

cv2.fillPoly(mask, [pts], 255)
# Небольшое размытие/дилатация маски для плавного перехода
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
mask = cv2.dilate(mask, kernel, iterations=2)

# Применяем Telea inpainting
inpainted = cv2.inpaint(img, mask, inpaintRadius=11, flags=cv2.INPAINT_TELEA)

# Дополнительно: продлим естественный теплый световой луч на стол и восстановим деревянную текстуру
# Верхняя граница стола проходит примерно на y=920
# Заполним деревянный стол текстурой слева/справа от стола
table_y = 920

# Сохраняем результат
out_path = r"C:\Users\vanya\.gemini\antigravity\brain\595d7ab7-6eb8-4a63-a314-66f392e88f80\afisha_fonarik_no_hands.jpg"
cv2.imwrite(out_path, inpainted)
print("Inpaint complete:", out_path)
