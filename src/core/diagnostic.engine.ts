/**
 * Inner Current (Внутренний ток)
 * Diagnostic Engine & Circuit Fault Classifier
 */

import { CircuitStatus, CanonicalLoadDomain } from '../types/circuit.types.ts';
import type {
  CircuitTelemetry,
  DiagnosticResult,
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
}
