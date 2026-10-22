import os
import pypdf
from playwright.sync_api import sync_playwright

OUTPUT_HTML = r"C:\Users\vanya\Antigravity Projects\Apps\Inner Current\presentation\flashlight_one_pager.html"
OUTPUT_PDF = r"C:\Users\vanya\Antigravity Projects\Apps\Inner Current\IC Library\Одностраничник — Тайна карманного фонарика (Школа креативных индустрий).pdf"
OUTPUT_PNG = r"C:\Users\vanya\Antigravity Projects\Apps\Inner Current\presentation\flashlight_one_pager.png"

html_content = """<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>Тайна карманного фонарика — Лекция для Школы Креативных Индустрий</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap');

  @page {
    size: A4 portrait;
    margin: 12mm 14mm 12mm 14mm;
  }

  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  html, body {
    height: 100%;
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: #ffffff;
    color: #0f172a;
    font-size: 12px;
    line-height: 1.45;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  .page-container {
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  /* HEADER */
  .header {
    border-bottom: 2.5px solid #0f172a;
    padding-bottom: 12px;
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }

  .badge-row {
    display: flex;
    gap: 8px;
    margin-bottom: 6px;
  }

  .badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9.5px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: 3px 8px;
    border-radius: 4px;
  }

  .badge-primary {
    background: #0f172a;
    color: #ffffff;
  }

  .badge-accent {
    background: #e0f2fe;
    color: #0369a1;
    border: 1px solid #bae6fd;
  }

  .badge-warm {
    background: #fef3c7;
    color: #92400e;
    border: 1px solid #fde68a;
  }

  .title {
    font-size: 24px;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.6px;
    line-height: 1.15;
  }

  .subtitle {
    font-size: 13px;
    font-weight: 600;
    color: #475569;
    margin-top: 3px;
  }

  .speaker-box {
    text-align: right;
    font-size: 10.5px;
    color: #334155;
    border-left: 2px solid #cbd5e1;
    padding-left: 14px;
    line-height: 1.35;
  }

  .speaker-name {
    font-weight: 800;
    font-size: 13px;
    color: #0f172a;
  }

  .speaker-tag {
    color: #2563eb;
    font-weight: 700;
  }

  /* WHY & CONTEXT */
  .intro-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-left: 5px solid #2563eb;
    border-radius: 8px;
    padding: 10px 14px;
    margin-bottom: 12px;
    font-size: 11.5px;
    line-height: 1.5;
    color: #1e293b;
  }

  .intro-card strong {
    color: #0f172a;
  }

  /* CORE PILLARS */
  .section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #64748b;
    margin-bottom: 7px;
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .section-label::after {
    content: "";
    flex: 1;
    height: 1px;
    background: #e2e8f0;
  }

  .pillars-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-bottom: 12px;
  }

  .pillar-card {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 8px;
    padding: 10px 11px;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
  }

  .pillar-header {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 6px;
  }

  .pillar-icon {
    font-size: 16px;
  }

  .pillar-title {
    font-weight: 800;
    font-size: 12px;
    color: #0f172a;
    line-height: 1.25;
  }

  .pillar-text {
    font-size: 10.5px;
    color: #475569;
    line-height: 1.45;
  }

  .pillar-text strong {
    color: #0f172a;
  }

  /* DIAGRAM STRIP */
  .circuit-strip {
    background: #0f172a;
    color: #ffffff;
    border-radius: 8px;
    padding: 11px 14px;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .circuit-step {
    text-align: center;
    flex: 1;
  }

  .circuit-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .circuit-val {
    font-weight: 800;
    font-size: 11.5px;
    color: #38bdf8;
    margin-top: 2px;
  }

  .circuit-desc {
    font-size: 9.5px;
    color: #cbd5e1;
    margin-top: 2px;
  }

  .circuit-arrow {
    color: #64748b;
    font-size: 14px;
    font-weight: 700;
    padding: 0 4px;
  }

  /* PROGRAM / AGENDA & OUTCOMES */
  .two-col-grid {
    display: grid;
    grid-template-columns: 1.25fr 1fr;
    gap: 11px;
    margin-bottom: 12px;
  }

  .agenda-box {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 10px 12px;
  }

  .timeline-item {
    display: flex;
    gap: 8px;
    margin-bottom: 6px;
    align-items: flex-start;
  }

  .timeline-item:last-child {
    margin-bottom: 0;
  }

  .time-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    font-weight: 700;
    background: #f1f5f9;
    color: #334155;
    padding: 2px 5px;
    border-radius: 4px;
    white-space: nowrap;
    border: 1px solid #e2e8f0;
  }

  .timeline-desc {
    font-size: 10.5px;
    line-height: 1.4;
    color: #334155;
  }

  .timeline-desc strong {
    color: #0f172a;
  }

  .outcomes-box {
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-radius: 8px;
    padding: 10px 12px;
  }

  .outcomes-list {
    list-style: none;
  }

  .outcomes-item {
    font-size: 10.5px;
    line-height: 1.45;
    color: #166534;
    margin-bottom: 6px;
    position: relative;
    padding-left: 14px;
  }

  .outcomes-item:last-child {
    margin-bottom: 0;
  }

  .outcomes-item::before {
    content: "✓";
    position: absolute;
    left: 0;
    top: 0;
    font-weight: 800;
    color: #16a34a;
  }

  .outcomes-item strong {
    color: #14532d;
  }

  /* QUOTE & INTERACTIVE HOOK STRIP */
  .hook-strip {
    background: #fffbeb;
    border: 1px solid #fde68a;
    border-radius: 8px;
    padding: 9px 12px;
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
  }

  .hook-text {
    font-size: 10.5px;
    color: #78350f;
    line-height: 1.4;
  }

  .hook-text strong {
    color: #451a03;
  }

  .hook-prop {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9.5px;
    font-weight: 700;
    background: #fef3c7;
    border: 1px solid #fcd34d;
    padding: 4px 8px;
    border-radius: 6px;
    color: #b45309;
    white-space: nowrap;
  }

  /* FOOTER */
  .footer {
    border-top: 1.5px solid #0f172a;
    padding-top: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 10.5px;
    color: #475569;
  }

  .footer-left {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .footer-tag {
    font-weight: 800;
    color: #0f172a;
  }

  .contact-pill {
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    background: #0f172a;
    color: #ffffff;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 10px;
  }
</style>
</head>
<body>
<div class="page-container">

  <!-- HEADER -->
  <div class="header">
    <div>
      <div class="badge-row">
        <span class="badge badge-primary">Школа Креативных Индустрий</span>
        <span class="badge badge-accent">Предложение открытой лекции-воркшопа</span>
        <span class="badge badge-warm">Для студийцев 10–17 лет</span>
      </div>
      <div class="title">Тайна Карманного Фонарика: Архитектура Радости</div>
      <div class="subtitle">Инженерная физика внимания, креативности и уверенности на стыке технологий, AI и социологии</div>
    </div>
    <div class="speaker-box">
      <div class="speaker-name">Владимир Аньянов</div>
      <div class="speaker-tag">Экс-преподаватель ИИ в ШКИ</div>
      <div>Автор прикладной онтологии сознания</div>
    </div>
  </div>

  <!-- INTRO CONTEXT -->
  <div class="intro-card">
    <strong>🎯 Почему эта лекция актуальна именно для воспитанников ШКИ:</strong> Студийцы виртуозно осваивают софт, нейросети, 3D-графику, саунд-дизайн и код. Но будучи творческими подростками, они первыми упираются в невидимые преграды: <em>страх белого листа, синдром самозванца («а вдруг я хуже других?»), экранное выгорание и конфликты в командах</em>. Мы снимем эти барьеры не скучными поучениями, а через <strong>точную технологическую схемотехнику человека</strong>, говоря с ребятами на одном инженерном языке.
  </div>

  <!-- THREE PILLARS -->
  <div class="section-label">Ключевые концепции лекции (стык технологий и психологии)</div>
  <div class="pillars-grid">
    <div class="pillar-card">
      <div class="pillar-header">
        <span class="pillar-icon">🔦</span>
        <div class="pillar-title">1. Разоблачение «Холодных Игрушек»</div>
      </div>
      <div class="pillar-text">
        В нейросетях <em>Attention</em> — это направленный математический луч. В человеке — то же самое! Figma, планшет, блендер или новая игра — <strong>холодные предметы</strong>, в них нет радости. Радость рождается из луча собственного внимания, отражающегося от созданного проекта.
      </div>
    </div>

    <div class="pillar-card">
      <div class="pillar-header">
        <span class="pillar-icon">⚡</span>
        <div class="pillar-title">2. Закон Прямого Луча и Мусин</div>
      </div>
      <div class="pillar-text">
        Главная причина творческого ступора — попытка <strong>светить внутрь себя</strong>: <em>«А я крутой? А не засмеют ли меня?»</em>. Процессор перегревается, а дороги не видно. Мы учим переводить внимание в чистый ток (Мусин): светить строго на холст, код и инструмент.
      </div>
    </div>

    <div class="pillar-card">
      <div class="pillar-header">
        <span class="pillar-icon">🤝</span>
        <div class="pillar-title">3. Правило Двух Лучей в Команде</div>
      </div>
      <div class="pillar-text">
        Социология созидателей: почему командные проекты рушатся, когда участники требуют «светите на меня!». Настоящая коллаборация — когда <strong>два суверенных фонарика соединяют лучи</strong> на общем сложном проекте, удваивая яркость и результат.
      </div>
    </div>
  </div>

  <!-- CIRCUIT DIAGRAM STRIP -->
  <div class="section-label">Принципиальная схема прибора человека (на языке систем)</div>
  <div class="circuit-strip">
    <div class="circuit-step">
      <div class="circuit-label">Узел 1</div>
      <div class="circuit-val">🔋 Батарейка</div>
      <div class="circuit-desc">Тело и дыхание · Заряд > 0 всегда</div>
    </div>
    <div class="circuit-arrow">→</div>
    <div class="circuit-step">
      <div class="circuit-label">Узел 2</div>
      <div class="circuit-val">🔘 Кнопка «Щёлк!»</div>
      <div class="circuit-desc">Фокус в t = сейчас · Режим 0 / 1</div>
    </div>
    <div class="circuit-arrow">→</div>
    <div class="circuit-step">
      <div class="circuit-label">Узел 3</div>
      <div class="circuit-val">⚡ Ток Мусин</div>
      <div class="circuit-desc">Внимание без ржавчины и страха</div>
    </div>
    <div class="circuit-arrow">→</div>
    <div class="circuit-step">
      <div class="circuit-label">Узел 4</div>
      <div class="circuit-val">💡 Лампочка</div>
      <div class="circuit-desc">Действие · Арт, код, трек, дизайн</div>
    </div>
    <div class="circuit-arrow">═►</div>
    <div class="circuit-step">
      <div class="circuit-label">Результат</div>
      <div class="circuit-val">🌍 Замкнутый Контур</div>
      <div class="circuit-desc">Отражённая радость и победа</div>
    </div>
  </div>

  <!-- PROGRAM & OUTCOMES (2 COLUMNS) -->
  <div class="two-col-grid">
    <div class="agenda-box">
      <div class="section-label" style="margin-bottom: 7px;">Сценарий встречи (45–50 минут)</div>
      
      <div class="timeline-item">
        <span class="time-badge">00–10'</span>
        <div class="timeline-desc"><strong>Интерактивный хук:</strong> «Где прячется кайф от игры?» Эксперимент с холодной коробкой и природой детского счастья.</div>
      </div>
      <div class="timeline-item">
        <span class="time-badge">10–25'</span>
        <div class="timeline-desc"><strong>Технологический разбор:</strong> Человек как фонарик. Как ток внимания превращается в шедевр или в омический ступор.</div>
      </div>
      <div class="timeline-item">
        <span class="time-badge">25–35'</span>
        <div class="timeline-desc"><strong>Практикум «Мытьё рук для ума»:</strong> 30-секундный соматический протокол снятия страха перед сценой и защитой проекта.</div>
      </div>
      <div class="timeline-item">
        <span class="time-badge">35–50'</span>
        <div class="timeline-desc"><strong>Открытый микрофон & Q&A:</strong> Честный диалог на равных о творчестве, сомнениях и будущем в мире генеративного ИИ.</div>
      </div>
    </div>

    <div class="outcomes-box">
      <div class="section-label" style="color: #15803d; margin-bottom: 7px;">Что получат учащиеся и Школа</div>
      
      <ul class="outcomes-list">
        <li class="outcomes-item"><strong>Снятие страха публичной защиты:</strong> Чит-код мгновенной фокусировки внимания перед выходом к доске или экспертному жюри.</li>
        <li class="outcomes-item"><strong>Иммунитет к цифровому выгоранию:</strong> Понимание, почему думскроллинг истощает, а прямое созидание заряжает энергией.</li>
        <li class="outcomes-item"><strong>Усиление командных проектов:</strong> Ликвидация токсичных споров в студиях через принцип «Правила двух лучей».</li>
        <li class="outcomes-item"><strong>Мост между технологиями и духом:</strong> Осознание ценности человека как живого автора в эпоху всемогущих нейросетей.</li>
      </ul>
    </div>
  </div>

  <!-- INTERACTIVE PROPS & HOOK -->
  <div class="hook-strip">
    <div class="hook-text">
      <strong>✨ Интерактивный реквизит лекции:</strong> В зал приносится настоящий мощный фонарик. Короткий 3-минутный эксперимент в полумраке наглядно показывает разницу между отражённым и прямым светом. Ребята понимают суть мгновенно и без лекционной скуки.
    </div>
    <div class="hook-prop">
      Формат: Живой эксперимент
    </div>
  </div>

  <!-- FOOTER -->
  <div class="footer">
    <div class="footer-left">
      <span class="footer-tag">Организация:</span> Очная интерактивная лекция в актовом зале / медиа-лектории ШКИ
      <span style="color: #cbd5e1;">|</span>
      <span>Свободный вход для студийцев и педагогов</span>
    </div>
    <div class="contact-pill">
      Спикер: Владимир Аньянов
    </div>
  </div>

</div>
</body>
</html>
"""

with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(html_content)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"file:///{OUTPUT_HTML.replace(os.sep, '/')}")
    page.wait_for_load_state("networkidle")
    
    page.pdf(
        path=OUTPUT_PDF,
        format="A4",
        print_background=True,
        margin={"top": "12mm", "right": "14mm", "bottom": "12mm", "left": "14mm"}
    )
    
    page.set_viewport_size({"width": 794, "height": 1123})
    page.screenshot(path=OUTPUT_PNG)
    browser.close()

reader = pypdf.PdfReader(OUTPUT_PDF)
num_pages = len(reader.pages)
if num_pages == 1:
    print("SUCCESS: Strictly 1 page!")
else:
    print(f"WARNING: Overflow! Total pages: {num_pages}")
