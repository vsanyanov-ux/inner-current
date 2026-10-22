import os
import re
import sys

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current"
INDEX_PATH = os.path.join(ROOT_DIR, "dist_site", "index.html")
PUBLIC_INDEX = os.path.join(ROOT_DIR, "public", "index.html")

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update title and meta
html = html.replace(
    "<title>Внутренний ток — Библиотека прикладных книг и руководств</title>",
    "<title>Внутренний ток — Библиотека «Золотая Семёрка 2.0» и Дом Внутреннего Тока</title>"
)

# 2. Add 'Дом Внутреннего Тока' to desktop nav
old_nav = '<a href="#books" class="hover:text-amber-300 transition">Книги</a>'
new_nav = '<a href="#house" class="hover:text-amber-300 transition flex items-center gap-1.5 text-amber-400 font-semibold"><span>🏛️</span> Дом Внутреннего Тока</a>\n        <a href="#books" class="hover:text-amber-300 transition">Книги (7)</a>'
if old_nav in html and 'href="#house"' not in html:
    html = html.replace(old_nav, new_nav, 1)

# 3. Update Hero Badge and Subtitle
old_hero_badge = '<span>⚡</span> ВНУТРЕННИЙ ТОК • 7 КНИГ И РУКОВОДСТВ'
new_hero_badge = '<span>🏛️</span> СИСТЕМА АНЬЯНОВА • ЗОЛОТАЯ СЕМЁРКА 2.0'
if old_hero_badge in html:
    html = html.replace(old_hero_badge, new_hero_badge, 1)

old_hero_sub = 'Практическая схемотехника человека: от экспресс-отладки острой боли и перегрузки до прикладной акустики, соматики и синтеза законов физики с природой сознания.'
new_hero_sub = 'Архитектура «Дома Внутреннего Тока»: от соматического фундамента человека ($NN=1) и топологии четверичного фрактала (C₄) до термодинамики негэнтропии и макроистории цивилизации.'
if old_hero_sub in html:
    html = html.replace(old_hero_sub, new_hero_sub, 1)

# 4. Add "Дом Внутреннего Тока" button to Hero actions
old_hero_actions = '<a href="#books" class="px-6 py-3.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 font-semibold text-sm transition flex items-center gap-2">\n          <span>📚</span> <span>Обзор всех изданий</span>\n        </a>'
new_hero_actions = '<a href="#house" class="px-6 py-3.5 rounded-xl bg-amber-500/15 hover:bg-amber-500/25 text-amber-300 border border-amber-500/40 font-semibold text-sm transition flex items-center gap-2 shadow-lg shadow-amber-500/10">\n          <span>🏛️</span> <span>Дом Внутреннего Тока</span>\n        </a>\n        <a href="#books" class="px-6 py-3.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 font-semibold text-sm transition flex items-center gap-2">\n          <span>📚</span> <span>Золотая Семёрка (7 книг)</span>\n        </a>'
if old_hero_actions in html:
    html = html.replace(old_hero_actions, new_hero_actions, 1)

