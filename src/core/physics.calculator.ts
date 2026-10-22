/**
 * Inner Current (Внутренний ток)
 * Pure Electrodynamic Physics Calculator (Законы Ома, Джоуля — Ленца и Кирхгофа)
 * 
 * Данный модуль содержит чистые функции расчёта без состояния (принцип Тандэн).
 */

import {
  ResistanceVector,
  type ConductanceBus,
  type EgoResistanceTriad,
  type BiometricNetworkTelemetry,
  type BiometricHappinessEvaluation
} from '../types/circuit.types.ts';

/**
 * Расчёт эффективного сопротивления проводки внимания (R_eff).
 * Паразитные индуктивности (прошлое / вина), емкости (будущее / контроль)
 * и делители напряжения (люди / одобрение) суммируются с базовым сопротивлением,
 * масштабируются шумом внутреннего критика и снижаются за счёт физического заземления (до 20%).
 */
export function calculateEffectiveResistance(bus: ConductanceBus, grounding: number): number {
  const base = Math.max(0, bus.baseResistance);
  const past = Math.max(0, bus.parasiticPast);
  const future = Math.max(0, bus.parasiticFuture);
  const approval = Math.max(0, bus.parasiticApproval ?? 0);
  const rawResistance = base + past + future + approval;

  const noiseMultiplier = 1 + Math.max(0, bus.innerCriticNoise);
  const effectiveResistance = Math.round(rawResistance * noiseMultiplier * 100) / 100;

  const groundingFactor = Math.max(0, Math.min(1, grounding));
  return Math.max(0, Math.round(effectiveResistance * (1 - 0.2 * groundingFactor) * 100) / 100);
}

/**
 * Анализирует триаду омического сопротивления эго (Глава 246):
 * Вина (прошлое), Контроль (будущее), Одобрение (мнение людей).
 */
export function analyzeEgoResistanceTriad(bus: ConductanceBus): EgoResistanceTriad {
  const guiltPast = Math.max(0, bus.parasiticPast);
  const controlFuture = Math.max(0, bus.parasiticFuture);
  const approvalPeople = Math.max(0, bus.parasiticApproval ?? 0);
  const totalEgoResistance = guiltPast + controlFuture + approvalPeople;

  let dominantVector: ResistanceVector | null = null;
  if (totalEgoResistance > 0) {
    if (guiltPast >= controlFuture && guiltPast >= approvalPeople) {
      dominantVector = ResistanceVector.GUILT_PAST;
    } else if (controlFuture >= guiltPast && controlFuture >= approvalPeople) {
      dominantVector = ResistanceVector.CONTROL_FUTURE;
    } else {
      dominantVector = ResistanceVector.APPROVAL_PEOPLE;
    }
  }

  return {
    guiltPast,
    controlFuture,
    approvalPeople,
    totalEgoResistance,
    dominantVector
  };
}

/**
 * Расчёт эквивалентного сопротивления внешней нагрузки по потребляемой мощности (Вт).
 */
export function calculateLoadResistance(powerRequirement: number): number {
  return Math.max(1, Math.round(Math.max(0, powerRequirement) / 10));
}

/**
 * Закон Ома для полной цепи: I = E / (R_проводки + R_нагрузки).
 * Возвращает силу полезного тока в амперах (с защитой от деления на 0).
 */
export function calculateCurrent(emf: number, totalResistance: number): number {
  if (totalResistance <= 0) return 0;
  return Math.round((Math.max(0, emf) / totalResistance) * 100) / 100;
}

/**
 * Закон Джоуля — Ленца: Q = I² · R · t (тепловое рассеяние в джоулях).
 * t переводится в секунды вычисления (durationMinutes * 10 для скейлинга модели).
 */
export function calculateJouleLenzHeat(
  currentAmperes: number,
  resistance: number,
  durationMinutes: number
): number {
  const t = Math.max(0, durationMinutes);
  const r = Math.max(0, resistance);
  return Math.round(Math.pow(currentAmperes, 2) * r * t * 10) / 10;
}

/**
 * Коэффициент сверхпроводимости потока Мусин (от 0 до 1.0).
 * При R -> 0 стремится к 1.0 (ламинарный поток чистой энергии).
 */
export function calculateSuperconductivityIndex(effectiveResistance: number): number {
  const r = Math.max(0, effectiveResistance);
  return Math.round((1 / (1 + (r / 8))) * 100) / 100;
}

/**
 * Расчёт параметров внутреннего короткого замыкания на паразитной петле Эго (Дзига).
 * Нагрузка пуста (Шуньята), полезный ток I_load = 0,
 * весь ток замыкается через внутренний шунт, вызывая лавинообразный нагрев.
 */
export function calculateEgoShortCircuit(
  emf: number,
  grounding: number,
  finalResistance: number,
  durationMinutes: number
): { internalShortCurrent: number; egoHeat: number } {
  const egoLoopResistance = 10;
  const clampedGrounding = Math.max(0, Math.min(1, grounding));
  const internalResistance = egoLoopResistance + (1 - clampedGrounding) * 20;

  const internalShortCurrent = Math.round((Math.max(0, emf) / internalResistance) * 100) / 100;
  const egoHeat = Math.round(
    Math.pow(internalShortCurrent, 2) * (Math.max(0, finalResistance) + 50) * Math.max(0, durationMinutes)
  );

  return { internalShortCurrent, egoHeat };
}

