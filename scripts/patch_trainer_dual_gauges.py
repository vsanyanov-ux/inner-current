# -*- coding: utf-8 -*-
"""
Patch public/trainer.html and dist_site/trainer.html to:
1. Remove the circular lens/target from the Speedometer needle tip.
2. Add the paired Tachometer (Тахометр Потока I / Обороты Ядра) right next to the Speedometer.
3. Update paired diagnostic engine (Tachometer + Speedometer) so the two instruments work together.
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

def patch_trainer_content(content):
    # 1. Remove circle lens from gauge-needle-group in SVG
    # Remove lines containing gauge-needle-lens-*
    content = re.sub(r'\s*<circle id="gauge-needle-lens-outer"[^>]*/>', '', content)
    content = re.sub(r'\s*<circle id="gauge-needle-lens-ring"[^>]*/>', '', content)
    content = re.sub(r'\s*<circle id="gauge-needle-lens-dot"[^>]*/>', '', content)
    content = re.sub(r'\s*<circle id="gauge-needle-lens-glint"[^>]*/>', '', content)

    # In JS, remove or guard lensOuter references
    content = re.sub(r'\s*const lensOuter = document\.getElementById\(\'gauge-needle-lens-outer\'\);[^\n]*\n'
                     r'\s*const lensRing = document\.getElementById\(\'gauge-needle-lens-ring\'\);[^\n]*\n'
                     r'\s*const lensDot = document\.getElementById\(\'gauge-needle-lens-dot\'\);[^\n]*\n'
                     r'\s*const lensGlint = document\.getElementById\(\'gauge-needle-lens-glint\'\);[^\n]*\n'
                     r'\s*if \(lensOuter\) \{[^\}]*\}\s*'
                     r'\s*if \(lensRing\) \{[^\}]*\}\s*'
                     r'\s*if \(lensDot\) \{[^\}]*\}\s*'
                     r'\s*if \(lensGlint\) \{[^\}]*\}\s*', '', content)

    # 2. Check if Tachometer is already present
    if 'id="tach-needle-group"' in content:
        print("Tachometer already present.")
        return content

    # 3. Create Tachometer SVG & Card markup
    tachometer_card = '''            <!-- LEFT: TACHOMETER DIAL (SVG) - НАПОР ВНИМАНИЯ (I) -->
            <div class="lg:col-span-6 flex flex-col items-center justify-between p-6 rounded-2xl bg-slate-950/85 border border-slate-800 text-center shadow-xl relative overflow-hidden">
              <div class="w-full flex items-center justify-between text-[11px] font-mono uppercase tracking-widest text-slate-400 font-bold mb-1">
                <span class="flex items-center gap-1.5 text-cyan-400">
                  <span id="tach-status-emoji" class="text-lg">⚡</span>
                  <span>ТАХОМЕТР ПОТОКА (I)</span>
                </span>
                <span id="tach-rpm-badge" class="px-2 py-0.5 rounded bg-cyan-950 border border-cyan-800 text-cyan-300 text-[10px] font-bold">
                  75 Ав
                </span>
              </div>

              <!-- SVG TACHOMETER DIAL -->
              <div class="w-full max-w-[290px] my-2 relative">
                <svg viewBox="0 0 300 170" class="w-full overflow-visible select-none drop-shadow-lg">
                  <defs>
                    <linearGradient id="tach-needle-gradient" x1="0%" y1="100%" x2="0%" y2="0%">
                      <stop offset="0%" stop-color="#0284c7"/>
                      <stop offset="35%" stop-color="#38bdf8"/>
                      <stop offset="85%" stop-color="#7dd3fc"/>
                      <stop offset="100%" stop-color="#ffffff"/>
                    </linearGradient>
                    <filter id="tach-needle-glow" x="-50%" y="-50%" width="200%" height="200%">
                      <feGaussianBlur in="SourceGraphic" stdDeviation="2.5" result="blur"/>
                      <feMerge>
                        <feMergeNode in="blur"/>
                        <feMergeNode in="SourceGraphic"/>
                      </feMerge>
                    </filter>
                  </defs>

                  <!-- Background Arc Track -->
                  <path d="M 50 140 A 100 100 0 0 1 250 140" fill="none" stroke="#1e293b" stroke-width="16" stroke-linecap="round"/>

                  <!-- Colored Arcs -->
                  <!-- Blue / Cyan Zone (0 to 60) -->
                  <path d="M 50 140 A 100 100 0 0 1 180.9 44.9" fill="none" stroke="#38bdf8" stroke-width="14" stroke-linecap="round" opacity="0.95"/>
                  <!-- Yellow Zone (60 to 85) -->
                  <path d="M 180.9 44.9 A 100 100 0 0 1 239.1 94.6" fill="none" stroke="#f59e0b" stroke-width="14" stroke-linecap="butt" opacity="0.95"/>
                  <!-- Red Overrev Zone (85 to 100) -->
                  <path d="M 239.1 94.6 A 100 100 0 0 1 250 140" fill="none" stroke="#ef4444" stroke-width="14" stroke-linecap="round" opacity="0.95"/>

                  <!-- Ticks and Scale Marks -->
                  <line x1="50" y1="140" x2="38" y2="140" stroke="#38bdf8" stroke-width="2"/>
                  <text x="32" y="144" fill="#38bdf8" font-size="10" font-family="monospace" text-anchor="end" font-weight="bold">0</text>

                  <line x1="79.3" y1="69.3" x2="71" y2="61" stroke="#38bdf8" stroke-width="2"/>
                  <text x="65" y="58" fill="#38bdf8" font-size="9" font-family="monospace" text-anchor="end">25</text>

                  <line x1="150" y1="40" x2="150" y2="28" stroke="#38bdf8" stroke-width="2"/>
                  <text x="150" y="24" fill="#38bdf8" font-size="11" font-family="monospace" text-anchor="middle" font-weight="bold">50</text>

                  <line x1="220.7" y1="69.3" x2="229" y2="61" stroke="#f59e0b" stroke-width="2"/>
                  <text x="235" y="58" fill="#fbbf24" font-size="9" font-family="monospace" text-anchor="start">75</text>

                  <line x1="250" y1="140" x2="262" y2="140" stroke="#ef4444" stroke-width="2"/>
                  <text x="268" y="144" fill="#ef4444" font-size="10" font-family="monospace" text-anchor="start" font-weight="bold">100</text>

                  <!-- Labels: ПОКОЙ / НАПОР / ОВЕРРЕВ -->
                  <text x="62" y="112" fill="#7dd3fc" font-size="8" font-family="sans-serif" font-weight="bold">🔵 ПОКОЙ</text>
                  <text x="150" y="70" fill="#fde68a" font-size="7" font-family="sans-serif" font-weight="semibold" text-anchor="middle">🟡 НАПОР</text>
                  <text x="238" y="112" fill="#fca5a5" font-size="8" font-family="sans-serif" font-weight="bold" text-anchor="end">🔴 ОВЕРРЕВ</text>

                  <!-- Dynamic Tachometer Needle (CLEAN - NO CIRCLE AT TIP) -->
                  <g id="tach-needle-group">
                    <polygon id="tach-needle-counter" points="146.5,140 153.5,140 150,154" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5" opacity="0.85"/>
                    <polygon id="tach-needle-beam" points="146.5,140 153.5,140 151,22 149,22" fill="url(#tach-needle-gradient)" filter="url(#tach-needle-glow)"/>
                    <line id="tach-needle-spine" x1="150" y1="140" x2="150" y2="22" stroke="#ffffff" stroke-width="0.8" opacity="0.9"/>
                    
                    <circle id="tach-needle-tip-glow" cx="150" cy="22" r="3" fill="#38bdf8" filter="url(#tach-needle-glow)"/>
                    <circle id="tach-needle-tip-core" cx="150" cy="22" r="1.2" fill="#ffffff"/>

                    <circle cx="150" cy="140" r="12" fill="#0b1329" stroke="#38bdf8" stroke-width="2.5" filter="url(#tach-needle-glow)"/>
                    <circle cx="150" cy="140" r="5.5" fill="#38bdf8"/>
                    <circle cx="150" cy="140" r="2" fill="#ffffff"/>
                  </g>
                </svg>
              </div>

              <!-- Main Numeric Readout -->
              <div class="my-1">
                <span id="tach-i-val" class="text-6xl md:text-7xl font-black font-mono tracking-tight bg-gradient-to-r from-cyan-400 via-sky-300 to-blue-400 bg-clip-text text-transparent">
                  75
                </span>
              </div>

              <div id="tach-state-label" class="text-sm font-bold font-mono text-cyan-300 uppercase tracking-wide">
                ⚡ ВЫСОКИЙ НАПОР ВНИМАНИЯ
              </div>
              <div class="text-xs text-slate-300 font-mono mt-0.5">
                Обороты ядра Тандэна: <span id="tach-i-sub" class="text-amber-300 font-bold">75 Ав</span> • Частота процессора
              </div>

              <!-- Slider for Current (I) -->
              <div class="w-full mt-4 pt-3 border-t border-slate-800/80">
                <div class="flex justify-between text-[10px] font-mono text-slate-400 mb-1">
                  <span>Штиль (0)</span>
                  <span>Газ в пол (100)</span>
                </div>
                <input type="range" id="slider-tach-i" min="0" max="100" value="75" oninput="tach_onSliderChange(this.value)"
                  class="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-cyan-400 transition" />
              </div>
            </div>
'''

    # Replace the layout:
    # Look for the Speedometer container:
    old_speedo_header = '<div class="lg:col-span-5 flex flex-col items-center justify-center p-6 rounded-2xl bg-slate-950/85 border border-slate-800 text-center shadow-xl relative overflow-hidden">'
    new_speedo_header = '<div class="lg:col-span-6 flex flex-col items-center justify-between p-6 rounded-2xl bg-slate-950/85 border border-slate-800 text-center shadow-xl relative overflow-hidden">'

    if old_speedo_header in content:
        # Prepend Tachometer card right before the Speedometer card!
        content = content.replace(old_speedo_header, tachometer_card + '\n\n            <!-- RIGHT: SPEEDOMETER DIAL (SVG) - ИНДЕКС ПРОВОДИМОСТИ (CI) -->\n            ' + new_speedo_header)
        print("Tachometer card injected side-by-side with Speedometer.")
    else:
        print("Warning: old_speedo_header not found.")

    # Now make the diagnosis & metrics section span full width (lg:col-span-12) below the two dials!
    content = content.replace('<div class="lg:col-span-7 space-y-4">', '<div class="lg:col-span-12 space-y-4 mt-2">')

    # Add Tachometer JS controller
    tach_js = '''
    // =========================================================================
    // TACHOMETER (I) CONTROLLER & DUAL INSTRUMENT COUPLING
    // =========================================================================
    let tachCurrentI = 75;
    let tachCurrentAngle = 45; // angle for I=75: (75/100)*180 - 90 = 45 deg
    let tachAnimFrame = null;

    function updateTachNeedleGeometry(angle) {
      const cx = 150;
      const cy = 140;
      const length = 118;
      const rad = (angle - 90) * Math.PI / 180;
      const tipX = cx + length * Math.cos(rad);
      const tipY = cy + length * Math.sin(rad);

      const normRad = angle * Math.PI / 180;
      const c = Math.cos(normRad);
      const s = Math.sin(normRad);

      const b1X = cx - 3.5 * c;
      const b1Y = cy - 3.5 * s;
      const b2X = cx + 3.5 * c;
      const b2Y = cy + 3.5 * s;

      const t1X = tipX - 1 * c;
      const t1Y = tipY - 1 * s;
      const t2X = tipX + 1 * c;
      const t2Y = tipY + 1 * s;

      const countX = cx - 14 * s;
      const countY = cy + 14 * c;

      const beam = document.getElementById('tach-needle-beam');
      if (beam) {
        beam.setAttribute('points', b1X.toFixed(1) + ',' + b1Y.toFixed(1) + ' ' + b2X.toFixed(1) + ',' + b2Y.toFixed(1) + ' ' + t2X.toFixed(1) + ',' + t2Y.toFixed(1) + ' ' + t1X.toFixed(1) + ',' + t1Y.toFixed(1));
      }
      const spine = document.getElementById('tach-needle-spine');
      if (spine) {
        spine.setAttribute('x1', cx);
        spine.setAttribute('y1', cy);
        spine.setAttribute('x2', tipX.toFixed(1));
        spine.setAttribute('y2', tipY.toFixed(1));
      }
      const counter = document.getElementById('tach-needle-counter');
      if (counter) {
        counter.setAttribute('points', b1X.toFixed(1) + ',' + b1Y.toFixed(1) + ' ' + b2X.toFixed(1) + ',' + b2Y.toFixed(1) + ' ' + countX.toFixed(1) + ',' + countY.toFixed(1));
      }

      const tipGlow = document.getElementById('tach-needle-tip-glow');
      const tipCore = document.getElementById('tach-needle-tip-core');
      if (tipGlow) { tipGlow.setAttribute('cx', tipX.toFixed(1)); tipGlow.setAttribute('cy', tipY.toFixed(1)); }
      if (tipCore) { tipCore.setAttribute('cx', tipX.toFixed(1)); tipCore.setAttribute('cy', tipY.toFixed(1)); }
    }

    function tach_render(val) {
      tachCurrentI = Math.max(0, Math.min(100, parseInt(val, 10) || 0));
      // targetAngle: 0 -> -90 deg, 50 -> 0 deg, 100 -> +90 deg
      const targetAngle = (tachCurrentI / 100.0) * 180 - 90;

      if (tachAnimFrame) cancelAnimationFrame(tachAnimFrame);
      const startAngle = tachCurrentAngle;
      const startTime = performance.now();
      const duration = 220;

      function step(now) {
        const elapsed = now - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const ease = 1 - Math.pow(1 - progress, 3);
        const current = startAngle + (targetAngle - startAngle) * ease;
        tachCurrentAngle = current;
        updateTachNeedleGeometry(current);
        if (progress < 1) {
          tachAnimFrame = requestAnimationFrame(step);
        } else {
          tachCurrentAngle = targetAngle;
          updateTachNeedleGeometry(targetAngle);
        }
      }
      tachAnimFrame = requestAnimationFrame(step);

      // Digital readouts
      const iVal = document.getElementById('tach-i-val');
      const iSub = document.getElementById('tach-i-sub');
      const iBadge = document.getElementById('tach-rpm-badge');
      const iLabel = document.getElementById('tach-state-label');
      const iEmoji = document.getElementById('tach-status-emoji');

      if (iVal) iVal.textContent = tachCurrentI;
      if (iSub) iSub.textContent = tachCurrentI + ' Ав';
      if (iBadge) iBadge.textContent = tachCurrentI + ' Ав';

      if (tachCurrentI >= 85) {
        if (iEmoji) iEmoji.textContent = '🔥';
        if (iLabel) {
          iLabel.textContent = '🔴 ОВЕРРЕВ (КРАСНАЯ ЗОНА)';
          iLabel.className = 'text-sm font-bold font-mono text-rose-400 uppercase tracking-wide';
        }
      } else if (tachCurrentI >= 55) {
        if (iEmoji) iEmoji.textContent = '⚡';
        if (iLabel) {
          iLabel.textContent = '⚡ ВЫСОКИЙ НАПОР ВНИМАНИЯ';
          iLabel.className = 'text-sm font-bold font-mono text-cyan-300 uppercase tracking-wide';
        }
      } else if (tachCurrentI >= 25) {
        if (iEmoji) iEmoji.textContent = '🌀';
        if (iLabel) {
          iLabel.textContent = '🟡 УМЕРЕННЫЙ ФОКУС';
          iLabel.className = 'text-sm font-bold font-mono text-amber-300 uppercase tracking-wide';
        }
      } else {
        if (iEmoji) iEmoji.textContent = '🧘';
        if (iLabel) {
          iLabel.textContent = '🔵 ХОЛОСТОЙ ХОД / ПОКОЙ';
          iLabel.className = 'text-sm font-bold font-mono text-sky-400 uppercase tracking-wide';
        }
      }

      // Re-trigger coupled diagnosis update
      if (typeof gauge_render === 'function') {
        updateCoupledVerdict();
      }
    }

    function tach_onSliderChange(val) {
      tach_render(val);
    }
    window.tach_onSliderChange = tach_onSliderChange;
    window.tach_render = tach_render;

    function updateCoupledVerdict() {
      const ciEl = document.getElementById('gauge-ci-val');
      if (!ciEl) return;
      const ci = parseInt(ciEl.textContent, 10) || 0;
      const I = tachCurrentI;

      const stateTitle = document.getElementById('gauge-state-title');
      const stateDesc = document.getElementById('gauge-state-desc');
      const stateBadge = document.getElementById('gauge-state-badge');
      const stateBox = document.getElementById('gauge-state-box');

      if (!stateTitle || !stateDesc) return;

      if (I >= 60 && ci < -30) {
        // OHMIC OVERHEAT (High RPM, Stuck Brakes)
        stateTitle.textContent = '🔥 ОМИЧЕСКИЙ ПОЖАР: ТАХОМЕТР В КРАСНОЙ ЗОНЕ ПРИ ЗАЖАТОМ ТОРМОЗЕ!';
        stateTitle.className = 'font-bold text-rose-300 animate-pulse';
        stateDesc.innerHTML = '<strong>Аварийная пара:</strong> Обороты мотора I = ' + I + ' Ав зашкаливают, а спидометр в глубоком минусе (CI = ' + ci + '). Вы жмёте на газ, но внутренний залом держит контур намертво. Энергия обращается в омический ожог проводки (Q = I²·R·t). <span class="text-white">Соматика:</span> Снимите ногу с педали газа, разожмите челюсть, выдохните через рот и отпустите внутреннее сопротивление.';
        if (stateBadge) { stateBadge.textContent = 'ОЖОГ ПРОВОДКИ'; stateBadge.className = 'text-[10px] px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/30'; }
        if (stateBox) stateBox.className = 'p-4 rounded-xl border bg-rose-950/50 border-rose-500/60 text-rose-200 text-xs md:text-sm font-mono space-y-2';
      } else if (I >= 55 && ci >= 20) {
        // SUPERCONDUCTIVITY (High RPM, Free Speed)
        stateTitle.textContent = '⚡ СВЕРХПРОВОДИМОСТЬ (МУСИН): ЧИСТЫЙ ХОД И КРЕЙСЕРСКАЯ СКОРОСТЬ';
        stateTitle.className = 'font-bold text-emerald-300';
        stateDesc.innerHTML = '<strong>Идеальная пара:</strong> Высокие обороты ядра (I = ' + I + ' Ав) при свободном сцеплении проводника (CI = +' + ci + '). Вся кинетическая мощность без трения материализуется в созидательный плод. Проводка ледяная, потерь ноль!';
        if (stateBadge) { stateBadge.textContent = 'КРЕЙСЕРСКИЙ ХОД'; stateBadge.className = 'text-[10px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'; }
        if (stateBox) stateBox.className = 'p-4 rounded-xl border bg-emerald-950/40 border-emerald-500/40 text-emerald-200 text-xs md:text-sm font-mono space-y-2';
      } else if (I < 35 && ci < -30) {
        // VISCOUS CLINCH (Stupor / Procrastination)
        stateTitle.textContent = '🧊 ВЯЗКИЙ КЛИН: МОТОР ЗАГЛУШЕН, ТОРМОЗ ЗАКЛИНИЛ';
        stateTitle.className = 'font-bold text-amber-300';
        stateDesc.innerHTML = '<strong>Пара ступора:</strong> Напор низкий (I = ' + I + ' Ав), а сопротивление максимально (CI = ' + ci + '). Бесполезно подстёгивать себя кофеином (поднимать I) — сначала нужно разблокировать тормоз через физическое движение или 15 минут тишины.';
        if (stateBadge) { stateBadge.textContent = 'СТУПОР КОНТУРА'; stateBadge.className = 'text-[10px] px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30'; }
        if (stateBox) stateBox.className = 'p-4 rounded-xl border bg-amber-950/40 border-amber-500/40 text-amber-200 text-xs md:text-sm font-mono space-y-2';
      } else if (I < 35 && ci >= 20) {
        // COLD CIRCUIT (Regeneration / Sleep)
        stateTitle.textContent = '🌌 ХОЛОДНЫЙ ПОКОЙ (ДЗАНСИН): ТИШИНА И РЕГЕНЕРАЦИЯ ЯДРА';
        stateTitle.className = 'font-bold text-sky-300';
        stateDesc.innerHTML = '<strong>Пара покоя:</strong> Минимальные обороты (I = ' + I + ' Ав) при расправленном чистом контуре (CI = +' + ci + '). Потерь нет, аккумулятор Тандэна восстанавливает заряд. Идеально для созерцания или глубокого сна.';
        if (stateBadge) { stateBadge.textContent = 'РЕГЕНЕРАЦИЯ'; stateBadge.className = 'text-[10px] px-2 py-0.5 rounded bg-sky-500/20 text-sky-300 border border-sky-500/30'; }
        if (stateBox) stateBox.className = 'p-4 rounded-xl border bg-sky-950/40 border-sky-500/40 text-sky-200 text-xs md:text-sm font-mono space-y-2';
      }
    }
'''

    # Inject Tachometer JS before gauge_init
    if 'tach_render' not in content:
        content = content.replace('function gauge_init() {', tach_js + '\n\n    function gauge_init() {\n      setTimeout(() => { if (typeof tach_render === "function") tach_render(75); }, 50);\n')
        print("Tachometer JS controller injected.")

    # In gauge_render, call updateCoupledVerdict at end
    if 'updateCoupledVerdict();' not in content:
        content = content.replace('const emoji = document.getElementById(\'gauge-status-emoji\');', 'const emoji = document.getElementById(\'gauge-status-emoji\');\n      updateCoupledVerdict();')

    return content

def main():
    for file_path in [PUBLIC_TRAINER, DIST_TRAINER]:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                c = f.read()
            patched = patch_trainer_content(c)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(patched)
            print(f"Patched: {file_path}")

if __name__ == '__main__':
    main()
