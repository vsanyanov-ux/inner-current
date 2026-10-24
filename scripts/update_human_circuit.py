# -*- coding: utf-8 -*-
"""
Update human circuit pages to add:
- Контур I inside Tanden battery (electrochemical reaction and circulation arrows)
- Контур II for the outer circuit (Mushin flow and center badge)
"""
import os
import re

def update_ru(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        c = f.read()

    # 1. Inside battery: replace circle 1 with Контур I (inner circuit)
    old_battery_circle = """              <g>
                <circle cx="310" cy="640" r="14" fill="#451a03" stroke="#fef08a" stroke-width="1.5" />
                <text x="310" y="644" fill="#fef08a" font-size="11" font-weight="900" text-anchor="middle">1</text>
              </g>"""

    new_battery_circuit = """              <!-- КОНТУР I ВНУТРИ БАТАРЕЙКИ (Электрохимическая реакция разделения зарядов) -->
              <g id="tandenInnerCircuit">
                <!-- Внутренний циркуляционный контур реактора -->
                <rect x="274" y="624" width="72" height="32" rx="8" fill="#2d0f02" fill-opacity="0.95" stroke="#fde047" stroke-width="1.6" stroke-dasharray="3 1.5" />
                
                <!-- Стрелки циркуляции внутри батарейки (Контур I: сторонние силы расталкивают заряды) -->
                <!-- Верхняя стрелка (влево, к отрицательной клемме) -->
                <path d="M 334,629 L 286,629" fill="none" stroke="#fef08a" stroke-width="1.3" stroke-linecap="round" />
                <polygon points="286,629 291,626.5 291,631.5" fill="#fef08a" />
                
                <!-- Нижняя стрелка (вправо, к положительной клемме) -->
                <path d="M 286,651 L 334,651" fill="none" stroke="#fef08a" stroke-width="1.3" stroke-linecap="round" />
                <polygon points="334,651 329,648.5 329,653.5" fill="#fef08a" />

                <!-- Надписи внутри батарейки -->
                <text x="310" y="639" fill="#ffffff" font-size="9" font-weight="900" text-anchor="middle" letter-spacing="0.5">КОНТУР I</text>
                <text x="310" y="648" fill="#fde047" font-size="6.5" font-weight="800" text-anchor="middle" letter-spacing="0.2">ХИМ. РЕАКЦИЯ</text>
              </g>"""

    if old_battery_circle in c:
        c = c.replace(old_battery_circle, new_battery_circuit, 1)
        print(f"[{file_path}] Replaced battery circle with Kontur I")
    else:
        print(f"[{file_path}] Warning: old_battery_circle not found")

    # 2. Tanden badge: update text to mention Контур I
    old_tanden_badge = """                <rect x="200" y="705" width="220" height="42" rx="12" fill="#451a03" fill-opacity="0.96" stroke="#f59e0b" stroke-width="2.5" />
                <circle cx="222" cy="726" r="11" fill="#f59e0b" />
                <text x="222" y="730" fill="#451a03" font-size="12" font-weight="900" text-anchor="middle">1</text>
                <text x="240" y="721" fill="#ffffff" font-size="11" font-weight="900">ТАНДЭН (丹田) — Живот</text>
                <text x="240" y="737" fill="#fef3c7" font-size="9" font-weight="bold">Батарейка • Нижний реактор</text>"""

    new_tanden_badge = """                <rect x="180" y="705" width="260" height="44" rx="12" fill="#451a03" fill-opacity="0.96" stroke="#f59e0b" stroke-width="2.5" />
                <circle cx="204" cy="727" r="11" fill="#f59e0b" />
                <text x="204" y="731" fill="#451a03" font-size="12" font-weight="900" text-anchor="middle">1</text>
                <text x="224" y="722" fill="#ffffff" font-size="11" font-weight="900">КОНТУР I: ТАНДЭН (丹田)</text>
                <text x="224" y="738" fill="#fef3c7" font-size="9" font-weight="bold">Батарейка • Химическая реакция (ЭДС)</text>"""

    if old_tanden_badge in c:
        c = c.replace(old_tanden_badge, new_tanden_badge, 1)
        print(f"[{file_path}] Updated Tanden badge")
    else:
        print(f"[{file_path}] Warning: old_tanden_badge not found")

    # 3. Outer circuit: add central "КОНТУР II" indicator badge in the torso loop
    # We place it right before <!-- 1. ТАНДЭН
    center_circuit2_svg = """            <!-- ЦЕНТРАЛЬНОЕ ОБОЗНАЧЕНИЕ: КОНТУР II (МУСИН) -->
            <g id="circuit2CenterBadge" opacity="0.95" class="transition-opacity duration-300">
              <!-- Плашка в центре замкнутого контура тела -->
              <rect x="220" y="470" width="180" height="46" rx="14" fill="#090d16" fill-opacity="0.88" stroke="#f59e0b" stroke-width="1.8" stroke-dasharray="4 2" />
              <!-- Круговая стрелка потока Мусин (против часовой стрелки: от батарейки через правую руку в лампу) -->
              <path d="M 242,493 A 9 9 0 1 1 244,484" fill="none" stroke="#fdba74" stroke-width="2" stroke-linecap="round" />
              <polygon points="247,482 240,480 243,487" fill="#fdba74" />
              <text x="318" y="488" fill="#fef08a" font-size="11.5" font-weight="900" text-anchor="middle" letter-spacing="1">КОНТУР II</text>
              <text x="318" y="504" fill="#fdba74" font-size="8.5" font-weight="bold" text-anchor="middle" letter-spacing="0.5">ВНЕШНИЙ ТОК • МУСИН</text>
            </g>

"""

    target_before_tanden = "            <!-- 1. ТАНДЭН (丹田) — БАТАРЕЙКА В ЖИВОТЕ (Нижний даньтянь / хара) -->"
    if target_before_tanden in c and "id=\"circuit2CenterBadge\"" not in c:
        c = c.replace(target_before_tanden, center_circuit2_svg + target_before_tanden, 1)
        print(f"[{file_path}] Added central circuit2CenterBadge")

    # 4. Mushin badge: update to КОНТУР II: МУСИН (無心)
    old_mushin_badge = """            <!-- 3. МУСИН (無心) — ТОК ВНИМАНИЯ (Течёт по правой руке в ладони) -->
            <g class="zen-pointer" onclick="showElement('mushin')" id="human-elem-mushin">
              <line x1="435" y1="345" x2="480" y2="305" stroke="#f97316" stroke-width="2" stroke-dasharray="2 2" />
              <rect id="humanMushinBadgeBg" x="410" y="265" width="195" height="40" rx="12" fill="#431407" fill-opacity="0.95" stroke="#f97316" stroke-width="2.5" />
              <circle cx="430" cy="285" r="11" fill="#f97316" />
              <text x="430" y="289" fill="#ffffff" font-size="12" font-weight="900" text-anchor="middle">3</text>
              <text x="448" y="280" fill="#fdba74" font-size="11" font-weight="900">МУСИН (無心) — Ток</text>
              <text x="448" y="295" fill="#ffffff" font-size="9" font-weight="bold">Поток по руке без эго</text>
            </g>"""

    new_mushin_badge = """            <!-- 3. МУСИН (無心) — ТОК ВНИМАНИЯ (КОНТУР II) -->
            <g class="zen-pointer" onclick="showElement('mushin')" id="human-elem-mushin">
              <line x1="435" y1="345" x2="480" y2="305" stroke="#f97316" stroke-width="2" stroke-dasharray="2 2" />
              <rect id="humanMushinBadgeBg" x="390" y="265" width="225" height="42" rx="12" fill="#431407" fill-opacity="0.95" stroke="#f97316" stroke-width="2.5" />
              <circle cx="410" cy="286" r="11" fill="#f97316" />
              <text x="410" y="290" fill="#ffffff" font-size="12" font-weight="900" text-anchor="middle">3</text>
              <text x="428" y="281" fill="#fdba74" font-size="11" font-weight="900">КОНТУР II: МУСИН (無心)</text>
              <text x="428" y="296" fill="#ffffff" font-size="9" font-weight="bold">Внешний сверхпроводящий ток</text>
            </g>"""

    if old_mushin_badge in c:
        c = c.replace(old_mushin_badge, new_mushin_badge, 1)
        print(f"[{file_path}] Updated Mushin badge to Kontur II")
    else:
        print(f"[{file_path}] Warning: old_mushin_badge not found")

    # 5. Interactive subtitle and status labels
    c = c.replace(
        '<div id="humanHotsuSub" class="text-sm font-black">Ток «Мусин» зажигает лампочку в руках!</div>',
        '<div id="humanHotsuSub" class="text-sm font-black text-amber-200">Контур I (Тандэн) питает Контур II (Мусин) и зажигает лампочку!</div>'
    )
    c = c.replace(
        '⚡ Цепь замкнута: Тандэн питает лампочку в руках через чистый ток Мусин!',
        '⚡ Контур I заряжает Контур II: Тандэн питает лампочку через чистый ток Мусин!'
    )
    c = c.replace(
        '⭕ Цепь разомкнута: контакт Хоцу отведен, ток Мусин остановлен',
        '⭕ Контур II разомкнут: контакт Хоцу отведен, внешний ток остановлен (Контур I в режиме ожидания)'
    )

    # 6. JavaScript humanElements updates
    c = c.replace(
        'title: "1. Тандэн (丹田) — Батарейка в животе (Энергетическое ядро)",\n        text: "Расположен на 3 пальца ниже пупка (нижний даньтянь / хара). Это биологический аккумулятор человека: клеточный метаболизм, глубокое диафрагмальное дыхание и запас витальной силы. Если батарейка разряжена или не заземлена, ни одно волевое усилие не сможет зажечь свет в руках."',
        'title: "1. Тандэн (丹田) — Контур I: Батарейка в животе (Электрохимический реактор)",\n        text: "Контур I замкнут внутри батарейки: электрохимическая реакция разделения зарядов, клеточный метаболизм, глубокое брюшное дыхание и запас витальной силы. Контур I вырабатывает ЭДС и непрерывно заряжает внешний Контур II. Если электролит истощён, ни одно волевое усилие не сможет зажечь свет в руках."'
    )
    c = c.replace(
        'role: "ИСТОЧНИК ПОТЕНЦИАЛА",',
        'role: "КОНТУР I • ИСТОЧНИК ЭДС",'
    )

    c = c.replace(
        'title: "3. Мусин (無心) — Ток внимания (Состояние потока)",\n        text: "Беспрепятственное протекание энергии по телу. Мусин — это \'не-ум\', отсутствие паразитного сопротивления эго, сомнений и зажимов. Ток мчится по чистым рукам прямо к ладоням с максимальным КПД, подчиняясь закону Ома."',
        'title: "3. Мусин (無心) — Контур II: Внешний ток внимания (Состояние потока)",\n        text: "Контур II — это внешняя цепь тока, питающая лампочку Гё. Беспрепятственное протекание энергии по телу без паразитного сопротивления эго (R_ego → 0). Мусин — это \'не-ум\', сверхпроводимость внимания от батарейки к созидательному действию."'
    )
    c = c.replace(
        'role: "ПОТОК ВНИМАНИЯ",',
        'role: "КОНТУР II • СВЕРХПРОВОДЯЩИЙ ПОТОК",'
    )

    # 7. Bottom quick switch buttons
    c = c.replace(
        '<span class="text-xs font-mono text-amber-400 font-bold">#1 • ЯДРО</span>',
        '<span class="text-xs font-mono text-amber-400 font-bold">#1 • КОНТУР I</span>'
    )
    c = c.replace(
        '<span class="text-[10px] text-slate-400 truncate">Батарейка • Реактор</span>',
        '<span class="text-[10px] text-slate-400 truncate">Контур I • Батарейка</span>'
    )
    c = c.replace(
        '<span class="text-xs font-mono text-orange-400 font-bold">#3 • ТОК</span>',
        '<span class="text-xs font-mono text-orange-400 font-bold">#3 • КОНТУР II</span>'
    )
    c = c.replace(
        '<span class="text-[10px] text-slate-400 truncate">Ток Мусин • Поток</span>',
        '<span class="text-[10px] text-slate-400 truncate">Контур II • Поток</span>'
    )

    # 8. Comparison table
    c = c.replace(
        '<td class="py-3.5 px-4 font-bold text-white">Тандэн (丹田)</td>',
        '<td class="py-3.5 px-4 font-bold text-white">Тандэн (丹田) — Контур I</td>'
    )
    c = c.replace(
        '<td class="py-3.5 px-4 text-slate-400">Источник электродвижущей силы (ЭДС)</td>',
        '<td class="py-3.5 px-4 text-slate-400">Контур I: электрохимическая реакция разделения зарядов и выработка ЭДС</td>'
    )
    c = c.replace(
        '<td class="py-3.5 px-4 font-bold text-white">Мусин (無心)</td>',
        '<td class="py-3.5 px-4 font-bold text-white">Мусин (無心) — Контур II</td>'
    )
    c = c.replace(
        '<td class="py-3.5 px-4 text-slate-400">Свободное течение тока без сопротивления эго (R_ego = 0)</td>',
        '<td class="py-3.5 px-4 text-slate-400">Контур II: внешний поток внимания и полезного действия без омического сопротивления эго</td>'
    )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"[{file_path}] Finished update successfully.")


