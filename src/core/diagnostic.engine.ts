/**
 * Inner Current (Внутренний ток)
 * Diagnostic Engine & Circuit Fault Classifier
 */

import { CircuitStatus, CanonicalLoadDomain, HumanPainArchetype } from '../types/circuit.types.ts';
import type {
  CircuitTelemetry,
  DiagnosticResult,
  HumanPainDefinition,
  SixBulbPanel,
  SixBulbAnalysis,
  TandenCore
} from '../types/circuit.types.ts';
import {
  KINTSUGI_CIRCUIT_BREAKER_PROTOCOL,
  MICRO_LOAD_TEA_PROTOCOL,
  MUSHIN_GROUNDING_PROTOCOL,
  NIJIRIGUCHI_POLARITY_PROTOCOL
} from './remediation.protocols.ts';

export class DiagnosticEngine {
  /**
   * Evaluates circuit telemetry and classifies system status into exact electrodynamic state.
   */
  public diagnose(telemetry: CircuitTelemetry): DiagnosticResult {
    const { core, bus, load, breaker, durationMinutes } = telemetry;

    // 1. Calculate Effective Resistance (R_eff)
    // Parasitic inductances (past) and capacitances (future) directly add to base resistance
    const rawResistance = bus.baseResistance + bus.parasiticPast + bus.parasiticFuture;
    const noiseMultiplier = 1 + Math.max(0, bus.innerCriticNoise);
    const effectiveResistance = Math.round(rawResistance * noiseMultiplier * 100) / 100;

    // Grounding bonus: strong physical grounding reduces effective resistance by up to 20%
    const groundingFactor = Math.max(0, Math.min(1, core.grounding));
    const finalResistance = Math.max(0, Math.round(effectiveResistance * (1 - 0.2 * groundingFactor) * 100) / 100);

    // 2. Check for OPEN_CIRCUIT (No load connected / idle stagnation)
    if (!load) {
      return {
        status: CircuitStatus.OPEN_CIRCUIT,
        severity: 'WARNING',
        currentAmperes: 0,
        effectiveResistance: finalResistance,
        thermalDissipationJoules: 0,
        superconductivityIndex: 0,
        code: 'ERR_04_OPEN_CIRCUIT',
        headline: 'Обрыв цепи: холостой ход генератора',
        physicsAnalysis: 'Энергия Тандэна застаивается в ядре без полезной нагрузки. Контур разомкнут, ток не течёт (I = 0). Субъективно переживается как апатия, лень и отсутствие вектора жизни.',
        remediationProtocols: MICRO_LOAD_TEA_PROTOCOL
      };
    }

    // 3. Check for REVERSE_POLARITY (Attempting to charge core from the load)
    if (load.expectationOfValidation) {
      const reverseCurrent = -Math.round((load.powerRequirement / (finalResistance + 10)) * 100) / 100;
      const reverseHeat = Math.round(Math.pow(reverseCurrent, 2) * (finalResistance + 50) * durationMinutes);

      return {
        status: CircuitStatus.REVERSE_POLARITY,
        severity: 'CRITICAL',
        currentAmperes: reverseCurrent,
        effectiveResistance: finalResistance,
        thermalDissipationJoules: reverseHeat,
        superconductivityIndex: 0,
        code: 'ERR_02_REVERSE_POLARITY',
        headline: 'Паразитный обратный ток: попытка зарядки от потребителя',
        physicsAnalysis: 'Полярность контура инвертирована. Сознание пытается использовать внешнюю лампу (признание, деньги, одобрение) как генератор. Это глушит Тандэн и раскаляет провода внимания до критических температур.',
        remediationProtocols: NIJIRIGUCHI_POLARITY_PROTOCOL
      };
    }

    // 4. Check for SHORT_CIRCUIT / Load Failure
    if (load.isDamagedOrFailed) {
      const zanshinProtected = breaker.zanshinAwareness >= breaker.tripThreshold;

      return {
        status: CircuitStatus.SHORT_CIRCUIT,
        severity: zanshinProtected ? 'WARNING' : 'CRITICAL',
        currentAmperes: 0,
        effectiveResistance: finalResistance,
        thermalDissipationJoules: zanshinProtected ? 50 : 5000,
        superconductivityIndex: 0.1,
        code: 'ERR_03_SHORT_CIRCUIT',
        headline: zanshinProtected
          ? 'Авария внешней нагрузки: сработал Circuit Breaker (Дзансин)'
          : 'Короткое замыкание: крах внешней опоры без предохранителя',
        physicsAnalysis: zanshinProtected
          ? 'Внешняя нагрузка вышла из строя, но автоматический размыкатель Дзансин вовремя изолировал ядро. Тандэн сохранил целостность, требуется регламент Ваби-саби и восстановительный шов Кинцуги.'
          : 'Катастрофический удар: внешняя нагрузка разрушилась, вызвав короткое замыкание прямо в реакторе из-за отсутствия ментального предохранителя Дзансин.',
        remediationProtocols: KINTSUGI_CIRCUIT_BREAKER_PROTOCOL
      };
    }

    // 5. Calculate Forward Current (I) & Joule-Lenz Thermal Dissipation (Q)
    // Ohm's law: I = EMF / (R_eff + R_load_normalized)
    const loadResistance = Math.max(1, Math.round(load.powerRequirement / 10));
    const totalLoopResistance = finalResistance + loadResistance;
    const currentAmperes = Math.round((core.emf / totalLoopResistance) * 100) / 100;

    // Joule-Lenz Law: Q = I^2 * R * t
    // t converted to relative calculation seconds (durationMinutes * 60)
    const thermalDissipationJoules = Math.round(Math.pow(currentAmperes, 2) * finalResistance * durationMinutes * 10) / 10;

    // Superconductivity index: 1.0 when R -> 0, dropping rapidly as R increases
    const superconductivityIndex = Math.round((1 / (1 + (finalResistance / 8))) * 100) / 100;

    // 6. Check for SUPERCONDUCTING (Mushin Flow state: R -> 0)
    if (finalResistance <= 5 && currentAmperes > 0) {
      return {
        status: CircuitStatus.SUPERCONDUCTING,
        severity: 'OPTIMAL',
        currentAmperes,
        effectiveResistance: finalResistance,
        thermalDissipationJoules: Math.round(Math.pow(currentAmperes, 2) * finalResistance),
        superconductivityIndex: 1.0,
        code: 'OK_00_SUPERCONDUCTING_MUSHIN',
        headline: 'Сверхпроводимость контура: чистое состояние Мусин',
        physicsAnalysis: `Сопротивление проводки упало до нуля (R = ${finalResistance} ≈ 0). Ток реактора без задержек и омических потерь подается прямо в лампочку текущего действия. Субъективно ощущается как глубокий покой, поток и подлинное счастье.`,
        remediationProtocols: []
      };
    }

    // 7. Check for OHMIC_OVERHEAT (Burnout from past/future thoughts)
    if (finalResistance > 25 || thermalDissipationJoules > 1500) {
      return {
        status: CircuitStatus.OHMIC_OVERHEAT,
        severity: finalResistance > 60 ? 'CRITICAL' : 'WARNING',
        currentAmperes,
        effectiveResistance: finalResistance,
        thermalDissipationJoules,
        superconductivityIndex,
        code: 'ERR_01_OHMIC_OVERHEAT',
        headline: 'Омический перегрев проводки: ментальное выгорание',
        physicsAnalysis: `Высокое паразитное сопротивление ума (R = ${finalResistance}) вызвало массивное тепловое рассеивание по закону Джоуля — Ленца (Q = ${thermalDissipationJoules} Дж). Энергия намерения сгорает в трении о мысли о прошлом и будущем, не доходя до полезного действия.`,
        remediationProtocols: MUSHIN_GROUNDING_PROTOCOL
      };
    }

    // 8. Nominal State
    return {
      status: CircuitStatus.NOMINAL,
      severity: 'OPTIMAL',
      currentAmperes,
      effectiveResistance: finalResistance,
      thermalDissipationJoules,
      superconductivityIndex,
      code: 'OK_01_NOMINAL',
      headline: 'Номинальный рабочий режим цепи',
      physicsAnalysis: `Контур функционирует в пределах допустимых допусков (R = ${finalResistance}). Нагрузка запитана, перегрева проводки не наблюдается.`,
      remediationProtocols: []
    };
  }

