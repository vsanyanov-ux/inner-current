# -*- coding: utf-8 -*-
"""
apply_sidebar.py
Integrates the responsive Left Sidebar across innercurrent.ru portal:
- index.html (Main portal & library)
- manifesto.html (Manifesto)
- whitepaper.html (Master Protocol Whitepaper)
Syncs both dist_site and public.
"""
import os
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST_DIR = os.path.join(ROOT_DIR, "dist_site")
PUBLIC_DIR = os.path.join(ROOT_DIR, "public")

SIDEBAR_CSS = """    /* ========================================================= */
    /* LEFT SIDEBAR STYLES (INNERCURRENT.RU) */
    /* ========================================================= */
    .custom-sidebar-scroll::-webkit-scrollbar {
      width: 4px;
    }
    .custom-sidebar-scroll::-webkit-scrollbar-track {
      background: rgba(9, 13, 22, 0.4);
    }
    .custom-sidebar-scroll::-webkit-scrollbar-thumb {
      background: #1e293b;
      border-radius: 2px;
    }
    .custom-sidebar-scroll::-webkit-scrollbar-thumb:hover {
      background: #f59e0b;
    }
    .sidebar-nav-item.active {
      background: rgba(245, 158, 11, 0.12) !important;
      border-color: rgba(245, 158, 11, 0.4) !important;
      color: #fcd34d !important;
      font-weight: 600 !important;
    }
    .sidebar-nav-item.active .sidebar-icon {
      filter: drop-shadow(0 0 6px rgba(245, 158, 11, 0.6));
    }
"""

