#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_en_site.py
Generates the complete English version of the Inner Current website:
- dist_site/en/index.html & dist_site/en.html
- dist_site/en/flashlight/index.html & dist_site/flashlight/en.html & dist_site/en/flashlight.html
- dist_site/en/human/index.html & dist_site/human/en.html & dist_site/en/human.html
And updates Russian files with bilingual language switcher [RU | EN].
"""

import os
import shutil

DIST_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "dist_site"))

def update_russian_files():
    # 1. Update index.html
    idx_path = os.path.join(DIST_DIR, "index.html")
    with open(idx_path, "r", encoding="utf-8") as f:
        html = f.read()

    ru_nav_switcher = """      <!-- Language Switcher & Quick Action Buttons -->
      <div class="flex items-center gap-3">
        <!-- Language Switcher -->
        <div class="flex items-center rounded-xl bg-slate-900 border border-slate-800 p-0.5 text-xs font-mono font-semibold" title="Выбор языка / Language selection">
          <span class="px-2.5 py-1 rounded-lg bg-amber-500 text-slate-950 font-bold shadow-sm cursor-default">RU</span>
          <a href="/en/" onclick="localStorage.setItem('inner_current_lang','en')" class="px-2.5 py-1 rounded-lg text-slate-400 hover:text-slate-100 hover:bg-slate-800/80 transition">EN</a>
        </div>"""

    if "<!-- Language Switcher -->" not in html:
        old_block = """      <!-- Quick Action Buttons -->\n      <div class="flex items-center gap-3">"""
        if old_block in html:
            html = html.replace(old_block, ru_nav_switcher, 1)

    if "English Version ↗" not in html:
        footer_old = """        <a href="audiobook/index.html" target="_blank" class="hover:text-slate-200 transition">Студия ↗</a>\n      </div>"""
        footer_new = """        <a href="audiobook/index.html" target="_blank" class="hover:text-slate-200 transition">Студия ↗</a>\n        <span>•</span>\n        <a href="/en/" onclick="localStorage.setItem('inner_current_lang','en')" class="text-amber-400 hover:underline">English Version ↗</a>\n      </div>"""
        if footer_old in html:
            html = html.replace(footer_old, footer_new, 1)

    with open(idx_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("Updated Russian index.html")

    # 2. Update flashlight.html and flashlight/index.html
    for rel_path in ["flashlight.html", "flashlight/index.html"]:
        p = os.path.join(DIST_DIR, rel_path)
        if not os.path.exists(p):
            continue
        with open(p, "r", encoding="utf-8") as f:
            f_html = f.read()
        if "<!-- Language Switcher -->" not in f_html:
            old_nav = """      <div class="flex items-center gap-3">
        <a href="/human/" class="px-3.5 py-1.5 rounded-xl bg-amber-500/10 hover:bg-amber-500/20 text-xs font-semibold text-amber-300 hover:text-amber-200 transition flex items-center gap-1.5 border border-amber-500/30">"""
            new_nav = """      <div class="flex items-center gap-3">
        <!-- Language Switcher -->
        <div class="flex items-center rounded-xl bg-slate-900 border border-slate-800 p-0.5 text-xs font-mono font-semibold" title="Выбор языка / Language selection">
          <span class="px-2.5 py-1 rounded-lg bg-amber-500 text-slate-950 font-bold shadow-sm cursor-default">RU</span>
          <a href="/en/flashlight/" onclick="localStorage.setItem('inner_current_lang','en')" class="px-2.5 py-1 rounded-lg text-slate-400 hover:text-slate-100 hover:bg-slate-800/80 transition">EN</a>
        </div>
        <a href="/human/" class="px-3.5 py-1.5 rounded-xl bg-amber-500/10 hover:bg-amber-500/20 text-xs font-semibold text-amber-300 hover:text-amber-200 transition flex items-center gap-1.5 border border-amber-500/30">"""
            if old_nav in f_html:
                f_html = f_html.replace(old_nav, new_nav, 1)
        with open(p, "w", encoding="utf-8") as f:
            f.write(f_html)
        print(f"Updated Russian {rel_path}")

    # 3. Update human.html and human/index.html
    for rel_path in ["human.html", "human/index.html"]:
        p = os.path.join(DIST_DIR, rel_path)
        if not os.path.exists(p):
            continue
        with open(p, "r", encoding="utf-8") as f:
            h_html = f.read()
        if "<!-- Language Switcher -->" not in h_html:
            old_nav = """      <div class="flex items-center gap-3">
        <a href="/flashlight/" class="px-3.5 py-1.5 rounded-xl bg-slate-800/80 hover:bg-slate-700 text-xs font-semibold text-slate-300 hover:text-white transition flex items-center gap-1.5 border border-slate-700/60">"""
            new_nav = """      <div class="flex items-center gap-3">
        <!-- Language Switcher -->
        <div class="flex items-center rounded-xl bg-slate-900 border border-slate-800 p-0.5 text-xs font-mono font-semibold" title="Выбор языка / Language selection">
          <span class="px-2.5 py-1 rounded-lg bg-amber-500 text-slate-950 font-bold shadow-sm cursor-default">RU</span>
          <a href="/en/human/" onclick="localStorage.setItem('inner_current_lang','en')" class="px-2.5 py-1 rounded-lg text-slate-400 hover:text-slate-100 hover:bg-slate-800/80 transition">EN</a>
        </div>
        <a href="/flashlight/" class="px-3.5 py-1.5 rounded-xl bg-slate-800/80 hover:bg-slate-700 text-xs font-semibold text-slate-300 hover:text-white transition flex items-center gap-1.5 border border-slate-700/60">"""
            if old_nav in h_html:
                h_html = h_html.replace(old_nav, new_nav, 1)
        with open(p, "w", encoding="utf-8") as f:
            f.write(h_html)
        print(f"Updated Russian {rel_path}")

def generate_en_index():
    en_dir = os.path.join(DIST_DIR, "en")
    os.makedirs(en_dir, exist_ok=True)
    out_path = os.path.join(en_dir, "index.html")

    base_path = os.path.join(DIST_DIR, "index.html")
    with open(base_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. HTML lang
    content = content.replace('<html lang="ru"', '<html lang="en"', 1)

    # 2. Title & Meta
    content = content.replace(
        '<title>Внутренний ток — Библиотека прикладных книг и руководств</title>',
        '<title>Inner Current — Applied Books & Engineering Guides</title>', 1
    )
    content = content.replace(
        '<meta name="description" content="Электродинамика сознания и архитектура внутреннего состояния. Семь практических книг и руководств: от экспресс-отладки острой перегрузки до прикладной акустики и синтеза физики с сознанием.">',
        '<meta name="description" content="Electrodynamics of consciousness and the architecture of the inner state. Seven practical books and guides: from emergency debugging of acute overload to applied acoustics and the synthesis of physics with consciousness.">', 1
    )

    # 3. Navbar brand sub
    content = content.replace('Библиотека книг', 'Library of Books', 1)

    # 4. Navbar links
    content = content.replace('<a href="#books" class="hover:text-amber-300 transition">Книги</a>', '<a href="#books" class="hover:text-amber-300 transition">Books</a>', 1)
    content = content.replace('<a href="#reader" class="hover:text-amber-300 transition">Онлайн-ридер</a>', '<a href="#reader" class="hover:text-amber-300 transition">Online Reader</a>', 1)
    content = content.replace('<span>🎧</span> Аудиокнига', '<span>🎧</span> Audiobook', 1)
    content = content.replace('<span>🔦</span> Дзен-фонарик', '<span>🔦</span> Zen Flashlight', 1)
    content = content.replace('<span>🧘</span> Человек-контур', '<span>🧘</span> Human Circuit', 1)
    content = content.replace('🎧 Аудиокнига', '🎧 Audiobook', 1)
    content = content.replace('// замкнут контакт на самом верхнем проводе', '// contact closed on top wire')
    content = content.replace('// контакт поднят на y=132 (внутри корпуса y=120..300, не пересекает провода!)', '// contact raised to y=132')
    content = content.replace('// КНОПКА ЗАМКНУТА -> ЗЕЛЕНАЯ!', '// BUTTON CLOSED -> GREEN')
    content = content.replace('// КНОПКА РАЗОМКНУТА -> КРАСНАЯ!', '// BUTTON OPEN -> RED')
    content = content.replace('<a href="/human/" class="hover:text-amber-300 transition flex items-center gap-1.5">', '<a href="/en/human/" class="hover:text-amber-300 transition flex items-center gap-1.5">', 1)
    content = content.replace('<a href="#monographs" class="hover:text-slate-100 transition">Материалы PDF</a>', '<a href="#monographs" class="hover:text-slate-100 transition">PDF Materials</a>', 1)
    content = content.replace('<a href="#principles" class="hover:text-slate-100 transition">Принципы</a>', '<a href="#principles" class="hover:text-slate-100 transition">Principles</a>', 1)

    # 5. Language Switcher in EN navbar
    en_switcher = """        <!-- Language Switcher -->
        <div class="flex items-center rounded-xl bg-slate-900 border border-slate-800 p-0.5 text-xs font-mono font-semibold" title="Language selection">
          <a href="/" onclick="localStorage.setItem('inner_current_lang','ru')" class="px-2.5 py-1 rounded-lg text-slate-400 hover:text-slate-100 hover:bg-slate-800/80 transition">RU</a>
          <span class="px-2.5 py-1 rounded-lg bg-amber-500 text-slate-950 font-bold shadow-sm cursor-default">EN</span>
        </div>"""
    ru_switcher_search = """        <!-- Language Switcher -->
        <div class="flex items-center rounded-xl bg-slate-900 border border-slate-800 p-0.5 text-xs font-mono font-semibold" title="Выбор языка / Language selection">
          <span class="px-2.5 py-1 rounded-lg bg-amber-500 text-slate-950 font-bold shadow-sm cursor-default">RU</span>
          <a href="/en/" onclick="localStorage.setItem('inner_current_lang','en')" class="px-2.5 py-1 rounded-lg text-slate-400 hover:text-slate-100 hover:bg-slate-800/80 transition">EN</a>
        </div>"""
    if ru_switcher_search in content:
        content = content.replace(ru_switcher_search, en_switcher, 1)

    # Navbar action buttons
    content = content.replace('<span class="hidden sm:inline">Слушать</span>', '<span class="hidden sm:inline">Listen</span>', 1)
    content = content.replace('<span>📖</span> <span>Ридер</span>', '<span>📖</span> <span>Reader</span>', 1)

    # 6. Hero section
    content = content.replace('<span>⚡</span> ВНУТРЕННИЙ ТОК • 7 КНИГ И РУКОВОДСТВ', '<span>⚡</span> INNER CURRENT • 7 BOOKS & MANUALS', 1)
    content = content.replace(
        'Внутренний ток <br class="hidden sm:inline"/>\n        <span class="bg-gradient-to-r from-amber-400 via-amber-300 to-sky-300 bg-clip-text text-transparent text-glow-amber">\n          Книги и прикладные руководства\n        </span>',
        'Inner Current <br class="hidden sm:inline"/>\n        <span class="bg-gradient-to-r from-amber-400 via-amber-300 to-sky-300 bg-clip-text text-transparent text-glow-amber">\n          Books & Applied Engineering Guides\n        </span>', 1
    )
    content = content.replace(
        'Практическая схемотехника человека: от экспресс-отладки острой боли и перегрузки до прикладной акустики, соматики и синтеза законов физики с природой сознания.',
        'Practical human electrodynamics: from rapid debugging of acute pain and overload to applied acoustics, somatics, and the synthesis of physical laws with the nature of consciousness.', 1
    )
    content = content.replace('<div class="text-xs text-slate-400 mt-0.5 font-medium">Книг и руководств</div>', '<div class="text-xs text-slate-400 mt-0.5 font-medium">Books & Manuals</div>', 1)
    content = content.replace('<div class="text-xs text-slate-400 mt-0.5 font-medium">Страниц текста</div>', '<div class="text-xs text-slate-400 mt-0.5 font-medium">Pages of Text</div>', 1)
    content = content.replace('<div class="text-2xl font-black text-emerald-400 font-mono">3 языка</div>', '<div class="text-2xl font-black text-emerald-400 font-mono">3 Languages</div>', 1)
    content = content.replace('<div class="text-xs text-slate-400 mt-0.5 font-medium">Свободный доступ</div>', '<div class="text-xs text-slate-400 mt-0.5 font-medium">Open Access</div>', 1)

    content = content.replace('<span>📖</span> <span>Онлайн-ридер</span>', '<span>📖</span> <span>Online Reader</span>', 1)
    content = content.replace('<span>🎧</span> <span>Аудиокнига онлайн</span>', '<span>🎧</span> <span>Audiobook Online</span>', 1)
    content = content.replace('<span>📚</span> <span>Обзор всех изданий</span>', '<span>📚</span> <span>Overview of All Books</span>', 1)

    # 7. Books Showcase Header
    content = content.replace('Семь книг библиотеки', 'Seven Books of the Library', 1)
    content = content.replace('Открытый доступ', 'Open Access', 1)
    content = content.replace(
        'Каждое издание решает прикладную задачу: от экстренного снятия соматического напряжения до построения целостной картины мира.',
        'Each edition solves a practical engineering challenge: from emergency release of somatic tension to building an integrated worldview.', 1
    )
    content = content.replace('<span>🎧</span> Аудио-студия ↗', '<span>🎧</span> Audio Studio ↗', 1)

    # Tooltip replacements across all books
    content = content.replace('title="Открыть в отдельной вкладке"', 'title="Open in new tab"')
    content = content.replace('title="Слушать аудиокнигу"', 'title="Listen to audiobook"')
    content = content.replace('title="Скачать PDF (1.5 МБ)"', 'title="Download PDF (1.5 MB)"')
    content = content.replace('title="Скачать PDF (1.1 МБ)"', 'title="Download PDF (1.1 MB)"')
    content = content.replace('title="Скачать PDF (30 стр.)"', 'title="Download PDF (30 pages)"')

    # Book 1: Field Manual
    content = content.replace('Полевой мануал', 'Field Manual', 1)
    content = content.replace('Внутренний ток: Полевой мануал отладки', 'Inner Current: Debugging Field Manual', 1)
    content = content.replace('Практическая инженерия человека: когда горит проводка', 'Practical human engineering: when the wiring burns', 1)
    content = content.replace(
        'Для тех, у кого прямо сейчас перегрузка или острая боль. Экспресс-диагностика 4 аварийных состояний, 5 протоколов помощи (соматический сброс, Black Start, микронагрузка, Мусин), ежедневная профилактика.',
        'For those experiencing acute overload or pain right now. Express diagnostics of 4 emergency states, 5 relief protocols (somatic ground, Black Start, micro-load, Mushin), daily preventative maintenance.', 1
    )
    content = content.replace('📖 Читать в ридере', '📖 Read in Reader', 1)

    # Book 2: Magnum Opus (Canonical)
    content = content.replace('Базовый труд', 'Master Treatise', 1)
    content = content.replace('Внутренний ток: Архитектура счастья', 'Inner Current: The Architecture of Happiness', 1)
    content = content.replace('Физика сверхпроводимости, дзен-онтология и точная инженерия духа', 'Physics of superconductivity, Zen ontology, and exact engineering of the spirit', 1)
    content = content.replace(
        'Полный фундаментальный труд: 22 главы, 850 страниц. Соединение законов электродинамики, дзенской практики, принципов децентрализации и созидательного действия. Доступен на RU, EN, IT.',
        'The complete fundamental treatise: 22 chapters, 850 pages. Synthesis of electrodynamics laws, Zen practice, decentralization principles, and creative action. Available in RU, EN, IT.', 1
    )
    content = content.replace('href="book/index.html" target="_blank"', 'href="../book/en/index.html" target="_blank"')
    content = content.replace('📖 Читать в ридере', '📖 Read in Reader', 1)

    # Book 3: Copernicus
    content = content.replace('Анатомия внимания', 'Attention Anatomy', 1)
    content = content.replace('Коперник Сознания', 'The Copernicus of Consciousness', 1)
    content = content.replace('Анатомия эго и физика внутренней свободы', 'Anatomy of the ego and physics of inner freedom', 1)
    content = content.replace(
        'Почему сопротивление не может быть проводником (<span class="font-mono text-amber-300">I_life ≠ R_ego</span>). Эффект Земмельвейса, акустика дребезжащего колка укулеле и метафора раскалённого угля без мистики и абстракций.',
        'Why resistance cannot be a conductor (<span class="font-mono text-amber-300">I_life ≠ R_ego</span>). Semmelweis effect, acoustics of a rattling ukulele peg, and the hot coal metaphor without mysticism or abstractions.', 1
    )
    content = content.replace('📖 Читать в ридере', '📖 Read in Reader', 1)

    # Book 4: Ukulele
    content = content.replace('Акустика • Соматика', 'Acoustics • Somatics', 1)
    content = content.replace('Укулеле Бытия', 'The Ukulele of Being', 1)
    content = content.replace('Простая акустика гармоничной жизни и искусство чистого звучания', 'Simple acoustics of a harmonious life and the art of pure resonance', 1)
    content = content.replace(
        '400 граммов дерева, 4 струны и принцип открытого звучания. Карманный соматический инструмент сброса внутреннего сопротивления в ноль (<span class="font-mono text-sky-300">R → 0</span>) через слух и тело.',
        '400 grams of wood, 4 strings, and the open resonance principle. A pocket somatic instrument to zero out internal resistance (<span class="font-mono text-sky-300">R → 0</span>) through auditory and body feedback.', 1
    )
    content = content.replace('📖 Читать в ридере', '📖 Read in Reader', 1)

    # Book 5: Primer
    content = content.replace('Праймер • 10+', 'Primer • Ages 10+', 1)
    content = content.replace('Инструкция к твоему суперкостюму', 'Instructions for Your Supersuit', 1)
    content = content.replace('Руководство по физике внутреннего равновесия для подростков', 'A guide to the physics of inner equilibrium for teenagers', 1)
    content = content.replace(
        'Как устроена батарейка внимания, проводка интереса, 6 ламп полезного действия и как защититься от короткого замыкания при стрессе. Схемотехника без занудства.',
        'How the battery of attention is built, the wiring of genuine interest, 6 work bulbs, and how to protect against short circuits during stress. Circuitry without condescension.', 1
    )
    content = content.replace('📖 Читать в ридере', '📖 Read in Reader', 1)

    # Book 6: White Paper
    content = content.replace('Макро-контур', 'Macro-Circuit', 1)
    content = content.replace('Суверенный термодинамический контур духа, ресурсов и общества', 'Sovereign thermodynamic circuit of spirit, resources, and society', 1)
    content = content.replace(
        'Манифест прямого созидательного потока (Zero Parasitic Rent). Структурное соответствие Протокола Биткоина, Единого налога на землю и концепции внутреннего тока.',
        'The direct creative flow manifesto (Zero Parasitic Rent). Structural isomorphism between Bitcoin Protocol, Henry George\'s Single Tax, and the Inner Current framework.', 1
    )
    content = content.replace('📥 Скачать PDF', '📥 Download PDF', 1)

    # Book 7: Great Synthesis
    content = content.replace('Книга VII • Большой синтез', 'Book VII • The Great Synthesis', 1)
    content = content.replace(
        'Великий Синтез: Революции Материи, Трагедия Духа и Электродинамика Человека',
        'The Great Synthesis: Revolutions of Matter, Tragedy of Spirit, and Human Electrodynamics', 1
    )
    content = content.replace(
        'Схождение фундаментальной физики, инженерной истории и устройства сознания',
        'Convergence of fundamental physics, engineering history, and the structure of consciousness', 1
    )
    content = content.replace(
        'Как Коперник, Ньютон, Ватт, Фарадей, Максвелл, Бенц, Циолковский и Сатоши преобразили материю через замкнутые цепи, почему морализаторский кнут в духовных учениях порождал омический перегрев (<span class="font-mono text-amber-300">Q = I² R t</span>), и как электродинамика человека замыкает созидательный ток на реальность (<span class="font-mono text-amber-300">R_ego → 0</span>).',
        'How Copernicus, Newton, Watt, Faraday, Maxwell, Benz, Tsiolkovsky, and Satoshi transformed matter via closed circuits; why the moralistic whip in spiritual teachings caused ohmic overheat (<span class="font-mono text-amber-300">Q = I² R t</span>); and how human electrodynamics closes creative current into reality (<span class="font-mono text-amber-300">R_ego → 0</span>).', 1
    )
    content = content.replace('<span>📖</span> <span>Читать в ридере онлайн</span>', '<span>📖</span> <span>Read Online in Reader</span>', 1)
    content = content.replace('<span>📥</span> PDF книги (30 стр.)', '<span>📥</span> Book PDF (30 pages)', 1)
    content = content.replace('↗ На весь экран', '↗ Fullscreen', 1)

    # 8. Audiobook Quick Player
    content = content.replace('1 ч 00 мин доступно', '1 hr 00 min available', 1)
    content = content.replace('00. Слово к русскому изданию: Русский синтез', '00. Note to the Russian Edition: Russian Synthesis', 1)
    content = content.replace('Голос: Дмитрий Neural • Студийный мастеринг EBU R128 (-16 LUFS)', 'Voice: Dmitry Neural • Studio Mastering EBU R128 (-16 LUFS)', 1)
    content = content.replace('<option value="0">00. Слово к русскому изданию (03:56)</option>', '<option value="0">00. Note to the Russian Edition (03:56)</option>', 1)
    content = content.replace('<option value="1">01. Манифест дзен-инженера (10:31)</option>', '<option value="1">01. Zen Engineer\'s Manifesto (10:31)</option>', 1)
    content = content.replace('<option value="2">02. Предисловие (23:06)</option>', '<option value="2">02. Preface: Physics Saves the Soul (23:06)</option>', 1)
    content = content.replace('<option value="3">03. Введение (23:18)</option>', '<option value="3">03. Introduction: Inner Current Anatomy (23:18)</option>', 1)
    content = content.replace('<option value="4">04. Глава 1.1 — Анатомия тройственности (08:58)</option>', '<option value="4">04. Ch. 1.1 — Anatomy of Triplicity (08:58)</option>', 1)
    content = content.replace('<span>🎧</span> <span>Полная студия ↗</span>', '<span>🎧</span> <span>Full Studio ↗</span>', 1)

    # 9. Embedded Reader section
    content = content.replace('Ридер:', 'Reader:', 1)
    content = content.replace('🧰 Полевой мануал', '🧰 Field Manual', 1)
    content = content.replace('🏛 Архитектура счастья', '🏛 Architecture of Happiness', 1)
    content = content.replace('🪞 Коперник Сознания', '🪞 Copernicus', 1)
    content = content.replace('🎸 Укулеле Бытия', '🎸 Ukulele of Being', 1)
    content = content.replace('🧒 Праймер', '🧒 Primer', 1)
    content = content.replace('👑 Великий Синтез', '👑 Great Synthesis', 1)
    content = content.replace('<span>↗</span> <span>На весь экран</span>', '<span>↗</span> <span>Fullscreen</span>', 1)
    content = content.replace('title="Онлайн-Ридер: Внутренний ток"', 'title="Online Reader: Inner Current"', 1)

    # 10. Monographs section
    content = content.replace('Тематические материалы и памятки', 'Thematic Materials and Special Issues', 1)
    content = content.replace('Отдельные прикладные документы, памятки и брошюры библиотеки.', 'Stand-alone applied documents, field guides, and brochures from the library.', 1)
    content = content.replace('Материал • PDF', 'Document • PDF', 1)
    content = content.replace('183. Итальянский триптих сверхпроводимости', '183. Italian Triptych of Superconductivity', 1)
    content = content.replace('Ольфакторно-акустический байпас неокортекса. Триада Versace и Леванте.', 'Olfactory-acoustic bypass of neocortex. Versace and Levante triad.', 1)
    content = content.replace('Памятка • PDF', 'Guide • PDF', 1)
    content = content.replace('Переход в эпоху Автомобиля (1886–2026)', 'Transition to the Era of the Automobile (1886–2026)', 1)
    content = content.replace('Трилогия Карла Бенца. Изобретение двигателя внутреннего сгорания как аналог электродинамики внимания.', 'Karl Benz Trilogy. Internal combustion engine as analogue to attention electrodynamics.', 1)
    content = content.replace('Брошюра • PDF', 'Brochure • PDF', 1)
    content = content.replace('Триптих Сверхпроводимости — Леванте', 'Triptych of Superconductivity — Levante', 1)
    content = content.replace('Леванте и Внутренний ток: физика созидательного действия и устранение паразитных звеньев.', 'Levante and Inner Current: physics of creative action and eliminating parasitic links.', 1)
    content = content.replace('<span>📥</span> Скачать PDF', '<span>📥</span> Download PDF')

    # 11. Flashlight section
    content = content.replace('ИНТЕРАКТИВНАЯ СХЕМОТЕХНИКА', 'INTERACTIVE CIRCUIT DIAGRAM', 1)
    content = content.replace('Дзен-фонарик: 5 элементов цепи', 'Zen Flashlight: 5 Elements of the Circuit', 1)
    content = content.replace(
        'Счастье и сознание подчиняются законам замкнутой электрической цепи. Попробуйте нажать кнопку «Хоцу», чтобы пустить ток «Мусин» через предохранитель «Дзансин» и зажечь лампочку «Гё»!',
        'Happiness and consciousness obey the laws of a closed electric circuit. Try toggling the "Hotsu" button to send "Mushin" current through the "Zanshin" fuse and illuminate the "Gyo" bulb!', 1
    )
    content = content.replace('<span>🔦</span> Страница фонарика ↗', '<span>🔦</span> Flashlight Page ↗', 1)
    content = content.replace('<span>🧘</span> Человек-контур ↗', '<span>🧘</span> Human Circuit ↗', 1)
    content = content.replace('Живой стенд цепи', 'Live Circuit Workbench', 1)
    content = content.replace('Замкнутый контур &bull; Чистый ток', 'Closed Loop &bull; Pure Current', 1)
    content = content.replace('Кнопка «Хоцу» нажата', 'Hotsu Button Pressed (ON)', 1)
    content = content.replace('Ток «Мусин» зажигает «Гё»!', 'Mushin Current Illuminates Gyo!', 1)
    content = content.replace('⚡ «Хоцу» замкнута: Ток Мусин (無心) течёт, лампочка Гё (行) сияет!', '⚡ Hotsu Closed: Mushin Current (無心) Flows, Gyo Bulb (行) Shines!', 1)

    # Flashlight SVG Labels
    content = content.replace('КАНСО: ЧИСТАЯ АРХИТЕКТУРА', 'KANSO: PURE ARCHITECTURE')
    content = content.replace('ТАНДЭН (丹田)', 'TANDEN (丹田)')
    content = content.replace('Батарейка • Ядро', 'Battery • Core')
    content = content.replace('ХОЦУ (発) — ЗАМКНУТО', 'HOTSU (発) — CLOSED')
    content = content.replace('Кнопка толкает контакт (ВКЛ)', 'Button pushes contact (ON)')
    content = content.replace('МУСИН (無心) — Ток', 'MUSHIN (無心) — Flow')
    content = content.replace('Чистый поток внимания', 'Pure attention current')
    content = content.replace('ГЁ (行) — Лампочка', 'GYO (行) — Light Bulb')
    content = content.replace('Действие & Плод света', 'Action & Fruit of Light')
    content = content.replace('ДЗАНСИН (残心)', 'ZANSHIN (残心)')
    content = content.replace('Предохранитель (Защита)', 'Fuse (Safeguard)')
    content = content.replace('👆 Нажимайте кнопку «Хоцу», чтобы пустить ток, или выбирайте карточки элементов ниже!', '👆 Toggle the "Hotsu" button to start the current, or select element cards below!', 1)

    # Flashlight initial elementCard state
    content = content.replace(
        '<span id="elemRankTag" class="text-xs font-black px-2.5 py-0.5 rounded-full bg-amber-500 text-slate-950 uppercase tracking-wide">\n                Элемент №1\n              </span>',
        '<span id="elemRankTag" class="text-xs font-black px-2.5 py-0.5 rounded-full bg-amber-500 text-slate-950 uppercase tracking-wide">\n                Element #1\n              </span>', 1
    )
    content = content.replace(
        '<h3 id="elemHeaderTitle" class="text-base sm:text-lg font-black text-slate-100">\n                1. Тандэн (丹田) — Батарейка (Ядро энергии)\n              </h3>',
        '<h3 id="elemHeaderTitle" class="text-base sm:text-lg font-black text-slate-100">\n                1. Tanden (丹田) — Battery (Energy Core)\n              </h3>', 1
    )
    content = content.replace(
        'Тандэн — источник всей жизненной силы цепи. В фонарике это батарейка: автономное ядро энергии. В покое хранит 100% заряда в чистой тишине, не растрачивая ни микроватта вхолостую.',
        'Tanden is the source of all vital power in the circuit. In the flashlight, this is the battery: an autonomous energy core. At rest, it holds 100% charge in pure silence without wasting a single microwatt in vain.', 1
    )
    content = content.replace(
        '<span>✨ Детское объяснение: Волшебная кладовая силы, где спокойно отдыхает вся энергия фонарика!</span>',
        '<span>✨ Child\'s explanation: The magical treasure-room of power where all the flashlight\'s energy rests peacefully!</span>', 1
    )

    # Flashlight 5 button titles
    content = content.replace('<span class="text-xs font-black text-slate-100">1. Тандэн (丹田)</span>', '<span class="text-xs font-black text-slate-100">1. Tanden (丹田)</span>')
    content = content.replace('<span class="text-[11px] text-slate-400 font-medium">Батарейка</span>', '<span class="text-[11px] text-slate-400 font-medium">Battery</span>')
    content = content.replace('<span class="text-xs font-black text-slate-100">2. Хоцу (発)</span>', '<span class="text-xs font-black text-slate-100">2. Hotsu (発)</span>')
    content = content.replace('<span class="text-[11px] text-slate-400 font-medium">Кнопка «Хочу»</span>', '<span class="text-[11px] text-slate-400 font-medium">"I Want" Switch</span>')
    content = content.replace('<span class="text-xs font-black text-slate-100">3. Мусин (無心)</span>', '<span class="text-xs font-black text-slate-100">3. Mushin (無心)</span>')
    content = content.replace('<span class="text-[11px] text-slate-400 font-medium">Чистый ток</span>', '<span class="text-[11px] text-slate-400 font-medium">Pure Current</span>')
    content = content.replace('<span class="text-xs font-black text-slate-100">4. Гё (行)</span>', '<span class="text-xs font-black text-slate-100">4. Gyo (行)</span>')
    content = content.replace('<span class="text-[11px] text-slate-400 font-medium">Лампочка (Свет)</span>', '<span class="text-[11px] text-slate-400 font-medium">Light Bulb (Action)</span>')
    content = content.replace('<span class="text-xs font-black text-slate-100">5. Дзансин (残心)</span>', '<span class="text-xs font-black text-slate-100">5. Zanshin (残心)</span>')
    content = content.replace('<span class="text-[11px] text-slate-400 font-medium">Предохранитель</span>', '<span class="text-[11px] text-slate-400 font-medium">Fuse (Safeguard)</span>')

    # 12. Principles section
    content = content.replace('⚡ ОСНОВЫ КОНТУРА', '⚡ CIRCUIT BASICS', 1)
    content = content.replace('Пять принципов Внутреннего тока', 'Five Principles of the Inner Current', 1)
    content = content.replace('Прикладная дзен-инженерия, точная схемотехника и снятие паразитного сопротивления.', 'Applied Zen engineering, precise circuitry, and elimination of parasitic resistance.', 1)
    content = content.replace('<h4 class="text-sm font-bold text-slate-100">Тандэн (丹田)</h4>', '<h4 class="text-sm font-bold text-slate-100">Tanden (丹田)</h4>', 1)
    content = content.replace('<h4 class="text-sm font-bold text-slate-100">Мусин (無心)</h4>', '<h4 class="text-sm font-bold text-slate-100">Mushin (無心)</h4>', 1)
    content = content.replace('<h4 class="text-sm font-bold text-slate-100">Хоцу (発)</h4>', '<h4 class="text-sm font-bold text-slate-100">Hotsu (発)</h4>', 1)
    content = content.replace('<h4 class="text-sm font-bold text-slate-100">Дзансин (残心)</h4>', '<h4 class="text-sm font-bold text-slate-100">Zanshin (残心)</h4>', 1)
    content = content.replace('<h4 class="text-sm font-bold text-slate-100">Гё (行)</h4>', '<h4 class="text-sm font-bold text-slate-100">Gyo (行)</h4>', 1)
    content = content.replace('Автономный внутренний источник. Ресурс созидания, независимый от внешних оценок.', 'Autonomous inner source. Resource of creation independent of external validation.', 1)
    content = content.replace('Бесшовный поток внимания без паразитных омических потерь и самосуда.', 'Seamless flow of attention without parasitic ohmic losses or self-judgment.', 1)
    content = content.replace('Чистый импульс воли. Замыкание цепи через непосредственное желание действовать без внутреннего насилия.', 'Pure impulse of will. Closing the circuit through immediate desire to act without internal coercion.', 1)
    content = content.replace('Внимательность и автоматический предохранитель при перегрузке (Circuit Breaker).', 'Vigilant awareness and automatic protection during overload (Circuit Breaker).', 1)
    content = content.replace('Полезная работа: перевод внутреннего ресурса в осязаемый результат в реальном мире.', 'Useful work: transforming internal energy into tangible impact in the physical world.', 1)

    # 13. Footer
    content = content.replace('Открытая библиотека материалов по архитектуре состояния • innercurrent.ru', 'Open library of state architecture and human engineering • innercurrent.ru', 1)
    content = content.replace('Лицензия MIT (Open Source)', 'MIT License (Open Source)', 1)
    content = content.replace('<a href="#books" class="hover:text-amber-300 transition">Книги</a>', '<a href="#books" class="hover:text-amber-300 transition">Books</a>', 1)
    content = content.replace('<a href="#audiobook" class="hover:text-cyan-300 transition">Аудиокнига</a>', '<a href="#audiobook" class="hover:text-cyan-300 transition">Audiobook</a>', 1)
    content = content.replace('Студия ↗', 'Studio ↗', 1)
    content = content.replace(
        '<a href="/en/" onclick="localStorage.setItem(\'inner_current_lang\',\'en\')" class="text-amber-400 hover:underline">English Version ↗</a>',
        '<a href="/" onclick="localStorage.setItem(\'inner_current_lang\',\'ru\')" class="text-amber-400 hover:underline">Русская версия ↗</a>', 1
    )

    # 14. Fix relative links for /en/ subfolder
    content = content.replace('href="audiobook/index.html"', 'href="../audiobook/index.html"')
    content = content.replace('href="book/index.html"', 'href="../book/en/index.html"')
    content = content.replace('href="books/', 'href="../books/')
    content = content.replace('href="/flashlight/"', 'href="/en/flashlight/"')
    content = content.replace('src="books/field_manual.html"', 'src="../book/en/index.html"')

    # 15. JS logic updates for English
    old_js_bookmap = """    const bookSrcMap = {
      'field_manual': 'books/field_manual.html',
      'canonical': 'book/index.html',
      'copernicus': 'books/copernicus.html',
      'ukulele': 'books/ukulele.html',
      'primer': 'books/primer.html',
      'great_synthesis': 'books/great_synthesis.html'
    };"""
    new_js_bookmap = """    const bookSrcMap = {
      'canonical': '../book/en/index.html',
      'field_manual': '../books/field_manual.html',
      'copernicus': '../books/copernicus.html',
      'ukulele': '../books/ukulele.html',
      'primer': '../books/primer.html',
      'great_synthesis': '../books/great_synthesis.html'
    };"""
    if old_js_bookmap in content:
        content = content.replace(old_js_bookmap, new_js_bookmap, 1)

    # Audio tracks relative paths & titles
    content = content.replace("src: 'audio/", "src: '../audio/")
    content = content.replace("title: '00. Слово к русскому изданию: Русский синтез'", "title: '00. Note to the Russian Edition: Russian Synthesis'")
    content = content.replace("title: '01. Манифест дзен-инженера: Электродинамика сознания'", "title: '01. The Zen Engineer Manifesto: Consciousness Electrodynamics'")
    content = content.replace("title: '02. Предисловие: Как физика спасает душу'", "title: '02. Preface: How Physics Saves the Soul'")
    content = content.replace("title: '03. Введение: Анатомия внутреннего тока'", "title: '03. Introduction: Anatomy of the Inner Current'")
    content = content.replace("title: '04. Глава 1.1 — Анатомия тройственности'", "title: '04. Ch. 1.1 — Anatomy of Triplicity'")

    # Zen Elements translations in JS
    old_zen_elements = """    const zenElements = {
      tanden: {
        rank: "Элемент №1",
        emoji: "🔋",
        title: "1. Тандэн (丹田) — Батарейка (Ядро энергии)",
        desc: "Тандэн — источник всей жизненной силы цепи. В фонарике это батарейка: автономное ядро энергии. В покое хранит 100% заряда в чистой тишине, не растрачивая ни микроватта вхолостую.",
        analogy: "✨ Детское объяснение: Волшебная кладовая силы, где спокойно отдыхает вся энергия фонарика!",
        badgeClass: "bg-amber-500 text-slate-950"
      },
      hotsu: {
        rank: "Элемент №2",
        emoji: "🔘",
        title: "2. Хоцу (発 / Хочу) — Кнопка воли и желания",
        desc: "Хоцу — это священное «Хочу»! По умолчанию выключатель разомкнут (Normally Open), чтобы беречь силы. Как только рождается искреннее живое желание действовать (а не рабское «надо») — кнопка замыкает цепь!",
        analogy: "✨ Детское объяснение: Кнопка-рубильник: искренне захотел — нажал пальчиком и открыл ворота для тока!",
        badgeClass: "bg-emerald-500 text-slate-950"
      },
      mushin: {
        rank: "Элемент №3",
        emoji: "⚡",
        title: "3. Мусин (無心) — Чистый ток (Поток внимания)",
        desc: "Мусин — это чистый электрический ток со скоростью света! Он пробуждается ТОЛЬКО когда нажата кнопка «Хоцу». В нём нет трения эго, сомнений, страха оценки и самоедства: он свободен, быстр и прямодушен.",
        analogy: "✨ Детское объяснение: Быстрая река электричества, которая мчится по проводам, как только нажали кнопку!",
        badgeClass: "bg-orange-500 text-white"
      },
      gyo: {
        rank: "Элемент №4",
        emoji: "💡",
        title: "4. Гё (行) — Лампочка (Полезное действие)",
        desc: "Гё — это конкретное созидательное действие в реальном физическом мире (труд, творчество, код, спорт, помощь). Ток Мусин входит в лампочку Гё и рождает яркий видимый свет, разгоняющий тьму!",
        analogy: "✨ Детское объяснение: Сердце света! Маленькая звёздочка, которая сияет, когда через неё бежит ток!",
        badgeClass: "bg-yellow-400 text-slate-950"
      },
      zanshin: {
        rank: "Элемент №5",
        emoji: "🛡️",
        title: "5. Дзансин (残心) — Предохранитель (Защита духа)",
        desc: "Дзансин — это бдительность мастера и защита контура (Circuit Breaker). Стоит на страже на обратном проводе. Если лампа в мире перегорит или задача сорвётся — Дзансин отсекает аварию и спасает батарейку Тандэна от выгорания.",
        analogy: "✨ Детское объяснение: Верный страж-телохранитель, который бережёт батарейку от замыкания и поломки!",
        badgeClass: "bg-sky-500 text-slate-950"
      }
    };"""

    new_zen_elements = """    const zenElements = {
      tanden: {
        rank: "Element #1",
        emoji: "🔋",
        title: "1. Tanden (丹田) — Battery (Energy Core)",
        desc: "Tanden is the source of all vital power in the circuit. In the flashlight, this is the battery: an autonomous energy core. At rest, it holds 100% charge in pure silence without wasting a single microwatt in vain.",
        analogy: "✨ Child's explanation: The magical treasure-room of power where all the flashlight's energy rests peacefully!",
        badgeClass: "bg-amber-500 text-slate-950"
      },
      hotsu: {
        rank: "Element #2",
        emoji: "🔘",
        title: "2. Hotsu (発) — Switch of Will & Desire",
        desc: "Hotsu is the sacred 'I want'! By default, the switch is Normally Open to conserve power. As soon as a sincere living desire to act is born (rather than servile moral duty) — the button closes the circuit!",
        analogy: "✨ Child's explanation: The power switch: when you truly want something, press the button and open the gate for the current!",
        badgeClass: "bg-emerald-500 text-slate-950"
      },
      mushin: {
        rank: "Element #3",
        emoji: "⚡",
        title: "3. Mushin (無心) — Pure Current (Flow of Attention)",
        desc: "Mushin is pure electric current traveling at the speed of light! It awakes ONLY when the Hotsu button is pressed. It carries zero ego friction, zero doubt, zero evaluation anxiety: it is free, swift, and direct.",
        analogy: "✨ Child's explanation: A swift river of electricity racing through wires the moment the button is pressed!",
        badgeClass: "bg-orange-500 text-white"
      },
      gyo: {
        rank: "Element #4",
        emoji: "💡",
        title: "4. Gyo (行) — Light Bulb (Constructive Action)",
        desc: "Gyo is concrete constructive action in physical reality (work, art, code, sport, assistance). Mushin current enters the Gyo bulb and produces bright visible light, banishing darkness!",
        analogy: "✨ Child's explanation: The heart of light! A glowing star that radiates whenever current runs through it!",
        badgeClass: "bg-yellow-400 text-slate-950"
      },
      zanshin: {
        rank: "Element #5",
        emoji: "🛡️",
        title: "5. Zanshin (残心) — Fuse (Safeguard)",
        desc: "Zanshin is the master's vigilance and circuit breaker. Standing guard on the return wire. If the light bulb in the world burns out or an action fails — Zanshin breaks the circuit, saving the Tanden battery from burnout.",
        analogy: "✨ Child's explanation: The faithful bodyguard protecting the battery from shorts and breakdowns!",
        badgeClass: "bg-sky-500 text-slate-950"
      }
    };"""

    if old_zen_elements in content:
        content = content.replace(old_zen_elements, new_zen_elements, 1)

    # In toggleHotsu() JS:
    content = content.replace("badgeTitle.textContent = 'ХОЦУ (発) — ЗАМКНУТО';", "badgeTitle.textContent = 'HOTSU (発) — CLOSED';")
    content = content.replace("badgeDesc.textContent = 'Кнопка толкает контакт (ВКЛ)';", "badgeDesc.textContent = 'Button pushes contact (ON)';")
    content = content.replace("statusLabel.textContent = '⚡ Кнопка «Хоцу» ЗЕЛЁНАЯ (замкнута): Ток Мусин бежит, лампочка Гё сияет!';", "statusLabel.textContent = '⚡ Hotsu button GREEN (closed): Mushin current flows, Gyo bulb shines!';")
    content = content.replace("stateBadge.textContent = 'Кнопка «Хоцу» замкнута (ВКЛ)';", "stateBadge.textContent = 'Hotsu button closed (ON)';")
    content = content.replace("btnSub.textContent = 'Ток «Мусин» зажигает «Гё»!';", "btnSub.textContent = 'Mushin current illuminates Gyo!';")

    content = content.replace("badgeTitle.textContent = 'ХОЦУ (発) — РАЗОМКНУТО';", "badgeTitle.textContent = 'HOTSU (発) — OPEN';")
    content = content.replace("badgeDesc.textContent = 'Контакт разомкнут (ВЫКЛ)';", "badgeDesc.textContent = 'Contact released (OFF)';")
    content = content.replace("statusLabel.textContent = '💤 Кнопка «Хоцу» КРАСНАЯ (разомкнута): Контакт отжат, ток Мусин спит';", "statusLabel.textContent = '💤 Hotsu button RED (open): Contact open, Mushin current is resting';")
    content = content.replace("stateBadge.textContent = 'Кнопка «Хоцу» разомкнута (ВЫКЛ)';", "stateBadge.textContent = 'Hotsu button open (OFF)';")
    content = content.replace("btnSub.textContent = 'Нажмите «Хоцу», чтобы пустить ток!';", "btnSub.textContent = 'Click Hotsu to start current!';")

    # Set default reader tab to canonical (Architecture of Happiness in EN)
    content = content.replace(
        """          <button id="rbtn-field_manual" onclick="readBookInReader('field_manual')" class="px-3.5 py-2 rounded-xl text-xs font-semibold transition cursor-pointer bg-amber-500 text-slate-950 font-bold shrink-0">
            🧰 Field Manual
          </button>
          <button id="rbtn-canonical" onclick="readBookInReader('canonical')" class="px-3.5 py-2 rounded-xl text-xs font-semibold transition cursor-pointer bg-slate-800 text-slate-300 hover:text-white shrink-0">
            🏛 Architecture of Happiness
          </button>""",
        """          <button id="rbtn-canonical" onclick="readBookInReader('canonical')" class="px-3.5 py-2 rounded-xl text-xs font-semibold transition cursor-pointer bg-amber-500 text-slate-950 font-bold shrink-0">
            🏛 Architecture of Happiness
          </button>
          <button id="rbtn-field_manual" onclick="readBookInReader('field_manual')" class="px-3.5 py-2 rounded-xl text-xs font-semibold transition cursor-pointer bg-slate-800 text-slate-300 hover:text-white shrink-0">
            🧰 Field Manual
          </button>"""
    )
    content = content.replace('href="books/field_manual.html"', 'href="../book/en/index.html"')

    # Write out
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated {out_path}")

    shutil.copyfile(out_path, os.path.join(DIST_DIR, "en.html"))
    print("Copied to dist_site/en.html")

def generate_en_flashlight():
    base_path = os.path.join(DIST_DIR, "flashlight.html")
    with open(base_path, "r", encoding="utf-8") as f:
        content = f.read()

    content = content.replace('<html lang="ru"', '<html lang="en"', 1)
    content = content.replace(
        '<title>Дзен-фонарик: Канон 5 первоэлементов — Inner Current</title>',
        '<title>Zen Flashlight: Canon of the 5 Primal Elements — Inner Current</title>', 1
    )
    content = content.replace(
        '<meta name="description" content="Интерактивная схемотехника фонарика: Тандэн (батарейка), Хоцу (кнопка воли), Мусин (электрический ток), Дзансин (предохранитель) и Гё (лампочка).">',
        '<meta name="description" content="Interactive flashlight circuitry: Tanden (battery), Hotsu (will button), Mushin (electric current), Zanshin (fuse), and Gyo (light bulb).">', 1
    )
    content = content.replace('Библиотека книг &bull; Канон', 'Library of Books &bull; Canon', 1)

    en_switcher = """      <div class="flex items-center gap-3">
        <!-- Language Switcher -->
        <div class="flex items-center rounded-xl bg-slate-900 border border-slate-800 p-0.5 text-xs font-mono font-semibold" title="Language selection">
          <a href="/flashlight/" onclick="localStorage.setItem('inner_current_lang','ru')" class="px-2.5 py-1 rounded-lg text-slate-400 hover:text-slate-100 hover:bg-slate-800/80 transition">RU</a>
          <span class="px-2.5 py-1 rounded-lg bg-amber-500 text-slate-950 font-bold shadow-sm cursor-default">EN</span>
        </div>"""
    ru_switcher_search = """      <div class="flex items-center gap-3">
        <!-- Language Switcher -->
        <div class="flex items-center rounded-xl bg-slate-900 border border-slate-800 p-0.5 text-xs font-mono font-semibold" title="Выбор языка / Language selection">
          <span class="px-2.5 py-1 rounded-lg bg-amber-500 text-slate-950 font-bold shadow-sm cursor-default">RU</span>
          <a href="/en/flashlight/" onclick="localStorage.setItem('inner_current_lang','en')" class="px-2.5 py-1 rounded-lg text-slate-400 hover:text-slate-100 hover:bg-slate-800/80 transition">EN</a>
        </div>"""
    if ru_switcher_search in content:
        content = content.replace(ru_switcher_search, en_switcher, 1)

    content = content.replace('<span class="hidden sm:inline">Человек-контур</span>', '<span class="hidden sm:inline">Human Circuit</span>', 1)
    content = content.replace('<span>←</span> На главную', '<span>←</span> Home', 1)
    content = content.replace('href="/"', 'href="/en/"')
    content = content.replace('href="/human/"', 'href="/en/human/"')

    # Header
    content = content.replace('КАНОН КАНСО: 5 ЭЛЕМЕНТОВ ЦЕПИ', 'KANSO CANON: 5 ELEMENTS OF THE CIRCUIT', 1)
    content = content.replace('Дзен-фонарик и физика сознания', 'Zen Flashlight & Consciousness Physics', 1)
    content = content.replace(
        'Наглядная детская и инженерная схемотехника: как устроен фонарик и почему счастье и поток подчиняются законам замкнутой электрической цепи.',
        'Intuitive child and engineering circuitry: how a flashlight works and why happiness and flow obey the laws of a closed electric circuit.', 1
    )
    content = content.replace('<span>🔦</span> Горизонтальная схема фонарика', '<span>🔦</span> Horizontal Flashlight Circuit', 1)
    content = content.replace('<span>🧘</span> Вертикальная схема человека', '<span>🧘</span> Vertical Human Circuit', 1)

    # Widget & SVG
    content = content.replace('Схемотехнический макет', 'Circuit Workbench', 1)
    content = content.replace('Замкнутый контур &bull; Чистый ток', 'Closed Loop &bull; Pure Current', 1)
    content = content.replace('Кнопка «Хоцу» нажата', 'Hotsu Button Pressed (ON)', 1)
    content = content.replace('Ток «Мусин» зажигает «Гё»!', 'Mushin Current Illuminates Gyo!', 1)
    content = content.replace('⚡ «Хоцу» замкнута: Ток Мусин (無心) течёт, лампочка Гё (行) сияет!', '⚡ Hotsu Closed: Mushin Current (無心) Flows, Gyo Bulb (行) Shines!', 1)

    content = content.replace('КАНСО: ЧИСТАЯ АРХИТЕКТУРА', 'KANSO: PURE ARCHITECTURE')
    content = content.replace('ТАНДЭН (丹田)', 'TANDEN (丹田)')
    content = content.replace('Батарейка • Ядро', 'Battery • Core')
    content = content.replace('ХОЦУ (発) — ЗАМКНУТО', 'HOTSU (発) — CLOSED')
    content = content.replace('Кнопка толкает контакт (ВКЛ)', 'Button pushes contact (ON)')
    content = content.replace('МУСИН (無心) — Ток', 'MUSHIN (無心) — Flow')
    content = content.replace('Чистый поток внимания', 'Pure attention current')
    content = content.replace('ГЁ (行) — Лампочка', 'GYO (行) — Light Bulb')
    content = content.replace('Действие & Плод света', 'Action & Fruit of Light')
    content = content.replace('ДЗАНСИН (残心)', 'ZANSHIN (残心)')
    content = content.replace('Предохранитель (Защита)', 'Fuse (Safeguard)')
    content = content.replace('👆 Нажимайте кнопку «Хоцу», чтобы пустить ток, или выбирайте карточки элементов ниже!', '👆 Toggle the "Hotsu" button to start the current, or select element cards below!', 1)

    # Flashlight elementCard initial state
    content = content.replace(
        '<span id="elemRankTag" class="text-xs font-black px-2.5 py-0.5 rounded-full bg-amber-500 text-slate-950 uppercase tracking-wide">\n                Элемент №1\n              </span>',
        '<span id="elemRankTag" class="text-xs font-black px-2.5 py-0.5 rounded-full bg-amber-500 text-slate-950 uppercase tracking-wide">\n                Element #1\n              </span>', 1
    )
    content = content.replace(
        '<h3 id="elemHeaderTitle" class="text-base sm:text-lg font-black text-slate-100">\n                1. Тандэн (丹田) — Батарейка (Ядро энергии)\n              </h3>',
        '<h3 id="elemHeaderTitle" class="text-base sm:text-lg font-black text-slate-100">\n                1. Tanden (丹田) — Battery (Energy Core)\n              </h3>', 1
    )
    content = content.replace(
        'Тандэн — источник всей жизненной силы цепи. В фонарике это батарейка: автономное ядро энергии. В покое хранит 100% заряда в чистой тишине, не растрачивая ни микроватта вхолостую.',
        'Tanden is the source of all vital power in the circuit. In the flashlight, this is the battery: an autonomous energy core. At rest, it holds 100% charge in pure silence without wasting a single microwatt in vain.', 1
    )
    content = content.replace(
        '<span>✨ Детское объяснение: Волшебная кладовая силы, где спокойно отдыхает вся энергия фонарика!</span>',
        '<span>✨ Child\'s explanation: The magical treasure-room of power where all the flashlight\'s energy rests peacefully!</span>', 1
    )

    # Flashlight 5 button titles
    content = content.replace('<span class="text-xs font-black text-slate-100">1. Тандэн (丹田)</span>', '<span class="text-xs font-black text-slate-100">1. Tanden (丹田)</span>')
    content = content.replace('<span class="text-[11px] text-slate-400 font-medium">Батарейка</span>', '<span class="text-[11px] text-slate-400 font-medium">Battery</span>')
    content = content.replace('<span class="text-xs font-black text-slate-100">2. Хоцу (発)</span>', '<span class="text-xs font-black text-slate-100">2. Hotsu (発)</span>')
    content = content.replace('<span class="text-[11px] text-slate-400 font-medium">Кнопка «Хочу»</span>', '<span class="text-[11px] text-slate-400 font-medium">"I Want" Switch</span>')
    content = content.replace('<span class="text-xs font-black text-slate-100">3. Мусин (無心)</span>', '<span class="text-xs font-black text-slate-100">3. Mushin (無心)</span>')
    content = content.replace('<span class="text-[11px] text-slate-400 font-medium">Чистый ток</span>', '<span class="text-[11px] text-slate-400 font-medium">Pure Current</span>')
    content = content.replace('<span class="text-xs font-black text-slate-100">4. Гё (行)</span>', '<span class="text-xs font-black text-slate-100">4. Gyo (行)</span>')
    content = content.replace('<span class="text-[11px] text-slate-400 font-medium">Лампочка (Свет)</span>', '<span class="text-[11px] text-slate-400 font-medium">Light Bulb (Action)</span>')
    content = content.replace('<span class="text-xs font-black text-slate-100">5. Дзансин (残心)</span>', '<span class="text-xs font-black text-slate-100">5. Zanshin (残心)</span>')
    content = content.replace('<span class="text-[11px] text-slate-400 font-medium">Предохранитель</span>', '<span class="text-[11px] text-slate-400 font-medium">Fuse (Safeguard)</span>')

    # Theory cards
    content = content.replace('<span>🧠</span> Почему фонарик объясняет счастье?', '<span>🧠</span> Why does a flashlight explain happiness?', 1)
    content = content.replace(
        'Большинство людей живут с разомкнутой цепью: они требуют от лампочки (Гё) света, не включая кнопку собственного намерения (Хоцу), либо выжигают контур без предохранителя (Дзансин), забывая подпитывать автономный Тандэн. Фонарик напоминает: счастье — это не статичная вещь, а <strong>динамический ток в замкнутом контуре</strong>.',
        'Most people live with an open circuit: they demand light from the bulb (Gyo) without engaging their own genuine intention switch (Hotsu), or they burn out the circuit without a fuse (Zanshin), forgetting to nourish the autonomous Tanden core. The flashlight reminds us: happiness is not a static object, but <strong>dynamic current in a closed loop</strong>.', 1
    )
    content = content.replace('<span>📖</span> Где читать подробнее?', '<span>📖</span> Where to read more?', 1)
    content = content.replace(
        'Этот изоморфизм подробно раскрыт в книге <a href="/#books" class="text-amber-400 underline font-semibold hover:text-amber-300">«Коперник Сознания»</a> и полевом руководстве <a href="/books/field_manual.html" class="text-cyan-400 underline font-semibold hover:text-cyan-300">«Внутренний ток: Полевой мануал отладки»</a>, доступных в открытой библиотеке проекта.',
        'This isomorphism is explored in depth in the book <a href="/en/#books" class="text-amber-400 underline font-semibold hover:text-amber-300">"The Copernicus of Consciousness"</a> and the field guide <a href="../books/field_manual.html" class="text-cyan-400 underline font-semibold hover:text-cyan-300">"Inner Current: Debugging Field Manual"</a>, available in the open library.', 1
    )

    # Footer
    content = content.replace('Inner Current &bull; Архитектура внутреннего состояния', 'Inner Current &bull; Architecture of Inner State', 1)
    content = content.replace('Главная', 'Home', 1)
    content = content.replace('Книги', 'Books', 1)
    content = content.replace('Ридер', 'Reader', 1)

    # JS Zen Elements
    old_zen_elements = """    const zenElements = {
      tanden: {
        rank: "Элемент №1",
        emoji: "🔋",
        title: "1. Тандэн (丹田) — Батарейка (Ядро энергии)",
        desc: "Тандэн — источник всей жизненной силы цепи. В фонарике это батарейка: автономное ядро энергии. В покое хранит 100% заряда в чистой тишине, не растрачивая ни микроватта вхолостую.",
        analogy: "✨ Детское объяснение: Волшебная кладовая силы, где спокойно отдыхает вся энергия фонарика!",
        badgeClass: "bg-amber-500 text-slate-950"
      },
      hotsu: {
        rank: "Элемент №2",
        emoji: "🔘",
        title: "2. Хоцу (発 / Хочу) — Кнопка воли и желания",
        desc: "Хоцу — это священное «Хочу»! По умолчанию выключатель разомкнут (Normally Open), чтобы беречь силы. Как только рождается искреннее живое желание действовать (а не рабское «надо») — кнопка замыкает цепь!",
        analogy: "✨ Детское объяснение: Кнопка-рубильник: искренне захотел — нажал пальчиком и открыл ворота для тока!",
        badgeClass: "bg-emerald-500 text-slate-950"
      },
      mushin: {
        rank: "Элемент №3",
        emoji: "⚡",
        title: "3. Мусин (無心) — Чистый ток (Поток внимания)",
        desc: "Мусин — это чистый электрический ток со скоростью света! Он пробуждается ТОЛЬКО когда нажата кнопка «Хоцу». В нём нет трения эго, сомнений, страха оценки и самоедства: он свободен, быстр и прямодушен.",
        analogy: "✨ Детское объяснение: Быстрая река электричества, которая мчится по проводам, как только нажали кнопку!",
        badgeClass: "bg-orange-500 text-white"
      },
      gyo: {
        rank: "Элемент №4",
        emoji: "💡",
        title: "4. Гё (行) — Лампочка (Полезное действие)",
        desc: "Гё — это конкретное созидательное действие в реальном физическом мире (труд, творчество, код, спорт, помощь). Ток Мусин входит в лампочку Гё и рождает яркий видимый свет, разгоняющий тьму!",
        analogy: "✨ Детское объяснение: Сердце света! Маленькая звёздочка, которая сияет, когда через неё бежит ток!",
        badgeClass: "bg-yellow-400 text-slate-950"
      },
      zanshin: {
        rank: "Элемент №5",
        emoji: "🛡️",
        title: "5. Дзансин (残心) — Предохранитель (Защита духа)",
        desc: "Дзансин — это бдительность мастера и защита контура (Circuit Breaker). Стоит на страже на обратном проводе. Если лампа в мире перегорит или задача сорвётся — Дзансин отсекает аварию и спасает батарейку Тандэна от выгорания.",
        analogy: "✨ Детское объяснение: Верный страж-телохранитель, который бережёт батарейку от замыкания и поломки!",
        badgeClass: "bg-sky-500 text-slate-950"
      }
    };"""

    new_zen_elements = """    const zenElements = {
      tanden: {
        rank: "Element #1",
        emoji: "🔋",
        title: "1. Tanden (丹田) — Battery (Energy Core)",
        desc: "Tanden is the source of all vital power in the circuit. In the flashlight, this is the battery: an autonomous energy core. At rest, it holds 100% charge in pure silence without wasting a single microwatt in vain.",
        analogy: "✨ Child's explanation: The magical treasure-room of power where all the flashlight's energy rests peacefully!",
        badgeClass: "bg-amber-500 text-slate-950"
      },
      hotsu: {
        rank: "Element #2",
        emoji: "🔘",
        title: "2. Hotsu (発) — Switch of Will & Desire",
        desc: "Hotsu is the sacred 'I want'! By default, the switch is Normally Open to conserve power. As soon as a sincere living desire to act is born (rather than servile moral duty) — the button closes the circuit!",
        analogy: "✨ Child's explanation: The power switch: when you truly want something, press the button and open the gate for the current!",
        badgeClass: "bg-emerald-500 text-slate-950"
      },
      mushin: {
        rank: "Element #3",
        emoji: "⚡",
        title: "3. Mushin (無心) — Pure Current (Flow of Attention)",
        desc: "Mushin is pure electric current traveling at the speed of light! It awakes ONLY when the Hotsu button is pressed. It carries zero ego friction, zero doubt, zero evaluation anxiety: it is free, swift, and direct.",
        analogy: "✨ Child's explanation: A swift river of electricity racing through wires the moment the button is pressed!",
        badgeClass: "bg-orange-500 text-white"
      },
      gyo: {
        rank: "Element #4",
        emoji: "💡",
        title: "4. Gyo (行) — Light Bulb (Constructive Action)",
        desc: "Gyo is concrete constructive action in physical reality (work, art, code, sport, assistance). Mushin current enters the Gyo bulb and produces bright visible light, banishing darkness!",
        analogy: "✨ Child's explanation: The heart of light! A glowing star that radiates whenever current runs through it!",
        badgeClass: "bg-yellow-400 text-slate-950"
      },
      zanshin: {
        rank: "Element #5",
        emoji: "🛡️",
        title: "5. Zanshin (残心) — Fuse (Safeguard)",
        desc: "Zanshin is the master's vigilance and circuit breaker. Standing guard on the return wire. If the light bulb in the world burns out or an action fails — Zanshin breaks the circuit, saving the Tanden battery from burnout.",
        analogy: "✨ Child's explanation: The faithful bodyguard protecting the battery from shorts and breakdowns!",
        badgeClass: "bg-sky-500 text-slate-950"
      }
    };"""

    if old_zen_elements in content:
        content = content.replace(old_zen_elements, new_zen_elements, 1)

    content = content.replace("badgeTitle.textContent = 'ХОЦУ (発) — ЗАМКНУТО';", "badgeTitle.textContent = 'HOTSU (発) — CLOSED';")
    content = content.replace("badgeDesc.textContent = 'Кнопка толкает контакт (ВКЛ)';", "badgeDesc.textContent = 'Button pushes contact (ON)';")
    content = content.replace("statusLabel.textContent = '⚡ Кнопка «Хоцу» ЗЕЛЁНАЯ (замкнута): Ток Мусин бежит, лампочка Гё сияет!';", "statusLabel.textContent = '⚡ Hotsu button GREEN (closed): Mushin current flows, Gyo bulb shines!';")
    content = content.replace("stateBadge.textContent = 'Кнопка «Хоцу» замкнута (ВКЛ)';", "stateBadge.textContent = 'Hotsu button closed (ON)';")
    content = content.replace("btnSub.textContent = 'Ток «Мусин» зажигает «Гё»!';", "btnSub.textContent = 'Mushin current illuminates Gyo!';")

    content = content.replace("badgeTitle.textContent = 'ХОЦУ (発) — РАЗОМКНУТО';", "badgeTitle.textContent = 'HOTSU (発) — OPEN';")
    content = content.replace("badgeDesc.textContent = 'Контакт разомкнут (ВЫКЛ)';", "badgeDesc.textContent = 'Contact released (OFF)';")
    content = content.replace("statusLabel.textContent = '💤 Кнопка «Хоцу» КРАСНАЯ (разомкнута): Контакт отжат, ток Мусин спит';", "statusLabel.textContent = '💤 Hotsu button RED (open): Contact open, Mushin current is resting';")
    content = content.replace("stateBadge.textContent = 'Кнопка «Хоцу» разомкнута (ВЫКЛ)';", "stateBadge.textContent = 'Hotsu button open (OFF)';")
    content = content.replace("btnSub.textContent = 'Нажмите «Хоцу», чтобы пустить ток!';", "btnSub.textContent = 'Click Hotsu to start current!';")

    out_dir = os.path.join(DIST_DIR, "en", "flashlight")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated {out_path}")

    shutil.copyfile(out_path, os.path.join(DIST_DIR, "flashlight", "en.html"))
    shutil.copyfile(out_path, os.path.join(DIST_DIR, "en", "flashlight.html"))
    print("Copied flashlight en.html")

def generate_en_human():
    base_path = os.path.join(DIST_DIR, "human.html")
    with open(base_path, "r", encoding="utf-8") as f:
        content = f.read()

    content = content.replace('<html lang="ru"', '<html lang="en"', 1)
    content = content.replace(
        '<title>Человек-контур: Канон 5 первоэлементов — Inner Current</title>',
        '<title>Human Circuit: Canon of the 5 Primal Elements — Inner Current</title>', 1
    )
    content = content.replace(
        '<meta name="description" content="Интерактивная схемотехника тела человека: Тандэн (батарейка в животе), Хоцу (импульс воли), Мусин (ток внимания), Гё (лампочка в руках на уровне груди) и Дзансин (предохранитель).">',
        '<meta name="description" content="Interactive human body circuitry: Tanden (battery in belly), Hotsu (will impulse), Mushin (attention current), Gyo (light bulb in hands at chest level), and Zanshin (fuse).">', 1
    )
    content = content.replace('Канон &bull; Человек-контур', 'Canon &bull; Human Circuit', 1)

    en_switcher = """      <div class="flex items-center gap-3">
        <!-- Language Switcher -->
        <div class="flex items-center rounded-xl bg-slate-900 border border-slate-800 p-0.5 text-xs font-mono font-semibold" title="Language selection">
          <a href="/human/" onclick="localStorage.setItem('inner_current_lang','ru')" class="px-2.5 py-1 rounded-lg text-slate-400 hover:text-slate-100 hover:bg-slate-800/80 transition">RU</a>
          <span class="px-2.5 py-1 rounded-lg bg-amber-500 text-slate-950 font-bold shadow-sm cursor-default">EN</span>
        </div>"""
    ru_switcher_search = """      <div class="flex items-center gap-3">
        <!-- Language Switcher -->
        <div class="flex items-center rounded-xl bg-slate-900 border border-slate-800 p-0.5 text-xs font-mono font-semibold" title="Выбор языка / Language selection">
          <span class="px-2.5 py-1 rounded-lg bg-amber-500 text-slate-950 font-bold shadow-sm cursor-default">RU</span>
          <a href="/en/human/" onclick="localStorage.setItem('inner_current_lang','en')" class="px-2.5 py-1 rounded-lg text-slate-400 hover:text-slate-100 hover:bg-slate-800/80 transition">EN</a>
        </div>"""
    if ru_switcher_search in content:
        content = content.replace(ru_switcher_search, en_switcher, 1)

    content = content.replace('<span class="hidden sm:inline">Схема фонарика</span>', '<span class="hidden sm:inline">Flashlight Schematic</span>', 1)
    content = content.replace('На главную', 'Home', 1)
    content = content.replace('href="/"', 'href="/en/"')
    content = content.replace('href="/flashlight/"', 'href="/en/flashlight/"')

    # Headings
    content = content.replace('Великий Изоморфизм &bull; Анатомия чистого тока', 'The Great Isomorphism &bull; Anatomy of Pure Current', 1)
    content = content.replace('Человек как замкнутый контур', 'The Human as a Closed Circuit', 1)
    content = content.replace(
        'Схемотехника жизни в теле человека: <strong class="text-amber-400">Тандэн</strong> в животе питает энергией, <strong class="text-emerald-400">Хоцу</strong> запускает волю, чистый ток <strong class="text-orange-400">Мусин</strong> течёт по рукам к груди, рождая свет действия <strong class="text-yellow-300">Гё</strong>, а чуткий предохранитель <strong class="text-sky-400">Дзансин</strong> бережёт контур от выгорания.',
        'Life circuitry in the human body: <strong class="text-amber-400">Tanden</strong> in the abdomen supplies energy, <strong class="text-emerald-400">Hotsu</strong> triggers will, pure current <strong class="text-orange-400">Mushin</strong> flows through arms to chest, radiating the light of action <strong class="text-yellow-300">Gyo</strong>, while vigilant fuse <strong class="text-sky-400">Zanshin</strong> protects the circuit from burnout.', 1
    )
    content = content.replace('<span>🔦</span> Горизонтальная схема фонарика', '<span>🔦</span> Horizontal Flashlight Circuit', 1)
    content = content.replace('<span>🧘</span> Вертикальная схема человека', '<span>🧘</span> Vertical Human Circuit', 1)

    # Workbench header
    content = content.replace('Схемотехника тела &bull; Вертикальный контур', 'Body Circuitry &bull; Vertical Circuit', 1)
    content = content.replace('Живот &rarr; Воля &rarr; Руки &rarr; Грудь &rarr; Защита', 'Belly &rarr; Will &rarr; Arms &rarr; Chest &rarr; Protection', 1)
    content = content.replace('Импульс «Хоцу» включен', 'Hotsu Impulse Engaged (ON)', 1)
    content = content.replace('Ток «Мусин» зажигает лампочку в руках!', 'Mushin current illuminates bulb in hands!', 1)
    content = content.replace('⚡ Цепь замкнута: Тандэн питает лампочку в руках через чистый ток Мусин!', '⚡ Circuit closed: Tanden powers bulb in hands via pure Mushin current!', 1)

    # SVG Labels
    content = content.replace('ТАНДЭН (丹田) — Живот', 'TANDEN (丹田) — Belly')
    content = content.replace('Батарейка • Нижний реактор', 'Battery • Lower Reactor')
    content = content.replace('ХОЦУ (発) — ЗАМКНУТО', 'HOTSU (発) — CLOSED')
    content = content.replace('Контакт воли нажат (ВКЛ)', 'Switch of will engaged (ON)')
    content = content.replace('МУСИН (無心) — Ток', 'MUSHIN (無心) — Flow')
    content = content.replace('Поток по руке без эго', 'Flow in arms without ego')
    content = content.replace('ГЁ (行) — Лампочка в руках', 'GYO (行) — Bulb in Hands')
    content = content.replace('Действие на уровне груди & Свет', 'Action at chest level & Light')
    content = content.replace('ХОЦУ (発) — ВОЛЯ ВКЛ', 'HOTSU (発) — WILL ENGAGED')
    content = content.replace('Контакт замкнут: импульс пошёл', 'Contact closed: impulse flowing')
    content = content.replace('ДЗАНСИН (残心)', 'ZANSHIN (残心)')
    content = content.replace('Предохранитель (Защита контура)', 'Fuse (Safeguard)')
    content = content.replace('Предохранитель на возврате', 'Fuse on return wire')
    content = content.replace('Предохранитель духа', 'Spirit Fuse')
    content = content.replace('Предохранитель', 'Fuse')
    content = content.replace('Дзен-схемотехника и физика духа', 'Zen Engineering & Physics of Spirit')
    content = content.replace(
        '💡 Нажимайте на кнопку <strong class="text-emerald-400">«Хоцу»</strong> или кликайте на любой элемент <strong class="text-amber-400">(1–5)</strong>, чтобы исследовать его работу в теле.',
        '💡 Press the <strong class="text-emerald-400">"Hotsu"</strong> button or click any element <strong class="text-amber-400">(1–5)</strong> to explore its function in the body.', 1
    )

    # 5 Quick buttons
    content = content.replace('<span class="text-[10px] font-mono text-amber-400 uppercase tracking-wider font-bold">1. Живот</span>', '<span class="text-[10px] font-mono text-amber-400 uppercase tracking-wider font-bold">1. Belly</span>')
    content = content.replace('<span class="text-xs font-black text-slate-100">Тандэн (丹田)</span>', '<span class="text-xs font-black text-slate-100">Tanden (丹田)</span>')
    content = content.replace('<span class="text-[10px] text-slate-400 truncate">Батарейка • Реактор</span>', '<span class="text-[10px] text-slate-400 truncate">Battery • Reactor</span>')

    content = content.replace('<span class="text-[10px] font-mono text-emerald-400 uppercase tracking-wider font-bold">2. Воля</span>', '<span class="text-[10px] font-mono text-emerald-400 uppercase tracking-wider font-bold">2. Will</span>')
    content = content.replace('<span class="text-xs font-black text-slate-100">Хоцу (発)</span>', '<span class="text-xs font-black text-slate-100">Hotsu (発)</span>')
    content = content.replace('<span class="text-[10px] text-slate-400 truncate">Кнопка намерения</span>', '<span class="text-[10px] text-slate-400 truncate">Intention Switch</span>')

    content = content.replace('<span class="text-[10px] font-mono text-orange-400 uppercase tracking-wider font-bold">3. Рука</span>', '<span class="text-[10px] font-mono text-orange-400 uppercase tracking-wider font-bold">3. Arm</span>')
    content = content.replace('<span class="text-xs font-black text-slate-100">Мусин (無心)</span>', '<span class="text-xs font-black text-slate-100">Mushin (無心)</span>')
    content = content.replace('<span class="text-[10px] text-slate-400 truncate">Чистый ток внимания</span>', '<span class="text-[10px] text-slate-400 truncate">Pure Attention Current</span>')

    content = content.replace('<span class="text-[10px] font-mono text-yellow-400 uppercase tracking-wider font-bold">4. Грудь</span>', '<span class="text-[10px] font-mono text-yellow-400 uppercase tracking-wider font-bold">4. Chest</span>')
    content = content.replace('<span class="text-xs font-black text-slate-100">Гё (行)</span>', '<span class="text-xs font-black text-slate-100">Gyo (行)</span>')
    content = content.replace('<span class="text-[10px] text-slate-400 truncate">Лампочка в руках</span>', '<span class="text-[10px] text-slate-400 truncate">Bulb in Hands</span>')

    content = content.replace('<span class="text-[10px] font-mono text-sky-400 uppercase tracking-wider font-bold">5. Спина</span>', '<span class="text-[10px] font-mono text-sky-400 uppercase tracking-wider font-bold">5. Spine</span>')
    content = content.replace('<span class="text-xs font-black text-slate-100">Дзансин (残心)</span>', '<span class="text-xs font-black text-slate-100">Zanshin (残心)</span>')
    content = content.replace('<span class="text-[10px] text-slate-400 truncate">Предохранитель духа</span>', '<span class="text-[10px] text-slate-400 truncate">Spirit Fuse</span>')

    # Card initial state
    content = content.replace('1. Тандэн (丹田) — Батарейка в животе (Энергетическое ядро)', '1. Tanden (丹田) — Battery in Belly (Energy Core)')
    content = content.replace('ИСТОЧНИК ПОТЕНЦИАЛА', 'SOURCE OF POTENTIAL')
    content = content.replace(
        'Расположен на 3 пальца ниже пупка (нижний даньтянь / хара). Это биологический аккумулятор человека: клеточный метаболизм, дыхание диафрагмой и запас витальной силы. Если батарейка разряжена или не заземлена, ни одно волевое усилие не сможет зажечь свет в руках.',
        'Located 3 finger-widths below the navel (lower Dan Tian / Hara). This is the biological accumulator of the human being: cellular metabolism, deep diaphragmatic breathing, and reservoir of vital power. If the battery is depleted or ungrounded, no amount of willpower can ignite the light in the hands.', 1
    )
    content = content.replace(
        '«Собери внимание в Тандэне, отпусти лишние мысли, и цепь наполнится плотным потенциалом без малейшего напряжения».',
        '“Gather attention in the Tanden, release redundant thoughts, and the circuit fills with dense potential without the slightest strain.”', 1
    )

    # Correspondence Table
    content = content.replace('<span>⚡</span> Таблица соответствий: Фонарик и Человек', '<span>⚡</span> Correspondence Table: Flashlight & Human', 1)
    content = content.replace(
        'Физика едина на всех масштабах. Один и тот же закон Ома и принцип замкнутой цепи действует как в копеечном карманном фонарике, так и в теле мастера дзен или созидателя.',
        'Physics is invariant across all scales. The same Ohm\'s law and closed circuit principle operates both in a humble pocket flashlight and in the living body of a Zen master or creator.', 1
    )
    content = content.replace('<th class="py-3 px-4">Первоэлемент</th>', '<th class="py-3 px-4">Primal Element</th>', 1)
    content = content.replace('<th class="py-3 px-4">В фонарике</th>', '<th class="py-3 px-4">In Flashlight</th>', 1)
    content = content.replace('<th class="py-3 px-4">В теле человека</th>', '<th class="py-3 px-4">In Human Body</th>', 1)
    content = content.replace('<th class="py-3 px-4">Смысл в контуре</th>', '<th class="py-3 px-4">Meaning in Circuit</th>', 1)

    content = content.replace('<td class="py-3.5 px-4 font-bold text-white">Тандэн (丹田)</td>', '<td class="py-3.5 px-4 font-bold text-white">Tanden (丹田)</td>', 1)
    content = content.replace('<td class="py-3.5 px-4 text-slate-300">Батарейка (ядро питания)</td>', '<td class="py-3.5 px-4 text-slate-300">Battery (Power Core)</td>', 1)
    content = content.replace('<td class="py-3.5 px-4 text-amber-300 font-semibold">Живот (хара / нижний даньтянь)</td>', '<td class="py-3.5 px-4 text-amber-300 font-semibold">Abdomen (Hara / Lower Dan Tian)</td>', 1)
    content = content.replace('<td class="py-3.5 px-4 text-slate-400">Источник электродвижущей силы (ЭДС)</td>', '<td class="py-3.5 px-4 text-slate-400">Source of Electromotive Force (EMF)</td>', 1)

    content = content.replace('<td class="py-3.5 px-4 font-bold text-white">Хоцу (発 / Хочу)</td>', '<td class="py-3.5 px-4 font-bold text-white">Hotsu (発 / I Want)</td>', 1)
    content = content.replace('<td class="py-3.5 px-4 text-slate-300">Кнопка-толкатель & контакт</td>', '<td class="py-3.5 px-4 text-slate-300">Push-button switch & contact</td>', 1)
    content = content.replace('<td class="py-3.5 px-4 text-emerald-300 font-semibold">Импульс намерения и воли</td>', '<td class="py-3.5 px-4 text-emerald-300 font-semibold">Impulse of intention & will</td>', 1)
    content = content.replace('<td class="py-3.5 px-4 text-slate-400">Физическое замыкание цепи</td>', '<td class="py-3.5 px-4 text-slate-400">Physical closing of the circuit</td>', 1)

    content = content.replace('<td class="py-3.5 px-4 font-bold text-white">Мусин (無心)</td>', '<td class="py-3.5 px-4 font-bold text-white">Mushin (無心)</td>', 1)
    content = content.replace('<td class="py-3.5 px-4 text-slate-300">Электрический ток в проводе</td>', '<td class="py-3.5 px-4 text-slate-300">Electric current in wire</td>', 1)
    content = content.replace('<td class="py-3.5 px-4 text-orange-300 font-semibold">Поток внимания по нервам и рукам</td>', '<td class="py-3.5 px-4 text-orange-300 font-semibold">Flow of attention via nerves & arms</td>', 1)
    content = content.replace('<td class="py-3.5 px-4 text-slate-400">Чистая проводимость без сопротивления эго</td>', '<td class="py-3.5 px-4 text-slate-400">Pure conductance without ego resistance</td>', 1)

    content = content.replace('<td class="py-3.5 px-4 font-bold text-white">Гё (行)</td>', '<td class="py-3.5 px-4 font-bold text-white">Gyo (行)</td>', 1)
    content = content.replace('<td class="py-3.5 px-4 text-slate-300">Лампочка (вольфрамовая нить)</td>', '<td class="py-3.5 px-4 text-slate-300">Light bulb (tungsten filament)</td>', 1)
    content = content.replace('<td class="py-3.5 px-4 text-yellow-300 font-semibold">Лампочка в руках у груди (Действие)</td>', '<td class="py-3.5 px-4 text-yellow-300 font-semibold">Bulb in hands at chest (Action)</td>', 1)
    content = content.replace('<td class="py-3.5 px-4 text-slate-400">Полезная нагрузка и рождение света</td>', '<td class="py-3.5 px-4 text-slate-400">Constructive load & birth of light</td>', 1)

    content = content.replace('<td class="py-3.5 px-4 font-bold text-white">Дзансин (残心)</td>', '<td class="py-3.5 px-4 font-bold text-white">Zanshin (残心)</td>', 1)
    content = content.replace('<td class="py-3.5 px-4 text-slate-300">Предохранитель на возврате</td>', '<td class="py-3.5 px-4 text-slate-300">Fuse on return wire</td>', 1)
    content = content.replace('<td class="py-3.5 px-4 text-sky-300 font-semibold">Бдительность вдоль спины/позвоночника</td>', '<td class="py-3.5 px-4 text-sky-300 font-semibold">Vigilance along spine & back</td>', 1)
    content = content.replace('<td class="py-3.5 px-4 text-slate-400">Защита от выгорания и возврат в Тандэн</td>', '<td class="py-3.5 px-4 text-slate-400">Burnout protection & return to Tanden</td>', 1)

    content = content.replace('>Главная<', '>Home<')
    content = content.replace('>Схема фонарика<', '>Flashlight Schematic<')
    content = content.replace('>Человек-контур<', '>Human Circuit<')
    content = content.replace('&copy; 2026 Владимир Аньянов &bull; Все права защищены', '&copy; 2026 Vladimir Anyanov &bull; All rights reserved', 1)

    # JS humanElements in human.html
    en_human_elements_js = """    const humanElements = {
      tanden: {
        num: 1,
        name: "Tanden (丹田)",
        location: "Abdomen (lower Dan Tian / Hara)",
        role: "SOURCE OF POTENTIAL",
        icon: "🔋",
        title: "1. Tanden (丹田) — Battery in Belly (Energy Core)",
        text: "Located 3 finger-widths below the navel (lower Dan Tian / Hara). This is the biological accumulator of the human being: cellular metabolism, deep diaphragmatic breathing, and reservoir of vital power. If the battery is depleted or ungrounded, no amount of willpower can ignite the light in the hands.",
        quote: "“Gather attention in the Tanden, release redundant thoughts, and the circuit fills with dense potential without the slightest strain.”",
        color: "amber"
      },
      hotsu: {
        num: 2,
        name: "Hotsu (発 / I Want)",
        location: "Impulse of Intention & Will",
        role: "CIRCUIT SWITCH",
        icon: "🔘",
        title: "2. Hotsu (発 / I Want) — Switch of Will & Intention",
        text: "This is the impulse of genuine desire and the decision to act. The 'Hotsu' button mechanically pushes the contact, closing the loop from belly to arms. Without pressing this switch, the Tanden potential remains dormant. When Hotsu is direct and uncoerced, current flows without internal struggle.",
        quote: "“True desire is not self-coercion, but the simple closing of contact: deciding to let energy flow into reality.”",
        color: "emerald"
      },
      mushin: {
        num: 3,
        name: "Mushin (無心)",
        location: "Right arm (conducting path)",
        role: "FLOW OF ATTENTION",
        icon: "🌊",
        title: "3. Mushin (無心) — Attention Current (Flow State)",
        text: "Unhindered flow of energy through the body. Mushin is 'no-mind', the absence of parasitic ego resistance, doubt, and tension. The current races through relaxed arms directly to the palms with maximum efficiency, obeying Ohm's law.",
        quote: "“Current does not think about where to go. It simply follows the closed circuit of least resistance.”",
        color: "orange"
      },
      gyo: {
        num: 4,
        name: "Gyo (行)",
        location: "Palms at chest level (Heart center)",
        role: "CONSTRUCTIVE ACTION & LIGHT",
        icon: "💡",
        title: "4. Gyo (行) — Light Bulb in Hands (Fruit of Creation)",
        text: "The bulb held gently in hands at chest level. This is tangible creative action: a written line, finished code, a spoken kind word illuminating darkness. The bulb shines only while Mushin current flows through it.",
        quote: "“Light in the hands is no miracle, but the inevitable consequence of a closed circuit. Do the work, and the light is born on its own.”",
        color: "yellow"
      },
      zanshin: {
        num: 5,
        name: "Zanshin (残心)",
        location: "Spine & back (return wire)",
        role: "PROTECTION & LINGERING SPIRIT",
        icon: "🛡️",
        title: "5. Zanshin (残心) — Circuit Breaker (Mindful Awareness)",
        text: "The vigilant fuse on the return journey along the spine back to Tanden. Zanshin is the 'lingering spirit', mindful awareness sustained after action. It prevents short circuits and protects the heart from burning out.",
        quote: "“Having released the arrow, do not drop your gaze. Keep the circuit closed, and energy returns to Tanden renewed.”",
        color: "sky"
      }
    };"""

    # Look for original humanElements in human.html
    import re
    human_elements_pattern = re.compile(r'const humanElements = \{.*?\n    \};', re.DOTALL)
    content = human_elements_pattern.sub(en_human_elements_js.strip(), content, count=1)

    # In updateHumanUI() JS
    content = content.replace('badge.innerText = "Импульс «Хоцу» включен";', 'badge.innerText = "Hotsu impulse engaged (ON)";')
    content = content.replace('sub.innerText = "Ток «Мусин» зажигает лампочку в руках!";', 'sub.innerText = "Mushin current illuminates bulb in hands!";')
    content = content.replace('statusLabel.innerText = "⚡ Цепь замкнута: Тандэн питает лампочку в руках через чистый ток Мусин!";', 'statusLabel.innerText = "⚡ Circuit closed: Tanden powers bulb in hands via pure Mushin current!";')
    content = content.replace('hotsuBadgeTitle.innerText = "ХОЦУ (発) — ВОЛЯ ВКЛ";', 'hotsuBadgeTitle.innerText = "HOTSU (発) — WILL ENGAGED";')
    content = content.replace('hotsuBadgeDesc.innerText = "Контакт замкнут: импульс пошёл";', 'hotsuBadgeDesc.innerText = "Contact closed: impulse flowing";')

    content = content.replace('badge.innerText = "Цепь разомкнута (ВЫКЛ)";', 'badge.innerText = "Circuit open (OFF)";')
    content = content.replace('sub.innerText = "Нажмите, чтобы включить волю Хоцу!";', 'sub.innerText = "Click to engage Hotsu will!";')
    content = content.replace('statusLabel.innerText = "⭕ Цепь разомкнута: контакт Хоцу отведен, ток Мусин остановлен";', 'statusLabel.innerText = "⭕ Circuit open: Hotsu contact disengaged, Mushin current paused";')
    content = content.replace('hotsuBadgeTitle.innerText = "ХОЦУ (発) — РАЗОМКНУТО";', 'hotsuBadgeTitle.innerText = "HOTSU (発) — OPEN";')
    content = content.replace('hotsuBadgeDesc.innerText = "Контакт отведен (НЕТ ТОКА)";', 'hotsuBadgeDesc.innerText = "Contact disengaged (NO CURRENT)";')

    out_dir = os.path.join(DIST_DIR, "en", "human")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated {out_path}")

    shutil.copyfile(out_path, os.path.join(DIST_DIR, "human", "en.html"))
    shutil.copyfile(out_path, os.path.join(DIST_DIR, "en", "human.html"))
    print("Copied human en.html")

if __name__ == "__main__":
    print("Building English site and updating Russian language switchers...")
    update_russian_files()
    generate_en_index()
    generate_en_flashlight()
    generate_en_human()
    print("=== All English pages generated and synchronized successfully! ===")
