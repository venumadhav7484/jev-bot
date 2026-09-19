import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {categories, prepare, sections, links, signal, filterCases, shuffled} from '../web/evidence.mjs';
const raw = JSON.parse(readFileSync(new URL('../docs/bot-cases.json', import.meta.url)));
const rows = raw.map(prepare);
test('Every public case remains discoverable, including held records and caveats', () => {
  assert.equal(rows.length, raw.length);
  assert.equal(new Set(rows.map(r => r.id)).size, rows.length);
  for (const row of rows) {
    assert.ok(categories.includes(row.group), row.id);
    assert.ok(row.what && row.how && row.limits, row.id);
    assert.equal(row.limits, sections(row.body)['Limits and reuse']);
  }
  assert.equal(filterCases(rows, 'All', '').length, raw.length);
  assert.ok(rows.some(r => !r.default_retrieval));
});
test('Filter and randomize preserve selected category, evidence, and input order', () => {
  const selected = filterCases(rows, 'Games & robotics', 'tetris');
  assert.ok(selected.length > 1);
  assert.ok(selected.every(r => r.group === 'Games & robotics' && `${r.title} ${r.what} ${r.how}`.toLowerCase().includes('tetris')));
  const before = [...selected]; const mixed = shuffled(selected, () => 0.3);
  assert.deepEqual(selected, before);
  assert.deepEqual(new Set(mixed), new Set(selected));
  assert.deepEqual(filterCases(rows, 'All', 'nonexistentzzzzzz'), []);
});
test('Evidence signals do not turn reported use or counterexamples into performance scores', () => {
  assert.equal(signal({evidence_role:'implementation_report'}).label, 'Conditional fit');
  assert.equal(signal({evidence_role:'counterexample'}).label, 'Known limitation');
  assert.equal(signal({evidence_role:'unvalidated_finance'}).label, 'Exploratory');
  assert.equal(signal({evidence_role:'thin'}).label, 'Not established');
  assert.equal(signal({id:'tetris-dayton',evidence_role:'implementation_report'}).tone, 'warn');
  assert.equal(rows.find(r => r.id === 'blakestone-jev-mcp').group, 'Code & agents');
});
test('Source links deduplicate, reject credentials, and only expose HTTP(S)', () => {
  const result = links('[Repo](https://github.com/example/repo) https://github.com/example/repo javascript:alert(1) https://user:secret@example.com/');
  assert.deepEqual(result.map(r => r.url), ['https://github.com/example/repo']);
  assert.equal(result[0].kind, 'Repository');
});