# 5. Insert HOUSE SECTION right before the BOOKS section
house_section_html = r'''  <!-- ========================================================= -->
  <!-- SECTION: THE HOUSE OF INNER CURRENT (ДОМ ВНУТРЕННЕГО ТОКА) -->
  <!-- ========================================================= -->
  <section id="house" class="py-16 md:py-24 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 border-b border-slate-800/80">
    <div class="text-center max-w-3xl mx-auto mb-12">
      <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/15 text-amber-300 border border-amber-500/30 text-xs font-mono font-medium tracking-wider mb-4">
        <span>🏛️</span> АРХИТЕКТУРНАЯ МОДЕЛЬ «ФУНДАМЕНТ → СТЕНЫ → КРЫША»
      </div>
      <h2 class="text-3xl sm:text-4xl font-extrabold text-slate-100 font-display">
        Дом Внутреннего Тока
      </h2>
      <p class="text-slate-300 text-sm sm:text-base mt-4 leading-relaxed font-serif">
        Принцип познания природы строится строго снизу вверх (<span class="font-mono text-amber-300">Ordo cognoscendi</span>): от прямого соматического опыта живого тела ($NN=1) через инвариант систем (C₄) к космологическому закону термодинамики негэнтропии.
      </p>
    </div>

    <!-- House Blueprint & Render Showcase Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center mb-16">
      
      <!-- Left: Interactive Isometric Blueprint -->
      <div class="lg:col-span-7 bg-slate-900/90 border border-amber-500/40 rounded-3xl p-4 sm:p-6 shadow-2xl relative group overflow-hidden box-glow-amber">
        <div class="relative rounded-2xl overflow-hidden bg-slate-950">
          <img src="assets/house_blueprint_cutaway.jpg" alt="Изометрический чертёж-разрез Дома Внутреннего Тока" class="w-full h-auto object-cover rounded-xl transition duration-500 group-hover:scale-[1.02]">
          <div class="absolute bottom-3 left-3 right-3 bg-slate-950/85 backdrop-blur-md border border-slate-800 p-3 rounded-xl flex items-center justify-between">
            <div class="text-xs">
              <div class="font-bold text-amber-300 font-mono">ЧЕРТЁЖ ДОМА ВНУТРЕННЕГО ТОКА</div>
              <div class="text-[11px] text-slate-400">Трёхмерный архитектурный срез: Фундамент • Стены • Крыша</div>
            </div>
            <a href="assets/house_blueprint_cutaway.jpg" target="_blank" class="px-3 py-1.5 rounded-lg bg-amber-500 text-slate-950 text-xs font-bold transition hover:bg-amber-400">
              Увеличить ↗
            </a>
          </div>
        </div>
      </div>

      <!-- Right: Tiers Breakdown -->
      <div class="lg:col-span-5 space-y-4">
        
        <!-- Tier 3: Roof -->
        <div class="p-5 rounded-2xl bg-gradient-to-r from-sky-950/30 to-slate-900 border border-sky-500/30 relative">
          <div class="flex items-center gap-3">
            <span class="text-2xl">🌌</span>
            <div>
              <div class="text-[10px] font-mono text-sky-400 font-bold uppercase tracking-wider">КРЫША И КОСМИЧЕСКИЙ КУПОЛ</div>
              <h4 class="text-base font-bold text-slate-100">Книга 3: Универсальный закон потоковых систем</h4>
            </div>
          </div>
          <p class="text-xs text-slate-300 mt-2 font-serif leading-relaxed">
            Термодинамика негэнтропии, открытые системы, экспорт энтропии наружу и формула КПД бытия $H = P_load / P_total$.
          </p>
          <div class="mt-3 flex items-center gap-2">
            <button onclick="readBookInReader('03_universal_law')" class="px-3 py-1.5 rounded-lg bg-sky-500/20 text-sky-300 border border-sky-500/40 text-xs font-semibold hover:bg-sky-500/30 transition">
              📖 Читать в ридере
            </button>
            <a href="books/03_universal_law.pdf" download class="px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300 text-xs font-medium hover:text-white transition">
              📥 PDF (42 стр.)
            </a>
          </div>
        </div>

        <!-- Tier 2: Walls -->
        <div class="p-5 rounded-2xl bg-gradient-to-r from-amber-950/30 to-slate-900 border border-amber-500/30 relative">
          <div class="flex items-center gap-3">
            <span class="text-2xl">🏛️</span>
            <div>
              <div class="text-[10px] font-mono text-amber-400 font-bold uppercase tracking-wider">НЕСУЩИЕ СТЕНЫ И 4 КОЛОННЫ</div>
              <h4 class="text-base font-bold text-slate-100">Книга 2: Четверичный фрактал цепи</h4>
            </div>
          </div>
          <p class="text-xs text-slate-300 mt-2 font-serif leading-relaxed">
            Топологический инвариант (C₄): 4 узла цепи в природе, клетке, человеке, Биткоине и обществе. Теория депосреднизации (Zero Parasitic Rent).
          </p>
          <div class="mt-3 flex items-center gap-2">
            <button onclick="readBookInReader('02_quaternary_fractal')" class="px-3 py-1.5 rounded-lg bg-amber-500/20 text-amber-300 border border-amber-500/40 text-xs font-semibold hover:bg-amber-500/30 transition">
              📖 Читать в ридере
            </button>
            <a href="books/02_quaternary_fractal.pdf" download class="px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300 text-xs font-medium hover:text-white transition">
              📥 PDF (43 стр.)
            </a>
          </div>
        </div>

        <!-- Tier 1: Foundation -->
        <div class="p-5 rounded-2xl bg-gradient-to-r from-amber-950/40 to-slate-900 border border-amber-500/50 relative shadow-lg shadow-amber-500/10">
          <div class="flex items-center gap-3">
            <span class="text-2xl">🪨</span>
            <div>
              <div class="text-[10px] font-mono text-amber-300 font-bold uppercase tracking-wider">МОНОЛИТНЫЙ ФУНДАМЕНТ (N=1)</div>
              <h4 class="text-base font-bold text-slate-100">Книга 1: Внутренний ток (Архитектура человека)</h4>
            </div>
          </div>
          <p class="text-xs text-slate-300 mt-2 font-serif leading-relaxed">
            Соматический базис человека: карманный фонарик, реактор Тандэн, проводник Мусин ($R_R_ego → 0), закон Джоуля — Ленца.
          </p>
          <div class="mt-3 flex items-center gap-2">
            <button onclick="readBookInReader('01_inner_current')" class="px-3 py-1.5 rounded-lg bg-amber-500 text-slate-950 font-bold text-xs hover:bg-amber-400 transition shadow-md shadow-amber-500/20">
              📖 Читать в ридере
            </button>
            <a href="books/01_inner_current.pdf" download class="px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300 text-xs font-medium hover:text-white transition">
              📥 PDF (218 стр.)
            </a>
          </div>
        </div>

      </div>
    </div>

    <!-- Additional Blueprint Downloads Gallery -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <a href="assets/house_blueprint_cutaway.jpg" target="_blank" class="p-4 rounded-2xl bg-slate-900 border border-slate-800 hover:border-amber-400/50 transition flex items-center gap-3 group">
        <span class="text-2xl group-hover:scale-110 transition">📐</span>
        <div class="min-w-0">
          <div class="text-xs font-bold text-slate-200 group-hover:text-amber-300 transition truncate">Изометрия Дома (3D Разрез)</div>
          <div class="text-[10px] text-slate-400">Аксонометрический чертёж JPG ↗</div>
        </div>
      </a>
      <a href="assets/house_blueprint_vector.png" target="_blank" class="p-4 rounded-2xl bg-slate-900 border border-slate-800 hover:border-amber-400/50 transition flex items-center gap-3 group">
        <span class="text-2xl group-hover:scale-110 transition">📊</span>
        <div class="min-w-0">
          <div class="text-xs font-bold text-slate-200 group-hover:text-amber-300 transition truncate">Архитектурная схема (2D)</div>
          <div class="text-[10px] text-slate-400">Поэтажный план PNG / SVG ↗</div>
        </div>
      </a>
      <a href="assets/house_concept_render.jpg" target="_blank" class="p-4 rounded-2xl bg-slate-900 border border-slate-800 hover:border-amber-400/50 transition flex items-center gap-3 group">
        <span class="text-2xl group-hover:scale-110 transition">🌄</span>
        <div class="min-w-0">
          <div class="text-xs font-bold text-slate-200 group-hover:text-amber-300 transition truncate">Концепт-арт Дома</div>
          <div class="text-[10px] text-slate-400">Кинематографический рендер ↗</div>
        </div>
      </a>
    </div>

  </section>
'''