  /**
   * Анализ балансировки мощности по 6 главным лампочкам контура
   */
  public analyzeSixBulbs(core: TandenCore, panel: SixBulbPanel): SixBulbAnalysis {
    const bulbs = Object.values(panel.bulbs);
    const totalDemandedPower = bulbs.reduce((sum, b) => sum + b.allocatedPower, 0);
    // Доступная мощность реактора (ЭДС * резерв аккумулятора)
    const availablePower = Math.round((core.emf * (core.reserve / 100)) * 100) / 100;
    const isUndervoltage = totalDemandedPower > availablePower;

    const activeBulbs = bulbs.filter(b => b.allocatedPower >= 15);
    const starvedBulbs = bulbs.filter(b => b.allocatedPower < 5).map(b => b.domain);

    let dominantDomain: CanonicalLoadDomain | null = null;
    let maxPower = 0;
    for (const b of bulbs) {
      if (b.allocatedPower > maxPower) {
        maxPower = b.allocatedPower;
        dominantDomain = b.domain;
      }
    }

    const diagnostics: string[] = [];

    if (isUndervoltage) {
      diagnostics.push(
        `🚨 Просадка напряжения (Undervoltage): запрошено ${totalDemandedPower} Вт при доступных ${availablePower} Вт. ` +
        `Все лампы тлеют вполнакала. Рекомендуется обесточить фоновые каналы и сфокусироваться на приоритетных.`
      );
    }

    const reverseLeaking = bulbs.filter(b => b.expectationOfValidation);
    if (reverseLeaking.length > 0) {
      const names = reverseLeaking.map(b => `${b.icon} ${b.name}`).join(', ');
      diagnostics.push(
        `⚠️ Паразитная утечка / Обратный ток на каналах [${names}]: ожидание, что внешняя лампа согреет или зарядит реактор.`
      );
    }

    if (activeBulbs.length === 0) {
      diagnostics.push(
        '🧘 Предупреждение: Активирован «Режим монаха» (все лампы обесточены, 0 / 6). ' +
        'Генератор работает вхолостую (I = 0). Длительное нахождение в этом режиме ведет к застою энергии, социальной изоляции и апатии.'
      );
    } else if (activeBulbs.length >= 4 && !isUndervoltage) {
      diagnostics.push('⚡ Высокоэффективная гармония: мощный реактор устойчиво держит сияние большинства каналов.');
    }

    if (starvedBulbs.includes(CanonicalLoadDomain.HEALTH) && totalDemandedPower > 40) {
      diagnostics.push('🚨 Критический перекос: канал «🩺 Здоровье» обесточен ради форсирования других нагрузок!');
    }

    return {
      totalDemandedPower,
      availablePower,
      isUndervoltage,
      activeBulbsCount: activeBulbs.length,
      dominantDomain,
      starvedDomains: starvedBulbs,
      diagnostics
    };
  }

