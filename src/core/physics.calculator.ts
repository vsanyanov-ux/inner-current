/**
 * Inner Current (Внутренний ток)
 * Pure Electrodynamic Physics Calculator (Законы Ома, Джоуля — Ленца и Кирхгофа)
 * 
 * Данный модуль содержит чистые функции расчёта без состояния (принцип Тандэн).
 */

import type { ConductanceBus } from '../types/circuit.types.ts';

/**
 * Расчёт эффективного сопротивления проводки внимания (R_eff).
 * Паразитные индуктивности (прошлое) и емкости (будущее) суммируются с базовым сопротивлением,
 * масштабируются шумом внутреннего критика и снижаются за счёт физического заземления (до 20%).
 */
export function calculateEffectiveResistance(bus: ConductanceBus, grounding: number): number {
  const base = Math.max(0, bus.baseResistance);
  const past = Math.max(0, bus.parasiticPast);
  const future = Math.max(0, bus.parasiticFuture);
  const rawResistance = base + past + future;

  const noiseMultiplier = 1 + Math.max(0, bus.innerCriticNoise);
  const effectiveResistance = Math.round(rawResistance * noiseMultiplier * 100) / 100;

  const groundingFactor = Math.max(0, Math.min(1, grounding));
  return Math.max(0, Math.round(effectiveResistance * (1 - 0.2 * groundingFactor) * 100) / 100);
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