if 'id="house"' not in html:
    books_marker = '<section id="books"'
    html = html.replace(books_marker, house_section_html + '\n  ' + books_marker, 1)

# 6. Replace the entire 7 Books Grid with the Canonical Golden Seven 2.0
new_books_section = r'''    <!-- 7 Books Grid: Golden Seven 2.0 -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

      <!-- Book 01: Inner Current (Foundation) -->
      <div class="bg-gradient-to-b from-amber-950/30 to-slate-900 border border-amber-500/40 rounded-2xl p-6 shadow-xl flex flex-col justify-between relative group hover:border-amber-400 transition-all duration-300 box-glow-amber">
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <span class="text-3xl">🪨</span>
            <span class="text-[10px] font-mono uppercase tracking-wider px-2.5 py-1 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/40 font-bold">
              Книга 1 • Фундамент (N=1)
            </span>
          </div>
          <div>
            <h3 class="text-lg font-bold text-slate-100 group-hover:text-amber-300 transition">
              Внутренний ток (Архитектура человека)
            </h3>
            <p class="text-xs text-amber-400/90 font-medium mt-1">
              Схемотехника карманного фонарика и соматическая сверхпроводимость
            </p>
          </div>
          <p class="text-xs text-slate-300 leading-relaxed font-serif">
            Фундаментальный труд соматической физики: 218 страниц, 46 разделов. Человек как электрическая цепь: батарейка Тандэн, проводник Мусин ($R_R_ego → 0), лампа созидания Гё и заземление Дзансин. Формула Джоуля — Ленца ($QQ = I²·R·t).
          </p>
        </div>
        <div class="pt-5 mt-4 border-t border-slate-800/80 flex items-center gap-2">
          <button onclick="readBookInReader('01_inner_current')" class="flex-1 py-2.5 px-3 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs transition text-center cursor-pointer shadow-md shadow-amber-500/20">
            📖 Читать в ридере
          </button>
          <a href="books/01_inner_current.pdf" download title="Скачать PDF книги (218 стр.)" class="px-3 py-2.5 rounded-xl bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 border border-amber-500/40 text-xs font-semibold transition flex items-center gap-1">
            <span>📥</span> PDF (218 с.)
          </a>
          <a href="book/index.html" target="_blank" title="Открыть в отдельной вкладке" class="p-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 text-xs transition">
            ↗
          </a>
        </div>
      </div>

      <!-- Book 02: Quaternary Fractal (Walls) -->
      <div class="bg-gradient-to-b from-amber-950/20 to-slate-900 border border-amber-500/30 rounded-2xl p-6 shadow-xl flex flex-col justify-between relative group hover:border-amber-400 transition-all duration-300">
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <span class="text-3xl">🏛️</span>
            <span class="text-[10px] font-mono uppercase tracking-wider px-2.5 py-1 rounded-full bg-amber-500/15 text-amber-300 border border-amber-500/30 font-semibold">
              Книга 2 • Стены (C4)
            </span>
          </div>
          <div>
            <h3 class="text-lg font-bold text-slate-100 group-hover:text-amber-300 transition">
              Четверичный фрактал цепи
            </h3>
            <p class="text-xs text-amber-400/90 font-medium mt-1">
              Архитектурный инвариант природы: от клетки и фонарика до Биткоина и общества
            </p>
          </div>
          <p class="text-xs text-slate-300 leading-relaxed font-serif">
            Архитектурно-топологический инвариант: 43 страницы. 4 узла контура (Источник → Проводник → Нагрузка → Обратный провод). Теория депосреднизации (Zero Parasitic Rent), Биткоин Сатоши Накамото и налог Генри Джорджа.
          </p>
        </div>
        <div class="pt-5 mt-4 border-t border-slate-800/80 flex items-center gap-2">
          <button onclick="readBookInReader('02_quaternary_fractal')" class="flex-1 py-2.5 px-3 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs transition text-center cursor-pointer shadow-md shadow-amber-500/20">
            📖 Читать в ридере
          </button>
          <a href="books/02_quaternary_fractal.pdf" download title="Скачать PDF книги (43 стр.)" class="px-3 py-2.5 rounded-xl bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 border border-amber-500/40 text-xs font-semibold transition flex items-center gap-1">
            <span>📥</span> PDF (43 с.)
          </a>
          <a href="books/quaternary_fractal.html" target="_blank" title="Открыть в отдельной вкладке" class="p-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 text-xs transition">
            ↗
          </a>
        </div>
      </div>

      <!-- Book 03: Universal Law (Roof) -->
      <div class="bg-gradient-to-b from-sky-950/25 to-slate-900 border border-sky-500/30 rounded-2xl p-6 shadow-xl flex flex-col justify-between relative group hover:border-sky-400 transition-all duration-300 box-glow-cyan">
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <span class="text-3xl">🌌</span>
            <span class="text-[10px] font-mono uppercase tracking-wider px-2.5 py-1 rounded-full bg-sky-500/15 text-sky-300 border border-sky-500/30 font-semibold">
              Книга 3 • Крыша (Космос)
            </span>
          </div>
          <div>
            <h3 class="text-lg font-bold text-slate-100 group-hover:text-sky-300 transition">
              Универсальный закон потоковых систем
            </h3>
            <p class="text-xs text-sky-400/90 font-medium mt-1">
              Термодинамика негэнтропии, открытые системы и КПД бытия
            </p>
          </div>
          <p class="text-xs text-slate-300 leading-relaxed font-serif">
            Космологическая термодинамика: 42 страницы. Неравновесная физика Больцмана, Шрёдингера и Пригожина. Каноническая формула КПД потока $\H = P_load / P_total$, три следствия и строгая фальсифицируемость по Карлу Попперу.
          </p>
        </div>
        <div class="pt-5 mt-4 border-t border-slate-800/80 flex items-center gap-2">
          <button onclick="readBookInReader('03_universal_law')" class="flex-1 py-2.5 px-3 rounded-xl bg-sky-500 hover:bg-sky-400 text-slate-950 font-bold text-xs transition text-center cursor-pointer shadow-md shadow-sky-500/20">
            📖 Читать в ридере
          </button>
          <a href="books/03_universal_law.pdf" download title="Скачать PDF книги (42 стр.)" class="px-3 py-2.5 rounded-xl bg-sky-500/20 hover:bg-sky-500/30 text-sky-300 border border-sky-500/40 text-xs font-semibold transition flex items-center gap-1">
            <span>📥</span> PDF (42 с.)
          </a>
          <a href="books/universal_law.html" target="_blank" title="Открыть в отдельной вкладке" class="p-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 text-xs transition">
            ↗
          </a>
        </div>
      </div>

      <!-- Book 04: Kids Primer -->
      <div class="bg-gradient-to-b from-amber-950/20 to-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-col justify-between relative group hover:border-amber-500/40 transition-all duration-300">
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <span class="text-3xl">🧸</span>
            <span class="text-[10px] font-mono uppercase tracking-wider px-2.5 py-1 rounded-full bg-amber-500/15 text-amber-300 border border-amber-500/30 font-semibold">
              Книга 4 • Детская (10+)
            </span>
          </div>
          <div>
            <h3 class="text-lg font-bold text-slate-100 group-hover:text-amber-300 transition">
              Тайна карманного фонарика
            </h3>
            <p class="text-xs text-amber-400/90 font-medium mt-1">
              Внутренний ток для детей и подростков — как устроена твоя суперсила
            </p>
          </div>
          <p class="text-xs text-slate-300 leading-relaxed font-serif">
            Детский праймер: 11 страниц. Батарейка в животике, кнопка действия и чистый луч внимания. Почему обижаться — это жечь свои проводки, и как сберечь проводимость с юных лет.
          </p>
        </div>
        <div class="pt-5 mt-4 border-t border-slate-800/80 flex items-center gap-2">
          <button onclick="readBookInReader('04_primer')" class="flex-1 py-2.5 px-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold text-xs transition text-center cursor-pointer border border-slate-700">
            📖 Читать в ридере
          </button>
          <a href="books/04_flashlight_primer.pdf" download title="Скачать PDF книги (11 стр.)" class="px-3 py-2.5 rounded-xl bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 border border-amber-500/40 text-xs font-semibold transition flex items-center gap-1">
            <span>📥</span> PDF (11 с.)
          </a>
          <a href="books/primer_flashlight.html" target="_blank" title="Открыть в отдельной вкладке" class="p-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 text-xs transition">
            ↗
          </a>
        </div>
      </div>

      <!-- Book 05: Field Manual -->
      <div class="bg-gradient-to-b from-amber-950/20 to-slate-900 border border-amber-500/30 rounded-2xl p-6 shadow-xl flex flex-col justify-between relative group hover:border-amber-400 transition-all duration-300">
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <span class="text-3xl">🧰</span>
            <span class="text-[10px] font-mono uppercase tracking-wider px-2.5 py-1 rounded-full bg-amber-500/15 text-amber-300 border border-amber-500/30 font-semibold">
              Книга 5 • Аптечка (30 сек)
            </span>
          </div>
          <div>
            <h3 class="text-lg font-bold text-slate-100 group-hover:text-amber-300 transition">
              Полевой мануал оператора
            </h3>
            <p class="text-xs text-amber-400/90 font-medium mt-1">
              Карманная аптечка первой помощи — 30-секундный протокол соматической отладки
            </p>
          </div>
          <p class="text-xs text-slate-300 leading-relaxed font-serif">
            Скорая помощь при остром стрессе и выгорании: 31 страница. Сброс аварийных кодов ошибок DTC OBD-II сознания, соматический сброс, запуск с толкача Black Start и тест мурашек.
          </p>
        </div>
        <div class="pt-5 mt-4 border-t border-slate-800/80 flex items-center gap-2">
          <button onclick="readBookInReader('05_field_manual')" class="flex-1 py-2.5 px-3 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs transition text-center cursor-pointer shadow-md shadow-amber-500/20">
            📖 Читать в ридере
          </button>
          <a href="books/05_field_manual.pdf" download title="Скачать PDF книги (31 стр.)" class="px-3 py-2.5 rounded-xl bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 border border-amber-500/40 text-xs font-semibold transition flex items-center gap-1">
            <span>📥</span> PDF (31 с.)
          </a>
          <a href="books/field_manual.html" target="_blank" title="Открыть в отдельной вкладке" class="p-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 text-xs transition">
            ↗
          </a>
        </div>
      </div>

      <!-- Book 06: Ukulele of Being -->
      <div class="bg-gradient-to-b from-sky-950/15 to-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-col justify-between relative group hover:border-sky-500/40 transition-all duration-300">
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <span class="text-3xl">🎶</span>
            <span class="text-[10px] font-mono uppercase tracking-wider px-2.5 py-1 rounded-full bg-sky-500/15 text-sky-300 border border-sky-500/30 font-semibold">
              Книга 6 • Гостиная (Акустика)
            </span>
          </div>
          <div>
            <h3 class="text-lg font-bold text-slate-100 group-hover:text-sky-300 transition">
              Укулеле Бытия
            </h3>
            <p class="text-xs text-sky-400/90 font-medium mt-1">
              Акустическая физика счастливой жизни — материя, звук и резонанс Мусин
            </p>
          </div>
          <p class="text-xs text-slate-300 leading-relaxed font-serif">
            Чувственный монизм: 46 страниц. 400 граммов дерева, 4 струны и снятие дуализма Декарта. Как звук рождается из материи без мистики, и почему струна под зажимом эго дребезжит.
          </p>
        </div>
        <div class="pt-5 mt-4 border-t border-slate-800/80 flex items-center gap-2">
          <button onclick="readBookInReader('06_ukulele')" class="flex-1 py-2.5 px-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold text-xs transition text-center cursor-pointer border border-slate-700">
            📖 Читать в ридере
          </button>
          <a href="books/06_ukulele.pdf" download title="Скачать PDF книги (46 стр.)" class="px-3 py-2.5 rounded-xl bg-sky-500/20 hover:bg-sky-500/30 text-sky-300 border border-sky-500/40 text-xs font-semibold transition flex items-center gap-1">
            <span>📥</span> PDF (46 с.)
          </a>
          <a href="books/ukulele.html" target="_blank" title="Открыть в отдельной вкладке" class="p-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 text-xs transition">
            ↗
          </a>
        </div>
      </div>

      <!-- Book 07: The Great Synthesis (Master Edition 2.0 Full Width Hero Card) -->
      <div class="bg-gradient-to-b from-amber-950/25 via-slate-900 to-slate-950 border border-amber-500/40 rounded-2xl p-6 md:p-8 shadow-2xl flex flex-col justify-between relative group hover:border-amber-400 transition-all duration-300 md:col-span-2 lg:col-span-3 box-glow-amber">
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <span class="text-4xl">📜</span>
            <span class="text-xs font-mono uppercase tracking-wider px-3 py-1 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/40 font-semibold">
              Книга 7 • Архив и библиотека (Макроистория)
            </span>
          </div>
          <div>
            <h3 class="text-xl md:text-2xl font-black text-slate-100 group-hover:text-amber-300 transition font-display">
              Великий Синтез (Master Edition 2.0)
            </h3>
            <p class="text-xs md:text-sm text-amber-400 font-medium mt-1">
              Революции материи, трагедия духа и электродинамика человека
            </p>
          </div>
          <p class="text-xs md:text-sm text-slate-300 leading-relaxed font-serif max-w-4xl">
            Макроисторический манифест: 52 страницы. 10 000 лет цивилизации: от открытия огня через конденсатор Уатта, автомобиль Карла Бенца и Биткоин к искусственному интеллекту. Преодоление 2500-летнего раскола Запада и Востока и замыкание двух абсолютных вершин познания (Дзен изнутри $R_R_ego → 0 и диссипативные структуры Пригожина снаружи).
          </p>
        </div>
        <div class="pt-6 mt-4 border-t border-slate-800/80 flex flex-wrap items-center gap-3">
          <button onclick="readBookInReader('07_great_synthesis')" class="flex-1 min-w-[200px] py-3 px-5 rounded-xl bg-gradient-to-r from-amber-500 to-amber-400 hover:from-amber-400 hover:to-amber-300 text-slate-950 font-bold text-sm transition text-center cursor-pointer shadow-lg shadow-amber-500/25 flex items-center justify-center gap-2">
            <span>📖</span> <span>Читать в ридере онлайн</span>
          </button>
          <a href="books/07_great_synthesis.pdf" download title="Скачать PDF книги (52 стр., Master Edition 2.0)" class="py-3 px-5 rounded-xl bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 border border-amber-500/40 text-sm font-semibold transition flex items-center gap-2">
            <span>📥</span> PDF книги (52 стр., Master Edition 2.0)
          </a>
          <a href="books/great_synthesis.html" target="_blank" title="Открыть в отдельной вкладке" class="p-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 text-sm transition">
            ↗ На весь экран
          </a>
        </div>
      </div>

    </div>'''

