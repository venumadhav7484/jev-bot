// The browser solver must agree with the tested Python solver (experiments/psychrometric-charts/src/psychro.py).
import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {solve, state, pressureAt, toSI} from '../web/psychro-solver.mjs';

const vectors = JSON.parse(readFileSync(new URL('./fixtures/psychro_vectors.json', import.meta.url)));

test('matches the Python solver on every usable pair and pressure', () => {
  for (const v of vectors) {
    const got = solve([v.a[0], v.a[1]], [v.b[0], v.b[1]], v.p);
    for (const [k, want] of Object.entries(v.truth)) assert.ok(Math.abs(got[k] - want) < 1e-6 * Math.max(1, Math.abs(want)) + 1e-7, `${v.a[0]}+${v.b[0]} ${k}`);
  }
  assert.equal(vectors.length, 300);  // 3 pressures × 5 states × 20 usable pairs
});

test('textbook state and altitude pressure', () => {
  const s = state(25, 0.009884, 101325);
  assert.ok(Math.abs(s.tdp - 13.86) < 0.05 && Math.abs(s.twb - 17.89) < 0.05);
  assert.ok(Math.abs(pressureAt(1500) - 84556) < 5);
});

test('refuses impossible or dependent inputs and mismatched units', () => {
  assert.throws(() => solve(['tdb', 20], ['rh', 1.2]));
  assert.throws(() => solve(['tdp', 10], ['w', 0.0076]));
  assert.throws(() => solve(['tdb', 20], ['tdb', 25]));
  assert.equal(toSI('tdp', 60, '%'), null);
  assert.equal(toSI('tdb', 86, '°F'), 30);
});
