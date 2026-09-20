import test from 'node:test';
import assert from 'node:assert/strict';
import {loadConfig} from '../web/bot-client.mjs';
test('HTTP error JSON never becomes missing-key configuration', async () => {
  await assert.rejects(loadConfig(async () => ({ok: false, json: async () => ({message: 'Not Found'})})), /connection failed/);
});
test('Malformed success response is a connection failure, not unavailable models', async () => {
  for (const data of [null, {}, {jev_available: 'true', writer_available: true}, {jev_available: true, writer_available: true, hosted: true}]) {
    await assert.rejects(loadConfig(async () => ({ok: true, json: async () => data})), /Invalid service/);
  }
});
test('Configured hosted and local modes preserve actual availability', async () => {
  for (const data of [{jev_available: true, writer_available: true, hosted: true, access_required: true}, {jev_available: true, writer_available: false}]) {
    assert.deepEqual(await loadConfig(async () => ({ok: true, json: async () => data})), data);
  }
});

import {summarizeAnswer} from '../web/bot-client.mjs';
test('Incomplete analysis never becomes a fit recommendation', () => {
  const cards = summarizeAnswer({coverage:{full_library_evaluated:false}, judgments:{fit:{choice:'conditional'}}});
  assert.equal(cards[0][1], 'Assessment incomplete');
});
test('Decision summary preserves uncertainty and suggests a practical next step', () => {
  const cards = summarizeAnswer({coverage:{full_library_evaluated:true}, judgments:{fit:{choice:'conditional'},primitive:{choice:'choice'},generation_needed:{noul:.9},perception_needed:{noul:.5},exact_code_needed:{noul:.1}}});
  assert.equal(cards[0][1], 'Potential fit');
  assert.match(cards[1][1], /Writing/);
  assert.match(cards[1][2], /Unclear: Image/);
  assert.equal(cards[2][1], 'Prototype one decision');
});