# Replace books grid using regex pattern matching the grid container
grid_regex = re.compile(r'<!-- 7 Books Grid -->[\s\S]*?</div>\s*</section>', re.MULTILINE)
if grid_regex.search(html):
    html = grid_regex.sub(lambda m: new_books_section + '\n  </section>', html, count=1)
    print("Replaced 7 Books Grid successfully!")
else:
    print("WARNING: Grid pattern not matched directly!")

# 7. Update Reader Tabs in the Reader Bar
reader_buttons_html = '''        <div class="flex items-center gap-2 overflow-x-auto pb-1 sm:pb-0 w-full sm:w-auto">
          <span class="text-xs text-slate-400 font-mono uppercase tracking-wider mr-2 hidden lg:inline">Ридер:</span>
          
          <button id="rbtn-01_inner_current" onclick="readBookInReader('01_inner_current')" class="px-3.5 py-2 rounded-xl text-xs font-semibold transition cursor-pointer bg-slate-800 text-slate-300 hover:text-white shrink-0">
            🪨 1. Внутренний ток
          </button>
          <button id="rbtn-02_quaternary_fractal" onclick="readBookInReader('02_quaternary_fractal')" class="px-3.5 py-2 rounded-xl text-xs font-semibold transition cursor-pointer bg-slate-800 text-slate-300 hover:text-white shrink-0">
            🏛️ 2. Четверичный фрактал
          </button>
          <button id="rbtn-03_universal_law" onclick="readBookInReader('03_universal_law')" class="px-3.5 py-2 rounded-xl text-xs font-semibold transition cursor-pointer bg-slate-800 text-slate-300 hover:text-white shrink-0">
            🌌 3. Универсальный закон
          </button>
          <button id="rbtn-04_primer" onclick="readBookInReader('04_primer')" class="px-3.5 py-2 rounded-xl text-xs font-semibold transition cursor-pointer bg-slate-800 text-slate-300 hover:text-white shrink-0">
            🧸 4. Тайна фонарика
          </button>
          <button id="rbtn-05_field_manual" onclick="readBookInReader('05_field_manual')" class="px-3.5 py-2 rounded-xl text-xs font-semibold transition cursor-pointer bg-amber-500 text-slate-950 font-bold shrink-0 shadow-md shadow-amber-500/20">
            🧰 5. Полевой мануал
          </button>
          <button id="rbtn-06_ukulele" onclick="readBookInReader('06_ukulele')" class="px-3.5 py-2 rounded-xl text-xs font-semibold transition cursor-pointer bg-slate-800 text-slate-300 hover:text-white shrink-0">
            🎶 6. Укулеле Бытия
          </button>
          <button id="rbtn-07_great_synthesis" onclick="readBookInReader('07_great_synthesis')" class="px-3.5 py-2 rounded-xl text-xs font-semibold transition cursor-pointer bg-slate-800 text-slate-300 hover:text-white shrink-0">
            📜 7. Великий Синтез
          </button>
        </div>'''

