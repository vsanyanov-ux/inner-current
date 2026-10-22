import { describe, it } from 'node:test';
import assert from 'node:assert';
import {
  ZEN_HAIKU_REGISTRY,
  getRandomZenHaiku,
  getZenHaikuById,
  filterZenHaikusByAuthor,
  getAllZenHaikus
} from '../src/domain/zen.haiku.registry.ts';

describe('Zen Haiku & Feline Circuit Registry Test Suite', () => {
  it('1. Registry contains at least 10 canonical haikus with full metadata', () => {
    assert.ok(ZEN_HAIKU_REGISTRY.length >= 10, 'Expected at least 10 haikus');
    for (const haiku of ZEN_HAIKU_REGISTRY) {
      assert.ok(haiku.id, 'Haiku must have an id');
      assert.ok(haiku.author, 'Haiku must have an author');
      assert.ok(haiku.haikuOriginal, 'Haiku must have original text');
      assert.ok(haiku.haikuRu, 'Haiku must have Russian translation');
      assert.ok(haiku.felineCircuitComment, 'Haiku must have feline circuit commentary');
      assert.ok(haiku.electrodynamicFormula, 'Haiku must have electrodynamic formula');
      assert.ok(haiku.somaticCalibration, 'Haiku must have somatic calibration');
    }
  });

  it('2. getRandomZenHaiku returns a valid entry', () => {
    const random = getRandomZenHaiku();
    assert.ok(random);
    assert.ok(random.id);
    assert.ok(random.haikuRu);
  });

  it('3. getZenHaikuById correctly finds entry or returns undefined', () => {
    const found = getZenHaikuById('basho-cold-rain');
    assert.ok(found);
    assert.strictEqual(found.author.includes('Басё'), true);

    const notFound = getZenHaikuById('non-existent-id');
    assert.strictEqual(notFound, undefined);
  });

  it('4. filterZenHaikusByAuthor filters correctly', () => {
    const bashoHaikus = filterZenHaikusByAuthor('Басё');
    assert.ok(bashoHaikus.length >= 3);
    for (const h of bashoHaikus) {
      assert.strictEqual(h.author.includes('Басё'), true);
    }
  });

  it('5. getAllZenHaikus returns a defensive copy', () => {
    const all = getAllZenHaikus();
    assert.strictEqual(all.length, ZEN_HAIKU_REGISTRY.length);
    all.pop();
    assert.strictEqual(ZEN_HAIKU_REGISTRY.length, all.length + 1);
  });
});
