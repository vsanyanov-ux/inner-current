# -*- coding: utf-8 -*-
"""
Add the 'Circuit Console' (Консоль контура: Напор I vs Сопротивление R)
to public/index.html and sync to dist_site/index.html.
"""
import os
import re
import sys

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(ROOT_DIR, 'public', 'index.html')
DIST_INDEX_PATH = os.path.join(ROOT_DIR, 'dist_site', 'index.html')

SIDEBAR_NEEDLE = '<a href="cockpit.html"'
SIDEBAR_ENTRY = '''          <a id="circuit-console-nav" href="#circuit-console" onclick="navigateSidebar('#circuit-console')" data-section="circuit-console" class="sidebar-nav-item flex items-center justify-between gap-2 px-2.5 py-2 rounded-xl text-slate-300 hover:text-white hover:bg-slate-800/60 border border-transparent transition">
            <span class="flex items-center gap-2">
              <span class="sidebar-icon text-amber-400">🧭</span>
              <span class="font-medium text-amber-200">Консоль контура</span>
            </span>
            <span class="text-[9px] font-mono px-1.5 py-0.5 rounded bg-amber-500/10 text-amber-300 border border-amber-500/20 font-bold">I + R</span>
          </a>
'''

CONSOLE_SECTION = '''
  <!-- ========================================================= -->
  <!-- CIRCUIT CONSOLE: TWO-DIAL TELEMETRY DASHBOARD (I vs R)   -->
  <!-- ========================================================= -->
  <section id="circuit-console" class="py-16 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 border-t border-slate-800/80">
    <div class="text-center max-w-3xl mx-auto mb-10">
      <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 border border-slate-800 text-amber-300 text-xs font-mono font-medium tracking-wider mb-3">
        🧭 БОРТОВОЙ ДАШБОРД СОСТОЯНИЯ • ДВУХСТРЕЛОЧНЫЙ HUD
      </div>
      <h2 class="text-2xl sm:text-3xl font-extrabold text-slate-100 font-display">
        Консоль контура: Сила Тока (<span class="text-cyan-400">I</span>) vs Сопротивление (<span class="text-emerald-400">R</span>)
      </h2>
      <p class="text-slate-400 text-sm mt-3 leading-relaxed">
        Главная приборная панель оператора. Два сопряжённых показателя раскрывают истинную динамику цепи: подаётся ли напор энергии в полезный созидательный ход, либо сгорает на омическом заломе в ожог выгорания.
      </p>
    </div>

    <!-- Main Cockpit Cluster Container -->
    <div class="bg-gradient-to-b from-slate-900/95 via-[#060b17] to-slate-950 border border-slate-800/90 hover:border-amber-500/40 rounded-3xl p-6 sm:p-8 shadow-2xl relative overflow-hidden transition-all duration-300">
      <div id="cc-ambient-glow" class="absolute -right-24 -top-24 w-72 h-72 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none transition-all duration-700"></div>
      <div id="cc-ambient-glow-left" class="absolute -left-24 -bottom-24 w-72 h-72 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none transition-all duration-700"></div>

      <!-- Quick Presets Toolbar -->
      <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800/80 pb-5 mb-8">
        <div class="flex items-center gap-2 text-xs font-mono text-slate-400">
          <span class="text-amber-400 text-base">⚙️</span>
          <span class="uppercase tracking-wider font-semibold text-slate-300">Калибровка контура:</span>
        </div>
        <div class="flex flex-wrap items-center gap-2">
          <button onclick="setCircuitConsolePreset(85, 8)" class="cc-preset-btn px-3 py-1.5 rounded-lg text-xs font-medium bg-cyan-950/60 text-cyan-300 border border-cyan-800/60 hover:bg-cyan-900/80 hover:text-white transition cursor-pointer flex items-center gap-1.5 shadow-sm">
            <span>⚡ Мусин (Поток)</span>
          </button>
          <button onclick="setCircuitConsolePreset(92, 85)" class="cc-preset-btn px-3 py-1.5 rounded-lg text-xs font-medium bg-red-950/60 text-red-300 border border-red-800/60 hover:bg-red-900/80 hover:text-white transition cursor-pointer flex items-center gap-1.5 shadow-sm">
            <span>🔥 Омический пожар</span>
          </button>
          <button onclick="setCircuitConsolePreset(20, 78)" class="cc-preset-btn px-3 py-1.5 rounded-lg text-xs font-medium bg-amber-950/60 text-amber-300 border border-amber-800/60 hover:bg-amber-900/80 hover:text-white transition cursor-pointer flex items-center gap-1.5 shadow-sm">
            <span>🧊 Вязкий клин</span>
          </button>
          <button onclick="setCircuitConsolePreset(15, 6)" class="cc-preset-btn px-3 py-1.5 rounded-lg text-xs font-medium bg-indigo-950/60 text-indigo-300 border border-indigo-800/60 hover:bg-indigo-900/80 hover:text-white transition cursor-pointer flex items-center gap-1.5 shadow-sm">
            <span>🌌 Холодный покой</span>
          </button>
          <button onclick="setCircuitConsolePreset(70, 32)" class="cc-preset-btn px-3 py-1.5 rounded-lg text-xs font-medium bg-emerald-950/60 text-emerald-300 border border-emerald-800/60 hover:bg-emerald-900/80 hover:text-white transition cursor-pointer flex items-center gap-1.5 shadow-sm">
            <span>🏃 Штатный спринт</span>
          </button>
        </div>
      </div>

      <!-- Gauges & HUD Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
        
        <!-- LEFT DIAL: Current / Tachometer (I) -->
        <div class="lg:col-span-4 bg-slate-950/80 border border-slate-800/90 rounded-2xl p-5 flex flex-col items-center relative shadow-inner">
          <div class="w-full flex items-center justify-between mb-3 text-xs font-mono">
            <span class="text-cyan-400 font-bold uppercase tracking-wider flex items-center gap-1.5">
              <span>⚡</span> ТАХОМЕТР ПОТОКА (<span class="font-bold">I</span>)
            </span>
            <span class="px-2 py-0.5 rounded bg-cyan-950/80 border border-cyan-800/50 text-cyan-300 text-[11px] font-bold" id="cc-i-badge">
              75 Ав
            </span>
          </div>

          <!-- SVG Gauge: Current (I) -->
          <div class="relative w-48 h-36 flex items-center justify-center my-1">
            <svg viewBox="0 0 220 155" class="w-full h-full overflow-visible">
              <defs>
                <linearGradient id="ccGradI" x1="0%" y1="100%" x2="100%" y2="0%">
                  <stop offset="0%" stop-color="#38bdf8" />
                  <stop offset="60%" stop-color="#38bdf8" />
                  <stop offset="82%" stop-color="#f59e0b" />
                  <stop offset="100%" stop-color="#ef4444" />
                </linearGradient>
                <filter id="needleShadow" x="-20%" y="-20%" width="140%" height="140%">
                  <feDropShadow dx="0" dy="1" stdDeviation="2" flood-color="#000000" flood-opacity="0.8"/>
                </filter>
              </defs>

              <!-- Track background arc (240 deg sweep) -->
              <circle cx="110" cy="115" r="80" fill="none" stroke="#1e293b" stroke-width="12"
                stroke-dasharray="335.1 167.55" transform="rotate(150, 110, 115)" stroke-linecap="round" />
              
              <!-- Active colored arc -->
              <circle id="cc-i-arc" cx="110" cy="115" r="80" fill="none" stroke="url(#ccGradI)" stroke-width="12"
                stroke-dasharray="251.3 502.65" transform="rotate(150, 110, 115)" stroke-linecap="round"
                style="transition: stroke-dasharray 0.35s cubic-bezier(0.4, 0, 0.2, 1);" />

              <!-- Scale tick texts -->
              <text x="25.1" y="164" fill="#64748b" font-size="10" font-family="monospace" text-anchor="middle">0</text>
              <text x="25.1" y="66" fill="#64748b" font-size="10" font-family="monospace" text-anchor="middle">25</text>
              <text x="110" y="24" fill="#64748b" font-size="10" font-family="monospace" text-anchor="middle">50</text>
              <text x="194.9" y="66" fill="#64748b" font-size="10" font-family="monospace" text-anchor="middle">75</text>
              <text x="194.9" y="164" fill="#ef4444" font-size="10" font-family="monospace" text-anchor="middle">100</text>

              <!-- Needle -->
              <g id="cc-i-needle" transform="rotate(60, 110, 115)" style="transition: transform 0.35s cubic-bezier(0.4, 0, 0.2, 1);">
                <line x1="110" y1="115" x2="110" y2="44" stroke="#f8fafc" stroke-width="3" stroke-linecap="round" filter="url(#needleShadow)" />
                <line x1="110" y1="115" x2="110" y2="52" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" />
                <circle cx="110" cy="115" r="8" fill="#0f172a" stroke="#38bdf8" stroke-width="3" />
                <circle cx="110" cy="115" r="2.5" fill="#f8fafc" />
              </g>
            </svg>
          </div>

          <!-- Digital Value & State -->
          <div class="text-center mt-2 mb-4">
            <div class="text-3xl font-mono font-black text-cyan-300 tracking-tight" id="cc-i-display">75</div>
            <div class="text-[11px] font-mono text-cyan-400/90 mt-0.5" id="cc-i-desc">Высокий рабочий напор</div>
          </div>

          <!-- Slider Control -->
          <div class="w-full space-y-1.5 pt-2 border-t border-slate-800/80">
            <div class="flex justify-between text-[10px] font-mono text-slate-400">
              <span>Штиль (0)</span>
              <span>Газ в пол (100)</span>
            </div>
            <input type="range" id="cc-slider-i" min="0" max="100" value="75"
              class="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-cyan-400 transition" />
            <div class="text-[10px] text-slate-400 text-center font-mono">
              Обороты Тандэна & сила внимания ($I$)
            </div>
          </div>
        </div>

        <!-- CENTER HUD: Diagnostic Computer & 4-Quadrant Radar -->
        <div class="lg:col-span-4 flex flex-col items-center justify-between space-y-4">
          
          <!-- Mode Indicator Badge -->
          <div class="w-full text-center">
            <div class="text-[10px] font-mono text-slate-400 uppercase tracking-widest mb-1.5">
              Диагностический режим контура
            </div>
            <div id="cc-mode-pill" class="w-full py-2.5 px-4 rounded-xl font-bold font-mono text-xs sm:text-sm tracking-wide border shadow-lg transition-all duration-500 bg-cyan-950/70 border-cyan-500/60 text-cyan-200">
              ⚡ СВЕРХПРОВОДИМОСТЬ (МУСИН)
            </div>
          </div>

          <!-- 2D Phase Radar (X = Resistance, Y = Current) -->
          <div class="w-full bg-slate-950/90 border border-slate-800 rounded-2xl p-4 relative shadow-inner">
            <div class="flex justify-between items-center text-[10px] font-mono text-slate-400 mb-2">
              <span>Фазовый радар цепи</span>
              <span id="cc-coords-badge" class="text-amber-400 font-bold">I: 75 | R: 15</span>
            </div>

            <!-- Coordinate Box -->
            <div class="relative w-full h-36 bg-[#040812] border border-slate-800/90 rounded-xl overflow-hidden p-2">
              <!-- Quadrant Background Tints -->
              <div class="absolute inset-0 grid grid-cols-2 grid-rows-2 opacity-30">
                <div class="bg-red-950/50 border-r border-b border-slate-800/60 p-1 flex items-start justify-start">
                  <span class="text-[8px] font-mono text-red-400">IV. Омический пожар</span>
                </div>
                <div class="bg-cyan-950/50 border-b border-slate-800/60 p-1 flex items-start justify-end">
                  <span class="text-[8px] font-mono text-cyan-400">I. Мусин (Поток)</span>
                </div>
                <div class="bg-amber-950/40 border-r border-slate-800/60 p-1 flex items-end justify-start">
                  <span class="text-[8px] font-mono text-amber-400">III. Вязкий клин</span>
                </div>
                <div class="bg-indigo-950/40 p-1 flex items-end justify-end">
                  <span class="text-[8px] font-mono text-indigo-400">II. Дзансин (Покой)</span>
                </div>
              </div>

              <!-- Center Crosshair Lines -->
              <div class="absolute left-1/2 top-0 bottom-0 w-[1px] bg-slate-700/60 pointer-events-none"></div>
              <div class="absolute top-1/2 left-0 right-0 h-[1px] bg-slate-700/60 pointer-events-none"></div>

              <!-- Real-time Position Blip -->
              <div id="cc-radar-blip" class="absolute w-4 h-4 -ml-2 -mt-2 rounded-full border-2 border-white bg-cyan-400 shadow-[0_0_12px_rgba(56,189,248,1)] transition-all duration-300 pointer-events-none" style="left: 15%; bottom: 75%;">
                <div class="w-full h-full rounded-full bg-cyan-300 animate-ping opacity-75"></div>
              </div>
            </div>

            <div class="flex justify-between items-center text-[9px] font-mono text-slate-400 mt-1.5 px-1">
              <span>◄ Залом (R=100)</span>
              <span>▲ Ток (I)</span>
              <span>Чистый кабель (R=0) ►</span>
            </div>
          </div>

          <!-- Calculated Metrics Strip -->
          <div class="w-full grid grid-cols-3 gap-2 text-center font-mono">
            <div class="bg-slate-950/70 border border-slate-800/80 rounded-xl p-2.5">
              <div class="text-[9px] text-slate-400 uppercase">Мощность (P)</div>
              <div class="text-xs sm:text-sm font-bold text-cyan-300 mt-0.5" id="cc-metric-p">63.8 Ан</div>
              <div class="text-[8px] text-slate-400">Свет плода</div>
            </div>
            <div class="bg-slate-950/70 border border-slate-800/80 rounded-xl p-2.5">
              <div class="text-[9px] text-slate-400 uppercase">Нагрев (Q)</div>
              <div class="text-xs sm:text-sm font-bold text-red-400 mt-0.5" id="cc-metric-q">8.4 Бн</div>
              <div class="text-[8px] text-slate-400">Тепловой ожог</div>
            </div>
            <div class="bg-slate-950/70 border border-slate-800/80 rounded-xl p-2.5">
              <div class="text-[9px] text-slate-400 uppercase">КПД (η)</div>
              <div class="text-xs sm:text-sm font-bold text-emerald-300 mt-0.5" id="cc-metric-eta">85%</div>
              <div class="text-[8px] text-slate-400">Проводимость</div>
            </div>
          </div>

          <!-- Diagnostic Verdict Box -->
          <div id="cc-verdict-box" class="w-full p-3.5 rounded-xl border border-cyan-500/30 bg-cyan-950/20 text-xs text-slate-200 leading-relaxed font-sans transition-all duration-300">
            <div class="flex items-start gap-2">
              <span class="text-base shrink-0" id="cc-verdict-icon">✨</span>
              <div id="cc-verdict-text">
                <span class="font-bold text-cyan-300">Режим Мусин:</span> Свободная цепь! Обороты согласованы с проводимостью, паразитное трение отсутствует. Ток беспрепятственно рождает плод.
              </div>
            </div>
          </div>

        </div>

        <!-- RIGHT DIAL: Resistance / Ohmmeter (R) -->
        <div class="lg:col-span-4 bg-slate-950/80 border border-slate-800/90 rounded-2xl p-5 flex flex-col items-center relative shadow-inner">
          <div class="w-full flex items-center justify-between mb-3 text-xs font-mono">
            <span class="text-emerald-400 font-bold uppercase tracking-wider flex items-center gap-1.5">
              <span>🛑</span> ОММЕТР ЗАЛОМА (<span class="font-bold">R</span>)
            </span>
            <span class="px-2 py-0.5 rounded bg-emerald-950/80 border border-emerald-800/50 text-emerald-300 text-[11px] font-bold" id="cc-r-badge">
              15 Ω
            </span>
          </div>

          <!-- SVG Gauge: Resistance (R) -->
          <div class="relative w-48 h-36 flex items-center justify-center my-1">
            <svg viewBox="0 0 220 155" class="w-full h-full overflow-visible">
              <defs>
                <linearGradient id="ccGradR" x1="0%" y1="100%" x2="100%" y2="0%">
                  <stop offset="0%" stop-color="#38bdf8" />
                  <stop offset="25%" stop-color="#10b981" />
                  <stop offset="65%" stop-color="#f59e0b" />
                  <stop offset="100%" stop-color="#ef4444" />
                </linearGradient>
              </defs>

              <!-- Track background arc -->
              <circle cx="110" cy="115" r="80" fill="none" stroke="#1e293b" stroke-width="12"
                stroke-dasharray="335.1 167.55" transform="rotate(150, 110, 115)" stroke-linecap="round" />
              
              <!-- Active colored arc -->
              <circle id="cc-r-arc" cx="110" cy="115" r="80" fill="none" stroke="url(#ccGradR)" stroke-width="12"
                stroke-dasharray="50.2 502.65" transform="rotate(150, 110, 115)" stroke-linecap="round"
                style="transition: stroke-dasharray 0.35s cubic-bezier(0.4, 0, 0.2, 1);" />

              <!-- Scale tick texts -->
              <text x="25.1" y="164" fill="#38bdf8" font-size="10" font-family="monospace" text-anchor="middle">0</text>
              <text x="25.1" y="66" fill="#10b981" font-size="10" font-family="monospace" text-anchor="middle">25</text>
              <text x="110" y="24" fill="#64748b" font-size="10" font-family="monospace" text-anchor="middle">50</text>
              <text x="194.9" y="66" fill="#f59e0b" font-size="10" font-family="monospace" text-anchor="middle">75</text>
              <text x="194.9" y="164" fill="#ef4444" font-size="10" font-family="monospace" text-anchor="middle">100</text>

              <!-- Needle -->
              <g id="cc-r-needle" transform="rotate(-84, 110, 115)" style="transition: transform 0.35s cubic-bezier(0.4, 0, 0.2, 1);">
                <line x1="110" y1="115" x2="110" y2="44" stroke="#f8fafc" stroke-width="3" stroke-linecap="round" filter="url(#needleShadow)" />
                <line x1="110" y1="115" x2="110" y2="52" stroke="#10b981" stroke-width="2" stroke-linecap="round" />
                <circle cx="110" cy="115" r="8" fill="#0f172a" stroke="#10b981" stroke-width="3" />
                <circle cx="110" cy="115" r="2.5" fill="#f8fafc" />
              </g>
            </svg>
          </div>

          <!-- Digital Value & State -->
          <div class="text-center mt-2 mb-4">
            <div class="text-3xl font-mono font-black text-emerald-300 tracking-tight" id="cc-r-display">15</div>
            <div class="text-[11px] font-mono text-emerald-400/90 mt-0.5" id="cc-r-desc">Свободная проводимость</div>
          </div>

          <!-- Slider Control -->
          <div class="w-full space-y-1.5 pt-2 border-t border-slate-800/80">
            <div class="flex justify-between text-[10px] font-mono text-slate-400">
              <span>Мусин (0)</span>
              <span>Глухой клин (100)</span>
            </div>
            <input type="range" id="cc-slider-r" min="0" max="100" value="15"
              class="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-emerald-400 transition" />
            <div class="text-[10px] text-slate-400 text-center font-mono">
              Внутреннее эго-сопротивление ($R$)
            </div>
          </div>
        </div>

      </div>

      <!-- Footer Telemetry Note -->
      <div class="mt-8 pt-4 border-t border-slate-800/80 flex flex-col sm:flex-row items-center justify-between gap-3 text-[11px] font-mono text-slate-400">
        <div class="flex items-center gap-2">
          <span class="text-amber-400">💡</span>
          <span>Формула состояния: <strong class="text-slate-200">P = I · (1 - R/100)</strong> | Тепловые потери: <strong class="text-red-400">Q = I² · R</strong></span>
        </div>
        <div class="flex items-center gap-3">
          <a href="cockpit.html" class="text-cyan-400 hover:text-cyan-300 underline transition">Открыть полный Кокпит OBD-II ↗</a>
        </div>
      </div>

    </div>
  </section>
'''

