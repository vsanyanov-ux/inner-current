# -*- coding: utf-8 -*-
import os
import shutil

ROOT_DIR = r"c:\Users\vanya\Antigravity Projects\Apps\Inner Current"
INDEX_DIST = os.path.join(ROOT_DIR, "dist_site", "index.html")
INDEX_PUB = os.path.join(ROOT_DIR, "public", "index.html")

with open(INDEX_DIST, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Add reader tab button
rbtn_target = """<button id="rbtn-dual_circuit" onclick="readBookInReader('dual_circuit')" class="px-3.5 py-2 rounded-xl text-xs font-semibold transition cursor-pointer bg-slate-800 text-amber-300 border border-amber-500/30 hover:text-white hover:bg-slate-700 shrink-0">
            ⚡ Двухконтурный человек
          </button>"""

rbtn_replacement = """<button id="rbtn-dual_circuit" onclick="readBookInReader('dual_circuit')" class="px-3.5 py-2 rounded-xl text-xs font-semibold transition cursor-pointer bg-slate-800 text-amber-300 border border-amber-500/30 hover:text-white hover:bg-slate-700 shrink-0">
            ⚡ Двухконтурный человек
          </button>
          <button id="rbtn-living_universe" onclick="readBookInReader('living_universe')" class="px-3.5 py-2 rounded-xl text-xs font-semibold transition cursor-pointer bg-slate-800 text-emerald-300 border border-emerald-500/30 hover:text-white hover:bg-slate-700 shrink-0">
            🌱 Оживление Вселенной
          </button>"""

if rbtn_target in html and "rbtn-living_universe" not in html:
    html = html.replace(rbtn_target, rbtn_replacement)
    print("Added living_universe tab button to reader")

# 2. Add brochure card in Monographs & Special Issues grid
card_target = """<!-- Item 0: Breakthrough Manifesto -->"""

card_replacement = """<!-- Item: Living Universe Master Manifesto -->
      <div class="bg-gradient-to-b from-emerald-950/40 via-slate-900 to-slate-900 border border-emerald-500/50 rounded-2xl p-5 flex flex-col justify-between hover:border-emerald-400 transition shadow-lg shadow-emerald-500/10 relative">
        <div class="absolute -top-2.5 right-4 px-2 py-0.5 rounded-full bg-emerald-500 text-slate-950 font-bold text-[9px] uppercase tracking-wider font-mono">
          Новый Манифест 2026
        </div>
        <div>
          <span class="text-xs font-mono uppercase tracking-wider text-emerald-300 font-bold">Брошюра • PDF + Web</span>
          <h4 class="text-base font-bold text-slate-100 mt-2">
            Оживление Вселенной
          </h4>
          <p class="text-xs text-emerald-400/90 font-mono text-[10px] mt-0.5">
            От энтропийного пессимизма к созидательному току бытия
          </p>
          <p class="text-xs text-slate-300 mt-2 leading-relaxed">
            Преодоление 300-летнего морга Декарта, Ньютона и Клаузиуса. Конец экзистенциального кризиса, активная самоорганизующаяся материя и человек как остриё космической негэнтропии.
          </p>
        </div>
        <div class="pt-4 mt-4 border-t border-slate-800 flex flex-wrap items-center gap-2">
          <button onclick="readBookInReader('living_universe')" class="flex-1 py-2 px-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 text-xs font-bold text-center transition cursor-pointer shadow-sm">
            📖 Читать
          </button>
          <a href="books/living_universe.pdf" download class="py-2 px-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold text-center border border-slate-700 transition flex items-center justify-center gap-1">
            <span>📥</span> PDF
          </a>
          <a href="books/living_universe.html" target="_blank" title="Открыть в отдельной вкладке" class="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 text-xs transition">
            ↗
          </a>
        </div>
      </div>

      <!-- Item 0: Breakthrough Manifesto -->"""

if card_target in html and "От энтропийного пессимизма к созидательному току бытия" not in html:
    html = html.replace(card_target, card_replacement)
    print("Added Living Universe card to brochures section")

# 3. Add to bookSrcMap & keys array
map_target = """'dual_circuit': 'books/dual_circuit.html',"""
map_replacement = """'dual_circuit': 'books/dual_circuit.html',
      'living_universe': 'books/living_universe.html',"""

if map_target in html and "'living_universe':" not in html:
    html = html.replace(map_target, map_replacement)
    print("Added living_universe to bookSrcMap")

keys_target = """const keys = [
        '01_inner_current', '02_quaternary_fractal', '03_universal_law',
        '04_primer', '05_field_manual', '06_ukulele', '07_great_synthesis',
        'dual_circuit'
      ];"""

keys_replacement = """const keys = [
        '01_inner_current', '02_quaternary_fractal', '03_universal_law',
        '04_primer', '05_field_manual', '06_ukulele', '07_great_synthesis',
        'dual_circuit', 'living_universe'
      ];"""

if keys_target in html:
    html = html.replace(keys_target, keys_replacement)
    print("Added living_universe to keys array")

# Write to dist_site/index.html
with open(INDEX_DIST, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Updated {INDEX_DIST}")

# Sync to public/index.html
shutil.copyfile(INDEX_DIST, INDEX_PUB)
print(f"Synced to {INDEX_PUB}")