def get_sidebar_html(page_type="index"):
    prefix = "" if page_type == "index" else "index.html"
    
    manifesto_active = ' active' if page_type == "manifesto" else ''
    whitepaper_active = ' active' if page_type == "whitepaper" else ''
    
    return f"""  <!-- ========================================================= -->
  <!-- LEFT SIDEBAR & MOBILE DRAWER OVERLAY -->
  <!-- ========================================================= -->
  <div id="sidebar-backdrop" onclick="toggleSidebarMobile(false)" class="fixed inset-0 z-40 bg-slate-950/80 backdrop-blur-sm hidden transition-opacity duration-300 lg:hidden"></div>

  <aside id="app-sidebar" class="fixed top-0 bottom-0 left-0 z-50 w-72 bg-[#070c18]/95 backdrop-blur-xl border-r border-slate-800/80 flex flex-col transition-transform duration-300 ease-in-out -translate-x-full lg:translate-x-0 shadow-2xl">
    
    <!-- Sidebar Header & Brand -->
    <div class="h-16 px-4 border-b border-slate-800/80 flex items-center justify-between shrink-0 bg-slate-950/70">
      <a href="{prefix}#" class="flex items-center gap-2.5 group">
        <div class="w-8 h-8 rounded-xl bg-gradient-to-tr from-amber-500 to-amber-300 text-slate-950 font-black text-lg flex items-center justify-center shadow-md shadow-amber-500/20 group-hover:scale-105 transition">
          ⚡
        </div>
        <div>
          <div class="font-display font-bold text-sm tracking-wide text-slate-100 group-hover:text-amber-300 transition">
            INNER CURRENT
          </div>
          <div class="text-[9px] uppercase font-mono tracking-widest text-slate-400 font-semibold">
            innercurrent.ru
          </div>
        </div>
      </a>
      
      <div class="flex items-center gap-1">
        <!-- Collapse on Desktop -->
        <button onclick="toggleSidebarDesktop()" title="Свернуть сайдбар [Ctrl+B или [ ]" class="hidden lg:flex p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800/80 transition cursor-pointer">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 19l-7-7 7-7m8 14l-7-7 7-7"/></svg>
        </button>
        <!-- Close on Mobile -->
        <button onclick="toggleSidebarMobile(false)" title="Закрыть меню" class="lg:hidden p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition cursor-pointer">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>
    </div>

    <!-- Telemetry Status Bar -->
    <div class="px-4 py-2 bg-slate-900/60 border-b border-slate-800/60 flex items-center justify-between text-[11px] font-mono">
      <span class="flex items-center gap-2 text-emerald-400 font-medium">
        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        Цепь замкнута
      </span>
      <span class="text-slate-400 text-[10px]">7 книг • 500+ ст.</span>
    </div>

    <!-- Live Section Search -->
    <div class="p-3 border-b border-slate-800/60">
      <div class="relative">
        <input 
          type="text" 
          id="sidebar-search-input" 
          oninput="filterSidebar(this.value)" 
          placeholder="Быстрый поиск раздела..." 
          class="w-full bg-slate-950/80 border border-slate-800 focus:border-amber-500/60 rounded-xl px-3 py-1.5 text-xs text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-1 focus:ring-amber-500/40 font-sans"
        >
        <span class="absolute right-2.5 top-1/2 -translate-y-1/2 text-[10px] font-mono text-slate-500 pointer-events-none">/</span>
      </div>
    </div>

    <!-- Navigation Scroll Container -->
    <div id="sidebar-nav-container" class="flex-1 overflow-y-auto px-3 py-3 space-y-5 custom-sidebar-scroll">
      
      <!-- Group: Манифесты и Протоколы -->
      <div class="sidebar-group">
        <div class="text-[10px] font-mono font-bold uppercase tracking-wider text-slate-400 px-2 mb-1.5 flex items-center justify-between">
          <span>Манифесты &amp; Протоколы</span>
          <span class="text-amber-400">⚡</span>
        </div>
        <div class="space-y-1 text-xs">
          <a href="manifesto.html" class="sidebar-nav-item{manifesto_active} flex items-center justify-between gap-2 px-2.5 py-2 rounded-xl text-slate-300 hover:text-white hover:bg-slate-800/60 border border-transparent transition">
            <span class="flex items-center gap-2">
              <span class="sidebar-icon text-amber-400">⚡</span>
              <span>Манифест Тока</span>
            </span>
            <span class="text-[9px] font-mono px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30 font-bold">Free</span>
          </a>
          <a href="whitepaper.html" class="sidebar-nav-item{whitepaper_active} flex items-center justify-between gap-2 px-2.5 py-2 rounded-xl text-slate-300 hover:text-white hover:bg-slate-800/60 border border-transparent transition">
            <span class="flex items-center gap-2">
              <span class="sidebar-icon text-sky-400">📄</span>
              <span>Master Whitepaper</span>
            </span>
            <span class="text-[9px] font-mono px-1.5 py-0.5 rounded bg-sky-500/20 text-sky-300 border border-sky-500/30 font-bold">L1</span>
          </a>
          <a href="{prefix}#house" onclick="navigateSidebar('{prefix}#house')" data-section="house" class="sidebar-nav-item flex items-center gap-2 px-2.5 py-2 rounded-xl text-slate-300 hover:text-white hover:bg-slate-800/60 border border-transparent transition">
            <span class="sidebar-icon text-amber-400">🏛️</span>
            <span>Дом Внутреннего Тока</span>
          </a>
        </div>
      </div>

      <!-- Group: Библиотека Книг (Золотая Семёрка) -->
      <div class="sidebar-group">
        <div class="text-[10px] font-mono font-bold uppercase tracking-wider text-slate-400 px-2 mb-1.5 flex items-center justify-between">
          <span>Золотая Семёрка 2.0</span>
          <span class="text-slate-400">7 книг</span>
        </div>
        <div class="space-y-1 text-xs">
          <a href="{prefix}#books" onclick="navigateSidebar('{prefix}#books')" data-section="books" class="sidebar-nav-item flex items-center justify-between gap-2 px-2.5 py-2 rounded-xl text-slate-300 hover:text-white hover:bg-slate-800/60 border border-transparent transition">
            <span class="flex items-center gap-2">
              <span class="sidebar-icon text-amber-400">📚</span>
              <span class="font-semibold">Все книги (Обзор)</span>
            </span>
            <span class="text-[9px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-300">7 томов</span>
          </a>
          <a href="{prefix}#reader" onclick="navigateSidebar('{prefix}#reader')" data-section="reader" class="sidebar-nav-item flex items-center gap-2 px-2.5 py-2 rounded-xl text-slate-300 hover:text-white hover:bg-slate-800/60 border border-transparent transition">
            <span class="sidebar-icon text-amber-300">📖</span>
            <span class="font-semibold">Онлайн-ридер книг</span>
          </a>
          <a href="{prefix}#audiobook" onclick="navigateSidebar('{prefix}#audiobook')" data-section="audiobook" class="sidebar-nav-item flex items-center justify-between gap-2 px-2.5 py-2 rounded-xl text-slate-300 hover:text-white hover:bg-slate-800/60 border border-transparent transition">
            <span class="flex items-center gap-2">
              <span class="sidebar-icon text-cyan-400">🎧</span>
              <span class="font-semibold">Аудиокнига онлайн</span>
            </span>
            <span class="text-[9px] font-mono px-1.5 py-0.5 rounded bg-cyan-500/10 text-cyan-300 border border-cyan-500/20">Audio</span>
          </a>

          <!-- Вложенный список 7 книг для мгновенного чтения -->
          <div class="pt-1.5 pl-2 border-l border-slate-800 ml-3 space-y-0.5 text-[11px]">
            <button onclick="openBookFromSidebar('01_inner_current')" class="w-full text-left px-2 py-1.5 rounded-lg text-slate-400 hover:text-amber-200 hover:bg-slate-800/40 transition flex items-center gap-2">
              <span class="text-amber-400 font-mono text-[10px]">1.</span>
              <span class="truncate">Внутренний ток (Базис)</span>
            </button>
            <button onclick="openBookFromSidebar('02_quaternary_fractal')" class="w-full text-left px-2 py-1.5 rounded-lg text-slate-400 hover:text-amber-200 hover:bg-slate-800/40 transition flex items-center gap-2">
              <span class="text-sky-400 font-mono text-[10px]">2.</span>
              <span class="truncate">Четверичный фрактал (C₄)</span>
            </button>
            <button onclick="openBookFromSidebar('03_universal_law')" class="w-full text-left px-2 py-1.5 rounded-lg text-slate-400 hover:text-amber-200 hover:bg-slate-800/40 transition flex items-center gap-2">
              <span class="text-indigo-400 font-mono text-[10px]">3.</span>
              <span class="truncate">Универсальный закон</span>
            </button>
            <button onclick="openBookFromSidebar('04_primer')" class="w-full text-left px-2 py-1.5 rounded-lg text-slate-400 hover:text-amber-200 hover:bg-slate-800/40 transition flex items-center gap-2">
              <span class="text-pink-400 font-mono text-[10px]">4.</span>
              <span class="truncate">Тайна фонарика (Детям)</span>
            </button>
            <button onclick="openBookFromSidebar('05_field_manual')" class="w-full text-left px-2 py-1.5 rounded-lg text-slate-400 hover:text-amber-200 hover:bg-slate-800/40 transition flex items-center gap-2">
              <span class="text-emerald-400 font-mono text-[10px]">5.</span>
              <span class="truncate">Полевое руководство</span>
            </button>
            <button onclick="openBookFromSidebar('06_ukulele')" class="w-full text-left px-2 py-1.5 rounded-lg text-slate-400 hover:text-amber-200 hover:bg-slate-800/40 transition flex items-center gap-2">
              <span class="text-amber-400 font-mono text-[10px]">6.</span>
              <span class="truncate">Дзен-гитара &amp; Укулеле</span>
            </button>
            <button onclick="openBookFromSidebar('07_great_synthesis')" class="w-full text-left px-2 py-1.5 rounded-lg text-slate-400 hover:text-amber-200 hover:bg-slate-800/40 transition flex items-center gap-2">
              <span class="text-amber-300 font-mono text-[10px]">7.</span>
              <span class="truncate font-semibold text-amber-300">Великий Синтез 2.0</span>
            </button>
            <button onclick="openBookFromSidebar('dual_circuit')" class="w-full text-left px-2 py-1.5 rounded-lg text-slate-400 hover:text-amber-200 hover:bg-slate-800/40 transition flex items-center gap-2">
              <span class="text-amber-400 font-mono text-[10px]">⚡</span>
              <span class="truncate text-amber-400/90 font-medium">Двухконтурный каскад</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Group: Инструменты и Тренажеры -->
      <div class="sidebar-group">
        <div class="text-[10px] font-mono font-bold uppercase tracking-wider text-slate-400 px-2 mb-1.5 flex items-center justify-between">
          <span>Интерактивные приборы</span>
          <span class="text-slate-400">🎛️</span>
        </div>
        <div class="space-y-1 text-xs">
          <a href="{prefix}#flashlight" onclick="navigateSidebar('{prefix}#flashlight')" data-section="flashlight" class="sidebar-nav-item flex items-center gap-2 px-2.5 py-2 rounded-xl text-slate-300 hover:text-white hover:bg-slate-800/60 border border-transparent transition">
            <span class="sidebar-icon text-amber-400">🔦</span>
            <span>Дзен-фонарик (Схема)</span>
          </a>
          <a href="/human/" class="sidebar-nav-item flex items-center justify-between gap-2 px-2.5 py-2 rounded-xl text-slate-300 hover:text-white hover:bg-slate-800/60 border border-transparent transition">
            <span class="flex items-center gap-2">
              <span class="sidebar-icon text-sky-400">🧘</span>
              <span>Человек-контур</span>
            </span>
            <span class="text-[9px] font-mono px-1.5 py-0.5 rounded bg-sky-500/10 text-sky-300 border border-sky-500/20">3D</span>
          </a>
          <a href="trainer.html" class="sidebar-nav-item flex items-center justify-between gap-2 px-2.5 py-2 rounded-xl text-slate-300 hover:text-white hover:bg-slate-800/60 border border-transparent transition">
            <span class="flex items-center gap-2">
              <span class="sidebar-icon text-amber-400">🎛️</span>
              <span>Тренажер цепи</span>
            </span>
            <span class="text-[9px] font-mono px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30">Стенд</span>
          </a>
          <a href="cockpit.html" class="sidebar-nav-item flex items-center gap-2 px-2.5 py-2 rounded-xl text-slate-300 hover:text-white hover:bg-slate-800/60 border border-transparent transition">
            <span class="sidebar-icon text-purple-400">📊</span>
            <span>Пульт Сверхпроводимости</span>
          </a>
        </div>
      </div>

      <!-- Group: База Знаний и Документы -->
      <div class="sidebar-group">
        <div class="text-[10px] font-mono font-bold uppercase tracking-wider text-slate-400 px-2 mb-1.5 flex items-center justify-between">
          <span>База Знаний &amp; PDF</span>
          <span class="text-slate-400">📚</span>
        </div>
        <div class="space-y-1 text-xs">
          <a href="wiki.html" class="sidebar-nav-item flex items-center justify-between gap-2 px-2.5 py-2 rounded-xl text-slate-300 hover:text-white hover:bg-slate-800/60 border border-transparent transition">
            <span class="flex items-center gap-2">
              <span class="sidebar-icon text-sky-400">📚</span>
              <span>Вики-ридер (LLM Wiki)</span>
            </span>
            <span class="text-[9px] font-mono px-1.5 py-0.5 rounded bg-sky-500/20 text-sky-300 border border-sky-500/30 font-bold">500+</span>
          </a>
          <a href="{prefix}#monographs" onclick="navigateSidebar('{prefix}#monographs')" data-section="monographs" class="sidebar-nav-item flex items-center gap-2 px-2.5 py-2 rounded-xl text-slate-300 hover:text-white hover:bg-slate-800/60 border border-transparent transition">
            <span class="sidebar-icon text-slate-400">📑</span>
            <span>Материалы и брошюры PDF</span>
          </a>
          <a href="/en/" onclick="setLanguage('en')" class="sidebar-nav-item flex items-center justify-between gap-2 px-2.5 py-2 rounded-xl text-slate-300 hover:text-white hover:bg-slate-800/60 border border-transparent transition">
            <span class="flex items-center gap-2">
              <span class="sidebar-icon">🌐</span>
              <span>English Edition</span>
            </span>
            <span class="text-[9px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-300">EN</span>
          </a>
        </div>
      </div>

    </div>

    <!-- Sidebar Footer -->
    <div class="p-3 border-t border-slate-800/80 bg-slate-950/90 text-xs shrink-0 space-y-2">
      <a href="https://t.me/inner_current" target="_blank" rel="noopener noreferrer" class="w-full py-2 px-3 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 hover:border-sky-500/40 text-slate-200 transition flex items-center justify-center gap-2 font-medium text-xs">
        <span>💬</span> <span>Telegram-канал</span> ↗
      </a>
      <div class="text-[10px] text-center text-slate-400 font-mono">
        © 2026 Владимир Аньянов
      </div>
    </div>
  </aside>
"""