CONSOLE_SCRIPT = '''
    // =========================================================================
    // CIRCUIT CONSOLE INTERACTIVE CONTROLLER (I vs R)
    // =========================================================================
    let ccCurrentI = 75;
    let ccCurrentR = 15;

    function updateCircuitConsole() {
      const sliderI = document.getElementById('cc-slider-i');
      const sliderR = document.getElementById('cc-slider-r');
      if (sliderI) ccCurrentI = parseInt(sliderI.value, 10);
      if (sliderR) ccCurrentR = parseInt(sliderR.value, 10);

      // Digital values
      const elIDisplay = document.getElementById('cc-i-display');
      const elIBadge = document.getElementById('cc-i-badge');
      const elIDesc = document.getElementById('cc-i-desc');
      if (elIDisplay) elIDisplay.textContent = ccCurrentI;
      if (elIBadge) elIBadge.textContent = ccCurrentI + ' Ав';

      const elRDisplay = document.getElementById('cc-r-display');
      const elRBadge = document.getElementById('cc-r-badge');
      const elRDesc = document.getElementById('cc-r-desc');
      if (elRDisplay) elRDisplay.textContent = ccCurrentR;
      if (elRBadge) elRBadge.textContent = ccCurrentR + ' Ω';

      // Update I Description
      if (elIDesc) {
        if (ccCurrentI < 25) elIDesc.textContent = 'Холостой ход / Покой';
        else if (ccCurrentI < 65) elIDesc.textContent = 'Умеренный рабочий ток';
        else if (ccCurrentI < 85) elIDesc.textContent = 'Высокий рабочий напор';
        else elIDesc.textContent = 'Красная зона (Предельный напор)';
      }

      // Update R Description
      if (elRDesc) {
        if (ccCurrentR <= 20) elRDesc.textContent = 'Сверхпроводимость (Мусин)';
        else if (ccCurrentR <= 50) elRDesc.textContent = 'Штатная нагрузка дела';
        else if (ccCurrentR <= 75) elRDesc.textContent = 'Паразитное трение / Залом';
        else elRDesc.textContent = 'Омический клин / Авария';
      }

      // Needle rotations: angle = -120 + (val / 100) * 240
      const angleI = -120 + (ccCurrentI / 100.0) * 240;
      const angleR = -120 + (ccCurrentR / 100.0) * 240;

      const needleI = document.getElementById('cc-i-needle');
      const needleR = document.getElementById('cc-r-needle');
      if (needleI) needleI.setAttribute('transform', `rotate(${angleI}, 110, 115)`);
      if (needleR) needleR.setAttribute('transform', `rotate(${angleR}, 110, 115)`);

      // Active Arcs: stroke-dasharray = (val / 100 * 335.1) 502.65
      const arcLengthI = (ccCurrentI / 100.0) * 335.1;
      const arcLengthR = (ccCurrentR / 100.0) * 335.1;
      const arcI = document.getElementById('cc-i-arc');
      const arcR = document.getElementById('cc-r-arc');
      if (arcI) arcI.setAttribute('stroke-dasharray', `${arcLengthI.toFixed(1)} 502.65`);
      if (arcR) arcR.setAttribute('stroke-dasharray', `${arcLengthR.toFixed(1)} 502.65`);

      // Physics Metrics Calculation
      // P = I * (1 - R/100) [Anyans]
      const powerP = (ccCurrentI * (1.0 - ccCurrentR / 100.0)).toFixed(1);
      // Q = I^2 * R / 100 / 100 [Bonno loss]
      const heatQ = ((ccCurrentI * ccCurrentI * ccCurrentR) / 10000.0).toFixed(1);
      // Efficiency eta
      const eta = Math.max(0, Math.round(100 - ccCurrentR));

      const elP = document.getElementById('cc-metric-p');
      const elQ = document.getElementById('cc-metric-q');
      const elEta = document.getElementById('cc-metric-eta');
      if (elP) elP.textContent = powerP + ' Ан';
      if (elQ) elQ.textContent = heatQ + ' Бн';
      if (elEta) elEta.textContent = eta + '%';

      // Radar Position Blip:
      // X axis: R (0 on the right, 100 on the left -> percentX = 100 - R)
      // Y axis: I (0 on bottom, 100 on top -> percentY = I)
      const blip = document.getElementById('cc-radar-blip');
      if (blip) {
        const leftPercent = Math.min(94, Math.max(6, 100 - ccCurrentR));
        const bottomPercent = Math.min(94, Math.max(6, ccCurrentI));
        blip.style.left = leftPercent + '%';
        blip.style.bottom = bottomPercent + '%';
      }

      const coordsBadge = document.getElementById('cc-coords-badge');
      if (coordsBadge) coordsBadge.textContent = `I: ${ccCurrentI} | R: ${ccCurrentR}`;

      // Mode Diagnosis & Somatic Verdict
      const modePill = document.getElementById('cc-mode-pill');
      const verdictIcon = document.getElementById('cc-verdict-icon');
      const verdictText = document.getElementById('cc-verdict-text');
      const verdictBox = document.getElementById('cc-verdict-box');
      const glowRight = document.getElementById('cc-ambient-glow');
      const glowLeft = document.getElementById('cc-ambient-glow-left');

      if (ccCurrentI >= 55 && ccCurrentR <= 30) {
        // QUADRANT I: SUPERCONDUCTIVITY (MUSHIN)
        if (modePill) {
          modePill.className = 'w-full py-2.5 px-4 rounded-xl font-bold font-mono text-xs sm:text-sm tracking-wide border shadow-lg transition-all duration-500 bg-cyan-950/80 border-cyan-500/70 text-cyan-200';
          modePill.textContent = '⚡ СВЕРХПРОВОДИМОСТЬ (МУСИН)';
        }
        if (verdictBox) verdictBox.className = 'w-full p-3.5 rounded-xl border border-cyan-500/40 bg-cyan-950/30 text-xs text-slate-200 leading-relaxed font-sans transition-all duration-300';
        if (verdictIcon) verdictIcon.textContent = '🚀';
        if (verdictText) {
          verdictText.innerHTML = '<span class="font-bold text-cyan-300">Режим Мусин (Чистый Поток):</span> Высокий напор при отсутствии внутреннего сопротивления! Колёса не заблокированы, вся энергия без потерь материализуется в результат. Тело расслаблено, фокус лазерный.';
        }
        if (glowRight) glowRight.className = 'absolute -right-24 -top-24 w-72 h-72 bg-cyan-500/20 rounded-full blur-3xl pointer-events-none transition-all duration-700';
        if (glowLeft) glowLeft.className = 'absolute -left-24 -bottom-24 w-72 h-72 bg-emerald-500/20 rounded-full blur-3xl pointer-events-none transition-all duration-700';
      }
      else if (ccCurrentI >= 55 && ccCurrentR > 50) {
        // QUADRANT IV: OHMIC OVERHEAT (BURNOUT / REDLINE BRAKE)
        if (modePill) {
          modePill.className = 'w-full py-2.5 px-4 rounded-xl font-bold font-mono text-xs sm:text-sm tracking-wide border shadow-lg transition-all duration-500 bg-red-950/90 border-red-500/80 text-red-200 animate-pulse';
          modePill.textContent = '🔥 ОМИЧЕСКИЙ ПОЖАР (АВАРИЯ ЦЕПИ)';
        }
        if (verdictBox) verdictBox.className = 'w-full p-3.5 rounded-xl border border-red-500/50 bg-red-950/40 text-xs text-slate-200 leading-relaxed font-sans transition-all duration-300';
        if (verdictIcon) verdictIcon.textContent = '⚠️';
        if (verdictText) {
          verdictText.innerHTML = '<span class="font-bold text-red-300">Авария: Тахометр в красной зоне при зажатом тормозе!</span> Вы давите на газ изо всех сил, но внутренний залом держит контур намертво. Энергия обращается в головную боль и ожог нервной системы. <strong class="text-white">Соматика:</strong> Снимите ногу с газа, разожмите челюсть, выдохните через рот и отпустите внутренний спор.';
        }
        if (glowRight) glowRight.className = 'absolute -right-24 -top-24 w-72 h-72 bg-red-500/25 rounded-full blur-3xl pointer-events-none transition-all duration-700';
        if (glowLeft) glowLeft.className = 'absolute -left-24 -bottom-24 w-72 h-72 bg-orange-500/20 rounded-full blur-3xl pointer-events-none transition-all duration-700';
      }
      else if (ccCurrentI < 45 && ccCurrentR > 50) {
        // QUADRANT III: VISCOUS CLINCH (PROCRASTINATION / STUPOR)
        if (modePill) {
          modePill.className = 'w-full py-2.5 px-4 rounded-xl font-bold font-mono text-xs sm:text-sm tracking-wide border shadow-lg transition-all duration-500 bg-amber-950/80 border-amber-500/70 text-amber-200';
          modePill.textContent = '🧊 ВЯЗКИЙ КЛИН (СТУПОР / БОЛОТО)';
        }
        if (verdictBox) verdictBox.className = 'w-full p-3.5 rounded-xl border border-amber-500/40 bg-amber-950/30 text-xs text-slate-200 leading-relaxed font-sans transition-all duration-300';
        if (verdictIcon) verdictIcon.textContent = '🐌';
        if (verdictText) {
          verdictText.innerHTML = '<span class="font-bold text-amber-300">Вязкий клин (Прокрастинация):</span> Мотор заглушен, но сопротивление пережало систему. Бесполезно подстёгивать себя кофеином (поднимать ток I) — сначала нужно сбросить сопротивление (R) через физическую прогулку или 15 минут тишины.';
        }
        if (glowRight) glowRight.className = 'absolute -right-24 -top-24 w-72 h-72 bg-amber-500/20 rounded-full blur-3xl pointer-events-none transition-all duration-700';
        if (glowLeft) glowLeft.className = 'absolute -left-24 -bottom-24 w-72 h-72 bg-slate-700/20 rounded-full blur-3xl pointer-events-none transition-all duration-700';
      }
      else if (ccCurrentI < 45 && ccCurrentR <= 30) {
        // QUADRANT II: COLD CIRCUIT (ZANSHIN / SHAVASANA / SLEEP)
        if (modePill) {
          modePill.className = 'w-full py-2.5 px-4 rounded-xl font-bold font-mono text-xs sm:text-sm tracking-wide border shadow-lg transition-all duration-500 bg-indigo-950/80 border-indigo-500/70 text-indigo-200';
          modePill.textContent = '🌌 ХОЛОДНЫЙ КОНТУР (ДЗАНСИН / РЕГЕНЕРАЦИЯ)';
        }
        if (verdictBox) verdictBox.className = 'w-full p-3.5 rounded-xl border border-indigo-500/40 bg-indigo-950/30 text-xs text-slate-200 leading-relaxed font-sans transition-all duration-300';
        if (verdictIcon) verdictIcon.textContent = '🧘';
        if (verdictText) {
          verdictText.innerHTML = '<span class="font-bold text-indigo-300">Холодный контур (Дзансин):</span> Проводка ледяная, потерь ноль. Система расправлена, реактор Тандэна накапливает заряд. Идеальное состояние для глубокого созерцания, вечернего чая или восстановительного сна.';
        }
        if (glowRight) glowRight.className = 'absolute -right-24 -top-24 w-72 h-72 bg-indigo-500/20 rounded-full blur-3xl pointer-events-none transition-all duration-700';
        if (glowLeft) glowLeft.className = 'absolute -left-24 -bottom-24 w-72 h-72 bg-purple-500/20 rounded-full blur-3xl pointer-events-none transition-all duration-700';
      }
      else {
        // BALANCED LOAD
        if (modePill) {
          modePill.className = 'w-full py-2.5 px-4 rounded-xl font-bold font-mono text-xs sm:text-sm tracking-wide border shadow-lg transition-all duration-500 bg-slate-900 border-slate-700 text-slate-200';
          modePill.textContent = '⚖️ ШТАТНАЯ НАГРУЗКА ДЕЛА';
        }
        if (verdictBox) verdictBox.className = 'w-full p-3.5 rounded-xl border border-slate-700 bg-slate-900/40 text-xs text-slate-200 leading-relaxed font-sans transition-all duration-300';
        if (verdictIcon) verdictIcon.textContent = '🏃';
        if (verdictText) {
          verdictText.innerHTML = '<span class="font-bold text-slate-100">Штатная нагрузка:</span> Рабочий баланс между напором задачи и текущим трением среды. Контур стабилен.';
        }
      }
    }

    function setCircuitConsolePreset(i, r) {
      const sliderI = document.getElementById('cc-slider-i');
      const sliderR = document.getElementById('cc-slider-r');
      if (sliderI) sliderI.value = i;
      if (sliderR) sliderR.value = r;
      updateCircuitConsole();
    }
    window.setCircuitConsolePreset = setCircuitConsolePreset;
    window.updateCircuitConsole = updateCircuitConsole;

    // Initialize Event Listeners for Circuit Console
    (function initCircuitConsole() {
      const sliderI = document.getElementById('cc-slider-i');
      const sliderR = document.getElementById('cc-slider-r');
      if (sliderI) {
        sliderI.addEventListener('input', updateCircuitConsole);
        sliderI.addEventListener('change', updateCircuitConsole);
      }
      if (sliderR) {
        sliderR.addEventListener('input', updateCircuitConsole);
        sliderR.addEventListener('change', updateCircuitConsole);
      }
      updateCircuitConsole();
    })();
'''