  /**
   * Pain-First Диагностика: локализация первопричины боли человека в электродинамической цепи
   * и выдача точного инженерного решения (протокола ремонта).
   */
  public diagnosePain(painId: HumanPainArchetype): HumanPainDefinition {
    const definition = PAIN_REGISTRY[painId];
    if (!definition) {
      throw new Error(`Неизвестный архетип человеческой боли: ${painId}`);
    }
    return definition;
  }

  /**
   * Возвращает весь реестр человеческих болей для навигатора и каталога
   */
  public getAllPains(): HumanPainDefinition[] {
    return Object.values(PAIN_REGISTRY);
  }
}

/**
 * Реестр 5 ключевых человеческих болей:
 * Живая фраза ➔ Физика цепи (причина) ➔ Немедленное действие (решение)
 */
export const PAIN_REGISTRY: Record<HumanPainArchetype, HumanPainDefinition> = {
  [HumanPainArchetype.BURNOUT_OVERTHINKING]: {
    id: HumanPainArchetype.BURNOUT_OVERTHINKING,
    humanSymptom: '«Голова кипит, куча мыслей о дедлайнах и прошлых ошибках, хроническая усталость»',
    humanCry: '«Я физически почти ничего тяжелого не делал, но чувствую себя выжатым как лимон. Мысли крутятся без остановки, голова тяжелая.»',
    electrodynamicCause: {
      faultCode: 'ERR_01_OHMIC_OVERHEAT',
      headline: 'Омический перегрев шины внимания (R ≫ 0)',
      physicsLaw: 'Закон Джоуля — Ленца: Q = I² · R · t. Энергия намерения сгорает в трении о виртуальные симуляции, не доходя до полезной нагрузки.',
      affectedNode: 'Шина внимания (нейронная проводка между Тандэном и действием)',
      parameterState: 'R_eff = 25...100+ Ом (высокие реактансы L_past и C_future)',
      explanation: 'Ваше внимание застряло в симуляциях того, чего сейчас физически нет: сожаления о прошлом (L_past) и тревога о будущем (C_future). Проводка раскалена докрасна.'
    },
    remediationSolution: {
      protocolName: 'Протокол «Мусин» (Сенсорное заземление R → 0)',
      actionHeadline: 'Мгновенный сброс сопротивления проводки в ноль',
      immediateAction: 'Отсечь виртуальные ветки времени (t_past → 0, t_future → 0). Перенести 100% фокуса в физические рецепторы тела прямо сейчас.',
      steps: MUSHIN_GROUNDING_PROTOCOL
    }
  },

  [HumanPainArchetype.IMPOSTOR_VALIDATION]: {
    id: HumanPainArchetype.IMPOSTOR_VALIDATION,
    humanSymptom: '«Чувствую себя самозванцем, панически боюсь критики, жду одобрения, откладываю релиз»',
    humanCry: '«Мне кажется, что меня вот-вот разоблачат. Я не могу выпустить проект, пока не буду на 100% уверен, что все будут в восторге.»',
    electrodynamicCause: {
      faultCode: 'ERR_02_REVERSE_POLARITY',
      headline: 'Паразитный обратный ток (I < 0)',
      physicsLaw: 'Закон однонаправленности тока и закон полярности питания. Нагрузка является пассивным потребителем и не имеет собственного генератора.',
      affectedNode: 'Узел подключения внешней нагрузки (инверсия вектора питания)',
      parameterState: 'I < 0 (обратная ЭДС, ток течёт из внешнего мира в ядро)',
      explanation: 'Вы пытаетесь согреться и зарядить свой Тандэн от внешней лампочки (одобрение, деньги, лайки, похвала). Но в лампочке нет генератора! Попытка сосать энергию извне разворачивает ток вспять, глушит реактор и плавит изоляцию.'
    },
    remediationSolution: {
      protocolName: 'Протокол «Нидзиригути» (Сброс эго и разворот полярности)',
      actionHeadline: 'Размыкание обратной линии и разворот вектора тока на отдачу',
      immediateAction: 'Осознать: лампочка не способна вас согреть. Оставить социальный меч у метрового входа и отдавать свет в форму ради чистоты действия.',
      steps: NIJIRIGUCHI_POLARITY_PROTOCOL
    }
  },

  [HumanPainArchetype.COLLAPSE_SHOCK]: {
    id: HumanPainArchetype.COLLAPSE_SHOCK,
    humanSymptom: '«Проект сорвался / бизнес рухнул / меня бросили — земля ушла из-под ног, жизнь кончена»',
    humanCry: '«Всё, во что я вкладывал душу, разбилось вдребезги. Я раздавлен, чувствую полную пустоту и бессилие.»',
    electrodynamicCause: {
      faultCode: 'ERR_03_SHORT_CIRCUIT',
      headline: 'Короткое замыкание при крахе нагрузки без предохранителя',
      physicsLaw: 'Принцип энтропии внешней материи: любые внешние формы бренны и смертны. Без ментального размыкателя авария нагрузки сжигает автономный реактор.',
      affectedNode: 'Защитный модуль цепи (Circuit Breaker)',
      parameterState: 'Breaker DISABLED / zanshinAwareness < tripThreshold',
      explanation: 'Вы припаяли свою личность намертво к внешнему проекту. Когда проект разбился, ударная волна короткого замыкания беспрепятственно ударила прямо в реактор личности.'
    },
    remediationSolution: {
      protocolName: 'Триада «Дзансин + Ваби-саби + Кинцуги»',
      actionHeadline: 'Изоляция аварийного узла и заливка трещины золотом опыта',
      immediateAction: 'Взвести предохранитель Дзансин: отделить себя от погибшего проекта. Принять неидеальность материи (Ваби-саби) и положить золотой шов Кинцуги.',
      steps: KINTSUGI_CIRCUIT_BREAKER_PROTOCOL
    }
  },

  [HumanPainArchetype.APATHY_STAGNATION]: {
    id: HumanPainArchetype.APATHY_STAGNATION,
    humanSymptom: '«Хроническая лень, апатия, нет сил встать с дивана, всё потеряло смысл»',
    humanCry: '«Я просто лежу, листаю ленту, ничего не хочу. Любое действие кажется бессмысленным и неподъемным.»',
    electrodynamicCause: {
      faultCode: 'ERR_04_OPEN_CIRCUIT',
      headline: 'Обрыв цепи / Холостой ход реактора (I = 0)',
      physicsLaw: 'Закон сохранения и циркуляции энергии: потенциал ЭДС без замыкания на полезную нагрузку вызывает застой и внутреннюю коррозию аккумулятора.',
      affectedNode: 'Ключ коммутации цепи (размыкание линии нагрузки)',
      parameterState: 'I = 0 А, P_load = 0 Вт, все каналы обесточены',
      explanation: 'Вы боитесь ошибиться и разомкнули цепь. ЭДС в ядре вырабатывается, но ток не течёт никуда. Нерастраченная энергия застаивается и субъективно переживается как болото апатии и бессмысленности.'
    },
    remediationSolution: {
      protocolName: 'Протокол «Чайный светодиод» (Микронагрузка 10 Вт)',
      actionHeadline: 'Замыкание контура на простейшем сенсорном действии',
      immediateAction: 'Не строить империю. Зажечь один микро-светодиод: заварить чашку чая, помыть чашку, сделать 10 вдохов. Запустить циркуляцию тока I > 0.',
      steps: MICRO_LOAD_TEA_PROTOCOL
    }
  },

  [HumanPainArchetype.OVERLOAD_HEALTH_DRAIN]: {
    id: HumanPainArchetype.OVERLOAD_HEALTH_DRAIN,
    humanSymptom: '«Разрываюсь между делами, здоровье посыпалось, ни на что не хватает сил, всё валится из рук»',
    humanCry: '«Я пытаюсь тащить работу, семью, быт, проекты одновременно, сплю по 4 часа, тело дает сбои, ничего не довожу до конца.»',
    electrodynamicCause: {
      faultCode: 'WARN_05_UNDERVOLTAGE',
      headline: 'Просадка сети (Undervoltage) и обесточивание канала Здоровья',
      physicsLaw: 'Закон сохранения мощности: P_total = sum(P_i). Если суммарный отбор ламп превышает мощность генератора, напряжение сети падает и все лампы тлеют.',
      affectedNode: 'Распределительный щит 6 ламп (шина распределения питания)',
      parameterState: 'P_demanded > P_available, P_health < 5 Вт',
      explanation: 'Вы включили сразу все лампы на максимум при ограниченной емкости аккумулятора. Напряжение просело, нити накала остыли, а канал «Здоровье» полностью обесточен ради карьеры.'
    },
    remediationSolution: {
      protocolName: 'Регламент балансировки щита мощности',
      actionHeadline: 'Принудительное отключение балласта и запитка канала Здоровья',
      immediateAction: 'Обесточить 3–4 второстепенные лампы. Подать гарантированные 20–30 Вт в канал «🩺 Здоровье» (сон, прогулка, вода, питание).',
      steps: [
        { order: 1, title: 'Аварийное отключение балласта', description: 'Снизить мощность второстепенных ламп до нуля.', protocolName: 'SHIELD_TRIM' },
        { order: 2, title: 'Восстановление питания Здоровья', description: 'Подать минимум 20 Вт на сон, физическое тело и питание.', protocolName: 'HEALTH_FEED' },
        { order: 3, title: 'Фокусировка на главном', description: 'Удерживать яркое горение только 1–2 ключевых ламп.', protocolName: 'FOCUS_MONOPOLY' }
      ]
    }
  }
};

