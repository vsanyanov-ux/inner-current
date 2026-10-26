# -*- coding: utf-8 -*-
"""
Add the 4-Quadrant Phase Space Radar directly into public/trainer.html and dist_site/trainer.html.
"""
import os
import re
import sys

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC_TRAINER = os.path.join(ROOT_DIR, 'public', 'trainer.html')
DIST_TRAINER = os.path.join(ROOT_DIR, 'dist_site', 'trainer.html')

QUADRANTS_HTML = '''              <!-- ============================================================== -->
              <!-- 4-QUADRANT PHASE RADAR (ТАКСОНОМИЯ СОСТОЯНИЙ КОНТУРА)          -->
              <!-- ============================================================== -->
              <div class="p-5 rounded-2xl bg-slate-950/90 border border-slate-800 shadow-xl space-y-3 relative overflow-hidden">
                <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800/80 pb-3">
                  <div class="flex items-center gap-2">
                    <span class="text-base text-cyan-400">🧭</span>
                    <span class="text-xs font-mono font-bold uppercase tracking-wider text-slate-200">
                      Матрица четырёх состояний (Фазовый 2D-радар)
                    </span>
                  </div>
                  <div class="flex items-center gap-2 text-xs font-mono">
                    <span class="text-slate-400 text-[10px]">ТОЧКА В ЦЕПИ:</span>
                    <span id="trainer-quad-coords" class="px-2 py-0.5 rounded bg-slate-900 border border-slate-700 text-amber-300 font-bold text-[11px]">
                      I: 75 Ав | CI: +84
                    </span>
                  </div>
                </div>

                <!-- 2D Coordinate Grid with 4 Quadrants -->
                <div class="relative w-full h-52 bg-[#040813] border border-slate-800 rounded-xl overflow-hidden p-2 select-none">
                  
                  <!-- Quadrant interactive tiles -->
                  <div class="absolute inset-0 grid grid-cols-2 grid-rows-2 gap-1 p-1">
                    
                    <!-- QUADRANT IV: Top-Left (Ohmic Overheat) -->
                    <div id="quad-tile-4" onclick="tach_applyQuadrant(85, -80)" class="cursor-pointer transition-all duration-300 rounded-lg p-2.5 flex flex-col justify-between border border-red-900/30 bg-red-950/20 hover:bg-red-950/40 group">
                      <div class="flex items-center justify-between">
                        <span class="text-[11px] font-mono font-bold text-red-400 flex items-center gap-1">
                          <span>🔥</span> IV. ОМИЧЕСКИЙ ПОЖАР
                        </span>
                        <span class="text-[9px] font-mono text-red-400/80 group-hover:text-red-300">Газ в пол + Тормоз</span>
                      </div>
                      <p class="text-[10px] text-slate-400 leading-tight">
                        Высокие обороты ($I \ge 50$) при зажатом заломе ($CI < 0$). Перегрев проводки, выгорание ($Q = I^2 R$).
                      </p>
                    </div>

                    <!-- QUADRANT I: Top-Right (Superconductivity / Mushin) -->
                    <div id="quad-tile-1" onclick="tach_applyQuadrant(85, 80)" class="cursor-pointer transition-all duration-300 rounded-lg p-2.5 flex flex-col justify-between border border-cyan-500/40 bg-cyan-950/30 hover:bg-cyan-950/50 group shadow-md shadow-cyan-950/50">
                      <div class="flex items-center justify-between">
                        <span class="text-[11px] font-mono font-bold text-cyan-300 flex items-center gap-1">
                          <span>⚡</span> I. СВЕРХПРОВОДИМОСТЬ (МУСИН)
                        </span>
                        <span class="text-[9px] font-mono text-cyan-300/80 group-hover:text-cyan-200">Чистый ход</span>
                      </div>
                      <p class="text-[10px] text-slate-400 leading-tight">
                        Высокие обороты ($I \ge 50$) при чистом проводнике ($CI \ge 0$). Максимальная мощность ($P \to \max$).
                      </p>
                    </div>

                    <!-- QUADRANT III: Bottom-Left (Viscous Clinch / Stupor) -->
                    <div id="quad-tile-3" onclick="tach_applyQuadrant(20, -70)" class="cursor-pointer transition-all duration-300 rounded-lg p-2.5 flex flex-col justify-between border border-amber-900/30 bg-amber-950/20 hover:bg-amber-950/40 group">
                      <div class="flex items-center justify-between">
                        <span class="text-[11px] font-mono font-bold text-amber-400 flex items-center gap-1">
                          <span>🧊</span> III. ВЯЗКИЙ КЛИН (СТУПОР)
                        </span>
                        <span class="text-[9px] font-mono text-amber-400/80 group-hover:text-amber-300">Клин мотора</span>
                      </div>
                      <p class="text-[10px] text-slate-400 leading-tight">
                        Низкие обороты ($I < 50$) при зажатом заломе ($CI < 0$). Апатия, прокрастинация, спазм действия.
                      </p>
                    </div>

                    <!-- QUADRANT II: Bottom-Right (Cold Circuit / Zanshin) -->
                    <div id="quad-tile-2" onclick="tach_applyQuadrant(15, 80)" class="cursor-pointer transition-all duration-300 rounded-lg p-2.5 flex flex-col justify-between border border-indigo-900/30 bg-indigo-950/20 hover:bg-indigo-950/40 group">
                      <div class="flex items-center justify-between">
                        <span class="text-[11px] font-mono font-bold text-indigo-300 flex items-center gap-1">
                          <span>🌌</span> II. ХОЛОДНЫЙ ПОКОЙ (ДЗАНСИН)
                        </span>
                        <span class="text-[9px] font-mono text-indigo-300/80 group-hover:text-indigo-200">Регенерация</span>
                      </div>
                      <p class="text-[10px] text-slate-400 leading-tight">
                        Низкие обороты ($I < 50$) при чистом проводнике ($CI \ge 0$). Накопление заряда, глубокий покой, сон.
                      </p>
                    </div>

                  </div>

                  <!-- Coordinate Crosshair Axes -->
                  <div class="absolute left-1/2 top-0 bottom-0 w-[1px] bg-slate-600/70 pointer-events-none"></div>
                  <div class="absolute top-1/2 left-0 right-0 h-[1px] bg-slate-600/70 pointer-events-none"></div>

                  <!-- Axis Arrow Annotations -->
                  <div class="absolute top-1.5 left-1/2 -translate-x-1/2 text-[8px] font-mono text-slate-500 pointer-events-none uppercase">
                    ▲ Напор внимания (I)
                  </div>
                  <div class="absolute bottom-1.5 left-2 text-[8px] font-mono text-rose-500 pointer-events-none uppercase">
                    ◄ Стресс (-100)
                  </div>
                  <div class="absolute bottom-1.5 right-2 text-[8px] font-mono text-emerald-500 pointer-events-none uppercase">
                    Счастье (+100) ►
                  </div>

                  <!-- Real-time Position Blip -->
                  <div id="trainer-radar-blip" class="absolute w-5 h-5 -ml-2.5 -mt-2.5 rounded-full border-2 border-white bg-cyan-400 shadow-[0_0_15px_rgba(56,189,248,1)] transition-all duration-200 pointer-events-none" style="left: 92%; bottom: 75%;">
                    <div class="w-full h-full rounded-full bg-cyan-300 animate-ping opacity-75"></div>
                  </div>
                </div>

                <div class="flex items-center justify-between text-[10px] font-mono text-slate-400 pt-1">
                  <span>💡 Кликните на любой квадрант, чтобы мгновенно перевести контур в это состояние</span>
                  <span id="trainer-quad-active-name" class="font-bold text-cyan-300">Активен: Квадрант I</span>
                </div>
              </div>
'''

