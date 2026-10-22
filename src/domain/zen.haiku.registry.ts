/**
 * Inner Current (Внутренний ток)
 * Zen Haiku & Feline Circuit Registry
 * Реестр Дзэн-хайку и кошачьей сверхпроводимости
 *
 * Содержит подлинные стихотворные формулы мастеров Дзэн (Басё, Исса, Рёкан,
 * Бусон, Сэкисо, Сосэки, Сики, Экон) с комментариями через кошачьи повадки
 * и контурную электродинамику.
 */

export interface ZenHaikuEntry {
  id: string;
  author: string;
  authorKanji?: string;
  haikuOriginal: string;
  haikuRu: string;
  theme: string;
  felineCircuitComment: string;
  electrodynamicFormula: string;
  somaticCalibration: string; // 15-30 секундная соматическая юстировка
}

export const ZEN_HAIKU_REGISTRY: ZenHaikuEntry[] = [
  {
    id: 'basho-cold-rain',
    author: 'Басё (Basho)',
    authorKanji: '松尾芭蕉',
    haikuOriginal: `A COLD RAIN STARTING,\nAND ME WITHOUT A HAT.\nON SECOND THOUGHT, WHO CARES?`,
    haikuRu: `Холодный дождь пошёл,\nА я без шляпы...\nВпрочем, какое мне до этого дело?`,
    theme: 'Мгновенный сброс эго-сопротивления',
    felineCircuitComment: 'Кот выходит на веранду под моросящий дождь. Никаких жалоб на климат, никакого самобичевания: уши прижаты, лапы пружинят, сопротивление R_ego мгновенно обнулено. Мокрая шерсть — это просто физика, а не трагедия.',
    electrodynamicFormula: 'R_ego: 100 Ω → 0 Ω за 0.05 с, Q_joule = 0',
    somaticCalibration: 'Разомкните зубы, сбросьте плечи вниз и спросите себя: «Какое мне до этого дело?» Почувствуйте, как уходит напряжение из скул.'
  },
  {
    id: 'ryokan-the-thief',
    author: 'Рёкан (Ryokan)',
    authorKanji: '良寛',
    haikuOriginal: `THE THIEF\nLEFT IT BEHIND —\nTHE MOON AT THE WINDOW.`,
    haikuRu: `Вор оставил её\nНетронутой —\nЛуна в окне.`,
    theme: 'Неуязвимость пустой полости (Шуньята)',
    felineCircuitComment: 'Вор обчистил хижину монаха, но кот продолжает дремать на подоконнике в пятне лунного света. Нельзя украсть то, за что ты не цепляешься когтями. Лунный свет принадлежит коту целиком, потому что кот пуст.',
    electrodynamicFormula: 'E_load = 0, Z_0 = const, I_theft = 0',
    somaticCalibration: 'Положите ладонь на живот под пупком. Выдохните всё имущество и тревогу. Внутренний свет украсть невозможно.'
  },
  {
    id: 'ryokan-stretched-out',
    author: 'Рёкан (Ryokan)',
    authorKanji: '良寛',
    haikuOriginal: `FORGETTING THE EQUAL DUSTS OF NAME AND FORTUNE,\nLISTENING TO THE NIGHT RAIN ON THE ROOF OF MY HUT,\nI SIT AT EASE,\nBOTH LEGS STRETCHED OUT.`,
    haikuRu: `Забыв одинаковую пыль славы и богатства,\nСлушаю ночной дождь по крыше хижины,\nСижу в полном покое,\nВытянув обе ноги.`,
    theme: 'Соматическая капитуляция в Тандэн',
    felineCircuitComment: 'Кот лежит на спине посреди ковра, раскинув лапы в форме звезды, подставив теплому воздуху беззащитное брюхо. Абсолютное доверие к несущей среде: социальный радар выключен, ток течет без омического сопротивления.',
    electrodynamicFormula: 'R_ego = 0, η = 100%, P_dissipated = 0',
    somaticCalibration: 'Вытяните ноги, размягчите живот так, чтобы он колыхался при дыхании. Пусть шум мира станет шелестом дождя по соломе.'
  },
  {
    id: 'basho-wild-violet',
    author: 'Басё (Basho)',
    authorKanji: '松尾芭蕉',
    haikuOriginal: `ALONG THE MOUNTAIN ROAD\nSOMEHOW IT TUGS AT MY HEART:\nA WILD VIOLET.`,
    haikuRu: `Вдоль горной дороги\nЧто-то тронуло сердце:\nДикая фиалка.`,
    theme: 'Сверхпроводимость эстетического резонанса',
    felineCircuitComment: 'Кот замирает перед трепещущим листком папоротника. Никакой утилитарной цели: листок несъедобен, за него не дадут мышь. Но внимание кота целокупно и бесконечно. Контур замкнут через красоту момента.',
    electrodynamicFormula: 'Z_in = Z_load (Идеальное согласование импедансов)',
    somaticCalibration: 'Остановите взгляд на любой случайной детали: узоре дерева, блике света на столе. Смотрите без названия 10 секунд.'
  },
  {
    id: 'issa-dewdrop-world',
    author: 'Исса (Issa)',
    authorKanji: '小林一茶',
    haikuOriginal: `THIS DEWDROP WORLD —\nIT MAY BE A DEWDROP,\nAND YET ... AND YET ...`,
    haikuRu: `Этот мир — капля росы.\nПусть всего лишь капля росы,\nИ все же... и все же...`,
    theme: 'Нежность к хрупкости бытия (Гальваническая развязка)',
    felineCircuitComment: 'Кот смотрит на тающую снежинку на кончике собственного носа. Она исчезнет через миг. Дзэн не требует быть каменным истуканом; дзэн позволяет любить каплю росы, не пытаясь запаять ее в сейф.',
    electrodynamicFormula: 'M_ind > 0, без короткого замыкания созависимости',
    somaticCalibration: 'Позвольте себе почувствовать грусть или нежность без попытки их исправить или подавить. Дайте току просто протечь.'
  },
  {
    id: 'basho-cicada-shell',
    author: 'Басё (Basho)',
    authorKanji: '松尾芭蕉',
    haikuOriginal: `ONLY THE SHELL\nOF THE CICADA LEFT?\nDID IT SING ITSELF OUT OF EXISTENCE?`,
    haikuRu: `Только сухая скорлупка\nОсталась от цикады?\nНеужели она выпела себя из бытия?`,
    theme: 'Предельная отдача в нагрузку (100% КПД)',
    felineCircuitComment: 'Кот, преследующий солнечный зайчик, отдает броску всю свою кошачью массу, до кончика вибрирующего хвоста. Никаких резервов на завтра, никакого сомнения. Спеть себя без остатка — единственный способ победить смерть.',
    electrodynamicFormula: 'η = P_out / P_in = 1.0, W_useful = max',
    somaticCalibration: 'Если делаете что-то прямо сейчас (пьете чай, пишете код, гладите кота) — погрузитесь в это так, будто завтра не существует.'
  },
  {
    id: 'zen-expression-grass',
    author: 'Дзэнский канон',
    authorKanji: '禅',
    haikuOriginal: `ENTERING THE FOREST,\nHE MOVES NOT THE GRASS.\nENTERING THE WATER,\nHE MAKES NOT A RIPPLE.`,
    haikuRu: `Входя в густой лес,\nНе колыхнет травинку.\nВступая в воду,\nНе поднимет ряби.`,
    theme: 'Ламинарный ток без омического следа',
    felineCircuitComment: 'Черный кот бесшумно ступает мягкими подушечками по скрипучему паркету старого дома. Ни звука когтей, ни удара пятки. Он движется не вопреки пространству, а протекая сквозь него, как жидкий ток.',
    electrodynamicFormula: 'R_contact → 0, ∇ × B = 0 (Безвихревой поток)',
    somaticCalibration: 'Сделайте следующий шаг или движение рукой медленно и бесшумно, как кот крадущийся по ветке. Почувствуйте кончики пальцев.'
  },
  {
    id: 'basho-wild-heron',
    author: 'Басё (Basho)',
    authorKanji: '松尾芭蕉',
    haikuOriginal: `THE WILD HERON\nSLEEPING —\nUNDISTURBED NOBILITY.`,
    haikuRu: `Дикая цапля уснула —\nНепоколебимое\nБлагородство.`,
    theme: 'Холостой ход чистого Тандэна (Дзансин)',
    felineCircuitComment: 'Сибирский кот спит на спинке дивана над пропастью в полтора метра. Баланс абсолютен. В его сне нет кошмаров о дедлайнах и невыплаченных кредитах. Он царственен, потому что не играет роль царя.',
    electrodynamicFormula: 'E = const, I = 0, P_loss = 0',
    somaticCalibration: 'Выпрямите позвоночник без натуги. Ощутите, что ваше достоинство вшито в саму гравитацию тела, а не в одобрение толпы.'
  },
  {
    id: 'shiki-tiny-village',
    author: 'Сики (Shiki)',
    authorKanji: '正岡子規',
    haikuOriginal: `ALONE, I GO THROUGH A TINY VILLAGE,\nA DARK WINTER DAY.\nA DOG BARKS AND BARKS.`,
    haikuRu: `Один иду сквозь глухую деревню,\nТемный зимний день.\nСобака лает и лает.`,
    theme: 'Слон и лающие собаки ума',
    felineCircuitComment: 'Дворовый кот неторопливо шествует по верхушке забора. Внизу захлебывается лаем соседская такса. Кот даже не поворачивает уха: собачий лай — это лишь шум генератора чужой тревоги. Забор прочен, путь свободен.',
    electrodynamicFormula: 'SNR → ∞ (Подавление синфазного шума DMN)',
    somaticCalibration: 'Заметьте навязчивую тревожную мысль. Скажите себе: «Пусть лает, это просто бродячая собака ума». Продолжайте свой шаг.'
  },
  {
    id: 'kikaku-straw-mat',
    author: 'Кикаку (Kikaku)',
    authorKanji: '宝井其角',
    haikuOriginal: `A BRILLIANT FULL MOON!\nON THE MATTING OF MY FLOOR\nSHADOWS OF PINES FALL.`,
    haikuRu: `Ослепительное полнолуние!\nНа циновку моего пола\nПадают тени сосен.`,
    theme: 'Созерцание без оценки (Мусин)',
    felineCircuitComment: 'Кот ловит лапой тень сосновой ветки на деревянном полу. Тень неосязаема, но игра с ней реальна на все сто процентов. Дзэн — это способность наслаждаться иллюзией игры, зная, что основание пола неколебимо.',
    electrodynamicFormula: 'Lila = True, R_friction = 0',
    somaticCalibration: 'Улыбнитесь уголками губ. Всё, что вас сейчас тревожит — лишь тени сосен на полу вашей спальни.'
  },
  {
    id: 'basho-spring-scene',
    author: 'Басё (Basho)',
    authorKanji: '松尾芭蕉',
    haikuOriginal: `SPRING TOO, VERY SOON!\nTHEY ARE SETTING THE SCENE FOR IT —\nPLUM TREE AND MOON.`,
    haikuRu: `Весна тоже придёт совсем скоро!\nДекорации для неё уже расставлены —\nДерево сливы и луна.`,
    theme: 'Готовность контура к фазовому переходу',
    felineCircuitComment: 'Февральский кот сидит у закрытой форточки и щурится на холодное солнце. Снег еще лежит, но в шерсти кота уже проснулась весна. Не нужно подгонять реку — когда созреют условия, весна взорвется цветением сама.',
    electrodynamicFormula: 'T → T_c (Приближение к критической температуре сверхпроводимости)',
    somaticCalibration: 'Сделайте глубокий медленный вдох носом. Не торопите события. Почувствуйте, как в глубине тела уже есть всё необходимое.'
  },
  {
    id: 'ekon-swan-flight',
    author: 'Экон (Ekon)',
    authorKanji: '慧可',
    haikuOriginal: `WHO SHALL HALT THE SWAN\nIN ITS FLIGHT?\nOR LIFE IN ITS FLOW?`,
    haikuRu: `Кто сможет остановить лебедя\nВ его свободном полете?\nИли жизнь в её течении?`,
    theme: 'Неостановимость естественного потока',
    felineCircuitComment: 'Попробуйте запереть кота в коробке — он станет жидкостью и вытечет в щель. Попробуйте навязать коту чужие планы — он мягко оттолкнется лапой и уйдет в сад. Жизнь нельзя удержать в кулаке; ее можно только прожить.',
    electrodynamicFormula: 'I = const, непрерывность уравнения Максвелла ∇ · J = -∂ρ/∂t',
    somaticCalibration: 'Раскройте сжатые кулаки ладонями вверх. Отпустите контроль над тем, что от вас не зависит.'
  }
];

/**
 * Получить случайное Дзэн-хайку с кошачьим комментарием
 */
export function getRandomZenHaiku(): ZenHaikuEntry {
  const index = Math.floor(Math.random() * ZEN_HAIKU_REGISTRY.length);
  return ZEN_HAIKU_REGISTRY[index];
}

/**
 * Найти хайку по идентификатору
 */
export function getZenHaikuById(id: string): ZenHaikuEntry | undefined {
  return ZEN_HAIKU_REGISTRY.find(h => h.id === id);
}

/**
 * Отфильтровать хайку по автору
 */
export function filterZenHaikusByAuthor(authorSubstring: string): ZenHaikuEntry[] {
  const query = authorSubstring.toLowerCase();
  return ZEN_HAIKU_REGISTRY.filter(h => h.author.toLowerCase().includes(query));
}

/**
 * Получить весь каталог хайку
 */
export function getAllZenHaikus(): ZenHaikuEntry[] {
  return [...ZEN_HAIKU_REGISTRY];
}
