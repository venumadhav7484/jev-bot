import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const rows = JSON.parse(readFileSync(new URL('../docs/bot-cases.json', import.meta.url)));
const designs = JSON.parse(readFileSync(new URL('../docs/case-designs.json', import.meta.url))).cases;
test('Every case has its own current prebuilt design, including held records', () => {
  assert.deepEqual(new Set(Object.keys(designs)), new Set(rows.map(r => r.id)));
  for (const row of rows) {
    const saved = designs[row.id];
    assert.equal(saved.case_id, row.id);
    assert.equal(saved.source_hash, row.design_source_hash, row.id);
    assert.deepEqual(Object.keys(saved).sort(), ['blueprint', 'case_id', 'source_hash', 'version']);
  }
});
test('Examples switch real state and stay within their request options', () => {
  for (const [id, saved] of Object.entries(designs)) {
    const d = saved.blueprint;
    assert.equal(d.examples.length, 2, id);
    assert.deepEqual(d.request.state, d.examples[0].state, id);
    assert.deepEqual(Object.keys(d.request.questions), ['decision'], id);
    assert.equal(d.request.questions.decision.type, 'choice', id);
    assert.ok(d.flow.some(step => step.owner === 'jev'), id);
    for (const ex of d.examples) {
      assert.ok(ex.output.decision in d.request.questions.decision.criteria, id);
      assert.deepEqual(Object.keys(ex.state).sort(), Object.keys(d.examples[0].state).sort(), id);
      assert.ok(typeof ex.output.action === 'string' && ex.output.action.length, id);
    }
  }
});
