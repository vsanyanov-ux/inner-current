/**
 * Inner Current (Внутренний ток)
 * Zen Ontological Atlas: 23 канона Дзен и их биективные физические аналоги
 */

import { ZenOntologyCanon } from '../types/circuit.types.ts';

export type OntologicalLevel = 1 | 2 | 3 | 4 | 5;

export interface ZenCanonDefinition {
  id: ZenOntologyCanon;
  kanji: string;
  romaji: string;
  russianName: string;
  level: OntologicalLevel;
  levelTitle: string;
  electrodynamicAnalogy: string;
  formula: string;
  description: string;
}

export const ZEN_CANON_CATALOG: Record<ZenOntologyCanon, ZenCanonDefinition> = {
  // Уровень 1: Источник (Генератор)
  [ZenOntologyCanon.TANDEN]: {
    id: ZenOntologyCanon.TANDEN,
    kanji: '丹田',
    romaji: 'Tanden',
    russianName: 'Тандэн (Киноварное поле)',
    level: 1,
    levelTitle: 'Источник (Генератор)',
    electrodynamicAnalogy: 'Автономный генератор ЭДС (E)',
    formula: 'E = const, r_int > 0',
    description: 'Внутренний неделимый реактор человека, вырабатывающий первичное напряжение воли и жизни без внешних подпорок.'
  },
  [ZenOntologyCanon.BUSSHO]: {
    id: ZenOntologyCanon.BUSSHO,
    kanji: '仏性',
    romaji: 'Bussho',
    russianName: 'Буссё (Природа Будды)',
    level: 1,
    levelTitle: 'Источник (Генератор)',
    electrodynamicAnalogy: 'Номинальная установленная мощность генератора (P_rated)',
    formula: 'P_rated = E_max · I_max',
    description: 'Изначальная безграничная полнота потенциала каждого сознания, присутствующая до любых искажений опыта.'
  },
  [ZenOntologyCanon.SHUNYATA]: {
    id: ZenOntologyCanon.SHUNYATA,
    kanji: '空',
    romaji: 'Shunyata',
    russianName: 'Шуньята (Пустотность формы)',
    level: 1,
    levelTitle: 'Источник (Генератор)',
    electrodynamicAnalogy: 'Волновой вакуум и нулевой внутренний импеданс (Z_0)',
    formula: 'E_load = 0',
    description: 'Фундаментальный закон пустотности внешних предметов и форм: они не содержат внутри себя постоянного источника питания.'
  },

  // Уровень 2: Проводимость (Среда и Состояние)
  [ZenOntologyCanon.MUSHIN]: {
    id: ZenOntologyCanon.MUSHIN,
    kanji: '無心',
    romaji: 'Mushin',
    russianName: 'Мусин (Не-ум / Чистое присутствие)',
    level: 2,
    levelTitle: 'Проводимость (Среда и Состояние)',
    electrodynamicAnalogy: 'Сверхпроводимость шины внимания (R -> 0)',
    formula: 'R_eff → 0, η = 1.0',
    description: 'Состояние ламинарного потока, когда сопротивление ума обнулено, и 100% мощности передаётся прямо в действие.'
  },
  [ZenOntologyCanon.FUDOSHIN]: {
    id: ZenOntologyCanon.FUDOSHIN,
    kanji: '不動心',
    romaji: 'Fudoshin',
    russianName: 'Фудосин (Непоколебимый дух)',
    level: 2,
    levelTitle: 'Проводимость (Среда и Состояние)',
    electrodynamicAnalogy: 'Стабилизатор рабочей точки цепи',
    formula: 'du / dt = 0',
    description: 'Невозмутимая устойчивость центра тяжести при любых внешних помехах, флуктуациях и провокациях среды.'
  },
  [ZenOntologyCanon.ZANSHIN]: {
    id: ZenOntologyCanon.ZANSHIN,
    kanji: '残心',
    romaji: 'Zanshin',
    russianName: 'Дзансин (Остаточное осознание)',
    level: 2,
    levelTitle: 'Проводимость (Среда и Состояние)',
    electrodynamicAnalogy: 'Быстродействующий автоматический выключатель (Circuit Breaker)',
    formula: 't_trip < 10 ms',
    description: 'Непрерывное осознавание после завершения действия, мгновенно размыкающее цепь при аварии внешней опоры.'
  },
  [ZenOntologyCanon.SHOSHIN]: {
    id: ZenOntologyCanon.SHOSHIN,
    kanji: '初心',
    romaji: 'Shoshin',
    russianName: 'Сёсин (Ум новичка)',
    level: 2,
    levelTitle: 'Проводимость (Среда и Состояние)',
    electrodynamicAnalogy: 'Холодный сброс реактивных емкостей и индуктивностей (Hard Reset)',
    formula: 'Q_cap = 0, Φ_ind = 0',
    description: 'Способность встречать каждое явление свободным от груза прошлого опыта и шаблонов.'
  },
  [ZenOntologyCanon.JIKISHININSHIN]: {
    id: ZenOntologyCanon.JIKISHININSHIN,
    kanji: '直指人心',
    romaji: 'Jikishininshin',
    russianName: 'Дзикисиннинсин (Прямое указание)',
    level: 2,
    levelTitle: 'Проводимость (Среда и Состояние)',
    electrodynamicAnalogy: 'Прямая магистральная шина без промежуточных буферов (Direct Bus)',
    formula: 'L_inter = 0',
    description: 'Прямая передача намерения в реальность без искажающих концептуальных надстроек и бюрократии ума.'
  },

  // Уровень 3: Аварии и Деградация (Потери цепи)
  [ZenOntologyCanon.JIGA]: {
    id: ZenOntologyCanon.JIGA,
    kanji: '自我',
    romaji: 'Jiga',
    russianName: 'Дзига (Эго)',
    level: 3,
    levelTitle: 'Аварии и Деградация (Потери цепи)',
    electrodynamicAnalogy: 'Внутренний паразитный шунт и ток КЗ',
    formula: 'I_кз = E / (r_int + R_ego), I_load = 0',
    description: 'Попытка замкнуть ток на себя ради валидации, приводящая к блокировке внешнего ремесла и выжиганию нервной системы.'
  },
  [ZenOntologyCanon.MAKYO]: {
    id: ZenOntologyCanon.MAKYO,
    kanji: '魔境',
    romaji: 'Makyo',
    russianName: 'Макё (Иллюзорный морок)',
    level: 3,
    levelTitle: 'Аварии и Деградация (Потери цепи)',
    electrodynamicAnalogy: 'Паразитные реактансы ума (L_past, C_future)',
    formula: 'X_L = ωL, X_C = 1 / (ωC)',
    description: 'Застревание внимания в симуляциях того, чего сейчас физически нет: сожаления о прошлом и тревожные сценарии будущего.'
  },
  [ZenOntologyCanon.DUKKHA]: {
    id: ZenOntologyCanon.DUKKHA,
    kanji: '苦',
    romaji: 'Dukkha',
    russianName: 'Дуккха (Страдание)',
    level: 3,
    levelTitle: 'Аварии и Деградация (Потери цепи)',
    electrodynamicAnalogy: 'Джоулево тепловое рассеяние на внутреннем сопротивлении',
    formula: 'Q = I² · R · t',
    description: 'Неизбежный физический нагрев проводки при протекании тока сквозь внутреннее сопротивление и неприятие реальности.'
  },
  [ZenOntologyCanon.BONNO]: {
    id: ZenOntologyCanon.BONNO,
    kanji: '煩悩',
    romaji: 'Bonno',
    russianName: 'Бонно (Омрачения / Страсти)',
    level: 3,
    levelTitle: 'Аварии и Деградация (Потери цепи)',
    electrodynamicAnalogy: 'Токи утечки диэлектрика и паразитная проводимость',
    formula: 'I_leak > 0',
    description: 'Хаотичный отток ментальной энергии в фоновые влечения и компульсивные привычки.'
  },

  // Уровень 4: Ремедиация и Инженерная практика
  [ZenOntologyCanon.SATORI]: {
    id: ZenOntologyCanon.SATORI,
    kanji: '悟り',
    romaji: 'Satori',
    russianName: 'Сатори (Просветление / Прозрение)',
    level: 4,
    levelTitle: 'Ремедиация и Инженерная практика',
    electrodynamicAnalogy: 'Фазовый переход второго рода в состояние сверхпроводимости',
    formula: 'T < T_c ⇒ R = 0',
    description: 'Внезапный скачкообразный сброс сопротивления ума в ноль при осознании истинной природы цепи.'
  },
  [ZenOntologyCanon.KOAN]: {
    id: ZenOntologyCanon.KOAN,
    kanji: '公案',
    romaji: 'Koan',
    russianName: 'Коан (Парадоксальная задача)',
    level: 4,
    levelTitle: 'Ремедиация и Инженерная практика',
    electrodynamicAnalogy: 'Контроллер прерывания бесконечных циклов (Exception Trap)',
    formula: 'while(true) break;',
    description: 'Парадокс, взрывающий рациональные замкнутые петли дуального рассудочного мышления.'
  },
  [ZenOntologyCanon.SAMU]: {
    id: ZenOntologyCanon.SAMU,
    kanji: '作務',
    romaji: 'Samu',
    russianName: 'Саму (Осознанный физический труд)',
    level: 4,
    levelTitle: 'Ремедиация и Инженерная практика',
    electrodynamicAnalogy: 'Сенсомоторный калибровочный стенд',
    formula: 'Grounding → 1.0',
    description: 'Простая ручная работа (мытьё пола, колка дров, садоводство) как мощный инструмент заземления и сброса ментального перегрева.'
  },
  [ZenOntologyCanon.ICHIGO_ICHIE]: {
    id: ZenOntologyCanon.ICHIGO_ICHIE,
    kanji: '一期一会',
    romaji: 'Ichigo Ichie',
    russianName: 'Итиго Итиэ (Один миг — одна встреча)',
    level: 4,
    levelTitle: 'Ремедиация и Инженерная практика',
    electrodynamicAnalogy: 'Дискретный неделимый квант времени (t = now)',
    formula: 'Δt = dt',
    description: 'Восприятие текущего момента как единственного и неповторимого шанса подать чистый ток в реальность.'
  },
  [ZenOntologyCanon.NIJIRIGUCHI]: {
    id: ZenOntologyCanon.NIJIRIGUCHI,
    kanji: '躙口',
    romaji: 'Nijiriguchi',
    russianName: 'Нидзиригути (Низкий лаз чайного дома)',
    level: 4,
    levelTitle: 'Ремедиация и Инженерная практика',
    electrodynamicAnalogy: 'Входной фильтр отсечения эго-шунта',
    formula: 'R_ego = ∞ (loop opened)',
    description: 'Метровый проём, заставляющий любого входящего снять меч, склонить голову и войти в комнату действия равным и смиренным.'
  },

  // Уровень 5: Форма, Структура и Эстетика
  [ZenOntologyCanon.KANSO]: {
    id: ZenOntologyCanon.KANSO,
    kanji: '簡素',
    romaji: 'Kanso',
    russianName: 'Кансо (Простота / Отсечение лишнего)',
    level: 5,
    levelTitle: 'Форма, Структура и Эстетика',
    electrodynamicAnalogy: 'Минимальная топология цепи без паразитных элементов (Бритва Оккама)',
    formula: 'N_elements = min',
    description: 'Совершенство, достигнутое не тогда, когда нечего добавить, а когда нечего убрать.'
  },
  [ZenOntologyCanon.WABI_SABI]: {
    id: ZenOntologyCanon.WABI_SABI,
    kanji: '侘寂',
    romaji: 'Wabi-sabi',
    russianName: 'Ваби-саби (Красота несовершенства)',
    level: 5,
    levelTitle: 'Форма, Структура и Эстетика',
    electrodynamicAnalogy: 'Толерантность к энтропии нагрузки и шуму реального мира',
    formula: 'Tolerance = High',
    description: 'Принятие шероховатостей, старения и неидеальности материальных вещей без разочарования и драмы.'
  },
  [ZenOntologyCanon.KINTSUGI]: {
    id: ZenOntologyCanon.KINTSUGI,
    kanji: '金継ぎ',
    romaji: 'Kintsugi',
    russianName: 'Кинцуги (Золотой шов)',
    level: 5,
    levelTitle: 'Форма, Структура и Эстетика',
    electrodynamicAnalogy: 'Высокопрочный диэлектрический ремонт места аварии с сохранением опыта',
    formula: 'Strength_repair > Strength_init',
    description: 'Реставрация разбитой формы золотым лаком: шрам превращается в самое ценное и устойчивое место структуры.'
  },
  [ZenOntologyCanon.SHIBUMI]: {
    id: ZenOntologyCanon.SHIBUMI,
    kanji: '渋味',
    romaji: 'Shibumi',
    russianName: 'Сибуми (Сдержанное совершенство)',
    level: 5,
    levelTitle: 'Форма, Структура и Эстетика',
    electrodynamicAnalogy: 'Идеальное согласование комплексных импедансов (Z_src = Z_load*)',
    formula: 'Z_src = Z_load*',
    description: 'Глубокая, неброская утонченность мастера, достигаемая максимальной эффективностью передачи энергии без показухи.'
  },
  [ZenOntologyCanon.YUGEN]: {
    id: ZenOntologyCanon.YUGEN,
    kanji: '幽玄',
    romaji: 'Yugen',
    russianName: 'Югэн (Неуловимая таинственная глубина)',
    level: 5,
    levelTitle: 'Форма, Структура и Эстетика',
    electrodynamicAnalogy: 'Внешнее электромагнитное поле проводника (B-поле)',
    formula: 'rot(B) = μ · j',
    description: 'Невидимое присутствие и благородное излучение человека, находящегося в состоянии сверхпроводящего потока.'
  },
  [ZenOntologyCanon.FUKINZOKU]: {
    id: ZenOntologyCanon.FUKINZOKU,
    kanji: '不均斉',
    romaji: 'Fukinzoku',
    russianName: 'Фукинзоку (Асимметрия и динамический баланс)',
    level: 5,
    levelTitle: 'Форма, Структура и Эстетика',
    electrodynamicAnalogy: 'Динамический закон Кирхгофа на распределительном щите 6 ламп',
    formula: 'sum(I_in) = sum(I_out)',
    description: 'Живое асимметричное равновесие жизненных сфер вместо искусственной жесткой статики.'
  }
};

/**
 * Получить список канонов по онтологическому уровню (1-5).
 */
export function getZenCanonsByLevel(level: OntologicalLevel): ZenCanonDefinition[] {
  return Object.values(ZEN_CANON_CATALOG).filter(c => c.level === level);
}

/**
 * Найти канон по идентификатору.
 */
export function getZenCanon(id: ZenOntologyCanon): ZenCanonDefinition {
  const canon = ZEN_CANON_CATALOG[id];
  if (!canon) {
    throw new Error(`Неизвестный канон Дзен: ${id}`);
  }
  return canon;
}
