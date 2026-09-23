/**
 * Inner Current (Внутренний ток)
 * Pain-First Registry: 5 ключевых архетипов человеческой боли
 * 
 * Живой симптом ➔ Электродинамическая причина сбоя ➔ Немедленное действие и пошаговый протокол.
 */

import { HumanPainArchetype } from '../types/circuit.types.ts';
import type { HumanPainDefinition } from '../types/circuit.types.ts';
import {
  CHANOYU_TEA_PROTOCOL,
  KANSO_SHIELD_BALANCING_PROTOCOL,
  KINTSUGI_CIRCUIT_BREAKER_PROTOCOL,
  MUSHIN_GROUNDING_PROTOCOL,
  NIJIRIGUCHI_POLARITY_PROTOCOL
} from '../core/remediation.protocols.ts';

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
      protocolName: 'Протокол «Мусин» (無心, Mushin — Сенсорное заземление R → 0)',
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
      faultCode: 'ERR_02_EGO_SHORT_CIRCUIT',
      headline: 'Короткое замыкание на Эго / Иллюзия внешнего источника (Ego Short Circuit)',
      physicsLaw: 'Закон пустотности нагрузки (Шуньята): E_load = 0, I_in = I_out. Лампочка — пассивный рассеиватель мощности, а не аккумулятор. Ожидание валидации закольцовывает внимание на себя.',
      affectedNode: 'Внутренний шунт внимания (паразитный контур Дзига)',
      parameterState: 'I_load = 0, I_КЗ = E_tanden / r_int (внутренний перегрев)',
      explanation: 'Вы ожидаете, что внешняя лампа (одобрение, деньги, лайки) подтвердит вашу состоятельность. Но лампа пуста: она лишь потребляет энергию. Внимание замыкается в петлю эго-рефлексии («А как меня оценят?»), порождая ток внутреннего КЗ, который кипятит нервную систему, пока ремесло остаётся тёмным.'
    },
    remediationSolution: {
      protocolName: 'Протокол «Нидзиригути» (躙口, Nijiriguchi — Размыкание петли эго и отдача)',
      actionHeadline: 'Размыкание паразитной петли Эго и подача прямого тока в форму',
      immediateAction: 'Осознать: лампочка пуста, в ней нет питания. Оставить социальный меч у метрового лаза Нидзиригути и направить чистый ток прямо в действие без рефлексии.',
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
      protocolName: 'Протокол «Кинцуги» (金継ぎ, Kintsugi — Дзансин-предохранитель и золотой шов)',
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
      protocolName: 'Протокол «Тяною» (茶の湯, Chanoyu — Искусство чая / Микронагрузка 10 Вт)',
      actionHeadline: 'Замыкание контура на простейшем сенсорном действии',
      immediateAction: 'Не строить империю. Зажечь один микро-светодиод: заварить чашку чая, помыть чашку, сделать 10 вдохов. Запустить циркуляцию тока I > 0.',
      steps: CHANOYU_TEA_PROTOCOL
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
      protocolName: 'Протокол «Кансо» (簡素, Kanso — Отсечение избытка и гармония щита Тёва)',
      actionHeadline: 'Принудительное отключение балласта и запитка канала Здоровья',
      immediateAction: 'Обесточить 3–4 второстепенные лампы. Подать гарантированные 20–30 Вт в канал «🩺 Здоровье» (сон, прогулка, вода, питание).',
      steps: KANSO_SHIELD_BALANCING_PROTOCOL
    }
  }
};
