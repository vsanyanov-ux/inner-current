#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_en_manifesto_whitepaper.py
Generates the complete English versions of the Manifesto and White Paper for innercurrent.ru:
- dist_site/en/manifesto.html & dist_site/en/manifesto/index.html & public/en/manifesto.html
- dist_site/en/whitepaper.html & dist_site/en/whitepaper/index.html & public/en/whitepaper.html
- Updates Russian dist_site/manifesto.html, public/manifesto.html with [RU | EN] language switcher
- Updates Russian dist_site/whitepaper.html, public/whitepaper.html with [RU | EN] language switcher
- Updates dist_site/en/index.html and dist_site/en.html with top nav links and Hero CTA button
"""

import os
import shutil
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST_DIR = os.path.join(ROOT_DIR, "dist_site")
PUBLIC_DIR = os.path.join(ROOT_DIR, "public")

def update_russian_manifesto():
    """Adds RU/EN language switcher to Russian manifesto.html"""
    for base_dir in [DIST_DIR, PUBLIC_DIR]:
        path = os.path.join(base_dir, "manifesto.html")
        if not os.path.exists(path):
            continue
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()

        # Update navbar with language switcher if not present
        ru_switcher = """        <div class="flex items-center gap-2">
          <!-- Language Switcher -->
          <div class="flex items-center rounded-xl bg-slate-900 border border-slate-800 p-0.5 text-xs font-mono font-semibold" title="Выбор языка / Language selection">
            <span class="px-2 py-1 rounded-lg bg-amber-500 text-slate-950 font-bold shadow-sm cursor-default text-[11px]">RU</span>
            <a href="/en/manifesto.html" onclick="setLanguage('en')" class="px-2 py-1 rounded-lg text-slate-400 hover:text-slate-100 hover:bg-slate-800/80 transition text-[11px]">EN</a>
          </div>
          <a href="index.html#reader" class="px-3.5 py-1.5 rounded-xl text-xs font-bold bg-amber-500 hover:bg-amber-400 text-slate-950 transition flex items-center gap-1.5 shadow-md shadow-amber-500/20">"""
        
        old_target = """        <div class="flex items-center gap-2">
          <a href="index.html#reader" class="px-3.5 py-1.5 rounded-xl text-xs font-bold bg-amber-500 hover:bg-amber-400 text-slate-950 transition flex items-center gap-1.5 shadow-md shadow-amber-500/20">"""
        
        if "href=\"/en/manifesto.html\"" not in html and old_target in html:
            html = html.replace(old_target, ru_switcher, 1)

        # Update sidebar English Edition link
        old_sidebar_link = '<a href="/en/" onclick="setLanguage(\'en\')" class="sidebar-nav-item flex items-center justify-between gap-2 px-2.5 py-2 rounded-xl text-slate-300 hover:text-white hover:bg-slate-800/60 border border-transparent transition">'
        new_sidebar_link = '<a href="/en/manifesto.html" onclick="setLanguage(\'en\')" class="sidebar-nav-item flex items-center justify-between gap-2 px-2.5 py-2 rounded-xl text-slate-300 hover:text-white hover:bg-slate-800/60 border border-transparent transition">'
        if old_sidebar_link in html:
            html = html.replace(old_sidebar_link, new_sidebar_link, 1)

        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Updated language switcher in {path}")

def update_russian_whitepaper():
    """Adds RU/EN language switcher to Russian whitepaper.html"""
    for base_dir in [DIST_DIR, PUBLIC_DIR]:
        path = os.path.join(base_dir, "whitepaper.html")
        if not os.path.exists(path):
            continue
        with open(path, "r", encoding="utf-8") as f:
            html = f.read()

        ru_switcher = """      <div class="flex items-center gap-3 text-xs font-medium">
        <a href="index.html" class="text-slate-400 hover:text-slate-200 transition">Главная</a>
        <a href="manifesto.html" class="text-amber-400 hover:text-amber-300 transition flex items-center gap-1 font-semibold"><span>⚡</span> Манифест</a>
        <!-- Language Switcher -->
        <div class="flex items-center rounded-xl bg-slate-900 border border-slate-800 p-0.5 text-xs font-mono font-semibold" title="Выбор языка / Language selection">
          <span class="px-2 py-1 rounded-lg bg-amber-500 text-slate-950 font-bold shadow-sm cursor-default text-[11px]">RU</span>
          <a href="/en/whitepaper.html" onclick="setLanguage('en')" class="px-2 py-1 rounded-lg text-slate-400 hover:text-slate-100 hover:bg-slate-800/80 transition text-[11px]">EN</a>
        </div>
        <a href="books/whitepaper.pdf" download class="px-3.5 py-1.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold transition flex items-center gap-1.5 shadow-md shadow-amber-500/10">"""

        old_target = """      <div class="flex items-center gap-4 text-xs font-medium">
        <a href="index.html" class="text-slate-400 hover:text-slate-200 transition">Главная</a>
        <a href="manifesto.html" class="text-amber-400 hover:text-amber-300 transition flex items-center gap-1 font-semibold"><span>⚡</span> Манифест</a>
        <a href="books/whitepaper.pdf" download class="px-3.5 py-1.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold transition flex items-center gap-1.5 shadow-md shadow-amber-500/10">"""

        if "href=\"/en/whitepaper.html\"" not in html and old_target in html:
            html = html.replace(old_target, ru_switcher, 1)

        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Updated language switcher in {path}")

def build_en_manifesto():
    """Builds English Manifesto HTML"""
    manifesto_path = os.path.join(DIST_DIR, "manifesto.html")
    with open(manifesto_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Replacements for English Manifesto
    html = html.replace('<html lang="ru"', '<html lang="en"')
    html = html.replace(
        '<title>Манифест Внутреннего Тока — Электродинамика сознания | innercurrent.ru</title>',
        '<title>The Inner Current Manifesto — Consciousness Electrodynamics | innercurrent.ru</title>'
    )
    html = html.replace(
        '<meta name="description" content="Манифест Внутреннего Тока: в чем суть открытия, почему мы выгораем, как устроен человек на самом деле и почему в лампочке нет батарейки. 500+ статей, 7 книг, 100% открытый доступ.">',
        '<meta name="description" content="The Inner Current Manifesto: why we burn out, how human beings are actually wired, and why there is no battery inside the lightbulb. 500+ articles, 7 books, 100% open access.">'
    )

    # Sidebar Brand & Telemetry
    html = html.replace('innercurrent.ru', 'innercurrent.ru/en')
    html = html.replace('Свернуть сайдбар [Ctrl+B или [ ]', 'Collapse sidebar [Ctrl+B or [ ]')
    html = html.replace('Закрыть меню', 'Close menu')
    html = html.replace('Цепь замкнута', 'Circuit Closed')
    html = html.replace('7 книг • 500+ ст.', '7 Books • 500+ Arts.')
    html = html.replace('placeholder="Поиск по разделам (нажмите /)..."', 'placeholder="Search sections (press /)..."')

    # Sidebar Groups
    html = html.replace('<span>Манифесты &amp; Протоколы</span>', '<span>Manifestos &amp; Protocols</span>')
    html = html.replace('<span>Манифест Тока</span>', '<span>Current Manifesto</span>')
    html = html.replace('<span>Дом Внутреннего Тока</span>', '<span>House of Inner Current</span>')
    html = html.replace('<span>Золотая Семёрка 2.0</span>', '<span>Golden Seven 2.0</span>')
    html = html.replace('<span class="text-slate-400">7 книг</span>', '<span class="text-slate-400">7 Books</span>')
    html = html.replace('Все книги (Обзор)', 'All Books (Overview)')
    html = html.replace('<span class="text-[9px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-300">7 томов</span>', '<span class="text-[9px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-300">7 Volumes</span>')
    html = html.replace('Онлайн-ридер книг', 'Online Book Reader')
    html = html.replace('<span>Аудиокнига онлайн</span>', '<span>Audiobook Online</span>')

    # Sidebar 7 Books
    html = html.replace('Внутренний ток (Базис)', 'Inner Current (Basis)')
    html = html.replace('Четверичный фрактал (C₄)', 'Quaternary Fractal (C₄)')
    html = html.replace('Универсальный закон', 'Universal Flow Law')
    html = html.replace('Тайна фонарика (Детям)', 'Flashlight Primer (Ages 10+)')
    html = html.replace('Полевое руководство', 'Field Manual')
    html = html.replace('Дзен-гитара &amp; Укулеле', 'Zen Ukulele of Being')
    html = html.replace('Великий Синтез 2.0', 'The Great Synthesis 2.0')
    html = html.replace('Двухконтурный каскад', 'Dual-Circuit Cascade')

    # Sidebar Instruments
    html = html.replace('<span>Интерактивные приборы</span>', '<span>Interactive Instruments</span>')
    html = html.replace('<span>Дзен-фонарик (Схема)</span>', '<span>Zen Flashlight (Circuit)</span>')
    html = html.replace('<span>Человек-контур</span>', '<span>Human Circuit</span>')
    html = html.replace('<span>Тренажер цепи</span>', '<span>Circuit Workbench</span>')
    html = html.replace('<span>Пульт Сверхпроводимости</span>', '<span>Superconductivity Cockpit</span>')
    html = html.replace('border-amber-500/30">Стенд</span>', 'border-amber-500/30">Lab</span>')

    # Sidebar Knowledge Base & Links
    html = html.replace('<span>База Знаний &amp; PDF</span>', '<span>Knowledge Base &amp; PDF</span>')
    html = html.replace('<span>Вики-ридер (LLM Wiki)</span>', '<span>Wiki Reader (LLM Wiki)</span>')
    html = html.replace('<span>Материалы и брошюры PDF</span>', '<span>PDF Materials &amp; Guides</span>')
    html = html.replace('<span>English Edition</span>', '<span>Russian Edition</span>')
    html = html.replace('href="/en/manifesto.html" onclick="setLanguage(\'en\')"', 'href="/manifesto.html" onclick="setLanguage(\'ru\')"')
    html = html.replace('<span class="text-[9px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-300">EN</span>', '<span class="text-[9px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-300">RU</span>')
    html = html.replace('<span>Telegram-канал</span>', '<span>Telegram Channel</span>')

    # Top Navbar in content area
    html = html.replace('title="Открыть меню"', 'title="Open menu"')
    html = html.replace('title="Скрыть/показать сайдбар (Ctrl+B)"', 'title="Toggle sidebar (Ctrl+B)"')
    html = html.replace('<span class="text-xs font-semibold">Меню</span>', '<span class="text-xs font-semibold">Menu</span>')
    html = html.replace('<span class="text-xs font-mono font-medium">Панель</span>', '<span class="text-xs font-mono font-medium">Panel</span>')
    html = html.replace('<div class="text-[9px] uppercase font-mono tracking-widest text-slate-400 font-semibold">Манифест Тока</div>', '<div class="text-[9px] uppercase font-mono tracking-widest text-slate-400 font-semibold">Current Manifesto</div>')
    html = html.replace('<a href="index.html" class="hover:text-amber-300 transition flex items-center gap-1"><span>←</span> Главная</a>', '<a href="index.html" class="hover:text-amber-300 transition flex items-center gap-1"><span>←</span> Home</a>')
    html = html.replace('<span>📄</span> White Paper</a>', '<span>📄</span> White Paper</a>')
    html = html.replace('href="whitepaper.html"', 'href="whitepaper.html"')
    html = html.replace('<a href="index.html#house" class="hover:text-amber-300 transition">Дом Тока</a>', '<a href="/en/flashlight/" class="hover:text-amber-300 transition flex items-center gap-1"><span>🔦</span> Flashlight</a>')
    html = html.replace('<a href="index.html#books" class="hover:text-amber-300 transition">Книги (7)</a>', '<a href="/en/human/" class="hover:text-amber-300 transition flex items-center gap-1"><span>🧘</span> Human Circuit</a>')
    html = html.replace('<span>📚</span> Вики</a>', '<span>📚</span> Wiki</a>')
    html = html.replace('<span>📖</span> <span>Ридер</span>', '<span>📖</span> <span>Reader</span>')

    # Language Switcher in English Manifesto navbar
    en_nav_switcher = """        <div class="flex items-center gap-2">
          <!-- Language Switcher -->
          <div class="flex items-center rounded-xl bg-slate-900 border border-slate-800 p-0.5 text-xs font-mono font-semibold" title="Language selection">
            <a href="/manifesto.html" onclick="setLanguage('ru')" class="px-2 py-1 rounded-lg text-slate-400 hover:text-slate-100 hover:bg-slate-800/80 transition text-[11px]">RU</a>
            <span class="px-2 py-1 rounded-lg bg-amber-500 text-slate-950 font-bold shadow-sm cursor-default text-[11px]">EN</span>
          </div>
          <a href="index.html#reader" class="px-3.5 py-1.5 rounded-xl text-xs font-bold bg-amber-500 hover:bg-amber-400 text-slate-950 transition flex items-center gap-1.5 shadow-md shadow-amber-500/20">"""
    
    # Replace navbar quick buttons area
    if 'href="/en/manifesto.html"' in html:
        html = html.replace(
            '<span class="px-2 py-1 rounded-lg bg-amber-500 text-slate-950 font-bold shadow-sm cursor-default text-[11px]">RU</span>\n            <a href="/en/manifesto.html" onclick="setLanguage(\'en\')" class="px-2 py-1 rounded-lg text-slate-400 hover:text-slate-100 hover:bg-slate-800/80 transition text-[11px]">EN</a>',
            '<a href="/manifesto.html" onclick="setLanguage(\'ru\')" class="px-2 py-1 rounded-lg text-slate-400 hover:text-slate-100 hover:bg-slate-800/80 transition text-[11px]">RU</a>\n            <span class="px-2 py-1 rounded-lg bg-amber-500 text-slate-950 font-bold shadow-sm cursor-default text-[11px]">EN</span>'
        )
    else:
        old_btn_block = """        <div class="flex items-center gap-2">\n          <a href="index.html#reader" class="px-3.5 py-1.5 rounded-xl text-xs font-bold bg-amber-500 hover:bg-amber-400 text-slate-950 transition flex items-center gap-1.5 shadow-md shadow-amber-500/20">"""
        if old_btn_block in html:
            html = html.replace(old_btn_block, en_nav_switcher, 1)

    # Hero Section
    html = html.replace('<span>⚡</span> СИСТЕМА АНЬЯНОВА • МАНИФЕСТ СУВЕРЕННОГО ЧЕЛОВЕКА', '<span>⚡</span> ANYANOV SYSTEM • MANIFESTO OF THE SOVEREIGN HUMAN')
    html = html.replace(
        'Манифест <br class="hidden sm:inline"/>\n        <span class="bg-gradient-to-r from-amber-400 via-amber-300 to-sky-300 bg-clip-text text-transparent text-glow-amber">\n          Внутреннего Тока\n        </span>',
        'The Inner Current <br class="hidden sm:inline"/>\n        <span class="bg-gradient-to-r from-amber-400 via-amber-300 to-sky-300 bg-clip-text text-transparent text-glow-amber">\n          Manifesto\n        </span>'
    )
    html = html.replace(
        'Электродинамика сознания: почему мы выгораем, как устроен человек на самом деле и почему в лампочке нет батарейки.',
        'Consciousness electrodynamics: why we burn out, how human beings are actually wired, and why there is no battery inside the lightbulb.'
    )
    html = html.replace('<div class="text-xs text-slate-400 mt-0.5 font-medium">Статей и глав в Базе</div>', '<div class="text-xs text-slate-400 mt-0.5 font-medium">Articles in Knowledge Base</div>')
    html = html.replace('<div class="text-xs text-slate-400 mt-0.5 font-medium">Книг Золотой Семёрки</div>', '<div class="text-xs text-slate-400 mt-0.5 font-medium">Golden Seven Books</div>')
    html = html.replace('<div class="text-xs text-slate-400 mt-0.5 font-medium">Свободный открытый код</div>', '<div class="text-xs text-slate-400 mt-0.5 font-medium">Free &amp; Open Access</div>')

    # Quote Epigraph Callout
    html = html.replace('<span>⚡</span> Главная аксиома суверенного контура', '<span>⚡</span> Core Axiom of the Sovereign Circuit')
    html = html.replace(
        '«Две с половиной тысячи лет цивилизация относилась к человеческому страданию либо как к мистической каре, требующей смирения и молитв, либо как к бесконечной гуманитарной драме, требующей десятилетий психоанализа. Никто не решился задать простой инженерный вопрос: по каким физическим законам прямо сейчас течет ток твоего внимания? Человек устроен не сложнее карманного фонарика: у тебя есть живой соматический генератор внизу живота, есть проводник внимания и есть реальное действие в мире. Когда внимание замыкается на самого себя в страхе и самолюбовании — проводка раскаляется докрасна по закону Джоуля — Ленца. Это не дефект твоей души. Это физический перегрев резистора при коротком замыкании. Отключи паразитное сопротивление, направь ток в дело — и в ту же секунду наступит сверхпроводимость».',
        '“For two and a half thousand years, civilization treated human suffering either as mystical punishment requiring prayers and submission, or as an endless psychological drama requiring decades of psychoanalysis. No one dared to ask a simple engineering question: by what physical laws does the current of your attention flow right now? A human being is wired no more complexly than a pocket flashlight: you have a living somatic generator in the lower abdomen, you have the conductor of attention, and you have real action in the world. When attention shorts into itself in fear and ego-vanity — the wiring turns red-hot according to the Joule–Lenz law. This is not a moral defect of your soul. This is physical ohmic overheating of a resistor during a short circuit. Disconnect the parasitic resistance, direct current into action — and in that very second, superconductivity arrives.”'
    )
    html = html.replace('— Владимир Аньянов', '— Vladimir Anyanov')

    # Schematic SVG Header & Labels
    html = html.replace('<span>📐</span> Принципиальная электрическая схема человека', '<span>📐</span> Principal Electrical Circuit of a Human Being')
    html = html.replace('СХЕМА «ДЗЕН-ФОНАРИКА» (Kanso v2.2)', 'ZEN FLASHLIGHT CIRCUIT (Kanso v2.2)')
    html = html.replace('>ТАНДЭН<', '>TANDEN<')
    html = html.replace('>丹田 • Источник ЭДС<', '>丹田 • Source of EMF<')
    html = html.replace('>Живое тело (Низ живота)<', '>Living Body (Lower belly)<')
    html = html.replace('>Биохимическая тяга<', '>Biochemical drive<')
    html = html.replace('>РЕЗИСТОР ЭГО (R_ego)<', '>EGO RESISTOR (R_ego)<')
    html = html.replace('>Омический ожог Q = I²Rt<', '>Ohmic Burn Q = I²·R·t<')
    html = html.replace('>ЛАМПОЧКА<', '>LIGHTBULB<')
    html = html.replace('>行 • Нагрузка (Дело)<', '>行 • Load (Action)<')
    html = html.replace('>Код, текст, чай, музыка<', '>Code, text, tea, music<')
    html = html.replace('>НЕТ БАТАРЕЙКИ! (E=0)<', '>NO BATTERY! (E_load=0)<')
    html = html.replace('>ПРОВОДНИК: ЛУЧ НАПРАВЛЕННОГО ВНИМАНИЯ (Мусин R → 0)<', '>CONDUCTOR: BEAM OF DIRECTED ATTENTION (Mushin R → 0)<')
    html = html.replace('>ОБРАТНЫЙ ПРОВОД: РЕАЛЬНЫЙ СЛЕД И РЕЗУЛЬТАТ В ФИЗИЧЕСКОМ МИРЕ<', '>RETURN WIRE: REAL TRACE &amp; FRUIT IN PHYSICAL REALITY<')
    html = html.replace(
        '<div><strong class="text-amber-300">Состояние сверхпроводимости:</strong> Резистор Эго разомкнут ($R_{\\text{ego}} = 0$). Ток внимания свободно течет в лампочку действия.</div>',
        '<div><strong class="text-amber-300">Superconductivity State:</strong> Ego resistor bypassed ($R_{\\text{ego}} = 0$). Attention current flows unimpeded into the action bulb.</div>'
    )
    html = html.replace(
        '<div class="font-mono text-emerald-400">КПД контура $\\mathcal{H} \\to 100\\%$</div>',
        '<div class="font-mono text-emerald-400">Circuit Efficiency $\\eta \\to 100\\%$</div>'
    )

    # Chapters content translation
    # Part I
    html = html.replace('<span class="text-amber-400 font-mono text-xl sm:text-2xl">Часть I.</span>', '<span class="text-amber-400 font-mono text-xl sm:text-2xl">Part I.</span>')
    html = html.replace('<span>Великий тупик XXI века: Изобилие психологии и эпидемия пепла</span>', '<span>The Great Dead-End of the 21st Century: Abundance of Psychology and Epidemic of Ashes</span>')
    html = html.replace('<p>Мы живем в эпоху поразительного исторического парадокса.</p>', '<p>We live in a striking historical paradox.</p>')
    html = html.replace(
        '<p>Никогда прежде человечество не обладало такой плотностью психологической литературы, коучинговых школ, марафонов осознанности и фармацевтических средств. Но никогда прежде люди дела — программисты, создающие сложнейшие архитектуры, предприниматели, строящие компании, ученые, двигающие фронтир науки, дизайнеры и врачи — не чувствовали себя настолько изможденными, опустошенными и внутренне потухшими.</p>',
        '<p>Never before has humanity possessed such a density of psychological literature, coaching academies, mindfulness marathons, and pharmaceutical therapies. Yet never before have creators — engineers designing massive software systems, entrepreneurs building companies, scientists advancing the frontier of knowledge, designers, and surgeons — felt so utterly exhausted, hollowed out, and depleted.</p>'
    )
    html = html.replace('<p>Каждое утро миллионы созидателей сталкиваются с одними и теми же симптомами:</p>', '<p>Every morning millions of productive minds confront the exact same four failure states:</p>')
    html = html.replace('<strong class="text-slate-100">Потухший взгляд и дефицит тяги:</strong> просыпаешься уже усталым, словно аккумулятор за ночь не зарядился ни на один процент.', '<strong class="text-slate-100">Extinguished Gaze and Drive Deficit:</strong> waking up pre-exhausted, as though the somatic battery failed to charge by even a single percent overnight.')
    html = html.replace('<strong class="text-slate-100">Фоновая радиация тревоги:</strong> бесконечное сканирование горизонта на предмет угроз, которое невозможно отключить даже на выходных или в отпуске.', '<strong class="text-slate-100">Background Radiation of Anxiety:</strong> an endless scanning of the horizon for invisible threats that cannot be disabled on weekends or holidays.')
    html = html.replace('<strong class="text-slate-100">Холостой ход неокортекса:</strong> изматывающее ночное переигрывание давних споров, совершенных ошибок или чужих косых взглядов.', '<strong class="text-slate-100">Idle Churn of the Neocortex:</strong> agonizing nighttime replays of old disputes, past mistakes, or perceived judgments from peers.')
    html = html.replace('<strong class="text-slate-100">Парализующий страх оценки:</strong> синдром самозванца, откладывание публикаций, застревание перед белым экраном: <em>«А что, если меня сочтут некомпетентным?»</em>', '<strong class="text-slate-100">Paralyzing Fear of Evaluation:</strong> imposter syndrome, hesitation to ship, freezing before the blank canvas: <em>“What if they find me inadequate?”</em>')
    html = html.replace('<p>Почему лучшие умы заходят в этот тупик?</p>', '<p>Why do the finest minds find themselves in this trap?</p>')
    html = html.replace('<p>Потому что на протяжении двух с половиной тысяч лет цивилизация предлагала человеку лишь две крайности:</p>', '<p>Because for two and a half millennia, civilization offered only two polarized escapes:</p>')
    html = html.replace('<strong>Религиозно-эзотерический туман:</strong> <em>«Смирись, кайся, повышай вибрации, дыши маткой, жди милости космоса»</em>.', '<strong>The Esoteric Mist:</strong> <em>“Submit, repent, raise your vibrations, breathe into cosmic abundance, wait for grace.”</em>')
    html = html.replace('<strong>Бесконечный гуманитарный самоанализ:</strong> <em>«Раскопай детскую психотравму 1998 года, проговори обиду на родителей, найди своё великое предназначение, научись безусловно любить себя»</em>.', '<strong>The Endless Psychoanalytic Ruminate:</strong> <em>“Excavate your 1998 childhood trauma, talk through your grievances with your parents, discover your higher purpose, learn unconditional self-love.”</em>')
    html = html.replace(
        '<p>Когда в серверной стойке выбивает пробки от перегрузки, дежурный инженер не садится медитировать перед шкафом и не пытается понять «детство серверной материнской платы». Он берет мультиметр, открывает электрическую схему и находит узел, где возникло короткое замыкание.</p>',
        '<p>When an electrical server rack blows a breaker under heavy load, the systems engineer on duty does not sit down to meditate before the cabinet or psychoanalyze the “childhood of the motherboard.” The engineer pulls out a digital multimeter, consults the electrical schematic, and localizes the exact junction where a short circuit occurred.</p>'
    )
    html = html.replace(
        '<p class="font-sans font-semibold text-amber-300 text-lg border-l-2 border-amber-400 pl-4 py-1">\n          Человек — это не литературная метафора. Человек — это замкнутая электродинамическая цепь.\n        </p>',
        '<p class="font-sans font-semibold text-amber-300 text-lg border-l-2 border-amber-400 pl-4 py-1">\n          A human being is not a literary metaphor. A human being is a closed electrodynamic circuit.\n        </p>'
    )

    # Part II
    html = html.replace('<span class="text-amber-400 font-mono text-xl sm:text-2xl">Часть II.</span>', '<span class="text-amber-400 font-mono text-xl sm:text-2xl">Part II.</span>')
    html = html.replace('<span>Суть открытия: Модель Дзен-Фонарика и Закон Лампочки</span>', '<span>The Core Discovery: The Zen Flashlight Model and the Bulb Law</span>')
    html = html.replace('<p>Суть открытия системы <strong>«Внутренний ток» (Inner Current)</strong> радикально проста:</p>', '<p>The core breakthrough of the <strong>Inner Current</strong> framework is radically simple:</p>')
    html = html.replace(
        'Любое состояние сознания, эмоция, вдохновение или страдание подчиняются тем же строгим законам физики, термодинамики и электродинамики, что и обычный карманный фонарик.',
        'Every conscious state, emotion, creative spark, or existential dread obeys the exact same physical, thermodynamic, and electrodynamic laws as an ordinary pocket flashlight.'
    )
    html = html.replace('<p>В цепи фонарика нет ничего лишнего:</p>', '<p>There are no extraneous components in this circuit:</p>')
    html = html.replace(
        '<strong>Источник питания (ЭДС) — это не мысли в голове. Это ваше живое тело.</strong><br>\n            В восточной традиции этот соматический центр называют <strong>Тандэн</strong> (точка на 3–5 см ниже пупка — физический центр тяжести человека и узел диафрагмального дыхания). Именно здесь вырабатывается биохимическая тяга, кислородный заряд и потенциал действия.',
        r'<strong>Power Source (EMF) — is not thoughts in your head. It is your living body.</strong><br>\n            In Eastern somatic traditions, this center is known as <strong>Tanden (丹田)</strong> — the somatic center of gravity located 3–5 cm below the navel, the anchor of diaphragmatic breathing. Here, biochemical ATP conversion and oxygen transport generate authentic somatic electromotive force ($\mathcal{E} \approx 1.5\text{ V}$).'
    )
    html = html.replace(
        '<strong>Проводник — это луч вашего внимания.</strong><br>\n            Куда направлено внимание — туда мгновенно течет ток нервных импульсов и энергии.',
        '<strong>Conductor — is the beam of your directed attention.</strong><br>\n            Wherever attention is pointed, electrical action potentials and neural transmission flow instantaneously.'
    )
    html = html.replace(
        '<strong>Нагрузка (Лампочка) — это реальное действие в физическом мире.</strong><br>\n            Написать функцию в коде. Пожарить яичницу. Обнять ребенка. Сыграть гамму на укулеле. Провести трудный диалог. Нагрузка — это то, что реально существует вне вашей черепной коробки прямо здесь и сейчас.',
        '<strong>Load (Lightbulb) — is physical action in the real world.</strong><br>\n            Writing a line of code. Frying an egg. Embracing your child. Playing a chord on an acoustic instrument. Conducting a straightforward conversation. The load exists strictly outside your skull in the physical “Here and Now.”'
    )
    html = html.replace('Фундаментальный Закон Лампочки', 'The Fundamental Bulb Law')
    html = html.replace('В САМОЙ ЛАМПОЧКЕ НЕТ И НИКОГДА НЕ БЫЛО БАТАРЕЙКИ.', 'THERE IS NO BATTERY INSIDE THE LIGHTBULB ITSELF.')
    html = html.replace(
        '<p>Это главное освобождающее открытие для каждого мыслящего существа. Ни в деньгах, ни в новой марке автомобиля, ни в красивом дипломе, ни в миллионе подписчиков <strong>нет встроенного счастья</strong>. Вещи, статусы и результаты — это стеклянные колбы с вольфрамовой нитью. Они светятся и радуют вас <strong>только тогда</strong>, когда через них течет ваш собственный внутренний ток. Как только ток прекращается — вещь мгновенно превращается в мертвый холодный мусор.</p>',
        '<p>This is the central liberating theorem of the Anyanov System. Neither money, nor luxury automobiles, nor prestigious titles, nor follower counts possess <strong>built-in happiness</strong>. Material artifacts and social status are hollow glass envelopes containing inert tungsten filaments. They illuminate <strong>only when your own inner current flows through them</strong>. The moment your attention retreats, the object instantly reverts to cold, dead matter.</p>'
    )

    # Part III
    html = html.replace('<span class="text-amber-400 font-mono text-xl sm:text-2xl">Часть III.</span>', '<span class="text-amber-400 font-mono text-xl sm:text-2xl">Part III.</span>')
    html = html.replace('<span>Физика душевной боли: Закон потерь Джоуля — Ленца</span>', '<span>Physics of Emotional Pain: The Joule–Lenz Law of Losses</span>')
    html = html.replace('<p>Почему же люди выгорают и мучаются?</p>', '<p>Why do intelligent people suffer and burn out?</p>')
    html = html.replace('<p>В 1841 году физики Джеймс Джоуль и Эмилий Ленц сформулировали незыблемый закон потерь электродинамики:</p>', '<p>In 1841–1842, James Prescott Joule and Emil Lenz formulated the invariant law of electrical heat dissipation:</p>')
    html = html.replace('Количество тепла Q пропорционально квадрату силы тока I, сопротивлению проводника R и времени t.', 'Heat Q is directly proportional to the square of current I, resistance R, and time t.')
    html = html.replace('<p>Когда внимание человека свободно течет в действие, сопротивление проводника равно нулю ($R \\to 0$). Наступает режим <strong>сверхпроводимости</strong>:</p>', '<p>When attention flows cleanly into tangible action, resistance tends to zero ($R \\to 0$). The system enters <strong>superconductivity</strong>:</p>')
    html = html.replace('<li>Ток беспрепятственно втекает в лампочку дела.</li>', '<li>Current flows unimpeded into the load of work.</li>')
    html = html.replace('<li>Лампа светит ровно и ярко.</li>', '<li>The bulb shines brightly and steadily.</li>')
    html = html.replace('<li>Проводка остается холодной.</li>', '<li>The wiring remains ice-cold.</li>')
    html = html.replace(
        '<li>В психологии это называют «состоянием потока», в Дзен — состоянием <strong>Мусин</strong> (無心, «чистый разум без застревания»). Вы работаете шесть часов подряд, создаете шедевр и выходите из-за стола полным сил.</li>',
        '<li>In psychology, this is called “flow”; in Zen, it is <strong>Mushin (無心)</strong> — mind without friction. You work for six hours straight, deliver a masterpiece, and rise from your desk revitalized.</li>'
    )
    html = html.replace('<h3 class="text-xl font-bold text-rose-400 font-sans">Авария короткого замыкания</h3>', '<h3 class="text-xl font-bold text-rose-400 font-sans">The Short-Circuit Emergency</h3>')
    html = html.replace('<p>Но что происходит, когда человек садится за работу и вместо действия начинает прокручивать мысли о себе?</p>', '<p>What happens when an operator sits down to work but, instead of acting, loops attention into thoughts about themselves?</p>')
    html = html.replace('<li>«А справлюсь ли я?»</li>', '<li>“Will I succeed?”</li>')
    html = html.replace('<li>«А что обо мне подумает тимлид / клиент / отец?»</li>', '<li>“What will the lead / client / peer think of me?”</li>')
    html = html.replace('<li>«А вдруг я опозорюсь?»</li>', '<li>“What if I embarrass myself?”</li>')
    html = html.replace(
        '<p>В этот момент ток внимания не идет в лампу. Он упирается в паразитный резистор — <strong>Сопротивление Эго ($R_{\\text{ego}}$)</strong>. Энергия внимания замыкается на самого себя.</p>',
        '<p>At that instant, current is diverted into a parasitic shunt — the <strong>Ego Resistor ($R_{\\text{ego}}$)</strong>. Attention shorts directly into self-reflection.</p>'
    )
    html = html.replace(
        '<p>По закону Джоуля — Ленца ток колоссальной силы упирается в сопротивление и превращается в <strong>омический термический ожог</strong>:</p>',
        '<p>Under Joule’s Law, high-amperage current encountering high ohmic resistance generates <strong>destructive thermal heat</strong>:</p>'
    )
    html = html.replace('<li>В теле это ощущается как спазм горла, сжатые зубы, ледяной ком под диафрагмой, каменные трапеции и бессонница.</li>', '<li>Somatically: tight throat, clenched jaw, frozen diaphragm, knotted shoulders, insomnia.</li>')
    html = html.replace('<li>В эмоциях это регистрируется как паника, вина, стыд, зависть, тревога и тотальное выгорание.</li>', '<li>Emotionally: panic, guilt, shame, envy, anxiety, and catastrophic burnout.</li>')
    html = html.replace(
        '<p class="font-sans font-semibold text-rose-300 text-lg border-l-2 border-rose-400 pl-4 py-1">\n          Выгорание — это не психологический тупик и не грех слабости. Это штатный тепловой нагрев проводника при коротком замыкании.\n        </p>',
        '<p class="font-sans font-semibold text-rose-300 text-lg border-l-2 border-rose-400 pl-4 py-1">\n          Burnout is not a moral failure or psychological weakness. It is textbook ohmic overheating of an electrical conductor during a short circuit.\n        </p>'
    )

    # Part IV
    html = html.replace('<span class="text-amber-400 font-mono text-xl sm:text-2xl">Часть IV.</span>', '<span class="text-amber-400 font-mono text-xl sm:text-2xl">Part IV.</span>')
    html = html.replace('<span>Триада Омического Сопротивления (Редукция Кансо)</span>', '<span>The Triad of Ohmic Resistance (Kanso Reduction)</span>')
    html = html.replace('<p>Вся колоссальная номенклатура душевных страданий сводится всего к трем измеримым векторам сопротивления ума:</p>', '<p>The entire inventory of human existential misery collapses into three measurable resistance vectors:</p>')
    html = html.replace('1. R_past (Прошлое)', '1. R_past (Past)')
    html = html.replace('Индуктивная петля', 'Inductive Loop')
    html = html.replace('Вина, обида, мысленное переигрывание старых споров.', 'Guilt, resentment, mental replay of old arguments.')
    html = html.replace('События уже нет в физическом мире, но контур сжигает амперы на холостом ходу.', 'The event no longer exists in physical spacetime, yet the circuit incinerates life energy in an idle loop.')
    html = html.replace('2. R_future (Будущее)', '2. R_future (Future)')
    html = html.replace('Емкостная утечка', 'Capacitive Leak')
    html = html.replace('Гиперконтроль, тревога, симуляции 150 сценариев катастроф.', 'Hyper-control, anxiety, simulating 150 catastrophe scenarios.')
    html = html.replace('Зарядка конденсатора фантазий, обесточивающая действие прямо сейчас.', 'Charging an imaginary capacitor while draining the power needed for right now.')
    html = html.replace('3. R_opinion (Одобрение)', '3. R_opinion (Validation)')
    html = html.replace('Паразитный делитель', 'Parasitic Voltage Divider')
    html = html.replace('Зависимость от лайков, страх критики, боязнь показаться глупым.', 'Addiction to likes, fear of criticism, obsession with looking foolish.')
    html = html.replace('Заземление суверенного генератора на чужую чужую сеть.', 'Grounding your sovereign generator into someone else\'s external power grid.')
    html = html.replace(
        '<p>Когда включены все три резистора, напряжение на лампочке дела падает до нуля. Человек лежит на диване, не сделав ни единого физического движения, но чувствует себя так, словно разгрузил вагон угля. Его сожгли собственные омические потери.</p>',
        '<p>When all three resistors engage simultaneously, voltage across the action load drops to zero. You lie exhausted on the couch without having taken a single physical step. Your own ohmic losses burned you alive.</p>'
    )

    # Part V
    html = html.replace('<span class="text-amber-400 font-mono text-xl sm:text-2xl">Часть V.</span>', '<span class="text-amber-400 font-mono text-xl sm:text-2xl">Part V.</span>')
    html = html.replace('<span>Для кого создана эта система?</span>', '<span>Who This System Is Built For</span>')
    html = html.replace('<p>«Внутренний ток» создан не для коллекционеров абстрактных цитат. Он спроектирован для тех, кто строит реальность:</p>', '<p>The Inner Current is engineered for reality builders:</p>')
    html = html.replace('<strong class="text-amber-300">Для программистов, инженеров и архитекторов систем:</strong>', '<strong class="text-amber-300">For Engineers, Programmers, and System Architects:</strong>')
    html = html.replace('<p class="text-slate-300 text-sm mt-1 m-0">Привыкших оперировать строгими моделями, спецификациями и законами сохранения, а не эзотерической болтологией.</p>', '<p class="text-slate-300 text-sm mt-1 m-0">Used to operating with rigorous models, state machines, and conservation laws rather than esoteric rhetoric.</p>')
    html = html.replace('<strong class="text-sky-300">Для предпринимателей, фаундеров и руководителей:</strong>', '<strong class="text-sky-300">For Founders, Executives, and Leaders:</strong>')
    html = html.replace('<p class="text-slate-300 text-sm mt-1 m-0">Несущих запредельный груз рисков и не имеющих права жечь батарею на сомнения, панику и синдром самозванца.</p>', '<p class="text-slate-300 text-sm mt-1 m-0">Carrying extreme risk who cannot afford to incinerate their battery on panic, hesitation, and imposter syndrome.</p>')
    html = html.replace('<strong class="text-emerald-300">Для авторов, дизайнеров и музыкантов:</strong>', '<strong class="text-emerald-300">For Artists, Authors, and Designers:</strong>')
    html = html.replace('<p class="text-slate-300 text-sm mt-1 m-0">Бьющихся о стену страха чистого листа, ступора перед публикой и зависимости от внешних оценок.</p>', '<p class="text-slate-300 text-sm mt-1 m-0">Facing the void of the blank screen, public exposure, and creative block.</p>')
    html = html.replace('<strong class="text-indigo-300">Для каждого уставшего человека:</strong>', '<strong class="text-indigo-300">For Every Exhausted Human Being:</strong>')
    html = html.replace('<p class="text-slate-300 text-sm mt-1 m-0">Кто устал быть «пациентом» или клиентом бесконечных психологических марафонов и хочет получить в руки понятный инженерный пульт от самого себя.</p>', '<p class="text-slate-300 text-sm mt-1 m-0">Tired of endless self-help loops, ready to master the sovereign dashboard of their own consciousness.</p>')

    # Part VI
    html = html.replace('<span class="text-amber-400 font-mono text-xl sm:text-2xl">Часть VI.</span>', '<span class="text-amber-400 font-mono text-xl sm:text-2xl">Part VI.</span>')
    html = html.replace('<span>Для чего это нужно? Деинтермедиация счастья</span>', '<span>The Purpose: Disintermediation of Happiness</span>')
    html = html.replace('<p>Главная цель системы — <strong>деинтермедиация (полная ликвидация посредников)</strong> между созидателем и источником его жизненной силы.</p>', '<p>The supreme purpose of this architecture is <strong>disintermediation — the total elimination of middlemen</strong> between a creator and their vital source of power.</p>')
    html = html.replace(
        '<p>Что Биткоин сделал для мировой финансовой системы, устранив монополию банков и третьих доверенных лиц, — то <strong>«Внутренний ток» делает для человеческого сознания:</strong></p>',
        '<p>What Bitcoin achieved for financial sovereignty by eliminating central banks and trusted third parties, <strong>Inner Current achieves for consciousness:</strong></p>'
    )
    html = html.replace('<li>Больше не нужно платить тысячи долларов за «доступ к тайным практикам».</li>', '<li>No expensive gatekeepers to “secret wisdom.”</li>')
    html = html.replace('<li>Больше не нужно годами ходить вокруг детских травм, если прямо сейчас горит резистор будущего $R_{\\text{future}}$.</li>', '<li>No years wasted excavating childhood grievances when the future resistor $R_{\\text{future}}$ is what is overheating today.</li>')
    html = html.replace('<li>Больше не нужно искать внешних пастырей и гуру.</li>', '<li>No dependence on external gurus or ideological clearance houses.</li>')
    html = html.replace('Оперативный полевой протокол (OBD-II)', 'Operator Field Protocol (OBD-II)')
    html = html.replace('3-Секундный Соматический Сброс в Тандэн', 'The 3-Second Somatic Reset to Tanden')
    html = html.replace('Когда в течение рабочего дня вы ловите приступ острой тревоги, ступора, раздражения или мысленного спора:', 'Whenever acute anxiety, hesitation, or mental loops strike during the workday:')
    html = html.replace('Секунда 1 (Детекция ожога):', 'Second 1 (Detect the Burn):')
    html = html.replace(
        'Заметить физический зажим (зубы сжаты, дыхание замерло, плечи вздернуты). Сказать себе: <em>«Стоп. Пошел нагрев $Q > 0$. Я включил паразитный резистор»</em>.',
        'Notice physical tension (jaw clenched, breath held, shoulders raised). Acknowledge: <em>“Stop. Ohmic heat detected ($Q > 0$). Parasitic resistor active.”</em>'
    )
    html = html.replace('Секунда 2 (Селекция Кансо):', 'Second 2 (Classify with Kanso):')
    html = html.replace(
        'Мгновенно классифицировать утечку: Я кручу прошлое? ($R_{\\text{past}}$) Я боюсь будущего? ($R_{\\text{future}}$) Я завишу от чужих глаз? ($R_{\\text{opinion}}$)?',
        'Instantly classify the leak: Past guilt ($R_{\\text{past}}$)? Future fear ($R_{\\text{future}}$)? Social validation ($R_{\\text{opinion}}$)? State: <em>“This is virtual noise.”</em>'
    )
    html = html.replace('Секунда 3 (Сброс в Тандэн):', 'Second 3 (Drop to Tanden):')
    html = html.replace(
        'Сделать длинный мягкий выдох животом в точку на 4 см ниже пупка. Расслабить диафрагму. Сбросить ментальное сопротивление в $0\\,\\text{Ом}$ ($R_{\\text{ego}} \\to 0$) и <strong>немедленно направить 100% внимания в ближайшее тактильное действие руками</strong> (нажать клавишу, сделать глоток воды, написать строку).',
        'Exhale gently into the belly 4 cm below the navel. Relax the diaphragm. Zero out the mental resistor ($R_{\\text{ego}} \\to 0$) and <strong>immediately deliver 100% of attention into a concrete physical action with your hands</strong> (strike a key, drink water, write one line).'
    )
    html = html.replace('✓ Сверхпроводимость восстановлена', '✓ Superconductivity restored')

    # Part VII
    html = html.replace('<span class="text-amber-400 font-mono text-xl sm:text-2xl">Часть VII.</span>', '<span class="text-amber-400 font-mono text-xl sm:text-2xl">Part VII.</span>')
    html = html.replace('<span>Архитектура открытого дара: База Знаний и Золотая Семёрка</span>', '<span>Architecture of the Open Gift: Knowledge Base and the Golden Seven</span>')
    html = html.replace('<p>Фундаментальные законы природы не продаются по подписке за $99 в месяц. Нельзя запатентовать закон всемирного тяготения или формулу фотоэффекта Эйнштейна.</p>', '<p>Fundamental physical laws cannot be locked behind a $99/month paywall. You cannot copyright universal gravitation or Ohm’s law.</p>')
    html = html.replace(
        '<p>Поэтому весь проект <strong>«Внутренний ток» на <a href="https://innercurrent.ru" class="text-amber-400 underline hover:text-amber-300">innercurrent.ru</a></strong> является открытым общественным достоянием:</p>',
        '<p>Therefore, the entire <strong>Inner Current</strong> project at <a href="/en/" class="text-amber-400 underline hover:text-amber-300">innercurrent.ru</a> is free open-source public domain:</p>'
    )
    html = html.replace('500+ глав и статей', '500+ Chapters & Articles')
    html = html.replace('Открытая модульная База Знаний (LLM Wiki) со сквозным MOC, навигацией по 4 осям координат и формулами KaTeX.', 'Open modular Knowledge Base (LLM Wiki) with global MOC, 4-axis navigation, and KaTeX equations.')
    html = html.replace('7 книг Золотой Семёрки', '7 Books of the Golden Seven')
    html = html.replace('От экспресс-руководства по выходу из штопора до «Великого Синтеза» — термодинамики негэнтропии и истории цивилизации.', 'From rapid crisis recovery manuals to “The Great Synthesis” — negentropy thermodynamics and civilization history.')
    html = html.replace('Кокпит Сознания OBD-II', 'OBD-II Consciousness Cockpit')
    html = html.replace('Интерактивный диагностический пульт с ползунками сопротивления, радаром утечек и автомобильными лампами аварий.', 'Interactive diagnostic console with resistance sliders, leak radar, and automotive fault indicators.')
    html = html.replace('Онлайн-ридер и аудиокнига на 3 языках без рекламы, пейволлов, трекеров и необходимости регистрации.', 'Online reader and audiobook in 3 languages without ads, paywalls, trackers, or registration.')

    # Seven Axioms
    html = html.replace('⚡ Семь аксиом человека-контура', '⚡ Seven Axioms of the Human Circuit')
    html = html.replace('<strong>Ты — не мысли в голове. Ты — электростанция, которая их питает.</strong> Твой соматический исток лежит в Тандэн.', '<strong>You are not the thoughts in your head. You are the power station that energizes them.</strong> Your somatic generator resides in Tanden.')
    html = html.replace(r'<strong>В лампочке нет батарейки ($\mathcal{E}_{\text{load}} \equiv 0$).</strong> Никакая покупка, цель или статус не сделают тебя счастливым, пока ты сам не пустишь через них ток внимания.', r'<strong>There is no battery inside the lightbulb ($\mathcal{E}_{\text{load}} \equiv 0$).</strong> No external acquisition, title, or status contains happiness until your own current flows through it.')
    html = html.replace('<strong>Любая душевная боль — это термический ожог ($Q = I^2 R t$).</strong> Не борись со следствием — просто разомкни паразитное сопротивление ума.', '<strong>All psychological suffering is ohmic dissipation ($Q = I^2 R t$).</strong> Do not fight the heat — open the parasitic resistance of ego.')
    html = html.replace('<strong>Прошлое — индуктивный морок, Будущее — емкостный мираж.</strong> Цепь можно замкнуть исключительно в физическом настоящем моменте.', '<strong>The past is an inductive illusion; the future is a capacitive mirage.</strong> The circuit closes only in physical present reality.')
    html = html.replace('<strong>Внимание — самая дорогая валюта во Вселенной.</strong> Хватит инвестировать её в симуляции собственных страхов и чужие ожидания.', '<strong>Attention is the most precious thermodynamic currency in the universe.</strong> Stop spending it on phantom simulations.')
    html = html.replace('<strong>Высшая сила созидателя — это сверхпроводимость ($R \\to 0$).</strong> Действуй всем телом, забыв об отражении в зеркале.', '<strong>The ultimate power of the creator is superconductivity ($R \\to 0$).</strong> Act with the whole body, free from the mirror of self-consciousness.')
    html = html.replace('<strong>Цепь должна быть замкнута.</strong> Зажги свой фонарик прямо сейчас — в том деле, которое ждет твоих рук.', '<strong>The circuit must be closed.</strong> Illuminate your flashlight right now — in the work waiting for your hands.')

    # Call to actions at bottom
    html = html.replace('Перейти к практике и изучению материалов', 'PROCEED TO PRACTICE &amp; STUDY MATERIALS')
    html = html.replace('Добро пожаловать в Дом Внутреннего Тока', 'Welcome to the House of Inner Current')
    html = html.replace('<span>📄</span> <span>White Paper (Протокол L1)</span>', '<span>📄</span> <span>White Paper (L1 Protocol)</span>')
    html = html.replace('<span>📖</span> <span>Онлайн-ридер (7 книг)</span>', '<span>📖</span> <span>Online Reader (7 Books)</span>')
    html = html.replace('<span>🎛️</span> <span>Кокпит OBD-II</span>', '<span>🎛️</span> <span>OBD-II Cockpit</span>')
    html = html.replace('<span>📚</span> <span>База Знаний (500+ статей)</span>', '<span>📚</span> <span>Knowledge Base (500+ Articles)</span>')
    html = html.replace('<span>🎧</span> <span>Аудиокнига</span>', '<span>🎧</span> <span>Audiobook</span>')

    # Footer
    html = html.replace('100% Открытое знание • 500+ статей • 7 книг • 2026', '100% Open Knowledge • 500+ Articles • 7 Books • 2026')
    html = html.replace('<a href="index.html" class="hover:text-amber-300 transition">Главная</a>', '<a href="index.html" class="hover:text-amber-300 transition">Home</a>')
    html = html.replace('<a href="manifesto.html" class="text-amber-400 font-semibold">Манифест</a>', '<a href="manifesto.html" class="text-amber-400 font-semibold">Manifesto</a>')
    html = html.replace('<a href="cockpit.html" class="hover:text-sky-300 transition">Кокпит</a>', '<a href="/cockpit.html" class="hover:text-sky-300 transition">Cockpit</a>')
    html = html.replace('<a href="wiki.html" class="hover:text-emerald-300 transition">Вики</a>', '<a href="/wiki.html" class="hover:text-emerald-300 transition">Wiki</a>')

    # Output paths
    en_manifesto_path = os.path.join(DIST_DIR, "en", "manifesto.html")
    with open(en_manifesto_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated: {en_manifesto_path}")

    # Create /en/manifesto/index.html
    en_manifesto_dir = os.path.join(DIST_DIR, "en", "manifesto")
    os.makedirs(en_manifesto_dir, exist_ok=True)
    shutil.copyfile(en_manifesto_path, os.path.join(en_manifesto_dir, "index.html"))

    # Sync to public/
    pub_en_dir = os.path.join(PUBLIC_DIR, "en")
    os.makedirs(pub_en_dir, exist_ok=True)
    shutil.copyfile(en_manifesto_path, os.path.join(pub_en_dir, "manifesto.html"))
    pub_manifesto_dir = os.path.join(pub_en_dir, "manifesto")
    os.makedirs(pub_manifesto_dir, exist_ok=True)
    shutil.copyfile(en_manifesto_path, os.path.join(pub_manifesto_dir, "index.html"))
    print("Synchronized English Manifesto to public/en/manifesto.html")

def build_en_whitepaper():
    """Builds English Master Protocol White Paper HTML"""
    ru_wp_path = os.path.join(DIST_DIR, "whitepaper.html")
    with open(ru_wp_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Base HTML & Head
    html = html.replace('<html lang="ru"', '<html lang="en"')
    html = html.replace(
        '<title>Белая книга: Внутренний ток — Открытый протокол суверенной электродинамики | innercurrent.ru</title>',
        '<title>White Paper: Inner Current — The Open Protocol of Sovereign Human Electrodynamics | innercurrent.ru</title>'
    )
    html = html.replace(
        '<meta name="description" content="Официальная Белая книга (Master Protocol Whitepaper) системы \'Внутренний ток\': двухконтурная электродинамика человека, Proof-of-Action, закон Джоуля-Ленца, теорема лампочки и режим сверхпроводимости.">',
        '<meta name="description" content="Official Master Protocol Whitepaper of the Inner Current system: dual-circuit human electrodynamics, Proof-of-Action, Joule-Lenz law, lightbulb theorem, and superconductivity mode.">'
    )

    # Navbar
    html = html.replace('<a href="index.html" class="text-slate-400 hover:text-slate-200 transition">Главная</a>', '<a href="index.html" class="text-slate-400 hover:text-slate-200 transition">Home</a>')
    html = html.replace('<span>⚡</span> Манифест</a>', '<span>⚡</span> Manifesto</a>')
    html = html.replace('<span>📥</span> <span>Скачать PDF</span>', '<span>📥</span> <span>Download PDF</span>')
    html = html.replace('href="books/whitepaper.pdf"', 'href="../books/whitepaper.pdf"')

    # Language Switcher in English Whitepaper navbar
    en_wp_switcher = """      <div class="flex items-center gap-3 text-xs font-medium">
        <a href="index.html" class="text-slate-400 hover:text-slate-200 transition">Home</a>
        <a href="manifesto.html" class="text-amber-400 hover:text-amber-300 transition flex items-center gap-1 font-semibold"><span>⚡</span> Manifesto</a>
        <!-- Language Switcher -->
        <div class="flex items-center rounded-xl bg-slate-900 border border-slate-800 p-0.5 text-xs font-mono font-semibold" title="Language selection">
          <a href="/whitepaper.html" onclick="setLanguage('ru')" class="px-2 py-1 rounded-lg text-slate-400 hover:text-slate-100 hover:bg-slate-800/80 transition text-[11px]">RU</a>
          <span class="px-2 py-1 rounded-lg bg-amber-500 text-slate-950 font-bold shadow-sm cursor-default text-[11px]">EN</span>
        </div>
        <a href="../books/whitepaper.pdf" download class="px-3.5 py-1.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold transition flex items-center gap-1.5 shadow-md shadow-amber-500/10">"""

    old_target = """      <div class="flex items-center gap-4 text-xs font-medium">
        <a href="index.html" class="text-slate-400 hover:text-slate-200 transition">Главная</a>
        <a href="manifesto.html" class="text-amber-400 hover:text-amber-300 transition flex items-center gap-1 font-semibold"><span>⚡</span> Манифест</a>
        <a href="books/whitepaper.pdf" download class="px-3.5 py-1.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold transition flex items-center gap-1.5 shadow-md shadow-amber-500/10">"""

    if "href=\"/en/whitepaper.html\"" in html:
        html = html.replace(
            '<span class="px-2 py-1 rounded-lg bg-amber-500 text-slate-950 font-bold shadow-sm cursor-default text-[11px]">RU</span>\n          <a href="/en/whitepaper.html" onclick="setLanguage(\'en\')" class="px-2 py-1 rounded-lg text-slate-400 hover:text-slate-100 hover:bg-slate-800/80 transition text-[11px]">EN</a>',
            '<a href="/whitepaper.html" onclick="setLanguage(\'ru\')" class="px-2 py-1 rounded-lg text-slate-400 hover:text-slate-100 hover:bg-slate-800/80 transition text-[11px]">RU</a>\n          <span class="px-2 py-1 rounded-lg bg-amber-500 text-slate-950 font-bold shadow-sm cursor-default text-[11px]">EN</span>'
        )
    elif old_target in html:
        html = html.replace(old_target, en_wp_switcher, 1)

    # Hero Header
    html = html.replace('<span>⚡</span> Официальная спецификация протокола • 2026', '<span>⚡</span> OFFICIAL PROTOCOL SPECIFICATION • 2026')
    html = html.replace(
        '<h1 class="text-3xl sm:text-5xl font-extrabold text-slate-100 tracking-tight leading-tight font-display mb-4">\n        Белая книга: Внутренний ток\n      </h1>',
        '<h1 class="text-3xl sm:text-5xl font-extrabold text-slate-100 tracking-tight leading-tight font-display mb-4">\n        White Paper: Inner Current\n      </h1>'
    )
    html = html.replace(
        '<p class="text-lg sm:text-xl text-slate-300 max-w-2xl mx-auto font-serif italic mb-8">\n        Открытый протокол суверенной электродинамики человека и двухконтурной сверхпроводимости\n      </p>',
        '<p class="text-lg sm:text-xl text-slate-300 max-w-2xl mx-auto font-serif italic mb-8">\n        The Open Protocol of Sovereign Human Electrodynamics and Dual-Circuit Superconductivity\n      </p>'
    )
    html = html.replace('<div>Автор: <span class="text-slate-200 font-semibold">Владимир Аньянов</span></div>', '<div>Author: <span class="text-slate-200 font-semibold">Vladimir Anyanov</span></div>')
    html = html.replace('<div>Версия: <span class="text-amber-400 font-semibold">Master Standard 2.0</span></div>', '<div>Version: <span class="text-amber-400 font-semibold">Master Standard 2.0</span></div>')
    html = html.replace('<div>Статус: <span class="text-emerald-400 font-semibold">Evergreen / Open-Source</span></div>', '<div>Status: <span class="text-emerald-400 font-semibold">Evergreen / Open-Source</span></div>')
    html = html.replace('<span>📥</span> Скачать официальный White Paper (PDF)', '<span>📥</span> Download Official White Paper (PDF)')
    html = html.replace('<span>⚡</span> Читать народный Манифест', '<span>⚡</span> Read Inner Current Manifesto')

    # Main Article Headings & Text
    html = html.replace('<h1>⚡ Белая книга: Внутренний ток</h1>', '<h1>⚡ White Paper: Inner Current</h1>')
    html = html.replace('<h3>Открытый протокол суверенной электродинамики человека и двухконтурной сверхпроводимости (Мастер-стандарт)</h3>', '<h3>The Open Protocol of Sovereign Human Electrodynamics and Dual-Circuit Superconductivity (Master Protocol Standard)</h3>')
    html = html.replace('<strong>Владимир Аньянов</strong><br />\n<em>Создатель Системы Аньянова и Архитектуры Внутреннего Тока</em>', '<strong>Vladimir Anyanov</strong><br />\n<em>Creator of the Anyanov System and Inner Current Architecture</em>')

    # Abstract
    html = html.replace('<h2>⚡ Аннотация (Abstract)</h2>', '<h2>⚡ Abstract</h2>')
    html = html.replace(
        '<p>Традиционные институты человеческого благополучия — от религиозных догм до современной академической поп-психологии и коучинга — опираются на модель доверия к внешним посредникам (Trust-Based Model): социальным валидаторам, культурным клиринговым палатам, одобрению окружающих и вербальным симуляциям неокортекса. Подобно фиатной финансовой системе с её инфляцией и скрытым сеньоражем, эта модель порождает хронический кризис человеческой энергосистемы: эмоциональное выгорание, депрессию, тревогу и синдром самозванца. Фундаментальный порок традиционного подхода заключается в его <strong>нефальсифицируемости</strong>: при крахе системы вина возлагается на самого оператора (<em>«ты недостаточно позитивно мыслил»</em>), поскольку метафорические модели лишены замкнутых уравнений сохранения.</p>',
        '<p>Traditional institutions of human well-being — from religious dogmas to modern academic pop-psychology and coaching — rely on a <strong>trust-based model of external intermediaries</strong>: social validators, cultural clearinghouses, peer approval, and verbal simulations of the neocortex. Much like fiat financial systems with their hidden inflation and seigniorage, this architecture drives a chronic crisis of the human energy system: burnout, depression, anxiety, and imposter syndrome. The fundamental flaw of the legacy approach is its <strong>non-falsifiability</strong>: whenever the system collapses, blame is placed upon the operator (<em>“you didn’t think positively enough”</em>), because metaphorical frameworks lack closed conservation equations.</p>'
    )
    html = html.replace(
        '<p>В настоящей Белой книге представлен <strong>«Внутренний ток» (Inner Current)</strong> — открытый, строгий, бездоверительный (trustless) протокол электродинамики сознания. Мы формулируем человека не как статическую вещь с мыслями, а как <strong>каскад двух открытых неравновесных диссипативных систем (двух вихрей)</strong>:<br />\n1. <strong>Контур I (Биохимический субстрат — Тело Пригожина, 1977):</strong> открытая метаболическая система (37 трлн митохондрий, АТФ, дыхание), рассеивающая энтропию через тепло и удерживающая биологический порядок.<br />\n2. <strong>Контур II (Когнитивное сознание — Дух Аньянова, 2026):</strong> электродинамическая цепь направленного внимания ($I$), совершающая полезную работу в физической реальности.</p>',
        '<p>This White Paper introduces <strong>Inner Current</strong> — an open, mathematically rigorous, trustless protocol of consciousness electrodynamics. We formulate human beings not as static objects possessing thoughts, but as a <strong>cascade of two open non-equilibrium dissipative systems (two vortices)</strong>:<br />\n1. <strong>Circuit I (Biochemical Substrate — Prigogine 1977 Body):</strong> an open metabolic system (37 trillion mitochondria, ATP synthesis, respiration) dissipating entropy via heat and sustaining biological order.<br />\n2. <strong>Circuit II (Cognitive Consciousness — Anyanov 2026 Spirit):</strong> an electrodynamic circuit of directed attention ($I$) performing constructive thermodynamic work in physical reality.</p>'
    )
    html = html.replace(
        '<p>Контуры сопрягаются через <strong>межконтурный гальванический шлюз (Тандэн)</strong>, конвертирующий химический потенциал диафрагмального дыхания в соматическую ЭДС ($\\mathcal{E} \\approx 1.5\\text{ В}$). </p>',
        '<p>The circuits interface through an <strong>inter-circuit galvanic gateway (Tanden)</strong>, transducing the biochemical potential of diaphragmatic respiration into somatic electromotive force ($\\mathcal{E} \\approx 1.5\\text{ V}$).</p>'
    )
    html = html.replace('Мы доказываем:', 'We rigorously prove:')
    html = html.replace('<strong>Закон потерь Джоуля — Ленца ($Q = I^2 R t$):</strong> душевное страдание — это не моральный дефект, а штатный омический перегрев проводников внимания при коротком замыкании на паразитный нихромовый реостат эго ($R_{\\text{ego}} > 0$).', '<strong>The Joule–Lenz Law of Losses ($Q = I^2 R t$):</strong> psychological suffering is not a moral defect, but textbook ohmic overheating of attention conductors during a short circuit through the parasitic nichrome ego rheostat ($R_{\\text{ego}} > 0$).')
    html = html.replace('<strong>Квадратичную ловушку воли:</strong> попытка преодолеть внутреннее сопротивление волевым напором ($I \\uparrow$) приводит к квадратичному росту тепловых потерь ($Q \\sim I^2$), разрушая нервную систему.', '<strong>The Quadratic Trap of Willpower:</strong> attempting to push through internal resistance via sheer willpower ($I \\uparrow$) causes a quadratic explosion of heat losses ($Q \\sim I^2$), frying the nervous system.')
    html = html.replace('<strong>Фундаментальную теорему о нагрузке (Закон Лампочки: $\\mathcal{E}_{\\text{load}} \\equiv 0$):</strong> внешние объекты, деньги, статусы и дипломы лишены собственной ЭДС; они светятся исключительно током оператора, протекающим сквозь них.', '<strong>The Fundamental Load Theorem (The Lightbulb Law: $\\mathcal{E}_{\\text{load}} \\equiv 0$):</strong> external objects, capital, prestige, and titles possess zero intrinsic electromotive force; they illuminate strictly through the operator\'s current flowing through them.')
    html = html.replace('<strong>Протокол Proof-of-Action (PoA):</strong> решение проблемы «двойной траты внимания» (Double-Spending of Attention) посредством запечатывания квантов внимания в материальный Сервер временных меток «Здесь и сейчас» ($t_{\\text{now}}$) с нулевой задержкой ($0\\text{ ms}$).', '<strong>The Proof-of-Action Protocol (PoA):</strong> resolving the “Double-Spending of Attention” problem by anchoring attention quanta into the physical Timestamp Server of the “Here and Now” ($t_{\\text{now}}$) with zero network latency ($0\\text{ ms}$).')
    html = html.replace('<strong>Сверхпроводимость ($R \\to 0$):</strong> формальное математическое определение счастья как состояния цепи без омического сопротивления, при котором КПД стремится к $100\\%$ ($\\eta \\to 1$), тепловые потери исчезают ($Q \\to 0$), а вокруг контура возникает когерентное поле радости.', '<strong>Superconductivity ($R \\to 0$):</strong> the formal mathematical definition of happiness as a zero-resistance circuit state where thermodynamic efficiency approaches $100\\%$ ($\\eta \\to 1$), thermal dissipation vanishes ($Q \\to 0$), and a coherent magnetic field of joy emerges around the loop.')
    html = html.replace(
        '<p>Протокол защищён аппаратными прерывателями цепи (<strong>Дзансин</strong>) и математически неуязвим к внешнему социальному давлению (<strong>Атака 51% социального консенсуса</strong>).</p>',
        '<p>The protocol is safeguarded by hardware circuit breakers (<strong>Zanshin</strong>) and mathematically immune to external crowd interference (<strong>51% Social Consensus Attack</strong>).</p>'
    )

    # Section 1
    html = html.replace('<h2>1. Парадигмальный сдвиг: От фиатного сознания к физике цепей</h2>', '<h2>1. Paradigmatic Shift: From Fiat Consciousness to Circuit Physics</h2>')
    html = html.replace(
        '<p>На протяжении тысячелетий цивилизация изучала душевное состояние человека через призму субъективной драмы: философии, мистики или психоанализа. Когда у современного человека пропадает энергия и начинается выгорание, общество предлагает ему:<br />\n* <em>«Раскопать детскую травму двадцатилетней давности»</em>;<br />\n* <em>«Найти своё истинное метафизическое предназначение»</em>;<br />\n* <em>«Медитировать на свет и повышать вибрации»</em>;<br />\n* <em>«Усилием воли преодолеть лень и победить прокрастинацию»</em>.</p>',
        '<p>For millennia, civilization examined the inner state of human beings through subjective drama: theology, mysticism, or psychotherapy. When a modern creator runs out of energy and burns out, society prescribes:<br />\n* <em>“Excavate a twenty-year-old childhood trauma”</em>;<br />\n* <em>“Discover your metaphysical life purpose”</em>;<br />\n* <em>“Meditate on the light and elevate your vibrations”</em>;<br />\n* <em>“Use willpower to overcome laziness and defeat procrastination.”</em></p>'
    )
    html = html.replace(
        '<p>Когда перегорает проводка в серверной стойке дата-центра, дежурный инженер не анализирует «детство материнской платы» и не читает серверу моральные нотации. Он берёт мультиметр, открывает электрическую схему и локализует точку короткого замыкания или пробоя изоляции на корпус.</p>',
        '<p>When the wiring burns out inside a data center server rack, the engineer on duty does not analyze the “childhood of the motherboard” or lecture the server on morality. The engineer takes a multimeter, opens the wiring diagram, and localizes the short circuit or insulation breakdown to ground.</p>'
    )

    # Mermaid diagram 1
    ru_mermaid_1 = """flowchart LR
    subgraph FiatModel["ТРАДИЦИОННАЯ 'ФИАТНАЯ' МОДЕЛЬ (Trust-Based)"]
        direction TB
        A1["Импульс действия"] --> A2["Посредник: Эго / Оценка / Социум"]
        A2 --> A3["Комиссия: сомнения, вина, стыд, страх"]
        A3 --> A4["Паразитный омический нагрев Q"]
        A4 --> A5["Хроническое выгорание и апатия"]
    end

    subgraph SovereignProtocol["ПРОТОКОЛ ВНУТРЕННЕГО ТОКА (Trustless Circuit)"]
        direction TB
        B1["Ядро Тандэн: Автономная ЭДС"] --> B2["Шунтирование эго (Кансо: R -> 0)"]
        B2 --> B3["Прямой ток внимания I"]
        B3 --> B4["Proof-of-Action: Нагрузка действия"]
        B4 --> B5["Замкнутый контур восполнения dS/dt < 0"]
    end

    FiatModel -.->|"Парадигмальный переход"| SovereignProtocol"""

    en_mermaid_1 = """flowchart LR
    subgraph FiatModel["TRADITIONAL 'FIAT' MODEL (Trust-Based)"]
        direction TB
        A1["Action Impulse"] --> A2["Intermediary: Ego / Peer Approval"]
        A2 --> A3["Commission: Doubt, Guilt, Shame, Fear"]
        A3 --> A4["Parasitic Ohmic Heat Q = I²Rt"]
        A4 --> A5["Chronic Burnout & Apathy"]
    end

    subgraph SovereignProtocol["INNER CURRENT PROTOCOL (Trustless Circuit)"]
        direction TB
        B1["Tanden Reactor: Autonomous EMF"] --> B2["Ego Shunt (Kanso: R -> 0)"]
        B2 --> B3["Direct Attention Current I"]
        B3 --> B4["Proof-of-Action: Physical Work Load"]
        B4 --> B5["Closed Restoration Loop dS/dt < 0"]
    end

    FiatModel -.->|"Paradigmatic Shift"| SovereignProtocol"""

    html = html.replace(ru_mermaid_1, en_mermaid_1)

    html = html.replace('<h3>Принципы инженерной строгости Протокола:</h3>', '<h3>Principles of Protocol Engineering Rigor:</h3>')
    html = html.replace('<li><strong>Бинарность состояния цепи:</strong> электрическая цепь либо замкнута, либо разомкнута. Ток внимания либо совершает полезную работу в объективном мире, либо рассеивается в тепловой ожог нейросети. Самообман здесь физически невозможен.</li>', '<li><strong>Circuit State Binarity:</strong> an electrical circuit is either closed or open. Attention current either performs constructive work in the physical world or dissipates as a thermal burn across neural pathways. Self-deception is physically impossible.</li>')
    html = html.replace('<li><strong>Абсолютная фальсифицируемость (Критерий Поппера):</strong> любой экзистенциальный сбой регистрируется в виде конкретной невязки баланса Кирхгофа ($\\Delta I \\ne 0$), падения напряжения на клеммах действия или соматического перегрева проводников ($Q > 0$).</li>', '<li><strong>Strict Falsifiability (Popper\'s Criterion):</strong> every existential fault registers as a concrete Kirchhoff balance deficit ($\\Delta I \\ne 0$), terminal voltage drop, or somatic conductor overheating ($Q > 0$).</li>')
    html = html.replace('<li><strong>Безобвинительный ремонт (Blameless Debugging):</strong> страдание — это не нравственный порок и не признак слабости характера. Это объективное физическое следствие высокого импеданса среды при протекании электрического тока.</li>', '<li><strong>Blameless Debugging:</strong> suffering is neither a moral defect nor character weakness. It is an objective physical consequence of high impedance during electric current flow.</li>')

    # Section 2
    html = html.replace('<h2>2. Двухконтурная архитектура: Каскад открытых диссипативных систем</h2>', '<h2>2. Dual-Circuit Architecture: Cascade of Open Dissipative Systems</h2>')
    html = html.replace(
        '<p>Фундаментальная ошибка классической науки заключалась в восприятии живого существа как закрытой, равновесной системы (подобной термосу или калориметру Карно — Клаузиуса). В закрытой системе энтропия непрерывно растёт ($dS/dt \\ge 0$), что неизбежно вело философию к романтизации распада, отчаяния и тепловой смерти.</p>',
        '<p>The fatal error of classical philosophy was treating human beings as closed, equilibrium thermodynamic systems (analogous to a Carnot calorimeter). In closed systems, entropy monotonically increases ($dS/dt \\ge 0$), condemning philosophy to romanticize decay, existential despair, and heat death.</p>'
    )
    html = html.replace(
        '<p>В 1977 году Илья Пригожин получил Нобелевскую премию за доказательство того, что <strong>в открытых неравновесных системах материя способна спонтанно организовываться в сложнейший порядок (диссипативные структуры)</strong> при условии прокачки сквозного потока энергии и вещества.</p>',
        '<p>In 1977, Ilya Prigogine received the Nobel Prize in Chemistry for proving that <strong>in open non-equilibrium systems, matter spontaneously organizes into intricate, self-sustaining order (dissipative structures)</strong> as long as a continuous throughput of energy and matter is maintained.</p>'
    )
    html = html.replace(
        '<p>Система Аньянова утверждает: <strong>Человек — это каскад двух открытых неравновесных диссипативных систем (двух вихрей)</strong>:</p>',
        '<p>The Anyanov System establishes: <strong>A human being is a cascade of two open non-equilibrium dissipative systems (two vortices)</strong>:</p>'
    )

    # ASCII Box 1: Dual-circuit
    ru_ascii_1 = """========================================================================================
   АРХИТЕКТУРА ДВУХКОНТУРНОГО ДИССИПАТИВНОГО ЧЕЛОВЕКА (ПРИГОЖИН 1977 — АНЬЯНОВ 2026)