def main():
    if not os.path.exists(INDEX_PATH):
        print(f"Error: {INDEX_PATH} not found!")
        return

    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add Sidebar link if not present
    if 'id="circuit-console-nav"' not in content:
        if SIDEBAR_NEEDLE in content:
            content = content.replace(SIDEBAR_NEEDLE, SIDEBAR_ENTRY + '\n          ' + SIDEBAR_NEEDLE)
            print("Sidebar link added successfully.")
        else:
            print("Warning: SIDEBAR_NEEDLE not found in index.html")

    # 2. Add Section if not present
    if 'id="circuit-console"' not in content:
        haiku_needle = '<!-- ZEN HAIKU & FELINE CIRCUIT GENERATOR -->'
        if haiku_needle in content:
            content = content.replace(haiku_needle, CONSOLE_SECTION + '\n\n  ' + haiku_needle)
            print("Circuit Console section added successfully.")
        else:
            print("Warning: haiku_needle not found in index.html")

    # 3. Add Script if not present
    if 'updateCircuitConsole' not in content:
        script_needle = 'function nextZenHaiku()'
        if script_needle in content:
            content = content.replace(script_needle, CONSOLE_SCRIPT + '\n\n    ' + script_needle)
            print("Circuit Console script added successfully.")
        else:
            print("Warning: script_needle not found in index.html")

    # 4. Update Scrollspy to include circuit-console
    scrollspy_old = "const sections = ['house', 'books', 'audiobook', 'reader', 'monographs', 'flashlight'];"
    scrollspy_new = "const sections = ['house', 'books', 'audiobook', 'reader', 'monographs', 'flashlight', 'circuit-console', 'zen-haiku'];"
    if scrollspy_old in content:
        content = content.replace(scrollspy_old, scrollspy_new)
        print("Scrollspy sections updated.")

    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {INDEX_PATH} ({len(content)} bytes)")

    # 5. Sync to dist_site/index.html
    if os.path.exists(os.path.dirname(DIST_INDEX_PATH)):
        with open(DIST_INDEX_PATH, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Synced to {DIST_INDEX_PATH}")

if __name__ == '__main__':
    main()
