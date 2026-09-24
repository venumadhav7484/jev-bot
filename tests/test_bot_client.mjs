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

import {readReply, sendJson, startJob, waitForJob, progressMessage, ServiceError} from '../web/bot-client.mjs';
const html = status => ({ok: false, status, json: async () => { throw new SyntaxError('Unexpected token <'); }});
const json = (status, data) => ({ok: status < 400, status, json: async () => data});
const offline = async () => { throw new TypeError('Failed to fetch'); };
test('Proxy HTML and network failures become visitor-safe messages', async () => {
  assert.equal(await readReply(html(502)), null);
  for (const fetcher of [async () => html(502), offline]) {
    await assert.rejects(startJob('idea', 'written', fetcher), e => e instanceof ServiceError && !/token|fetch/i.test(e.message));
    await assert.rejects(sendJson('/api/feedback', {}, 'Couldn’t save feedback.', fetcher), e => e instanceof ServiceError && !/token|fetch/i.test(e.message));
  }
  await assert.rejects(startJob('idea', 'written', async () => json(429, {error: 'All answer slots are busy.'})), /slots are busy/);
});
test('Transient poll failures are retried without abandoning the job', async () => {
  const replies = [offline, async () => html(504), async () => json(200, {status: 'running', progress: {stage: 'x'}}), async () => html(502), async () => json(200, {status: 'complete', result: {mode: 'written'}})];
  const seen = [];
  const result = await waitForJob('a'.repeat(32), p => seen.push(p), {fetcher: () => replies.shift()(), sleep: async () => {}});
  assert.deepEqual(result, {mode: 'written'});
  assert.equal(seen.length, 1);
});
test('Polling stops after repeated failures or a definitive server answer', async () => {
  await assert.rejects(waitForJob('id', () => {}, {fetcher: offline, sleep: async () => {}, maxMisses: 3}), /Connection interrupted/);
  await assert.rejects(waitForJob('id', () => {}, {fetcher: async () => json(404, {error: 'Answer job not found or expired.'}), sleep: async () => {}}), /expired/);
  await assert.rejects(waitForJob('id', () => {}, {fetcher: async () => json(200, {status: 'failed', error: 'Couldn’t complete this answer. Please retry.'}), sleep: async () => {}}), /Please retry/);
  await assert.rejects(waitForJob('id', () => {}, {fetcher: async () => json(200, {status: 'complete'}), sleep: async () => {}}), ServiceError);
});
test('Progress never shows NaN or exceeds the known stages', () => {
  const stage = 'Jev is evaluating every research passage';
  for (const p of [{stage, total: 0, completed: 0}, {stage}, {stage, total: 'x', completed: 1}]) assert.equal(progressMessage(p), 'Jev is reviewing the library for your idea…');
  assert.match(progressMessage({stage, total: 200, completed: 50}), /25%$/);
  assert.match(progressMessage({stage, total: 10, completed: 10}), /Library review complete/);
  assert.match(progressMessage({}), /Preparing/);
});