========================================================================================

   [ КОНТУР I: БИОХИМИЧЕСКИЙ СУБСТРАТ — ТЕЛО (ИЛЬЯ ПРИГОЖИН, 1977) ]

     Поток вещества: Пища, H2O, O2  ──►  [ МЕТАБОЛИЧЕСКИЙ ВИХРЬ ]  ──► Сброс CO2, тепла
                                         (37 трлн митохондрий, АТФ)      (Выдох Карно)
                                                    │
                                                    ▼
   ═════════════════════════════════════════════════════════════════════════════════════
   [ МЕЖКОНТУРНЫЙ ГАЛЬВАНИЧЕСКИЙ ШЛЮЗ — ТАНДЭН (丹田) ]

     • Энтеральная нервная система (ENS, 500 млн нейронов), венозная диафрагмальная помпа
     • Преобразователь мощности АТФ в соматическую ЭДС (ℰ ≈ 1.5 В)
   ═════════════════════════════════════════════════════════════════════════════════════
                                                    │
                                                    ▼ I_attention (Ток внимания)
   [ КОНТУР II: КОГНИТИВНОЕ СОЗНАНИЕ — ДУХ (ВЛАДИМИР АНЬЯНОВ, 2026) ]

                     [ РАЗВИЛКА РЕЖИМА ПРОВОДИМОСТИ ВТОРОГО КОНТУРА ]
                                  /                    \\
              (R_ego >> 0)       /                      \\       (R_ego -> 0)
                                /                        \\
   ┌───────────────────────────┐                          ┌───────────────────────────┐
   │    ПАРАЗИТНЫЙ РЕОСТАТ ЭГО │                          │   СВЕРХПРОВОДНИК МУСИН    │
   │  Руминация, вина, тревога │                          │    (Бесшовное присутствие)│
   │  "Что обо мне подумают?"  │                          │    Внимание течет в дело  │
   └─────────────┬─────────────┘                          └─────────────┬─────────────┘
                 │                                                      │
          Q = I² R_ego t                                                ▼
                 ▼                                        ┌───────────────────────────┐
   [ ОМИЧЕСКИЙ ПЕРЕГРЕВ: ТОСКА, ]                         │     ПОЛЕЗНАЯ НАГРУЗКА     │
   [ ВЫГОРАНИЕ, ДЕПРЕССИЯ, АД   ]                         │  (ЩИТ 6 ЛАМП ДЕЙСТВИЯ)    │
   (Короткое замыкание на себя)                           │  Код, текст, музыка, диалог│
                                                          └─────────────┬─────────────┘
                                                                        │
                                                           Return Wire  │ (Сенсорный отклик)
                                                                        ▼
                                                          ┌───────────────────────────┐
                                                          │   СЧАСТЬЕ: dS_total/dt < 0│
                                                          │   СВЕРХПРОВОДИМОСТЬ (η=1) │
                                                          └───────────────────────────┘
