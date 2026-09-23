/**
 * Inner Current (Внутренний ток)
 * Domain Entity Factories & Builders (Канон Кансо: лаконичность и типобезопасность)
 */

import {
  BreakerStatus,
  LoadScale,
  CanonicalLoadDomain
} from '../types/circuit.types.ts';
import type {
  TandenCore,
  ConductanceBus,
  LoadNode,
  CircuitBreaker,
  CircuitTelemetry,
  SixBulbPanel,
  BulbChannel
} from '../types/circuit.types.ts';

/**
 * Создаёт автономный генератор Тандэн с возможностью переопределения параметров.
 */
export function createTandenCore(partial: Partial<TandenCore> = {}): TandenCore {
  return {
    emf: 80,
    reserve: 90,
    grounding: 0.8,
    ...partial
  };
}

/**
 * Создаёт шину внимания с возможностью переопределения параметров.
 */
export function createConductanceBus(partial: Partial<ConductanceBus> = {}): ConductanceBus {
  return {
    baseResistance: 5,
    parasiticPast: 0,
    parasiticFuture: 0,
    innerCriticNoise: 0,
    ...partial
  };
}

/**
 * Создаёт узел нагрузки с возможностью переопределения параметров.
 */
export function createLoadNode(partial: Partial<LoadNode> = {}): LoadNode {
  return {
    id: 'sample-load',
    name: 'Каноническое действие',
    scale: LoadScale.MICRO_TEA,
    powerRequirement: 10,
    fragility: 0.5,
    isDamagedOrFailed: false,
    expectationOfValidation: false,
    ...partial
  };
}

/**
 * Создаёт модуль защиты Дзансин с возможностью переопределения параметров.
 */
export function createCircuitBreaker(partial: Partial<CircuitBreaker> = {}): CircuitBreaker {
  return {
    status: BreakerStatus.ARMED,
    zanshinAwareness: 0.9,
    tripThreshold: 0.5,
    ...partial
  };
}

/**
 * Создаёт полный снимок телеметрии цепи.
 */
export function createCircuitTelemetry(partial: Partial<CircuitTelemetry> = {}): CircuitTelemetry {
  return {
    timestamp: Date.now(),
    core: createTandenCore(partial.core),
    bus: createConductanceBus(partial.bus),
    load: partial.load !== undefined ? partial.load : createLoadNode(),
    breaker: createCircuitBreaker(partial.breaker),
    durationMinutes: partial.durationMinutes ?? 5
  };
}

/**
 * Создаёт 6-канальный распределительный щит со стандартными лампами.
 */
export function createDefaultSixBulbPanel(
  overrides: Partial<Record<CanonicalLoadDomain, Partial<BulbChannel>>> = {}
): SixBulbPanel {
  const defaults: Record<CanonicalLoadDomain, BulbChannel> = {
    [CanonicalLoadDomain.CAR]: {
      domain: CanonicalLoadDomain.CAR,
      name: 'Машина',
      icon: '🚗',
      allocatedPower: 20,
      expectationOfValidation: false
    },
    [CanonicalLoadDomain.HOME]: {
      domain: CanonicalLoadDomain.HOME,
      name: 'Дом',
      icon: '🏡',
      allocatedPower: 20,
      expectationOfValidation: false
    },
    [CanonicalLoadDomain.CAREER]: {
      domain: CanonicalLoadDomain.CAREER,
      name: 'Карьера',
      icon: '💼',
      allocatedPower: 40,
      expectationOfValidation: false
    },
    [CanonicalLoadDomain.RELATIONSHIPS]: {
      domain: CanonicalLoadDomain.RELATIONSHIPS,
      name: 'Отношения',
      icon: '❤️',
      allocatedPower: 20,
      expectationOfValidation: false
    },
    [CanonicalLoadDomain.HEALTH]: {
      domain: CanonicalLoadDomain.HEALTH,
      name: 'Здоровье',
      icon: '🩺',
      allocatedPower: 25,
      expectationOfValidation: false
    },
    [CanonicalLoadDomain.ENTERTAINMENT]: {
      domain: CanonicalLoadDomain.ENTERTAINMENT,
      name: 'Развлечения',
      icon: '🎉',
      allocatedPower: 15,
      expectationOfValidation: false
    }
  };

  for (const domain of Object.keys(overrides) as CanonicalLoadDomain[]) {
    if (overrides[domain]) {
      defaults[domain] = { ...defaults[domain], ...overrides[domain] };
    }
  }

  return { bulbs: defaults };
}