/**
 * Расчёт доступной мощности генератора Тандэн (Вт).
 * P_avail = ЭДС · (Запас аккумулятора / 100).
 */
export function calculateAvailablePower(emf: number, reservePercent: number): number {
  const clampedReserve = Math.max(0, Math.min(100, reservePercent));
  return Math.round((Math.max(0, emf) * (clampedReserve / 100)) * 100) / 100;
}

/**
 * Оценка состояния единой биометрической сети и расчёт индекса счастья H_bio (Глава 254).
 * Формула: H_bio = K_sleep · (SpO2 / 100) · (1 - Stress / 100) · eta_cardio
 */
export function evaluateBiometricNetwork(
  biometrics: BiometricNetworkTelemetry
): BiometricHappinessEvaluation {
  // 1. Коэффициент восстановления сна (номинал 7.5 ч)
  const sleepHours = Math.max(0, Math.min(14, biometrics.sleepHours));
  const sleepQuality = Math.max(0, Math.min(1.0, biometrics.sleepQuality ?? 0.9));
  const sleepRatio = Math.min(1.0, sleepHours / 7.5);
  const sleepBatteryCoefficient = Math.round(sleepRatio * sleepQuality * 100) / 100;

  // 2. Фактор оксигенации митохондрий (SpO2)
  const spO2 = Math.max(50, Math.min(100, biometrics.spO2Percentage));
  let oxygenConductivityFactor = 1.0;
  if (spO2 >= 98) {
    oxygenConductivityFactor = 1.0;
  } else if (spO2 >= 94) {
    oxygenConductivityFactor = Math.round((spO2 / 98) * 100) / 100;
  } else {
    // Резкий штраф при тканевой гипоксии (панический контур ствола мозга)
    oxygenConductivityFactor = Math.max(0.2, Math.round(Math.pow(spO2 / 98, 3) * 100) / 100);
  }

  // 3. Вагусная проводимость (1 - Stress / 100)
  const stress = Math.max(0, Math.min(100, biometrics.stressLevel));
  const vagusConductivity = Math.round((1 - stress / 100) * 100) / 100;

  // 4. Кардиодинамическая эффективность (номинальный пульс покоя 55 - 75 уд/мин)
  const bpm = Math.max(30, Math.min(220, biometrics.heartRateBpm));
  let cardioEfficiency = 1.0;
  if (bpm >= 50 && bpm <= 75) {
    cardioEfficiency = 1.0;
  } else if (bpm > 75 && bpm <= 100) {
    cardioEfficiency = Math.max(0.5, Math.round((1 - (bpm - 75) / 50) * 100) / 100);
  } else if (bpm > 100) {
    cardioEfficiency = Math.max(0.2, Math.round((1 - (bpm - 75) / 40) * 100) / 100);
  } else {
    // bpm < 50
    cardioEfficiency = bpm >= 45 ? 0.95 : 0.85;
  }

  // Общий интегральный индекс H_bio
  const rawIndex =
    sleepBatteryCoefficient *
    oxygenConductivityFactor *
    vagusConductivity *
    cardioEfficiency;
  const biocircuitHappinessIndex = Math.max(0, Math.min(1.0, Math.round(rawIndex * 100) / 100));

  // Зона проводимости цепи
  let zone: 'SUPERCONDUCTING' | 'NOMINAL' | 'OHMIC_OVERHEAT' = 'NOMINAL';
  if (biocircuitHappinessIndex >= 0.75) {
    zone = 'SUPERCONDUCTING';
  } else if (biocircuitHappinessIndex < 0.40) {
    zone = 'OHMIC_OVERHEAT';
  }

  // Инженерная подсказка оператору
  let operatorGuidance = '';
  if (zone === 'SUPERCONDUCTING') {
    operatorGuidance =
      '⚡ Единая биосеть в режиме сверхпроводимости! Ламинарный ток внимания, ясный кристалл проводника.';
  } else if (sleepBatteryCoefficient < 0.6) {
    operatorGuidance =
      '🔋 Батарея сна разряжена. Не форсируйте нагрузку волевым кнутом — сначала восстановите ЭДС сном и покоем.';
  } else if (stress > 60) {
    operatorGuidance =
      '🔥 Высокое омическое сопротивление зажима блуждающего нерва (HRV). 3 диафрагмальных выдоха и сброс в Тандэн.';
  } else if (oxygenConductivityFactor < 0.9) {
    operatorGuidance =
      '🫁 Тканевая гипоксия снижает проводимость митохондрий. Проветрите помещение и сделайте дыхательную паузу.';
  } else {
    operatorGuidance =
      '⚖️ Рабочий номинал цепи. Поддерживайте ровный фокус без форсирования ЧСС.';
  }

  return {
    biocircuitHappinessIndex,
    zone,
    sleepBatteryCoefficient,
    oxygenConductivityFactor,
    vagusConductivity,
    cardioEfficiency,
    operatorGuidance
  };
}

