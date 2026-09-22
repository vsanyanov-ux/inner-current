import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

describe('Visualizer public/index.html Integrity & Script Syntax Test Suite', () => {
  const htmlPath = path.resolve('public/index.html');
  const html = fs.readFileSync(htmlPath, 'utf8');

  it('1. All embedded JavaScript blocks in index.html have zero syntax errors', () => {
    const scriptMatches = [...html.matchAll(/<script[\s\S]*?>([\s\S]*?)<\/script>/gi)];
    assert.ok(scriptMatches.length > 0, 'Should find at least one <script> tag');

    scriptMatches.forEach((m, idx) => {
      const code = m[1].trim();
      if (!code) return; // External script tag like Tailwind
      try {
        new Function(code);
      } catch (err: any) {
        assert.fail(`Script #${idx} failed to parse: ${err.message}`);
      }
    });
  });

  it('2. All onclick handler functions in index.html are defined and callable', () => {
    const onclickMatches = [...html.matchAll(/onclick="([^"]+)"/g)];
    assert.ok(onclickMatches.length > 0, 'Should find onclick attributes');

    const fnCalls = new Set<string>();
    const ignoredKeywords = new Set(['typeof', 'if', 'playZenChime', 'setTimeout']);

    onclickMatches.forEach(m => {
      const code = m[1];
      const matches = [...code.matchAll(/([a-zA-Z0-9_$]+)\s*\(/g)];
      matches.forEach(call => {
        const fn = call[1];
        if (!ignoredKeywords.has(fn)) {
          fnCalls.add(fn);
        }
      });
    });

    const scriptMatches = [...html.matchAll(/<script[\s\S]*?>([\s\S]*?)<\/script>/gi)];
    const fullJs = scriptMatches.map(m => m[1]).join('\n');

    const missingFns: string[] = [];
    for (const fn of fnCalls) {
      const regex = new RegExp(`(?:function\\s+${fn}\\b|${fn}\\s*=|window\\.${fn}\\b)`);
      if (!regex.test(fullJs)) {
        missingFns.push(fn);
      }
    }

    assert.deepEqual(missingFns, [], `Found missing onclick functions: ${missingFns.join(', ')}`);
  });

  it('3. Happiness Dashboard DOM elements exist and are accessible', () => {
    const requiredIds = [
      'view-happiness-dashboard',
      'dash-score-value',
      'dash-state-label',
      'dash-r-value',
      'dash-i-value',
      'dash-q-value',
      'dash-breaker-value',
      'dash-btn-calibrate',
      'hbtn-focus-now',
      'hbtn-motive-creation',
      'hbtn-body-ok'
    ];

    for (const id of requiredIds) {
      assert.ok(html.includes(`id="${id}"`), `Element with id "${id}" should exist in public/index.html`);
    }
  });
});
