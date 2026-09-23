/**
 * Inner Current (Внутренний ток)
 * Remediation Protocols for Circuit Fault Recovery
 */

import type { RemediationStep } from '../types/circuit.types.ts';

export const MUSHIN_GROUNDING_PROTOCOL: RemediationStep[] = [
  {
    order: 1,
    protocolName: 'MUSHIN_ZERO_RESISTANCE',
    title: 'Выдернуть виртуальные резисторы времени',
    description: 'Мысленно отсечь виртуальные ветки прошлого (сожаления) и будущего (тревога). Запрет на обслуживание симуляций: t_past → 0, t_future → 0.'
  },
  {
    order: 2,
    protocolName: 'MUSHIN_ZERO_RESISTANCE',
    title: 'Заземление сенсорного тракта',
    description: 'Перевести 100% фокуса на физические рецепторы: почувствовать давление подошв на пол, температуру воздуха, вес ладоней на столе.'
  },
  {
    order: 3,
    protocolName: 'MUSHIN_ZERO_RESISTANCE',
    title: 'Синхронизация дыхания с Тандэном',
    description: 'Три глубоких диафрагмальных цикла с концентрацией в точке на 4 см ниже пупка. Падение R до нуля и чистая подача мощности в текущее движение.'
  }
];

export const NIJIRIGUCHI_POLARITY_PROTOCOL: RemediationStep[] = [
  {
    order: 1,
    protocolName: 'NIJIRIGUCHI_SEVER_EGO_LOOP',
    title: 'Размыкание паразитной петли Эго и осознание Шуньяты',
    description: 'Осознать физический закон: внешняя лампочка (деньги, похвала, метрики) пуста (E_load = 0). В ней нет накопленного заряда. Ожидание валидации лишь закольцовывает ток внутрь на себя.'
  },
  {
    order: 2,
    protocolName: 'NIJIRIGUCHI_SEVER_EGO_LOOP',
    title: 'Проход через низкий портал Нидзиригути',
    description: 'Оставить за порогом комнаты мечи, социальный статус, регалии и страх оценки. Подойти к работе на коленях — как чистый ученик.'
  },
  {
    order: 3,
    protocolName: 'NIJIRIGUCHI_SEVER_EGO_LOOP',
    title: 'Подача прямого тока в форму',
    description: 'Направить ток от Тандэна напрямую в лампу ремесла ради чистоты действия, без петли эго-рефлексии.'
  }
];

export const KINTSUGI_CIRCUIT_BREAKER_PROTOCOL: RemediationStep[] = [
  {
    order: 1,
    protocolName: 'KINTSUGI_ZANSHIN_RECOVERY',
    title: 'Активация аварийного размыкателя Дзансин',
    description: 'Изолировать сбойный внешний узел. Убедиться, что падение проекта не затрагивает целостность Тандэна: внешняя форма смертна, генератор автономен.'
  },
  {
    order: 2,
    protocolName: 'KINTSUGI_ZANSHIN_RECOVERY',
    title: 'Принятие Ваби-саби (Неидеальность материи)',
    description: 'Признать скол или трещину естественным законом энтропии. Отказ от истерики и обвинений.'
  },
  {
    order: 3,
    protocolName: 'KINTSUGI_ZANSHIN_RECOVERY',
    title: 'Золотой шов Кинцуги',
    description: 'Залить трещину золотом архитектурного анализа: извлечь телеметрический урок из ошибки и продолжить подачу тока в новую форму.'
  }
];

export const CHANOYU_TEA_PROTOCOL: RemediationStep[] = [
  {
    order: 1,
    protocolName: 'CHANOYU_MICRO_ACTION',
    title: 'Запрет на запуск мегаваттных нагрузок',
    description: 'При обрыве цепи запрещено браться за глобальные империи. Это вызовет лишь прокрастинацию и холодный ступор.'
  },
  {
    order: 2,
    protocolName: 'CHANOYU_MICRO_ACTION',
    title: 'Ритуал Тяною (茶の湯): заваривание одной чашки',
    description: 'Выбрать предельно простое физическое действие: заварить чашку чая, помыть кружку, написать 3 строки чистого кода.'
  },
  {
    order: 3,
    protocolName: 'CHANOYU_MICRO_ACTION',
    title: 'Замыкание контура и запуск тока (I > 0)',
    description: 'Выполнить действие с идеальным присутствием Мусин. Как только микро-нагрузка загорится — плавно повышать ток.'
  }
];

// Alias for backwards compatibility
export const MICRO_LOAD_TEA_PROTOCOL = CHANOYU_TEA_PROTOCOL;

export const KANSO_SHIELD_BALANCING_PROTOCOL: RemediationStep[] = [
  {
    order: 1,
    protocolName: 'KANSO_TRIM_BALAST',
    title: 'Отсечение избытка Кансо (簡素)',
    description: 'Безжалостно обесточить второстепенные каналы щита. Отключить балластные потребители, устранить распыление энергии.'
  },
  {
    order: 2,
    protocolName: 'KANSO_HEALTH_PRIORITY',
    title: 'Восстановление шины Здоровья',
    description: 'Подать гарантированные 20–30 Вт в критический канал «🩺 Здоровье» (сон, вода, дыхание, прогулка). Без реактора тела все остальные лампы бессмысленны.'
  },
  {
    order: 3,
    protocolName: 'CHOWA_MONOPOLY_FOCUS',
    title: 'Достижение баланса Тёва (調和)',
    description: 'Удерживать яркое горение только 1–2 ключевых ламп в единицу времени. Перевести нагрузку из хаотичного перегруза в гармоничный последовательный резонанс.'
  }
];
