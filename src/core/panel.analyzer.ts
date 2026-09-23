/**
 * Inner Current (Внутренний ток)
 * 6-Bulb Load Panel Analyzer (Анализ распределительного щита нагрузок)
 */

import { CanonicalLoadDomain } from '../types/circuit.types.ts';
import type { TandenCore, SixBulbPanel, SixBulbAnalysis } from '../types/circuit.types.ts';
import { calculateAvailablePower } from './physics.calculator.ts';

/**
 * Анализирует балансировку мощности по 6 жизненным нагрузкам (Канон Кансо и Тёва):
 * Выявляет просадку сети (undervoltage), замыкания на Эго, голодание критических сфер и режим монаха.
 */
export function analyzeSixBulbPanel(core: TandenCore, panel: SixBulbPanel): SixBulbAnalysis {
  const bulbs = Object.values(panel.bulbs);
  const totalDemandedPower = bulbs.reduce((sum, b) => sum + (Math.max(0, b.allocatedPower) || 0), 0);
  const availablePower = calculateAvailablePower(core.emf, core.reserve);
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

  const egoShunted = bulbs.filter(b => b.expectationOfValidation);
  if (egoShunted.length > 0) {
    const names = egoShunted.map(b => `${b.icon} ${b.name}`).join(', ');
    diagnostics.push(
      `⚠️ Замыкание на Эго на каналах [${names}]: ожидание, что пустая лампа подтвердит ценность реактора. Полезный ток блокирован.`
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
