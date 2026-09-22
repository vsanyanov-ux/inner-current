/**
 * Inner Current (Внутренний ток)
 * Interactive Terminal Telemetry Demo & Simulator
 */

import { DiagnosticEngine } from '../core/diagnostic.engine.ts';
import {
  BreakerStatus,
  LoadScale,
  CanonicalLoadDomain
} from '../types/circuit.types.ts';
import type { CircuitTelemetry, SixBulbPanel } from '../types/circuit.types.ts';

const engine = new DiagnosticEngine();

console.log('='.repeat(70));
console.log('⚡ INNER CURRENT (Внутренний ток) — ДЕМОНСТРАЦИЯ ДИАГНОСТИКИ');
console.log('='.repeat(70));

const scenarios: { name: string; telemetry: CircuitTelemetry }[] = [
  {
    name: '🍵 Сценарий 1: Мастер за чаем (Мусин, R ≈ 0)',
    telemetry: {
      timestamp: Date.now(),
      core: { emf: 85, reserve: 95, grounding: 0.9 },
      bus: { baseResistance: 1, parasiticPast: 0, parasiticFuture: 0, innerCriticNoise: 0 },
      load: {
        id: 'tea',
        name: 'Чаша зелёного чая матча',
        scale: LoadScale.MICRO_TEA,
        powerRequirement: 10,
        fragility: 0.7,
        isDamagedOrFailed: false,
        expectationOfValidation: false
      },
      breaker: { status: BreakerStatus.ARMED, zanshinAwareness: 0.95, tripThreshold: 0.5 },
      durationMinutes: 15
    }
  },
  {
    name: '🔥 Сценарий 2: Выгорание разработчика перед дедлайном (Омический перегрев)',
    telemetry: {
      timestamp: Date.now(),
      core: { emf: 75, reserve: 40, grounding: 0.2 },
      bus: { baseResistance: 20, parasiticPast: 25, parasiticFuture: 45, innerCriticNoise: 0.8 },
      load: {
        id: 'code-release',
        name: 'Релиз сложного микросервиса',
        scale: LoadScale.FLOW_CODE,
        powerRequirement: 40,
        fragility: 0.5,
        isDamagedOrFailed: false,
        expectationOfValidation: false
      },
      breaker: { status: BreakerStatus.ARMED, zanshinAwareness: 0.3, tripThreshold: 0.6 },
      durationMinutes: 60
    }
  },
  {
    name: '🪤 Сценарий 3: Ловушка признания (Обратный ток / Синдром самозванца)',
    telemetry: {
      timestamp: Date.now(),
      core: { emf: 60, reserve: 50, grounding: 0.3 },
      bus: { baseResistance: 15, parasiticPast: 10, parasiticFuture: 20, innerCriticNoise: 0.5 },
      load: {
        id: 'pitch',
        name: 'Выступление перед инвесторами (жажда одобрения)',
        scale: LoadScale.MACRO_ENTERPRISE,
        powerRequirement: 90,
        fragility: 0.8,
        isDamagedOrFailed: false,
        expectationOfValidation: true // Опасное ожидание подпитки извне!
      },
      breaker: { status: BreakerStatus.ARMED, zanshinAwareness: 0.4, tripThreshold: 0.5 },
      durationMinutes: 30
    }
  },
  {
    name: '🏺 Сценарий 4: Отказ внешнего проекта при высоком Дзансин (Кинцуги / Ваби-саби)',
    telemetry: {
      timestamp: Date.now(),
      core: { emf: 80, reserve: 80, grounding: 0.85 },
      bus: { baseResistance: 5, parasiticPast: 0, parasiticFuture: 0, innerCriticNoise: 0 },
      load: {
        id: 'failed-contract',
        name: 'Сорвавшийся крупный контракт',
        scale: LoadScale.MACRO_ENTERPRISE,
        powerRequirement: 100,
        fragility: 0.9,
        isDamagedOrFailed: true, // Внешний отказ!
        expectationOfValidation: false
      },
      breaker: { status: BreakerStatus.ARMED, zanshinAwareness: 0.88, tripThreshold: 0.5 },
      durationMinutes: 5
    }
  },
  {
    name: '💔 Сценарий 5: Ступор перед девушкой (Двойной разлад: Обратный ток + Омический взрыв симуляций)',
    telemetry: {
      timestamp: Date.now(),
      core: { emf: 75, reserve: 65, grounding: 0.15 }, // Потенциал есть, но оторван от тела, всё ушло в голову
      bus: {
        baseResistance: 20,
        parasiticPast: 25,     // Страх повторить былые неловкости
        parasiticFuture: 85,   // Взрывной рой симуляций "а что если пошлёт", "что подумают люди"
        innerCriticNoise: 0.9  // Внутренний критик парализует волю
      },
      load: {
        id: 'approach-anxiety',
        name: 'Девушка (попытка получить валидацию привлекательности)',
        scale: LoadScale.FLOW_CODE,
        powerRequirement: 80,
        fragility: 0.95,
        isDamagedOrFailed: false,
        expectationOfValidation: true // ⚡ Попытка зарядиться от внешнего одобрения: обратный ток!
      },
      breaker: { status: BreakerStatus.ARMED, zanshinAwareness: 0.15, tripThreshold: 0.5 },
      durationMinutes: 5
    }
  },
  {
    name: '✨ Сценарий 6: Сверхпроводящее знакомство (Смена полярности на отдачу + Дзансин + R → 0)',
    telemetry: {
      timestamp: Date.now(),
      core: { emf: 85, reserve: 85, grounding: 0.9 }, // Полное заземление в тело, опора на стопы, дыхание в Тандэн
      bus: {
        baseResistance: 2,
        parasiticPast: 0,
        parasiticFuture: 0,    // Будущее отключено: есть только этот физический шаг здесь и сейчас
        innerCriticNoise: 0.05
      },
      load: {
        id: 'authentic-approach',
        name: 'Искреннее приветствие / бескорыстный комплимент (поток из избытка)',
        scale: LoadScale.MICRO_TEA, // Масштабировано до простоты глотка чая (микро-нагрузка)
        powerRequirement: 15,
        fragility: 0.3,
        isDamagedOrFailed: false,
        expectationOfValidation: false // ⚡ Прямой ток: дарить свет и тепло без нужды в одобрении
      },
      breaker: { status: BreakerStatus.ARMED, zanshinAwareness: 0.9, tripThreshold: 0.5 }, // Предохранитель Дзансин
      durationMinutes: 1
    }
  }
];

