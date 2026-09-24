/**
 * Inner Current (Внутренний ток)
 * Ten Bulls of Zen Registry & Operator Evolution Evaluator (Дзюгю, 十牛)
 * 
 * 10 стадий эволюции оператора цепи: от первичного разрыва контура
 * до абсолютной сверхпроводимости служения миру на шумном базаре.
 */

import {
  CircuitStatus,
  LoadScale,
  TenBullsStage
} from '../types/circuit.types.ts';
import type {
  CircuitTelemetry,
  DiagnosticResult,
  SixBulbPanel,
  TenBullsStageInfo
} from '../types/circuit.types.ts';

export const TEN_BULLS_CATALOG: Record<TenBullsStage, TenBullsStageInfo> = {
  [TenBullsStage.SEEKING_THE_OX]: {
    stage: 1,
    id: TenBullsStage.SEEKING_THE_OX,
    kanji: '寻牛',
    romaji: 'Xun Niu (Seeking the Ox)',
    russianTitle: 'В поисках быка',
    circuitState: 'Разрыв контура / Фиатная слепота (I = 0, R_eff >> 0)',
    operatorGuidance: 'Прекратите искать энергию во внешних аккумуляторах. Внешние формы пусты (Шуньята). Ваш генератор спит внутри — обратите внимание в тело.'
  },
  [TenBullsStage.DISCOVERING_FOOTPRINTS]: {
    stage: 2,
    id: TenBullsStage.DISCOVERING_FOOTPRINTS,
    kanji: '见迹',
    romaji: 'Jian Ji (Discovering the Footprints)',
    russianTitle: 'Обнаружение следов',
    circuitState: 'Первичная телеметрия и чтение схемы (R распознано)',
    operatorGuidance: 'Осциллограф включен. Вы видите, где именно греется проводка (прошлое/будущее). Замеряйте сопротивление без самоосуждения.'
  },
  [TenBullsStage.PERCEIVING_THE_OX]: {
    stage: 3,
    id: TenBullsStage.PERCEIVING_THE_OX,
    kanji: '见牛',
    romaji: 'Jian Niu (Perceiving the Ox)',
    russianTitle: 'Первый взгляд на быка',
    circuitState: 'Вспышка Сатори / Первый контакт с Тандэном (R -> 0 кратко)',
    operatorGuidance: 'Вы физически ощутили автономный реактор внизу живота. Источник найден. Закрепите соматический якорь в Тандэне.'
  },
  [TenBullsStage.CATCHING_THE_OX]: {
    stage: 4,
    id: TenBullsStage.CATCHING_THE_OX,
    kanji: '得牛',
    romaji: 'De Niu (Catching the Ox)',
    russianTitle: 'Поимка быка',
    circuitState: 'Борьба с реостатом Эго и привычками DMN (нестабильная точка)',
    operatorGuidance: 'Держите поводок! Дефолт-система мозга сопротивляется и пытается закоротить цепь. Дышите диафрагмой, включайте TPN через физический контакт.'
  },
  [TenBullsStage.TAMING_THE_OX]: {
    stage: 5,
    id: TenBullsStage.TAMING_THE_OX,
    kanji: '牧牛',
    romaji: 'Mu Niu (Taming the Ox)',
    russianTitle: 'Укрощение быка',
    circuitState: 'Калибровка проводки / Режим Мусин (R <= 5 Ом, ламинарный ток)',
    operatorGuidance: 'Поводок провис. Ток течет ровно, клеммы не искрят. Мышление о себе затихает, энергия реактора чисто питает текущую задачу.'
  },
  [TenBullsStage.RIDING_HOME]: {
    stage: 6,
    id: TenBullsStage.RIDING_HOME,
    kanji: '骑牛归家',
    romaji: 'Qi Niu Gui Jia (Riding the Ox Home)',
    russianTitle: 'Возвращение домой на быке',
    circuitState: 'Согласование импедансов и Поток (Z_src = Z_load*, Flow)',
    operatorGuidance: 'Борьба окончена. Исчезло усилие воли. Тандэн сам несет вас сквозь сложное ремесло. Играйте свою мелодию без сопротивления среды.'
  },
  [TenBullsStage.OX_TRANSCENDED]: {
    stage: 7,
    id: TenBullsStage.OX_TRANSCENDED,
    kanji: '忘牛存人',
    romaji: 'Wang Niu Cun Ren (The Ox Transcended)',
    russianTitle: 'Бык забыт, пастух один',
    circuitState: 'Ликвидация концептуальных костылей (автономный покой)',
    operatorGuidance: 'Метод выполнил задачу. Вам больше не нужно непрерывно проверять приборы. Просто присутствуйте в ясном свете текущего момента.'
  },
  [TenBullsStage.BOTH_TRANSCENDED]: {
    stage: 8,
    id: TenBullsStage.BOTH_TRANSCENDED,
    kanji: '人牛俱忘',
    romaji: 'Ren Niu Ju Wang (Both Ox and Man Transcended)',
    russianTitle: 'И бык, и пастух забыты (Энсо)',
    circuitState: 'Квантовая Шуньята / Нуль-импеданс вакуума (R = 0, Z0 = 0)',
    operatorGuidance: 'Круг Энсо. Исчез дуализм наблюдателя и наблюдаемого. Нет отдельно вас и отдельно счастья. Чистый квантовый штиль мироздания.'
  },
  [TenBullsStage.RETURNING_TO_SOURCE]: {
    stage: 9,
    id: TenBullsStage.RETURNING_TO_SOURCE,
    kanji: '返本还源',
    romaji: 'Fan Ben Huan Yuan (Returning to the Source)',
    russianTitle: 'Возвращение к истоку',
    circuitState: 'Инвариантная Таковость (Татхата) и законы природы',
    operatorGuidance: 'Река течет, сосны зелены. Полное отсутствие претензий к миру. Сознание совершенно синхронизировано с термодинамикой космоса.'
  },
  [TenBullsStage.ENTERING_MARKETPLACE]: {
    stage: 10,
    id: TenBullsStage.ENTERING_MARKETPLACE,
    kanji: '入廛垂手',
    romaji: 'Ru Chan Chui Shou (Entering the Marketplace)',
    russianTitle: 'Вхождение на базар с открытыми руками',
    circuitState: 'Запитка 6 ламп мира и Внешний магнетизм (Кульминация)',
    operatorGuidance: 'Высшее мастерство. Вы в самом центре мирского хаоса, бизнеса и отношений. Ваш Тандэн светит столь мощно, что зажигает потухшие сердца вокруг.'
  }
};

