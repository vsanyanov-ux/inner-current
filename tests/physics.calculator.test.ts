import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import {
  calculateEffectiveResistance,
  calculateLoadResistance,
  calculateCurrent,
  calculateJouleLenzHeat,
  calculateSuperconductivityIndex,
  calculateEgoShortCircuit,
  calculateAvailablePower
} from '../src/core/physics.calculator.ts';
import {
  sanitizeNumber,
  normalizeTandenCore,
  normalizeConductanceBus,
  normalizeLoadNode,
  normalizeCircuitBreaker,
  validateAndNormalizeTelemetry
} from '../src/core/telemetry.validator.ts';
import { analyzeSixBulbPanel } from '../src/core/panel.analyzer.ts';
import {
  ZEN_CANON_CATALOG,
  getZenCanonsByLevel,
  getZenCanon
} from '../src/domain/zen.canon.registry.ts';
import {
  createTandenCore,
  createConductanceBus,
  createLoadNode,
  createCircuitBreaker,
  createCircuitTelemetry,
  createDefaultSixBulbPanel
} from '../src/domain/factories.ts';
import {
  BreakerStatus,
  CanonicalLoadDomain,
  ZenOntologyCanon
} from '../src/types/circuit.types.ts';

describe('Inner Current Core Physics & Domain Test Suite', () => {
  describe('1. Pure Physics Calculations', () => {
    it('calculates effective resistance with critic noise and physical grounding bonus', () => {
      // Base: 10, past: 5, future: 5 => raw = 20. Noise = 0.5 => 20 * 1.5 = 30.
      // Grounding = 1.0 => 30 * (1 - 0.2) = 24.
      const bus = { baseResistance: 10, parasiticPast: 5, parasiticFuture: 5, innerCriticNoise: 0.5 };
      const r = calculateEffectiveResistance(bus, 1.0);
      assert.equal(r, 24);

      // Superconductivity (all zero, perfect grounding)
      const zeroBus = { baseResistance: 0, parasiticPast: 0, parasiticFuture: 0, innerCriticNoise: 0 };
      assert.equal(calculateEffectiveResistance(zeroBus, 1.0), 0);
    });

    it('calculates load resistance with minimum lower bound of 1 Ohm', () => {
      assert.equal(calculateLoadResistance(100), 10);
      assert.equal(calculateLoadResistance(10), 1);
      assert.equal(calculateLoadResistance(0), 1);
      assert.equal(calculateLoadResistance(-50), 1);
    });

    it('calculates current via Ohm law with zero-division protection', () => {
      assert.equal(calculateCurrent(80, 20), 4);
      assert.equal(calculateCurrent(80, 0), 0);
      assert.equal(calculateCurrent(0, 10), 0);
    });

    it('calculates Joule-Lenz heat dissipation Q = I^2 * R * t', () => {
      // I = 2 A, R = 10 Ohm, t = 5 min => 4 * 10 * 5 = 200 J
      assert.equal(calculateJouleLenzHeat(2, 10, 5), 200);
      // t = 0 => 0 J
      assert.equal(calculateJouleLenzHeat(5, 50, 0), 0);
    });

    it('calculates superconductivity index correctly', () => {
      assert.equal(calculateSuperconductivityIndex(0), 1.0);
      // R = 8 => 1 / (1 + 1) = 0.5
      assert.equal(calculateSuperconductivityIndex(8), 0.5);
      // R = 24 => 1 / (1 + 3) = 0.25
      assert.equal(calculateSuperconductivityIndex(24), 0.25);
    });

    it('calculates Ego short circuit current and heat', () => {
      const res = calculateEgoShortCircuit(80, 0.5, 20, 10);
      assert.ok(res.internalShortCurrent > 0);
      assert.ok(res.egoHeat > 0);
    });

    it('calculates available power P = EMF * (reserve / 100)', () => {
      assert.equal(calculateAvailablePower(80, 50), 40);
      assert.equal(calculateAvailablePower(100, 100), 100);
      assert.equal(calculateAvailablePower(100, 0), 0);
      assert.equal(calculateAvailablePower(100, 150), 100); // clamped to 100%
    });
  });

  describe('2. Telemetry Validator & Sanitizer', () => {
    it('sanitizes invalid numbers (NaN, Infinity, undefined) and clamps ranges', () => {
      assert.equal(sanitizeNumber(NaN, 10), 10);
      assert.equal(sanitizeNumber(Infinity, 10), 10);
      assert.equal(sanitizeNumber(undefined, 25), 25);
      assert.equal(sanitizeNumber(150, 50, 0, 100), 100);
      assert.equal(sanitizeNumber(-20, 50, 0, 100), 0);
      assert.equal(sanitizeNumber(75, 50, 0, 100), 75);
    });

    it('normalizes core, bus, load and breaker structures', () => {
      const core = normalizeTandenCore({ emf: 120, reserve: -10, grounding: 2.5 });
      assert.equal(core.emf, 100);
      assert.equal(core.reserve, 0);
      assert.equal(core.grounding, 1);

      const bus = normalizeConductanceBus({ baseResistance: -5, innerCriticNoise: 3 });
      assert.equal(bus.baseResistance, 0);
      assert.equal(bus.innerCriticNoise, 1);

      const load = normalizeLoadNode({ powerRequirement: -20, fragility: 1.5 });
      assert.ok(load);
      assert.equal(load.powerRequirement, 0);
      assert.equal(load.fragility, 1);

      const breaker = normalizeCircuitBreaker({ zanshinAwareness: -0.2 });
      assert.equal(breaker.zanshinAwareness, 0);
    });

    it('validates full telemetry object without crashing on empty values', () => {
      const partialTelemetry: any = {
        core: null,
        bus: undefined,
        load: null,
        breaker: null
      };
      const normalized = validateAndNormalizeTelemetry(partialTelemetry);
      assert.equal(normalized.core.emf, 50);
      assert.equal(normalized.load, null);
      assert.equal(normalized.breaker.status, BreakerStatus.ARMED);
    });
  });

  describe('3. Panel Analyzer (6 Bulbs)', () => {
    it('analyzes panel balance, detects undervoltage and health starvation', () => {
      const panel = createDefaultSixBulbPanel({
        [CanonicalLoadDomain.HEALTH]: { allocatedPower: 0 },
        [CanonicalLoadDomain.CAREER]: { allocatedPower: 80, expectationOfValidation: true }
      });
      const core = createTandenCore({ emf: 50, reserve: 50 }); // 25 W available
      const analysis = analyzeSixBulbPanel(core, panel);

      assert.equal(analysis.isUndervoltage, true);
      assert.ok(analysis.starvedDomains.includes(CanonicalLoadDomain.HEALTH));
      assert.equal(analysis.dominantDomain, CanonicalLoadDomain.CAREER);
      assert.ok(analysis.diagnostics.some(d => d.includes('Просадка напряжения')));
      assert.ok(analysis.diagnostics.some(d => d.includes('Замыкание на Эго')));
    });
  });

  describe('4. Zen Canon Registry', () => {
    it('contains all 23 bijective canons with rich metadata', () => {
      const keys = Object.keys(ZEN_CANON_CATALOG);
      assert.equal(keys.length, 23);

      for (const [key, canon] of Object.entries(ZEN_CANON_CATALOG)) {
        assert.equal(canon.id, key);
        assert.ok(canon.kanji.length > 0);
        assert.ok(canon.romaji.length > 0);
        assert.ok(canon.russianName.length > 0);
        assert.ok(canon.level >= 1 && canon.level <= 5);
        assert.ok(canon.electrodynamicAnalogy.length > 5);
        assert.ok(canon.formula.length > 0);
        assert.ok(canon.description.length > 10);
      }
    });

    it('filters canons by ontological level', () => {
      const level1 = getZenCanonsByLevel(1);
      assert.equal(level1.length, 3); // Tanden, Bussho, Shunyata

      const level2 = getZenCanonsByLevel(2);
      assert.equal(level2.length, 5); // Mushin, Fudoshin, Zanshin, Shoshin, Jikishininshin

      const level3 = getZenCanonsByLevel(3);
      assert.equal(level3.length, 4); // Jiga, Makyo, Dukkha, Bonno

      const level4 = getZenCanonsByLevel(4);
      assert.equal(level4.length, 5); // Satori, Koan, Samu, Ichigo Ichie, Nijiriguchi

      const level5 = getZenCanonsByLevel(5);
      assert.equal(level5.length, 6); // Kanso, Wabi-sabi, Kintsugi, Shibumi, Yugen, Fukinzoku
    });

    it('looks up canon by ID or throws on unknown canon', () => {
      const tanden = getZenCanon(ZenOntologyCanon.TANDEN);
      assert.equal(tanden.kanji, '丹田');
      assert.throws(() => getZenCanon('UNKNOWN_CANON' as any));
    });
  });

  describe('5. Entity Factories', () => {
    it('creates default and customized entities', () => {
      const core = createTandenCore({ emf: 99 });
      assert.equal(core.emf, 99);
      assert.equal(core.reserve, 90);

      const bus = createConductanceBus({ baseResistance: 1 });
      assert.equal(bus.baseResistance, 1);

      const load = createLoadNode({ name: 'Тестовая задача' });
      assert.equal(load.name, 'Тестовая задача');

      const telemetry = createCircuitTelemetry({ durationMinutes: 12 });
      assert.equal(telemetry.durationMinutes, 12);
      assert.ok(telemetry.core);
      assert.ok(telemetry.bus);

      const panel = createDefaultSixBulbPanel();
      assert.equal(Object.keys(panel.bulbs).length, 6);
    });
  });
});
