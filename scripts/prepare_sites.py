# -*- coding: utf-8 -*-
"""
Prepare and separate sites:
1. Book Library Portal (innercurrent.ru / index.html)
2. Interactive Diagnostic Trainer / Cockpit (trainer.html / cockpit.html)
"""
import os
import re
import sys

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC_DIR = os.path.join(ROOT_DIR, 'public')
DIST_DIR = os.path.join(ROOT_DIR, 'dist_site')

def separate_sites():
    # -------------------------------------------------------------
    # STEP 1: Prepare trainer.html from the local 422KB trainer
    # -------------------------------------------------------------
    source_trainer_path = os.path.join(PUBLIC_DIR, 'index.html')
    with open(source_trainer_path, 'r', encoding='utf-8') as f:
        trainer_html = f.read()

    # Ensure it is indeed the trainer
    if 'Inner Current — Внутренний ток & Электродинамика Контуров' not in trainer_html:
        raise ValueError("Source file in public/index.html is not the diagnostic trainer!")

    # Add a prominent "Библиотека книг" link into the sidebar of trainer.html
    library_link = '''          <!-- Books Library Link -->
          <a href="/" class="w-full text-left p-3 rounded-xl border border-amber-500/50 bg-gradient-to-r from-amber-950/60 to-orange-950/40 hover:border-amber-400 flex items-center gap-3 group relative overflow-hidden transition shadow-lg shadow-amber-500/10">
            <span class="text-xl shrink-0">📖</span>
            <div class="flex-1 min-w-0">
              <div class="flex items-center justify-between gap-1">
                <span class="text-xs font-bold text-amber-200 group-hover:text-white transition truncate">
                  Библиотека книг
                </span>
                <span class="text-[9px] font-mono px-1.5 py-0.5 rounded bg-amber-400/20 text-amber-300 border border-amber-400/30">7 книг</span>
              </div>
              <p class="text-[10px] text-slate-300 truncate mt-0.5">Портал innercurrent.ru</p>
            </div>
          </a>
'''
    target_needle = '<!-- Cockpit Master Link -->'
    if target_needle in trainer_html and '<!-- Books Library Link -->' not in trainer_html:
        trainer_html = trainer_html.replace(target_needle, library_link + '\n          ' + target_needle)

    # Save to public/trainer.html and dist_site/trainer.html
    public_trainer_path = os.path.join(PUBLIC_DIR, 'trainer.html')
    dist_trainer_path = os.path.join(DIST_DIR, 'trainer.html')

    with open(public_trainer_path, 'w', encoding='utf-8') as f:
        f.write(trainer_html)
    print(f"Saved: {public_trainer_path} ({len(trainer_html)} bytes)")

    with open(dist_trainer_path, 'w', encoding='utf-8') as f:
        f.write(trainer_html)
    print(f"Saved: {dist_trainer_path} ({len(trainer_html)} bytes)")

    # -------------------------------------------------------------
    # STEP 2: Prepare the Book Library Portal index.html
    # -------------------------------------------------------------
    recovered_path = os.path.join(DIST_DIR, 'index_books_recovered.html')
    if not os.path.exists(recovered_path):
        raise FileNotFoundError(f"Missing {recovered_path}")

    with open(recovered_path, 'r', encoding='utf-8') as f:
        books_html = f.read()

    # 1. Add trainer link to nav
    old_nav = '<a href="#principles" class="hover:text-slate-100 transition">Принципы</a>'
    new_nav = '<a href="#principles" class="hover:text-slate-100 transition">Принципы</a>\n        <a href="trainer.html" class="hover:text-amber-300 transition flex items-center gap-1.5 text-slate-400"><span class="text-xs">🎛️</span> Тренажер</a>'
    if old_nav in books_html and 'href="trainer.html"' not in books_html:
        books_html = books_html.replace(old_nav, new_nav, 1)

    # 2. Update Great Synthesis card
    old_synth_sub = '<p class="text-xs md:text-sm text-amber-400 font-medium mt-1">\n              Схождение фундаментальной физики, инженерной истории и устройства сознания\n            </p>'
    new_synth_sub = '<p class="text-xs md:text-sm text-amber-400 font-medium mt-1">\n              Master Edition 2.0: Универсальный закон потоковых систем, Онтологическая триада и схождение физики, техники, религии и эпохи ИИ\n            </p>'
    if old_synth_sub in books_html:
        books_html = books_html.replace(old_synth_sub, new_synth_sub, 1)

    old_synth_pdf = '<a href="books/great_synthesis.pdf" download title="Скачать PDF (30 стр.)" class="py-3 px-5 rounded-xl bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 border border-amber-500/40 text-sm font-semibold transition flex items-center gap-2">\n            <span>📥</span> PDF книги (30 стр.)\n          </a>'
    new_synth_pdf = '<a href="books/great_synthesis.pdf" download title="Скачать PDF книги (Master Edition 2.0, 49 стр.)" class="py-3 px-5 rounded-xl bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 border border-amber-500/40 text-sm font-semibold transition flex items-center gap-2">\n            <span>📥</span> PDF книги (49 стр., Master Edition 2.0)\n          </a>'
    if old_synth_pdf in books_html:
        books_html = books_html.replace(old_synth_pdf, new_synth_pdf, 1)

    # 3. Primer links
    books_html = books_html.replace('href="books/primer.html"', 'href="books/primer_flashlight.html"')
    books_html = books_html.replace("'primer': 'books/primer.html'", "'primer': 'books/primer_flashlight.html'")

    # 4. Footer link
    old_footer = '<a href="#audiobook" class="hover:text-cyan-300 transition">Аудиокнига</a>'
    new_footer = '<a href="#audiobook" class="hover:text-cyan-300 transition">Аудиокнига</a>\n        <span>•</span>\n        <a href="trainer.html" class="hover:text-amber-300 transition">Тренажер цепи</a>'
    if old_footer in books_html and 'Тренажер цепи' not in books_html:
        books_html = books_html.replace(old_footer, new_footer, 1)

    # Save to dist_site/index.html and public/index.html
    dist_index_path = os.path.join(DIST_DIR, 'index.html')
    public_index_path = os.path.join(PUBLIC_DIR, 'index.html')

    with open(dist_index_path, 'w', encoding='utf-8') as f:
        f.write(books_html)
    print(f"Saved: {dist_index_path} ({len(books_html)} bytes)")

    with open(public_index_path, 'w', encoding='utf-8') as f:
        f.write(books_html)
    print(f"Saved: {public_index_path} ({len(books_html)} bytes)")

    # Clean up temporary recovered file
    if os.path.exists(recovered_path):
        os.remove(recovered_path)
        print(f"Removed temporary file: {recovered_path}")

    print("\n✅ Separation complete:")
    print(" - Book Library Portal -> public/index.html & dist_site/index.html")
    print(" - Local Diagnostic Trainer -> public/trainer.html & dist_site/trainer.html")

if __name__ == '__main__':
    separate_sites()