def get_sidebar_js(page_type="index"):
    is_index = page_type == "index"
    index_prefix = "" if is_index else "index.html"
    
    return f"""  <!-- ========================================================= -->
  <!-- SIDEBAR CONTROLLER & SCROLLSPY (INNERCURRENT.RU) -->
  <!-- ========================================================= -->
  <script>
    function toggleSidebarMobile(open) {{
      const sidebar = document.getElementById('app-sidebar');
      const backdrop = document.getElementById('sidebar-backdrop');
      if (!sidebar || !backdrop) return;
      
      if (open) {{
        sidebar.classList.remove('-translate-x-full');
        sidebar.classList.add('translate-x-0');
        backdrop.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
      }} else {{
        sidebar.classList.add('-translate-x-full');
        sidebar.classList.remove('translate-x-0');
        backdrop.classList.add('hidden');
        document.body.style.overflow = '';
      }}
    }}

    function toggleSidebarDesktop() {{
      const sidebar = document.getElementById('app-sidebar');
      const layout = document.getElementById('main-layout');
      if (!sidebar || !layout) return;

      const isCollapsed = sidebar.classList.contains('lg:-translate-x-full');
      if (isCollapsed) {{
        // Развернуть
        sidebar.classList.remove('lg:-translate-x-full');
        layout.classList.remove('lg:pl-0');
        layout.classList.add('lg:pl-72');
        localStorage.setItem('innercurrent_sidebar_desktop', 'expanded');
      }} else {{
        // Свернуть
        sidebar.classList.add('lg:-translate-x-full');
        layout.classList.remove('lg:pl-72');
        layout.classList.add('lg:pl-0');
        localStorage.setItem('innercurrent_sidebar_desktop', 'collapsed');
      }}
    }}

    // Восстановление состояния десктопного сайдбара
    (function initSidebar() {{
      if (window.innerWidth >= 1024) {{
        const pref = localStorage.getItem('innercurrent_sidebar_desktop');
        if (pref === 'collapsed') {{
          const sidebar = document.getElementById('app-sidebar');
          const layout = document.getElementById('main-layout');
          if (sidebar && layout) {{
            sidebar.classList.add('lg:-translate-x-full');
            layout.classList.remove('lg:pl-72');
            layout.classList.add('lg:pl-0');
          }}
        }}
      }}
    }})();

    // Хоткей Ctrl+B или [ для быстрого переключения сайдбара
    window.addEventListener('keydown', function(e) {{
      if ((e.ctrlKey && e.key.toLowerCase() === 'b') || (e.key === '[' && !['INPUT', 'TEXTAREA'].includes(e.target.tagName))) {{
        e.preventDefault();
        if (window.innerWidth >= 1024) {{
          toggleSidebarDesktop();
        }} else {{
          const sidebar = document.getElementById('app-sidebar');
          const isOpen = !sidebar.classList.contains('-translate-x-full');
          toggleSidebarMobile(!isOpen);
        }}
      }} else if (e.key === 'Escape') {{
        toggleSidebarMobile(false);
      }}
    }});

    // Навигация по якорю с закрытием мобильного меню
    function navigateSidebar(anchor) {{
      if (window.innerWidth < 1024) {{
        toggleSidebarMobile(false);
      }}
      if (!{str(is_index).lower()} && anchor.startsWith('index.html')) {{
        window.location.href = anchor;
      }}
    }}

    // Открытие книги в ридере из сайдбара
    function openBookFromSidebar(bookKey) {{
      if ({str(is_index).lower()}) {{
        if (typeof readBookInReader === 'function') {{
          readBookInReader(bookKey);
        }}
        const readerSection = document.getElementById('reader');
        if (readerSection) {{
          readerSection.scrollIntoView({{ behavior: 'smooth' }});
        }}
      }} else {{
        window.location.href = 'index.html?book=' + encodeURIComponent(bookKey) + '#reader';
      }}
      if (window.innerWidth < 1024) {{
        toggleSidebarMobile(false);
      }}
    }}

    // Живой фильтр разделов сайдбара
    function filterSidebar(query) {{
      const q = (query || '').toLowerCase().trim();
      const items = document.querySelectorAll('#sidebar-nav-container .sidebar-nav-item, #sidebar-nav-container button');
      items.forEach(el => {{
        const text = el.textContent.toLowerCase();
        if (!q || text.includes(q)) {{
          el.style.display = '';
        }} else {{
          el.style.display = 'none';
        }}
      }});
    }}

    // Scrollspy (только на главной странице)
    if ({str(is_index).lower()}) {{
      (function initScrollspy() {{
        const sections = ['house', 'books', 'audiobook', 'reader', 'monographs', 'flashlight'];
        const navItems = document.querySelectorAll('.sidebar-nav-item[data-section]');
        
        window.addEventListener('scroll', function() {{
          let current = '';
          const scrollY = window.pageYOffset || document.documentElement.scrollTop;
          
          sections.forEach(id => {{
            const el = document.getElementById(id);
            if (el) {{
              const top = el.offsetTop - 140;
              const height = el.offsetHeight;
              if (scrollY >= top && scrollY < top + height) {{
                current = id;
              }}
            }}
          }});
          
          navItems.forEach(item => {{
            if (item.getAttribute('data-section') === current) {{
              item.classList.add('active');
            }} else {{
              item.classList.remove('active');
            }}
          }});
        }}, {{ passive: true }});
      }})();

      // Read ?book= parameter from URL on page load
      (function checkUrlBookParam() {{
        const urlParams = new URLSearchParams(window.location.search);
        const bookParam = urlParams.get('book');
        if (bookParam && typeof readBookInReader === 'function') {{
          readBookInReader(bookParam);
        }}
      }})();
    }}
  </script>
"""