========================================================================================"""

    en_ascii_1 = """========================================================================================
   DUAL-CIRCUIT DISSIPATIVE HUMAN ARCHITECTURE (PRIGOGINE 1977 — ANYANOV 2026)
========================================================================================

   [ CIRCUIT I: BIOCHEMICAL SUBSTRATE — THE BODY (ILYA PRIGOGINE, 1977) ]

     Throughput: Nutrition, H2O, O2  ──►  [ METABOLIC VORTEX ]  ──► Exhaust: CO2, Heat
                                         (37T Mitochondria, ATP)      (Carnot Exhaust)
                                                    │
                                                    ▼
   ═════════════════════════════════════════════════════════════════════════════════════
   [ INTER-CIRCUIT GALVANIC GATEWAY — TANDEN (丹田) ]

     • Enteric Nervous System (ENS, 500M neurons), diaphragmatic hemodynamic pump
     • Transducer of metabolic ATP into somatic EMF (ℰ ≈ 1.5 V)
   ═════════════════════════════════════════════════════════════════════════════════════
                                                    │
                                                    ▼ I_attention (Current of Directed Attention)
   [ CIRCUIT II: COGNITIVE CONSCIOUSNESS — THE SPIRIT (VLADIMIR ANYANOV, 2026) ]

                     [ CONDUCTIVITY JUNCTION OF CIRCUIT II ]
                                  /                    \\
              (R_ego >> 0)       /                      \\       (R_ego -> 0)
                                /                        \\
   ┌───────────────────────────┐                          ┌───────────────────────────┐
   │   PARASITIC EGO RHEOSTAT  │                          │    MUSHIN SUPERCONDUCTOR  │
   │  Rumination, guilt, fear  │                          │   (Frictionless Presence) │
   │  "What will they think?"  │                          │   Attention flows to work │
   └─────────────┬─────────────┘                          └─────────────┬─────────────┘
                 │                                                      │
          Q = I² R_ego t                                                ▼
                 ▼                                        ┌───────────────────────────┐
   [ OHMIC OVERHEAT: DESPAIR,  ]                          │      CONSTRUCTIVE LOAD    │
   [ BURNOUT, PANIC, AGONY     ]                          │   (BOARD OF 6 WORK BULBS) │
   (Self-referential short)                               │   Code, text, music, work │
                                                          └─────────────┬─────────────┘
                                                                        │
                                                           Return Wire  │ (Sensory confirmation)
                                                                        ▼
                                                          ┌───────────────────────────┐
                                                          │  HAPPINESS: dS_total/dt < 0
                                                          │  SUPERCONDUCTIVITY (η = 1)│
                                                          └───────────────────────────┘