def update_en(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        c = f.read()

    # 1. Inside battery: replace circle 1 with Circuit I
    old_battery_circle = """              <g>
                <circle cx="310" cy="640" r="14" fill="#451a03" stroke="#fef08a" stroke-width="1.5" />
                <text x="310" y="644" fill="#fef08a" font-size="11" font-weight="900" text-anchor="middle">1</text>
              </g>"""

    new_battery_circuit = """              <!-- CIRCUIT I INSIDE BATTERY (Electrochemical charge separation) -->
              <g id="tandenInnerCircuit">
                <!-- Inner circulation loop -->
                <rect x="274" y="624" width="72" height="32" rx="8" fill="#2d0f02" fill-opacity="0.95" stroke="#fde047" stroke-width="1.6" stroke-dasharray="3 1.5" />
                
                <!-- Circulation arrows inside battery (Circuit I: nonelectrostatic EMF forces) -->
                <!-- Top arrow (left, towards negative terminal) -->
                <path d="M 334,629 L 286,629" fill="none" stroke="#fef08a" stroke-width="1.3" stroke-linecap="round" />
                <polygon points="286,629 291,626.5 291,631.5" fill="#fef08a" />
                
                <!-- Bottom arrow (right, towards positive terminal) -->
                <path d="M 286,651 L 334,651" fill="none" stroke="#fef08a" stroke-width="1.3" stroke-linecap="round" />
                <polygon points="334,651 329,648.5 329,653.5" fill="#fef08a" />

                <!-- Battery labels -->
                <text x="310" y="639" fill="#ffffff" font-size="9" font-weight="900" text-anchor="middle" letter-spacing="0.5">CIRCUIT I</text>
                <text x="310" y="648" fill="#fde047" font-size="6.5" font-weight="800" text-anchor="middle" letter-spacing="0.2">CHEM. REACTION</text>
              </g>"""

    if old_battery_circle in c:
        c = c.replace(old_battery_circle, new_battery_circuit, 1)
        print(f"[{file_path}] Replaced battery circle with Circuit I")

    # 2. Tanden badge: update text to mention Circuit I
    old_tanden_badge = """                <rect x="200" y="705" width="220" height="42" rx="12" fill="#451a03" fill-opacity="0.96" stroke="#f59e0b" stroke-width="2.5" />
                <circle cx="222" cy="726" r="11" fill="#f59e0b" />
                <text x="222" y="730" fill="#451a03" font-size="12" font-weight="900" text-anchor="middle">1</text>
                <text x="240" y="721" fill="#ffffff" font-size="11" font-weight="900">TANDEN (丹田) — Belly</text>
                <text x="240" y="737" fill="#fef3c7" font-size="9" font-weight="bold">Battery • Lower Reactor</text>"""

    new_tanden_badge = """                <rect x="180" y="705" width="260" height="44" rx="12" fill="#451a03" fill-opacity="0.96" stroke="#f59e0b" stroke-width="2.5" />
                <circle cx="204" cy="727" r="11" fill="#f59e0b" />
                <text x="204" y="731" fill="#451a03" font-size="12" font-weight="900" text-anchor="middle">1</text>
                <text x="224" y="722" fill="#ffffff" font-size="11" font-weight="900">CIRCUIT I: TANDEN (丹田)</text>
                <text x="224" y="738" fill="#fef3c7" font-size="9" font-weight="bold">Battery • Chemical Reaction (EMF)</text>"""

    if old_tanden_badge in c:
        c = c.replace(old_tanden_badge, new_tanden_badge, 1)
        print(f"[{file_path}] Updated Tanden badge to Circuit I")

    # 3. Outer circuit: add central "CIRCUIT II" indicator badge in the torso loop
    center_circuit2_svg = """            <!-- CENTRAL LABEL: CIRCUIT II (MUSHIN) -->
            <g id="circuit2CenterBadge" opacity="0.95" class="transition-opacity duration-300">
              <!-- Central badge in the loop -->
              <rect x="220" y="470" width="180" height="46" rx="14" fill="#090d16" fill-opacity="0.88" stroke="#f59e0b" stroke-width="1.8" stroke-dasharray="4 2" />
              <!-- Circular flow arrow -->
              <path d="M 242,493 A 9 9 0 1 1 244,484" fill="none" stroke="#fdba74" stroke-width="2" stroke-linecap="round" />
              <polygon points="247,482 240,480 243,487" fill="#fdba74" />
              <text x="318" y="488" fill="#fef08a" font-size="11.5" font-weight="900" text-anchor="middle" letter-spacing="1">CIRCUIT II</text>
              <text x="318" y="504" fill="#fdba74" font-size="8.5" font-weight="bold" text-anchor="middle" letter-spacing="0.5">OUTER FLOW • MUSHIN</text>
            </g>

"""

    target_before_tanden = "            <!-- 1. ТАНДЭН (丹田) — БАТАРЕЙКА В ЖИВОТЕ"
    if target_before_tanden not in c:
        target_before_tanden = "            <!-- 1. TANDEN (丹田)"
    if target_before_tanden in c and "id=\"circuit2CenterBadge\"" not in c:
        c = c.replace(target_before_tanden, center_circuit2_svg + target_before_tanden, 1)
        print(f"[{file_path}] Added central circuit2CenterBadge EN")

    # 4. Mushin badge: update to CIRCUIT II: MUSHIN (無心)
    c = c.replace(
        '<text x="448" y="280" fill="#fdba74" font-size="11" font-weight="900">MUSHIN (無心) — Flow</text>',
        '<text x="448" y="280" fill="#fdba74" font-size="11" font-weight="900">CIRCUIT II: MUSHIN (無心)</text>'
    )
    c = c.replace(
        '<text x="448" y="295" fill="#ffffff" font-size="9" font-weight="bold">Superconducting current</text>',
        '<text x="448" y="295" fill="#ffffff" font-size="9" font-weight="bold">Outer superconducting current</text>'
    )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"[{file_path}] Finished EN update successfully.")


if __name__ == '__main__':
    update_ru('dist_site/human/index.html')
    update_ru('dist_site/human.html')
    update_en('dist_site/en/human/index.html')
    update_en('dist_site/en/human.html')
    update_en('dist_site/flashlight/en.html') if os.path.exists('dist_site/flashlight/en.html') else None