reader_bar_regex = re.compile(r'<div class="flex items-center gap-2 overflow-x-auto pb-1 sm:pb-0 w-full sm:w-auto">[\s\S]*?</div>\s*<div class="flex items-center gap-2">', re.MULTILINE)
if reader_bar_regex.search(html):
    html = reader_bar_regex.sub(lambda m: reader_buttons_html + '\n\n        <div class="flex items-center gap-2">', html, count=1)
    print("Replaced Reader buttons successfully!")

# 8. Update JavaScript Reader Mapping
new_js = '''    // --- 1. Interactive Book Reader Logic (Golden Seven 2.0) ---
    const bookSrcMap = {
      '01_inner_current': 'book/index.html',
      '02_quaternary_fractal': 'books/quaternary_fractal.html',
      '03_universal_law': 'books/universal_law.html',
      '04_primer': 'books/primer_flashlight.html',
      '05_field_manual': 'books/field_manual.html',
      '06_ukulele': 'books/ukulele.html',
      '07_great_synthesis': 'books/great_synthesis.html',
      // backward aliases
      'field_manual': 'books/field_manual.html',
      'canonical': 'book/index.html',
      'copernicus': 'books/copernicus.html',
      'ukulele': 'books/ukulele.html',
      'primer': 'books/primer_flashlight.html',
      'great_synthesis': 'books/great_synthesis.html'
    };

    function readBookInReader(bookKey) {
      const iframe = document.getElementById('mainBookIframe');
      const extBtn = document.getElementById('readerExternalBtn');
      const keys = [
        '01_inner_current', '02_quaternary_fractal', '03_universal_law',
        '04_primer', '05_field_manual', '06_ukulele', '07_great_synthesis'
      ];
      
      // map aliases to canonical keys for button highlighting
      const aliasMap = {
        'canonical': '01_inner_current',
        'primer': '04_primer',
        'field_manual': '05_field_manual',
        'ukulele': '06_ukulele',
        'great_synthesis': '07_great_synthesis'
      };
      const activeKey = aliasMap[bookKey] || bookKey;

      keys.forEach(k => {
        const btn = document.getElementById('rbtn-' + k);
        if (btn) {
          if (k === activeKey) {
            btn.className = 'px-3.5 py-2 rounded-xl text-xs font-semibold transition cursor-pointer bg-amber-500 text-slate-950 font-bold shrink-0 shadow-md shadow-amber-500/20';
          } else {
            btn.className = 'px-3.5 py-2 rounded-xl text-xs font-semibold transition cursor-pointer bg-slate-800 text-slate-300 hover:text-white shrink-0';
          }
        }
      });

      const src = bookSrcMap[bookKey] || 'books/field_manual.html';
      if (iframe) iframe.src = src;
      if (extBtn) extBtn.href = src;

      // Scroll to reader smoothly
      const readerEl = document.getElementById('reader');
      if (readerEl) {
        readerEl.scrollIntoView({ behavior: 'smooth' });
      }
    }'''

js_regex = re.compile(r'// --- 1\. Interactive Book Reader Logic ---[\s\S]*?// --- 2\. Quick Audiobook Player Logic ---', re.MULTILINE)
if js_regex.search(html):
    html = js_regex.sub(lambda m: new_js + '\n\n    // --- 2. Quick Audiobook Player Logic ---', html, count=1)
    print("Replaced JS reader logic successfully!")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Updated {INDEX_PATH} ({len(html)} bytes)")

with open(PUBLIC_INDEX, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Updated {PUBLIC_INDEX} ({len(html)} bytes)")
