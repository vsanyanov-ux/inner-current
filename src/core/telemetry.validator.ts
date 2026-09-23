/**
 * Inner Current (Внутренний ток)
 * Telemetry Validator & Sanitizer (Канон Мусин: защита от искажений и шума)
 */

import { BreakerStatus } from '../types/circuit.types.ts';
import type {
  CircuitTelemetry,
  TandenCore,
  ConductanceBus,
  LoadNode,
  CircuitBreaker
} from '../types/circuit.types.ts';

/**
 * Безопасное приведение значения к числу с клампингом и дефолтным значением при NaN/невалидности.
 */
export function sanitizeNumber(
  val: unknown,
  defaultValue: number,
  min: number = -Infinity,
  max: number = Infinity
): number {
  if (typeof val !== 'number' || Number.isNaN(val) || !Number.isFinite(val)) {
    return defaultValue;
  }
  return Math.max(min, Math.min(max, val));
}

/**
 * Нормализует параметры генератора Тандэн в допустимые пределы:
 * emf: [0, 100], reserve: [0, 100], grounding: [0, 1]
 */
export function normalizeTandenCore(core: Partial<TandenCore> | null | undefined): TandenCore {
  return {
    emf: sanitizeNumber(core?.emf, 50, 0, 100),
    reserve: sanitizeNumber(core?.reserve, 50, 0, 100),
    grounding: sanitizeNumber(core?.grounding, 0.5, 0, 1)
  };
}

/**
 * Нормализует параметры шины внимания:
 * baseResistance: >= 0, parasiticPast: >= 0, parasiticFuture: >= 0, innerCriticNoise: >= 0
 */
export function normalizeConductanceBus(bus: Partial<ConductanceBus> | null | undefined): ConductanceBus {
  return {
    baseResistance: sanitizeNumber(bus?.baseResistance, 10, 0),
    parasiticPast: sanitizeNumber(bus?.parasiticPast, 0, 0),
    parasiticFuture: sanitizeNumber(bus?.parasiticFuture, 0, 0),
    innerCriticNoise: sanitizeNumber(bus?.innerCriticNoise, 0, 0, 1)
  };
}

/**
 * Нормализует параметры внешнего потребителя (LoadNode).
 */
export function normalizeLoadNode(load: Partial<LoadNode> | null | undefined): LoadNode | null {
  if (!load) return null;
  return {
    id: String(load.id || 'anonymous-load'),
    name: String(load.name || 'Безымянная задача'),
    scale: load.scale || 'MICRO_TEA',
    domain: load.domain,
    powerRequirement: sanitizeNumber(load.powerRequirement, 10, 0),
    fragility: sanitizeNumber(load.fragility, 0.5, 0, 1),
    isDamagedOrFailed: Boolean(load.isDamagedOrFailed),
    expectationOfValidation: Boolean(load.expectationOfValidation)
  };
}

/**
 * Нормализует параметры автоматического размыкателя Дзансин (CircuitBreaker).
 */
export function normalizeCircuitBreaker(breaker: Partial<CircuitBreaker> | null | undefined): CircuitBreaker {
  return {
    status: breaker?.status || BreakerStatus.ARMED,
    zanshinAwareness: sanitizeNumber(breaker?.zanshinAwareness, 0.5, 0, 1),
    tripThreshold: sanitizeNumber(breaker?.tripThreshold, 0.5, 0, 1)
  };
}

/**
 * Полная защитная нормализация телеметрии перед расчётом.
 */
export function validateAndNormalizeTelemetry(telemetry: CircuitTelemetry): CircuitTelemetry {
  return {
    timestamp: sanitizeNumber(telemetry.timestamp, Date.now(), 0),
    core: normalizeTandenCore(telemetry.core),
    bus: normalizeConductanceBus(telemetry.bus),
    load: normalizeLoadNode(telemetry.load),
    breaker: normalizeCircuitBreaker(telemetry.breaker),
    durationMinutes: sanitizeNumber(telemetry.durationMinutes, 1, 0)
  };
}
