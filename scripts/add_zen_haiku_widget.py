import json
import re

# Haiku catalogue for client-side widget
haikus = [
  {
    "id": "basho-cold-rain",
    "author": "Басё (Basho)",
    "authorKanji": "松尾芭蕉",
    "haikuOriginal": "A COLD RAIN STARTING,\nAND ME WITHOUT A HAT.\nON SECOND THOUGHT, WHO CARES?",
    "haikuRu": "Холодный дождь пошёл,\nА я без шляпы...\nВпрочем, какое мне до этого дело?",
    "theme": "Мгновенный сброс эго-сопротивления",
    "felineCircuitComment": "Кот выходит на веранду под моросящий дождь. Никаких жалоб на климат, никакого самобичевания: уши прижаты, лапы пружинят, сопротивление R_ego мгновенно обнулено. Мокрая шерсть — это просто физика, а не трагедия.",
    "electrodynamicFormula": "R_ego: 100 Ω → 0 Ω за 0.05 с, Q_joule = 0",
    "somaticCalibration": "Разомкните зубы, сбросьте плечи вниз и спросите себя: «Какое мне до этого дело?» Почувствуйте, как уходит спазм со скул."
  },
  {
    "id": "ryokan-the-thief",
    "author": "Рёкан (Ryokan)",
    "authorKanji": "良寛",
    "haikuOriginal": "THE THIEF\nLEFT IT BEHIND —\nTHE MOON AT THE WINDOW.",
    "haikuRu": "Вор оставил её\nНетронутой —\nЛуна в окне.",
    "theme": "Неуязвимость пустой полости (Шуньята)",
    "felineCircuitComment": "Вор обчистил хижину монаха, но кот продолжает дремать на подоконнике в пятне лунного света. Нельзя украсть то, за что ты не цепляешься когтями. Лунный свет принадлежит коту целиком, потому что кот пуст.",
    "electrodynamicFormula": "E_load = 0, Z_0 = const, I_theft = 0",
    "somaticCalibration": "Положите ладонь на живот под пупком. Выдохните всё имущество и тревогу. Внутренний свет украсть невозможно."
  },
  {
    "id": "ryokan-stretched-out",
    "author": "Рёкан (Ryokan)",
    "authorKanji": "良寛",
    "haikuOriginal": "FORGETTING THE EQUAL DUSTS OF NAME AND FORTUNE,\nLISTENING TO THE NIGHT RAIN ON THE ROOF OF MY HUT,\nI SIT AT EASE,\nBOTH LEGS STRETCHED OUT.",
    "haikuRu": "Забыв одинаковую пыль славы и богатства,\nСлушаю ночной дождь по крыше хижины,\nСижу в полном покое,\nВытянув обе ноги.",
    "theme": "Соматическая капитуляция в Тандэн",
    "felineCircuitComment": "Кот лежит на спине посреди ковра, раскинув лапы в форме звезды, подставив теплому воздуху беззащитное брюхо. Абсолютное доверие к несущей среде: социальный радар выключен, ток течет без омического сопротивления.",
    "electrodynamicFormula": "R_ego = 0, η = 100%, P_dissipated = 0",
    "somaticCalibration": "Вытяните ноги, размягчите живот так, чтобы он колыхался при дыхании. Пусть шум мира станет шелестом дождя по соломе."
  },
  {
    "id": "basho-wild-violet",
    "author": "Басё (Basho)",
    "authorKanji": "松尾芭蕉",
    "haikuOriginal": "ALONG THE MOUNTAIN ROAD\nSOMEHOW IT TUGS AT MY HEART:\nA WILD VIOLET.",
    "haikuRu": "Вдоль горной дороги\nЧто-то тронуло сердце:\nДикая фиалка.",
    "theme": "Сверхпроводимость эстетического резонанса",
    "felineCircuitComment": "Кот замирает перед трепещущим листком папоротника. Никакой утилитарной цели: листок несъедобен, за него не дадут мышь. Но внимание кота целокупно и бесконечно. Контур замкнут через красоту момента.",
    "electrodynamicFormula": "Z_in = Z_load (Идеальное согласование импедансов)",
    "somaticCalibration": "Остановите взгляд на любой случайной детали: узоре дерева, блике света на столе. Смотрите без названия 10 секунд."
  },
  {
    "id": "issa-dewdrop-world",
    "author": "Исса (Issa)",
    "authorKanji": "小林一茶",
    "haikuOriginal": "THIS DEWDROP WORLD —\nIT MAY BE A DEWDROP,\nAND YET ... AND YET ...",
    "haikuRu": "Этот мир — капля росы.\nПусть всего лишь капля росы,\nИ все же... и все же...",
    "theme": "Нежность к хрупкости бытия (Гальваническая развязка)",
    "felineCircuitComment": "Кот смотрит на тающую снежинку на кончике собственного носа. Она исчезнет через миг. Дзэн не требует быть каменным истуканом; дзэн позволяет любить каплю росы, не пытаясь запаять ее в сейф.",
    "electrodynamicFormula": "M_ind > 0, без короткого замыкания созависимости",
    "somaticCalibration": "Позвольте себе почувствовать грусть или нежность без попытки их исправить или подавить. Дайте току просто протечь."
  },
  {
    "id": "basho-cicada-shell",
    "author": "Басё (Basho)",
    "authorKanji": "松尾芭蕉",
    "haikuOriginal": "ONLY THE SHELL\nOF THE CICADA LEFT?\nDID IT SING ITSELF OUT OF EXISTENCE?",
    "haikuRu": "Только сухая скорлупка\nОсталась от цикады?\nНеужели она выпела себя из бытия?",
    "theme": "Предельная отдача в нагрузку (100% КПД)",
    "felineCircuitComment": "Кот, преследующий солнечный зайчик, отдает броску всю свою кошачью массу, до кончика вибрирующего хвоста. Никаких резервов на завтра, никакого сомнения. Спеть себя без остатка — единственный способ победить смерть.",
    "electrodynamicFormula": "η = P_out / P_in = 1.0, W_useful = max",
    "somaticCalibration": "Если делаете что-то прямо сейчас (пьете чай, пишете код, гладите кота) — погрузитесь в это так, будто завтра не существует."
  },
  {
    "id": "zen-expression-grass",
    "author": "Дзэнский канон",
    "authorKanji": "禅",
    "haikuOriginal": "ENTERING THE FOREST,\nHE MOVES NOT THE GRASS.\nENTERING THE WATER,\nHE MAKES NOT A RIPPLE.",
    "haikuRu": "Входя в густой лес,\nНе колыхнет травинку.\nВступая в воду,\nНе поднимет ряби.",
    "theme": "Ламинарный ток без омического следа",
    "felineCircuitComment": "Черный кот бесшумно ступает мягкими подушечками по скрипучему паркету старого дома. Ни звука когтей, ни удара пятки. Он движется не вопреки пространству, а протекая сквозь него, как жидкий ток.",
    "electrodynamicFormula": "R_contact → 0, ∇ × B = 0 (Безвихревой поток)",
    "somaticCalibration": "Сделайте следующий шаг или движение рукой медленно и бесшумно, как кот крадущийся по ветке. Почувствуйте кончики пальцев."
  },
  {
    "id": "basho-wild-heron",
    "author": "Басё (Basho)",
    "authorKanji": "松尾芭蕉",
    "haikuOriginal": "THE WILD HERON\nSLEEPING —\nUNDISTURBED NOBILITY.",
    "haikuRu": "Дикая цапля уснула —\nНепоколебимое\nБлагородство.",
    "theme": "Холостой ход чистого Тандэна (Дзансин)",
    "felineCircuitComment": "Сибирский кот спит на спинке дивана над пропастью в полтора метра. Баланс абсолютен. В его сне нет кошмаров о дедлайнах и невыплаченных кредитах. Он царственен, потому что не играет роль царя.",
    "electrodynamicFormula": "E = const, I = 0, P_loss = 0",
    "somaticCalibration": "Выпрямите позвоночник без натуги. Ощутите, что ваше достоинство вшито в саму гравитацию тела, а не в одобрение толпы."
  },
  {
    "id": "shiki-tiny-village",
    "author": "Сики (Shiki)",
    "authorKanji": "正岡子規",
    "haikuOriginal": "ALONE, I GO THROUGH A TINY VILLAGE,\nA DARK WINTER DAY.\nA DOG BARKS AND BARKS.",
    "haikuRu": "Один иду сквозь глухую деревню,\nТемный зимний день.\nСобака лает и лает.",
    "theme": "Слон и лающие собаки ума",
    "felineCircuitComment": "Дворовый кот неторопливо шествует по верхушке забора. Внизу захлебывается лаем соседская такса. Кот даже не поворачивает уха: собачий лай — это лишь шум генератора чужой тревоги. Забор прочен, путь свободен.",
    "electrodynamicFormula": "SNR → ∞ (Подавление синфазного шума DMN)",
    "somaticCalibration": "Заметьте навязчивую тревожную мысль. Скажите себе: «Пусть лает, это просто бродячая собака ума». Продолжайте свой шаг."
  },
  {
    "id": "kikaku-straw-mat",
    "author": "Кикаку (Kikaku)",
    "authorKanji": "宝井其角",
    "haikuOriginal": "A BRILLIANT FULL MOON!\nON THE MATTING OF MY FLOOR\nSHADOWS OF PINES FALL.",
    "haikuRu": "Ослепительное полнолуние!\nНа циновку моего пола\nПадают тени сосен.",
    "theme": "Созерцание без оценки (Мусин)",
    "felineCircuitComment": "Кот ловит лапой тень сосновой ветки на деревянном полу. Тень неосязаема, но игра с ней реальна на все сто процентов. Дзэн — это способность наслаждаться иллюзией игры, зная, что основание пола неколебимо.",
    "electrodynamicFormula": "Lila = True, R_friction = 0",
    "somaticCalibration": "Улыбнитесь уголками губ. Всё, что вас сейчас тревожит — лишь тени сосен на полу вашей спальни."
  },
  {
    "id": "basho-spring-scene",
    "author": "Басё (Basho)",
    "authorKanji": "松尾芭蕉",
    "haikuOriginal": "SPRING TOO, VERY SOON!\nTHEY ARE SETTING THE SCENE FOR IT —\nPLUM TREE AND MOON.",
    "haikuRu": "Весна тоже придёт совсем скоро!\nДекорации для неё уже расставлены —\nДерево сливы и луна.",
    "theme": "Готовность контура к фазовому переходу",
    "felineCircuitComment": "Февральский кот сидит у закрытой форточки и щурится на холодное солнце. Снег еще лежит, но в шерсти кота уже проснулась весна. Не нужно подгонять реку — когда созреют условия, весна взорвется цветением сама.",
    "electrodynamicFormula": "T → T_c (Приближение к критической температуре сверхпроводимости)",
    "somaticCalibration": "Сделайте глубокий медленный вдох носом. Не торопите события. Почувствуйте, как в глубине тела уже есть всё необходимое."
  },
  {
    "id": "ekon-swan-flight",
    "author": "Экон (Ekon)",
    "authorKanji": "慧可",
    "haikuOriginal": "WHO SHALL HALT THE SWAN\nIN ITS FLIGHT?\nOR LIFE IN ITS FLOW?",
    "haikuRu": "Кто сможет остановить лебедя\nВ его свободном полете?\nИли жизнь в её течении?",
    "theme": "Неостановимость естественного потока",
    "felineCircuitComment": "Попробуйте запереть кота в коробке — он станет жидкостью и вытечет в щель. Попробуйте навязать коту чужие планы — он мягко оттолкнется лапой и уйдет в сад. Жизнь нельзя удержать в кулаке; ее можно только прожить.",
    "electrodynamicFormula": "I = const, непрерывность уравнения Максвелла ∇ · J = -∂ρ/∂t",
    "somaticCalibration": "Раскройте сжатые кулаки ладонями вверх. Отпустите контроль над тем, что от вас не зависит."
  }
]