RADAR_JS = '''
    function updateRadarPosition() {
      const ciEl = document.getElementById('gauge-ci-val');
      if (!ciEl) return;
      const ci = parseInt(ciEl.textContent, 10) || 0;
      const I = tachCurrentI;

      const blip = document.getElementById('trainer-radar-blip');
      if (blip) {
        // CI from -100 to +100 -> percentX from 5% to 95%
        const percentX = Math.max(5, Math.min(95, ((ci + 100) / 200.0) * 100));
        // I from 0 to 100 -> percentY from 5% to 95%
        const percentY = Math.max(5, Math.min(95, I));
        blip.style.left = percentX.toFixed(1) + '%';
        blip.style.bottom = percentY.toFixed(1) + '%';
      }

      const coordsEl = document.getElementById('trainer-quad-coords');
      if (coordsEl) {
        coordsEl.textContent = `I: ${I} Ав | CI: ${(ci > 0 ? '+' : '')}${ci}`;
      }

      // Highlight active quadrant tile
      const t1 = document.getElementById('quad-tile-1');
      const t2 = document.getElementById('quad-tile-2');
      const t3 = document.getElementById('quad-tile-3');
      const t4 = document.getElementById('quad-tile-4');
      const activeName = document.getElementById('trainer-quad-active-name');

      [t1, t2, t3, t4].forEach(t => {
        if (t) {
          t.classList.remove('ring-2', 'ring-cyan-400', 'ring-red-500', 'ring-amber-400', 'ring-indigo-400', 'scale-[1.01]');
        }
      });

      if (I >= 50 && ci >= 0) {
        // QUADRANT I: Superconductivity
        if (t1) t1.classList.add('ring-2', 'ring-cyan-400', 'scale-[1.01]');
        if (activeName) activeName.innerHTML = '<span class="text-cyan-300 font-bold">⚡ Квадрант I • Сверхпроводимость (Мусин)</span>';
      } else if (I < 50 && ci >= 0) {
        // QUADRANT II: Cold Circuit
        if (t2) t2.classList.add('ring-2', 'ring-indigo-400', 'scale-[1.01]');
        if (activeName) activeName.innerHTML = '<span class="text-indigo-300 font-bold">🌌 Квадрант II • Холодный покой (Дзансин)</span>';
      } else if (I < 50 && ci < 0) {
        // QUADRANT III: Viscous Clinch
        if (t3) t3.classList.add('ring-2', 'ring-amber-400', 'scale-[1.01]');
        if (activeName) activeName.innerHTML = '<span class="text-amber-300 font-bold">🧊 Квадрант III • Вязкий клин (Ступор)</span>';
      } else {
        // QUADRANT IV: Ohmic Overheat
        if (t4) t4.classList.add('ring-2', 'ring-red-500', 'scale-[1.01]');
        if (activeName) activeName.innerHTML = '<span class="text-rose-400 font-bold">🔥 Квадрант IV • Омический пожар (Перегрев)</span>';
      }
    }

    function tach_applyQuadrant(targetI, targetCI) {
      // 1. Set Tachometer
      const sliderTach = document.getElementById('slider-tach-i');
      if (sliderTach) sliderTach.value = targetI;
      tach_render(targetI);

      // 2. Set Biological Systems to approximate targetCI
      ['ans', 'endo', 'brain', 'cardio', 'soma'].forEach(sys => {
        gaugeState[sys] = targetCI;
        const slider = document.getElementById('slider-gauge-' + sys);
        if (slider) slider.value = targetCI;
      });

      gauge_render();
      playZenChime(targetCI > 0 ? 640 : 380);
    }
    window.tach_applyQuadrant = tach_applyQuadrant;
    window.updateRadarPosition = updateRadarPosition;
'''

