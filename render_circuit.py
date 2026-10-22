import os
from playwright.sync_api import sync_playwright

html_content = """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>Схема Пентады ТХГДМ — Человек-Фонарик</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      background-color: #060913;
      width: 1100px;
      height: 1450px;
      display: flex;
      justify-content: center;
      align-items: center;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }
  </style>
</head>
<body>
  <svg viewBox="0 0 1100 1450" width="1100" height="1450" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <!-- Сетка чертежа -->
      <pattern id="grid" width="36" height="36" patternUnits="userSpaceOnUse">
        <path d="M 36 0 L 0 0 0 36" fill="none" stroke="#13233a" stroke-width="0.8"/>
      </pattern>

      <!-- Свечение Тандэна -->
      <radialGradient id="tandenGlow" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="#ff3b30" stop-opacity="1"/>
        <stop offset="35%" stop-color="#ef4444" stop-opacity="0.85"/>
        <stop offset="70%" stop-color="#991b1b" stop-opacity="0.35"/>
        <stop offset="100%" stop-color="#7f1d1d" stop-opacity="0"/>
      </radialGradient>

      <!-- Свечение Лампы Гё -->
      <radialGradient id="bulbAura" cx="50%" cy="50%" r="50%">
        <stop offset="0%" stop-color="#ffffff" stop-opacity="1"/>
        <stop offset="22%" stop-color="#fef08a" stop-opacity="0.95"/>
        <stop offset="50%" stop-color="#f59e0b" stop-opacity="0.65"/>
        <stop offset="80%" stop-color="#d97706" stop-opacity="0.2"/>
        <stop offset="100%" stop-color="#b45309" stop-opacity="0"/>
      </radialGradient>

      <!-- Заливка тела человека -->
      <linearGradient id="bodyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="#1e293b" stop-opacity="0.6"/>
        <stop offset="50%" stop-color="#0f172a" stop-opacity="0.7"/>
        <stop offset="100%" stop-color="#090d16" stop-opacity="0.8"/>
      </linearGradient>

      <!-- Стрелка направления тока (голубая) -->
      <marker id="arrowCyan" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#38bdf8"/>
      </marker>
      <!-- Стрелка направления тока (золотая) -->
      <marker id="arrowGold" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#fbbf24"/>
      </marker>
      <!-- Стрелка направления тока (алая) -->
      <marker id="arrowRed" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
        <path d="M 0 1 L 10 5 L 0 9 z" fill="#ef4444"/>
      </marker>
    </defs>

    <!-- Фон: тёмный сланцевый блюпринт -->
    <rect width="1100" height="1450" fill="#070b14"/>
    <rect width="1100" height="1450" fill="url(#grid)"/>

    <!-- Рамка чертежа -->
    <rect x="25" y="25" width="1050" height="1400" rx="16" fill="none" stroke="#1e293b" stroke-width="2"/>
    <rect x="35" y="35" width="1030" height="1380" rx="12" fill="none" stroke="#0f172a" stroke-width="1"/>

    <!-- ВЕРХНИЙ ЗАГОЛОВОК -->
    <g transform="translate(60, 75)">
      <rect x="0" y="0" width="230" height="32" rx="6" fill="#1e1b4b" stroke="#4338ca" stroke-width="1.2"/>
      <text x="115" y="21" fill="#a5b4fc" font-size="12" font-weight="700" font-family="monospace" text-anchor="middle" letter-spacing="2">СИСТЕМА АНЬЯНОВА</text>
      
      <text x="250" y="23" fill="#ffffff" font-size="25" font-weight="900" letter-spacing="1">ПЕНТАДА Т-Х-Г-Д-М : ЧЕЛОВЕК-ФОНАРИК</text>
      <text x="250" y="47" fill="#64748b" font-size="13" font-family="monospace">ЕДИНАЯ ЗАМКНУТАЯ ЦЕПЬ: ИСТОЧНИК В ЖИВОТЕ, ДЕЛО В РУКАХ И ГОЛОВЕ</text>
    </g>

    <!-- ======================================================== -->
    <!-- 1. ВЫРАЗИТЕЛЬНЫЙ АНАТОМИЧЕСКИЙ СИЛУЭТ ЧЕЛОВЕКА          -->
    <!-- ======================================================== -->
    <g id="humanBody" stroke="#475569" stroke-width="2" fill="url(#bodyGrad)">
      <!-- Голова -->
      <path d="M 505 240 C 505 170 595 170 595 240 C 595 295 565 330 550 335 C 535 330 505 295 505 240 Z" />
      <!-- Черты лица / медитативный покой -->
      <path d="M 532 235 Q 540 238 548 235" stroke="#64748b" stroke-width="1.5" fill="none"/>
      <path d="M 552 235 Q 560 238 568 235" stroke="#64748b" stroke-width="1.5" fill="none"/>
      <path d="M 547 245 L 550 258 L 553 258" stroke="#64748b" stroke-width="1.2" fill="none"/>
      <path d="M 543 270 Q 550 274 557 270" stroke="#64748b" stroke-width="1.5" fill="none"/>

      <!-- Шея и ключицы -->
      <path d="M 535 330 L 530 365 L 430 405" fill="none"/>
      <path d="M 565 330 L 570 365 L 670 405" fill="none"/>
      <path d="M 500 380 Q 550 395 600 380" stroke="#334155" stroke-width="1.5" fill="none"/>

      <!-- Плечи и руки (поднимаются и бережно держат лампу в руках!) -->
      <!-- Левая рука (с точки зрения рисунка: слева) -->
      <path d="M 430 405 C 380 435 350 490 350 560 C 350 630 380 610 435 550 L 485 510"/>
      <!-- Правая рука (справа) -->
      <path d="M 670 405 C 720 435 750 490 750 560 C 750 630 720 610 665 550 L 615 510"/>

      <!-- Кисти рук, бережно удерживающие цоколь и основание лампы -->
      <path d="M 480 505 C 490 485 520 490 528 520 C 510 535 485 525 480 505 Z" fill="#334155" stroke="#64748b"/>
      <path d="M 620 505 C 610 485 580 490 572 520 C 590 535 615 525 620 505 Z" fill="#334155" stroke="#64748b"/>

      <!-- Торс и мышечный рельеф -->
      <path d="M 430 405 C 445 530 455 690 445 930 C 445 960 480 990 550 990 C 620 990 655 960 655 930 C 645 690 655 530 670 405 Z"/>
      <!-- Грудная клетка -->
      <path d="M 470 450 Q 550 485 630 450" stroke="#334155" stroke-width="1.5" fill="none"/>
      <!-- Линия живота и пупок -->
      <circle cx="550" cy="850" r="3" fill="#475569"/>

      <!-- Таз и устойчивые ноги (чистые, без единого провода!) -->
      <path d="M 445 960 C 455 1060 465 1190 475 1320" stroke="#334155" stroke-width="2" stroke-dasharray="4,4" fill="none"/>
      <path d="M 655 960 C 645 1060 635 1190 625 1320" stroke="#334155" stroke-width="2" stroke-dasharray="4,4" fill="none"/>
      <path d="M 550 1010 L 550 1320" stroke="#334155" stroke-width="1.5" stroke-dasharray="3,3" fill="none"/>

      <!-- Заземление стоп на горизонт реальности -->
      <line x1="430" y1="1330" x2="670" y2="1330" stroke="#475569" stroke-width="2"/>
      <line x1="460" y1="1340" x2="640" y2="1340" stroke="#334155" stroke-width="2"/>
      <line x1="500" y1="1350" x2="600" y2="1350" stroke="#1e293b" stroke-width="2"/>
      <text x="550" y="1375" fill="#475569" font-size="11" font-family="monospace" text-anchor="middle">ЗАЗЕМЛЕНИЕ НА РЕАЛЬНОСТЬ (ОПОРА СТОП)</text>
    </g>

    <!-- ======================================================== -->
    <!-- 2. ЕДИНАЯ НЕРАЗРЫВНАЯ ЦЕПЬ (90° ТОПОЛОГИЯ)               -->
    <!-- Координаты:                                              -->
    <!-- Нижняя шина:  y = 930 (строго через Тандэн в животе)     -->
    <!-- Левая шина:   x = 190 (строго через выключатель ХОЦУ)    -->
    <!-- Верхняя шина: y = 470 (строго через ЛАМПУ ГЁ в руках!)   -->
    <!-- Правая шина:  x = 910 (строго через предохранитель)      -->
    <!-- ======================================================== -->

    <!-- Внешний защитный канал шинопровода -->
    <rect x="190" y="470" width="720" height="460" rx="4" fill="none" stroke="#0f172a" stroke-width="16"/>
    <rect x="190" y="470" width="720" height="460" rx="4" fill="none" stroke="#1e293b" stroke-width="8"/>

    <!-- 1. НИЖНЯЯ ВЕТВЬ ШИНЫ (y = 930): выход из Тандэна налево -->
    <line x1="502" y1="930" x2="190" y2="930" stroke="#ef4444" stroke-width="5"/>
    <line x1="390" y1="930" x2="330" y2="930" stroke="#ef4444" stroke-width="5" marker-end="url(#arrowRed)"/>

    <!-- Нижний левый угол 90° -->
    <circle cx="190" cy="930" r="8" fill="#ffffff" stroke="#ef4444" stroke-width="3"/>

    <!-- 2. ЛЕВАЯ ВЕРТИКАЛЬНАЯ ШИНА (x = 190): снизу до ХОЦУ -->
    <line x1="190" y1="930" x2="190" y2="740" stroke="#ef4444" stroke-width="5"/>
    <line x1="190" y1="860" x2="190" y2="800" stroke="#ef4444" stroke-width="5" marker-end="url(#arrowRed)"/>

    <!-- ВЫКЛЮЧАТЕЛЬ ХОЦУ (ВРЕЗАН В ЦЕПЬ ПОСЛЕДОВАТЕЛЬНО НА x=190) -->
    <!-- Нижняя клемма -->
    <circle cx="190" cy="740" r="7" fill="#38bdf8" stroke="#ffffff" stroke-width="2.5"/>
    <!-- Верхняя клемма -->
    <circle cx="190" cy="650" r="7" fill="#38bdf8" stroke="#ffffff" stroke-width="2.5"/>
    <!-- Замкнутое массивное лезвие ключа -->
    <line x1="190" y1="740" x2="190" y2="650" stroke="#38bdf8" stroke-width="6" stroke-linecap="round"/>
    <!-- Электрическая дуга / искра "ХОЧУ!" -->
    <circle cx="190" cy="650" r="16" fill="#38bdf8" fill-opacity="0.25"/>
    <circle cx="190" cy="650" r="6" fill="#ffffff"/>

    <!-- Левая шина от ХОЦУ вверх к верхнему левому углу -->
    <line x1="190" y1="650" x2="190" y2="470" stroke="#38bdf8" stroke-width="5"/>
    <line x1="190" y1="580" x2="190" y2="520" stroke="#38bdf8" stroke-width="5" marker-end="url(#arrowCyan)"/>

    <!-- Верхний левый угол 90° -->
    <circle cx="190" cy="470" r="8" fill="#ffffff" stroke="#38bdf8" stroke-width="3"/>

    <!-- 3. ВЕРХНЯЯ ГОРИЗОНТАЛЬНАЯ ШИНА (y = 470): ВХОД В ЛАМПУ СЛЕВА -->
    <line x1="190" y1="470" x2="480" y2="470" stroke="#38bdf8" stroke-width="5"/>
    <line x1="310" y1="470" x2="370" y2="470" stroke="#38bdf8" stroke-width="5" marker-end="url(#arrowCyan)"/>

    <!-- ======================================================== -->
    <!-- 3. ЛАМПА ГЁ (ФИЗИЧЕСКИ ВРЕЗАНА В ЦЕПЬ ПО ЦЕНТРУ Y = 470)  -->
    <!-- Левый контакт: x = 480. Ток заходит в лампу!            -->
    <!-- Нить накала светит!                                      -->
    <!-- Правый контакт: x = 620. Ток выходит из лампы!           -->
    <!-- ======================================================== -->
    <!-- Ореол яркого света -->
    <circle cx="550" cy="470" r="155" fill="url(#bulbAura)"/>

    <!-- Левая клемма лампы -->
    <circle cx="480" cy="470" r="7" fill="#facc15" stroke="#ffffff" stroke-width="2.5"/>

    <!-- Стеклянный баллон лампы -->
    <ellipse cx="550" cy="470" rx="58" ry="72" fill="#fef9c3" fill-opacity="0.9" stroke="#f59e0b" stroke-width="3.5"/>

    <!-- Вольфрамовая нить накаливания: ЗАМЫКАЕТ ЦЕПЬ МЕЖДУ 480 И 620! -->
    <path d="M 480 470 L 512 470 L 526 430 L 540 480 L 550 430 L 560 480 L 574 430 L 588 470 L 620 470" 
          stroke="#b45309" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>

    <!-- Правая клемма лампы -->
    <circle cx="620" cy="470" r="7" fill="#facc15" stroke="#ffffff" stroke-width="2.5"/>

    <!-- 4. ВЕРХНЯЯ ГОРИЗОНТАЛЬНАЯ ШИНА (y = 470): ВЫХОД ИЗ ЛАМПЫ СПРАВА -->
    <line x1="620" y1="470" x2="910" y2="470" stroke="#fbbf24" stroke-width="5"/>
    <line x1="730" y1="470" x2="790" y2="470" stroke="#fbbf24" stroke-width="5" marker-end="url(#arrowGold)"/>

    <!-- Верхний правый угол 90° -->
    <circle cx="910" cy="470" r="8" fill="#ffffff" stroke="#fbbf24" stroke-width="3"/>

    <!-- 5. ПРАВАЯ ВЕРТИКАЛЬНАЯ ШИНА (x = 910): спуск к ДЗАНСИНУ -->
    <line x1="910" y1="470" x2="910" y2="650" stroke="#fbbf24" stroke-width="5"/>
    <line x1="910" y1="540" x2="910" y2="600" stroke="#fbbf24" stroke-width="5" marker-end="url(#arrowGold)"/>

    <!-- ПРЕДОХРАНИТЕЛЬ ДЗАНСИН (ВРЕЗАН В ЦЕПЬ ПОСЛЕДОВАТЕЛЬНО НА x=910) -->
    <!-- Верхняя клемма -->
    <circle cx="910" cy="650" r="7" fill="#f59e0b" stroke="#ffffff" stroke-width="2.5"/>
    <!-- Корпус защитного автомата отсечки -->
    <rect x="893" y="656" width="34" height="78" rx="8" fill="#0f172a" stroke="#f59e0b" stroke-width="3"/>
    <!-- Внутренний калиброванный элемент (Fuse) -->
    <line x1="910" y1="662" x2="910" y2="728" stroke="#fef08a" stroke-width="4"/>
    <circle cx="910" cy="695" r="5" fill="#ef4444"/>
    <!-- Нижняя клемма -->
    <circle cx="910" cy="740" r="7" fill="#f59e0b" stroke="#ffffff" stroke-width="2.5"/>

    <!-- Правая шина от ДЗАНСИН вниз к нижнему правому углу -->
    <line x1="910" y1="740" x2="910" y2="930" stroke="#ef4444" stroke-width="5"/>
    <line x1="910" y1="810" x2="910" y2="870" stroke="#ef4444" stroke-width="5" marker-end="url(#arrowRed)"/>

    <!-- Нижний правый угол 90° -->
    <circle cx="910" cy="930" r="8" fill="#ffffff" stroke="#ef4444" stroke-width="3"/>

    <!-- 6. НИЖНЯЯ ВЕТВЬ ШИНЫ (y = 930): возврат справа в ТАНДЭН -->
    <line x1="910" y1="930" x2="598" y2="930" stroke="#ef4444" stroke-width="5"/>
    <line x1="770" y1="930" x2="710" y2="930" stroke="#ef4444" stroke-width="5" marker-end="url(#arrowRed)"/>

    <!-- ======================================================== -->
    <!-- 4. РЕАКТОР ТАНДЭН (ВРЕЗАН В ЦЕПЬ ПО ЦЕНТРУ Y = 930)      -->
    <!-- Левая клемма: x = 502, Правая клемма: x = 598            -->
    <!-- ======================================================== -->
    <g transform="translate(550, 930)">
      <!-- Алое сияние в глубине живота -->
      <circle cx="0" cy="0" r="85" fill="url(#tandenGlow)"/>
      <!-- Бронированный корпус генератора -->
      <rect x="-48" y="-48" width="96" height="96" rx="20" fill="#0b1120" stroke="#ef4444" stroke-width="4.5"/>
      <!-- Сердечник ядерной ЭДС -->
      <circle cx="0" cy="0" r="32" fill="#7f1d1d" stroke="#f87171" stroke-width="2.5"/>
      <circle cx="0" cy="0" r="18" fill="#ef4444"/>
      <circle cx="0" cy="0" r="9" fill="#ffffff"/>
      <!-- Клеммы ввода/вывода генератора -->
      <circle cx="-48" cy="0" r="7" fill="#f87171" stroke="#ffffff" stroke-width="2.5"/>
      <circle cx="48" cy="0" r="7" fill="#f87171" stroke="#ffffff" stroke-width="2.5"/>
      <!-- Маркировка ЭДС -->
      <text x="0" y="5" font-family="monospace" font-size="14" font-weight="900" fill="#ffffff" text-anchor="middle">⚡ E</text>
    </g>


    <!-- ======================================================== -->
    <!-- 5. ТЕКСТОВЫЕ БЛОКИ И РУССКИЕ ПОЯСНЕНИЯ                   -->
    <!-- ======================================================== -->

    <!-- БЛОК 1: ТАНДЭН (внизу под животом) -->
    <g transform="translate(550, 1035)" text-anchor="middle">
      <rect x="-150" y="0" width="300" height="74" rx="10" fill="#0f172a" stroke="#ef4444" stroke-width="2.5"/>
      <text x="0" y="27" font-size="20" font-weight="900" fill="#ffffff" letter-spacing="1">ТАНДЭН (丹田)</text>
      <text x="0" y="47" font-size="13" font-weight="700" fill="#ef4444">ИСТОЧНИК ЭДС / ГЕНЕРАТОР</text>
      <text x="0" y="64" font-size="11" font-family="monospace" fill="#94a3b8">Уровень живота / Первичный покой и заряд</text>
    </g>

    <!-- БЛОК 2: ГЁ (вверху над лампой) -->
    <g transform="translate(550, 335)" text-anchor="middle">
      <rect x="-160" y="0" width="320" height="74" rx="10" fill="#0f172a" stroke="#f59e0b" stroke-width="2.5"/>
      <text x="0" y="27" font-size="20" font-weight="900" fill="#ffffff" letter-spacing="1">ГЁ (行)</text>
      <text x="0" y="47" font-size="13" font-weight="700" fill="#facc15">ДЕЛО / ЛАМПА НАГРУЗКИ</text>
      <text x="0" y="64" font-size="11" font-family="monospace" fill="#cbd5e1">В руках на уровне головы / Излучение света в мир</text>
    </g>

    <!-- БЛОК 3: ХОЦУ (слева от выключателя) -->
    <g transform="translate(170, 695)" text-anchor="end">
      <rect x="-240" y="-37" width="230" height="74" rx="10" fill="#0f172a" stroke="#38bdf8" stroke-width="2.5"/>
      <text x="-15" y="-12" font-size="18" font-weight="900" fill="#ffffff" letter-spacing="1">ХОЦУ (発)</text>
      <text x="-15" y="10" font-size="12" font-weight="700" fill="#38bdf8">ВЫКЛЮЧАТЕЛЬ «ХОЧУ»</text>
      <text x="-15" y="27" font-size="10" font-family="monospace" fill="#94a3b8">Ключ Normally Open (ВКЛ)</text>
    </g>

    <!-- БЛОК 4: ДЗАНСИН (справа от предохранителя) -->
    <g transform="translate(930, 695)" text-anchor="start">
      <rect x="10" y="-37" width="240" height="74" rx="10" fill="#0f172a" stroke="#f59e0b" stroke-width="2.5"/>
      <text x="25" y="-12" font-size="18" font-weight="900" fill="#ffffff" letter-spacing="1">ДЗАНСИН (残心)</text>
      <text x="25" y="10" font-size="12" font-weight="700" fill="#f59e0b">ПРЕДОХРАНИТЕЛЬ / FUSE</text>
      <text x="25" y="27" font-size="10" font-family="monospace" fill="#94a3b8">Circuit Breaker / Защита ядра</text>
    </g>

    <!-- БЛОК 5: МУСИН (надписи на верхней шине) -->
    <g transform="translate(340, 442)" text-anchor="middle">
      <rect x="-120" y="-16" width="240" height="22" rx="4" fill="#030712" stroke="#38bdf8" stroke-width="1.2"/>
      <text x="0" y="-1" font-family="monospace" font-size="11" font-weight="700" fill="#38bdf8" letter-spacing="1">МУСИН: ШИНА ВНИМАНИЯ (R → 0)</text>
    </g>
    <g transform="translate(760, 442)" text-anchor="middle">
      <rect x="-120" y="-16" width="240" height="22" rx="4" fill="#030712" stroke="#fbbf24" stroke-width="1.2"/>
      <text x="0" y="-1" font-family="monospace" font-size="11" font-weight="700" fill="#fbbf24" letter-spacing="1">МУСИН: ОБРАТНАЯ ШИНА (無心)</text>
    </g>

    <!-- ПОЯСНИТЕЛЬНЫЙ ПОДВАЛ ЧЕРТЕЖА -->
    <g transform="translate(60, 1375)">
      <rect x="0" y="0" width="980" height="42" rx="8" fill="#0f172a" stroke="#1e293b" stroke-width="1.5"/>
      <text x="20" y="26" font-size="13" font-weight="800" fill="#38bdf8" font-family="monospace">ЕДИНАЯ НЕРАЗРЫВНАЯ ЦЕПЬ:</text>
      <text x="235" y="26" font-size="13" font-weight="600" fill="#f8fafc">
        Тандэн (питает) ➔ Хоцу (включает) ➔ Гё (светит) ➔ Дзансин (бережёт) ➔ Мусин (проводит без потерь)
      </text>
      <text x="960" y="26" font-size="11" font-family="monospace" fill="#64748b" text-anchor="end">I > 0 | R_ego = 0</text>
    </g>

  </svg>
</body>
</html>
"""

with open("temp_circuit.html", "w", encoding="utf-8") as f:
    f.write(html_content)

output_path = r"C:\Users\vanya\.gemini\antigravity\brain\3ebdfd13-c38d-47bb-b8a5-4e69c7e0d70c\thgdm_human_circuit.png"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1100, "height": 1450}, device_scale_factor=2)
    page.goto("file:///" + os.path.abspath("temp_circuit.html").replace("\\", "/"))
    page.wait_for_timeout(400)
    page.screenshot(path=output_path)
    browser.close()

print("UPDATED_IMAGE_CREATED:", os.path.exists(output_path))
