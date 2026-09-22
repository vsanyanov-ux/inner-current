import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { DiagnosticEngine } from '../src/core/diagnostic.engine.ts';
import {
  BreakerStatus,
  CircuitStatus,
  LoadScale,
  CanonicalLoadDomain
} from '../src/types/circuit.types.ts';
import type { CircuitTelemetry, SixBulbPanel } from '../src/types/circuit.types.ts';

describe('Inner Current Diagnostic Engine Test Suite', () => {
  const engine = new DiagnosticEngine();

  const baseCore = {
    emf: 80,
    reserve: 90,
    grounding: 0.8
  };

  const baseBreaker = {
    status: BreakerStatus.ARMED,
    zanshinAwareness: 0.9,
    tripThreshold: 0.5
  };

  it('1. Detects pure Superconductivity (Mushin state, R -> 0)', () => {
    const telemetry: CircuitTelemetry = {
      timestamp: Date.now(),
      core: baseCore,
      bus: {
        baseResistance: 1,
        parasiticPast: 0,
        parasiticFuture: 0,
        innerCriticNoise: 0
      },
      load: {
        id: 'tea-01',
        name: 'Чашка зелёного чая (Сэнтя)',
        scale: LoadScale.MICRO_TEA,
        powerRequirement: 10,
        fragility: 0.7,
        isDamagedOrFailed: false,
        expectationOfValidation: false
      },
      breaker: baseBreaker,
      durationMinutes: 10
    };

    const result = engine.diagnose(telemetry);

    assert.equal(result.status, CircuitStatus.SUPERCONDUCTING);
    assert.equal(result.severity, 'OPTIMAL');
    assert.equal(result.code, 'OK_00_SUPERCONDUCTING_MUSHIN');
    assert.equal(result.superconductivityIndex, 1.0);
    assert.ok(result.currentAmperes > 0);
    assert.ok(result.effectiveResistance <= 5);
    assert.equal(result.remediationProtocols.length, 0);
  });

  it('2. Detects Ohmic Overheat (Burnout via Joule-Lenz law: Q = I^2 * R * t)', () => {
    const telemetry: CircuitTelemetry = {
      timestamp: Date.now(),
      core: baseCore,
      bus: {
        baseResistance: 15,
        parasiticPast: 25,     // Heavy regrets
        parasiticFuture: 30,   // High anxiety
        innerCriticNoise: 0.5  // Severe self-criticism
      },
      load: {
        id: 'work-01',
        name: 'Квартальный отчет',
        scale: LoadScale.FLOW_CODE,
        powerRequirement: 30,
        fragility: 0.3,
        isDamagedOrFailed: false,
        expectationOfValidation: false
      },
      breaker: baseBreaker,
      durationMinutes: 45
    };

    const result = engine.diagnose(telemetry);

    assert.equal(result.status, CircuitStatus.OHMIC_OVERHEAT);
    assert.equal(result.code, 'ERR_01_OHMIC_OVERHEAT');
    assert.ok(result.effectiveResistance > 50);
    assert.ok(result.thermalDissipationJoules > 1000);
    assert.equal(result.remediationProtocols[0].protocolName, 'MUSHIN_ZERO_RESISTANCE');
  });

  it('3. Detects Reverse Polarity (Attempting to charge core from load)', () => {
    const telemetry: CircuitTelemetry = {
      timestamp: Date.now(),
      core: baseCore,
      bus: {
        baseResistance: 10,
        parasiticPast: 5,
        parasiticFuture: 10,
        innerCriticNoise: 0.2
      },
      load: {
        id: 'startup-01',
        name: 'Публикация на ProductHunt / Лайки',
        scale: LoadScale.MACRO_ENTERPRISE,
        powerRequirement: 100,
        fragility: 0.8,
        isDamagedOrFailed: false,
        expectationOfValidation: true // Reverse trap!
      },
      breaker: baseBreaker,
      durationMinutes: 30
    };

    const result = engine.diagnose(telemetry);

    assert.equal(result.status, CircuitStatus.REVERSE_POLARITY);
    assert.equal(result.severity, 'CRITICAL');
    assert.equal(result.code, 'ERR_02_REVERSE_POLARITY');
    assert.ok(result.currentAmperes < 0, 'Current must flow backwards');
    assert.equal(result.remediationProtocols[0].protocolName, 'NIJIRIGUCHI_SEVER_REVERSE');
  });

  it('4. Handles Load Crash with Zanshin Circuit Breaker (Graceful Degradation)', () => {
    const telemetry: CircuitTelemetry = {
      timestamp: Date.now(),
      core: baseCore,
      bus: {
        baseResistance: 5,
        parasiticPast: 0,
        parasiticFuture: 0,
        innerCriticNoise: 0
      },
      load: {
        id: 'ceramic-cup',
        name: 'Раритетная пиала для чая',
        scale: LoadScale.MICRO_TEA,
        powerRequirement: 10,
        fragility: 0.95,
        isDamagedOrFailed: true, // Cup shattered!
        expectationOfValidation: false
      },
      breaker: {
        status: BreakerStatus.ARMED,
        zanshinAwareness: 0.9, // High Zanshin
        tripThreshold: 0.5
      },
      durationMinutes: 5
    };

    const result = engine.diagnose(telemetry);

    assert.equal(result.status, CircuitStatus.SHORT_CIRCUIT);
    assert.equal(result.severity, 'WARNING', 'Zanshin should soften the shock to WARNING');
    assert.ok(result.headline.includes('Дзансин'));
    assert.equal(result.remediationProtocols[0].protocolName, 'KINTSUGI_ZANSHIN_RECOVERY');
  });

  it('5. Handles Load Crash WITHOUT Zanshin (Total Mental Shock)', () => {
    const telemetry: CircuitTelemetry = {
      timestamp: Date.now(),
      core: baseCore,
      bus: {
        baseResistance: 5,
        parasiticPast: 0,
        parasiticFuture: 0,
        innerCriticNoise: 0
      },
      load: {
        id: 'deal-01',
        name: 'Сорванная инвестиционная сделка',
        scale: LoadScale.MACRO_ENTERPRISE,
        powerRequirement: 80,
        fragility: 0.9,
        isDamagedOrFailed: true,
        expectationOfValidation: false
      },
      breaker: {
        status: BreakerStatus.ARMED,
        zanshinAwareness: 0.1, // Absent Zanshin
        tripThreshold: 0.6
      },
      durationMinutes: 10
    };

    const result = engine.diagnose(telemetry);

    assert.equal(result.status, CircuitStatus.SHORT_CIRCUIT);
    assert.equal(result.severity, 'CRITICAL', 'Lack of Zanshin causes CRITICAL short circuit shock');
  });

  it('6. Detects Open Circuit (Idle stagnation / apathy without load)', () => {
    const telemetry: CircuitTelemetry = {
      timestamp: Date.now(),
      core: baseCore,
      bus: {
        baseResistance: 10,
        parasiticPast: 5,
        parasiticFuture: 5,
        innerCriticNoise: 0.1
      },
      load: null, // Disconnected!
      breaker: baseBreaker,
      durationMinutes: 60
    };

    const result = engine.diagnose(telemetry);

    assert.equal(result.status, CircuitStatus.OPEN_CIRCUIT);
    assert.equal(result.currentAmperes, 0);
    assert.equal(result.code, 'ERR_04_OPEN_CIRCUIT');
    assert.equal(result.remediationProtocols[0].protocolName, 'MICRO_LOAD_CALIBRATION');
  });

  it('7. Validates Scale Invariance (Tea vs Enterprise follow identical Ohm laws)', () => {
    const teaTelemetry: CircuitTelemetry = {
      timestamp: Date.now(),
      core: baseCore,
      bus: { baseResistance: 2, parasiticPast: 0, parasiticFuture: 0, innerCriticNoise: 0 },
      load: {
        id: 'tea',
        name: 'Чай',
        scale: LoadScale.MICRO_TEA,
        powerRequirement: 10,
        fragility: 0.5,
        isDamagedOrFailed: false,
        expectationOfValidation: false
      },
      breaker: baseBreaker,
      durationMinutes: 5
    };

    const enterpriseTelemetry: CircuitTelemetry = {
      timestamp: Date.now(),
      core: baseCore,
      bus: { baseResistance: 2, parasiticPast: 0, parasiticFuture: 0, innerCriticNoise: 0 },
      load: {
        id: 'enterprise',
        name: 'Холдинг',
        scale: LoadScale.MACRO_ENTERPRISE,
        powerRequirement: 100,
        fragility: 0.5,
        isDamagedOrFailed: false,
        expectationOfValidation: false
      },
      breaker: baseBreaker,
      durationMinutes: 5
    };

    const teaResult = engine.diagnose(teaTelemetry);
    const entResult = engine.diagnose(enterpriseTelemetry);

    // Both remain in healthy forward states
    assert.equal(teaResult.status, CircuitStatus.SUPERCONDUCTING);
    assert.ok(teaResult.currentAmperes > 0);
    assert.ok(entResult.currentAmperes > 0);
    // Larger load resistance draws appropriate current without inverting polarity
    assert.ok(teaResult.currentAmperes > entResult.currentAmperes);
  });

  it('8. Detects Engineer Romance Split: Validation Lock & Ohmic Future Blowout', () => {
    const approachLockTelemetry: CircuitTelemetry = {
      timestamp: Date.now(),
      core: { emf: 75, reserve: 65, grounding: 0.15 },
      bus: {
        baseResistance: 20,
        parasiticPast: 25,
        parasiticFuture: 85,
        innerCriticNoise: 0.9
      },
      load: {
        id: 'approach-lock',
        name: 'Девушка (требование подтверждения ценности)',
        scale: LoadScale.FLOW_CODE,
        powerRequirement: 80,
        fragility: 0.95,
        isDamagedOrFailed: false,
        expectationOfValidation: true // Reverse current trap!
      },
      breaker: { status: BreakerStatus.ARMED, zanshinAwareness: 0.15, tripThreshold: 0.5 },
      durationMinutes: 5
    };

    const result = engine.diagnose(approachLockTelemetry);

    assert.equal(result.status, CircuitStatus.REVERSE_POLARITY);
    assert.equal(result.severity, 'CRITICAL');
    assert.equal(result.code, 'ERR_02_REVERSE_POLARITY');
    assert.ok(result.currentAmperes < 0, 'Must produce negative reverse current');
    assert.ok(result.effectiveResistance > 150, 'Effective resistance must spike due to future simulations and critic noise');
    assert.equal(result.remediationProtocols[0].protocolName, 'NIJIRIGUCHI_SEVER_REVERSE');
  });

  it('9. Validates Calibrated Approach: Zero Resistance Mushin and Zanshin Safety', () => {
    const calibratedApproachTelemetry: CircuitTelemetry = {
      timestamp: Date.now(),
      core: { emf: 85, reserve: 85, grounding: 0.9 },
      bus: {
        baseResistance: 2,
        parasiticPast: 0,
        parasiticFuture: 0,
        innerCriticNoise: 0.05
      },
      load: {
        id: 'calibrated-approach',
        name: 'Искреннее приветствие из избытка',
        scale: LoadScale.MICRO_TEA,
        powerRequirement: 15,
        fragility: 0.3,
        isDamagedOrFailed: false,
        expectationOfValidation: false // Forward polarity!
      },
      breaker: { status: BreakerStatus.ARMED, zanshinAwareness: 0.9, tripThreshold: 0.5 },
      durationMinutes: 1
    };

    const result = engine.diagnose(calibratedApproachTelemetry);

    assert.equal(result.status, CircuitStatus.SUPERCONDUCTING);
    assert.equal(result.severity, 'OPTIMAL');
    assert.equal(result.code, 'OK_00_SUPERCONDUCTING_MUSHIN');
    assert.ok(result.currentAmperes > 0, 'Positive forward current delivering warmth and presence');
    assert.ok(result.effectiveResistance <= 5);
    assert.equal(result.superconductivityIndex, 1.0);
  });

  it('10. Analyzes Six-Bulb load panel, detecting undervoltage, starved domains and reverse leakage', () => {
    const testPanel: SixBulbPanel = {
      bulbs: {
        [CanonicalLoadDomain.CAR]: {
          domain: CanonicalLoadDomain.CAR,
          name: 'Машина',
          icon: '🚗',
          allocatedPower: 30,
          expectationOfValidation: false
        },
        [CanonicalLoadDomain.HOME]: {
          domain: CanonicalLoadDomain.HOME,
          name: 'Дом',
          icon: '🏡',
          allocatedPower: 10,
          expectationOfValidation: false
        },
        [CanonicalLoadDomain.CAREER]: {
          domain: CanonicalLoadDomain.CAREER,
          name: 'Карьера',
          icon: '💼',
          allocatedPower: 55,
          expectationOfValidation: true // reverse expectation
        },
        [CanonicalLoadDomain.RELATIONSHIPS]: {
          domain: CanonicalLoadDomain.RELATIONSHIPS,
          name: 'Отношения',
          icon: '❤️',
          allocatedPower: 5,
          expectationOfValidation: false
        },
        [CanonicalLoadDomain.HEALTH]: {
          domain: CanonicalLoadDomain.HEALTH,
          name: 'Здоровье',
          icon: '🩺',
          allocatedPower: 0, // completely starved
          expectationOfValidation: false
        },
        [CanonicalLoadDomain.ENTERTAINMENT]: {
          domain: CanonicalLoadDomain.ENTERTAINMENT,
          name: 'Развлечения',
          icon: '🎉',
          allocatedPower: 25,
          expectationOfValidation: false
        }
      }
    };

    const core = { emf: 75, reserve: 80, grounding: 0.5 }; // Available = 60 W
    const analysis = engine.analyzeSixBulbs(core, testPanel);

    assert.equal(analysis.totalDemandedPower, 125);
    assert.equal(analysis.availablePower, 60);
    assert.equal(analysis.isUndervoltage, true, 'Demanding 125W with only 60W available causes undervoltage');
    assert.equal(analysis.dominantDomain, CanonicalLoadDomain.CAREER);
    assert.ok(analysis.starvedDomains.includes(CanonicalLoadDomain.HEALTH));
    assert.equal(analysis.activeBulbsCount, 3); // CAR (30), CAREER (55), ENTERTAINMENT (25)
    assert.ok(analysis.diagnostics.some(d => d.includes('Просадка напряжения')));
    assert.ok(analysis.diagnostics.some(d => d.includes('Здоровье')));
    assert.ok(analysis.diagnostics.some(d => d.includes('Паразитная утечка')));
  });
});
