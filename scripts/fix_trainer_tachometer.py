# -*- coding: utf-8 -*-
"""
Fix Tachometer (I) interactivity and needle animation in public/trainer.html and dist_site/trainer.html.
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

TACH_CONTROLLER_JS = '''
    // =========================================================================
    // TACHOMETER (I) CONTROLLER & DUAL COUPLING ENGINE
    // =========================================================================
    let tachCurrentI = 75;
    let tachCurrentAngle = 45; // angle for I=75: (75-50)*1.8 = 45 deg
    let tachAnimFrame = null;

    function updateTachNeedleGeometry(angleDeg) {
      const rad = (angleDeg * Math.PI) / 180;
      const s = Math.sin(rad);
      const c = Math.cos(rad);
      const cx = 150;
      const cy = 140;

      const tipX = cx + 118 * s;
      const tipY = cy - 118 * c;

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
      const targetAngle = (tachCurrentI - 50) * 1.8;

      if (tachAnimFrame) cancelAnimationFrame(tachAnimFrame);
      const startAngle = tachCurrentAngle !== null ? tachCurrentAngle : targetAngle;
      const startTime = performance.now();
      const duration = 200;

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
        if (iEmoji) iEmoji.textContent = '🟡';
        if (iLabel) {
          iLabel.textContent = '🟡 УМЕРЕННЫЙ ФОКУС';
          iLabel.className = 'text-sm font-bold font-mono text-amber-300 uppercase tracking-wide';
        }
      } else {
        if (iEmoji) iEmoji.textContent = '🔵';
        if (iLabel) {
          iLabel.textContent = '🔵 ХОЛОСТОЙ ХОД / ПОКОЙ';
          iLabel.className = 'text-sm font-bold font-mono text-sky-400 uppercase tracking-wide';
        }
      }

      updateCoupledVerdict();
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
        stateTitle.textContent = '🔥 ОМИЧЕСКИЙ ПОЖАР: ТАХОМЕТР В КРАСНОЙ ЗОНЕ ПРИ ЗАЖАТОМ ТОРМОЗЕ!';
        stateTitle.className = 'font-bold text-rose-300 animate-pulse';
        stateDesc.innerHTML = '<strong>Аварийная пара:</strong> Обороты мотора I = ' + I + ' Ав зашкаливают, а спидометр в глубоком минусе (CI = ' + ci + '). Вы жмёте на газ, но внутренний залом держит контур намертво. Энергия обращается в омический ожог проводки (Q = I²·R·t). <span class="text-white">Соматика:</span> Снимите ногу с педали газа, разожмите челюсть, выдохните через рот и отпустите внутреннее сопротивление.';
        if (stateBadge) { stateBadge.textContent = 'ОЖОГ ПРОВОДКИ'; stateBadge.className = 'text-[10px] px-2 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/30'; }
        if (stateBox) stateBox.className = 'p-4 rounded-xl border bg-rose-950/50 border-rose-500/60 text-rose-200 text-xs md:text-sm font-mono space-y-2';
      } else if (I >= 55 && ci >= 20) {
        stateTitle.textContent = '⚡ СВЕРХПРОВОДИМОСТЬ (МУСИН): ЧИСТЫЙ ХОД И КРЕЙСЕРСКАЯ СКОРОСТЬ';
        stateTitle.className = 'font-bold text-emerald-300';
        stateDesc.innerHTML = '<strong>Идеальная пара:</strong> Высокие обороты ядра (I = ' + I + ' Ав) при свободном сцеплении проводника (CI = +' + ci + '). Вся кинетическая мощность без трения материализуется в созидательный плод. Проводка ледяная, потерь ноль!';
        if (stateBadge) { stateBadge.textContent = 'КРЕЙСЕРСКИЙ ХОД'; stateBadge.className = 'text-[10px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'; }
        if (stateBox) stateBox.className = 'p-4 rounded-xl border bg-emerald-950/40 border-emerald-500/40 text-emerald-200 text-xs md:text-sm font-mono space-y-2';
      } else if (I < 35 && ci < -30) {
        stateTitle.textContent = '🧊 ВЯЗКИЙ КЛИН: МОТОР ЗАГЛУШЕН, ТОРМОЗ ЗАКЛИНИЛ';
        stateTitle.className = 'font-bold text-amber-300';
        stateDesc.innerHTML = '<strong>Пара ступора:</strong> Напор низкий (I = ' + I + ' Ав), а сопротивление максимально (CI = ' + ci + '). Бесполезно подстёгивать себя кофеином (поднимать I) — сначала нужно разблокировать тормоз через физическое движение или 15 минут тишины.';
        if (stateBadge) { stateBadge.textContent = 'СТУПОР КОНТУРА'; stateBadge.className = 'text-[10px] px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30'; }
        if (stateBox) stateBox.className = 'p-4 rounded-xl border bg-amber-950/40 border-amber-500/40 text-amber-200 text-xs md:text-sm font-mono space-y-2';
      } else if (I < 35 && ci >= 20) {
        stateTitle.textContent = '🌌 ХОЛОДНЫЙ ПОКОЙ (ДЗАНСИН): ТИШИНА И РЕГЕНЕРАЦИЯ ЯДРА';
        stateTitle.className = 'font-bold text-sky-300';
        stateDesc.innerHTML = '<strong>Пара покоя:</strong> Минимальные обороты (I = ' + I + ' Ав) при расправленном чистом контуре (CI = +' + ci + '). Потерь нет, аккумулятор Тандэна восстанавливает заряд. Идеально для созерцания или глубокого сна.';
        if (stateBadge) { stateBadge.textContent = 'РЕГЕНЕРАЦИЯ'; stateBadge.className = 'text-[10px] px-2 py-0.5 rounded bg-sky-500/20 text-sky-300 border border-sky-500/30'; }
        if (stateBox) stateBox.className = 'p-4 rounded-xl border bg-sky-950/40 border-sky-500/40 text-sky-200 text-xs md:text-sm font-mono space-y-2';
      }
    }
'''

def patch_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Clean out any previous incomplete tach_render fragments if any
    if 'function tach_render' in content:
        content = re.sub(r'// =+\s*// TACHOMETER \(I\) CONTROLLER[\s\S]*?window\.tach_render = tach_render;', '', content)

    # 2. Insert TACH_CONTROLLER_JS before gauge_render()
    needle = 'function gauge_render() {'
    if needle in content:
        content = content.replace(needle, TACH_CONTROLLER_JS + '\n\n    ' + needle)
        print(f"Injected TACH_CONTROLLER_JS before gauge_render in {file_path}")
    else:
        print(f"Error: {needle} not found in {file_path}")

    # 3. In DOMContentLoaded, initialize tachometer properly
    dom_needle = 'gauge_render();'
    dom_replacement = '''gauge_render();
      if (typeof tach_render === 'function') {
        const sliderTach = document.getElementById('slider-tach-i');
        const initialI = sliderTach ? parseInt(sliderTach.value, 10) || 75 : 75;
        tach_render(initialI);
        if (sliderTach) {
          sliderTach.addEventListener('input', (e) => tach_onSliderChange(e.target.value));
          sliderTach.addEventListener('change', (e) => tach_onSliderChange(e.target.value));
        }
      }'''
    if dom_needle in content and 'slider-tach-i' not in content[content.find(dom_needle):content.find(dom_needle)+300]:
        content = content.replace(dom_needle, dom_replacement, 1)
        print(f"Updated DOMContentLoaded in {file_path}")

    # 4. In gauge_applyPreset, also set Tachometer I to match preset
    preset_needle = 'gauge_render();\n      playZenChime(640);'
    preset_replacement = '''if (typeof tach_render === 'function') {
        let presetI = 75;
        if (presetName === 'mushin') presetI = 85;
        else if (presetName === 'flow') presetI = 75;
        else if (presetName === 'npc') presetI = 20;
        else if (presetName === 'rumination') presetI = 70;
        else if (presetName === 'panic') presetI = 95;
        const sliderTach = document.getElementById('slider-tach-i');
        if (sliderTach) sliderTach.value = presetI;
        tach_render(presetI);
      }
      gauge_render();
      playZenChime(640);'''
    if preset_needle in content:
        content = content.replace(preset_needle, preset_replacement)
        print(f"Updated gauge_applyPreset in {file_path}")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Saved: {file_path}")

def main():
    patch_file(PUBLIC_TRAINER)
    patch_file(DIST_TRAINER)

if __name__ == '__main__':
    main()
