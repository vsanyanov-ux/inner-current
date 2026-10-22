import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 960" width="1200" height="960" style="background: #0d1322; font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;">
  <defs>
    <!-- Gradients -->
    <linearGradient id="skyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#080c18"/>
      <stop offset="100%" stop-color="#111827"/>
    </linearGradient>
    <linearGradient id="domeGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#818cf8" stop-opacity="0.35"/>
      <stop offset="100%" stop-color="#6366f1" stop-opacity="0.05"/>
    </linearGradient>
    <linearGradient id="wallGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#06b6d4" stop-opacity="0.15"/>
      <stop offset="100%" stop-color="#0891b2" stop-opacity="0.05"/>
    </linearGradient>
    <linearGradient id="baseGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#d97706" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#b45309" stop-opacity="0.4"/>
    </linearGradient>
    <radialGradient id="tandenGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#fef08a" stop-opacity="1"/>
      <stop offset="30%" stop-color="#f59e0b" stop-opacity="0.8"/>
      <stop offset="70%" stop-color="#b45309" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#78350f" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="beamGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#c084fc" stop-opacity="0.7"/>
      <stop offset="50%" stop-color="#818cf8" stop-opacity="0.3"/>
      <stop offset="100%" stop-color="#f59e0b" stop-opacity="0.6"/>
    </linearGradient>
    <linearGradient id="lanternBeam" x1="0%" y1="50%" x2="100%" y2="50%">
      <stop offset="0%" stop-color="#fef08a" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#f59e0b" stop-opacity="0"/>
    </linearGradient>
    
    <!-- Filter for glow -->
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="6" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>

  <!-- Background Blueprint Grid -->
  <rect width="1200" height="960" fill="url(#skyGrad)"/>
  <g stroke="#1e293b" stroke-width="0.6" opacity="0.6">
    <path d="M0 120 H1200 M0 240 H1200 M0 360 H1200 M0 480 H1200 M0 600 H1200 M0 720 H1200 M0 840 H1200"/>
    <path d="M150 0 V960 M300 0 V960 M450 0 V960 M600 0 V960 M750 0 V960 M900 0 V960 M1050 0 V960"/>
  </g>

  <!-- HEADER -->
  <text x="600" y="55" text-anchor="middle" fill="#f8fafc" font-size="24" font-weight="800" letter-spacing="2">ДОМ ВНУТРЕННЕГО ТОКА</text>
  <text x="600" y="82" text-anchor="middle" fill="#94a3b8" font-size="13" font-weight="500" letter-spacing="1">АРХИТЕКТУРНАЯ СХЕМА ОНТОЛОГИИ • «ЗОЛОТАЯ СЕМЁРКА 2.0»</text>

  <!-- CENTRAL VERTICAL AXIS / COSMIC FLOW BEAM -->
  <polygon points="585,90 615,90 640,730 560,730" fill="url(#beamGrad)" opacity="0.4"/>
  <line x1="600" y1="90" x2="600" y2="730" stroke="#c084fc" stroke-width="1.5" stroke-dasharray="4,4" opacity="0.8"/>

  <!-- ======================================================== -->
  <!-- 3. КРЫША И КУПОЛ (КНИГА 3: УНИВЕРСАЛЬНЫЙ ЗАКОН)          -->
  <!-- ======================================================== -->
  <g id="roof-section">
    <!-- Geodesic Dome -->
    <path d="M420 310 C420 180, 780 180, 780 310 Z" fill="url(#domeGrad)" stroke="#818cf8" stroke-width="2.5" filter="url(#glow)"/>
    <!-- Dome facets -->
    <path d="M420 310 Q600 190 780 310" stroke="#a5b4fc" stroke-width="1" fill="none" opacity="0.6"/>
    <path d="M480 310 Q600 220 720 310" stroke="#a5b4fc" stroke-width="1" fill="none" opacity="0.4"/>
    <line x1="600" y1="185" x2="600" y2="310" stroke="#a5b4fc" stroke-width="1.5" opacity="0.8"/>
    <line x1="500" y1="250" x2="700" y2="250" stroke="#a5b4fc" stroke-width="1" opacity="0.5"/>
    <line x1="450" y1="290" x2="750" y2="290" stroke="#a5b4fc" stroke-width="1" opacity="0.5"/>

    <!-- Overhanging Roof Eaves -->
    <polygon points="240,325 960,325 920,310 280,310" fill="#1e1b4b" stroke="#818cf8" stroke-width="2"/>

    <!-- CALLOUT BADGE: КНИГА 3 (КРЫША) -->
    <g transform="translate(850, 170)">
      <rect x="0" y="0" width="310" height="95" rx="10" fill="#1e1b4b" stroke="#818cf8" stroke-width="2" filter="url(#glow)"/>
      <circle cx="24" cy="28" r="12" fill="#6366f1"/>
      <text x="24" y="33" text-anchor="middle" fill="#ffffff" font-size="12" font-weight="800">3</text>
      <text x="48" y="28" fill="#c7d2fe" font-size="11" font-weight="700" letter-spacing="1">КРЫША И КОСМИЧЕСКИЙ КУПОЛ</text>
      <text x="48" y="48" fill="#ffffff" font-size="15" font-weight="800">Книга 3: Универсальный закон</text>
      <text x="16" y="70" fill="#94a3b8" font-size="11">Термодинамика негэнтропии, открытые</text>
      <text x="16" y="84" fill="#94a3b8" font-size="11">системы, Пригожин, КПД бытия (H = 1.0)</text>
      <line x1="0" y1="45" x2="-70" y2="45" stroke="#818cf8" stroke-width="1.5" stroke-dasharray="3,3"/>
      <circle cx="-70" cy="45" r="4" fill="#818cf8"/>
    </g>
  </g>

  <!-- ======================================================== -->
  <!-- 2. СТЕНЫ И КОМНАТЫ (КНИГА 2: ЧЕТВЕРИЧНЫЙ ФРАКТАЛ)        -->
  <!-- ======================================================== -->
  <g id="walls-section">
    <!-- Main Living Pavilion Box -->
    <rect x="280" y="325" width="640" height="280" fill="url(#wallGrad)" stroke="#06b6d4" stroke-width="2"/>
    
    <!-- 4 INVARIANT PILLARS (COLUMNS) -->
    <!-- Pillar 1: Source -->
    <rect x="300" y="325" width="18" height="280" fill="#0e7490" stroke="#22d3ee" stroke-width="1.5"/>
    <text x="309" y="470" text-anchor="middle" fill="#e0f2fe" font-size="9" font-weight="700" transform="rotate(-90 309 470)">1. ИСТОЧНИК (ЭДС)</text>
    
    <!-- Pillar 2: Conductor -->
    <rect x="480" y="325" width="14" height="280" fill="#0e7490" stroke="#22d3ee" stroke-width="1" opacity="0.8"/>
    <text x="487" y="470" text-anchor="middle" fill="#e0f2fe" font-size="9" font-weight="700" transform="rotate(-90 487 470)">2. ПРОВОДНИК (МУСИН)</text>
    
    <!-- Pillar 3: Load -->
    <rect x="700" y="325" width="14" height="280" fill="#0e7490" stroke="#22d3ee" stroke-width="1" opacity="0.8"/>
    <text x="707" y="470" text-anchor="middle" fill="#e0f2fe" font-size="9" font-weight="700" transform="rotate(-90 707 470)">3. НАГРУЗКА (ДЕЛО)</text>
    
    <!-- Pillar 4: Return Wire -->
    <rect x="882" y="325" width="18" height="280" fill="#0e7490" stroke="#22d3ee" stroke-width="1.5"/>
    <text x="891" y="470" text-anchor="middle" fill="#e0f2fe" font-size="9" font-weight="700" transform="rotate(-90 891 470)">4. ОБРАТНЫЙ ПРОВОД (ДЗАНСИН)</text>

    <!-- CALLOUT BADGE: КНИГА 2 (СТЕНЫ) -->
    <g transform="translate(40, 360)">
      <rect x="0" y="0" width="310" height="95" rx="10" fill="#083344" stroke="#06b6d4" stroke-width="2" filter="url(#glow)"/>
      <circle cx="24" cy="28" r="12" fill="#0284c7"/>
      <text x="24" y="33" text-anchor="middle" fill="#ffffff" font-size="12" font-weight="800">2</text>
      <text x="48" y="28" fill="#67e8f9" font-size="11" font-weight="700" letter-spacing="1">СТЕНЫ И НЕСУЩИЙ КАРКАС</text>
      <text x="48" y="48" fill="#ffffff" font-size="15" font-weight="800">Книга 2: Четверичный фрактал</text>
      <text x="16" y="70" fill="#94a3b8" font-size="11">4 узла (C4), масштабы от клетки до Биткоина,</text>
      <text x="16" y="84" fill="#94a3b8" font-size="11">P2P-общество, депосреднизация (Zero Rent)</text>
      <line x1="310" y1="45" x2="360" y2="45" stroke="#06b6d4" stroke-width="1.5" stroke-dasharray="3,3"/>
      <circle cx="360" cy="45" r="4" fill="#06b6d4"/>
    </g>

    <!-- INTERIOR ROOMS & ARTIFACTS ("И ТАК ДАЛЕЕ") -->
    <!-- Room A: Книга 6 - Музыкальная гостиная (Укулеле) -->
    <g transform="translate(515, 345)">
      <rect x="0" y="0" width="165" height="95" rx="6" fill="#713f12" fill-opacity="0.3" stroke="#eab308" stroke-width="1.2"/>
      <text x="82" y="22" text-anchor="middle" fill="#fef08a" font-size="11" font-weight="800">Книга 6: Укулеле Бытия</text>
      <text x="82" y="40" text-anchor="middle" fill="#fef08a" font-size="9" opacity="0.8">Музыкальная гостиная</text>
      <!-- Mini ukulele icon -->
      <circle cx="82" cy="65" r="10" fill="#ca8a04" stroke="#fef08a" stroke-width="1"/>
      <line x1="82" y1="55" x2="82" y2="45" stroke="#fef08a" stroke-width="2"/>
      <text x="82" y=\"85\" text-anchor="middle" fill="#fef9c3" font-size="8">Акустика и резонанс Мусин</text>
    </g>

    <!-- Room B: Книга 7 - Библиотека / Летопись (Великий Синтез) -->
    <g transform="translate(735, 345)">
      <rect x="0" y="0" width="135" height="115" rx="6" fill="#4c0519" fill-opacity="0.3" stroke="#f43f5e" stroke-width="1.2"/>
      <text x="67" y="22" text-anchor="middle" fill="#fecdd3" font-size="11" font-weight="800">Книга 7: Великий</text>
      <text x="67" y="36" text-anchor="middle" fill="#fecdd3" font-size="11" font-weight="800">Синтез</text>
      <text x="67" y="54" text-anchor="middle" fill="#fda4af" font-size="9">Библиотека и архив</text>
      <text x="67" y="75" text-anchor="middle" fill="#cbd5e1" font-size="8">2500 лет сборки цепи</text>
      <text x="67" y="88" text-anchor="middle" fill="#cbd5e1" font-size="8">Восток vs Запад</text>
      <text x="67" y="101" text-anchor="middle" fill="#cbd5e1" font-size="8">Дзен + Пригожин</text>
    </g>

    <!-- Room C: Книга 4 - Детская комната (Тайна фонарика) -->
    <g transform="translate(335, 345)">
      <rect x="0" y="0" width="130" height="100" rx="6" fill="#7c2d12" fill-opacity="0.3" stroke="#f97316" stroke-width="1.2"/>
      <text x="65" y="22" text-anchor="middle" fill="#fed7aa" font-size="11" font-weight="800">Книга 4: Тайна</text>
      <text x="65" y="36" text-anchor="middle" fill="#fed7aa" font-size="11" font-weight="800">фонарика</text>
      <text x="65" y="54" text-anchor="middle" fill="#fdba74" font-size="9">Детская комната</text>
      <text x="65" y="75" text-anchor="middle" fill="#ffedd5" font-size="8">Как устроена твоя</text>
      <text x="65" y="88" text-anchor="middle" fill="#ffedd5" font-size="8">суперсила (10+ лет)</text>
    </g>

    <!-- Room D: Книга 5 - Аптечка первой помощи (Полевой мануал) -->
    <g transform="translate(515, 475)">
      <rect x="0" y="0" width="165" height="80" rx="6" fill="#064e3b" fill-opacity="0.3" stroke="#10b981" stroke-width="1.2"/>
      <text x="82" y="20" text-anchor="middle" fill="#a7f3d0" font-size="11" font-weight="800">Книга 5: Мануал</text>
      <text x="82" y="35" text-anchor="middle" fill="#6ee7b7" font-size="9">Аптечка в прихожей</text>
      <text x="82" y="54" text-anchor="middle" fill="#d1fae5" font-size="8">30-секундный протокол</text>
      <text x="82" y="68" text-anchor="middle" fill="#d1fae5" font-size="8">соматической отладки</text>
    </g>
  </g>

  <!-- ======================================================== -->
  <!-- 1. ОСНОВАНИЕ / ФУНДАМЕНТ (КНИГА 1: ВНУТРЕННИЙ ТОК)      -->
  <!-- ======================================================== -->
  <g id="foundation-section">
    <!-- Solid Monolithic Foundation Base -->
    <rect x="220" y="605" width="760" height="175" fill="url(#baseGrad)" stroke="#d97706" stroke-width="2.5" filter="url(#glow)"/>
    
    <!-- Stone texture lines -->
    <line x1="220" y1="660" x2="980" y2="660" stroke="#78350f" stroke-width="1.5" opacity="0.6"/>
    <line x1="220" y1="720" x2="980" y2="720" stroke="#78350f" stroke-width="1.5" opacity="0.6"/>
    <line x1="450" y1="605" x2="450" y2="660" stroke="#78350f" stroke-width="1.5" opacity="0.6"/>
    <line x1="750" y1="605" x2="750" y2="660" stroke="#78350f" stroke-width="1.5" opacity="0.6"/>
    <line x1="600" y1="660" x2="600" y2="720" stroke="#78350f" stroke-width="1.5" opacity="0.6"/>
    <line x1="380" y1="720" x2="380" y2="780" stroke="#78350f" stroke-width="1.5" opacity="0.6"/>
    <line x1="820" y1="720" x2="820" y2="780" stroke="#78350f" stroke-width="1.5" opacity="0.6"/>

    <!-- THE TANDEN REACTOR CORE (GLOWING SPHERE) -->
    <circle cx="600" cy="690" r="55" fill="url(#tandenGlow)"/>
    <circle cx="600" cy="690" r="26" fill="#fef08a" stroke="#f59e0b" stroke-width="3" filter="url(#glow)"/>
    <text x="600" y="694" text-anchor="middle" fill="#78350f" font-size="11" font-weight="900">ТАНДЭН</text>

    <!-- FOCUSED LANTERN BEAM ON PEDESTAL -->
    <g transform="translate(250, 640)">
      <rect x="0" y="30" width="24" height="45" fill="#334155" stroke="#64748b" stroke-width="1"/>
      <path d="M-4 30 L28 30 L20 15 L4 15 Z" fill="#f59e0b" stroke="#fbbf24" stroke-width="1"/>
      <!-- Horizontal Beam -->
      <polygon points="26,20 200,-10 200,60 26,30" fill="url(#lanternBeam)" opacity="0.85"/>
      <text x="12" y="88" text-anchor="middle" fill="#fde047" font-size="9" font-weight="700">Фонарик</text>
    </g>

    <!-- CALLOUT BADGE: КНИГА 1 (ФУНДАМЕНТ) -->
    <g transform="translate(850, 645)">
      <rect x="0" y="0" width="310" height="95" rx="10" fill="#451a03" stroke="#f59e0b" stroke-width="2" filter="url(#glow)"/>
      <circle cx="24" cy="28" r="12" fill="#d97706"/>
      <text x="24" y="33" text-anchor="middle" fill="#ffffff" font-size="12" font-weight="800">1</text>
      <text x="48" y="28" fill="#fde68a" font-size="11" font-weight="700" letter-spacing="1">ОСНОВАНИЕ И ФУНДАМЕНТ</text>
      <text x="48" y="48" fill="#ffffff" font-size="15" font-weight="800">Книга 1: Внутренний ток</text>
      <text x="16" y="70" fill="#94a3b8" font-size="11">Архитектура человека (N=1), Тандэн, Мусин,</text>
      <text x="16" y="84" fill="#94a3b8" font-size="11">схемотехника фонарика, ликвидация выгорания</text>
      <line x1="0" y1="45" x2="-65" y2="45" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="3,3"/>
      <circle cx="-65" cy="45" r="4" fill="#f59e0b"/>
    </g>
  </g>

  <!-- GROUND / WATER BEDROCK -->
  <g id="ground">
    <rect x="100" y="780" width="1000" height="80" rx="8" fill="#090d16" stroke="#334155" stroke-width="1.5"/>
    <text x="600" y="825" text-anchor="middle" fill="#64748b" font-size="12" font-weight="600" letter-spacing="2">ЗЕМЛЯ И СЕНСОРНАЯ ОБРАТНАЯ СВЯЗЬ РЕАЛЬНОСТИ • СОМАТИЧЕСКОЕ ЗАЗЕМЛЕНИЕ</text>
  </g>

  <!-- FOOTER SUMMARY LEGEND -->
  <g transform="translate(150, 880)">
    <rect x="0" y="0" width="900" height="55" rx="8" fill="#111827" stroke="#1f2937" stroke-width="1"/>
    <text x="30" y="32" fill="#e2e8f0" font-size="12" font-weight="700">КЛЮЧ ДОМА:</text>
    <circle cx="130" cy="28" r="5" fill="#f59e0b"/>
    <text x="142" y="32" fill="#cbd5e1" font-size="11">1. Фундамент (Человек N=1)</text>
    <circle cx="340" cy="28" r="5" fill="#06b6d4"/>
    <text x="352" y="32" fill="#cbd5e1" font-size="11">2. Стены (Фрактал C4)</text>
    <circle cx="530" cy="28" r="5" fill="#818cf8"/>
    <text x="542" y="32" fill="#cbd5e1" font-size="11">3. Крыша (Закон систем)</text>
    <circle cx="720" cy="28" r="5" fill="#10b981"/>
    <text x="732" y="32" fill="#cbd5e1" font-size="11">4-7. Комнаты и Летопись</text>
  </g>