for (const sc of scenarios) {
  console.log(`\n▶ ${sc.name}`);
  const res = engine.diagnose(sc.telemetry);
  console.log(`  Статус: [${res.status}] | Серьезность: ${res.severity} | Код: ${res.code}`);
  console.log(`  Сила тока (I): ${res.currentAmperes} A | R_eff: ${res.effectiveResistance} Ом | Q: ${res.thermalDissipationJoules} Дж | КПД: ${(res.superconductivityIndex * 100).toFixed(0)}%`);
  console.log(`  Вердикт: ${res.headline}`);
  console.log(`  Физика: ${res.physicsAnalysis}`);
  if (res.remediationProtocols.length > 0) {
    console.log(`  Регламент починки:`);
    for (const step of res.remediationProtocols) {
      console.log(`    ${step.order}. ${step.title} (${step.description})`);
    }
  }
}

// --------------------------------------------------------------------------
// ДЕМОНСТРАЦИЯ 6-КАНАЛЬНОГО РАСПРЕДЕЛИТЕЛЬНОГО ЩИТА НАГРУЗОК
// --------------------------------------------------------------------------
console.log('\n' + '='.repeat(70));
console.log('💡 6-КАНАЛЬНЫЙ РАСПРЕДЕЛИТЕЛЬНЫЙ ЩИТ (БАЛАНСИРОВКА НАГРУЗКИ)');
console.log('='.repeat(70));

const samplePanel: SixBulbPanel = {
  bulbs: {
    [CanonicalLoadDomain.CAR]: {
      domain: CanonicalLoadDomain.CAR,
      name: 'Машина',
      icon: '🚗',
      allocatedPower: 30, // 30 Вт
      expectationOfValidation: false
    },
    [CanonicalLoadDomain.HOME]: {
      domain: CanonicalLoadDomain.HOME,
      name: 'Дом',
      icon: '🏡',
      allocatedPower: 10, // 10 Вт
      expectationOfValidation: false
    },
    [CanonicalLoadDomain.CAREER]: {
      domain: CanonicalLoadDomain.CAREER,
      name: 'Карьера',
      icon: '💼',
      allocatedPower: 55, // 55 Вт (основной потребитель)
      expectationOfValidation: true // ⚠️ Паразитная утечка: ждет признания
    },
    [CanonicalLoadDomain.RELATIONSHIPS]: {
      domain: CanonicalLoadDomain.RELATIONSHIPS,
      name: 'Отношения',
      icon: '❤️',
      allocatedPower: 5,  // 5 Вт (тлеет)
      expectationOfValidation: false
    },
    [CanonicalLoadDomain.HEALTH]: {
      domain: CanonicalLoadDomain.HEALTH,
      name: 'Здоровье',
      icon: '🩺',
      allocatedPower: 0,  // 0 Вт (полностью обесточено!)
      expectationOfValidation: false
    },
    [CanonicalLoadDomain.ENTERTAINMENT]: {
      domain: CanonicalLoadDomain.ENTERTAINMENT,
      name: 'Развлечения',
      icon: '🎉',
      allocatedPower: 25, // 25 Вт
      expectationOfValidation: false
    }
  }
};

