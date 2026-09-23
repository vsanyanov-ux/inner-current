/**
 * Inner Current (Внутренний ток)
 * Diagnostic Engine & Circuit Fault Classifier
 * 
 * Фасад-оркестратор электродинамической диагностики сознания.
 * Реализует принципы Тандэн (автономия ядра) и Мусин (чистота потока).
 */

import { CircuitStatus } from '../types/circuit.types.ts';
import type {
  CircuitTelemetry,
  DiagnosticResult,
  HumanPainDefinition,
  HumanPainArchetype,
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
import {
  calculateEffectiveResistance,
  calculateLoadResistance,
  calculateCurrent,
  calculateJouleLenzHeat,
  calculateSuperconductivityIndex,
  calculateEgoShortCircuit
} from './physics.calculator.ts';
import { validateAndNormalizeTelemetry } from './telemetry.validator.ts';
import { analyzeSixBulbPanel } from './panel.analyzer.ts';
import { PAIN_REGISTRY } from '../domain/pain.registry.ts';

// Реэкспорт для обратной совместимости существующих модулей
export { PAIN_REGISTRY };

export class DiagnosticEngine {
  /**
   * Анализирует телеметрию цепи и классифицирует состояние системы
   * по законам электродинамики и онтологии Дзен.
   */
  public diagnose(telemetry: CircuitTelemetry): DiagnosticResult {
    // 1. Нормализация телеметрии (канон Мусин: защита от искажений и шума)
    const normalized = validateAndNormalizeTelemetry(telemetry);
    const { core, bus, load, breaker, durationMinutes } = normalized;

    // 2. Расчёт эффективного сопротивления проводки внимания (R_eff)
    const finalResistance = calculateEffectiveResistance(bus, core.grounding);

    // 3. Проверка на обрыв цепи (OPEN_CIRCUIT: нет нагрузки, застой энергии)
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
        physicsAnalysis:
          'Энергия Тандэна застаивается в ядре без полезной нагрузки. Контур разомкнут, ток не течёт (I = 0). Субъективно переживается как апатия, лень и отсутствие вектора жизни.',
        remediationProtocols: MICRO_LOAD_TEA_PROTOCOL
      };
    }

    // 4. Проверка на короткое замыкание на Эго (EGO_SHORT_CIRCUIT)
    if (load.expectationOfValidation) {
      const { egoHeat } = calculateEgoShortCircuit(
        core.emf,
        core.grounding,
        finalResistance,
        durationMinutes
      );

      return {
        status: CircuitStatus.EGO_SHORT_CIRCUIT,
        severity: 'CRITICAL',
        currentAmperes: 0, // Полезный ток в нагрузку не поступает — замкнут на Эго
        effectiveResistance: finalResistance,
        thermalDissipationJoules: egoHeat,
        superconductivityIndex: 0,
        code: 'ERR_02_EGO_SHORT_CIRCUIT',
        headline: 'Короткое замыкание на Эго: иллюзия внешнего источника',
        physicsAnalysis:
          'Внешняя нагрузка пуста (Шуньята, E_load = 0) и не содержит заряда. Ожидание подпитки замыкает внимание во внутренний паразитный контур Эго (Дзига) до нагрузки. Полезный ток в ремесло блокирован (I_load = 0), а сверхток внутреннего КЗ раскаляет проводку внимания до кипения по закону Джоуля — Ленца.',
        remediationProtocols: NIJIRIGUCHI_POLARITY_PROTOCOL
      };
    }

    // 5. Проверка на аварию нагрузки (SHORT_CIRCUIT / Load Failure)
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

    // 6. Расчёт тока (I), теплового рассеяния (Q) и коэффициента сверхпроводимости
    const loadResistance = calculateLoadResistance(load.powerRequirement);
    const totalLoopResistance = finalResistance + loadResistance;
    const currentAmperes = calculateCurrent(core.emf, totalLoopResistance);
    const thermalDissipationJoules = calculateJouleLenzHeat(currentAmperes, finalResistance, durationMinutes);
    const superconductivityIndex = calculateSuperconductivityIndex(finalResistance);

    // 7. Сверхпроводимость потока Мусин (R -> 0)
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

    // 8. Омический перегрев (выгорание от мыслей о прошлом и будущем)
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

    // 9. Номинальный рабочий режим цепи
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
    return analyzeSixBulbPanel(core, panel);
  }

  /**
   * Pain-First Диагностика: локализация первопричины боли человека в цепи
   */
  public diagnosePain(painId: HumanPainArchetype): HumanPainDefinition {
    const definition = PAIN_REGISTRY[painId];
    if (!definition) {
      throw new Error(`Неизвестный архетип человеческой боли: ${painId}`);
    }
    return definition;
  }

  /**
   * Возвращает весь реестр человеческих болей для навигатора и каталога
   */
  public getAllPains(): HumanPainDefinition[] {
    return Object.values(PAIN_REGISTRY);
  }
}