haikus_json = json.dumps(haikus, ensure_ascii=False)

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update Sidebar
    if 'id="zen-haiku-nav"' not in content:
        pattern = r'(<a href="cockpit\.html"[^>]*>[\s\S]*?<span>Пульт Сверхпроводимости</span>\s*</a>)'
        replacement = r'''\1
          <a id="zen-haiku-nav" href="#zen-haiku" onclick="navigateSidebar('#zen-haiku')" data-section="zen-haiku" class="sidebar-nav-item flex items-center justify-between gap-2 px-2.5 py-2 rounded-xl text-slate-300 hover:text-white hover:bg-slate-800/60 border border-transparent transition">
            <span class="flex items-center gap-2">
              <span class="sidebar-icon text-amber-300">🐾</span>
              <span>Кошачий Дзэн (Хайку)</span>
            </span>
            <span class="text-[9px] font-mono px-1.5 py-0.5 rounded bg-amber-500/10 text-amber-300 border border-amber-500/20 font-bold">Zen</span>
          </a>'''
        content = re.sub(pattern, replacement, content)

    # 2. Add #zen-haiku section before footer
    if 'id="zen-haiku"' not in content:
        section_html = '''
  <!-- ========================================================= -->
  <!-- ZEN HAIKU & FELINE CIRCUIT GENERATOR -->
  <!-- ========================================================= -->
  <section id="zen-haiku" class="py-16 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 border-t border-slate-800/80">
    <div class="text-center max-w-3xl mx-auto mb-10">
      <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-900 border border-slate-800 text-amber-300 text-xs font-mono font-medium tracking-wider mb-3">
        🐾 КВАНТ ДЗЭНА &amp; СВЕРХПРОВОДИМОСТЬ
      </div>
      <h2 class="text-2xl sm:text-3xl font-extrabold text-slate-100 font-display">
        Кошачий дзэн: Осциллограф живого присутствия
      </h2>
      <p class="text-slate-400 text-sm mt-3">
        Внутренний ток — не сухой механизм: он про изобилие жизни, поэзию и созерцание невыразимого. Дзэн-хайку и повадки кошек — два зеркала чистой проводимости без эго-шума.
      </p>
    </div>

    <!-- Haiku Card Container -->
    <div class="max-w-3xl mx-auto bg-gradient-to-b from-slate-900/90 to-slate-950 border border-slate-800/90 hover:border-amber-500/40 rounded-3xl p-6 sm:p-8 shadow-2xl relative overflow-hidden transition-all duration-300">
      <div class="absolute -right-16 -top-16 w-48 h-48 bg-amber-500/10 rounded-full blur-3xl pointer-events-none"></div>
      <div class="absolute -left-16 -bottom-16 w-48 h-48 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none"></div>

      <!-- Card Top: Author & Kanji -->
      <div class="flex items-center justify-between border-b border-slate-800/80 pb-4 mb-6">
        <div class="flex items-center gap-3">
          <span class="text-2xl">🐾</span>
          <div>
            <div id="zen-haiku-author" class="font-display font-bold text-amber-300 text-base">Басё (Basho)</div>
            <div id="zen-haiku-theme" class="text-xs font-mono text-slate-400">Мгновенный сброс эго-сопротивления</div>
          </div>
        </div>
        <div id="zen-haiku-kanji" class="text-2xl font-serif text-slate-500/40 select-none">松尾芭蕉</div>
      </div>

      <!-- Haiku Russian Text (Display) -->
      <div class="my-6 text-center">
        <blockquote id="zen-haiku-text-ru" class="font-serif italic text-lg sm:text-xl text-slate-100 leading-relaxed tracking-wide">
          Холодный дождь пошёл,<br>А я без шляпы...<br>Впрочем, какое мне до этого дело?
        </blockquote>
        <div id="zen-haiku-text-orig" class="text-[11px] font-mono text-slate-500 mt-3 tracking-widest uppercase">
          A COLD RAIN STARTING, AND ME WITHOUT A HAT. ON SECOND THOUGHT, WHO CARES?
        </div>
      </div>

      <!-- Feline Circuit Insight -->
      <div class="bg-slate-950/70 border border-slate-800/80 rounded-2xl p-4 sm:p-5 my-5 space-y-2">
        <div class="text-[11px] font-mono uppercase tracking-wider text-amber-400 font-semibold flex items-center gap-2">
          <span>🐾 Кошачий контур</span>
          <span class="text-slate-600">•</span>
          <span id="zen-haiku-formula" class="text-cyan-400 normal-case font-normal">R_ego: 100 Ω → 0 Ω за 0.05 с, Q_joule = 0</span>
        </div>
        <p id="zen-haiku-feline" class="text-xs sm:text-sm text-slate-300 leading-relaxed font-sans">
          Кот выходит на веранду под моросящий дождь. Никаких жалоб на климат, никакого самобичевания: уши прижаты, лапы пружинят, сопротивление R_ego мгновенно обнулено. Мокрая шерсть — это просто физика, а не трагедия.
        </p>
      </div>

      <!-- Somatic Calibration Hint -->
      <div class="bg-amber-500/5 border border-amber-500/20 rounded-xl p-3.5 flex items-start gap-3 text-xs text-amber-200/90 font-sans mb-6">
        <span class="text-base shrink-0">🧘</span>
        <div>
          <span class="font-semibold text-amber-300">Соматическая юстировка (20 сек):</span>
          <span id="zen-haiku-somatic" class="text-slate-300 ml-1">Разомкните зубы, сбросьте плечи вниз и спросите себя: «Какое мне до этого дело?» Почувствуйте, как уходит спазм со скул.</span>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex flex-col sm:flex-row items-center justify-between gap-3 pt-2">
        <button onclick="nextZenHaiku()" class="w-full sm:w-auto px-5 py-2.5 rounded-xl bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 font-semibold text-xs tracking-wide shadow-lg hover:shadow-amber-500/20 transition flex items-center justify-center gap-2 cursor-pointer">
          <span>⚡ Следующий квант</span>
          <span class="text-[10px] font-mono opacity-80">(Space)</span>
        </button>

        <a href="wiki.html" class="w-full sm:w-auto px-4 py-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-800 hover:border-slate-700 text-slate-300 hover:text-white text-xs transition flex items-center justify-center gap-2">
          <span>📖 Читать манифест «Кошачий дзэн» в Вики</span>
        </a>
      </div>
    </div>
  </section>
'''
        content = content.replace('  <!-- ========================================================= -->\n  <!-- FOOTER -->', section_html + '\n  <!-- ========================================================= -->\n  <!-- FOOTER -->')

    # 3. Add JavaScript code and data
    if 'window.nextZenHaiku' not in content:
        script_code = f'''
    // ZEN HAIKU & FELINE CIRCUIT ENGINE
    const ZEN_HAIKUS = {haikus_json};
    let currentZenHaikuIndex = 0;

    function renderZenHaiku(index) {{
      const h = ZEN_HAIKUS[index];
      if (!h) return;
      const elAuthor = document.getElementById('zen-haiku-author');
      const elTheme = document.getElementById('zen-haiku-theme');
      const elKanji = document.getElementById('zen-haiku-kanji');
      const elRu = document.getElementById('zen-haiku-text-ru');
      const elOrig = document.getElementById('zen-haiku-text-orig');
      const elFormula = document.getElementById('zen-haiku-formula');
      const elFeline = document.getElementById('zen-haiku-feline');
      const elSomatic = document.getElementById('zen-haiku-somatic');

      if (elAuthor) elAuthor.textContent = h.author;
      if (elTheme) elTheme.textContent = h.theme;
      if (elKanji) elKanji.textContent = h.authorKanji || '禅';
      if (elRu) elRu.innerHTML = h.haikuRu.replace(/\\n/g, '<br>');
      if (elOrig) elOrig.textContent = h.haikuOriginal.replace(/\\n/g, ' / ');
      if (elFormula) elFormula.textContent = h.electrodynamicFormula;
      if (elFeline) elFeline.textContent = h.felineCircuitComment;
      if (elSomatic) elSomatic.textContent = h.somaticCalibration;
    }}

    function nextZenHaiku() {{
      currentZenHaikuIndex = (currentZenHaikuIndex + 1) % ZEN_HAIKUS.length;
      renderZenHaiku(currentZenHaikuIndex);
    }}
    window.nextZenHaiku = nextZenHaiku;

    // Hotkey: Space to cycle haiku when in #zen-haiku section
    window.addEventListener('keydown', function(e) {{
      if (e.code === 'Space' && e.target === document.body) {{
        const section = document.getElementById('zen-haiku');
        if (section) {{
          const rect = section.getBoundingClientRect();
          if (rect.top < window.innerHeight && rect.bottom > 0) {{
            e.preventDefault();
            nextZenHaiku();
          }}
        }}
      }}
    }});
'''
        # Insert before closing script tag
        content = content.replace('    // Scrollspy: подсветка активного раздела в сайдбаре', script_code + '\n    // Scrollspy: подсветка активного раздела в сайдбаре')

    # Also update scrollspy sections list
    if "'zen-haiku'" not in content:
        content = content.replace("const sections = ['house', 'books', 'audiobook', 'reader', 'monographs', 'flashlight'];",
                                  "const sections = ['house', 'books', 'audiobook', 'reader', 'monographs', 'flashlight', 'zen-haiku'];")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filepath} successfully.")

update_file('public/index.html')
if re.search(r'public', 'dist_site'):
    try:
        update_file('dist_site/index.html')
    except Exception as e:
        print("dist_site/index.html skipped:", e)