========================================================================================"""

    html = html.replace(ru_ascii_1, en_ascii_1)

    html = html.replace('<h3>2.1. Контур I: Метаболический вихрь Тела</h3>', '<h3>2.1. Circuit I: The Metabolic Vortex of the Body</h3>')
    html = html.replace('<strong>Функция:</strong> Обеспечение биологической жизни через прокачку материальных носителей энергии (кислород, глюкоза, вода).', '<strong>Function:</strong> Sustaining biological life via continuous throughput of energy substrates (oxygen, glucose, hydration).')
    html = html.replace('<strong>Уравнение энтропии:</strong>', '<strong>Entropy Equation:</strong>')
    html = html.replace('где $d_i S_I > 0$ — внутреннее производство энтропии метаболизма, а $d_e S_I < 0$ — сброс энтропии в окружающую среду через выдох, теплоотдачу и экскрецию.', 'where $d_i S_I > 0$ is internal metabolic entropy production, and $d_e S_I < 0$ is entropy dissipation into the environment through respiration, heat exchange, and excretion.')
    html = html.replace('<strong>Свойство:</strong> Идеально налаженный Контур I (спортзал, сон, нутрицевтики, биохакинг) поставляет колоссальную электрическую мощность, <strong>но сам по себе не гарантирует человеческого счастья</strong>.', '<strong>Property:</strong> An impeccably tuned Circuit I (gym, sleep, nutrition, biohacking) delivers immense electrical power, <strong>yet alone never guarantees human happiness</strong>.')
    html = html.replace('<h3>2.2. Контур II: Электродинамический вихрь Духа</h3>', '<h3>2.2. Circuit II: The Electrodynamic Vortex of the Spirit</h3>')
    html = html.replace('<strong>Функция:</strong> Прокачка информации, смыслов и квантов внимания через физические действия в объективную ткань мира.', '<strong>Function:</strong> Throughput of information, meaning, and attention quanta through physical action into the objective fabric of reality.')
    html = html.replace('<strong>Принцип Изоморфизма:</strong> Внимание подчиняется тем же строгим законам открытых потоковых систем, что и молекулы воды в вихре. Если поток внимания замкнуть внутри самого себя (закрыть сливное отверстие вихря рефлексией над собой) — система немедленно деградирует в гнилое болото энтропийного распада.', '<strong>Isomorphism Principle:</strong> Attention obeys the exact same conservation laws of open flow systems as water in a vortex. If attention is throttled inside itself (blocking the drain via self-referential rumination), the system instantly degrades into an entropy swamp of despair.')

    # Section 3
    html = html.replace('<h2>3. Межконтурный гальванический шлюз: Тандэн</h2>', '<h2>3. Inter-Circuit Galvanic Gateway: Tanden</h2>')
    html = html.replace(
        '<p>В традиционных восточных трактатах соматический центр внизу живота (<strong>Тандэн / 丹田</strong>, точка на 3–5 см ниже пупка) описывался в терминах мистической энергии «Ци». Протокол Внутреннего тока очищает этот узел от эзотерического налёта и даёт ему строгое анатомическое и электродинамическое определение:</p>',
        '<p>In traditional Eastern treatises, the somatic center in the lower abdomen (<strong>Tanden / 丹田</strong>, 3–5 cm below the navel) was described in terms of mystical “Qi.” The Inner Current Protocol strips away esoteric fog, establishing an exact anatomical and electrodynamic definition:</p>'
    )
    html = html.replace(
        '<p><strong>Тандэн — это межконтурный гальванический шлюз (соматический трансформатор)</strong>, конвертирующий биохимическую мощность АТФ и диафрагмальной гемодинамики Контура I в направленную электродвижущую силу намерения ($\\mathcal{E}_{\\text{tanden}} \\approx 1.5\\text{ В}$) Контура II.</p>',
        '<p><strong>Tanden is the inter-circuit galvanic gateway (somatic transformer)</strong>, converting the biochemical power of ATP and diaphragmatic hemodynamics in Circuit I into directed electromotive force of intention ($\\mathcal{E}_{\\text{tanden}} \\approx 1.5\\text{ V}$) across Circuit II.</p>'
    )

    # Mermaid diagram 2
    ru_mermaid_2 = """flowchart TD
    subgraph Circuit1["Контур I: Метаболизм"]
        ENS["Энтеральная нервная система
(ENS: 500 млн нейронов)"]
        VAGUS["Блуждающий нерв
(Nervus Vagus)"]
        DIAPH["Диафрагмальная помпа
(Венозный возврат)"]
    end

    subgraph Gateway["ТАНДЭН (丹田) — Межконтурный шлюз"]
        TRANS["Соматический преобразователь:
АТФ + Дыхание ──► ЭДС ℰ_tanden"]
    end

    subgraph Circuit2["Контур II: Внимание и действие"]
        ATTN["Луч внимания I
(Task-Positive Network)"]
    end

    ENS --> TRANS
    VAGUS --> TRANS
    DIAPH --> TRANS
    TRANS --> ATTN"""

    en_mermaid_2 = """flowchart TD
    subgraph Circuit1["Circuit I: Metabolism (Body)"]
        ENS["Enteric Nervous System
(ENS: 500M Neurons)"]
        VAGUS["Vagus Nerve
(Nervus Vagus)"]
        DIAPH["Diaphragmatic Pump
(Venous Return)"]
    end

    subgraph Gateway["TANDEN (丹田) — Inter-Circuit Gateway"]
        TRANS["Somatic Transducer:
ATP + Respiration ──► EMF ℰ_tanden"]
    end

    subgraph Circuit2["Circuit II: Attention & Action (Spirit)"]
        ATTN["Attention Beam I
(Task-Positive Network)"]
    end

    ENS --> TRANS
    VAGUS --> TRANS
    DIAPH --> TRANS
    TRANS --> ATTN"""

    html = html.replace(ru_mermaid_2, en_mermaid_2)

    html = html.replace('<h3>Аппаратный субстрат Тандэна:</h3>', '<h3>Hardware Substrate of Tanden:</h3>')
    html = html.replace(r'<li><strong>Энтеральная нервная система (ENS):</strong> автономная нейронная сеть кишечника, насчитывающая свыше 500 миллионов нейронов (больше, чем во всем спинном мозге) и производящая до $90\%$ серотонина и $50\%$ дофамина организма.</li>', r"<li><strong>Enteric Nervous System (ENS):</strong> the autonomous neural network of the gut, containing over 500 million neurons (more than the spinal cord) and synthesizing $90\%$ of the body's serotonin and $50\%$ of dopamine.</li>")
    html = html.replace('<li><strong>Диафрагмальная гидравлическая помпа:</strong> при глубоком брюшном вдохе купол диафрагмы опускается, механически массируя органы брюшной полости и создавая отрицательное давление в грудной клетке, что резко увеличивает приток венозной крови к правому предсердию.</li>', '<li><strong>Diaphragmatic Hemodynamic Pump:</strong> during deep abdominal inhalation, the descending diaphragmatic dome massages visceral organs and generates negative intrathoracic pressure, dramatically accelerating venous return to the right atrium.</li>')
    html = html.replace('<li><strong>Парасимпатический тонус блуждающего нерва (<em>Nervus Vagus</em>):</strong> соматическое якорение внимания в Тандэне мгновенно переводит нервную систему из стрессового симпатического режима «бей или беги» в режим высокой вариабельности сердечного ритма (HRV), открывая канал свободной проводимости.</li>', '<li><strong>Parasympathetic Vagal Tone (<em>Nervus Vagus</em>):</strong> somatic anchoring into Tanden instantly shifts the autonomic nervous system from sympathetic fight-or-flight into high heart rate variability (HRV), opening the superconductivity channel.</li>')
    html = html.replace(
        '<p>Генератор Тандэн <strong>автономен</strong>: его напряжение генерируется из соматического контакта с дыханием и гравитацией, и физически не зависит от внешних лайков, социального одобрения или чужого мнения.</p>',
        '<p>The Tanden generator is <strong>autonomous</strong>: its voltage is generated directly from somatic contact with breath and gravity, physically immune to external peer validation or crowd opinion.</p>'
    )

    # Section 4
    html = html.replace('<h2>4. Физика душевной боли: Закон Джоуля — Ленца и квадратичная ловушка воли</h2>', '<h2>4. Physics of Emotional Pain: The Joule–Lenz Law and the Quadratic Will Trap</h2>')
    html = html.replace(
        '<p>В 1841–1842 годах физики Джеймс Джоуль и Эмилий Ленц независимо сформулировали фундаментальный закон теплового действия тока:</p>',
        '<p>In 1841–1842, physicists James Prescott Joule and Emil Lenz independently formulated the invariant law of thermal electrical dissipation:</p>'
    )
    html = html.replace(
        '<p><em>Количество теплоты $Q$, выделяемое в проводнике, прямо пропорционально квадрату силы тока $I$, электрическому сопротивлению $R$ и времени протекания тока $t$.</em></p>',
        '<p><em>The heat energy $Q$ dissipated in a conductor is directly proportional to the square of current $I$, electrical resistance $R$, and duration $t$.</em></p>'
    )
    html = html.replace('<h3>4.1. Природа страданий и выгорания</h3>', '<h3>4.1. The Nature of Suffering and Burnout</h3>')
    html = html.replace(
        '<p>Вся номенклатура экзистенциальных мучений (тревога, панические атаки, тоска, чувство вины, стыд, синдром самозванца) представляет собой <strong>омический термический ожог проводников нервной системы</strong>.</p>',
        '<p>The full taxonomy of existential suffering (anxiety, panic attacks, despair, guilt, shame, imposter syndrome) represents <strong>textbook ohmic thermal damage to nervous system conductors</strong>.</p>'
    )
    html = html.replace('<p>Когда человек направляет внимание не в реальное действие, а начинает рефлексировать над собой:<br />\n* <em>«А что, если я не справлюсь?»</em><br />\n* <em>«А что обо мне подумают?»</em><br />\n* <em>«Почему именно я совершил эту ошибку?»</em></p>', '<p>Whenever an operator diverts attention from physical action into self-referential rumination:<br />\n* <em>“What if I fail?”</em><br />\n* <em>“What will they think of me?”</em><br />\n* <em>“Why was it me who made this mistake?”</em></p>')
    html = html.replace(
        '<p>В этот момент в Контуре II подключается паразитный шунт — <strong>Сопротивление Эго ($R_{\\text{ego}} \\gg 0$)</strong>:<br />\n$$R_{\\text{ego}} = R_{\\text{past}} + R_{\\text{future}} + R_{\\text{opinion}}$$<br />\nТок высокой мощности $I$, вырабатываемый живым телом, упирается в высокое сопротивление. По закону Джоуля — Ленца вся мощность цепи сбрасывается в тепло $Q$:<br />\n* На соматическом уровне: спазм гортани («ком в горле»), зажатые челюсти, хронический гипертонус плечевого пояса, холод в брюшной полости.<br />\n* На психоэмоциональном уровне: ощущение адского внутреннего пекла, бессилия и выгорания.</p>',
        '<p>At that instant, Circuit II engages a parasitic shunt — the <strong>Ego Resistance ($R_{\\text{ego}} \\gg 0$)</strong>:<br />\n$$R_{\\text{ego}} = R_{\\text{past}} + R_{\\text{future}} + R_{\\text{opinion}}$$<br />\nHigh-power current $I$ generated by the living body hits high resistance. Under the Joule–Lenz law, the entire power of the circuit converts into destructive heat $Q$:<br />\n* Somatically: laryngeal spasm (“lump in throat”), clenched jaw, shoulder hypertonus, cold abdominal core.<br />\n* Psychoemotionally: sensations of burning agony, paralysis, and exhaustion.</p>'
    )
    html = html.replace(
        '<p><strong>Выгорание — это не дефект души и не признак лени. Это штатный тепловой нагрев проводника при коротком замыкании.</strong></p>',
        '<p><strong>Burnout is not a spiritual flaw or laziness. It is predictable thermal dissipation in a conductor during a short circuit.</strong></p>'
    )
    html = html.replace('<h3>4.2. Теорема о квадратичной ловушке воли (The Quadratic Trap of Ego-Will)</h3>', '<h3>4.2. Theorem of the Quadratic Will Trap (The Quadratic Trap of Ego-Will)</h3>')
    html = html.replace(
        '<p>В традиционной культуре при падении производительности человеку советуют «взять себя в руки» и применить «силу воли». Протокол Внутреннего тока доказывает математическую катастрофичность этой стратегии:</p>',
        '<p>In conventional self-help culture, when output drops, individuals are urged to “grit their teeth” and apply “willpower.” The Inner Current Protocol proves the mathematical catastrophe of this approach:</p>'
    )

    # Mermaid diagram 3
    ru_mermaid_3 = """flowchart TD
    subgraph Trap["КВАДРАТИЧНАЯ ЛОВУШКА ВОЛИ"]
        A["Сопротивление эго R_ego > 0
(Страх, сомнение, вина)"] --> B["Снижение полезной отдачи"]
        B --> C["Попытка преодолеть волей:
Форсирование тока I в 2 раза (2*I)"]
        C --> D["ТЕПЛОВОЙ ВЗРЫВ:
Тепловые потери Q = (2*I)² * R * t = 4 * Q_0"]
        D --> E["Катастрофический пробой изоляции:
Глубокая депрессия, паническая атака"]
    end"""

    en_mermaid_3 = """flowchart TD
    subgraph Trap["QUADRATIC WILLPOWER TRAP"]
        A["Ego Resistance R_ego > 0
(Fear, Doubt, Guilt)"] --> B["Drop in Constructive Output"]
        B --> C["Willpower Forcing:
Doubling Current (2 * I)"]
        C --> D["THERMAL EXPLOSION:
Heat Dissipation Q = (2*I)² · R · t = 4 · Q_0"]
        D --> E["Catastrophic Insulation Breakdown:
Deep Burnout, Panic, Breakdown"]
    end"""

    html = html.replace(ru_mermaid_3, en_mermaid_3)

    html = html.replace(
        '<p><strong>ТЕОРЕМА I (О квадратичном штрафе):</strong><br />\nЕсли оператор пытается преодолеть внутреннее сопротивление $R_{\\text{ego}} > 0$ путём волевого увеличения силы тока ($I \\to k \\cdot I$, где $k > 1$), количество паразитного разрушительного тепла возрастает <strong>пропорционально квадрату коэффициента усилия</strong>:<br />\n$$Q_{\\text{new}} = k^2 \\cdot Q_{\\text{base}}$$<br />\nПопытка преодолеть страх «насилием над собой» гарантированно ведёт к омическому разрушению нейросети.</p>',
        '<p><strong>THEOREM I (Quadratic Penalty of Willpower):</strong><br />\nIf an operator attempts to overcome internal resistance $R_{\\text{ego}} > 0$ by forcing current through willpower ($I \\to k \\cdot I$, where $k > 1$), destructive thermal dissipation scales <strong>with the square of the effort coefficient</strong>:<br />\n$$Q_{\\text{new}} = k^2 \\cdot Q_{\\text{base}}$$<br />\nOvercoming fear through self-violence mathematically guarantees the thermal destruction of the neural substrate.</p>'
    )
    html = html.replace(
        '<p><strong>Инженерный вывод:</strong> Сопротивление невозможно «продавить» силой. Единственное решение — <strong>мгновенное шунтирование паразитного резистора в ноль ($R_{\\text{ego}} \\to 0$) через канон Кансо</strong>.</p>',
        '<p><strong>Engineering Conclusion:</strong> Resistance cannot be forced. The only sustainable solution is <strong>instant shunting of the parasitic resistor to zero ($R_{\\text{ego}} \\to 0$) via the Canon of Kanso</strong>.</p>'
    )

    # Section 5
    html = html.replace('<h2>5. Фундаментальная теорема о нагрузке: Закон Лампочки ($\\mathcal{E}_{\\text{load}} \\equiv 0$)</h2>', '<h2>5. Fundamental Load Theorem: The Lightbulb Law ($\\mathcal{E}_{\\text{load}} \\equiv 0$)</h2>')
    html = html.replace(
        '<p>Главный бич потребительской цивилизации — когнитивная иллюзия, будто счастье встроено в объекты внешнего мира: деньги, недвижимость, автомобили, карьерные грейды или романтических партнёров. Человек искренне верит: <em>«Вот куплю этот дом — и стану счастливым»</em>.</p>',
        '<p>The great scourge of consumer civilization is the illusion that happiness resides inside external objects: capital, real estate, supercars, corporate ranks, or romantic partners. The individual naively believes: <em>“Once I acquire this house, I will finally be happy.”</em></p>'
    )
    html = html.replace(
        '<p>Протокол Внутреннего тока формулирует незыблемый физический закон:</p>',
        '<p>The Inner Current Protocol states an immutable physical law:</p>'
    )
    html = html.replace(
        '<p><strong>ТЕОРЕМА II (Закон Лампочки):</strong><br />\nВсякий внешний объект материального или социального мира является электрической нагрузкой (потребителем мощности), собственная электродвижущая сила которой тождественно равна нулю:<br />\n$$\\mathcal{E}_{\\text{load}} \\equiv 0$$<br />\n<strong>В САМОЙ ЛАМПОЧКЕ НЕТ И НИКОГДА НЕ БЫЛО БАТАРЕЙКИ.</strong></p>',
        '<p><strong>THEOREM II (The Lightbulb Law):</strong><br />\nEvery external material or social artifact is an electrical load (power consumer) whose intrinsic electromotive force is identically zero:<br />\n$$\\mathcal{E}_{\\text{load}} \\equiv 0$$<br />\n<strong>THERE IS NO BATTERY INSIDE THE LIGHTBULB ITSELF.</strong></p>'
    )

    # ASCII Box 2: Bulb illusion
    ru_ascii_2 = """          ИЛЛЮЗИЯ ПОТРЕБЛЕНИЯ                      ФИЗИЧЕСКАЯ РЕАЛЬНОСТЬ
   ┌───────────────────────────────┐         ┌───────────────────────────────┐
   │ "В машине / деньгах / статусе │         │ Любая вещь — это пассивная    │
   │  содержится энергия счастья"  │   VS    │ вольфрамовая нить лампы.      │
   │   (E_load > 0) — ЛОЖЬ!        │         │ E_load = 0.                   │
   │                               │         │ Лампа светит ТОЛЬКО ТОГДА,    │
   │ Результат: гедонистический    │         │ когда СКВОЗЬ НЕЁ течет ток    │
   │ тупик, разочарование, пустота │         │ вашего собственного генератора│
   └───────────────────────────────┘         └───────────────────────────────┘"""

    en_ascii_2 = """          CONSUMER ILLUSION                        PHYSICAL REALITY
   ┌───────────────────────────────┐         ┌───────────────────────────────┐
   │ "Cars, money, and status      │         │ Every object is an inert      │
   │  contain happiness energy"    │   VS    │ tungsten bulb filament.       │
   │   (E_load > 0) — FALSE!       │         │ E_load ≡ 0.                   │
   │                               │         │ The bulb illuminates ONLY     │
   │ Outcome: hedonic treadmill,   │         │ while current from your own   │
   │ burnout, existential void     │         │ generator flows THROUGH it.   │
   └───────────────────────────────┘         └───────────────────────────────┘"""

    html = html.replace(ru_ascii_2, en_ascii_2)

    html = html.replace(
        '<p>Ни в стакане чая, ни в миллионе долларов, ни в строчке программного кода нет встроенной радости. Это стеклянные колбы. Они светятся и радуют человека <strong>исключительно в те секунды, когда сквозь них течёт его собственный внутренний ток внимания и созидания</strong>. </p>',
        '<p>Neither a cup of tea, nor a million dollars, nor a line of code contains built-in joy. They are glass bulbs. They illuminate <strong>strictly during the seconds when your own current of directed attention and craft passes through them</strong>.</p>'
    )
    html = html.replace(
        '<p>Как только ток выключается, самый дорогой суперкар или самый высокий статус мгновенно превращаются в холодный мёртвый груз. Попытка требовать от лампочки, чтобы она питала генератор — физический абсурд, порождающий кризис опустошения.</p>',
        '<p>The moment current ceases, the most luxurious vehicle or highest title instantly reverts to dead weight. Demanding that the lightbulb recharge the generator is physical absurdity, breeding deep disillusionment.</p>'
    )
    html = html.replace('<h3>5.1. Распределительный Щит 6 ламп</h3>', '<h3>5.1. Distribution Board of 6 Bulbs</h3>')
    html = html.replace(
        '<p>Полноценная жизнь оператора строится на параллельном распределении тока генератора по <strong>6 независимым терминалам полезной нагрузки</strong>:</p>',
        '<p>A resilient human architecture relies on the parallel distribution of generator current across <strong>6 independent work load terminals</strong>:</p>'
    )

    # Mermaid diagram 4
    ru_mermaid_4 = """flowchart TD
    T["Генератор Тандэн
(ЭДС ℰ_tanden)"] --> Dist["Распределительный щит контура"]
    Dist --> L1["1. ТЕЛО (Здоровье, сон, биохимия Контура I)"]
    Dist --> L2["2. ДЕЛО (Мастерство, архитектура, код, ремесло)"]
    Dist --> L3["3. ЛЮДИ (Близкий круг, контакт без масок, резонанс)"]
    Dist --> L4["4. ДОМ (Физическое пространство, порядок, практика Саму)"]
    Dist --> L5["5. УМ (Познание, объективная истина, чтение, логика)"]
    Dist --> L6["6. ИГРА (Чистая спонтанность, творчество, праздник бытия)"]"""

    en_mermaid_4 = """flowchart TD
    T["Tanden Reactor
(EMF ℰ_tanden)"] --> Dist["Circuit Distribution Board"]
    Dist --> L1["1. BODY (Somatic Health, Sleep, Circuit I)"]
    Dist --> L2["2. WORK (Craftsmanship, Architecture, Code)"]
    Dist --> L3["3. PEOPLE (Authentic Resonance, Intimate Circle)"]
    Dist --> L4["4. HOME (Physical Space, Order, Samu Practice)"]
    Dist --> L5["5. MIND (Consilience, Truth, Reason, Reading)"]
    Dist --> L6["6. PLAY (Pure Spontaneity, Music, Celebration)"]"""

    html = html.replace(ru_mermaid_4, en_mermaid_4)

    html = html.replace(r'<li><strong>Закон параллельной надёжности:</strong> ни одна лампа не должна забирать $100\%$ мощности контура. Монополия работы («Дело» при выключенном «Теле») приводит к расплавлению патрона и аварийному отключению всей подстанции.</li>', r'<li><strong>Law of Parallel Reliability:</strong> no single bulb may consume $100\%$ of circuit power. Workaholism (running Work while Body is switched off) melts the socket, triggering an emergency substation blackout.</li>')
    html = html.replace('<li><strong>Изоляция сбоев:</strong> перегорание одного терминала (например, временная неудача в рабочем проекте) не должно гасить остальные 5 ламп. Автоматический выключатель отсекает повреждённый сектор, сохраняя целостность системы.</li>', '<li><strong>Fault Isolation:</strong> a burnout on one terminal (e.g. temporary project setback) must never extinguish the remaining 5 bulbs. The circuit breaker isolates the faulted branch, safeguarding overall continuity.</li>')

    # Section 6
    html = html.replace('<h2>6. Протокол Proof-of-Action (PoA) и Сервер временных меток ($t_{\\text{now}}$)</h2>', '<h2>6. The Proof-of-Action Protocol (PoA) and the Physical Timestamp Server ($t_{\\text{now}}$)</h2>')
    html = html.replace(
        '<p>В криптографии фундаментальным прорывом Сатоши Накамото стало решение проблемы «двойной траты» (Double-Spending Problem) без обращения к централизованному банку: каждый блок транзакций подтверждается доказательством проделанной термодинамической работы (Proof-of-Work).</p>',
        '<p>In cryptography, Satoshi Nakamoto\'s breakthrough was solving the Double-Spending Problem without trusting a central authority: every block of transactions is anchored by thermodynamic verification (Proof-of-Work).</p>'
    )
    html = html.replace('<p>В сфере человеческого сознания существует аналогичный, разрушительный дефект:</p>', '<p>Within human consciousness exists an identical, destructive vulnerability:</p>')
    html = html.replace('<h3>6.1. Проблема двойной траты внимания (Double-Spending of Attention)</h3>', '<h3>6.1. The Double-Spending of Attention Problem</h3>')
    html = html.replace(
        '<p>Человек физически сидит за рабочим столом или ужинает с семьёй (тратит квант внимания $N$ на физическое действие), но одновременно пытается потратить <strong>тот же самый неделимый квант внимания</strong> на:<br />\n* Прокручивание вчерашней обиды (двойная трата №1);<br />\n* Тревогу о курсе валют или дедлайне следующего месяца (двойная трата №2);<br />\n* Оценку того, как он сейчас выглядит со стороны (двойная трата №3).</p>',
        '<p>An individual sits physically at a desk or dines with family (allocating attention quantum $N$ to tangible reality), yet simultaneously attempts to double-spend <strong>that very same indivisible quantum</strong> on:<br />\n* Replaying yesterday\'s grievance (double-spend #1);<br />\n* Simulating next quarter\'s deadlines (double-spend #2);<br />\n* Auditing how one appears to external observers (double-spend #3).</p>'
    )
    html = html.replace(
        '<p>В электродинамике попытка направить один и тот же рабочий ток генератора одновременно в несколько взаимно несогласованных цепей с разным импедансом вызывает фазовый разбаланс, синфазный резонанс и мгновенный пробой изоляции.</p>',
        '<p>In electrodynamics, attempting to drive the same generator current simultaneously into multiple mismatched circuits with conflicting impedances causes severe phase distortion, resonant surge, and insulation breakdown.</p>'
    )

    # ASCII Box 3: Double spending
    ru_ascii_3 = """       [ ПРОБЛЕМА ДВОЙНОЙ ТРАТЫ ВНИМАНИЯ (DOUBLE-SPENDING) ]

                    ┌──► Трата 1: Реальное действие (Код, чай)
                    │
   [ Квант Тока I ] ┼──► Трата 2: Руминация прошлого (Вина, обида)  ──► АВАРИЯ КЗ,
                    │                                                    РАЗРЫВ ЦЕПИ,
                    └──► Трата 3: Симуляция будущего (Паника, страх)     ПЕРЕГРЕВ Q"""

    en_ascii_3 = """       [ THE DOUBLE-SPENDING OF ATTENTION PROBLEM ]

                    ┌──► Spend 1: Real Physical Action (Code, tea, dialogue)
                    │
   [ Current Quantum I ] ──► Spend 2: Past Rumination (Guilt, grievance)  ──► SHORT CIRCUIT,
                    │                                                         PHASE COLLAPSE,
                    └──► Spend 3: Future Simulation (Panic, dread)            OHMIC BURN Q"""

    html = html.replace(ru_ascii_3, en_ascii_3)

    html = html.replace('<h3>6.2. Решение: Физический Сервер временных меток ($t_{\\text{now}}$)</h3>', '<h3>6.2. Solution: The Physical Timestamp Server ($t_{\\text{now}}$)</h3>')
    html = html.replace(
        '<p>Протокол Внутреннего тока решает проблему двойной траты через привязку внимания к материальному <strong>Серверу временных меток (Timestamp Server)</strong>: непосредственному физическому срезу «Здесь и сейчас» ($t_{\\text{now}}$).</p>',
        '<p>The Inner Current Protocol resolves double-spending by anchoring attention into a physical <strong>Timestamp Server</strong>: the immediate material slice of the “Here and Now” ($t_{\\text{now}}$).</p>'
    )

    # Mermaid diagram 5
    ru_mermaid_5 = """flowchart TD
    TS["Материальный сервер временных меток (t_now)"]
    S1["Сенсорный хэш: тактильный контакт стоп, вдох, температура"] --> TS
    TS --> B1["Запечатанный блок N (t_0)"]
    B1 --> S2["Материальный отклик: клик клавиши, глоток чая, взгляд"]
    S2 --> B2["Запечатанный блок N+1 (t_1)"]"""

    en_mermaid_5 = """flowchart TD
    TS["Material Timestamp Server (t_now)"]
    S1["Sensory Hash: Foot contact, diaphragmatic breath, tactile touch"] --> TS
    TS --> B1["Sealed Block N (t_0)"]
    B1 --> S2["Physical Confirmation: Keystroke, sip of water, spoken word"]
    S2 --> B2["Sealed Block N+1 (t_1)"]"""

    html = html.replace(ru_mermaid_5, en_mermaid_5)

    html = html.replace(
        '<li><strong>Прошлое и Будущее не проводят ток:</strong> Прошлое ($t < t_{\\text{now}}$) и Будущее ($t > t_{\\text{now}}$) в физической реальности не имеют материальных проводников. Это нематериальные виртуальные симуляции в дефолт-системе мозга (DMN). Подача реального тока внимания в виртуальные координаты тождественна подаче высокого напряжения на разомкнутые клеммы: $R_{\\text{simulation}} \\to \\infty \\implies Q \\to \\infty$.</li>',
        '<li><strong>Past and Future Do Not Conduct Current:</strong> Past ($t < t_{\\text{now}}$) and Future ($t > t_{\\text{now}}$) lack material conductors in physical reality. They are virtual simulations in the Default Mode Network (DMN). Directing real electrical attention into virtual coordinates is identical to applying high voltage across open terminals: $R_{\\text{simulation}} \\to \\infty \\implies Q \\to \\infty$.</li>'
    )
    html = html.replace(
        '<li><strong>Протокол Proof-of-Action (PoA):</strong><br />\n   Единственной транзакцией, признаваемой контуром валидной, является физически необратимое действие, совершённое в текущий момент времени $t_{\\text{now}}$:</li>\n<li>Нажатие клавиши клавиатуры;</li>\n<li>Тактильный контакт пальцев с чашкой;</li>\n<li>Диафрагмальный выдох в Тандэн;</li>\n<li>Произнесение честного слова вслух.</li>',
        '<li><strong>The Proof-of-Action (PoA) Protocol:</strong><br />\n   The only transaction validated by the circuit is an irreversible physical act executed at time $t_{\\text{now}}$:</li>\n<li>Striking a mechanical keystroke;</li>\n<li>Tactile contact of fingers against a teacup;</li>\n<li>Diaphragmatic exhalation into Tanden;</li>\n<li>Speaking a clear, truthful word aloud.</li>'
    )
    html = html.replace(
        '<p>Как только физическое действие совершено — блок запечатывается. Задержка сети падает до <strong>$0\\text{ ms}$</strong>. Сомнения отключаются, поскольку действие термодинамически необратимо.</p>',
        '<p>The moment physical action is executed, the block is permanently sealed. Network latency drops to <strong>$0\\text{ ms}$</strong>. Doubts evaporate because physical action is thermodynamically irreversible.</p>'
    )

    # Section 7
    html = html.replace('<h2>7. Канон Кансо: Мгновенное шунтирование эго и прунинг памяти</h2>', '<h2>7. The Canon of Kanso: Instant Ego Shunting and Memory Pruning</h2>')
    html = html.replace(
        '<p>В японской традиции дзен канон <strong>Кансо (簡素)</strong> означает предельную строгость, отсечение всего декоративного и ненужного. В Протоколе Внутреннего тока Кансо — это прецизионный хирургический инструмент.</p>',
        '<p>In Zen aesthetics, the canon of <strong>Kanso (簡素)</strong> signifies supreme simplicity — eliminating all decorative and superfluous clutter. In the Inner Current Protocol, Kanso is a surgical engineering tool.</p>'
    )
    html = html.replace('<h3>7.1. Клинок Кансо (Шунт паразитного реостата)</h3>', '<h3>7.1. The Blade of Kanso (Ego Shunt)</h3>')
    html = html.replace(
        '<p>Человеку не нужно тратить годы на психоанализ, чтобы «договориться с эго». С паразитным сопротивлением не договариваются — его <strong>шунтируют проводником с нулевым сопротивлением</strong>:</p>',
        '<p>One does not need years of psychotherapy to “negotiate with the ego.” One does not negotiate with parasitic resistance — one <strong>shunts it via a zero-resistance superconductor</strong>:</p>'
    )

    # ASCII Box 4: Kanso shunt
    ru_ascii_4 = """                       КЛИНОК КАНСО: ШУНТИРОВАНИЕ ЭГО

               ┌───────► [ СВЕРХПРОВОДНИК МУСИН: R -> 0 ] ───────┐
               │         (Прямое включение в действие)           │
   Ток Тандэна │                                                 ▼ Нагрузка
  ─────────────┤                                                 ├────────►
   (Внимание)  │         ┌──────────────────────────────┐        │
               └───────X │ ПАРАЗИТНЫЙ РЕЗИСТОР ЭГО      │ X──────┘
                         │ (Сомнения, страх, оценка)    │
                         │ R_ego >> 0 — ШУНТИРОВАН В 0! │
                         └──────────────────────────────┘"""

    en_ascii_4 = """                       THE BLADE OF KANSO: EGO SHUNTING

               ┌───────► [ MUSHIN SUPERCONDUCTOR: R -> 0 ] ──────┐
               │         (Direct execution in reality)           │
   Tanden EMF  │                                                 ▼ Work Load
  ─────────────┤                                                 ├────────►
  (Attention)  │         ┌──────────────────────────────┐        │
               └───────X │ PARASITIC EGO RESISTOR       │ X──────┘
                         │ (Doubts, anxiety, approval)  │
                         │ R_ego >> 0 — SHUNTED TO 0!   │
                         └──────────────────────────────┘"""

    html = html.replace(ru_ascii_4, en_ascii_4)

    html = html.replace('По закону параллельного соединения проводников ток течёт по пути наименьшего сопротивления:', 'Under Kirchhoff’s laws of parallel conductors, current follows the path of least resistance:')
    html = html.replace(
        'В ту же микросекунду, когда оператор переводит внимание из мыслей «о себе» в физическое действие, ток через резистор эго падает до нуля. Омический нагрев прекращается мгновенно.',
        'In the very microsecond the operator directs attention away from self-reflection into tangible physical action, current across the ego resistor collapses to zero. Ohmic heating ceases instantly.'
    )
    html = html.replace('<h3>7.2. Прунинг оперативной памяти (State Space Pruning)</h3>', '<h3>7.2. State Space Pruning</h3>')
    html = html.replace(
        '<p>Подобно тому как полные ноды блокчейна используют алгоритмы отсечения (Pruning) устаревших данных для экономии дискового пространства, оператор Внутреннего тока применяет Кансо для очистки кратковременной памяти сознания:<br />\n* Любая прошлая ошибка сжимается в <strong>одну строчку инженерного вывода (хэш-корень)</strong>;<br />\n* Сырой эмоциональный лог (обида, стыд, переигрывание диалогов) стирается из памяти безвозвратно. Проводка освобождается от паразитной ёмкости.</p>',
        '<p>Much like blockchain full nodes employ state pruning to discard obsolete history and conserve disk space, the Inner Current operator uses Kanso to prune working memory:<br />\n* Any past failure is compressed into <strong>a single line of engineering conclusion (hash root)</strong>;<br />\n* Raw emotional logs (resentment, shame, debate replays) are purged permanently. Conductor wiring is freed from parasitic capacitance.</p>'
    )

    # Section 8
    html = html.replace('<h2>8. Аппаратная защита: Прерыватель Дзансин и расчёт стойкости к «Атаке 51%»</h2>', '<h2>8. Hardware Safeguards: Zanshin Circuit Breaker and Resistance to “51% Attacks”</h2>')
    html = html.replace('<h3>8.1. Прерыватель цепи (Circuit Breaker): Дзансин (残心)</h3>', '<h3>8.1. Circuit Breaker: Zanshin (残心)</h3>')
    html = html.replace(
        '<p>В боевых искусствах Дзансин означает непрерывную готовность духа, сохранение осознанности после удара. В электродинамике это <strong>автоматический дифференциальный выключатель (Circuit Breaker)</strong>:</p>',
        '<p>In martial arts, Zanshin denotes unshakeable presence and sustained awareness after delivering a strike. In electrodynamics, it functions as an <strong>automatic differential Circuit Breaker</strong>:</p>'
    )

    # Mermaid diagram 6
    ru_mermaid_6 = """flowchart LR
    L["Нагрузка (Действие)"] --> CB{"ДЗАНСИН (Circuit Breaker)
Ток утечки I_leak > I_safe?"}
    CB -- "НЕТ: Норма" --> RET["Замкнутый контур восполнения"]
    CB -- "ДА: Авария (Удар, потеря, критика)" --> TRIP["Мгновенное размыкание
Изоляция повреждения
Сброс тока в Тандэн"]"""

    en_mermaid_6 = """flowchart LR
    L["Load (Action)"] --> CB{"ZANSHIN (Circuit Breaker)
Leakage current I_leak > I_safe?"}
    CB -- "NO: Nominal" --> RET["Closed Restoration Loop"]
    CB -- "YES: Shock (Critique, loss, blow)" --> TRIP["Instant Trip & Isolation
Contain Fault
Ground Current to Tanden"]"""

    html = html.replace(ru_mermaid_6, en_mermaid_6)

    html = html.replace(
        '<p>Если результат действия оказался катастрофическим (срыв сделки, предательство, внешняя агрессия), неопытный оператор пробивает контур на землю: впадает в истерику или самобичевание.<br />\nАвтомат Дзансин срабатывает быстрее, чем неокортекс успеет включить руминацию: он <strong>мгновенно изолирует аварийный участок цепи</strong>, предотвращая разрушение всей электростанции человека.</p>',
        '<p>When action outcomes prove catastrophic (deal failure, betrayal, external crisis), an untrained operator shorts the circuit to ground: descending into panic or self-loathing.<br />\nThe Zanshin circuit breaker trips before the neocortex can initiate rumination: it <strong>instantly isolates the damaged circuit branch</strong>, shielding the somatic power plant from collapse.</p>'
    )
    html = html.replace('<h3>8.2. Математический расчёт: Защита против «Атаки 51% социального консенсуса»</h3>', '<h3>8.2. Mathematical Proof: Protection Against the “51% Social Consensus Attack”</h3>')
    html = html.replace(
        '<p>В распределённых сетях «Атакой 51%» называют захват контроля над историей транзакций пулом злоумышленников, сосредоточивших более половины вычислительной мощности.</p>',
        '<p>In distributed networks, a 51% Attack represents malicious takeover of the transaction ledger by a cartel controlling more than half of the mining hashpower.</p>'
    )
    html = html.replace(
        '<p>В социуме суверенная нода человека непрерывно подвергается <strong>Атаке 51% социального шума</strong>: толпа, информационные агентства, тренды и алгоритмические ленты пытаются навязать ноде свои фальшивые транзакции: тревогу, страх, конформизм и подчинение.</p>',
        '<p>In society, a sovereign human node faces a perpetual <strong>51% Attack of Social Noise</strong>: crowds, algorithmic feeds, and media cartels attempt to force invalid transactions into the local ledger: fear, outrage, conformity, and submission.</p>'
    )

    # ASCII Box 5: 51% Attack
    ru_ascii_5 = """                  АТАКА 51% СОЦИАЛЬНОГО КОНСЕНСУСА
   Внешний хаос: 99% голосов толпы      Суверенная Нода Аньянова
   [ КРИТИКА / ПАНИКА / ТРЕНДЫ ]  ───►  [ ЛОКАЛЬНЫЙ РЕЕСТР: ТАНДЭН ]
                                        • Валидация только по Proof-of-Action
                                        • Внешний шум признан фальшивым блоком
                                        • Результат атаки: ОТКЛОНЕНО (P_z -> 0)"""

    en_ascii_5 = """                  51% SOCIAL CONSENSUS ATTACK
   External Chaos: 99% Crowd Consensus   Sovereign Anyanov Node
   [ CRITIQUE / PANIC / ALGORITHMS ] ──► [ LOCAL LEDGER: TANDEN REACTOR ]
                                         • Validated strictly via Proof-of-Action
                                         • External noise tagged as unverified block
                                         • Attack Result: REJECTED (P_z -> 0)"""

    html = html.replace(ru_ascii_5, en_ascii_5)

    html = html.replace(
        '<p>Пусть $p$ — вероятность того, что оператор удерживает фокус в Тандэне и прямом действии ($R_{\\text{ego}} = 0$), а $q = 1 - p$ — вероятность поддаться внешнему социальному давлению. <br />\nОтношение шансов захвата контура внешним шумом описывается классической теорией случайных блужданий (задача о разорении игрока):</p>',
        '<p>Let $p$ be the probability that an operator maintains focus in Tanden and direct action ($R_{\\text{ego}} = 0$), and $q = 1 - p$ the probability of capitulating to external social coercion.<br />\nThe odds ratio of ledger takeover follows the Gambler\'s Ruin random walk:</p>'
    )
    html = html.replace(
        '<p>Если оператор заземлён в материальном поле ($p > q$), вероятность успешного захвата контура $P_z$ внешним шумом на глубине заземления $z$ (где $z$ — число точек соматического контроля по канону Дзансин) падает <strong>экспоненциально</strong>:</p>',
        '<p>If the operator is grounded in physical reality ($p > q$), the probability $P_z$ of an adversary successfully rewriting local consensus at grounding depth $z$ (number of somatic Zanshin checkpoints) drops <strong>exponentially</strong>:</p>'
    )
    html = html.replace('<p>При наличии хотя бы трёх точек физического заземления ($z \\ge 3$: опора стоп в пол, диафрагмальный вдох, конкретный предмет в руках):<br />\n$$P_z \\to 0 \\quad \\text{при } z \\to \\infty$$</p>', '<p>With as few as three physical grounding anchors ($z \\ge 3$: feet firmly on floor, diaphragmatic exhalation, concrete physical object in hands):<br />\n$$P_z \\to 0 \\quad \\text{as } z \\to \\infty$$</p>')
    html = html.replace('<p><strong>Инженерная теорема суверенитета:</strong>  </p>', '<p><strong>Engineering Theorem of Sovereignty:</strong></p>')
    html = html.replace(
        '<p>Никакое внешнее большинство — обладай оно даже $99.9\\%$ голосов социального шума — <strong>физически не способно нарушить баланс цепи внутри суверенной ноды</strong>, пока нода сохраняет холодное хранение внимания (Cold Storage) и отказывается валидировать фальшивые транзакции чужих проекций.</p>',
        '<p>No external majority — even commanding $99.9\\%$ of crowd noise — <strong>can physically destabilize a sovereign node</strong> as long as the node maintains Cold Storage of attention and refuses to validate ungrounded external projections.</p>'
    )

    # Section 9
    html = html.replace('<h2>9. Спецификация состояний (FSM) и 30-секундный протокол калибровки</h2>', '<h2>9. Finite State Machine (FSM) Specification and 30-Second Calibration</h2>')
    html = html.replace(
        '<p>Суверенная нода человека описывается как детерминированный <strong>конечный автомат (Finite State Machine, FSM)</strong>:</p>',
        '<p>The sovereign human node is modeled as a deterministic <strong>Finite State Machine (FSM)</strong>:</p>'
    )

    # Mermaid diagram 7: FSM
    ru_mermaid_7 = """stateDiagram-v2
    [*] --> STATE_SUPERCONDUCTING

    STATE_SUPERCONDUCTING: СВЕРХПРОВОДИМОСТЬ (Мусин)
    STATE_SUPERCONDUCTING: R = 0, I > 0, Q = 0, η = 100%
    STATE_SUPERCONDUCTING: Чистый поток, радость, действие

    STATE_OHMIC_OVERHEAT: ОМИЧЕСКИЙ ПЕРЕГРЕВ (Авария КЗ)
    STATE_OHMIC_OVERHEAT: R_ego >> 0, Q -> Max, I_load = 0
    STATE_OHMIC_OVERHEAT: Тревога, вина, стыд, выгорание

    STATE_OPEN_CIRCUIT: РАЗРЫВ ЦЕПИ (Холостой ход)
    STATE_OPEN_CIRCUIT: I = 0, Нагрузка обесточена
    STATE_OPEN_CIRCUIT: Апатия, прокрастинация, тупость

    STATE_GROUND_FAULT: УТЕЧКА НА ЗЕМЛЮ (Энтропия)
    STATE_GROUND_FAULT: I_leak > 0, Слив внимания наружу
    STATE_GROUND_FAULT: Зависимость от соцсетей, поиск одобрения

    STATE_SUPERCONDUCTING --> STATE_OHMIC_OVERHEAT: Включение рефлексии эго (R_ego > 0)
    STATE_OHMIC_OVERHEAT --> STATE_SUPERCONDUCTING: Клинок Кансо (Шунт в ноль + Вдох)

    STATE_SUPERCONDUCTING --> STATE_OPEN_CIRCUIT: Потеря контакта с нагрузкой
    STATE_OPEN_CIRCUIT --> STATE_SUPERCONDUCTING: Импульс Тандэна (Proof-of-Action)

    STATE_SUPERCONDUCTING --> STATE_GROUND_FAULT: Социальная валидация (Потеря приватности)
    STATE_GROUND_FAULT --> STATE_SUPERCONDUCTING: Дзансин: Прерывание утечки + Заземление"""

    en_mermaid_7 = """stateDiagram-v2
    [*] --> STATE_SUPERCONDUCTING

    STATE_SUPERCONDUCTING: SUPERCONDUCTING (Mushin)
    STATE_SUPERCONDUCTING: R = 0, I > 0, Q = 0, η = 100%
    STATE_SUPERCONDUCTING: Frictionless flow, joy, tangible output

    STATE_OHMIC_OVERHEAT: OHMIC OVERHEAT (Short Circuit)
    STATE_OHMIC_OVERHEAT: R_ego >> 0, Q -> Max, I_load = 0
    STATE_OHMIC_OVERHEAT: Anxiety, guilt, shame, burnout

    STATE_OPEN_CIRCUIT: OPEN CIRCUIT (Idle Disconnection)
    STATE_OPEN_CIRCUIT: I = 0, Load de-energized
    STATE_OPEN_CIRCUIT: Apathy, procrastination, numbness

    STATE_GROUND_FAULT: GROUND FAULT (Entropy Leak)
    STATE_GROUND_FAULT: I_leak > 0, Attention siphoned away
    STATE_GROUND_FAULT: Compulsive feeds, validation seeking

    STATE_SUPERCONDUCTING --> STATE_OHMIC_OVERHEAT: Ego reflection triggered (R_ego > 0)
    STATE_OHMIC_OVERHEAT --> STATE_SUPERCONDUCTING: Blade of Kanso (Zero shunt + Exhale)

    STATE_SUPERCONDUCTING --> STATE_OPEN_CIRCUIT: Disconnection from action load
    STATE_OPEN_CIRCUIT --> STATE_SUPERCONDUCTING: Tanden impulse (Proof-of-Action)

    STATE_SUPERCONDUCTING --> STATE_GROUND_FAULT: External validation drain (Cold storage breach)
    STATE_GROUND_FAULT --> STATE_SUPERCONDUCTING: Zanshin breaker: Disconnect leak + Ground"""

    html = html.replace(ru_mermaid_7, en_mermaid_7)

    # State Matrix Table
    html = html.replace('<h3>Матрица состояний ноды:</h3>', '<h3>Node State Matrix:</h3>')
    html = html.replace('<th style="text-align: left;">Состояние</th>', '<th style="text-align: left;">State</th>')
    html = html.replace('<th style="text-align: left;">Физический маркер</th>', '<th style="text-align: left;">Physical Marker</th>')
    html = html.replace('<th style="text-align: left;">Параметры цепи</th>', '<th style="text-align: left;">Circuit Metrics</th>')
    html = html.replace('<th style="text-align: left;">Диагностика</th>', '<th style="text-align: left;">Diagnosis</th>')
    html = html.replace('<th style="text-align: left;">Протокол исправления</th>', '<th style="text-align: left;">Remediation Protocol</th>')

    html = html.replace('Легкость, тепло в животе, ясный фокус', 'Buoyancy, warmth in belly, razor focus')
    html = html.replace('<strong>ШТАТНЫЙ РЕЖИМ (МУСИН)</strong>', '<strong>NOMINAL OPERATING MODE (MUSHIN)</strong>')
    html = html.replace('Удержание рабочего такта', 'Maintain operating cadence')

    html = html.replace('Зажим челюстей, спазм горла, паника', 'Clenched jaw, throat spasm, panic')
    html = html.replace('<strong>КОРОТКОЕ ЗАМЫКАНИЕ</strong>', '<strong>SHORT CIRCUIT (OVERHEAT)</strong>')
    html = html.replace('Срез Кансо, выдох в Тандэн', 'Kanso cut, abdominal exhalation to Tanden')

    html = html.replace('Тяжесть век, туман в голове, лень', 'Heavy eyelids, brain fog, apathy')
    html = html.replace('<strong>ОБРЫВ ПРОВОДКИ</strong>', '<strong>OPEN CIRCUIT (DISCONNECTED)</strong>')
    html = html.replace('Микро-действие (Proof-of-Action)', 'Micro-action (Proof-of-Action)')

    html = html.replace('Зуд в пальцах, скроллинг ленты', 'Restless fingers, doomscrolling feeds')
    html = html.replace('<strong>ПРОБОЙ НА ЗЕМЛЮ</strong>', '<strong>GROUND FAULT (ENERGY LEAK)</strong>')
    html = html.replace('Размыкатель Дзансин, изоляция', 'Zanshin circuit trip, quarantine')

    # Calibration Algorithm Box
    html = html.replace('<h3>Экспресс-протокол калибровки: 30-секундный SPV-аудит</h3>', '<h3>Express Calibration Protocol: 30-Second SPV Audit</h3>')
    html = html.replace(
        '<p>Калибровка ноды выполняется без использования громоздких приборов по 4 простым шагам:</p>',
        '<p>Operator calibration requires no complex apparatus, executed in 4 crisp steps:</p>'
    )

    ru_ascii_6 = """┌────────────────────────────────────────────────────────────────────────┐
│               30-СЕКУНДНЫЙ АЛГОРИТМ КАЛИБРОВКИ ОПЕРАТОРА               │
├────────────────────────────────────────────────────────────────────────┤
│ 1. ТЕСТ ГЕНЕРАТОРА (0–5 сек):                                          │
│    Переведи внимание в точку на 3-5 см ниже пупка (Тандэн).            │
│    Сделай глубокий брюшной вдох диафрагмой. Ощути физический вес тела. │
│    ──► СТАТУС: Генератор онлайн. Первичное напряжение верифицировано.   │
│                                                                        │
│ 2. ТЕСТ РЕОСТАТА (5–12 сек):                                           │
│    Где застряло внимание? В прошлом (вина)? Будущем (страх)? В оценке? │
│    ──► ДЕЙСТВИЕ: Примени Клинок Кансо: "Это нематериальный шум".       │
│    Сбрось сопротивление в ноль: R_ego -> 0.                            │
│                                                                        │
│ 3. ВЫПОЛНЕНИЕ PROOF-OF-ACTION (12–25 сек):                             │
│    Мгновенно соверши микроскопическое действие в материальном мире     │
│    с задержкой 0 мс: выпей глоток воды, расправь плечи, напечатай      │
│    строку, прикоснись к столу.                                         │
│    ──► СТАТУС: Блок запечатан. Ток течет в нагрузку.                   │
│                                                                        │
│ 4. АКТИВАЦИЯ СВЕРХПРОВОДИМОСТИ (25–30 сек):                            │
│    Контур замкнут. Нагрузка светит. Проводка холодная.                 │
│    СУВЕРЕННЫЙ ЧЕЛОВЕК НА СВЯЗИ С РЕАЛЬНОСТЬЮ.                          │
└────────────────────────────────────────────────────────────────────────┘"""

    en_ascii_6 = """┌────────────────────────────────────────────────────────────────────────┐
│                30-SECOND OPERATOR CALIBRATION ALGORITHM                │
├────────────────────────────────────────────────────────────────────────┤
│ 1. GENERATOR VERIFICATION (0–5 sec):                                   │
│    Direct attention to point 3–5 cm below navel (Tanden).              │
│    Execute deep abdominal diaphragmatic breath. Feel physical gravity. │
│    ──► STATUS: Reactor Online. Primary Somatic EMF Verified.           │
│                                                                        │
│ 2. RHEOSTAT SHUNTING (5–12 sec):                                       │
│    Where is current trapped? Past (guilt)? Future (dread)? Validation? │
│    ──► ACTION: Apply Blade of Kanso: "This is virtual noise."          │
│    Short-circuit parasitic resistance to absolute zero: R_ego -> 0.    │
│                                                                        │
│ 3. EXECUTE PROOF-OF-ACTION (12–25 sec):                                │
│    Perform an irreversible physical act with 0 ms network delay:       │
│    take a sip of water, square shoulders, strike a key, touch desk.    │
│    ──► STATUS: Block Sealed. Current flowing unimpeded to load.        │
│                                                                        │
│ 4. SUPERCONDUCTIVITY ENGAGED (25–30 sec):                              │
│    Circuit closed. Bulb illuminating. Conductor wiring ice-cold.       │
│    SOVEREIGN HUMAN NODE CONNECTED TO PHYSICAL REALITY.                  │
└────────────────────────────────────────────────────────────────────────┘"""

    html = html.replace(ru_ascii_6, en_ascii_6)

    # Section 10 Conclusion
    html = html.replace('<h2>10. Заключение: Архитектура суверенной цивилизации</h2>', '<h2>10. Conclusion: Architecture of a Sovereign Civilization</h2>')
    html = html.replace(
        '<p>Протокол «Внутренний ток» снимает с человеческого благополучия двухтысячелетний налёт гуманитарной беспомощности и религиозно-эзотерического фатализма.</p>',
        '<p>The Inner Current Protocol strips human well-being of millennia of psychological helplessness and esoteric fatalism.</p>'
    )
    html = html.replace(
        '<li><strong>Человек не сломан.</strong> В его природе нет встроенного дефекта. Страдание — это не проклятие, а точный физический сигнал мультиметра о наличии паразитного омического сопротивления в цепи.</li>',
        '<li><strong>Human beings are not broken.</strong> There is no built-in flaw in human nature. Suffering is not a divine curse, but a precise multimeter reading signaling parasitic ohmic resistance in the loop.</li>'
    )
    html = html.replace(
        '<li><strong>В вещах нет счастья.</strong> Ни одна внешняя лампа не имеет встроенной батарейки ($\\mathcal{E}_{\\text{load}} \\equiv 0$). Жизнь светится только тогда, когда сквозь неё течёт свободный ток внимания оператора.</li>',
        '<li><strong>Objects do not hold happiness.</strong> No external bulb has an internal battery ($\\mathcal{E}_{\\text{load}} \\equiv 0$). Life illuminates only when the operator\'s free current of attention passes through it.</li>'
    )
    html = html.replace(
        '<li><strong>Два контура — основа устойчивости.</strong> Контур I (Тело Пригожина) поставляет метаболическую энергию жизни; Контур II (Дух Аньянова) преобразует её в порядок, творчество и сверхпроводимость через прямое действие (Proof-of-Action).</li>',
        '<li><strong>Two circuits form the bedrock of resilience.</strong> Circuit I (Prigogine Body) supplies metabolic vital energy; Circuit II (Anyanov Spirit) transduces it into order, craft, and superconductivity via direct action (Proof-of-Action).</li>'
    )
    html = html.replace(
        '<p>Каждый родившийся человек является полноценной, автономной, суверенной нодой этой вселенской электродинамической сети. Чтобы войти в состояние несокрушимого мира и творческой мощи, оператору не требуются посредники, культы или внешние клиринговые палаты.</p>',
        '<p>Every human being is a complete, autonomous, sovereign node of this universal electrodynamic network. To enter an unshakable state of peace and creative power, the operator requires no intermediaries, no gurus, and no external clearinghouses.</p>'
    )
    html = html.replace(
        '<p><strong>Достаточно запереть свой контур, охладить проводку внимания до сверхпроводимости и зажечь лампы прямого действия.</strong></p>',
        '<p><strong>It is enough to close your circuit, cool the wiring of attention into superconductivity, and illuminate the bulbs of direct action.</strong></p>'
    )

    # References
    html = html.replace('<h2>📚 Литература (References)</h2>', '<h2>📚 References</h2>')
    html = html.replace('Нобелевская лекция по химии.', 'Nobel Lecture in Chemistry.')
    html = html.replace('О теплоте, выделяемой металлическими проводниками при прохождении электричества.', 'On the heat produced by metallic conductors of electricity.')
    html = html.replace('О законах выделения тепла гальваническим током.', 'On the laws of heat dissipation by galvanic currents.')
    html = html.replace('Записки Императорской Академии Наук Санкт-Петербурга.', 'Proceedings of the Imperial Academy of Sciences, St. Petersburg.')
    html = html.replace('О законах распределения электрических токов в разветвленных проводниках.', 'On the laws of distribution of electrical currents in branched conductors.')
    html = html.replace('Фудосин Синсэцу (Записи о непоколебимой мудрости) — трактат о природе состояния Мусин.', 'Fudōshin Shinsetsu (The Mysterious Record of Immovable Wisdom) — on the nature of Mushin.')
    html = html.replace('Логика научного исследования (Logik der Forschung).', 'The Logic of Scientific Discovery (Logik der Forschung).')
    html = html.replace('Что такое жизнь с точки зрения физики?', 'What is Life? The Physical Aspect of the Living Cell.')
    html = html.replace('Архитектура Внутреннего Тока: Двухконтурная электродинамика сознания, каскадные диссипативные системы и онтология счастья.', 'Architecture of the Inner Current: Dual-Circuit Consciousness Electrodynamics, Cascading Dissipative Systems, and the Ontology of Happiness.')

    # Footer
    html = html.replace('© 2026 Владимир Аньянов • Архитектура Внутреннего Тока (Inner Current)', '© 2026 Vladimir Anyanov • Architecture of the Inner Current')
    html = html.replace('Открытый протокол человеческого благополучия и суверенной сверхпроводимости.', 'The open protocol of human well-being and sovereign superconductivity.')
    html = html.replace('Скачать White Paper в PDF', 'Download White Paper (PDF)')
    html = html.replace('>Манифест<', '>Manifesto<')
    html = html.replace('Библиотека «Золотая Семёрка»', 'The Golden Seven Library')
    html = html.replace('href="books/whitepaper.pdf"', 'href="../books/whitepaper.pdf"')

    en_wp_path = os.path.join(DIST_DIR, "en", "whitepaper.html")
    with open(en_wp_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated: {en_wp_path}")

    # Create /en/whitepaper/index.html
    en_wp_dir = os.path.join(DIST_DIR, "en", "whitepaper")
    os.makedirs(en_wp_dir, exist_ok=True)
    shutil.copyfile(en_wp_path, os.path.join(en_wp_dir, "index.html"))

    # Sync to public/
    shutil.copyfile(en_wp_path, os.path.join(PUBLIC_DIR, "en", "whitepaper.html"))
    pub_wp_dir = os.path.join(PUBLIC_DIR, "en", "whitepaper")
    os.makedirs(pub_wp_dir, exist_ok=True)
    shutil.copyfile(en_wp_path, os.path.join(pub_wp_dir, "index.html"))
    print("Synchronized English Whitepaper to public/en/whitepaper.html")

def update_en_index():
    """Updates dist_site/en/index.html and dist_site/en.html with Manifesto and White Paper links"""
    for file_path in [os.path.join(DIST_DIR, "en", "index.html"), os.path.join(DIST_DIR, "en.html")]:
        if not os.path.exists(file_path):
            continue
        with open(file_path, "r", encoding="utf-8") as f:
            html = f.read()

        # 1. Update top navbar
        en_nav_links = """      <!-- Desktop Nav Links -->
      <div class="hidden md:flex items-center gap-5 text-xs font-medium text-slate-300">
        <a href="manifesto.html" class="hover:text-amber-200 transition flex items-center gap-1.5 text-amber-300 font-bold px-2.5 py-1 rounded-lg bg-amber-500/15 border border-amber-500/30"><span>⚡</span> Manifesto</a>
        <a href="whitepaper.html" class="hover:text-sky-300 transition flex items-center gap-1.5 text-slate-300 font-semibold px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800 hover:border-sky-500/40"><span>📄</span> Whitepaper</a>
        <a href="#books" class="hover:text-amber-300 transition">Books (7)</a>
        <a href="#reader" class="hover:text-amber-300 transition">Reader</a>
        <a href="#audiobook" class="hover:text-cyan-300 transition flex items-center gap-1">
          <span>🎧</span> Audio
        </a>
        <a href="/en/flashlight/" class="hover:text-amber-300 transition flex items-center gap-1">
          <span>🔦</span> Flashlight
        </a>
        <a href="/en/human/" class="hover:text-amber-300 transition flex items-center gap-1">
          <span>🧘</span> Human
        </a>
        <a href="#monographs" class="hover:text-slate-100 transition">PDF</a>
      </div>"""

        old_nav_links = """      <!-- Desktop Nav Links -->
      <div class="hidden md:flex items-center gap-6 text-sm font-medium text-slate-300">
        <a href="#books" class="hover:text-amber-300 transition">Books</a>
        <a href="#reader" class="hover:text-amber-300 transition">Online Reader</a>
        <a href="#audiobook" class="hover:text-cyan-300 transition flex items-center gap-1.5">
          <span>🎧</span> Audiobook
        </a>
        <a href="#flashlight" class="hover:text-amber-300 transition flex items-center gap-1.5">
          <span>🔦</span> Zen Flashlight
        </a>
        <a href="/en/human/" class="hover:text-amber-300 transition flex items-center gap-1.5">
          <span>🧘</span> Human Circuit
        </a>
        <a href="#monographs" class="hover:text-slate-100 transition">PDF Materials</a>
        <a href="#principles" class="hover:text-slate-100 transition">Principles</a>
      </div>"""

        if old_nav_links in html:
            html = html.replace(old_nav_links, en_nav_links, 1)

        # 2. Update Hero CTA buttons
        en_hero_buttons = """      <!-- Quick Action Buttons -->
      <div class="mt-10 flex flex-wrap items-center justify-center gap-4">
        <a href="manifesto.html" class="px-7 py-3.5 rounded-xl bg-gradient-to-r from-amber-500 via-amber-400 to-amber-300 hover:from-amber-400 hover:to-amber-200 text-slate-950 font-black text-sm transition shadow-xl shadow-amber-500/30 flex items-center gap-2 transform hover:-translate-y-0.5">
          <span class="text-base">⚡</span> <span>Read Manifesto</span>
        </a>
        <a href="whitepaper.html" class="px-6 py-3.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-sky-300 border border-sky-500/40 font-bold text-sm transition shadow-lg shadow-sky-500/10 flex items-center gap-2">
          <span>📄</span> <span>White Paper</span>
        </a>
        <a href="#reader" class="px-6 py-3.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-amber-300 border border-amber-500/40 font-bold text-sm transition shadow-lg shadow-amber-500/10 flex items-center gap-2">
          <span>📖</span> <span>Online Reader</span>
        </a>
        <a href="#audiobook" class="px-6 py-3.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-cyan-300 border border-cyan-500/40 font-semibold text-sm transition flex items-center gap-2 shadow-lg shadow-cyan-500/10">
          <span>🎧</span> <span>Audiobook Online</span>
        </a>
        <a href="#books" class="px-6 py-3.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 font-semibold text-sm transition flex items-center gap-2">
          <span>📚</span> <span>Overview (7 Books)</span>
        </a>
      </div>"""

        old_hero_buttons = """      <!-- Quick Action Buttons -->
      <div class="mt-10 flex flex-wrap items-center justify-center gap-4">
        <a href="#reader" class="px-6 py-3.5 rounded-xl bg-gradient-to-r from-amber-500 to-amber-400 hover:from-amber-400 hover:to-amber-300 text-slate-950 font-bold text-sm transition shadow-lg shadow-amber-500/25 flex items-center gap-2">
          <span>📖</span> <span>Online Reader</span>
        </a>
        <a href="#audiobook" class="px-6 py-3.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-cyan-300 border border-cyan-500/40 font-semibold text-sm transition flex items-center gap-2 shadow-lg shadow-cyan-500/10">
          <span>🎧</span> <span>Audiobook Online</span>
        </a>
        <a href="#books" class="px-6 py-3.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 font-semibold text-sm transition flex items-center gap-2">
          <span>📚</span> <span>Overview of All Books</span>
        </a>
      </div>"""

        if old_hero_buttons in html:
            html = html.replace(old_hero_buttons, en_hero_buttons, 1)

        # 3. Update Book 6 card: add "Read Online" button
        old_wp_card_btns = """        <div class="pt-5 mt-4 border-t border-slate-800/80 flex items-center gap-2">
          <a href="../books/whitepaper.pdf" download class="flex-1 py-2.5 px-3 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs transition text-center shadow-lg shadow-emerald-500/20">
            📥 Download PDF
          </a>
          <a href="../books/whitepaper.pdf" target="_blank" class="p-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 text-xs transition">
            ↗
          </a>
        </div>"""

        new_wp_card_btns = """        <div class="pt-5 mt-4 border-t border-slate-800/80 flex items-center gap-2">
          <a href="whitepaper.html" class="flex-1 py-2.5 px-3 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs transition text-center shadow-lg shadow-emerald-500/20">
            📖 Read Online
          </a>
          <a href="../books/whitepaper.pdf" download title="Download PDF" class="p-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 text-xs transition flex items-center justify-center">
            📥
          </a>
          <a href="whitepaper.html" target="_blank" title="Open in new tab" class="p-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 text-xs transition">
            ↗
          </a>
        </div>"""

        if old_wp_card_btns in html:
            html = html.replace(old_wp_card_btns, new_wp_card_btns, 1)

        # 4. Update Footer
        old_en_footer = """        <a href="#principles" class="hover:text-amber-300 transition">Principles</a>
        <span>•</span>
        <a href="/en/human/" class="hover:text-amber-300 transition">Human Circuit</a>
        <span>•</span>
        <a href="#audiobook" class="hover:text-cyan-300 transition">Audiobook</a>"""

        new_en_footer = """        <a href="manifesto.html" class="text-amber-300 font-bold hover:text-amber-200 transition">⚡ Manifesto</a>
        <span>•</span>
        <a href="whitepaper.html" class="text-sky-300 font-semibold hover:text-sky-200 transition">📄 White Paper</a>
        <span>•</span>
        <a href="#principles" class="hover:text-amber-300 transition">Principles</a>
        <span>•</span>
        <a href="/en/human/" class="hover:text-amber-300 transition">Human Circuit</a>
        <span>•</span>
        <a href="#audiobook" class="hover:text-cyan-300 transition">Audiobook</a>"""

        if old_en_footer in html:
            html = html.replace(old_en_footer, new_en_footer, 1)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Updated: {file_path}")

    # Sync dist_site/en/index.html to public/en/index.html
    shutil.copyfile(os.path.join(DIST_DIR, "en", "index.html"), os.path.join(PUBLIC_DIR, "en", "index.html"))
    print("Synchronized public/en/index.html")

if __name__ == "__main__":
    print("=== ⚡ Generating English Manifesto and White Paper ===")
    update_russian_manifesto()
    update_russian_whitepaper()
    build_en_manifesto()
    build_en_whitepaper()
    update_en_index()
    print("=== 🚀 Done! ===")
