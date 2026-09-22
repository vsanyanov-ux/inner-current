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
    protocolName: 'NIJIRIGUCHI_SEVER_REVERSE',
    title: 'Размыкание обратной линии питания',
    description: 'Осознать физический закон: внешняя лампочка (деньги, похвала, метрики) является ПОТРЕБИТЕЛЕМ, в ней нет встроенного генератора.'
  },
  {
    order: 2,
    protocolName: 'NIJIRIGUCHI_SEVER_REVERSE',
    title: 'Проход через низкий портал Нидзиригути',
    description: 'Оставить за порогом комнаты мечи, социальный статус, регалии и страх оценки. Подойти к работе на коленях — как чистый ученик.'
  },
  {
    order: 3,
    protocolName: 'NIJIRIGUCHI_SEVER_REVERSE',
    title: 'Разворот вектора тока',
    description: 'Переключить полярность: отдавать качество и свет в проект ради совершенства формы, а не ради подзарядки своего эго.'
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

export const MICRO_LOAD_TEA_PROTOCOL: RemediationStep[] = [
  {
    order: 1,
    protocolName: 'MICRO_LOAD_CALIBRATION',
    title: 'Запрет на запуск мегаваттных нагрузок',
    description: 'При обрыве цепи запрещено браться за глобальные империи. Это вызовет лишь прокрастинацию и холодный ступор.'
  },
  {
    order: 2,
    protocolName: 'MICRO_LOAD_CALIBRATION',
    title: 'Подключение низковольтного светодиода (Чай)',
    description: 'Выбрать предельно простое физическое действие: заварить чашку чая, помыть кружку, написать 3 строки чистого кода.'
  },
  {
    order: 3,
    protocolName: 'MICRO_LOAD_CALIBRATION',
    title: 'Калибровка сверхпроводимости на малом токе',
    description: 'Выполнить действие с идеальным присутствием Мусин. Как только светодиод загорится — плавно повышать нагрузку.'
  }
];
