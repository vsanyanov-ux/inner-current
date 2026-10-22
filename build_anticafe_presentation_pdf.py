import os
import pypdf
from playwright.sync_api import sync_playwright

OUTPUT_HTML = r"C:\Users\vanya\Antigravity Projects\Apps\Inner Current\presentation\happiness_flashlight_deck.html"
OUTPUT_PDF = r"C:\Users\vanya\Antigravity Projects\Apps\Inner Current\IC Library\Презентация — Счастье это карманный фонарик (Лекция в антикафе).pdf"

# Slides HTML template with 16:9 layout
html_content = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Счастье: это карманный фонарик — Владимир Аньянов</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap');

  @page {
    size: 297mm 167.0625mm; /* 16:9 landscape */
    margin: 0;
  }

  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  body {
    background: #080c14;
    color: #f1f5f9;
    font-family: 'Plus Jakarta Sans', sans-serif;
    overflow-x: hidden;
    margin: 0;
    padding: 0;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  /* SLIDE CONTAINER FOR SCREEN PRESENTATION */
  .deck {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .slide {
    width: 100vw;
    height: 100vh;
    max-width: 1920px;
    max-height: 1080px;
    aspect-ratio: 16 / 9;
    padding: 4.5vw 6vw;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
    background: #0b1120;
    border-bottom: 2px solid #1e293b;
    page-break-after: always;
    overflow: hidden;
  }

  @media print {
    .slide {
      width: 297mm !important;
      height: 167mm !important;
      max-width: none !important;
      max-height: none !important;
      padding: 14mm 18mm !important;
      border: none !important;
    }
  }

  /* DECORATIVE BACKGROUND GLOW */
  .glow {
    position: absolute;
    width: 35vw;
    height: 35vw;
    border-radius: 50%;
    filter: blur(100px);
    opacity: 0.12;
    pointer-events: none;
    z-index: 0;
  }
  .glow-amber { background: #f59e0b; top: -10vw; right: -10vw; }
  .glow-blue { background: #38bdf8; bottom: -10vw; left: -10vw; }

  /* SLIDE CONTENT Z-INDEX */
  .slide-header, .slide-body, .slide-footer {
    position: relative;
    z-index: 1;
  }

  /* SLIDE HEADER */
  .slide-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
  }

  .badge-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85vw;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #f59e0b;
    background: rgba(245, 158, 11, 0.12);
    border: 1px solid rgba(245, 158, 11, 0.3);
    padding: 0.35vw 0.9vw;
    border-radius: 6px;
    display: inline-block;
    margin-bottom: 0.6vw;
  }

  .slide-title {
    font-size: 2.5vw;
    font-weight: 800;
    color: #ffffff;
    line-height: 1.15;
    letter-spacing: -0.5px;
  }

  .slide-title span {
    color: #f59e0b;
  }

  .slide-subtitle {
    font-size: 1.1vw;
    color: #94a3b8;
    margin-top: 0.4vw;
  }

  .slide-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1vw;
    font-weight: 700;
    color: #475569;
    background: #111827;
    padding: 0.3vw 0.8vw;
    border-radius: 6px;
    border: 1px solid #1f2937;
  }

  /* SLIDE BODY */
  .slide-body {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    margin: 1.5vw 0;
  }

  /* SLIDE FOOTER */
  .slide-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    padding-top: 1vw;
    font-size: 0.85vw;
    color: #64748b;
  }

  .speaker-brand {
    font-weight: 700;
    color: #cbd5e1;
  }

  /* SPECIAL CARDS & GRIDS */
  .grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2vw;
  }

  .grid-3 {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1.8vw;
  }

  .grid-4 {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.4vw;
  }

  .card {
    background: rgba(17, 24, 39, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 1.5vw;
    backdrop-filter: blur(10px);
  }

  .card-highlight {
    background: rgba(245, 158, 11, 0.05);
    border-color: rgba(245, 158, 11, 0.3);
  }

  .card-danger {
    background: rgba(239, 68, 68, 0.05);
    border-color: rgba(239, 68, 68, 0.3);
  }

  .card-success {
    background: rgba(16, 185, 129, 0.05);
    border-color: rgba(16, 185, 129, 0.3);
  }

  .card-icon {
    font-size: 2.2vw;
    margin-bottom: 0.8vw;
  }

  .card-title {
    font-size: 1.3vw;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.5vw;
  }

  .card-text {
    font-size: 0.95vw;
    line-height: 1.45;
    color: #94a3b8;
  }

  .card-text strong {
    color: #f1f5f9;
  }

  /* BIG HERO CALLOUT */
  .hero-quote {
    font-size: 1.8vw;
    font-weight: 700;
    line-height: 1.4;
    color: #f8fafc;
    border-left: 5px solid #f59e0b;
    padding-left: 1.8vw;
    margin: 1vw 0;
  }

  .hero-quote span {
    color: #f59e0b;
  }

  /* SCHEMATIC STRIP & VECTOR BLUEPRINT */
  .schematic-wrapper {
    background: #090e1a;
    border: 1px solid #1e293b;
    border-radius: 14px;
    padding: 0.8vw 1.2vw;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.05);
    position: relative;
  }

  .card-compact {
    background: rgba(17, 24, 39, 0.75);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 10px;
    padding: 0.8vw 1.1vw;
    backdrop-filter: blur(10px);
  }

  .card-compact .card-title {
    font-size: 0.95vw;
    font-weight: 700;
    margin-bottom: 0.3vw;
  }

  .card-compact .card-text {
    font-size: 0.78vw;
    line-height: 1.4;
    color: #94a3b8;
  }

  @media print {
    #slide-3 {
      padding: 8mm 12mm !important;
    }
    .schematic-wrapper {
      padding: 1.5mm 3mm !important;
    }
    .card-compact {
      padding: 2.2mm 3mm !important;
    }
    .card-compact .card-title {
      font-size: 8pt !important;
      margin-bottom: 0.8mm !important;
    }
    .card-compact .card-text {
      font-size: 6.8pt !important;
      line-height: 1.25 !important;
    }
  }

  .schematic-bar {
    background: #0f172a;
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 1.5vw 2vw;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .schematic-node {
    text-align: center;
    flex: 1;
  }

  .node-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75vw;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  .node-name {
    font-size: 1.25vw;
    font-weight: 800;
    color: #38bdf8;
    margin: 0.3vw 0;
  }

  .node-desc {
    font-size: 0.85vw;
    color: #cbd5e1;
  }

  .node-arrow {
    font-size: 1.8vw;
    color: #475569;
    font-weight: 800;
    padding: 0 0.8vw;
  }

  /* INTERACTIVE KEYS HELPER */
  .nav-hint {
    position: fixed;
    bottom: 15px;
    right: 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: #64748b;
    background: #0b1120;
    padding: 6px 12px;
    border-radius: 8px;
    border: 1px solid #1e293b;
    z-index: 100;
  }

  @media print {
    .nav-hint { display: none !important; }
  }
</style>
</head>
<body>

<div class="nav-hint">Клавиши: ← / → или Пробел · F: Полный экран</div>

<div class="deck">

  <!-- ==================== СЛАЙД 1: ТИТУЛЬНЫЙ ==================== -->
  <section class="slide" id="slide-1">
    <div class="glow glow-amber"></div>
    <div class="glow glow-blue"></div>
    
    <div class="slide-header">
      <div>
        <div class="badge-tag">Открытая лекция · Антикафе</div>
        <div class="slide-subtitle" style="font-size: 1.2vw; color: #94a3b8;">Простая физика человеческого состояния</div>
      </div>
      <div class="slide-num">01 / 12</div>
    </div>

    <div class="slide-body" style="justify-content: center;">
      <h1 style="font-size: 4vw; font-weight: 800; line-height: 1.1; margin-bottom: 1.2vw; letter-spacing: -1px;">
        Счастье: это <span style="color: #f59e0b;">карманный фонарик</span>
      </h1>
      <p style="font-size: 1.6vw; color: #cbd5e1; max-width: 80%; line-height: 1.4; margin-bottom: 2vw;">
        Почему мы ждём свет снаружи, покупаем вещи, гонимся за успехом, но чувствуем себя как выключенный прибор — и как устроен наш внутренний контур.
      </p>
      
      <div style="display: flex; gap: 2vw; align-items: center;">
        <div style="background: rgba(245, 158, 11, 0.1); border: 1px solid rgba(245, 158, 11, 0.3); padding: 0.8vw 1.5vw; border-radius: 8px;">
          <div style="font-size: 1.1vw; font-weight: 800; color: #ffffff;">Владимир Аньянов</div>
          <div style="font-size: 0.85vw; color: #f59e0b;">Исследователь · Автор Системы «Внутренний ток»</div>
        </div>
        <div style="font-size: 1vw; color: #64748b;">
          45 минут живого диалога · Ноль занудства · Только чистая наглядная физика
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <div>Антикафе · Уютный лекторий</div>
      <div class="speaker-brand">Система Аньянова · Лекция для взрослых</div>
    </div>
  </section>


  <!-- ==================== СЛАЙД 2: ЛОВУШКА 21 ВЕКА ==================== -->
  <section class="slide" id="slide-2">
    <div class="glow glow-amber"></div>
    <div class="slide-header">
      <div>
        <div class="badge-tag">Парадокс современности</div>
        <div class="slide-title">Великая ловушка: <span>«Вот куплю — и заживу!»</span></div>
      </div>
      <div class="slide-num">02 / 12</div>
    </div>

    <div class="slide-body">
      <div class="hero-quote">
        «Каждый из нас хоть раз покупал новый телефон, машину или пальто с тайной мыслью: <span>„Вот теперь моя жизнь станет яркой!“</span>. Но проходит две недели... и магия исчезает».
      </div>

      <div class="grid-3" style="margin-top: 1.5vw;">
        <div class="card">
          <div class="card-icon">📱</div>
          <div class="card-title">День 1: Эйфория</div>
          <div class="card-text">
            Сняли плёночку, глаза горят, восторг! Кажется, что внутри коробки лежало само счастье.
          </div>
        </div>
        <div class="card">
          <div class="card-icon">⏳</div>
          <div class="card-title">День 14: Привычка</div>
          <div class="card-text">
            Тот же телефон лежит на столе. Обычный кусок стекла и алюминия. Чудо испарилось.
          </div>
        </div>
        <div class="card card-highlight">
          <div class="card-icon">❓</div>
          <div class="card-title">Главный вопрос</div>
          <div class="card-text">
            <strong>Куда делось счастье?</strong> Украли? Выветрилось? Или его в телефоне никогда и не было?
          </div>
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <div>Интерактивный вопрос в зал</div>
      <div>Ловушка материального ожидания</div>
    </div>
  </section>


  <!-- ==================== СЛАЙД 3: ПРИНЦИПИАЛЬНАЯ СХЕМА ФОНАРИКА ==================== -->
  <section class="slide" id="slide-3">
    <div class="glow glow-blue"></div>
    <div class="glow glow-amber"></div>

    <div class="slide-header">
      <div>
        <div class="badge-tag">Фундаментальная модель · Принципиальная схема</div>
        <div class="slide-title">Человек — это <span>Карманный Фонарик</span></div>
        <div class="slide-subtitle">Принципиальная схема счастья: как устроен наш внутренний контур и где бежит ток жизни</div>
      </div>
      <div class="slide-num">03 / 12</div>
    </div>

    <div class="slide-body" style="margin: 0.8vw 0; gap: 0.9vw;">
      <!-- SVG SCHEMATIC OF THE FLASHLIGHT -->
      <div class="schematic-wrapper">
        <svg viewBox="0 0 1440 430" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" style="display: block; max-height: 420px;">
          <defs>
            <linearGradient id="beamGrad" x1="0%" y1="50%" x2="100%" y2="50%">
              <stop offset="0%" stop-color="#fbbf24" stop-opacity="0.95"/>
              <stop offset="25%" stop-color="#f59e0b" stop-opacity="0.55"/>
              <stop offset="65%" stop-color="#f59e0b" stop-opacity="0.18"/>
              <stop offset="100%" stop-color="#f59e0b" stop-opacity="0.0"/>
            </linearGradient>
            <linearGradient id="tandenGrad" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stop-color="#10b981"/>
              <stop offset="60%" stop-color="#059669"/>
              <stop offset="100%" stop-color="#047857"/>
            </linearGradient>
            <filter id="glowCyan" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="3" result="blur" />
              <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
            </filter>
            <filter id="glowAmber" x="-20%" y="-20%" width="140%" height="140%">
              <feGaussianBlur stdDeviation="5" result="blur" />
              <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
            </filter>
          </defs>

          <!-- FLASHLIGHT CASING (DASHED CHASSIS) -->
          <rect x="25" y="10" width="985" height="410" rx="20" fill="#0d1424" stroke="#253349" stroke-width="2" stroke-dasharray="6 6"/>
          <text x="50" y="34" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="700" fill="#64748b" letter-spacing="1.5">МЕТАЛЛИЧЕСКИЙ КОРПУС ФОНАРИКА (СОМАТИЧЕСКАЯ АРХИТЕКТУРА ЧЕЛОВЕКА)</text>

          <!-- LIGHT BEAM SPREADING OUT TO THE RIGHT -->
          <polygon points="985,170 1425,25 1425,395 985,250" fill="url(#beamGrad)"/>
          <line x1="985" y1="170" x2="1425" y2="25" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="4 4" stroke-opacity="0.8"/>
          <line x1="985" y1="250" x2="1425" y2="395" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="4 4" stroke-opacity="0.8"/>

          <!-- TEXT INSIDE LIGHT BEAM -->
          <g transform="translate(1040, 145)">
            <rect x="-10" y="-18" width="290" height="150" rx="12" fill="rgba(11, 17, 32, 0.9)" stroke="rgba(245, 158, 11, 0.45)" stroke-width="1.5"/>
            <text x="0" y="8" font-family="'Plus Jakarta Sans', sans-serif" font-size="16" font-weight="800" fill="#fbbf24">🔦 СВЕТОВОЙ ЛУЧ</text>
            <text x="0" y="32" font-family="'Plus Jakarta Sans', sans-serif" font-size="13" font-weight="700" fill="#ffffff">Направлен во внешний мир!</text>
            <text x="0" y="52" font-family="'Plus Jakarta Sans', sans-serif" font-size="11.5" fill="#94a3b8">Люди, дела, текст, чашка чая</text>
            <line x1="0" y1="64" x2="265" y2="64" stroke="#334155" stroke-width="1"/>
            <text x="0" y="84" font-family="'Plus Jakarta Sans', sans-serif" font-size="11.5" font-weight="600" fill="#38bdf8">Вещи холодные и тёмные.</text>
            <text x="0" y="104" font-family="'Plus Jakarta Sans', sans-serif" font-size="11.5" fill="#cbd5e1">Они лишь отражают ваш свет!</text>
          </g>

          <!-- ================= UZEL 1: BATTERY (TANDEN) ================= -->
          <g transform="translate(65, 110)">
            <rect x="0" y="0" width="130" height="225" rx="16" fill="#111827" stroke="#10b981" stroke-width="2.5"/>
            <!-- Terminal cap -->
            <rect x="35" y="-12" width="60" height="12" rx="4" fill="#10b981"/>
            <!-- Battery level block -->
            <rect x="15" y="15" width="100" height="130" rx="8" fill="url(#tandenGrad)" opacity="0.95"/>
            <text x="65" y="62" text-anchor="middle" font-size="28">🔋</text>
            <text x="65" y="96" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="16" font-weight="800" fill="#ffffff">100%</text>
            <text x="65" y="118" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="700" fill="#d1fae5" letter-spacing="1">ЭДС ПОЛНА</text>
            
            <text x="65" y="172" text-anchor="middle" font-family="'Plus Jakarta Sans', sans-serif" font-size="14" font-weight="800" fill="#10b981">ТАНДЭН (丹田)</text>
            <text x="65" y="192" text-anchor="middle" font-family="'Plus Jakarta Sans', sans-serif" font-size="11" font-weight="700" fill="#f1f5f9">Низ живота · Тело</text>
            <text x="65" y="210" text-anchor="middle" font-family="'Plus Jakarta Sans', sans-serif" font-size="10" fill="#94a3b8">Заряжен каждое утро!</text>

            <!-- Terminal Markers -->
            <circle cx="65" cy="-4" r="8" fill="#f59e0b"/>
            <text x="65" y="0" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="12" font-weight="800" fill="#000">+</text>
            <circle cx="65" cy="230" r="8" fill="#38bdf8"/>
            <text x="65" y="234" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="12" font-weight="800" fill="#000">−</text>
          </g>

          <!-- ================= UPPER WIRE: CURRENT FLOW (MUSHIN) ================= -->
          <path d="M 130 98 L 130 65 L 340 65" fill="none" stroke="#38bdf8" stroke-width="4" stroke-linecap="round" filter="url(#glowCyan)"/>
          <!-- Arrowhead -->
          <polygon points="215,60 230,65 215,70" fill="#38bdf8"/>
          <polygon points="295,60 310,65 295,70" fill="#38bdf8"/>
          <text x="155" y="52" font-family="'JetBrains Mono', monospace" font-size="11" font-weight="700" fill="#38bdf8">ТОК ВНИМАНИЯ (I)</text>

          <!-- ================= UZEL 2: SWITCH (HOTSU) ================= -->
          <g transform="translate(340, 35)">
            <rect x="0" y="0" width="160" height="60" rx="10" fill="#111827" stroke="#38bdf8" stroke-width="1.5"/>
            <circle cx="25" cy="30" r="6" fill="#38bdf8"/>
            <circle cx="135" cy="30" r="6" fill="#38bdf8"/>
            <!-- Closed lever -->
            <line x1="25" y1="30" x2="135" y2="30" stroke="#10b981" stroke-width="4" stroke-linecap="round"/>
            <text x="80" y="22" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="10" font-weight="800" fill="#10b981">ЗАМКНУТО [ 1 ]</text>
            <text x="80" y="46" text-anchor="middle" font-family="'Plus Jakarta Sans', sans-serif" font-size="12" font-weight="800" fill="#ffffff">КНОПКА «ЩЁЛК!»</text>
            <text x="80" y="76" text-anchor="middle" font-family="'Plus Jakarta Sans', sans-serif" font-size="11" font-weight="600" fill="#94a3b8">Хоцу: решение прямо сейчас</text>
          </g>

          <!-- WIRE FROM SWITCH TO CONDUCTOR / EGO -->
          <path d="M 500 65 L 575 65" fill="none" stroke="#38bdf8" stroke-width="4" stroke-linecap="round"/>
          <polygon points="535,60 550,65 535,70" fill="#38bdf8"/>

          <!-- ================= PARASITIC EGO RESISTOR (R_EGO) ================= -->
          <g transform="translate(575, 25)">
            <rect x="0" y="0" width="225" height="80" rx="10" fill="rgba(239, 68, 68, 0.08)" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="4 4"/>
            <!-- Direct bypass superconducting line (Mushin) -->
            <line x1="15" y1="35" x2="210" y2="35" stroke="#10b981" stroke-width="3.5" stroke-linecap="round"/>
            <text x="112" y="24" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="10.5" font-weight="800" fill="#10b981">МУСИН: R = 0 (ПОТОК)</text>
            <!-- Ego Resistor Hazard below -->
            <path d="M 40 52 L 55 62 L 70 45 L 85 62 L 100 45 L 115 62 L 130 45 L 145 62 L 160 52" fill="none" stroke="#ef4444" stroke-width="2"/>
            <text x="112" y="73" text-anchor="middle" font-family="'Plus Jakarta Sans', sans-serif" font-size="10" font-weight="700" fill="#f87171">Реостат Эго: сомнения и страх</text>
            <text x="112" y="100" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="9.5" fill="#fca5a5">Омический перегрев Q = I²·R·t</text>
          </g>

          <!-- WIRE TO BULB -->
          <path d="M 800 65 L 920 65 L 920 145" fill="none" stroke="#f59e0b" stroke-width="4" stroke-linecap="round" filter="url(#glowAmber)"/>
          <polygon points="850,60 865,65 850,70" fill="#f59e0b"/>

          <!-- ================= UZEL 3: BULB & REFLECTOR (GYO) ================= -->
          <g transform="translate(860, 145)">
            <!-- Parabolic Reflector -->
            <path d="M 15 10 C 75 30, 75 110, 15 130 Z" fill="#1e293b" stroke="#f59e0b" stroke-width="2"/>
            <!-- Lens -->
            <line x1="75" y1="20" x2="75" y2="120" stroke="#38bdf8" stroke-width="4" stroke-linecap="round" opacity="0.9"/>
            <!-- Bulb Socket -->
            <circle cx="50" cy="70" r="24" fill="#111827" stroke="#f59e0b" stroke-width="2"/>
            <!-- Glowing Filament -->
            <circle cx="50" cy="70" r="14" fill="#fbbf24" filter="url(#glowAmber)"/>
            <text x="50" y="77" text-anchor="middle" font-size="18">💡</text>
            
            <text x="50" y="152" text-anchor="middle" font-family="'Plus Jakarta Sans', sans-serif" font-size="13.5" font-weight="800" fill="#fbbf24">ЛАМПОЧКА (ГЁ)</text>
            <text x="50" y="170" text-anchor="middle" font-family="'Plus Jakarta Sans', sans-serif" font-size="11" font-weight="700" fill="#f1f5f9">Созидательное действие</text>
            <text x="50" y="186" text-anchor="middle" font-family="'Plus Jakarta Sans', sans-serif" font-size="10" fill="#94a3b8">Руки, голос, внимание</text>
          </g>

          <!-- ================= UZEL 4: RETURN WIRE (KIRCHHOFF / ZANSHIN) ================= -->
          <path d="M 920 335 L 920 375 L 130 375 L 130 340" fill="none" stroke="#38bdf8" stroke-width="4" stroke-linecap="round"/>
          <!-- Return Arrows -->
          <polygon points="760,380 745,375 760,370" fill="#38bdf8"/>
          <polygon points="520,380 505,375 520,370" fill="#38bdf8"/>
          <polygon points="280,380 265,375 280,370" fill="#38bdf8"/>
          
          <text x="510" y="365" text-anchor="middle" font-family="'Plus Jakarta Sans', sans-serif" font-size="13" font-weight="800" fill="#38bdf8">🔄 ОБРАТНЫЙ ПРОВОД КИРХГОФА (ДЗАНСИН) · ЗАМЫКАНИЕ КОНТУРА</text>
          <text x="510" y="398" text-anchor="middle" font-family="'Plus Jakarta Sans', sans-serif" font-size="11" fill="#94a3b8">Действие завершено в реальности ➜ Энергия возвращается в тело ➜ Покой, сытость, прохладный корпус</text>

          <!-- ================= CENTRAL BLUEPRINT FORMULA CARD ================= -->
          <g transform="translate(230, 150)">
            <rect x="0" y="0" width="580" height="175" rx="14" fill="rgba(15, 23, 42, 0.96)" stroke="#f59e0b" stroke-width="1.5"/>
            <text x="290" y="28" text-anchor="middle" font-family="'Plus Jakarta Sans', sans-serif" font-size="13" font-weight="800" fill="#f59e0b" letter-spacing="1">⚡ СХЕМОТЕХНИКА СЧАСТЬЯ: ТОК В ЗАМКНУТОЙ СВЕРХПРОВОДЯЩЕЙ ЦЕПИ</text>
            
            <text x="290" y="54" text-anchor="middle" font-family="'JetBrains Mono', monospace" font-size="14" font-weight="700" fill="#ffffff">
              I > 0  ·  R_ego = 0  ·  Кнопка [ 1 ]  ·  Контур замкнут наружу
            </text>
            
            <line x1="25" y1="66" x2="555" y2="66" stroke="#334155" stroke-width="1"/>
            
            <!-- State 1: Green -->
            <text x="35" y="90" font-family="'Plus Jakarta Sans', sans-serif" font-size="11.5" font-weight="700" fill="#34d399">✔ НОРМА (Счастье):</text>
            <text x="180" y="90" font-family="'Plus Jakarta Sans', sans-serif" font-size="11.5" fill="#e2e8f0">Ток из живота без трения в руки ➜ луч в мир ➜ контур замкнут ➜ радость.</text>
            
            <!-- State 2: Red -->
            <text x="35" y="120" font-family="'Plus Jakarta Sans', sans-serif" font-size="11.5" font-weight="700" fill="#f87171">✖ СБОЙ 1 (Тревога):</text>
            <text x="180" y="120" font-family="'Plus Jakarta Sans', sans-serif" font-size="11.5" fill="#e2e8f0">Включён реостат сомнений (R_ego &gt; 0) ➜ корпус кипит, впереди тьма.</text>
            
            <!-- State 3: Amber -->
            <text x="35" y="150" font-family="'Plus Jakarta Sans', sans-serif" font-size="11.5" font-weight="700" fill="#fbbf24">✖ СБОЙ 2 (Истощение):</text>
            <text x="180" y="150" font-family="'Plus Jakarta Sans', sans-serif" font-size="11.5" fill="#e2e8f0">Обрыв обратного провода (думскроллинг) ➜ ток слит в экран без возврата.</text>
          </g>
        </svg>
      </div>

      <!-- 4 BOTTOM CARDS FOR SPEAKER TALKING POINTS -->
      <div class="grid-4">
        <div class="card-compact">
          <div class="card-title" style="color: #10b981;">🔋 1. Батарейка (Тандэн)</div>
          <div class="card-text">
            Заряжена с рождения каждое утро (дыхание, тело). <strong>Энергия есть всегда</strong> — она не зависит от погоды или мнения начальника.
          </div>
        </div>
        <div class="card-compact">
          <div class="card-title" style="color: #38bdf8;">🔘 2. Кнопка «Щёлк!»</div>
          <div class="card-text">
            Режим <strong>0 или 1</strong>. Фонарик не бывает «на 15% включён». Ты либо варишься в мыслях, либо нажал кнопку и делаешь дело.
          </div>
        </div>
        <div class="card-compact">
          <div class="card-title" style="color: #f87171;">⚠️ 3. Реостат Эго (R_ego)</div>
          <div class="card-text">
            Самоедство и страх оценки. При R &gt; 0 проводка плавится (Q = I²·R·t). <strong>Снимите оценку</strong> — включится сверхпроводимость.
          </div>
        </div>
        <div class="card-compact">
          <div class="card-title" style="color: #fbbf24;">💡 4. Луч и Замыкание</div>
          <div class="card-text">
            Светить <strong>только наружу</strong>! А реальное завершённое действие замыкает провод Кирхгофа: корпус остывает, в душе мир.
          </div>
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <div>Принципиальная схемотехника человека</div>
      <div class="speaker-brand">Система Аньянова · Лекция для взрослых</div>
    </div>
  </section>


  <!-- ==================== СЛАЙД 4: ОШИБКА ХОЛОДНЫХ ВЕЩЕЙ ==================== -->
  <section class="slide" id="slide-4">
    <div class="glow glow-amber"></div>
    <div class="slide-header">
      <div>
        <div class="badge-tag">Оптический закон</div>
        <div class="slide-title">Разоблачение: <span>Вещи — холодные!</span></div>
        <div class="slide-subtitle">Ошибка атрибуции: почему мы приписываем вещам собственный свет</div>
      </div>
      <div class="slide-num">04 / 12</div>
    </div>

    <div class="slide-body">
      <div class="grid-2">
        <div class="card card-danger">
          <div class="card-title" style="color: #f87171;">❌ Оптическая иллюзия:</div>
          <div class="card-text" style="font-size: 1.05vw;">
            «Чашка рафа, новый автомобиль, ресторан или город светятся радостью сами по себе. Мне нужно подойти к ним и впитать их свет».
            <br><br>
            <strong>Итог:</strong> Разочарование, ненасытность, бесконечный шопинг и опустошение.
          </div>
        </div>

        <div class="card card-success">
          <div class="card-title" style="color: #4ade80;">✅ Физический факт:</div>
          <div class="card-text" style="font-size: 1.05vw;">
            Все предметы в мире — <strong>тёмные и холодные</strong>. Но когда вы смотрите на них с включённым лучом внимания, они <strong>отражают ваш свет обратно</strong>!
            <br><br>
            <strong>Итог:</strong> Источник тепла и праздника — вы сами. Вещи лишь экран для вашего луча.
          </div>
        </div>
      </div>

      <div class="hero-quote" style="font-size: 1.4vw; margin-top: 1.5vw;">
        «Новый айфон не умеет радоваться. Радуетесь вы, когда светите на него. А когда луч уходит — айфон остаётся куском металла».
      </div>
    </div>

    <div class="slide-footer">
      <div>Снятие потребительского гипноза</div>
      <div>Свет рождается внутри</div>
    </div>
  </section>


  <!-- ==================== СЛАЙД 5: СВЕЧЕНИЕ ВНУТРЬ СЕБЯ ==================== -->
  <section class="slide" id="slide-5">
    <div class="glow glow-amber"></div>
    <div class="slide-header">
      <div>
        <div class="badge-tag">Диагностика сбоя</div>
        <div class="slide-title">Самая нелепая поломка: <span>Светить внутрь себя</span></div>
        <div class="slide-subtitle">Как рождается взрослая тревожность, паника и бессонница</div>
      </div>
      <div class="slide-num">05 / 12</div>
    </div>

    <div class="slide-body">
      <div class="grid-2">
        <div>
          <div class="card card-danger" style="height: 100%;">
            <div class="card-title" style="color: #f87171;">💥 Что делает взрослый человек:</div>
            <div class="card-text" style="font-size: 1vw; line-height: 1.5;">
              Выкручивает лампочку из фонарика и засовывает её внутрь корпуса, прямо к батарейке:
              <br><br>
              • <em>«А я достаточно успешен к 30 годам?»</em><br>
              • <em>«А что обо мне подумал начальник?»</em><br>
              • <em>«А не глупо ли я сейчас выгляжу со стороны?»</em><br>
              • <em>«А вдруг я хуже других?»</em>
            </div>
          </div>
        </div>

        <div>
          <div class="card" style="height: 100%;">
            <div class="card-title">🌡️ Физические последствия:</div>
            <div class="card-text" style="font-size: 1vw; line-height: 1.5;">
              <strong>1. Корпус раскаляется докрасна:</strong><br>
              Краснеют щёки, потеют ладони, тахикардия, ком в горле — энергия сжигает саму себя.<br><br>
              <strong>2. Впереди наступает тьма:</strong><br>
              Дороги под ногами не видно. Человек спотыкается на работе, в разговорах и делах.<br><br>
              <strong>3. Ток крадёт ржавый реостат сомнений.</strong>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <div>Анатомия невротической рефлексии</div>
      <div>Перегрев корпуса вместо света</div>
    </div>
  </section>


  <!-- ==================== СЛАЙД 6: ЗАКОН ПРЯМОГО ЛУЧА ==================== -->
  <section class="slide" id="slide-6">
    <div class="glow glow-blue"></div>
    <div class="slide-header">
      <div>
        <div class="badge-tag">Оптический закон №1</div>
        <div class="slide-title">Закон Прямого Луча: <span>Светить только наружу!</span></div>
        <div class="slide-subtitle">Мгновенный чит-код от любого социального страха</div>
      </div>
      <div class="slide-num">06 / 12</div>
    </div>

    <div class="slide-body">
      <div class="hero-quote">
        «Фонарик конструктивно создан для того, чтобы <span>светить только вперёд</span>. Как только вы направляете луч на собеседника, текст или задачу — корпус мгновенно остывает».
      </div>

      <div class="grid-3" style="margin-top: 1.5vw;">
        <div class="card">
          <div class="card-icon">🎤</div>
          <div class="card-title">Публичное выступление</div>
          <div class="card-text">
            Забудьте о себе. Направьте луч на людей в зале: <em>«Что ценного я могу подарить этим глазам прямо сейчас?»</em>. Страх испаряется за 2 секунды.
          </div>
        </div>
        <div class="card">
          <div class="card-icon">💼</div>
          <div class="card-title">Трудные переговоры</div>
          <div class="card-text">
            Не думайте «как я выгляжу». Светите на задачу на столе. Собеседник почувствует ваше спокойствие и уважение.
          </div>
        </div>
        <div class="card card-highlight">
          <div class="card-icon">⚡</div>
          <div class="card-title">Чистый ток (Мусин)</div>
          <div class="card-text">
            Режим, когда между намерением и действием нет трения. Руки делают, слова звучат точно и легко.
          </div>
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <div>Прикладная калибровка внимания</div>
      <div>Свобода от оценки себя</div>
    </div>
  </section>


  <!-- ==================== СЛАЙД 7: ЗАМКНУТЫЙ КОНТУР ==================== -->
  <section class="slide" id="slide-7">
    <div class="glow glow-amber"></div>
    <div class="slide-header">
      <div>
        <div class="badge-tag">Энергетический баланс</div>
        <div class="slide-title">Замкнутый контур: <span>Почему диван истощает</span></div>
        <div class="slide-subtitle">Разгадка феномена усталости от безделья и скроллинга ленты</div>
      </div>
      <div class="slide-num">07 / 12</div>
    </div>

    <div class="slide-body">
      <div class="grid-2">
        <div class="card card-danger">
          <div class="card-title" style="color: #f87171;">📴 Разомкнутая цепь (Думскроллинг)</div>
          <div class="card-text" style="font-size: 1vw;">
            Лежали 4 часа в телефоне. Ничего не создали. Внимание ушло в холодное мерцание пикселей.
            <br><br>
            <strong>Результат:</strong> Ток ушёл в пустоту. Возврата энергии нет. Вы встаёте разбитыми, словно разгружали вагоны с углем.
          </div>
        </div>

        <div class="card card-success">
          <div class="card-title" style="color: #4ade80;">🔄 Замкнутая цепь (Прямое созидание)</div>
          <div class="card-text" style="font-size: 1vw;">
            Приготовили ужин, починили стул, написали главу, вышли на пробежку. Луч встретил <strong>реальный предмет</strong>.
            <br><br>
            <strong>Результат:</strong> Отражённый свет возвращается теплом победы прямо в батарейку. Цепь замкнута — сил стало БОЛЬШЕ!
          </div>
        </div>
      </div>

      <div class="hero-quote" style="font-size: 1.3vw; margin-top: 1.5vw;">
        «Батарейка человека садится не от созидательной работы. Она садится от разомкнутого контура — когда энергия вытекает в никуда».
      </div>
    </div>

    <div class="slide-footer">
      <div>Электродинамика действия</div>
      <div>Обратный провод реальности</div>
    </div>
  </section>


  <!-- ==================== СЛАЙД 8: ФИЗИКА ЛЮБВИ ==================== -->
  <section class="slide" id="slide-8">
    <div class="glow glow-amber"></div>
    <div class="slide-header">
      <div>
        <div class="badge-tag">Социология отношений</div>
        <div class="slide-title">Физика любви: <span>«Правило двух лучей»</span></div>
        <div class="slide-subtitle">Почему 90% пар выгорают в созависимости и как любить свободно</div>
      </div>
      <div class="slide-num">08 / 12</div>
    </div>

    <div class="slide-body">
      <div class="grid-2">
        <div class="card card-danger">
          <div class="card-title" style="color: #f87171;">⚠️ Созависимость (Война вампиров)</div>
          <div class="card-text" style="font-size: 1vw;">
            Два выключенных фонарика сидят на кухне и требуют:
            <br><br>
            • <em>«Освети меня! Развлеки меня!»</em><br>
            • <em>«Ты мало отдаёшь мне тепла!»</em><br>
            • <em>«Сделай меня счастливым!»</em><br><br>
            <strong>Итог:</strong> Попытка высосать чужую батарейку приводит к короткому замыканию и взаимным ожогам.
          </div>
        </div>

        <div class="card card-success">
          <div class="card-title" style="color: #4ade80;">🌟 Зрелая любовь (Два генератора)</div>
          <div class="card-text" style="font-size: 1vw;">
            Два автономных фонарика встречаются вместе:
            <br><br>
            • Каждый заряжен и полон сам по себе.<br>
            • Никто не клянчит чужой свет.<br>
            • Они встают рядом и <strong>светят в одну сторону</strong> — на общий дом, детей, проекты и жизнь.<br><br>
            <strong>Итог:</strong> Лучи соединяются — впереди в два раза светлее!
          </div>
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <div>Суверенные генераторы</div>
      <div>Любовь без паразитизма</div>
    </div>
  </section>


  <!-- ==================== СЛАЙД 9: МЫТЬЁ РУК ДЛЯ УМА ==================== -->
  <section class="slide" id="slide-9">
    <div class="glow glow-blue"></div>
    <div class="slide-header">
      <div>
        <div class="badge-tag">Экспресс-практика</div>
        <div class="slide-title">Мытьё рук для ума: <span>30-секундный протокол</span></div>
        <div class="slide-subtitle">Отмена культа многолетней вины и бесконечного копания в прошлом</div>
      </div>
      <div class="slide-num">09 / 12</div>
    </div>

    <div class="slide-body">
      <div class="grid-4">
        <div class="card">
          <div class="card-icon">🛑</div>
          <div class="card-title">1. СТОП</div>
          <div class="card-text">
            Опустите плечи. Разожмите челюсти. Не развивайте мысленный спор. Сделайте паузу.
          </div>
        </div>

        <div class="card">
          <div class="card-icon">🫁</div>
          <div class="card-title">2. ВДОХ В ЖИВОТ</div>
          <div class="card-text">
            Внимание в Тандэн (низ живота). Выдохните. Батарейка на месте, она полна энергии.
          </div>
        </div>

        <div class="card">
          <div class="card-icon">🧼</div>
          <div class="card-title">3. СБРОС ПЫЛИ</div>
          <div class="card-text">
            Стряхните пальцы: <em>«Обида и тревога — это налипшая грязь на стекле, а не мои провода»</em>.
          </div>
        </div>

        <div class="card card-highlight">
          <div class="card-icon">🔦</div>
          <div class="card-title">4. ЛУЧ ВПЕРЁД!</div>
          <div class="card-text">
            Нажмите «Щёлк!». Выберите одно реальное действие прямо сейчас и сделайте его.
          </div>
        </div>
      </div>

      <div class="hero-quote" style="font-size: 1.3vw; margin-top: 1.5vw;">
        «Вы же не изучаете историю пыли на руках 5 лет у терапевта перед тем, как пообедать? Вы просто моете руки тёплой водой. Точно так же мойте ум».
      </div>
    </div>

    <div class="slide-footer">
      <div>Санитарная гигиена сознания</div>
      <div>Регламент ежедневного ТО</div>
    </div>
  </section>


  <!-- ==================== СЛАЙД 10: ЭКСПЕРИМЕНТ В ЗАЛЕ ==================== -->
  <section class="slide" id="slide-10">
    <div class="glow glow-amber"></div>
    <div class="slide-header">
      <div>
        <div class="badge-tag">Живой интерактив</div>
        <div class="slide-title">Эксперимент: <span>Тайный свет антикафе</span></div>
        <div class="slide-subtitle">Наглядная физика прямо сейчас в полумраке зала</div>
      </div>
      <div class="slide-num">10 / 12</div>
    </div>

    <div class="slide-body">
      <div class="grid-3">
        <div class="card">
          <div class="card-icon">🌑</div>
          <div class="card-title">Шаг 1. Выключаем свет</div>
          <div class="card-text">
            Погружаем зал в полумрак. Все предметы вокруг — кружки с чаем, кресла, картины — становятся невидимыми и серыми.
          </div>
        </div>

        <div class="card card-highlight">
          <div class="card-icon">🔦</div>
          <div class="card-title">Шаг 2. Включаем луч</div>
          <div class="card-text">
            Спикер направляет узкий луч на обычную белую чашку. Она вспыхивает ярким сиянием! Вся комната видит её красоту.
          </div>
        </div>

        <div class="card card-success">
          <div class="card-title">👁️ Шаг 3. Инсайт момента</div>
          <div class="card-text">
            <strong>Чашка не светится сама.</strong> Но когда вы дарите ей своё внимание, она становится прекрасной. Так устроена вся ваша жизнь!
          </div>
        </div>
      </div>

      <div class="hero-quote" style="margin-top: 1.5vw;">
        «Ваша работа, ваш дом, ваши близкие — станут тёплыми и светлыми ровно в тот миг, когда вы перестанете ждать света от них и <span>включите свой собственный фонарик</span>».
      </div>
    </div>

    <div class="slide-footer">
      <div>Интерактивный опыт в реальном времени</div>
      <div>От абстракций к соматике</div>
    </div>
  </section>


  <!-- ==================== СЛАЙД 11: КОДЕКС ЧЕЛОВЕКА ==================== -->
  <section class="slide" id="slide-11">
    <div class="glow glow-blue"></div>
    <div class="slide-header">
      <div>
        <div class="badge-tag">Памятка на жизнь</div>
        <div class="slide-title">Кодекс Свободного Человека: <span>5 Аксиом</span></div>
        <div class="slide-subtitle">Инструкция, которую забыли приложить к нам при рождении</div>
      </div>
      <div class="slide-num">11 / 12</div>
    </div>

    <div class="slide-body">
      <div class="grid-2">
        <div class="card">
          <div style="font-size: 1.1vw; font-weight: 700; color: #f59e0b; margin-bottom: 0.3vw;">1. Я — сам источник света</div>
          <div class="card-text">Я не нищий в тёмной комнате. Моя батарейка в теле заряжена каждое утро.</div>
        </div>

        <div class="card">
          <div style="font-size: 1.1vw; font-weight: 700; color: #f59e0b; margin-bottom: 0.3vw;">2. Вещи — холодные</div>
          <div class="card-text">Радость не живёт в коробках, покупках и статусах. Они лишь отражают мой луч.</div>
        </div>

        <div class="card">
          <div style="font-size: 1.1vw; font-weight: 700; color: #f59e0b; margin-bottom: 0.3vw;">3. Луч светит только наружу</div>
          <div class="card-text">Я не выжигаю корпус вопросом «а как я выгляжу?». Я свечу на мир и людей.</div>
        </div>

        <div class="card">
          <div style="font-size: 1.1vw; font-weight: 700; color: #f59e0b; margin-bottom: 0.3vw;">4. Контур должен быть замкнут</div>
          <div class="card-text">Я не сливаю ток в пустые экраны. Я создаю реальные дела и забираю радость.</div>
        </div>
      </div>

      <div class="card card-highlight" style="margin-top: 1.2vw; text-align: center;">
        <div style="font-size: 1.2vw; font-weight: 800; color: #ffffff;">5. Дружба и любовь — это светить вместе на общую дорогу!</div>
      </div>
    </div>

    <div class="slide-footer">
      <div>Сверхпроводимость жизни</div>
      <div>Формула простого счастья</div>
    </div>
  </section>


  <!-- ==================== СЛАЙД 12: ФИНАЛ ==================== -->
  <section class="slide" id="slide-12">
    <div class="glow glow-amber"></div>
    <div class="glow glow-blue"></div>
    <div class="slide-header">
      <div>
        <div class="badge-tag">Открытый микрофон</div>
        <div class="slide-title">Чай, вопросы и <span>живой разговор</span></div>
      </div>
      <div class="slide-num">12 / 12</div>
    </div>

    <div class="slide-body" style="text-align: center; justify-content: center;">
      <div style="font-size: 3.5vw; margin-bottom: 1vw;">🔦✨</div>
      <h2 style="font-size: 2.8vw; font-weight: 800; margin-bottom: 1vw;">
        Включайте фонарики.<br>И не забывайте <span style="color: #f59e0b;">светить</span>!
      </h2>
      <p style="font-size: 1.3vw; color: #94a3b8; max-width: 60%; margin: 0 auto 2vw auto;">
        Спасибо за теплоту и внимание. Давайте обсудим ваши вопросы, ситуации и сомнения за чашкой чая.
      </p>

      <div style="display: inline-flex; gap: 2vw; background: rgba(17, 24, 39, 0.8); border: 1px solid rgba(255, 255, 255, 0.1); padding: 1vw 2vw; border-radius: 12px;">
        <div style="text-align: left;">
          <div style="font-size: 1vw; font-weight: 700; color: #ffffff;">Владимир Аньянов</div>
          <div style="font-size: 0.85vw; color: #f59e0b;">Автор Системы «Внутренний ток»</div>
        </div>
        <div style="border-left: 1px solid #334155; padding-left: 2vw; text-align: left;">
          <div style="font-size: 0.85vw; color: #94a3b8;">Материалы и книги:</div>
          <div style="font-size: 0.95vw; font-weight: 700; color: #38bdf8;">Внутренний ток · Архитектура прямого потока</div>
        </div>
      </div>
    </div>

    <div class="slide-footer">
      <div>Антикафе · Тёплый вечер воскресенья</div>
      <div>До новых встреч!</div>
    </div>
  </section>

</div>

<script>
  // Simple Keyboard Slide Navigation
  let currentSlide = 1;
  const totalSlides = 12;

  function scrollToSlide(index) {
    if (index < 1) index = 1;
    if (index > totalSlides) index = totalSlides;
    currentSlide = index;
    const el = document.getElementById(`slide-${index}`);
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  }

  window.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
      e.preventDefault();
      scrollToSlide(currentSlide + 1);
    } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
      e.preventDefault();
      scrollToSlide(currentSlide - 1);
    } else if (e.key === 'Home') {
      e.preventDefault();
      scrollToSlide(1);
    } else if (e.key === 'End') {
      e.preventDefault();
      scrollToSlide(totalSlides);
    } else if (e.key === 'f' || e.key === 'F') {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen();
      } else {
        document.exitFullscreen();
      }
    }
  });
</script>
</body>
</html>
"""

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"HTML saved to {OUTPUT_HTML}")

# Render 16:9 PDF with Playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"file:///{OUTPUT_HTML.replace(os.sep, '/')}")
    page.wait_for_load_state("networkidle")
    
    # 297mm x 167.0625mm is exact 16:9 landscape
    page.pdf(
        path=OUTPUT_PDF,
        width="297mm",
        height="167.0625mm",
        print_background=True,
        margin={"top": "0mm", "right": "0mm", "bottom": "0mm", "left": "0mm"}
    )
    
    # Take screenshot of Slide 1 and Slide 3 for quick visual check
    page.set_viewport_size({"width": 1920, "height": 1080})
    page.screenshot(path=r"C:\Users\vanya\Antigravity Projects\Apps\Inner Current\presentation\slide1_preview.png")
    
    browser.close()

reader = pypdf.PdfReader(OUTPUT_PDF)
print(f"Generated presentation PDF with {len(reader.pages)} slides successfully.")