def patch_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Insert 4-Quadrant HTML if not present
    if 'id="trainer-radar-blip"' not in content:
        needle = '<!-- Metaphor Banner -->'
        if needle in content:
            content = content.replace(needle, QUADRANTS_HTML + '\n\n              ' + needle)
            print(f"Injected QUADRANTS_HTML before Metaphor Banner in {file_path}")
        else:
            print(f"Error: {needle} not found in {file_path}")

    # 2. Insert RADAR_JS into JS section
    if 'updateRadarPosition' not in content:
        js_needle = 'function updateCoupledVerdict() {'
        if js_needle in content:
            content = content.replace(js_needle, RADAR_JS + '\n\n    ' + js_needle)
            print(f"Injected RADAR_JS before updateCoupledVerdict in {file_path}")
        else:
            print(f"Error: {js_needle} not found in {file_path}")

    # 3. Call updateRadarPosition in updateCoupledVerdict
    call_needle = 'updateRadarPosition();'
    if call_needle not in content:
        content = content.replace('if (!stateTitle || !stateDesc) return;', 'updateRadarPosition();\n      if (!stateTitle || !stateDesc) return;')
        print(f"Added updateRadarPosition call in {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Saved: {file_path}")

def main():
    patch_file(PUBLIC_TRAINER)
    patch_file(DIST_TRAINER)

if __name__ == '__main__':
    main()
