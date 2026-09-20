import test from 'node:test';
import assert from 'node:assert/strict';
import {referenceUrls} from '../web/evidence.mjs';
import {exampleDesign} from '../web/answer-design.mjs';
test('Multiple source links remain URL strings usable by the renderer', () => {
  const urls = referenceUrls({text: 'https://example.com/article https://github.com/example/project https://example.com/image.png'});
  assert.deepEqual(urls, ['https://github.com/example/project', 'https://example.com/article']);
  for (const url of urls) assert.ok(new URL(url).hostname);
});
test('Failed custom answers never fall back to unrelated patterns', () => {
  const r = {mode:'written', idea:'Monitor sensitive information in AI applications', coverage:{full_library_evaluated:true}, judgments:{example_pattern:{choice:'inbox_routing'}}, writer:{status:'invalid_output'}};
  assert.equal(exampleDesign(r), null);
  assert.equal(exampleDesign({...r,writer:undefined}), null);
  const valid={...r,writer:{status:'success',blueprint:{title:'Screen model-bound text'}}};
  assert.equal(exampleDesign(valid).title, 'Screen model-bound text');
  assert.equal(exampleDesign({...valid,coverage:{full_library_evaluated:false}}), null);
});