const userCore = { emf: 75, reserve: 80, grounding: 0.5 }; // Доступная мощность ≈ 60 Вт
const sixBulbAnalysis = engine.analyzeSixBulbs(userCore, samplePanel);

console.log(`\n📊 Диагностика профиля нагрузок:`);
console.log(`  Генератор: ЭДС ${userCore.emf} В | Запас ${userCore.reserve}% | Доступно: ${sixBulbAnalysis.availablePower} Вт`);
console.log(`  Суммарная нагрузка сети: ${sixBulbAnalysis.totalDemandedPower} Вт (6 каналов)`);
console.log(`  Горящих ламп: ${sixBulbAnalysis.activeBulbsCount} из 6 | Доминирующий канал: [${sixBulbAnalysis.dominantDomain}]`);
console.log(`  Обесточенные каналы: [${sixBulbAnalysis.starvedDomains.join(', ')}]`);

console.log(`\nИнженерные предупреждения сети:`);
for (const diag of sixBulbAnalysis.diagnostics) {
  console.log(`  ${diag}`);
}

// Демонстрация Режима Монаха (все лампы 0 Вт)
const monkPanel: SixBulbPanel = {
  bulbs: {
    [CanonicalLoadDomain.CAR]: { domain: CanonicalLoadDomain.CAR, name: 'Машина', icon: '🚗', allocatedPower: 0, expectationOfValidation: false },
    [CanonicalLoadDomain.HOME]: { domain: CanonicalLoadDomain.HOME, name: 'Дом', icon: '🏡', allocatedPower: 0, expectationOfValidation: false },
    [CanonicalLoadDomain.CAREER]: { domain: CanonicalLoadDomain.CAREER, name: 'Карьера', icon: '💼', allocatedPower: 0, expectationOfValidation: false },
    [CanonicalLoadDomain.RELATIONSHIPS]: { domain: CanonicalLoadDomain.RELATIONSHIPS, name: 'Отношения', icon: '❤️', allocatedPower: 0, expectationOfValidation: false },
    [CanonicalLoadDomain.HEALTH]: { domain: CanonicalLoadDomain.HEALTH, name: 'Здоровье', icon: '🩺', allocatedPower: 0, expectationOfValidation: false },
    [CanonicalLoadDomain.ENTERTAINMENT]: { domain: CanonicalLoadDomain.ENTERTAINMENT, name: 'Развлечения', icon: '🎉', allocatedPower: 0, expectationOfValidation: false }
  }
};

const monkAnalysis = engine.analyzeSixBulbs(userCore, monkPanel);
console.log(`\n🧘 Тест сценария «Режим монаха» (0 Вт на всех лампах):`);
console.log(`  Активных ламп: ${monkAnalysis.activeBulbsCount} из 6 | Нагрузка: ${monkAnalysis.totalDemandedPower} Вт`);
for (const diag of monkAnalysis.diagnostics) {
  console.log(`  ${diag}`);
}

console.log('\n' + '='.repeat(70));
console.log('🚨 PAIN-FIRST НАВИГАТОР: 5 КЛЮЧЕВЫХ БОЛЕЙ И ИХ ИСЦЕЛЕНИЕ');
console.log('='.repeat(70));

const allPains = engine.getAllPains();
allPains.forEach((p, idx) => {
  console.log(`\n[Боль #${idx + 1}]: ${p.humanSymptom}`);
  console.log(`  🗣️ Переживание: ${p.humanCry}`);
  console.log(`  ⚡ Физика сбоя: ${p.electrodynamicCause.headline} (${p.electrodynamicCause.faultCode})`);
  console.log(`  📍 Узел цепи: ${p.electrodynamicCause.affectedNode} [${p.electrodynamicCause.parameterState}]`);
  console.log(`  ⚙️ Закон: ${p.electrodynamicCause.physicsLaw}`);
  console.log(`  💡 Почему болит: ${p.electrodynamicCause.explanation}`);
  console.log(`  🔧 Рецепт: ${p.remediationSolution.protocolName}`);
  console.log(`  🚀 Действие СЕЙЧАС: ${p.remediationSolution.immediateAction}`);
});

console.log('\n' + '='.repeat(70));