</svg>"""

p_svg_brain = r'C:\Users\vanya\.gemini\antigravity\brain\00695de1-489c-4545-976e-b3329c001a98\house_schematic.svg'
p_svg_lib = r'c:\Users\vanya\Antigravity Projects\Apps\Inner Current\IC Library\Золотая семерка 2.0\Схема Дома Внутреннего Тока.svg'
p_svg_vault = r'C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\00_Attachments\Схема Дома Внутреннего Тока.svg'

for p in [p_svg_brain, p_svg_lib, p_svg_vault]:
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    print(f'Wrote SVG to: {p}')

# Convert to PNG using Playwright
png_brain = r'C:\Users\vanya\.gemini\antigravity\brain\00695de1-489c-4545-976e-b3329c001a98\house_schematic.png'
png_lib = r'c:\Users\vanya\Antigravity Projects\Apps\Inner Current\IC Library\Золотая семерка 2.0\Схема Дома Внутреннего Тока.png'
png_vault = r'C:\Users\vanya\Antigravity Projects\Misc\LLM Wiki\00_Attachments\Схема Дома Внутреннего Тока.png'

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1200, "height": 960})
    page.set_content(svg_content)
    page.screenshot(path=png_brain)
    page.screenshot(path=png_lib)
    page.screenshot(path=png_vault)
    browser.close()

print('Successfully rendered PNG screenshots!')