/**
 * Оценивает текущую ступень зрелости оператора по канону Десяти быков
 * на основе точной электродинамической телеметрии цепи.
 */
export function evaluateTenBullsStage(
  telemetry: CircuitTelemetry,
  diagnostic: DiagnosticResult,
  _panel?: SixBulbPanel
): TenBullsStageInfo {
  const { core, bus, load, breaker } = telemetry;
  const R = diagnostic.effectiveResistance;
  const isSuper = diagnostic.status === CircuitStatus.SUPERCONDUCTING;
  const isEgoShort = diagnostic.status === CircuitStatus.EGO_SHORT_CIRCUIT;
  const isOpen = diagnostic.status === CircuitStatus.OPEN_CIRCUIT;
  const isShortCircuit = diagnostic.status === CircuitStatus.SHORT_CIRCUIT;

  // 1. Авария КЗ на Эго
  if (isEgoShort || load?.expectationOfValidation) {
    if (core.reserve < 45 || bus.baseResistance > 25) {
      return TEN_BULLS_CATALOG[TenBullsStage.SEEKING_THE_OX];
    }
    // Если ядро развито, но сорвался в петлю признания — это 4-я ступень (борьба с диким быком)
    return TEN_BULLS_CATALOG[TenBullsStage.CATCHING_THE_OX];
  }

  // 2. Обрыв контура (нет полезной нагрузки)
  if (isOpen || !load) {
    return TEN_BULLS_CATALOG[TenBullsStage.SEEKING_THE_OX];
  }

  // 3. Авария внешней нагрузки (SHORT_CIRCUIT)
  if (isShortCircuit) {
    const zanshinActive = breaker.zanshinAwareness >= breaker.tripThreshold;
    if (zanshinActive) {
      // Оператор высокого класса: сработал предохранитель Дзансин, ядро сохранено (Ваби-саби / Кинцуги)
      return TEN_BULLS_CATALOG[TenBullsStage.TAMING_THE_OX];
    }
    return TEN_BULLS_CATALOG[TenBullsStage.CATCHING_THE_OX];
  }

  // 4. Сверхпроводимость контура (R <= 5 Ом, ток течет)
  if (isSuper) {
    // Если масштаб нагрузки — макро-предприятие или высокая социальная нагрузка с высоким Дзансин
    if (
      load.scale === LoadScale.MACRO_ENTERPRISE ||
      (breaker.zanshinAwareness >= 0.85 && core.emf >= 80 && load.powerRequirement >= 50)
    ) {
      return TEN_BULLS_CATALOG[TenBullsStage.ENTERING_MARKETPLACE];
    }

    // Если созерцательная микро-нагрузка (чай, дыхание, тишина)
    if (load.scale === LoadScale.MICRO_TEA) {
      if (core.grounding >= 0.88 && bus.innerCriticNoise === 0) {
        return TEN_BULLS_CATALOG[TenBullsStage.BOTH_TRANSCENDED];
      }
      return TEN_BULLS_CATALOG[TenBullsStage.OX_TRANSCENDED];
    }

    // Творческий поток (ремесло, код, инженерия)
    return TEN_BULLS_CATALOG[TenBullsStage.RIDING_HOME];
  }

  // 5. Омический перегрев (мысли о прошлом и будущем)
  if (diagnostic.status === CircuitStatus.OHMIC_OVERHEAT) {
    if (R > 55 || diagnostic.thermalDissipationJoules > 2500) {
      return TEN_BULLS_CATALOG[TenBullsStage.SEEKING_THE_OX];
    }
    // Человек на стенде, видит показатели и осознает причину перегрева
    return TEN_BULLS_CATALOG[TenBullsStage.DISCOVERING_FOOTPRINTS];
  }

  // 6. Номинальный режим цепи (R от 6 до 25 Ом)
  if (R <= 12 && core.grounding >= 0.6) {
    return TEN_BULLS_CATALOG[TenBullsStage.TAMING_THE_OX];
  }

  if (R <= 25) {
    return TEN_BULLS_CATALOG[TenBullsStage.CATCHING_THE_OX];
  }

  return TEN_BULLS_CATALOG[TenBullsStage.DISCOVERING_FOOTPRINTS];
}