def update_manifesto_file(filepath):
    print(f"Processing manifesto: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    if "/* LEFT SIDEBAR STYLES" not in html:
        html = html.replace("</style>", SIDEBAR_CSS + "\n  </style>", 1)

    if '<aside id="app-sidebar"' not in html:
        body_pattern = r'(<body[^>]*>)'
        m = re.search(body_pattern, html)
        if not m:
            return False
        body_tag = m.group(1)

        old_nav_pattern = r'(<nav class="sticky top-0 z-50[^\n]*\n[\s\S]*?</nav>)'
        nav_match = re.search(old_nav_pattern, html)
        if not nav_match:
            return False

        new_nav = """    <!-- TOP STICKY NAVBAR -->
    <nav class="sticky top-0 z-40 bg-slate-950/90 backdrop-blur-md border-b border-slate-800/80 transition-all duration-200">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-3">
        <!-- Left: Sidebar Trigger & Brand -->
        <div class="flex items-center gap-3">
          <button onclick="toggleSidebarMobile(true)" class="lg:hidden p-2 rounded-xl bg-slate-900 border border-slate-800 text-amber-300 hover:bg-slate-800 transition cursor-pointer flex items-center gap-1.5" title="Открыть меню">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
            <span class="text-xs font-semibold">Меню</span>
          </button>
          <button id="desktop-sidebar-btn" onclick="toggleSidebarDesktop()" class="hidden lg:flex p-2 rounded-xl bg-slate-900/80 border border-slate-800 text-slate-300 hover:text-amber-300 hover:border-amber-500/40 transition cursor-pointer items-center gap-1.5" title="Скрыть/показать сайдбар (Ctrl+B)">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7"/></svg>
            <span class="text-xs font-mono font-medium">Панель</span>
          </button>
          <a href="index.html" class="flex items-center gap-2.5 group">
            <div class="w-8 h-8 rounded-xl bg-gradient-to-tr from-amber-500 to-amber-300 text-slate-950 font-black text-lg flex items-center justify-center shadow-lg shadow-amber-500/20 group-hover:scale-105 transition">⚡</div>
            <div>
              <div class="font-display font-bold text-sm tracking-wide text-slate-100 group-hover:text-amber-300 transition">INNER CURRENT</div>
              <div class="text-[9px] uppercase font-mono tracking-widest text-slate-400 font-semibold">Манифест Тока</div>
            </div>
          </a>
        </div>

        <!-- Desktop Nav Links -->
        <div class="hidden md:flex items-center gap-5 text-xs font-medium text-slate-300">
          <a href="index.html" class="hover:text-amber-300 transition flex items-center gap-1"><span>←</span> Главная</a>
          <a href="whitepaper.html" class="text-sky-300 hover:text-sky-200 transition flex items-center gap-1 font-semibold"><span>📄</span> White Paper</a>
          <a href="index.html#house" class="hover:text-amber-300 transition">Дом Тока</a>
          <a href="index.html#books" class="hover:text-amber-300 transition">Книги (7)</a>
          <a href="wiki.html" class="hover:text-emerald-300 transition flex items-center gap-1"><span>📚</span> Вики</a>
        </div>

        <div class="flex items-center gap-2">
          <a href="index.html#reader" class="px-3.5 py-1.5 rounded-xl text-xs font-bold bg-amber-500 hover:bg-amber-400 text-slate-950 transition flex items-center gap-1.5 shadow-md shadow-amber-500/20">
            <span>📖</span> <span>Ридер</span>
          </a>
        </div>
      </div>
    </nav>"""

        sidebar_html = get_sidebar_html("manifesto")
        sidebar_js = get_sidebar_js("manifesto")

        replacement_top = body_tag + "\n\n" + sidebar_html + '\n\n  <div id="main-layout" class="flex-1 flex flex-col min-w-0 transition-all duration-300 lg:pl-72">\n' + new_nav
        html = html[:m.start()] + replacement_top + html[nav_match.end():]
        html = html.replace("</body>", "  </div> <!-- /#main-layout -->\n\n" + sidebar_js + "\n</body>", 1)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Successfully updated manifesto: {filepath}")

def update_whitepaper_file(filepath):
    print(f"Processing whitepaper: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()

    if "/* LEFT SIDEBAR STYLES" not in html:
        html = html.replace("</style>", SIDEBAR_CSS + "\n  </style>", 1)

    if '<aside id="app-sidebar"' not in html:
        body_pattern = r'(<body[^>]*>)'
        m = re.search(body_pattern, html)
        if not m:
            return False
        body_tag = m.group(1)

        old_nav_pattern = r'(<nav class="sticky top-0 z-50[^\n]*\n[\s\S]*?</nav>)'
        nav_match = re.search(old_nav_pattern, html)
        if not nav_match:
            return False

        new_nav = """    <!-- TOP STICKY NAVBAR -->
    <nav class="sticky top-0 z-40 bg-slate-950/85 backdrop-blur-md border-b border-slate-800/80">
      <div class="max-w-6xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between gap-3">
        <div class="flex items-center gap-3">
          <button onclick="toggleSidebarMobile(true)" class="lg:hidden p-2 rounded-xl bg-slate-900 border border-slate-800 text-amber-300 hover:bg-slate-800 transition cursor-pointer flex items-center gap-1.5" title="Открыть меню">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
            <span class="text-xs font-semibold">Меню</span>
          </button>
          <button id="desktop-sidebar-btn" onclick="toggleSidebarDesktop()" class="hidden lg:flex p-2 rounded-xl bg-slate-900/80 border border-slate-800 text-slate-300 hover:text-amber-300 hover:border-amber-500/40 transition cursor-pointer items-center gap-1.5" title="Скрыть/показать сайдбар (Ctrl+B)">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7"/></svg>
            <span class="text-xs font-mono font-medium">Панель</span>
          </button>
          <a href="index.html" class="flex items-center gap-2.5 group">
            <div class="w-8 h-8 rounded-lg bg-gradient-to-tr from-amber-500 to-amber-300 text-slate-950 font-black text-lg flex items-center justify-center shadow-lg shadow-amber-500/20 group-hover:scale-105 transition">⚡</div>
            <div>
              <div class="font-display font-bold text-sm tracking-wide text-slate-100 group-hover:text-amber-300 transition">INNER CURRENT</div>
              <div class="text-[9px] uppercase font-mono tracking-widest text-slate-400 font-semibold">Master Protocol Whitepaper</div>
            </div>
          </a>
        </div>

        <div class="flex items-center gap-3 text-xs font-medium">
          <a href="index.html" class="text-slate-400 hover:text-slate-200 transition">Главная</a>
          <a href="manifesto.html" class="text-amber-400 hover:text-amber-300 transition flex items-center gap-1 font-semibold"><span>⚡</span> Манифест</a>
          <a href="books/whitepaper.pdf" download class="px-3 py-1.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold transition flex items-center gap-1.5 shadow-md shadow-amber-500/10">
            <span>📥</span> <span>Скачать PDF</span>
          </a>
        </div>
      </div>
    </nav>"""

        sidebar_html = get_sidebar_html("whitepaper")
        sidebar_js = get_sidebar_js("whitepaper")

        replacement_top = body_tag + "\n\n" + sidebar_html + '\n\n  <div id="main-layout" class="flex-1 flex flex-col min-w-0 transition-all duration-300 lg:pl-72">\n' + new_nav
        html = html[:m.start()] + replacement_top + html[nav_match.end():]
        html = html.replace("</body>", "  </div> <!-- /#main-layout -->\n\n" + sidebar_js + "\n</body>", 1)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Successfully updated whitepaper: {filepath}")

if __name__ == "__main__":
    # Update index.html
    # (index files were updated by previous run, but let's ensure full consistency)
    
    # Update manifesto.html
    for base in [DIST_DIR, PUBLIC_DIR]:
        m_file = os.path.join(base, "manifesto.html")
        if os.path.exists(m_file):
            update_manifesto_file(m_file)
            
        w_file = os.path.join(base, "whitepaper.html")
        if os.path.exists(w_file):
            update_whitepaper_file(w_file)
