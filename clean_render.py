import os
from playwright.sync_api import sync_playwright

base_img_path = r"C:\Users\vanya\.gemini\antigravity\brain\3ebdfd13-c38d-47bb-b8a5-4e69c7e0d70c\human_circuit_flashlight_1791440045463.jpg"
base_img_url = "file:///" + base_img_path.replace("\\", "/")

html_content = f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>Пентада ТХГДМ: Человек-Фонарик</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      background-color: #030712;
      width: 1200px;
      height: 1450px;
      display: flex;
      justify-content: center;
      align-items: center;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      overflow: hidden;
    }}
    .stage {{
      position: relative;
      width: 1200px;
      height: 1450px;
      background: #020617;
    }}
    .bg-art {{
      position: absolute;
      top: 60px;
      left: 152px;
      width: 896px;
      height: 1200px;
      object-fit: cover;
      opacity: 0.94;
      filter: contrast(1.08) brightness(0.96);
    }}
    .svg-overlay {{
      position: absolute;
      top: 0;
      left: 0;
      width: 1200px;
      height: 1450px;
      z-index: 10;
    }}
  </style>
</head>
<body>
  <div class="stage">
    <!-- Исходный аутентичный рисунок человека во Вселенной -->
    <img src="{base_img_url}" class="bg-art" alt="Человек-Фонарик" />

    <!-- Благородное мягкое виньетирование для глубины космоса -->
    <div style="position: absolute; inset: 0; background: radial-gradient(ellipse at center 48%, rgba(2,6,23,0) 38%, rgba(2,6,23,0.72) 70%, rgba(2,6,23,0.98) 98%); pointer-events: none;"></div>

    <!-- Векторный оверлей: только схема и 5 главных плашек -->
    <svg class="svg-overlay" viewBox="0 0 1200 1450" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <!-- Стрелки направления тока -->
        <marker id="arrowCyan" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="#38bdf8"/>
        </marker>
        <marker id="arrowGold" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="#facc15"/>
        </marker>
        <marker id="arrowRed" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
          <path d="M 0 1 L 10 5 L 0 9 z" fill="#ef4444"/>
        </marker>

        <!-- Неоновое свечение элементов -->
        <filter id="glowCyan" x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur stdDeviation="3.5" result="blur" />
          <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>
        <filter id="glowGold" x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur stdDeviation="4.5" result="blur" />
          <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>
        <filter id="glowRed" x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur stdDeviation="5.5" result="blur" />
          <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>
      </defs>

      <!-- ======================================================== -->
      <!-- ЕДИНАЯ ЗАМКНУТАЯ ЦЕПЬ (90° ТОПОЛОГИЯ)                     -->
      <!-- Центр фигуры: X = 600                                    -->
      <!-- Высота лампы (ГЁ / ДЕЛО): Y = 494                        -->
      <!-- Высота Тандэна: Y = 874                                  -->
      <!-- Левая шина (ХОЦУ): X = 230                               -->
      <!-- Правая шина (ДЗАНСИН): X = 970                           -->
      <!-- ======================================================== -->

      <!-- Защитный экранирующий шинопровод -->
      <rect x="230" y="494" width="740" height="380" rx="4" fill="none" stroke="#020617" stroke-width="16" opacity="0.85"/>
      <rect x="230" y="494" width="740" height="380" rx="4" fill="none" stroke="#0f172a" stroke-width="8" opacity="0.95"/>

      <!-- 1. НИЖНЯЯ ВЕТВЬ (Y = 874): выход из Тандэна влево к ХОЦУ -->
      <line x1="550" y1="874" x2="230" y2="874" stroke="#ef4444" stroke-width="5" filter="url(#glowRed)"/>
      <line x1="430" y1="874" x2="370" y2="874" stroke="#ef4444" stroke-width="5" marker-end="url(#arrowRed)"/>

      <!-- Нижний левый угол 90° -->
      <circle cx="230" cy="874" r="8" fill="#ffffff" stroke="#ef4444" stroke-width="3"/>

      <!-- 2. ЛЕВАЯ ВЕРТИКАЛЬНАЯ ВЕТВЬ (X = 230): от нижнего угла к ХОЦУ -->
      <line x1="230" y1="874" x2="230" y2="730" stroke="#ef4444" stroke-width="5"/>
      <line x1="230" y1="820" x2="230" y2="760" stroke="#ef4444" stroke-width="5" marker-end="url(#arrowRed)"/>

      <!-- ВЫКЛЮЧАТЕЛЬ ХОЦУ (ВРЕЗАН В ЦЕПЬ ПОСЛЕДОВАТЕЛЬНО НА X = 230) -->
      <!-- Нижняя клемма ключа -->
      <circle cx="230" cy="730" r="7" fill="#38bdf8" stroke="#ffffff" stroke-width="2.5"/>
      <!-- Верхняя клемма ключа -->
      <circle cx="230" cy="640" r="7" fill="#38bdf8" stroke="#ffffff" stroke-width="2.5"/>
      <!-- Замкнутое массивное лезвие ключа -->
      <line x1="230" y1="730" x2="230" y2="640" stroke="#38bdf8" stroke-width="6.5" stroke-linecap="round" filter="url(#glowCyan)"/>
      <!-- Вспышка соматического контакта -->
      <circle cx="230" cy="640" r="16" fill="#38bdf8" fill-opacity="0.3"/>
      <circle cx="230" cy="640" r="6" fill="#ffffff"/>

      <!-- Левая шина от ХОЦУ вверх к верхнему левому углу -->
      <line x1="230" y1="640" x2="230" y2="494" stroke="#38bdf8" stroke-width="5" filter="url(#glowCyan)"/>
      <line x1="230" y1="580" x2="230" y2="530" stroke="#38bdf8" stroke-width="5" marker-end="url(#arrowCyan)"/>

      <!-- Верхний левый угол 90° -->
      <circle cx="230" cy="494" r="8" fill="#ffffff" stroke="#38bdf8" stroke-width="3"/>

      <!-- 3. ВЕРХНЯЯ ГОРИЗОНТАЛЬНАЯ ВЕТВЬ (Y = 494): ВХОД В ЛАМПУ СЛЕВА -->
      <line x1="230" y1="494" x2="545" y2="494" stroke="#38bdf8" stroke-width="5" filter="url(#glowCyan)"/>
      <line x1="360" y1="494" x2="420" y2="494" stroke="#38bdf8" stroke-width="5" marker-end="url(#arrowCyan)"/>

      <!-- ======================================================== -->
      <!-- ЛАМПА «ГЁ / ДЕЛО» (ВРЕЗАНА В ЦЕПЬ ПО ЦЕНТРУ Y = 494)     -->
      <!-- ======================================================== -->
      <!-- Левая клемма лампы -->
      <circle cx="545" cy="494" r="7" fill="#facc15" stroke="#ffffff" stroke-width="2.5"/>

      <!-- СВЕТЯЩАЯСЯ СПИРАЛЬ ВНУТРИ ЛАМПЫ (ЗАМЫКАЕТ ЦЕПЬ 545 -> 655) -->
      <path d="M 545 494 L 575 494 L 588 460 L 600 510 L 612 460 L 625 510 L 638 494 L 655 494" 
            stroke="#ffffff" stroke-width="4.5" fill="none" stroke-linecap="round" stroke-linejoin="round" filter="url(#glowGold)"/>

      <!-- Правая клемма лампы -->
      <circle cx="655" cy="494" r="7" fill="#facc15" stroke="#ffffff" stroke-width="2.5"/>

      <!-- 4. ВЕРХНЯЯ ГОРИЗОНТАЛЬНАЯ ВЕТВЬ (Y = 494): ВЫХОД ИЗ ЛАМПЫ ВПРАВО -->
      <line x1="655" y1="494" x2="970" y2="494" stroke="#fbbf24" stroke-width="5" filter="url(#glowGold)"/>
      <line x1="780" y1="494" x2="840" y2="494" stroke="#fbbf24" stroke-width="5" marker-end="url(#arrowGold)"/>

      <!-- Верхний правый угол 90° -->
      <circle cx="970" cy="494" r="8" fill="#ffffff" stroke="#fbbf24" stroke-width="3"/>

      <!-- 5. ПРАВАЯ ВЕРТИКАЛЬНАЯ ВЕТВЬ (X = 970): спуск к ДЗАНСИНУ -->
      <line x1="970" y1="494" x2="970" y2="640" stroke="#fbbf24" stroke-width="5" filter="url(#glowGold)"/>
      <line x1="970" y1="550" x2="970" y2="600" stroke="#fbbf24" stroke-width="5" marker-end="url(#arrowGold)"/>

      <!-- ПРЕДОХРАНИТЕЛЬ ДЗАНСИН (ВРЕЗАН В ЦЕПЬ ПОСЛЕДОВАТЕЛЬНО НА X = 970) -->
      <!-- Верхняя клемма -->
      <circle cx="970" cy="640" r="7" fill="#f59e0b" stroke="#ffffff" stroke-width="2.5"/>
      <!-- Корпус автомата отсечки -->
      <rect x="952" y="646" width="36" height="84" rx="8" fill="#0b1329" stroke="#f59e0b" stroke-width="3"/>
      <!-- Плавкая вставка -->
      <line x1="970" y1="654" x2="970" y2="722" stroke="#fef08a" stroke-width="4.5"/>
      <circle cx="970" cy="688" r="5" fill="#ef4444"/>
      <!-- Нижняя клемма -->
      <circle cx="970" cy="730" r="7" fill="#f59e0b" stroke="#ffffff" stroke-width="2.5"/>

      <!-- Правая шина от ДЗАНСИН вниз к нижнему правому углу -->
      <line x1="970" y1="730" x2="970" y2="874" stroke="#ef4444" stroke-width="5" filter="url(#glowRed)"/>
      <line x1="970" y1="790" x2="970" y2="840" stroke="#ef4444" stroke-width="5" marker-end="url(#arrowRed)"/>

      <!-- Нижний правый угол 90° -->
      <circle cx="970" cy="874" r="8" fill="#ffffff" stroke="#ef4444" stroke-width="3"/>

      <!-- 6. НИЖНЯЯ ВЕТВЬ (Y = 874): возврат справа в ТАНДЭН -->
      <line x1="970" y1="874" x2="650" y2="874" stroke="#ef4444" stroke-width="5" filter="url(#glowRed)"/>
      <line x1="830" y1="874" x2="770" y2="874" stroke="#ef4444" stroke-width="5" marker-end="url(#arrowRed)"/>

      <!-- РЕАКТОР ТАНДЭН (ВРЕЗАН В ЦЕПЬ В ЖИВОТЕ НА X = 600, Y = 874) -->
      <g transform="translate(600, 874)">
        <circle cx="0" cy="0" r="68" fill="#ef4444" fill-opacity="0.35" filter="url(#glowRed)"/>
        <!-- Корпус реактора -->
        <rect x="-48" y="-48" width="96" height="96" rx="20" fill="#090d16" stroke="#ef4444" stroke-width="4.5"/>
        <circle cx="0" cy="0" r="30" fill="#7f1d1d" stroke="#f87171" stroke-width="2"/>
        <circle cx="0" cy="0" r="18" fill="#ef4444"/>
        <circle cx="0" cy="0" r="9" fill="#ffffff"/>
        <!-- Клеммы генератора -->
        <circle cx="-48" cy="0" r="7" fill="#f87171" stroke="#ffffff" stroke-width="2.5"/>
        <circle cx="48" cy="0" r="7" fill="#f87171" stroke="#ffffff" stroke-width="2.5"/>
        <text x="0" y="5" font-family="monospace" font-size="14" font-weight="900" fill="#ffffff" text-anchor="middle">⚡ E</text>
      </g>


      <!-- ======================================================== -->
      <!-- 5 КАНОНИЧЕСКИХ ПЛАШЕК (ЧИСТАЯ ЭСТЕТИКА, БЕЗ ЛИШНЕГО)      -->
      <!-- ======================================================== -->

      <!-- 1. ПЛАШКА «МУСИН» (ВВЕРХУ ПО ЦЕНТРУ НАД ВСЕЙ СХЕМОЙ) -->
      <g transform="translate(600, 100)" text-anchor="middle">
        <!-- Тонкие эстетичные соединительные трассы от плашки к углам цепи -->
        <path d="M -130 0 L -370 0 L -370 394" fill="none" stroke="#38bdf8" stroke-width="1.2" stroke-dasharray="4,4" opacity="0.4"/>
        <path d="M 130 0 L 370 0 L 370 394" fill="none" stroke="#38bdf8" stroke-width="1.2" stroke-dasharray="4,4" opacity="0.4"/>
        <rect x="-135" y="-30" width="270" height="60" rx="14" fill="#070e20" stroke="#38bdf8" stroke-width="2.5" opacity="0.96"/>
        <text x="0" y="9" font-size="22" font-weight="900" fill="#ffffff" letter-spacing="1">Мусин (無心)</text>
      </g>

      <!-- 2. ПЛАШКА «ГЁ / ДЕЛО» (НАД ЛАМПОЙ В РУКАХ) -->
      <g transform="translate(600, 365)" text-anchor="middle">
        <rect x="-135" y="-35" width="270" height="70" rx="14" fill="#070e20" stroke="#f59e0b" stroke-width="2.5" opacity="0.96"/>
        <text x="0" y="-7" font-size="22" font-weight="900" fill="#ffffff" letter-spacing="1">Гё (行)</text>
        <text x="0" y="20" font-size="16" font-weight="800" fill="#facc15" letter-spacing="2">ДЕЛО</text>
      </g>

      <!-- 3. ПЛАШКА «ТАНДЭН» (ПОД РЕАКТОРОМ В ЖИВОТЕ) -->
      <g transform="translate(600, 985)" text-anchor="middle">
        <rect x="-140" y="-30" width="280" height="60" rx="14" fill="#070e20" stroke="#ef4444" stroke-width="2.5" opacity="0.96"/>
        <text x="0" y="9" font-size="22" font-weight="900" fill="#ffffff" letter-spacing="1">Тандэн (丹田)</text>
      </g>

      <!-- 4. ПЛАШКА «ХОЦУ» (СЛЕВА У ВЫКЛЮЧАТЕЛЯ) -->
      <g transform="translate(200, 685)" text-anchor="end">
        <rect x="-170" y="-30" width="170" height="60" rx="14" fill="#070e20" stroke="#38bdf8" stroke-width="2.5" opacity="0.96"/>
        <text x="-15" y="9" font-size="21" font-weight="900" fill="#ffffff" letter-spacing="1">Хоцу (発)</text>
      </g>

      <!-- 5. ПЛАШКА «ДЗАНСИН» (СПРАВА У ПРЕДОХРАНИТЕЛЯ) -->
      <g transform="translate(1000, 685)" text-anchor="start">
        <rect x="0" y="-30" width="180" height="60" rx="14" fill="#070e20" stroke="#f59e0b" stroke-width="2.5" opacity="0.96"/>
        <text x="18" y="9" font-size="21" font-weight="900" fill="#ffffff" letter-spacing="1">Дзансин (残心)</text>
      </g>

    </svg>
  </div>
</body>
</html>
"""

temp_html = "temp_clean_render.html"
with open(temp_html, "w", encoding="utf-8") as f:
    f.write(html_content)

output_path = r"C:\Users\vanya\.gemini\antigravity\brain\3ebdfd13-c38d-47bb-b8a5-4e69c7e0d70c\thgdm_human_cosmos_circuit.png"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1200, "height": 1450}, device_scale_factor=2)
    page.goto("file:///" + os.path.abspath(temp_html).replace("\\", "/"))
    page.wait_for_timeout(400)
    page.screenshot(path=output_path)
    browser.close()

print("FINAL_IMAGE_RENDERED:", os.path.exists(output_path))
