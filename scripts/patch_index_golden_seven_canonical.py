import os
import re

def update_index_file(filepath):
    print(f"Updating {filepath}...")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update Sidebar item 6
    old_sidebar_6 = '''            <button onclick="openBookFromSidebar('06_ukulele')" class="w-full text-left px-2 py-1.5 rounded-lg text-slate-400 hover:text-amber-200 hover:bg-slate-800/40 transition flex items-center gap-2">
              <span class="text-amber-400 font-mono text-[10px]">6.</span>
              <span class="truncate">Дзен-гитара &amp; Укулеле</span>
            </button>'''
    new_sidebar_6 = '''            <button onclick="openBookFromSidebar('06_human_instruction')" class="w-full text-left px-2 py-1.5 rounded-lg text-slate-400 hover:text-amber-200 hover:bg-slate-800/40 transition flex items-center gap-2">
              <span class="text-sky-400 font-mono text-[10px]">6.</span>
              <span class="truncate font-medium text-sky-200">Инструкция к человеку</span>
            </button>'''
    if old_sidebar_6 in content:
        content = content.replace(old_sidebar_6, new_sidebar_6)
        print(" -> Updated sidebar item 6")

    # 2. Update Book 06 card in the 7 Books Grid
    old_book_6_pattern = re.compile(
        r'<!-- Book 06: Ukulele of Being -->\s*<div class="bg-gradient-to-b from-sky-950/15[\s\S]*?<!-- Book 07: The Great Synthesis',
        re.MULTILINE
    )
    new_book_6_html = '''<!-- Book 06: Human Instruction (Technical Passport) -->
      <div class="bg-gradient-to-b from-sky-950/25 to-slate-900 border border-sky-500/40 rounded-2xl p-6 shadow-xl flex flex-col justify-between relative group hover:border-sky-400 transition-all duration-300">
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <span class="text-3xl">📘</span>
            <span class="text-[10px] font-mono uppercase tracking-wider px-2.5 py-1 rounded-full bg-sky-500/20 text-sky-300 border border-sky-500/40 font-bold">
              Книга 6 • Экспресс-старт (Техпаспорт)
            </span>
          </div>
          <div>
            <h3 class="text-lg font-bold text-slate-100 group-hover:text-sky-300 transition">
              Инструкция к человеку
            </h3>
            <p class="text-xs text-sky-400/90 font-medium mt-1">
              Технический паспорт открытого сверхпроводника и 25 побед цепи
            </p>
          </div>
          <p class="text-xs text-slate-300 leading-relaxed font-serif">
            Заводской техпаспорт и быстрый старт: 14 страниц. 25 побед цепи над заблуждениями веков, трёхэтажная схема свободы воли (Тандэн → Эго-автомат → Мусин), разотождествление с автоматом, 4 кода поломок контура (ERR-01…04) и дашборд калибровки за 45 секунд.
          </p>
        </div>
        <div class="pt-5 mt-4 border-t border-slate-800/80 flex items-center gap-2">
          <button onclick="readBookInReader('06_human_instruction')" class="flex-1 py-2.5 px-3 rounded-xl bg-sky-500 hover:bg-sky-400 text-slate-950 font-bold text-xs transition text-center cursor-pointer shadow-md shadow-sky-500/20">
            📖 Читать в ридере
          </button>
          <a href="books/06_human_instruction.pdf" download title="Скачать PDF книги (14 стр.)" class="px-3 py-2.5 rounded-xl bg-sky-500/20 hover:bg-sky-500/30 text-sky-300 border border-sky-500/40 text-xs font-semibold transition flex items-center gap-1">
            <span>📥</span> PDF (14 с.)
          </a>
          <a href="books/human_instruction.html" target="_blank" title="Открыть в отдельной вкладке" class="p-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 text-xs transition">
            ↗
          </a>
        </div>
      </div>

      <!-- Book 07: The Great Synthesis'''

    if old_book_6_pattern.search(content):
        content = old_book_6_pattern.sub(new_book_6_html, content)
        print(" -> Updated Book 06 card in 7 Books Grid")
    else:
        print(" !! Pattern for Book 06 card not found, checking manual string replacement")

    # 3. Add Ukulele of Being into "Тематические материалы и памятки" as a Special Art Edition
    if '<!-- Item: Ukulele of Being (Special Art Edition) -->' not in content:
        target_grid = '<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">'
        ukulele_card = '''        <!-- Item: Ukulele of Being (Special Art Edition) -->
        <div class="bg-gradient-to-b from-sky-950/30 via-slate-900 to-slate-900 border border-sky-500/40 rounded-2xl p-5 flex flex-col justify-between hover:border-sky-400 transition shadow-lg shadow-sky-500/10 relative">
          <div class="absolute -top-2.5 right-4 px-2 py-0.5 rounded-full bg-sky-500 text-slate-950 font-bold text-[9px] uppercase tracking-wider font-mono">
            Арт-издание
          </div>
          <div>
            <span class="text-xs font-mono uppercase tracking-wider text-sky-300 font-bold">Эссе • PDF + Web</span>
            <h4 class="text-base font-bold text-slate-100 mt-2">
              Укулеле Бытия
            </h4>
            <p class="text-xs text-sky-400/90 font-mono text-[10px] mt-0.5">
              Акустическая физика счастливой жизни — звук, материя и Мусин
            </p>
            <p class="text-xs text-slate-300 mt-2 leading-relaxed">
              Чувственный монизм духа и материи: 48 страниц. 400 граммов дерева, 4 струны и снятие дуализма Декарта. Как звук рождается из материи без мистики, и почему струна под зажимом эго дребезжит.
            </p>
          </div>
          <div class="pt-4 mt-4 border-t border-slate-800 flex flex-wrap items-center gap-2">
            <button onclick="readBookInReader('06_ukulele')" class="flex-1 py-2 px-2.5 rounded-xl bg-sky-500 hover:bg-sky-400 text-slate-950 text-xs font-bold text-center transition cursor-pointer shadow-sm">
              📖 Читать
            </button>
            <a href="books/06_ukulele.pdf" download class="py-2 px-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold text-center border border-slate-700 transition flex items-center justify-center gap-1">
              <span>📥</span> PDF
            </a>
            <a href="books/ukulele.html" target="_blank" title="Открыть в отдельной вкладке" class="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 text-xs transition">
              ↗
            </a>
          </div>
        </div>
'''
        content = content.replace(target_grid, target_grid + '\n' + ukulele_card)
        print(" -> Added Ukulele Art Edition card to thematic brochures section")

    # 4. Update Reader top bar tabs
    old_reader_tabs = '''          <button id="rbtn-06_ukulele" onclick="readBookInReader('06_ukulele')" class="px-3.5 py-2 rounded-xl text-xs font-semibold transition cursor-pointer bg-slate-800 text-slate-300 hover:text-white shrink-0">
            🎶 6. Укулеле Бытия
          </button>'''
    new_reader_tabs = '''          <button id="rbtn-06_human_instruction" onclick="readBookInReader('06_human_instruction')" class="px-3.5 py-2 rounded-xl text-xs font-semibold transition cursor-pointer bg-slate-800 text-slate-300 hover:text-white shrink-0">
            📘 6. Инструкция к человеку
          </button>
          <button id="rbtn-06_ukulele" onclick="readBookInReader('06_ukulele')" class="px-3.5 py-2 rounded-xl text-xs font-semibold transition cursor-pointer bg-slate-800 text-sky-300 hover:text-white shrink-0">
            🎶 Укулеле Бытия
          </button>'''
    if old_reader_tabs in content:
        content = content.replace(old_reader_tabs, new_reader_tabs)
        print(" -> Updated Reader tabs")

    # 5. Update bookSrcMap and keys in script
    old_book_src_map = "'05_field_manual': 'books/field_manual.html',\n      '06_ukulele': 'books/ukulele.html',"
    new_book_src_map = "'05_field_manual': 'books/field_manual.html',\n      '06_human_instruction': 'books/human_instruction.html',\n      '06_ukulele': 'books/ukulele.html',\n      'human_instruction': 'books/human_instruction.html',"
    if old_book_src_map in content:
        content = content.replace(old_book_src_map, new_book_src_map)
        print(" -> Updated bookSrcMap")

    old_keys = "'04_primer', '05_field_manual', '06_ukulele', '07_great_synthesis',"
    new_keys = "'04_primer', '05_field_manual', '06_human_instruction', '06_ukulele', '07_great_synthesis',"
    if old_keys in content:
        content = content.replace(old_keys, new_keys)
        print(" -> Updated keys array in reader")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Saved {filepath} successfully.")

if __name__ == "__main__":
    update_index_file(r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\dist_site\index.html")
    update_index_file(r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current\public\index.html")
