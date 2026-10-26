import fs from 'node:fs';
import path from 'node:path';

const htmlContent = `<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Тренажёр Внутреннего Тока 2.0 — Спидометр R_ego и Живая Цепь</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    @keyframes pulse-glow {
      0%, 100% { filter: drop-shadow(0 0 15px rgba(234, 179, 8, 0.6)); }
      50% { filter: drop-shadow(0 0 35px rgba(234, 179, 8, 0.9)); }
    }
    @keyframes pulse-superconduct {
      0%, 100% { filter: drop-shadow(0 0 15px rgba(56, 189, 248, 0.7)); }
      50% { filter: drop-shadow(0 0 40px rgba(56, 189, 248, 1)); }
    }
    @keyframes pulse-overheat {
      0%, 100% { filter: drop-shadow(0 0 18px rgba(239, 68, 68, 0.8)); transform: scale(1); }
      50% { filter: drop-shadow(0 0 38px rgba(239, 68, 68, 1)); transform: scale(1.02); }
    }
    .flow-line {
      stroke-dasharray: 8 8;
      animation: dash 1s linear infinite;
    }
    .flow-reverse {
      stroke-dasharray: 8 8;
      animation: dash-reverse 1.2s linear infinite;
    }
    @keyframes dash {
      from { stroke-dashoffset: 32; }
      to { stroke-dashoffset: 0; }
    }
    @keyframes dash-reverse {
      from { stroke-dashoffset: 0; }
      to { stroke-dashoffset: 32; }
    }
    
    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    ::-webkit-scrollbar-track {
      background: #020617;
    }
    ::-webkit-scrollbar-thumb {
      background: #1e293b;
      border-radius: 9999px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: #334155;
    }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen font-sans antialiased selection:bg-amber-500 selection:text-black">

  <div class="flex flex-col md:flex-row min-h-screen">
    
    <!-- ==================== LEFT SIDEBAR ==================== -->
    <aside class="w-full md:w-72 lg:w-80 shrink-0 bg-slate-900/95 border-r border-slate-800/80 p-5 flex flex-col justify-between backdrop-blur-xl md:sticky md:top-0 md:h-screen z-30 md:overflow-y-auto">
      <div class="space-y-6">
        
        <!-- Brand & Logo -->
        <div class="flex items-center gap-3 pb-4 border-b border-slate-800">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-amber-500 to-cyan-400 flex items-center justify-center text-xl shadow-lg shadow-amber-500/20 shrink-0 font-mono font-bold text-slate-950">
            ⚡
          </div>
          <div>
            <h1 class="text-base font-bold tracking-tight bg-gradient-to-r from-amber-400 via-cyan-300 to-sky-300 bg-clip-text text-transparent">
              Inner Current
            </h1>
            <p class="text-[11px] text-slate-400 font-mono">Тренажёр цепи 2.0 • Кансо</p>
          </div>
        </div>

        <!-- Mode Indicator Badge -->
        <div class="p-3 rounded-xl bg-slate-950/70 border border-slate-800/80 space-y-1">
          <div class="text-[10px] font-mono uppercase tracking-wider text-slate-400 flex items-center justify-between">
            <span>Режим оператора</span>
            <span id="sidebarActiveBadge" class="px-1.5 py-0.5 rounded text-[9px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">Спидометр</span>
          </div>
          <div id="sidebarModeDesc" class="text-xs text-slate-200 font-medium">
            Калибровка внутреннего сопротивления R_ego
          </div>
        </div>

        <!-- 3 Master Navigation Buttons -->
        <div class="space-y-2">
          <div class="text-[10px] font-mono uppercase tracking-widest text-slate-400 font-semibold px-1">
            Приборы оператора
          </div>

          <!-- Tab 1: Speedometer (DEFAULT / HERO) -->
          <button id="nav-tab-speedometer" onclick="switchTab('speedometer')" class="w-full text-left p-3 rounded-xl border transition-all duration-200 flex items-center gap-3 group relative overflow-hidden bg-gradient-to-r from-emerald-500/15 via-slate-900 to-slate-900 border-emerald-500/40 cursor-pointer shadow-lg shadow-emerald-500/10">
            <span class="text-xl shrink-0" id="nav-icon-speedometer">🎯</span>
            <div class="flex-1 min-w-0">
              <div class="flex items-center justify-between gap-1">
                <span class="text-xs font-bold text-emerald-300 group-hover:text-emerald-200 transition truncate" id="nav-title-speedometer">
                  1. Спидометр R_ego
                </span>
                <span id="nav-ci-pill" class="text-[9px] font-mono font-bold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">+84</span>
              </div>
              <p class="text-[10px] text-slate-400 truncate mt-0.5">Зонтик 5 систем • Живая цепь</p>
            </div>
          </button>

          <!-- Tab 2: Pain-First Navigator -->
          <button id="nav-tab-pains" onclick="switchTab('pains')" class="w-full text-left p-3 rounded-xl border transition-all duration-200 flex items-center gap-3 group relative overflow-hidden bg-slate-950/40 border-slate-800 hover:border-slate-700 cursor-pointer">
            <span class="text-xl shrink-0" id="nav-icon-pains">🚨</span>
            <div class="flex-1 min-w-0">
              <div class="flex items-center justify-between gap-1">
                <span class="text-xs font-bold text-slate-200 group-hover:text-rose-300 transition truncate" id="nav-title-pains">
                  2. Аптечка болей
                </span>
                <span class="text-[9px] font-mono px-1.5 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/30">5 аварий</span>
              </div>
              <p class="text-[10px] text-slate-400 truncate mt-0.5">Сброс перегрева за 60 секунд</p>
            </div>
          </button>

          <!-- Tab 3: Laboratory & Laws -->
          <button id="nav-tab-lab" onclick="switchTab('lab')" class="w-full text-left p-3 rounded-xl border transition-all duration-200 flex items-center gap-3 group relative overflow-hidden bg-slate-950/40 border-slate-800 hover:border-slate-700 cursor-pointer">
            <span class="text-xl shrink-0" id="nav-icon-lab">⚡</span>
            <div class="flex-1 min-w-0">
              <div class="flex items-center justify-between gap-1">
                <span class="text-xs font-bold text-slate-200 group-hover:text-amber-300 transition truncate" id="nav-title-lab">
                  3. Лаборатория R→0
                </span>
                <span class="text-[9px] font-mono px-1.5 py-0.5 rounded bg-cyan-500/20 text-cyan-300 border border-cyan-500/30">Канон</span>
              </div>
              <p class="text-[10px] text-slate-400 truncate mt-0.5">Формулы • 10 быков • Законы цепи</p>
            </div>
          </button>
        </div>

        <!-- Live Status Card -->
        <div class="p-3.5 rounded-xl bg-gradient-to-b from-slate-950/90 to-slate-900 border border-slate-800 text-xs font-mono space-y-2">
          <div class="flex items-center justify-between text-[10px] text-slate-400 uppercase tracking-wider">
            <span>Телеметрия</span>
            <span id="side-status-dot" class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          </div>
          <div class="flex items-baseline justify-between">
            <span class="text-slate-400">Индекс проводимости:</span>
            <span id="side-ci-readout" class="font-bold text-emerald-400 text-sm">+84 CI</span>
          </div>
          <div class="flex items-baseline justify-between">
            <span class="text-slate-400">Сопротивление эго:</span>
            <span id="side-r-readout" class="font-bold text-cyan-400">0.05 Ω</span>
          </div>
          <div class="flex items-baseline justify-between">
            <span class="text-slate-400">Омический нагрев:</span>
            <span id="side-q-readout" class="font-bold text-emerald-400">0.1 Вт</span>
          </div>
        </div>

        <!-- Portal Navigation & Ecosystem Links -->
        <div class="space-y-1.5 pt-2 border-t border-slate-800">
          <div class="text-[10px] font-mono uppercase tracking-widest text-slate-400 font-semibold px-1 mb-2">
            Экосистема
          </div>

          <a href="/cockpit" class="flex items-center justify-between p-2 rounded-lg bg-slate-950/50 hover:bg-slate-800/80 text-xs text-slate-300 hover:text-white border border-slate-800/60 transition group">
            <span class="flex items-center gap-2">
              <span>🎛️</span>
              <span>Пульт Cockpit</span>
            </span>
            <span class="text-[10px] text-slate-400 group-hover:text-cyan-300 font-mono">↗</span>
          </a>

          <a href="/book" class="flex items-center justify-between p-2 rounded-lg bg-slate-950/50 hover:bg-slate-800/80 text-xs text-slate-300 hover:text-white border border-slate-800/60 transition group">
            <span class="flex items-center gap-2">
              <span>📖</span>
              <span>Ридер книг</span>
            </span>
            <span class="text-[10px] text-slate-400 group-hover:text-amber-300 font-mono">7 книг ↗</span>
          </a>

          <a href="/audiobook" class="flex items-center justify-between p-2 rounded-lg bg-slate-950/50 hover:bg-slate-800/80 text-xs text-slate-300 hover:text-white border border-slate-800/60 transition group">
            <span class="flex items-center gap-2">
              <span>🎧</span>
              <span>Аудиокнига</span>
            </span>
            <span class="text-[10px] text-slate-400 group-hover:text-cyan-300 font-mono">Студия ↗</span>
          </a>

          <a href="/wiki" class="flex items-center justify-between p-2 rounded-lg bg-slate-950/50 hover:bg-slate-800/80 text-xs text-slate-300 hover:text-white border border-slate-800/60 transition group">
            <span class="flex items-center gap-2">
              <span>📚</span>
              <span>База Знаний (Вики)</span>
            </span>
            <span class="text-[10px] text-slate-400 group-hover:text-sky-300 font-mono">230+ ↗</span>
          </a>
        </div>

      </div>

      <!-- Footer Info -->
      <div class="pt-4 border-t border-slate-800 text-[10px] text-slate-400 space-y-1">
        <div class="flex items-center justify-between">
          <span>Версия: 2.0 Kanso</span>
          <span class="text-amber-400/80 font-mono">R → 0</span>
        </div>
        <p class="text-slate-400">© Владимир Аньянов • innercurrent.ru</p>
      </div>
    </aside>

    <!-- ==================== MAIN CONTENT AREA ==================== -->
    <main class="flex-1 p-4 md:p-8 overflow-y-auto max-w-7xl mx-auto w-full">

      <!-- ============================================================== -->
      <!-- VIEW 1: SPEEDOMETER & LIVE CIRCUIT (HERO / DEFAULT)            -->
      <!-- ============================================================== -->
      <div id="view-speedometer" class="space-y-6">
        
        <!-- Header & Quick Scenarios -->
        <header class="bg-slate-900/90 border border-emerald-500/30 rounded-2xl p-6 backdrop-blur-md shadow-2xl flex flex-col lg:flex-row justify-between items-start lg:items-center gap-5 relative overflow-hidden">
          <div class="absolute -right-10 -top-10 w-48 h-48 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none"></div>
          <div class="space-y-1 relative z-10">
            <div class="flex items-center gap-3">
              <span class="text-3xl p-2.5 rounded-xl bg-gradient-to-br from-emerald-500/20 to-teal-500/20 border border-emerald-500/40 text-emerald-300 shadow-lg shadow-emerald-500/10">🎯</span>
              <div>
                <div class="flex items-center gap-2 flex-wrap">
                  <h1 class="text-2xl md:text-3xl font-bold tracking-tight bg-gradient-to-r from-emerald-300 via-teal-200 to-cyan-300 bg-clip-text text-transparent">
                    Спидометр внутреннего сопротивления
                  </h1>
                  <span class="text-xs uppercase tracking-widest px-2.5 py-0.5 bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 rounded-full font-mono font-bold">
                    Калибровка цепи R_ego
                  </span>
                </div>
                <p class="text-slate-300 text-xs md:text-sm mt-1">
                  Сведение 5 биологических систем к единому Закону Проводимости: Тандэн ⟶ Внимание ⟶ Действие.
                </p>
              </div>
            </div>
          </div>

          <!-- Quick Scenario Presets -->
          <div class="flex flex-wrap items-center gap-2 relative z-10">
            <span class="text-xs uppercase tracking-wider text-slate-400 font-mono">Пресеты:</span>
            <button onclick="gauge_applyPreset('mushin')" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-emerald-950/80 border border-emerald-700/60 text-emerald-300 hover:bg-emerald-900 transition flex items-center gap-1.5 cursor-pointer shadow-md">
              <span>🍵</span> Мусин (+95)
            </button>
            <button onclick="gauge_applyPreset('flow')" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-cyan-950/80 border border-cyan-700/60 text-cyan-300 hover:bg-cyan-900 transition flex items-center gap-1.5 cursor-pointer">
              <span>💻</span> Flow (+75)
            </button>
            <button onclick="gauge_applyPreset('npc')" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 border border-slate-700 text-slate-300 hover:bg-slate-700 transition flex items-center gap-1.5 cursor-pointer">
              <span>🥱</span> Дрейф (0)
            </button>
            <button onclick="gauge_applyPreset('rumination')" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-amber-950/80 border border-amber-700/60 text-amber-300 hover:bg-amber-900 transition flex items-center gap-1.5 cursor-pointer">
              <span>🧠</span> DMN тревога (-55)
            </button>
            <button onclick="gauge_applyPreset('panic')" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-rose-950/80 border border-rose-700/60 text-rose-300 hover:bg-rose-900 transition flex items-center gap-1.5 cursor-pointer">
              <span>🔥</span> Дистресс (-90)
            </button>
          </div>
        </header>

        <!-- Master Instrument: Speedometer Gauge + Live Status -->
        <div class="bg-gradient-to-b from-slate-900/90 via-slate-900/70 to-slate-950/90 border border-slate-800 rounded-2xl p-6 md:p-8 backdrop-blur-md shadow-2xl relative overflow-hidden">
          <div id="gauge-ambient-glow" class="absolute -right-16 -top-16 w-80 h-80 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none transition-all duration-700"></div>

          <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center relative z-10">
            
            <!-- Left: Speedometer Dial (SVG) -->
            <div class="lg:col-span-5 flex flex-col items-center justify-center p-6 rounded-2xl bg-slate-950/85 border border-slate-800 text-center shadow-xl relative overflow-hidden">
              <div class="text-[11px] font-mono uppercase tracking-widest text-slate-400 font-bold mb-1 flex items-center gap-2">
                <span id="gauge-status-emoji" class="text-lg">🎯</span>
                <span>Индекс Проводимости (CI)</span>
              </div>

              <!-- SVG SPEEDOMETER DIAL -->
              <div class="w-full max-w-[290px] my-2 relative">
                <svg viewBox="0 0 300 170" class="w-full overflow-visible select-none drop-shadow-lg">
                  <defs>
                    <linearGradient id="needle-gradient" x1="0%" y1="100%" x2="0%" y2="0%">
                      <stop offset="0%" stop-color="#0284c7"/>
                      <stop offset="35%" stop-color="#38bdf8"/>
                      <stop offset="85%" stop-color="#7dd3fc"/>
                      <stop offset="100%" stop-color="#ffffff"/>
                    </linearGradient>
                    <filter id="needle-glow" x="-50%" y="-50%" width="200%" height="200%">
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
                  <!-- Red Zone (-100 to -30) -->
                  <path d="M 50 140 A 100 100 0 0 1 100 53.4" fill="none" stroke="#ef4444" stroke-width="14" stroke-linecap="round" opacity="0.95"/>
                  <!-- Yellow Zone (-30 to +20) -->
                  <path d="M 100 53.4 A 100 100 0 0 1 184.2 46.0" fill="none" stroke="#f59e0b" stroke-width="14" stroke-linecap="butt" opacity="0.95"/>
                  <!-- Green Zone (+20 to +100) -->
                  <path d="M 184.2 46.0 A 100 100 0 0 1 250 140" fill="none" stroke="#10b981" stroke-width="14" stroke-linecap="round" opacity="0.95"/>

                  <!-- Ticks and Scale Marks -->
                  <line x1="50" y1="140" x2="38" y2="140" stroke="#ef4444" stroke-width="2"/>
                  <text x="32" y="144" fill="#f87171" font-size="10" font-family="monospace" text-anchor="end" font-weight="bold">-100</text>

                  <line x1="79.3" y1="69.3" x2="71" y2="61" stroke="#ef4444" stroke-width="2"/>
                  <text x="65" y="58" fill="#f87171" font-size="9" font-family="monospace" text-anchor="end">-50</text>

                  <line x1="150" y1="40" x2="150" y2="28" stroke="#f59e0b" stroke-width="2"/>
                  <text x="150" y="24" fill="#fbbf24" font-size="11" font-family="monospace" text-anchor="middle" font-weight="bold">0</text>

                  <line x1="220.7" y1="69.3" x2="229" y2="61" stroke="#10b981" stroke-width="2"/>
                  <text x="235" y="58" fill="#34d399" font-size="9" font-family="monospace" text-anchor="start">+50</text>

                  <line x1="250" y1="140" x2="262" y2="140" stroke="#10b981" stroke-width="2"/>
                  <text x="268" y="144" fill="#34d399" font-size="10" font-family="monospace" text-anchor="start" font-weight="bold">+100</text>

                  <!-- Labels: СТРЕСС / ДРЕЙФ / СЧАСТЬЕ -->
                  <text x="62" y="112" fill="#fca5a5" font-size="8" font-family="sans-serif" font-weight="bold">🔴 СТРЕСС</text>
                  <text x="150" y="70" fill="#fde68a" font-size="7" font-family="sans-serif" font-weight="semibold" text-anchor="middle">🟡 ДРЕЙФ</text>
                  <text x="238" y="112" fill="#6ee7b7" font-size="8" font-family="sans-serif" font-weight="bold" text-anchor="end">🟢 СЧАСТЬЕ</text>

                  <!-- Dynamic Speedometer Needle -->
                  <g id="gauge-needle-group">
                    <polygon id="gauge-needle-counter" points="146.5,140 153.5,140 150,154" fill="#0f172a" stroke="#38bdf8" stroke-width="1.5" opacity="0.85"/>
                    <polygon id="gauge-needle-beam" points="146.5,140 153.5,140 151,22 149,22" fill="url(#needle-gradient)" filter="url(#needle-glow)"/>
                    <line id="gauge-needle-spine" x1="150" y1="140" x2="150" y2="22" stroke="#ffffff" stroke-width="0.8" opacity="0.9"/>
                    
                    <circle id="gauge-needle-tip-glow" cx="150" cy="22" r="3" fill="#38bdf8" filter="url(#needle-glow)"/>
                    <circle id="gauge-needle-tip-core" cx="150" cy="22" r="1.2" fill="#ffffff"/>

                    <circle id="gauge-needle-lens-outer" cx="150" cy="40" r="10" fill="#090d16" stroke="#38bdf8" stroke-width="2.5" filter="url(#needle-glow)"/>
                    <circle id="gauge-needle-lens-ring" cx="150" cy="40" r="5.5" fill="none" stroke="#7dd3fc" stroke-width="1.2" stroke-dasharray="2 1.5"/>
                    <circle id="gauge-needle-lens-dot" cx="150" cy="40" r="2.5" fill="#38bdf8"/>
                    <circle id="gauge-needle-lens-glint" cx="150" cy="40" r="1" fill="#ffffff"/>

                    <circle cx="150" cy="140" r="12" fill="#0b1329" stroke="#38bdf8" stroke-width="2.5" filter="url(#needle-glow)"/>
                    <circle cx="150" cy="140" r="5.5" fill="#38bdf8"/>
                    <circle cx="150" cy="140" r="2" fill="#ffffff"/>
                  </g>
                </svg>
              </div>

              <!-- Main Numeric Readout -->
              <div class="my-1">
                <span id="gauge-ci-val" class="text-6xl md:text-7xl font-black font-mono tracking-tight bg-gradient-to-r from-emerald-400 via-teal-300 to-cyan-300 bg-clip-text text-transparent">
                  +84
                </span>
              </div>

              <div id="gauge-state-label" class="text-sm font-bold font-mono text-emerald-300 uppercase tracking-wide">
                🟢 СВЕРХПРОВОДИМОСТЬ (МУСИН)
              </div>
              <div id="gauge-h-sub" class="text-xs text-slate-300 font-mono mt-0.5">
                КПД Бытия: <span id="gauge-h-val" class="text-amber-300 font-bold">92%</span> • Ток без потерь
              </div>
            </div>

            <!-- Right: State Diagnosis, Automotive Metaphor & 30s Reset -->
            <div class="lg:col-span-7 space-y-4">
              
              <!-- Metaphor Banner -->
              <div class="p-4 rounded-xl bg-slate-950/70 border border-slate-800 space-y-2">
                <div class="flex items-center gap-2 text-xs font-mono font-bold text-slate-200">
                  <span class="text-base">🚗</span>
                  <span class="uppercase tracking-widest text-slate-400">Принцип одного спидометра:</span>
                </div>
                <p class="text-xs text-slate-300 leading-relaxed">
                  Водителю не нужны 50 графиков давления в топливной рампе — ему нужен <strong>один спидометр</strong>. Все 5 биологических датчиков ниже измеряют <strong>одно и то же паразитное сопротивление эго (R_ego)</strong>. В красной зоне цепь горит по закону Джоуля — Ленца (Q = I² · R · t). В зелёной зоне ток совершает созидательную работу в мире (R → 0).
                </p>
              </div>

              <!-- Dynamic Verdict Box -->
              <div id="gauge-state-box" class="p-4 rounded-xl border bg-emerald-950/40 border-emerald-500/40 text-emerald-200 text-xs md:text-sm font-mono space-y-2">
                <div class="flex items-center justify-between">
                  <span class="font-bold text-emerald-300" id="gauge-state-title">СТАТУС: КОНТУР В РЕЖИМЕ СВЕРХПРОВОДИМОСТИ</span>
                  <span id="gauge-state-badge" class="text-[10px] px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">H &gt; 60%</span>
                </div>
                <div class="text-slate-300 text-xs leading-relaxed" id="gauge-state-desc">
                  Внутреннее сопротивление сведено к минимуму (R_ego → 0). Вентральный блуждающий нерв синхронизирует дыхание и сердце, DMN молчит, префронтальная кора работает в режиме TPN (поток). Энергия течёт сквозь проводник без омического трения. Вы переживаете счастье как физическую проводимость жизни!
                </div>
              </div>

              <!-- Live Formula HUD -->
              <div class="grid grid-cols-3 gap-2 text-center font-mono">
                <div class="p-2.5 rounded-xl bg-slate-950/90 border border-slate-800">
                  <div class="text-[10px] text-slate-400 uppercase">Сопротивление</div>
                  <div class="text-base font-bold text-cyan-300" id="live-rego-val">0.05 Ω</div>
                </div>
                <div class="p-2.5 rounded-xl bg-slate-950/90 border border-slate-800">
                  <div class="text-[10px] text-slate-400 uppercase">Нагрев Q</div>
                  <div class="text-base font-bold text-emerald-400" id="live-heat-val">0.1 Вт</div>
                </div>
                <div class="p-2.5 rounded-xl bg-slate-950/90 border border-slate-800">
                  <div class="text-[10px] text-slate-400 uppercase">КПД Контура</div>
                  <div class="text-base font-bold text-amber-300" id="live-eff-val">92%</div>
                </div>
              </div>

              <!-- Quick Action Calibration -->
              <div class="flex flex-wrap items-center gap-3 pt-1">
                <button onclick="gauge_calibrateMushin()" class="py-2.5 px-5 rounded-xl bg-gradient-to-r from-emerald-500 via-teal-400 to-cyan-400 hover:opacity-95 text-slate-950 font-bold text-xs shadow-lg shadow-emerald-500/20 transition flex items-center gap-2 cursor-pointer active:scale-98">
                  <span>⚡</span>
                  <span>Калибровка: Вернуть стрелку в Зеленую зону (R → 0)</span>
                </button>
                <button onclick="switchTab('pains')" class="py-2.5 px-4 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold text-xs transition border border-slate-700 flex items-center gap-1.5 cursor-pointer">
                  <span>🚨</span>
                  <span>Открыть Аптечку болей</span>
                </button>
              </div>

            </div>

          </div>

        </div>

        <!-- ==================== LIVE CIRCUIT SCHEMATIC (FLASHLIGHT MODEL) ==================== -->
        <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-2xl relative overflow-hidden space-y-4">
          <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
            <div>
              <h2 class="text-sm font-semibold tracking-wider uppercase text-slate-400 flex items-center gap-2">
                <span>📡</span> Принципиальная схема человеческого контура (Схема фонарика)
              </h2>
              <p class="text-xs text-slate-400 mt-0.5">
                Показывает физическое прохождение тока внимания через резистор эго в реальность в точке t = now.
              </p>
            </div>
            <div id="circuitStatusTag" class="px-3 py-1 rounded-full text-xs font-mono font-semibold tracking-wide border bg-emerald-500/15 text-emerald-300 border-emerald-500/30">
              СВЕРХПРОВОДИМОСТЬ • R → 0
            </div>
          </div>

          <!-- SVG Visual Stage -->
          <div class="w-full bg-slate-950/80 rounded-xl border border-slate-800/80 p-4 relative flex items-center justify-center overflow-x-auto">
            <svg id="liveCircuitSvg" viewBox="0 0 940 230" class="w-full max-w-[940px] min-w-[680px] h-auto select-none">
              <defs>
                <radialGradient id="tanden-reactor-glow" cx="50%" cy="50%" r="50%">
                  <stop offset="0%" stop-color="#fbbf24" stop-opacity="1"/>
                  <stop offset="60%" stop-color="#f59e0b" stop-opacity="0.5"/>
                  <stop offset="100%" stop-color="#d97706" stop-opacity="0"/>
                </radialGradient>
                <linearGradient id="wire-flow-cyan" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stop-color="#38bdf8"/>
                  <stop offset="100%" stop-color="#34d399"/>
                </linearGradient>
                <filter id="circuit-glow" x="-20%" y="-20%" width="140%" height="140%">
                  <feGaussianBlur stdDeviation="4" result="blur"/>
                  <feMerge>
                    <feMergeNode in="blur"/>
                    <feMergeNode in="SourceGraphic"/>
                  </feMerge>
                </filter>
              </defs>

              <!-- Return Wire (Bottom Bus) -->
              <path d="M 760 165 L 140 165" stroke="#334155" stroke-width="7" stroke-linecap="round"/>
              <path id="svg-return-flow" d="M 760 165 L 140 165" stroke="#38bdf8" stroke-width="4" stroke-linecap="round" class="flow-reverse opacity-70"/>
              <text x="450" y="185" text-anchor="middle" fill="#64748b" font-size="10" font-family="monospace">ОБРАТНЫЙ ПРОВОД / ЗАЗЕМЛЕНИЕ В СТОПЫ</text>

              <!-- Forward Wire (Attention Bus) -->
              <path d="M 140 65 L 300 65" stroke="#334155" stroke-width="7" stroke-linecap="round"/>
              <path id="svg-wire-1" d="M 140 65 L 300 65" stroke="#38bdf8" stroke-width="4" stroke-linecap="round" class="flow-line"/>

              <path d="M 480 65 L 590 65" stroke="#334155" stroke-width="7" stroke-linecap="round"/>
              <path id="svg-wire-2" d="M 480 65 L 590 65" stroke="#38bdf8" stroke-width="4" stroke-linecap="round" class="flow-line"/>

              <path d="M 680 65 L 760 65" stroke="#334155" stroke-width="7" stroke-linecap="round"/>
              <path id="svg-wire-3" d="M 680 65 L 760 65" stroke="#38bdf8" stroke-width="4" stroke-linecap="round" class="flow-line"/>

              <!-- Vertical Wires -->
              <path d="M 140 165 L 140 65" stroke="#334155" stroke-width="7" stroke-linecap="round"/>
              <path d="M 760 65 L 760 165" stroke="#334155" stroke-width="7" stroke-linecap="round"/>

              <!-- NODE 1: TANDEN REACTOR -->
              <g transform="translate(140, 115)">
                <circle r="36" fill="url(#tanden-reactor-glow)" id="svg-tanden-glow"/>
                <circle r="22" fill="#0f172a" stroke="#f59e0b" stroke-width="3"/>
                <text y="5" text-anchor="middle" fill="#fbbf24" font-size="14" font-weight="bold" font-family="monospace">丹田</text>
                <text y="42" text-anchor="middle" fill="#94a3b8" font-size="10" font-family="monospace">ТАНДЭН (ЭДС)</text>
              </g>

              <!-- NODE 2: PARASITIC EGO RESISTOR -->
              <g transform="translate(300, 38)" id="svg-resistor-group">
                <rect x="0" y="0" width="180" height="54" rx="10" fill="#0f172a" stroke="#10b981" stroke-width="2.5" id="svg-resistor-box"/>
                <text x="90" y="22" text-anchor="middle" fill="#94a3b8" font-size="10" font-family="monospace" font-weight="bold">РЕЗИСТОР ЭГО (R_ego)</text>
                <text x="90" y="42" text-anchor="middle" fill="#38bdf8" font-size="13" font-weight="bold" font-family="monospace" id="svg-resistor-val">0.05 Ω • МУСИН</text>
              </g>

              <!-- NODE 3: ZANSHIN CIRCUIT BREAKER (SWITCH) -->
              <g transform="translate(590, 42)">
                <rect x="0" y="0" width="90" height="46" rx="8" fill="#0f172a" stroke="#0ea5e9" stroke-width="2"/>
                <line x1="16" y1="23" x2="74" y2="23" stroke="#38bdf8" stroke-width="4" stroke-linecap="round" id="svg-switch-bar"/>
                <circle cx="16" cy="23" r="4" fill="#38bdf8"/>
                <circle cx="74" cy="23" r="4" fill="#38bdf8"/>
                <text x="45" y="38" text-anchor="middle" fill="#7dd3fc" font-size="9" font-family="monospace">ДЗАНСИН</text>
              </g>

              <!-- NODE 4: LOAD / FLASHLIGHT BEAM INTO REALITY -->
              <g transform="translate(760, 115)">
                <!-- Emitted Light Cone -->
                <polygon id="svg-light-beam" points="0,-18 140,-50 140,50 0,18" fill="rgba(251, 191, 36, 0.35)" filter="url(#circuit-glow)"/>
                <circle r="30" fill="rgba(251, 191, 36, 0.4)" id="svg-lamp-glow" filter="url(#circuit-glow)"/>
                <circle r="18" fill="#1e293b" stroke="#f59e0b" stroke-width="2.5" id="svg-lamp-circle"/>
                <text y="5" text-anchor="middle" fill="#fbbf24" font-size="13">💡</text>
                <text y="42" text-anchor="middle" fill="#94a3b8" font-size="10" font-family="monospace">ДЕЙСТВИЕ (t=now)</text>
              </g>
            </svg>
          </div>
        </div>

        <!-- ==================== 5 BIOLOGICAL SYSTEMS SLIDERS ==================== -->
        <div class="space-y-4">
          <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-2 px-1">
            <div>
              <h2 class="text-lg md:text-xl font-bold tracking-tight text-slate-100 flex items-center gap-2">
                <span>🎛️</span>
                <span>5 систем человека под зонтиком Закона Проводимости</span>
              </h2>
              <p class="text-xs text-slate-300 mt-0.5">
                Двигайте ползунки, чтобы откалибровать влияние каждой системы на общее сопротивление контура:
              </p>
            </div>
            <span class="text-[11px] font-mono text-slate-300 bg-slate-900 px-3 py-1 rounded-lg border border-slate-800">
              Каждая система вносит 20% веса
            </span>
          </div>

          <!-- Cards Grid -->
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            
            <!-- 1. Вегетативная нервная система (ВНС) -->
            <div class="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 hover:border-slate-700 transition flex flex-col justify-between space-y-4 shadow-xl">
              <div>
                <div class="flex items-center justify-between mb-2">
                  <div class="flex items-center gap-2">
                    <span class="text-xl">🫀</span>
                    <h3 class="text-xs font-bold text-slate-200">1. Вегетативная система</h3>
                  </div>
                  <span id="badge-gauge-ans" class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                    +85 • Вагус
                  </span>
                </div>
                <p class="text-[11px] text-slate-300 mb-3">
                  <strong>Манометр давления:</strong> симпатический овердрайв (зажим сосудов) vs вентральный вагус (свободный проток).
                </p>

                <!-- Slider -->
                <div class="space-y-1">
                  <div class="flex justify-between text-[10px] font-mono text-slate-300">
                    <span class="text-rose-400">Симпатика (-100)</span>
                    <span class="text-emerald-400">Вагус (+100)</span>
                  </div>
                  <input id="slider-gauge-ans" type="range" min="-100" max="100" value="85" oninput="gauge_updateSystem('ans', this.value)" class="w-full accent-emerald-500 cursor-pointer">
                </div>
              </div>

              <div class="p-2.5 rounded-lg bg-slate-950/70 border border-slate-800/80 text-[10px] font-mono text-slate-300 leading-relaxed" id="desc-gauge-ans">
                Вентральный блуждающий нерв активен. Сосуды расширены, пальцы рук и стопы тёплые, сердечный ритм когерентен дыханию.
              </div>
            </div>

            <!-- 2. Эндокринный каскад (Гормоны) -->
            <div class="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 hover:border-slate-700 transition flex flex-col justify-between space-y-4 shadow-xl">
              <div>
                <div class="flex items-center justify-between mb-2">
                  <div class="flex items-center gap-2">
                    <span class="text-xl">🧪</span>
                    <h3 class="text-xs font-bold text-slate-200">2. Эндокринный каскад</h3>
                  </div>
                  <span id="badge-gauge-endo" class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                    +80 • Анаболизм
                  </span>
                </div>
                <p class="text-[11px] text-slate-300 mb-3">
                  <strong>Химический охладитель:</strong> кортизоловый чад перегрева vs окситоцин и анаболическое восстановление.
                </p>

                <!-- Slider -->
                <div class="space-y-1">
                  <div class="flex justify-between text-[10px] font-mono text-slate-300">
                    <span class="text-rose-400">Кортизол (-100)</span>
                    <span class="text-emerald-400">Окситоцин (+100)</span>
                  </div>
                  <input id="slider-gauge-endo" type="range" min="-100" max="100" value="80" oninput="gauge_updateSystem('endo', this.value)" class="w-full accent-emerald-500 cursor-pointer">
                </div>
              </div>

              <div class="p-2.5 rounded-lg bg-slate-950/70 border border-slate-800/80 text-[10px] font-mono text-slate-300 leading-relaxed" id="desc-gauge-endo">
                Ось HPA спокойна. Кортизол на базовом уровне. Высокий анаболизм, синтез нейротрофина BDNF и регенерация тканей.
              </div>
            </div>

            <!-- 3. Нейросети мозга (фМРТ) -->
            <div class="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 hover:border-slate-700 transition flex flex-col justify-between space-y-4 shadow-xl">
              <div>
                <div class="flex items-center justify-between mb-2">
                  <div class="flex items-center gap-2">
                    <span class="text-xl">🧠</span>
                    <h3 class="text-xs font-bold text-slate-200">3. Нейросети мозга</h3>
                  </div>
                  <span id="badge-gauge-brain" class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                    +80 • TPN Поток
                  </span>
                </div>
                <p class="text-[11px] text-slate-300 mb-3">
                  <strong>Вихрь холостого хода:</strong> руминация DMN (самоедство) vs TPN (растворение в реальной задаче).
                </p>

                <!-- Slider -->
                <div class="space-y-1">
                  <div class="flex justify-between text-[10px] font-mono text-slate-300">
                    <span class="text-rose-400">DMN Руминация (-100)</span>
                    <span class="text-emerald-400">TPN Поток (+100)</span>
                  </div>
                  <input id="slider-gauge-brain" type="range" min="-100" max="100" value="80" oninput="gauge_updateSystem('brain', this.value)" class="w-full accent-emerald-500 cursor-pointer">
                </div>
              </div>

              <div class="p-2.5 rounded-lg bg-slate-950/70 border border-slate-800/80 text-[10px] font-mono text-slate-300 leading-relaxed" id="desc-gauge-brain">
                DMN спит. Внутренний критик и страх оценки отключены. Префронтальная кора соединена с созидательным действием.
              </div>
            </div>

            <!-- 4. Вариабельность пульса (HRV) -->
            <div class="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 hover:border-slate-700 transition flex flex-col justify-between space-y-4 shadow-xl">
              <div>
                <div class="flex items-center justify-between mb-2">
                  <div class="flex items-center gap-2">
                    <span class="text-xl">📊</span>
                    <h3 class="text-xs font-bold text-slate-200">4. Вариабельность пульса (HRV)</h3>
                  </div>
                  <span id="badge-gauge-cardio" class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                    +85 • Когерентность
                  </span>
                </div>
                <p class="text-[11px] text-slate-300 mb-3">
                  <strong>Осциллограф контура:</strong> монотонный спазм сердца (стресс) vs гибкая когерентность ритма.
                </p>

                <!-- Slider -->
                <div class="space-y-1">
                  <div class="flex justify-between text-[10px] font-mono text-slate-300">
                    <span class="text-rose-400">Спазм ритма (-100)</span>
                    <span class="text-emerald-400">Когерентность (+100)</span>
                  </div>
                  <input id="slider-gauge-cardio" type="range" min="-100" max="100" value="85" oninput="gauge_updateSystem('cardio', this.value)" class="w-full accent-emerald-500 cursor-pointer">
                </div>
              </div>

              <div class="p-2.5 rounded-lg bg-slate-950/70 border border-slate-800/80 text-[10px] font-mono text-slate-300 leading-relaxed" id="desc-gauge-cardio">
                Высокая вариабельность сердечного ритма. Сердце гибко адаптируется к нагрузке, фазы дыхания синхронизированы.
              </div>
            </div>

            <!-- 5. Соматика и диафрагма (Тандэн) -->
            <div class="p-5 rounded-2xl bg-slate-900/90 border border-slate-800 hover:border-slate-700 transition flex flex-col justify-between space-y-4 shadow-xl">
              <div>
                <div class="flex items-center justify-between mb-2">
                  <div class="flex items-center gap-2">
                    <span class="text-xl">🧘</span>
                    <h3 class="text-xs font-bold text-slate-200">5. Соматика и Тандэн</h3>
                  </div>
                  <span id="badge-gauge-soma" class="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                    +90 • Тандэн
                  </span>
                </div>
                <p class="text-[11px] text-slate-300 mb-3">
                  <strong>Физическая изоляция:</strong> челюстной панцирь Райха vs свободная диафрагма и опущенный центр тяжести.
                </p>

                <!-- Slider -->
                <div class="space-y-1">
                  <div class="flex justify-between text-[10px] font-mono text-slate-300">
                    <span class="text-rose-400">Спазм мышц (-100)</span>
                    <span class="text-emerald-400">Тандэн (+100)</span>
                  </div>
                  <input id="slider-gauge-soma" type="range" min="-100" max="100" value="90" oninput="gauge_updateSystem('soma', this.value)" class="w-full accent-emerald-500 cursor-pointer">
                </div>
              </div>

              <div class="p-2.5 rounded-lg bg-slate-950/70 border border-slate-800/80 text-[10px] font-mono text-slate-300 leading-relaxed" id="desc-gauge-soma">
                Челюсти разомкнуты, плечи опущены, дыхание идёт нижним резервуаром живота. Мышечный панцирь полностью разомкнут.
              </div>
            </div>

            <!-- Formula Summary Card -->
            <div class="p-5 rounded-2xl bg-gradient-to-br from-slate-950 to-slate-900 border border-emerald-500/20 flex flex-col justify-between space-y-3 shadow-xl">
              <div class="space-y-2">
                <div class="text-[11px] font-mono uppercase tracking-widest text-emerald-400 font-bold flex items-center gap-1.5">
                  <span>📐</span>
                  <span>Математический зонтик</span>
                </div>
                <div class="text-[11px] font-mono text-slate-300 space-y-1">
                  <div>CI = 0.20 × (S₁ + S₂ + S₃ + S₄ + S₅)</div>
                  <div>КПД H = (CI + 100) / 2 = <span class="text-amber-300 font-bold" id="gauge-formula-h">92%</span></div>
                  <div>Потери Q = I² · R_ego · t</div>
                </div>
              </div>
              <p class="text-[10px] text-slate-300 leading-relaxed">
                Счастье — это объективный физический режим открытого контура с КПД &gt; 60%. Устраняя затор в любой из 5 систем, вы возвращаете стрелку в зеленую зону.
              </p>
            </div>

          </div>
        </div>

        <!-- Section 3: 30-Second Recovery Protocol -->
        <div class="bg-gradient-to-r from-emerald-950/40 via-slate-900 to-slate-900 border border-emerald-500/30 rounded-2xl p-6 shadow-xl space-y-4">
          <div class="flex items-center gap-3">
            <span class="text-2xl p-2 rounded-xl bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">🛠️</span>
            <div>
              <h3 class="text-base font-bold text-slate-100">30-секундный протокол оператора: Как вернуть стрелку в Зеленую зону</h3>
              <p class="text-xs text-slate-300">Детерминированная процедура сброса омического перегрева цепи</p>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-4 gap-3 text-xs font-mono">
            <div class="p-3.5 rounded-xl bg-slate-950/80 border border-slate-800 space-y-1.5">
              <span class="text-emerald-400 font-bold block">1. ТАНДЭН</span>
              <p class="text-slate-300 text-[11px] leading-relaxed">
                Сбросить внимание из головы в точку на 3 пальца ниже пупка. Сделать медленный удлинённый выдох (вагусный тормоз).
              </p>
            </div>
            <div class="p-3.5 rounded-xl bg-slate-950/80 border border-slate-800 space-y-1.5">
              <span class="text-teal-400 font-bold block">2. ЧЕЛЮСТЬ &amp; ПЛЕЧИ</span>
              <p class="text-slate-300 text-[11px] leading-relaxed">
                Разомкнуть зубы, отпустить плечи вниз. Разомкнуть верхний панцирь напряжения, пустив кровь в конечности.
              </p>
            </div>
            <div class="p-3.5 rounded-xl bg-slate-950/80 border border-slate-800 space-y-1.5">
              <span class="text-cyan-400 font-bold block">3. ОБРЫВ DMN</span>
              <p class="text-slate-300 text-[11px] leading-relaxed">
                Сказать себе: «Я не продавливаю реальность. Ток течёт сам через сверхпроводник». Снять статус подвига.
              </p>
            </div>
            <div class="p-3.5 rounded-xl bg-slate-950/80 border border-slate-800 space-y-1.5">
              <span class="text-amber-400 font-bold block">4. МИКРОДЕЙСТВИЕ</span>
              <p class="text-slate-300 text-[11px] leading-relaxed">
                Зажечь лампу нагрузки в точке t = now: сделать одно маленькое физическое действие (выпить глоток воды, написать 1 строчку).
              </p>
            </div>
          </div>
        </div>

      </div>

      <!-- ============================================================== -->
      <!-- VIEW 2: PAIN-FIRST NAVIGATOR (EMERGENCY AID)                   -->
      <!-- ============================================================== -->
      <div id="view-pains" class="space-y-6 hidden">
        
        <!-- Top Header -->
        <header class="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 backdrop-blur-md shadow-2xl flex flex-col lg:flex-row justify-between items-start lg:items-center gap-5">
          <div>
            <div class="flex items-center gap-3">
              <span class="text-3xl p-2.5 rounded-xl bg-rose-500/15 border border-rose-500/30 text-rose-400">🚨</span>
              <div>
                <div class="flex items-center gap-2">
                  <h1 class="text-2xl md:text-3xl font-bold tracking-tight bg-gradient-to-r from-rose-400 via-amber-400 to-cyan-300 bg-clip-text text-transparent">
                    Навигатор болей человека
                  </h1>
                  <span class="text-xs uppercase tracking-widest px-2.5 py-0.5 bg-rose-500/15 text-rose-300 border border-rose-500/30 rounded-full font-mono font-bold">
                    Pain-First
                  </span>
                </div>
                <p class="text-slate-300 text-sm mt-1">
                  «Всякая система рождается как ответ на боль. Если боли нет — система не нужна».
                </p>
              </div>
            </div>
          </div>

          <!-- Quick Symptom Selector Bar -->
          <div class="flex flex-wrap items-center gap-2">
            <span class="text-xs uppercase tracking-wider text-slate-400 font-mono">Где болит?</span>
            <button onclick="scrollToPainCard('card-pain-01')" class="px-3 py-1.5 rounded-lg text-xs font-medium bg-rose-950/70 border border-rose-700/50 text-rose-300 hover:bg-rose-900/60 transition flex items-center gap-1.5 cursor-pointer">
              <span>🔥</span> 1. Голова кипит
            </button>
            <button onclick="scrollToPainCard('card-pain-02')" class="px-3 py-1.5 rounded-lg text-xs font-medium bg-purple-950/70 border border-purple-700/50 text-purple-300 hover:bg-purple-900/60 transition flex items-center gap-1.5 cursor-pointer">
              <span>🪤</span> 2. Самозванец
            </button>
            <button onclick="scrollToPainCard('card-pain-03')" class="px-3 py-1.5 rounded-lg text-xs font-medium bg-amber-950/70 border border-amber-700/50 text-amber-300 hover:bg-amber-900/60 transition flex items-center gap-1.5 cursor-pointer">
              <span>🏺</span> 3. Крах проекта
            </button>
            <button onclick="scrollToPainCard('card-pain-04')" class="px-3 py-1.5 rounded-lg text-xs font-medium bg-indigo-950/70 border border-indigo-700/50 text-indigo-300 hover:bg-indigo-900/60 transition flex items-center gap-1.5 cursor-pointer">
              <span>🧘</span> 4. Апатия и лень
            </button>
            <button onclick="scrollToPainCard('card-pain-05')" class="px-3 py-1.5 rounded-lg text-xs font-medium bg-cyan-950/70 border border-cyan-700/50 text-cyan-300 hover:bg-cyan-900/60 transition flex items-center gap-1.5 cursor-pointer">
              <span>⚖️</span> 5. Разрываюсь
            </button>
          </div>
        </header>

        <!-- Core Insight Callout Box -->
        <div class="p-6 rounded-2xl bg-gradient-to-r from-rose-950/40 via-slate-900 to-slate-950 border border-rose-500/30 shadow-xl relative overflow-hidden">
          <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-5">
            <div class="space-y-2 max-w-3xl">
              <div class="flex items-center gap-2 text-xs font-mono uppercase tracking-widest text-rose-400 font-bold">
                <span>⚡</span> Инженерная природа человеческого несчастья
              </div>
              <p class="text-sm text-slate-200 leading-relaxed">
                Человек несчастлив не вообще и не по воле рока. Он страдает от <strong>вполне определённых физических сбоев электродинамической цепи</strong>. Система «Inner Current» переводит душевную муку в локализованную аварию проводки внимания и даёт <strong>немедленный детерминированный протокол исцеления</strong>.
              </p>
            </div>
            <div class="shrink-0 p-4 rounded-xl bg-slate-950 border border-slate-800 text-center font-mono">
              <div class="text-[10px] uppercase text-slate-400">Формула нормы</div>
              <div class="text-base font-bold text-cyan-400">R → 0 &amp; I &gt; 0</div>
              <div class="text-[10px] text-emerald-400 font-bold">Сверхпроводимость</div>
            </div>
          </div>
        </div>

        <!-- Live Healing Protocol HUD Banner -->
        <div id="liveHealingBanner" class="hidden bg-slate-900/95 border border-emerald-500/50 shadow-2xl backdrop-blur-md rounded-2xl p-5 md:p-6 space-y-4 transition-all duration-300 relative overflow-hidden">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-800">
            <div class="flex items-center gap-3">
              <div id="liveHealingIcon" class="w-10 h-10 rounded-xl bg-emerald-500/20 border border-emerald-500/40 flex items-center justify-center text-xl shrink-0 text-emerald-400">
                ⚡
              </div>
              <div>
                <div class="flex items-center gap-2">
                  <h3 class="font-bold text-emerald-300 text-sm md:text-base tracking-wide" id="liveHealingTitle">
                    Протокол «Мусин» запущен: Сброс R → 0
                  </h3>
                </div>
                <div class="text-xs text-slate-300 mt-0.5" id="liveHealingDesc">
                  Отсекаем симуляции прошлого и будущего. Внимание заземлено в рецепторы стоп и дыхание низом живота.
                </div>
              </div>
            </div>
            <button onclick="closeLiveHealingBanner()" class="text-slate-400 hover:text-white p-1 text-sm self-end sm:self-center">✕</button>
          </div>

          <!-- Progress Bar -->
          <div class="space-y-1.5">
            <div class="flex justify-between text-xs font-mono">
              <span id="liveHealingStatusText" class="text-emerald-400 font-bold">ФАЗА 1/3: СОМАТИЧЕСКИЙ СБРОС</span>
              <span id="liveHealingProgressPercent" class="text-cyan-300 font-bold">25%</span>
            </div>
            <div class="w-full bg-slate-950 rounded-full h-2.5 overflow-hidden border border-slate-800">
              <div id="liveHealingProgressBar" class="h-full bg-gradient-to-r from-emerald-500 to-cyan-400 transition-all duration-500" style="width: 25%;"></div>
            </div>
          </div>

          <div id="liveHealingSomaticCue" class="p-3 rounded-xl bg-emerald-950/40 border border-emerald-500/30 text-xs font-mono text-emerald-200">
            🌬️ Медленный выдох через рот на 6 счетов. Челюсть разомкнута, плечи свободно опущены.
          </div>

          <div id="liveHealingPostActions" class="hidden pt-2 flex flex-wrap gap-2">
            <button onclick="switchTab('speedometer')" class="px-4 py-2 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs transition">
              🎯 Посмотреть стрелку на Спидометре ↗
            </button>
          </div>
        </div>

        <!-- 5 Master Pain Cards Grid -->
        <div class="space-y-5">
          
          <!-- Card 1: Burnout -->
          <div id="card-pain-01" class="bg-slate-900/90 border border-rose-500/40 rounded-2xl p-6 shadow-xl space-y-4">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
              <div class="flex items-center gap-3">
                <span class="text-2xl p-2 rounded-xl bg-rose-500/20 text-rose-400">🔥</span>
                <div>
                  <h2 class="text-lg font-bold text-slate-100">1. «Голова кипит, челюсти сжаты, я выгораю»</h2>
                  <p class="text-xs text-rose-300 font-mono">Омический перегрев цепи • Закон Джоуля — Ленца: Q = I² · R · t</p>
                </div>
              </div>
              <button onclick="executePainRemediation('burnout')" class="px-4 py-2 rounded-xl bg-rose-500 hover:bg-rose-400 text-slate-950 font-bold text-xs transition cursor-pointer shadow-lg shadow-rose-500/20">
                Запустить протокол «Мусин» ⚡
              </button>
            </div>
            <p class="text-xs text-slate-300 leading-relaxed">
              <strong>Физика сбоя:</strong> Вы пытаетесь продавить реальность волевым усилием (I) при высоком сопротивлении эго (R_ego). Вся энергия уходит не в полезную нагрузку, а в тепловой нагрев черепной коробки. Проводка плавится.
            </p>
            <div class="p-3 rounded-xl bg-slate-950/80 border border-slate-800 text-xs font-mono text-slate-300 space-y-1">
              <div class="text-rose-400 font-bold">СОМАТИЧЕСКИЙ РЕЦЕПТ:</div>
              <div>1. Разомкнуть зубы, сделать медленный выдох через рот в Тандэн на 6 счетов.</div>
              <div>2. Снять установку «Я совершаю подвиг» ⟶ перейти в «Я просто сверхпроводник».</div>
              <div>3. Переключить спидометр в режим Мусин (+95).</div>
            </div>
          </div>

          <!-- Card 2: Imposter Syndrome -->
          <div id="card-pain-02" class="bg-slate-900/90 border border-purple-500/40 rounded-2xl p-6 shadow-xl space-y-4">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
              <div class="flex items-center gap-3">
                <span class="text-2xl p-2 rounded-xl bg-purple-500/20 text-purple-400">🪤</span>
                <div>
                  <h2 class="text-lg font-bold text-slate-100">2. «Я самозванец, боюсь оценки и осуждения»</h2>
                  <p class="text-xs text-purple-300 font-mono">Паразитный шунт на внешнюю оценку • Короткое замыкание на Эго</p>
                </div>
              </div>
              <button onclick="executePainRemediation('imposter')" class="px-4 py-2 rounded-xl bg-purple-500 hover:bg-purple-400 text-slate-950 font-bold text-xs transition cursor-pointer shadow-lg shadow-purple-500/20">
                Запустить протокол «Нидзиригути» ⚡
              </button>
            </div>
            <p class="text-xs text-slate-300 leading-relaxed">
              <strong>Физика сбоя:</strong> Цепь закольцована на саму себя: вместо подачи тока в реальный продукт вы тратите 100% мощности на симуляцию «что обо мне подумают другие». Ток нагрузки I_load = 0.
            </p>
            <div class="p-3 rounded-xl bg-slate-950/80 border border-slate-800 text-xs font-mono text-slate-300 space-y-1">
              <div class="text-purple-400 font-bold">СОМАТИЧЕСКИЙ РЕЦЕПТ:</div>
              <div>1. Протокол чайного домика (Нидзиригути): оставить меч статуса и эго снаружи.</div>
              <div>2. Закон вольтметра: прибор не обижается на 110 Вольт, он просто замеряет контакт.</div>
              <div>3. Направить луч фонарика на пользу человеку, а не на защиту своего образа.</div>
            </div>
          </div>

          <!-- Card 3: Project Crash -->
          <div id="card-pain-03" class="bg-slate-900/90 border border-amber-500/40 rounded-2xl p-6 shadow-xl space-y-4">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
              <div class="flex items-center gap-3">
                <span class="text-2xl p-2 rounded-xl bg-amber-500/20 text-amber-400">🏺</span>
                <div>
                  <h2 class="text-lg font-bold text-slate-100">3. «Проект рухнул, мир рушится, я уничтожен»</h2>
                  <p class="text-xs text-amber-300 font-mono">Авария внешней нагрузки • Изоляция Тандэна через Дзансин &amp; Кинцуги</p>
                </div>
              </div>
              <button onclick="executePainRemediation('kintsugi')" class="px-4 py-2 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs transition cursor-pointer shadow-lg shadow-amber-500/20">
                Запустить протокол «Кинцуги» ⚡
              </button>
            </div>
            <p class="text-xs text-slate-300 leading-relaxed">
              <strong>Физика сбоя:</strong> Лампочка снаружи взорвалась, но оператор ошибочно посчитал, что сгорел сам генератор. Разомкните автомат защиты Дзансин: проект умер, но реактор Тандэна цел и автономен.
            </p>
            <div class="p-3 rounded-xl bg-slate-950/80 border border-slate-800 text-xs font-mono text-slate-300 space-y-1">
              <div class="text-amber-400 font-bold">СОМАТИЧЕСКИЙ РЕЦЕПТ:</div>
              <div>1. Сработал автомат защиты: генератор цел. Проект — лишь внешняя сменная лампа.</div>
              <div>2. Золотой шов Кинцуги: шрам ошибки склеивается золотой смолой осознанности.</div>
              <div>3. Пауза 10 секунд в полном покое. Батарея готова к подключению новой нагрузки.</div>
            </div>
          </div>

          <!-- Card 4: Apathy -->
          <div id="card-pain-04" class="bg-slate-900/90 border border-indigo-500/40 rounded-2xl p-6 shadow-xl space-y-4">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
              <div class="flex items-center gap-3">
                <span class="text-2xl p-2 rounded-xl bg-indigo-500/20 text-indigo-400">🧘</span>
                <div>
                  <h2 class="text-lg font-bold text-slate-100">4. «Апатия, лень, ничего не хочу, нет сил»</h2>
                  <p class="text-xs text-indigo-300 font-mono">Обрыв цепи • Холостой ход • Застой нерастраченной ЭДС</p>
                </div>
              </div>
              <button onclick="executePainRemediation('apathy')" class="px-4 py-2 rounded-xl bg-indigo-500 hover:bg-indigo-400 text-slate-950 font-bold text-xs transition cursor-pointer shadow-lg shadow-indigo-500/20">
                Запустить протокол «Микронагрузка 10W» ⚡
              </button>
            </div>
            <p class="text-xs text-slate-300 leading-relaxed">
              <strong>Физика сбоя:</strong> Ключ нагрузки разомкнут. Энергия не течёт, потому что планка задачи задрана слишком высоко («построить империю»). Нерастраченный потенциал вызывает соматический застой.
            </p>
            <div class="p-3 rounded-xl bg-slate-950/80 border border-slate-800 text-xs font-mono text-slate-300 space-y-1">
              <div class="text-indigo-400 font-bold">СОМАТИЧЕСКИЙ РЕЦЕПТ:</div>
              <div>1. Включить микронагрузку 10 Вт: помыть чашку, заварить чай, сделать 10 приседаний.</div>
              <div>2. Как только ток пошёл через физический объект, цепь замкнута — силы возвращаются мгновенно.</div>
            </div>
          </div>

          <!-- Card 5: Scattered focus -->
          <div id="card-pain-05" class="bg-slate-900/90 border border-cyan-500/40 rounded-2xl p-6 shadow-xl space-y-4">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
              <div class="flex items-center gap-3">
                <span class="text-2xl p-2 rounded-xl bg-cyan-500/20 text-cyan-400">⚖️</span>
                <div>
                  <h2 class="text-lg font-bold text-slate-100">5. «Разрываюсь между делами, расфокус, тело сыплется»</h2>
                  <p class="text-xs text-cyan-300 font-mono">Мультиплексирование внимания • Просадка напряжения сети</p>
                </div>
              </div>
              <button onclick="executePainRemediation('scattered')" class="px-4 py-2 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs transition cursor-pointer shadow-lg shadow-cyan-500/20">
                Запустить протокол «Кансо» ⚡
              </button>
            </div>
            <p class="text-xs text-slate-300 leading-relaxed">
              <strong>Физика сбоя:</strong> Вы пытаетесь одновременно запитать 10 параллельных ламп при ограниченной мощности генератора. Напряжение на всех приборах падает до 50 Вольт, ни одна лампа не светит, тело обесточено.
            </p>
            <div class="p-3 rounded-xl bg-slate-950/80 border border-slate-800 text-xs font-mono text-slate-300 space-y-1">
              <div class="text-cyan-400 font-bold">СОМАТИЧЕСКИЙ РЕЦЕПТ:</div>
              <div>1. Канон Кансо: безжалостно обесточить все второстепенные приборы.</div>
              <div>2. Подать 30 Вт в скафандр: сон, тёплая еда, прогулка на воздухе без телефона.</div>
              <div>3. Только 1 фокус луча в один момент времени.</div>
            </div>
          </div>

        </div>

      </div>

      <!-- ============================================================== -->
      <!-- VIEW 3: LABORATORY & LAWS OF SUPERCONDUCTIVITY                 -->
      <!-- ============================================================== -->
      <div id="view-lab" class="space-y-6 hidden">
        
        <!-- Header -->
        <header class="bg-slate-900/90 border border-amber-500/30 rounded-2xl p-6 backdrop-blur-md shadow-2xl flex flex-col lg:flex-row justify-between items-start lg:items-center gap-5">
          <div class="flex items-center gap-3">
            <span class="text-3xl p-2.5 rounded-xl bg-amber-500/20 border border-amber-500/40 text-amber-300">⚡</span>
            <div>
              <h1 class="text-2xl md:text-3xl font-bold tracking-tight bg-gradient-to-r from-amber-300 via-yellow-200 to-cyan-300 bg-clip-text text-transparent">
                Лаборатория сверхпроводимости
              </h1>
              <p class="text-slate-300 text-sm mt-1">
                Фундаментальные законы цепи, формула Джоуля — Ленца и Канон Десяти быков дзэн.
              </p>
            </div>
          </div>
          <button onclick="switchTab('speedometer')" class="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold text-xs border border-slate-700 transition">
            🎯 Вернуться к Спидометру
          </button>
        </header>

        <!-- The 4 Nodes Fractal Callout -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div class="p-5 rounded-2xl bg-slate-900/90 border border-amber-500/30 space-y-2">
            <div class="text-amber-400 font-bold font-mono text-sm flex items-center gap-1.5">
              <span>1. 丹田</span> ТАНДЭН
            </div>
            <p class="text-xs text-slate-300 leading-relaxed">
              <strong>Ядро-Реактор:</strong> Неделимый центр силы и баланса внизу живота. Ток течёт из Тандэна в мир, но никогда обратно. Запрет паразитной подзарядки от внешних похвал.
            </p>
          </div>
          <div class="p-5 rounded-2xl bg-slate-900/90 border border-cyan-500/30 space-y-2">
            <div class="text-cyan-400 font-bold font-mono text-sm flex items-center gap-1.5">
              <span>2. 無心</span> МУСИН
            </div>
            <p class="text-xs text-slate-300 leading-relaxed">
              <strong>Сверхпроводник:</strong> Чистое сознание без формы. Сопротивление эго сведено к нулю (R_ego → 0). Нет самоедства, нет трения, энергия беспрепятственно выходит в мир.
            </p>
          </div>
          <div class="p-5 rounded-2xl bg-slate-900/90 border border-emerald-500/30 space-y-2">
            <div class="text-emerald-400 font-bold font-mono text-sm flex items-center gap-1.5">
              <span>3. 💡</span> НАГРУЗКА
            </div>
            <p class="text-xs text-slate-300 leading-relaxed">
              <strong>Свет фонарика:</strong> Фокус луча на физическом объекте в точке t = now. Вещи сами по себе пусты (E_load ≡ 0), свет рождается от вашего свободного тока.
            </p>
          </div>
          <div class="p-5 rounded-2xl bg-slate-900/90 border border-sky-500/30 space-y-2">
            <div class="text-sky-400 font-bold font-mono text-sm flex items-center gap-1.5">
              <span>4. 残心</span> ДЗАНСИН
            </div>
            <p class="text-xs text-slate-300 leading-relaxed">
              <strong>Предохранитель:</strong> Непоколебимое сохранение духа после выстрела. Автомат защиты от короткого замыкания: проект может разбиться, но реактор мастера цел.
            </p>
          </div>
        </div>

        <!-- Master Formula Card -->
        <div class="p-6 rounded-2xl bg-gradient-to-r from-amber-950/40 via-slate-900 to-cyan-950/40 border border-amber-500/30 space-y-4">
          <div class="flex items-center justify-between flex-wrap gap-2">
            <div class="text-xs font-mono uppercase tracking-widest text-amber-400 font-bold">
              Физический инвариант счастья
            </div>
            <span class="text-xs font-mono px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/40 font-bold">
              R → 0 &amp; I &gt; 0
            </span>
          </div>
          <p class="text-sm text-slate-200 leading-relaxed">
            В Системе Аньянова счастье — это не настроение и не каприз фортуны. <strong>Счастье — это субъективное переживание режима нулевого сопротивления цепи при созидательном действии.</strong>
          </p>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-3 font-mono text-xs">
            <div class="p-3 rounded-xl bg-slate-950 border border-slate-800">
              <span class="text-slate-400 block mb-1">Закон Джоуля — Ленца:</span>
              <span class="text-rose-400 font-bold text-sm">Q = I² · R_ego · t</span>
              <p class="text-[10px] text-slate-300 mt-1">Омический перегрев пропорционален квадрату волевого давления на эго-сопротивление.</p>
            </div>
            <div class="p-3 rounded-xl bg-slate-950 border border-slate-800">
              <span class="text-slate-400 block mb-1">Сверхпроводимость:</span>
              <span class="text-emerald-400 font-bold text-sm">R_ego = 0 ⟹ Q = 0</span>
              <p class="text-[10px] text-slate-300 mt-1">Когда эго не цепляется за плоды, 100% энергии идёт в созидание без выгорания.</p>
            </div>
            <div class="p-3 rounded-xl bg-slate-950 border border-slate-800">
              <span class="text-slate-400 block mb-1">Закон фонарика:</span>
              <span class="text-cyan-400 font-bold text-sm">Φ = I · S_now</span>
              <p class="text-[10px] text-slate-300 mt-1">Смысл — это не далёкая цель на горизонте, а свет луча прямо под ногами.</p>
            </div>
          </div>
        </div>

        <!-- 10 Bulls of Zen Canon -->
        <div class="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-sm font-bold text-slate-200 flex items-center gap-2">
              <span>🐂</span>
              <span>Канон Десяти быков дзэн (十牛) — Шкала проводимости оператора</span>
            </h3>
            <span class="text-[10px] font-mono text-cyan-300 bg-cyan-950 px-2 py-0.5 rounded border border-cyan-800">
              От DMN к сверхпроводимости
            </span>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3 text-xs font-mono">
            <div class="p-3 rounded-xl bg-slate-950/70 border border-slate-800 space-y-1">
              <span class="text-slate-400 font-bold">1. Поиски быка</span>
              <p class="text-[11px] text-slate-300">Тотальный расфокус DMN, человек потерян в руминации.</p>
            </div>
            <div class="p-3 rounded-xl bg-slate-950/70 border border-slate-800 space-y-1">
              <span class="text-slate-400 font-bold">2. Обнаружение следов</span>
              <p class="text-[11px] text-slate-300">Первое понимание: причина страданий — в собственном сопротивлении эго.</p>
            </div>
            <div class="p-3 rounded-xl bg-slate-950/70 border border-slate-800 space-y-1">
              <span class="text-slate-400 font-bold">3. Видение быка</span>
              <p class="text-[11px] text-slate-300">Взгляд на внутренний критик со стороны через дыхание в Тандэн.</p>
            </div>
            <div class="p-3 rounded-xl bg-slate-950/70 border border-slate-800 space-y-1">
              <span class="text-slate-400 font-bold">4. Поимка быка</span>
              <p class="text-[11px] text-slate-300">Обуздание мышечного панциря Райха, расслабление челюстей.</p>
            </div>
            <div class="p-3 rounded-xl bg-slate-950/70 border border-slate-800 space-y-1">
              <span class="text-slate-400 font-bold">5. Укрощение быка</span>
              <p class="text-[11px] text-slate-300">Стрелка спидометра уверенно держится в районе 0...+50.</p>
            </div>
            <div class="p-3 rounded-xl bg-slate-950/70 border border-slate-800 space-y-1">
              <span class="text-emerald-400 font-bold">6. Езда на быке домой</span>
              <p class="text-[11px] text-slate-300">Усилие исчезает, ток начинает течь сам собой через проводник.</p>
            </div>
            <div class="p-3 rounded-xl bg-slate-950/70 border border-slate-800 space-y-1">
              <span class="text-emerald-400 font-bold">7. Бык забыт, человек один</span>
              <p class="text-[11px] text-slate-300">Техники и правила растворяются, остаётся естественная проводимость.</p>
            </div>
            <div class="p-3 rounded-xl bg-slate-950/70 border border-slate-800 space-y-1">
              <span class="text-cyan-400 font-bold">8. И бык, и человек забыты</span>
              <p class="text-[11px] text-slate-300">Полный Мусин (R = 0, CI = +100). Чистая пустота Шуньяты.</p>
            </div>
            <div class="p-3 rounded-xl bg-slate-950/70 border border-slate-800 space-y-1">
              <span class="text-cyan-400 font-bold">9. Возврат к истоку</span>
              <p class="text-[11px] text-slate-300">Река течёт, горы стоят. Мир воспринимается без фильтра концепций.</p>
            </div>
            <div class="p-3 rounded-xl bg-slate-950/70 border border-amber-400/50 space-y-1 bg-amber-950/20">
              <span class="text-amber-300 font-bold">10. Вход на базар</span>
              <p class="text-[11px] text-slate-300">Свободное действие в социуме с дарящими руками. Полный цикл замкнут.</p>
            </div>
          </div>
        </div>

      </div>

    </main>

  </div>

  <!-- ============================================================== -->
  <!-- 🎯 CORE INTERACTIVE SCRIPTS                                     -->
  <!-- ============================================================== -->
  <script>
    // -------------------------------------------------------------
    // Tab Router
    // -------------------------------------------------------------
    function switchTab(tabId) {
      const viewSpeedometer = document.getElementById('view-speedometer');
      const viewPains = document.getElementById('view-pains');
      const viewLab = document.getElementById('view-lab');

      const navSpeedometer = document.getElementById('nav-tab-speedometer');
      const navPains = document.getElementById('nav-tab-pains');
      const navLab = document.getElementById('nav-tab-lab');

      const activeBadge = document.getElementById('sidebarActiveBadge');
      const modeDesc = document.getElementById('sidebarModeDesc');

      // Hide all
      [viewSpeedometer, viewPains, viewLab].forEach(v => {
        if (v) v.classList.add('hidden');
      });

      // Reset nav classes
      const inactiveClass = 'bg-slate-950/40 border-slate-800 hover:border-slate-700';
      [navSpeedometer, navPains, navLab].forEach(btn => {
        if (btn) {
          btn.className = 'w-full text-left p-3 rounded-xl border transition-all duration-200 flex items-center gap-3 group relative overflow-hidden ' + inactiveClass + ' cursor-pointer';
        }
      });

      if (tabId === 'pains') {
        if (viewPains) viewPains.classList.remove('hidden');
        if (navPains) navPains.className = 'w-full text-left p-3 rounded-xl border transition-all duration-200 flex items-center gap-3 group relative overflow-hidden bg-gradient-to-r from-rose-500/15 via-slate-900 to-slate-900 border-rose-500/40 cursor-pointer shadow-lg shadow-rose-500/10';
        if (activeBadge) {
          activeBadge.textContent = 'Аптечка';
          activeBadge.className = 'px-1.5 py-0.5 rounded text-[9px] font-bold bg-rose-500/20 text-rose-300 border border-rose-500/30';
        }
        if (modeDesc) modeDesc.textContent = 'Экспресс-диагностика и устранение 5 болей';
      } else if (tabId === 'lab') {
        if (viewLab) viewLab.classList.remove('hidden');
        if (navLab) navLab.className = 'w-full text-left p-3 rounded-xl border transition-all duration-200 flex items-center gap-3 group relative overflow-hidden bg-gradient-to-r from-cyan-500/15 via-slate-900 to-slate-900 border-cyan-500/40 cursor-pointer shadow-lg shadow-cyan-500/10';
        if (activeBadge) {
          activeBadge.textContent = 'Лаборатория';
          activeBadge.className = 'px-1.5 py-0.5 rounded text-[9px] font-bold bg-cyan-500/20 text-cyan-300 border border-cyan-500/30';
        }
        if (modeDesc) modeDesc.textContent = 'Законы электродинамики и Десять быков дзэн';
      } else {
        // speedometer default
        if (viewSpeedometer) viewSpeedometer.classList.remove('hidden');
        if (navSpeedometer) navSpeedometer.className = 'w-full text-left p-3 rounded-xl border transition-all duration-200 flex items-center gap-3 group relative overflow-hidden bg-gradient-to-r from-emerald-500/15 via-slate-900 to-slate-900 border-emerald-500/40 cursor-pointer shadow-lg shadow-emerald-500/10';
        if (activeBadge) {
          activeBadge.textContent = 'Спидометр';
          activeBadge.className = 'px-1.5 py-0.5 rounded text-[9px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/30';
        }
        if (modeDesc) modeDesc.textContent = 'Калибровка внутреннего сопротивления R_ego';
      }

      try {
        localStorage.setItem('inner_current_active_tab', tabId);
      } catch (e) {}

      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // Keyboard Shortcuts: 1 (Speedometer), 2 (Pains), 3 (Lab)
    window.addEventListener('keydown', (e) => {
      if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) return;
      if (e.key === '1') switchTab('speedometer');
      if (e.key === '2') switchTab('pains');
      if (e.key === '3') switchTab('lab');
    });

    // -------------------------------------------------------------
    // Speedometer & 5 Biological Systems Engine
    // -------------------------------------------------------------
    const gaugeState = {
      ans: 85,
      endo: 80,
      brain: 80,
      cardio: 85,
      soma: 90
    };

    function gauge_updateSystem(sys, val) {
      gaugeState[sys] = parseInt(val, 10);
      gauge_render();
    }

    function gauge_applyPreset(presetName) {
      if (presetName === 'mushin') {
        gaugeState.ans = 95; gaugeState.endo = 90; gaugeState.brain = 95; gaugeState.cardio = 95; gaugeState.soma = 100;
      } else if (presetName === 'flow') {
        gaugeState.ans = 75; gaugeState.endo = 70; gaugeState.brain = 85; gaugeState.cardio = 75; gaugeState.soma = 75;
      } else if (presetName === 'npc') {
        gaugeState.ans = 0; gaugeState.endo = 0; gaugeState.brain = -10; gaugeState.cardio = 5; gaugeState.soma = 0;
      } else if (presetName === 'rumination') {
        gaugeState.ans = -40; gaugeState.endo = -50; gaugeState.brain = -90; gaugeState.cardio = -45; gaugeState.soma = -30;
      } else if (presetName === 'panic') {
        gaugeState.ans = -95; gaugeState.endo = -90; gaugeState.brain = -85; gaugeState.cardio = -95; gaugeState.soma = -90;
      }

      ['ans', 'endo', 'brain', 'cardio', 'soma'].forEach(sys => {
        const slider = document.getElementById('slider-gauge-' + sys);
        if (slider) slider.value = gaugeState[sys];
      });

      gauge_render();
      playZenChime(640);
    }

    function gauge_calibrateMushin() {
      gauge_applyPreset('mushin');
    }

    function gauge_renderSystemBadgeAndDesc(sys, val) {
      const badge = document.getElementById('badge-gauge-' + sys);
      const desc = document.getElementById('desc-gauge-' + sys);
      if (!badge || !desc) return;

      const sign = val > 0 ? '+' : '';
      let colorClass = '';
      let text = '';
      let descText = '';

      if (val >= 20) {
        colorClass = 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30';
      } else if (val >= -30) {
        colorClass = 'bg-amber-500/20 text-amber-300 border-amber-500/30';
      } else {
        colorClass = 'bg-rose-500/20 text-rose-300 border-rose-500/30';
      }

      if (sys === 'ans') {
        if (val >= 20) {
          text = sign + val + ' • Вагус';
          descText = 'Вентральный блуждающий нерв активен. Сосуды расширены, пальцы рук и стопы тёплые, сердечный ритм когерентен дыханию.';
        } else if (val >= -30) {
          text = sign + val + ' • Баланс';
          descText = 'Промежуточный тонус ВНС. Симпатика и парасимпатика в нейтральном равновесии без выраженной когерентности.';
        } else {
          text = val + ' • Симпатика';
          descText = 'Симпатический овердрайв (fight-or-flight). Выброс адреналина, спазм сосудов, холодные конечности.';
        }
      } else if (sys === 'endo') {
        if (val >= 20) {
          text = sign + val + ' • Анаболизм';
          descText = 'Ось HPA спокойна. Кортизол на базовом уровне. Высокий анаболизм, синтез BDNF и регенерация тканей.';
        } else if (val >= -30) {
          text = sign + val + ' • Фон';
          descText = 'Умеренный гормональный фон. Кортизол компенсируется базовым метаболизмом.';
        } else {
          text = val + ' • Кортизол';
          descText = 'Активация оси HPA. Острый избыток кортизола, катаболизм, омическое выгорание клеток.';
        }
      } else if (sys === 'brain') {
        if (val >= 20) {
          text = sign + val + ' • TPN Поток';
          descText = 'DMN спит. Внутренний критик и страх оценки отключены. Префронтальная кора соединена с созидательным действием.';
        } else if (val >= -30) {
          text = sign + val + ' • Дрейф';
          descText = 'Смешанный режим. Внимание периодически ускользает в мысли о прошлом и будущем.';
        } else {
          text = val + ' • DMN Жвачка';
          descText = 'Гиперактивность DMN (Default Mode Network). Руминация, страх оценки, самоедство, паралич действия.';
        }
      } else if (sys === 'cardio') {
        if (val >= 20) {
          text = sign + val + ' • Когерентность';
          descText = 'Высокая вариабельность ритма (HRV). Сердце гибко адаптируется к нагрузке, фазы дыхания синхронизированы.';
        } else if (val >= -30) {
          text = sign + val + ' • Норма';
          descText = 'Средняя вариабельность ритма. Базовая гемодинамика без выраженного кардиовагусного резонанса.';
        } else {
          text = val + ' • Спазм ритма';
          descText = 'Низкая вариабельность ритма (HRV). Монотонный тахикардический ритм хронического стресса.';
        }
      } else if (sys === 'soma') {
        if (val >= 20) {
          text = sign + val + ' • Тандэн';
          descText = 'Челюсти разомкнуты, плечи опущены, дыхание идёт нижним резервуаром живота. Мышечный панцирь разомкнут.';
        } else if (val >= -30) {
          text = sign + val + ' • Тонус';
          descText = 'Привычный фоновый мышечный тонус без острого напряжения.';
        } else {
          text = val + ' • Спазм мышц';
          descText = 'Хронический спазм (челюсти, шея, диафрагма — мышечный панцирь Райха). Грудное дыхание.';
        }
      }

      badge.textContent = text;
      badge.className = 'px-2 py-0.5 rounded text-[10px] font-mono font-bold border ' + colorClass;
      desc.textContent = descText;
    }

    let currentGaugeAngle = null;
    let gaugeAnimFrame = null;

    function updateNeedleGeometry(angleDeg) {
      const rad = (angleDeg * Math.PI) / 180;
      const s = Math.sin(rad);
      const c = Math.cos(rad);
      const cx = 150;
      const cy = 140;

      const arcX = cx + 100 * s;
      const arcY = cy - 100 * c;
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

      const beam = document.getElementById('gauge-needle-beam');
      if (beam) {
        beam.setAttribute('points', b1X.toFixed(1) + ',' + b1Y.toFixed(1) + ' ' + b2X.toFixed(1) + ',' + b2Y.toFixed(1) + ' ' + t2X.toFixed(1) + ',' + t2Y.toFixed(1) + ' ' + t1X.toFixed(1) + ',' + t1Y.toFixed(1));
      }
      const spine = document.getElementById('gauge-needle-spine');
      if (spine) {
        spine.setAttribute('x1', cx);
        spine.setAttribute('y1', cy);
        spine.setAttribute('x2', tipX.toFixed(1));
        spine.setAttribute('y2', tipY.toFixed(1));
      }
      const counter = document.getElementById('gauge-needle-counter');
      if (counter) {
        counter.setAttribute('points', b1X.toFixed(1) + ',' + b1Y.toFixed(1) + ' ' + b2X.toFixed(1) + ',' + b2Y.toFixed(1) + ' ' + countX.toFixed(1) + ',' + countY.toFixed(1));
      }

      const tipGlow = document.getElementById('gauge-needle-tip-glow');
      const tipCore = document.getElementById('gauge-needle-tip-core');
      if (tipGlow) { tipGlow.setAttribute('cx', tipX.toFixed(1)); tipGlow.setAttribute('cy', tipY.toFixed(1)); }
      if (tipCore) { tipCore.setAttribute('cx', tipX.toFixed(1)); tipCore.setAttribute('cy', tipY.toFixed(1)); }

      const lensOuter = document.getElementById('gauge-needle-lens-outer');
      const lensRing = document.getElementById('gauge-needle-lens-ring');
      const lensDot = document.getElementById('gauge-needle-lens-dot');
      const lensGlint = document.getElementById('gauge-needle-lens-glint');
      if (lensOuter) { lensOuter.setAttribute('cx', arcX.toFixed(1)); lensOuter.setAttribute('cy', arcY.toFixed(1)); }
      if (lensRing) { lensRing.setAttribute('cx', arcX.toFixed(1)); lensRing.setAttribute('cy', arcY.toFixed(1)); }
      if (lensDot) { lensDot.setAttribute('cx', arcX.toFixed(1)); lensDot.setAttribute('cy', arcY.toFixed(1)); }
      if (lensGlint) { lensGlint.setAttribute('cx', arcX.toFixed(1)); lensGlint.setAttribute('cy', arcY.toFixed(1)); }
    }

    function gauge_render() {
      const ci = Math.round(0.20 * (gaugeState.ans + gaugeState.endo + gaugeState.brain + gaugeState.cardio + gaugeState.soma));
      const h = Math.round((ci + 100) / 2);

      // Angle: -100 -> -90 deg, 0 -> 0 deg, +100 -> +90 deg
      const targetAngle = (ci / 100) * 90;

      if (currentGaugeAngle === null) {
        currentGaugeAngle = targetAngle;
        updateNeedleGeometry(targetAngle);
      } else {
        if (gaugeAnimFrame) cancelAnimationFrame(gaugeAnimFrame);
        const startAngle = currentGaugeAngle;
        const startTime = performance.now();
        const duration = 240;

        function animStep(now) {
          const elapsed = now - startTime;
          const progress = Math.min(elapsed / duration, 1);
          const ease = 1 - Math.pow(1 - progress, 3);
          const current = startAngle + (targetAngle - startAngle) * ease;
          currentGaugeAngle = current;
          updateNeedleGeometry(current);
          if (progress < 1) {
            gaugeAnimFrame = requestAnimationFrame(animStep);
          } else {
            currentGaugeAngle = targetAngle;
            updateNeedleGeometry(targetAngle);
          }
        }
        gaugeAnimFrame = requestAnimationFrame(animStep);
      }

      // Calculate Physical Values (R_ego and Heat Q)
      let r_ego = 0.05;
      let heat_q = 0.1;
      if (ci >= 0) {
        r_ego = parseFloat((0.02 + (1.0 - 0.02) * Math.pow((100 - ci) / 100, 2)).toFixed(2));
        heat_q = parseFloat((0.1 + (15.0 - 0.1) * Math.pow((100 - ci) / 100, 2)).toFixed(1));
      } else {
        r_ego = parseFloat((1.0 + (15.0 - 1.0) * Math.pow(Math.abs(ci) / 100, 1.5)).toFixed(1));
        heat_q = parseFloat((15.0 + (160.0 - 15.0) * Math.pow(Math.abs(ci) / 100, 1.5)).toFixed(1));
      }

      // Update CI readouts
      const ciEl = document.getElementById('gauge-ci-val');
      if (ciEl) {
        ciEl.textContent = (ci > 0 ? '+' : '') + ci;
        if (ci >= 20) {
          ciEl.className = 'text-6xl md:text-7xl font-black font-mono tracking-tight bg-gradient-to-r from-emerald-400 via-teal-300 to-cyan-300 bg-clip-text text-transparent';
        } else if (ci >= -30) {
          ciEl.className = 'text-6xl md:text-7xl font-black font-mono tracking-tight bg-gradient-to-r from-amber-400 to-yellow-300 bg-clip-text text-transparent';
        } else {
          ciEl.className = 'text-6xl md:text-7xl font-black font-mono tracking-tight bg-gradient-to-r from-rose-500 to-red-400 bg-clip-text text-transparent';
        }
      }

      const hVal = document.getElementById('gauge-h-val');
      if (hVal) hVal.textContent = h + '%';
      const formulaH = document.getElementById('gauge-formula-h');
      if (formulaH) formulaH.textContent = h + '%';

      // Update HUD metrics
      const regoEl = document.getElementById('live-rego-val');
      const heatEl = document.getElementById('live-heat-val');
      const effEl = document.getElementById('live-eff-val');
      if (regoEl) regoEl.textContent = r_ego + ' Ω';
      if (heatEl) heatEl.textContent = heat_q + ' Вт';
      if (effEl) effEl.textContent = h + '%';

      // Update Sidebar readouts
      const sideCi = document.getElementById('side-ci-readout');
      const sideR = document.getElementById('side-r-readout');
      const sideQ = document.getElementById('side-q-readout');
      const navCiPill = document.getElementById('nav-ci-pill');
      if (sideCi) sideCi.textContent = (ci > 0 ? '+' : '') + ci + ' CI';
      if (sideR) sideR.textContent = r_ego + ' Ω';
      if (sideQ) sideQ.textContent = heat_q + ' Вт';
      if (navCiPill) {
        navCiPill.textContent = (ci > 0 ? '+' : '') + ci;
        if (ci >= 20) navCiPill.className = 'text-[9px] font-mono font-bold px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/30';
        else if (ci >= -30) navCiPill.className = 'text-[9px] font-mono font-bold px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/30';
        else navCiPill.className = 'text-[9px] font-mono font-bold px-1.5 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/30';
      }

      // Update Verdict & Explanations
      const stateLabel = document.getElementById('gauge-state-label');
      const stateTitle = document.getElementById('gauge-state-title');
      const stateDesc = document.getElementById('gauge-state-desc');
      const stateBox = document.getElementById('gauge-state-box');
      const emoji = document.getElementById('gauge-status-emoji');

      if (ci >= 20) {
        if (emoji) emoji.textContent = '🟢';
        if (stateLabel) {
          stateLabel.textContent = '🟢 СВЕРХПРОВОДИМОСТЬ (МУСИН)';
          stateLabel.className = 'text-sm font-bold font-mono text-emerald-300 uppercase tracking-wide';
        }
        if (stateTitle) {
          stateTitle.textContent = 'СТАТУС: КОНТУР В РЕЖИМЕ СВЕРХПРОВОДИМОСТИ';
          stateTitle.className = 'font-bold text-emerald-300';
        }
        if (stateDesc) {
          stateDesc.textContent = 'Внутреннее сопротивление сведено к минимуму (R_ego → 0). Вентральный блуждающий нерв синхронизирует дыхание и сердце, DMN молчит, префронтальная кора работает в режиме TPN (поток). Энергия течёт сквозь проводник без омического трения. Вы переживаете счастье как физическую проводимость жизни!';
        }
        if (stateBox) {
          stateBox.className = 'p-4 rounded-xl border bg-emerald-950/40 border-emerald-500/40 text-emerald-200 text-xs md:text-sm font-mono space-y-2';
        }
      } else if (ci >= -30) {
        if (emoji) emoji.textContent = '🟡';
        if (stateLabel) {
          stateLabel.textContent = '🟡 ХОЛОСТОЙ ХОД (ДРЕЙФ / NPC)';
          stateLabel.className = 'text-sm font-bold font-mono text-amber-300 uppercase tracking-wide';
        }
        if (stateTitle) {
          stateTitle.textContent = 'СТАТУС: КОНТУР В РЕЖИМЕ НЕЙТРАЛИ (ХОЛОСТОЙ ХОД)';
          stateTitle.className = 'font-bold text-amber-300';
        }
        if (stateDesc) {
          stateDesc.textContent = 'Внимание рассеяно. Двигатель работает на нейтральной передаче: резкого выгорания нет, но полезная работа не совершается. Сцепление с реальностью проскальзывает. Для перехода в сверхпроводимость выберите одну ясную задачу в t = now.';
        }
        if (stateBox) {
          stateBox.className = 'p-4 rounded-xl border bg-amber-950/40 border-amber-500/40 text-amber-200 text-xs md:text-sm font-mono space-y-2';
        }
      } else {
        if (emoji) emoji.textContent = '🔴';
        if (stateLabel) {
          stateLabel.textContent = '🔴 ОМИЧЕСКИЙ ПЕРЕГРЕВ (ДИСТРЕСС)';
          stateLabel.className = 'text-sm font-bold font-mono text-rose-400 uppercase tracking-wide';
        }
        if (stateTitle) {
          stateTitle.textContent = 'АВАРИЯ: ОМИЧЕСКИЙ ПЕРЕГРЕВ ПРОВОДКИ (Q = I² · R)';
          stateTitle.className = 'font-bold text-rose-400';
        }
        if (stateDesc) {
          stateDesc.textContent = 'Критический затор проводки! Симпатический овердрайв, выброс кортизола, DMN гиперактивна, дыхание зажато. Энергия преобразуется в разрушительное тепловое трение. Немедленно выполните 30-секундный протокол сброса или откройте Аптечку болей!';
        }
        if (stateBox) {
          stateBox.className = 'p-4 rounded-xl border bg-rose-950/50 border-rose-500/50 text-rose-200 text-xs md:text-sm font-mono space-y-2';
        }
      }

      // Update 5 System Badges
      ['ans', 'endo', 'brain', 'cardio', 'soma'].forEach(sys => {
        gauge_renderSystemBadgeAndDesc(sys, gaugeState[sys]);
      });

      // Synchronize Live Circuit SVG
      updateCircuitSvg(ci, r_ego, heat_q);
    }

    // -------------------------------------------------------------
    // Live Circuit SVG Synchronizer
    // -------------------------------------------------------------
    function updateCircuitSvg(ci, r_ego, heat_q) {
      const tag = document.getElementById('circuitStatusTag');
      const resBox = document.getElementById('svg-resistor-box');
      const resVal = document.getElementById('svg-resistor-val');
      const beam = document.getElementById('svg-light-beam');
      const lampGlow = document.getElementById('svg-lamp-glow');
      const w1 = document.getElementById('svg-wire-1');
      const w2 = document.getElementById('svg-wire-2');
      const w3 = document.getElementById('svg-wire-3');

      if (ci >= 20) {
        if (tag) {
          tag.textContent = 'СВЕРХПРОВОДИМОСТЬ • R → 0';
          tag.className = 'px-3 py-1 rounded-full text-xs font-mono font-semibold tracking-wide border bg-emerald-500/15 text-emerald-300 border-emerald-500/30';
        }
        if (resBox) {
          resBox.setAttribute('stroke', '#10b981');
          resBox.style.animation = 'none';
        }
        if (resVal) {
          resVal.textContent = r_ego + ' Ω • МУСИН (Q=0)';
          resVal.setAttribute('fill', '#34d399');
        }
        if (beam) beam.setAttribute('fill', 'rgba(251, 191, 36, 0.45)');
        if (lampGlow) lampGlow.setAttribute('fill', 'rgba(251, 191, 36, 0.5)');
        [w1, w2, w3].forEach(w => {
          if (w) {
            w.setAttribute('stroke', '#38bdf8');
            w.style.animationDuration = '0.7s';
          }
        });
      } else if (ci >= -30) {
        if (tag) {
          tag.textContent = 'ДРЕЙФ • ХОЛОСТОЙ ХОД';
          tag.className = 'px-3 py-1 rounded-full text-xs font-mono font-semibold tracking-wide border bg-amber-500/15 text-amber-300 border-amber-500/30';
        }
        if (resBox) {
          resBox.setAttribute('stroke', '#f59e0b');
          resBox.style.animation = 'none';
        }
        if (resVal) {
          resVal.textContent = r_ego + ' Ω • ДРЕЙФ';
          resVal.setAttribute('fill', '#fbbf24');
        }
        if (beam) beam.setAttribute('fill', 'rgba(251, 191, 36, 0.2)');
        if (lampGlow) lampGlow.setAttribute('fill', 'rgba(251, 191, 36, 0.25)');
        [w1, w2, w3].forEach(w => {
          if (w) {
            w.setAttribute('stroke', '#f59e0b');
            w.style.animationDuration = '1.3s';
          }
        });
      } else {
        if (tag) {
          tag.textContent = 'ОМИЧЕСКИЙ ПЕРЕГРЕВ • АВАРИЯ';
          tag.className = 'px-3 py-1 rounded-full text-xs font-mono font-semibold tracking-wide border bg-rose-500/20 text-rose-300 border-rose-500/40 animate-pulse';
        }
        if (resBox) {
          resBox.setAttribute('stroke', '#ef4444');
          resBox.style.animation = 'pulse-overheat 1s infinite';
        }
        if (resVal) {
          resVal.textContent = r_ego + ' Ω • ПЕРЕГРЕВ (' + heat_q + 'W)';
          resVal.setAttribute('fill', '#f87171');
        }
        if (beam) beam.setAttribute('fill', 'rgba(239, 68, 68, 0.08)');
        if (lampGlow) lampGlow.setAttribute('fill', 'rgba(239, 68, 68, 0.15)');
        [w1, w2, w3].forEach(w => {
          if (w) {
            w.setAttribute('stroke', '#ef4444');
            w.style.animationDuration = '2.2s';
          }
        });
      }
    }

    // -------------------------------------------------------------
    // Pain-First Remediation Protocol Engine
    // -------------------------------------------------------------
    const HEALING_PROTOCOLS = {
      burnout: {
        icon: '🔥',
        title: 'Протокол «Мусин» запущен: Сброс омического перегрева (R → 0)',
        desc: 'Отсекаем симуляции прошлого и будущего. Внимание заземлено в рецепторы стоп и дыхание низом живота.',
        cardId: 'card-pain-01',
        phases: [
          { progress: 25, badge: 'ФАЗА 1/3: СОМАТИЧЕСКИЙ СБРОС', cue: 'Разомкните зубы, опустите плечи вниз. Медленный выдох через рот...' },
          { progress: 65, badge: 'ФАЗА 2/3: ЗАЗЕМЛЕНИЕ В СТОПЫ', cue: 'Ощутите твёрдый контакт стоп с полом. Переведите вес в низ живота (Тандэн).' },
          { progress: 100, badge: '✓ СВЕРХПРОВОДИМОСТЬ ВОССТАНОВЛЕНА', cue: '«Я не продавливаю реальность. Ток течёт свободно». Перегрев устранён!' }
        ],
        cardTag: '✓ ПРОТОКОЛ «МУСИН» ВЫПОЛНЕН • R → 0'
      },
      imposter: {
        icon: '🪤',
        title: 'Протокол «Нидзиригути» запущен: Разрыв паразитного шунта на Эго',
        desc: 'Сброс статуса и эго-панциря. Внимание переводится с самооценки на служение человеку.',
        cardId: 'card-pain-02',
        phases: [
          { progress: 30, badge: 'ФАЗА 1/3: СБРОС МЕЧА ЭГО', cue: 'Оставьте попытки произвести впечатление. В чайную комнату входят без оружия.' },
          { progress: 70, badge: 'ФАЗА 2/3: ЗАКОН ВОЛЬТМЕТРА', cue: 'Прибор не обижается на напряжение сети. Вы лишь замеряете проводимость контакта.' },
          { progress: 100, badge: '✓ ШУНТ РАЗОМКНУТ', cue: 'Фокус внимания на 100% переведён в решение задачи человека!' }
        ],
        cardTag: '✓ ПРОТОКОЛ «НИДЗИРИГУТИ» ВЫПОЛНЕН • КЗ СНЯТО'
      },
      kintsugi: {
        icon: '🏺',
        title: 'Протокол «Кинцуги & Дзансин»: Изоляция Тандэна после сбоя',
        desc: 'Взвод автомата защиты цепи. Генератор мастера цел, разбита лишь внешняя лампа.',
        cardId: 'card-pain-03',
        phases: [
          { progress: 30, badge: 'ФАЗА 1/3: АВТОМАТ ДЗАНСИН', cue: 'Пауза 10 секунд. Неподвижная осанка лучника. Генератор внутри абсолютно цел.' },
          { progress: 70, badge: 'ФАЗА 2/3: ЗОЛОТОЙ ШОВ КИНЦУГИ', cue: 'Опыт ошибки заполняется золотой смолой осознанности. Проводка стала прочнее.' },
          { progress: 100, badge: '✓ ЦЕПЬ ГОТОВА К НОВОЙ НАГРУЗКЕ', cue: 'Батарея Тандэна готова питать новый замысел!' }
        ],
        cardTag: '✓ ПРОТОКОЛ «КИНЦУГИ» ВЫПОЛНЕН • ДЗАНСИН ВЗВЕДЕН'
      },
      apathy: {
        icon: '🧘',
        title: 'Протокол «Микронагрузка 10W»: Замыкание цепи через микродействие',
        desc: 'Снятие завышенной планки. Запуск тока через элементарный физический контакт.',
        cardId: 'card-pain-04',
        phases: [
          { progress: 30, badge: 'ФАЗА 1/3: СБРОС ИМПЕРИИ', cue: 'Отмените требование свернуть горы. Зажечь лампочку мощностью всего 10 Вт.' },
          { progress: 70, badge: 'ФАЗА 2/3: МИКРОКОНТАКТ', cue: 'Сделайте один крошечный физический шаг прямо сейчас (глоток чая, чистый стол).' },
          { progress: 100, badge: '✓ ЦЕПЬ ЗАМКНУТА', cue: 'Ток пошёл! Силы вернулись через реальное физическое действие.' }
        ],
        cardTag: '✓ ПРОТОКОЛ «МИКРОНАГРУЗКА» ВЫПОЛНЕН • ТОК ТЕЧЁТ'
      },
      scattered: {
        icon: '⚖️',
        title: 'Протокол «Кансо»: Обесточивание балласта и запитка скафандра',
        desc: 'Отключение второстепенных потребителей. Подача энергии в тело и сон.',
        cardId: 'card-pain-05',
        phases: [
          { progress: 30, badge: 'ФАЗА 1/3: ОТСЕЧЕНИЕ БАЛЛАСТА', cue: 'Отключите 9 из 10 параллельных задач. Напряжение генератора не резиновое.' },
          { progress: 70, badge: 'ФАЗА 2/3: ЗАПИТКА СКАФАНДРА', cue: 'Подайте 30 Вт в тело: тёплая вода, глубокое дыхание, прогулка без экрана.' },
          { progress: 100, badge: '✓ СЕТЬ СТАБИЛИЗИРОВАНА', cue: 'Один фокус луча в один момент времени. Баланс восстановлен!' }
        ],
        cardTag: '✓ ПРОТОКОЛ «КАНСО» ВЫПОЛНЕН • СЕТЬ В БАЛАНСЕ'
      }
    };

    let activeHealingPainType = null;
    let healingTimeouts = [];

    function clearHealingTimers() {
      healingTimeouts.forEach(t => clearTimeout(t));
      healingTimeouts = [];
    }

    function scrollToPainCard(cardId) {
      const el = document.getElementById(cardId);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        el.classList.add('ring-2', 'ring-rose-400', 'ring-offset-2', 'ring-offset-slate-950');
        setTimeout(() => {
          el.classList.remove('ring-2', 'ring-rose-400', 'ring-offset-2', 'ring-offset-slate-950');
        }, 1500);
      }
    }

    function executePainRemediation(painType) {
      const proto = HEALING_PROTOCOLS[painType] || HEALING_PROTOCOLS.burnout;
      activeHealingPainType = painType;
      clearHealingTimers();

      const banner = document.getElementById('liveHealingBanner');
      const icon = document.getElementById('liveHealingIcon');
      const title = document.getElementById('liveHealingTitle');
      const desc = document.getElementById('liveHealingDesc');
      const postActions = document.getElementById('liveHealingPostActions');

      if (icon) icon.textContent = proto.icon;
      if (title) title.textContent = proto.title;
      if (desc) desc.textContent = proto.desc;
      if (postActions) postActions.classList.add('hidden');

      if (banner) {
        banner.classList.remove('hidden');
        banner.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }

      playZenChime(528);

      // Phase 1
      renderHealingPhase(proto, 0);

      // Phase 2 after 1.8s
      healingTimeouts.push(setTimeout(() => {
        renderHealingPhase(proto, 1);
        playZenChime(587);
      }, 1800));

      // Phase 3 after 3.8s
      healingTimeouts.push(setTimeout(() => {
        renderHealingPhase(proto, 2);
        playZenChime(659);
        gauge_applyPreset('mushin');
      }, 3800));
    }

    function renderHealingPhase(proto, phaseIndex) {
      const phase = proto.phases[phaseIndex];
      const pBar = document.getElementById('liveHealingProgressBar');
      const pText = document.getElementById('liveHealingProgressPercent');
      const statusText = document.getElementById('liveHealingStatusText');
      const cue = document.getElementById('liveHealingSomaticCue');

      if (pBar) pBar.style.width = phase.progress + '%';
      if (pText) pText.textContent = phase.progress + '%';
      if (statusText) statusText.textContent = phase.badge;
      if (cue) cue.innerHTML = '<span>🌬️</span> ' + phase.cue;

      if (phase.progress === 100) {
        const postActions = document.getElementById('liveHealingPostActions');
        if (postActions) postActions.classList.remove('hidden');
        markPainCardHealed(proto.cardId, proto.cardTag);
      }
    }

    function markPainCardHealed(cardId, tagText) {
      const card = document.getElementById(cardId);
      if (!card) return;
      card.classList.add('ring-2', 'ring-emerald-500/80', 'ring-offset-2', 'ring-offset-slate-950');
      let badge = document.getElementById(cardId + '-healed-badge');
      if (!badge) {
        badge = document.createElement('div');
        badge.id = cardId + '-healed-badge';
        badge.className = 'p-3 rounded-xl bg-emerald-950/70 border border-emerald-500/50 text-emerald-300 text-xs font-mono flex items-center justify-between shadow-lg mb-2';
        card.prepend(badge);
      }
      badge.innerHTML = '<span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-emerald-400"></span>' + tagText + '</span><span class="text-[10px] text-emerald-400/80 uppercase">СВЕРХПРОВОДИМОСТЬ</span>';
    }

    function closeLiveHealingBanner() {
      clearHealingTimers();
      const banner = document.getElementById('liveHealingBanner');
      if (banner) banner.classList.add('hidden');
    }

    // -------------------------------------------------------------
    // Zen Chime Audio Synthesis (Web Audio API)
    // -------------------------------------------------------------
    function playZenChime(freq = 528) {
      try {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (!AudioCtx) return;
        const ctx = new AudioCtx();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, ctx.currentTime);
        gain.gain.setValueAtTime(0.08, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 1.2);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 1.2);
      } catch (e) {}
    }

    // -------------------------------------------------------------
    // App Initialization
    // -------------------------------------------------------------
    window.addEventListener('DOMContentLoaded', () => {
      let initialTab = 'speedometer';
      const hash = window.location.hash.replace('#', '');
      const validTabs = ['speedometer', 'pains', 'lab', 'dashboard', 'gauge', 'stress', 'errors', 'ideal'];

      if (validTabs.includes(hash)) {
        if (hash === 'errors' || hash === 'pains') {
          initialTab = 'pains';
        } else if (hash === 'ideal' || hash === 'lab') {
          initialTab = 'lab';
        } else {
          initialTab = 'speedometer';
        }
      } else {
        try {
          const saved = localStorage.getItem('inner_current_active_tab');
          if (saved === 'pains' || saved === 'lab' || saved === 'speedometer') {
            initialTab = saved;
          }
        } catch (e) {}
      }

      switchTab(initialTab);
      gauge_render();
    });
  </script>

  <script src="/assets/tracker.js" defer></script>
</body>
</html>
`;

fs.writeFileSync('public/trainer.html', htmlContent, 'utf8');
fs.writeFileSync('dist_site/trainer.html', htmlContent, 'utf8');
console.log('Successfully written trainer.html to public/ and dist_site/! Size:', (htmlContent.length / 1024).toFixed(2), 'KB');
