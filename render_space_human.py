import os
from playwright.sync_api import sync_playwright

base_img_path = r"C:\Users\vanya\.gemini\antigravity\brain\3ebdfd13-c38d-47bb-b8a5-4e69c7e0d70c\human_circuit_flashlight_1791440045463.jpg"
base_img_url = "file:///" + base_img_path.replace("\\", "/")

html_content = f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>Человек-Фонарик в Космосе: Пентада ТХГДМ</title>
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
      opacity: 0.92;
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
    <!-- Живописный рисунок человека на фоне космоса и созвездий -->
    <img src="{base_img_url}" class="bg-art" alt="Человек в космосе" />

    <!-- Мягкое виньетирование для идеальной читаемости инженерного контура -->
    <div style="position: absolute; inset: 0; background: radial-gradient(ellipse at center 48%, rgba(2,6,23,0) 38%, rgba(2,6,23,0.75) 70%, rgba(2,6,23,0.98) 98%); pointer-events: none;"></div>

    <!-- Векторный схемотехнический оверлей (ортогональный контур 90°) -->
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

      <!-- ВЕРХНИЙ КОЛОНТИТУЛ ЧЕРТЕЖА -->
      <g transform="translate(60, 45)">
        <rect x="0" y="0" width="220" height="30" rx="6" fill="#1e1b4b" stroke="#4338ca" stroke-width="1.2"/>
        <text x="110" y="20" fill="#a5b4fc" font-size="11" font-weight="700" font-family="monospace" text-anchor="middle" letter-spacing="2">СИСТЕМА АНЬЯНОВА</text>
        
        <text x="240" y="23" fill="#ffffff" font-size="24" font-weight="900" letter-spacing="1">ПЕНТАДА Т-Х-Г-Д-М : ЧЕЛОВЕК-ФОНАРИК</text>
        <text x="240" y="46" fill="#94a3b8" font-size="13" font-family="monospace">ЕДИНАЯ ЗАМКНУТАЯ ЦЕПЬ: ИСТОЧНИК В ЖИВОТЕ, ДЕЛО В РУКАХ И ГОЛОВЕ</text>
      </g>

      <!-- ======================================================== -->
      <!-- ЕДИНАЯ ЗАМКНУТАЯ ЦЕПЬ ПОД ПРЯМЫМИ УГЛАМИ 90°             -->
      <!-- Центр фигуры: X = 600                                    -->
      <!-- Высота лампы (ГЁ / ДЕЛО): Y = 494                        -->
      <!-- Высота Тандэна: Y = 874                                  -->
      <!-- Левая шина (ХОЦУ): X = 230                               -->
      <!-- Правая шина (ДЗАНСИН): X = 970                           -->
      <!-- ======================================================== -->

      <!-- Канал экранирующего шинопровода -->
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
      <!-- Вспышка искры «ХОЧУ!» -->
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
      <!-- Ток входит слева в x=545, проходит спираль и             -->
      <!-- выходит справа в x=655 дальше по цепи!                   -->
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
        <circle cx="0" cy="0" r="68" fill="#ef4444" fill-opacity="0.3" filter="url(#glowRed)"/>
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
      <!-- РУССКАЯ НОМЕНКЛАТУРА И ПОЯСНЯЮЩИЕ БЛОКИ                  -->
      <!-- ======================================================== -->

      <!-- БЛОК «ГЁ (行) / ДЕЛО» НАД ЛАМПОЙ (ТОЧНО ПО ЗАПРОСУ ПОЛЬЗОВАТЕЛЯ!) -->
      <g transform="translate(600, 362)" text-anchor="middle">
        <rect x="-140" y="0" width="280" height="72" rx="10" fill="#0b1329" stroke="#f59e0b" stroke-width="2.5" opacity="0.96"/>
        <text x="0" y="28" font-size="22" font-weight="900" fill="#ffffff" letter-spacing="1">Гё (行)</text>
        <text x="0" y="54" font-size="16" font-weight="800" fill="#facc15" letter-spacing="2">ДЕЛО</text>
      </g>

      <!-- БЛОК «ТАНДЭН» ПОД РЕАКТОРОМ В ЖИВОТЕ -->
      <g transform="translate(600, 980)" text-anchor="middle">
        <rect x="-150" y="0" width="300" height="68" rx="10" fill="#0b1329" stroke="#ef4444" stroke-width="2.5" opacity="0.96"/>
        <text x="0" y="27" font-size="20" font-weight="900" fill="#ffffff" letter-spacing="1">ТАНДЭН (丹田)</text>
        <text x="0" y="47" font-size="12" font-weight="700" fill="#ef4444">ИСТОЧНИК ЭДС / ГЕНЕРАТОР</text>
      </g>

      <!-- БЛОК «ХОЦУ» СЛЕВА -->
      <g transform="translate(210, 685)" text-anchor="end">
        <rect x="-185" y="-34" width="180" height="68" rx="10" fill="#0b1329" stroke="#38bdf8" stroke-width="2.5" opacity="0.96"/>
        <text x="-15" y="-8" font-size="18" font-weight="900" fill="#ffffff" letter-spacing="1">ХОЦУ (発)</text>
        <text x="-15" y="14" font-size="12" font-weight="700" fill="#38bdf8">ВЫКЛЮЧАТЕЛЬ</text>
      </g>

      <!-- БЛОК «ДЗАНСИН» СПРАВА -->
      <g transform="translate(990, 685)" text-anchor="start">
        <rect x="5" y="-34" width="185" height="68" rx="10" fill="#0b1329" stroke="#f59e0b" stroke-width="2.5" opacity="0.96"/>
        <text x="20" y="-8" font-size="18" font-weight="900" fill="#ffffff" letter-spacing="1">ДЗАНСИН (残心)</text>
        <text x="20" y="14" font-size="12" font-weight="700" fill="#f59e0b">ПРЕДОХРАНИТЕЛЬ</text>
      </g>

      <!-- МАРКИРОВКА МУСИН НА ШИНАХ -->
      <g transform="translate(385, 470)" text-anchor="middle">
        <rect x="-110" y="-14" width="220" height="20" rx="4" fill="#020617" stroke="#38bdf8" stroke-width="1"/>
        <text x="0" y="0" font-family="monospace" font-size="10" font-weight="700" fill="#38bdf8">МУСИН: ШИНА ВНИМАНИЯ (R → 0)</text>
      </g>
      <g transform="translate(815, 470)" text-anchor="middle">
        <rect x="-110" y="-14" width="220" height="20" rx="4" fill="#020617" stroke="#fbbf24" stroke-width="1"/>
        <text x="0" y="0" font-family="monospace" font-size="10" font-weight="700" fill="#fbbf24">МУСИН: ОБРАТНАЯ ШИНА (無心)</text>
      </g>

      <!-- НИЖНЯЯ ПЛАШКА В ПОДВАЛЕ -->
      <g transform="translate(60, 1375)">
        <rect x="0" y="0" width="1080" height="42" rx="8" fill="#0b1329" stroke="#1e293b" stroke-width="1.5" opacity="0.96"/>
        <text x="20" y="26" font-size="13" font-weight="800" fill="#38bdf8" font-family="monospace">ЕДИНАЯ НЕРАЗРЫВНАЯ ЦЕПЬ:</text>
        <text x="245" y="26" font-size="13" font-weight="600" fill="#f8fafc">
          Тандэн (живот) ➔ Хоцу (хочу) ➔ Гё / ДЕЛО (лампа в руках и голове) ➔ Дзансин (защита) ➔ Мусин (ток без трения)
        </text>
        <text x="1060" y="26" font-size="11" font-family="monospace" fill="#64748b" text-anchor="end">I > 0 | R_ego = 0</text>
      </g>

    </svg>
  </div>
</body>
</html>
"""

with open("temp_space_human.html", "w", encoding="utf-8") as f:
    f.write(html_content)

output_path = r"C:\Users\vanya\.gemini\antigravity\brain\3ebdfd13-c38d-47bb-b8a5-4e69c7e0d70c\thgdm_human_cosmos_circuit.png"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1200, "height": 1450}, device_scale_factor=2)
    page.goto("file:///" + os.path.abspath("temp_space_human.html").replace("\\", "/"))
    page.wait_for_timeout(400)
    page.screenshot(path=output_path)
    browser.close()

print("UPDATED_COSMOS_IMAGE_CREATED:", os.path.exists(output_path))
