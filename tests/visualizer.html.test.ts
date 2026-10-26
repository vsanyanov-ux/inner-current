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

  const trainerHtmlPath = path.resolve('public/trainer.html');
  const trainerHtml = fs.existsSync(trainerHtmlPath) ? fs.readFileSync(trainerHtmlPath, 'utf8') : html;

  it('3. Trainer 2.0 Speedometer & 5 Biological Systems DOM elements exist and are accessible', () => {
    const requiredIds = [
      'view-speedometer',
      'gauge-ci-val',
      'gauge-state-label',
      'gauge-h-val',
      'live-rego-val',
      'live-heat-val',
      'live-eff-val',
      'slider-gauge-ans',
      'slider-gauge-endo',
      'slider-gauge-brain',
      'slider-gauge-cardio',
      'slider-gauge-soma'
    ];

    for (const id of requiredIds) {
      assert.ok(trainerHtml.includes(`id="${id}"`), `Element with id "${id}" should exist in trainer.html`);
    }
  });

  it('4. Pain-First Emergency Navigator DOM elements exist and are accessible', () => {
    const painIds = [
      'view-pains',
      'card-pain-01',
      'card-pain-02',
      'card-pain-03',
      'card-pain-04',
      'card-pain-05',
      'liveHealingBanner'
    ];

    for (const id of painIds) {
      assert.ok(trainerHtml.includes(`id="${id}"`), `Pain-First element with id "${id}" should exist in trainer.html`);
    }
  });

  it('5. Laboratory & Living Circuit SVG elements exist and are accessible', () => {
    const labIds = [
      'view-lab',
      'liveCircuitSvg',
      'svg-resistor-box',
      'svg-resistor-val',
      'svg-light-beam',
      'svg-lamp-glow'
    ];

    for (const id of labIds) {
      assert.ok(trainerHtml.includes(`id="${id}"`), `Circuit / Lab element with id "${id}" should exist in trainer.html`);
    }
  });

  it('6. Trainer 2.0 embedded scripts and onclick handlers are valid', () => {
    const scriptMatches = [...trainerHtml.matchAll(/<script[\s\S]*?>([\s\S]*?)<\/script>/gi)];
    assert.ok(scriptMatches.length > 0, 'Should find at least one <script> tag in trainer.html');

    scriptMatches.forEach((m, idx) => {
      const scriptCode = m[1].trim();
      if (!scriptCode) return;
      try {
        new Function(scriptCode);
      } catch (err: any) {
        assert.fail(`Trainer script #${idx} failed to parse: ${err.message}`);
      }
    });

    const onclickMatches = [...trainerHtml.matchAll(/onclick="([^"]+)"/g)];
    const fnCalls = new Set<string>();
    const ignored = new Set(['typeof', 'if', 'setTimeout']);

    onclickMatches.forEach(m => {
      const clickCode = m[1];
      const matches = [...clickCode.matchAll(/([a-zA-Z0-9_$]+)\s*\(/g)];
      matches.forEach(call => {
        const fn = call[1];
        if (!ignored.has(fn)) {
          fnCalls.add(fn);
        }
      });
    });

    const fullJs = scriptMatches.map(m => m[1]).join('\n');
    const missingFns: string[] = [];
    for (const fn of fnCalls) {
      const regex = new RegExp(`(?:function\\s+${fn}\\b|${fn}\\s*=|window\\.${fn}\\b)`);
      if (!regex.test(fullJs)) {
        missingFns.push(fn);
      }
    }

    assert.deepEqual(missingFns, [], `Found missing onclick functions in trainer.html: ${missingFns.join(', ')}`);
  });

  it('7. Manifesto public/manifesto.html Integrity: exists and renders correctly', () => {
    const manifestoPath = path.resolve('public/manifesto.html');
    assert.ok(fs.existsSync(manifestoPath), 'public/manifesto.html should exist');
    const manifestoHtml = fs.readFileSync(manifestoPath, 'utf8');
    assert.ok(manifestoHtml.includes('Манифест Внутреннего Тока'), 'Manifesto title should exist');
    assert.ok(manifestoHtml.includes('500+'), 'Manifesto should mention 500+ articles');
    assert.ok(manifestoHtml.includes('ТАНДЭН'), 'Manifesto should feature Tanden in schematic');
    assert.ok(manifestoHtml.includes('ЛАМПОЧКА'), 'Manifesto should feature Bulb in schematic');
  });

  it('7. Cockpit public/cockpit.html Integrity: scripts parse cleanly and Triad HUD exists', () => {
    const cockpitPath = path.resolve('public/cockpit.html');
    const cockpitHtml = fs.readFileSync(cockpitPath, 'utf8');

    // Embedded scripts parse check
    const scriptMatches = [...cockpitHtml.matchAll(/<script[\s\S]*?>([\s\S]*?)<\/script>/gi)];
    assert.ok(scriptMatches.length > 0, 'Should find at least one <script> tag in cockpit.html');

    scriptMatches.forEach((m, idx) => {
      const code = m[1].trim();
      if (!code) return;
      try {
        new Function(code);
      } catch (err: any) {
        assert.fail(`Cockpit script #${idx} failed to parse: ${err.message}`);
      }
    });

    // Check Triad of Ego Resistance UI elements
    const cockpitTriadIds = [
      'cockpit-triad-badge',
      'cockpit-btn-guilt',
      'cockpit-btn-control',
      'cockpit-btn-approval',
      'cockpit-btn-triad-reset'
    ];

    for (const id of cockpitTriadIds) {
      assert.ok(cockpitHtml.includes(`id="${id}"`), `Cockpit Triad element with id "${id}" should exist`);
    }

    // Verify all onclick handlers in cockpit.html are defined
    const onclickMatches = [...cockpitHtml.matchAll(/onclick="([^"]+)"/g)];
    const fnCalls = new Set<string>();
    const ignored = new Set(['typeof', 'if', 'setTimeout']);

    onclickMatches.forEach(m => {
      const code = m[1];
      const matches = [...code.matchAll(/([a-zA-Z0-9_$]+)\s*\(/g)];
      matches.forEach(call => {
        const fn = call[1];
        if (!ignored.has(fn)) {
          fnCalls.add(fn);
        }
      });
    });

    const fullJs = scriptMatches.map(m => m[1]).join('\n');
    const missingFns: string[] = [];
    for (const fn of fnCalls) {
      const regex = new RegExp(`(?:function\\s+${fn}\\b|${fn}\\s*=|window\\.${fn}\\b)`);
      if (!regex.test(fullJs)) {
        missingFns.push(fn);
      }
    }

    assert.deepEqual(missingFns, [], `Found missing onclick functions in cockpit.html: ${missingFns.join(', ')}`);
  });
it('8. Circuit Console (I vs R HUD) DOM elements exist and are accessible in index.html', () => {
    const consoleIds = [
      'circuit-console',
      'circuit-console-nav',
      'cc-slider-i',
      'cc-slider-r',
      'cc-i-display',
      'cc-r-display',
      'cc-i-needle',
      'cc-r-needle',
      'cc-i-arc',
      'cc-r-arc',
      'cc-mode-pill',
      'cc-radar-blip',
      'cc-coords-badge',
      'cc-metric-p',
      'cc-metric-q',
      'cc-metric-eta',
      'cc-verdict-box'
    ];

    for (const id of consoleIds) {
      assert.ok(html.includes(`id="${id}"`), `Circuit Console element with id "${id}" should exist in index.html`);
    }
  });
});
