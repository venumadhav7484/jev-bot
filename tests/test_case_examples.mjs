import test from 'node:test';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';
import {newsRequest, newsPython, newsSource} from '../web/case-examples.mjs';
test('News example uses bounded Choice and Noul with pinned provenance', () => {
  assert.equal(newsRequest.questions.relevance.type, 'choice');
  assert.deepEqual(Object.keys(newsRequest.questions.relevance.criteria), ['relevant', 'irrelevant', 'insufficient_evidence']);
  assert.equal(newsRequest.questions.importance.type, 'noul');
  assert.match(newsSource, /blob\/[a-f0-9]{40}\/$/);
});
test('Runnable Python example preserves articles on errors and maps valid decisions', () => {
  const checks = `
import contextlib,io,json,os,urllib.error
from unittest.mock import patch
code=json.load(__import__('sys').stdin)
ns={'__name__':'example'}
exec(compile(code,'filter_news.py','exec'),ns)
for choice, expected in [('relevant','send_to_writer'),('irrelevant','skip'),('insufficient_evidence','retain_for_review')]:
 assert ns['action_for']({'answers':{'relevance':{'type':'choice','choice':choice}}})==expected
for response in [{'answers':{'relevance':{'type':'choice','choice':'irrelevant'}}}, {'answers':{}}, {'answers':{'relevance':{'type':'choice','choice':'unknown'}}}]:
 output=io.StringIO()
 with patch.dict(os.environ,{'JEV_API_KEY':'test-placeholder'},clear=True), patch('pathlib.Path.read_text',return_value='{}'), patch('urllib.request.build_opener') as opener, contextlib.redirect_stdout(output):
  opener.return_value.open.return_value.__enter__.return_value=io.StringIO(json.dumps(response))
  ns['main']()
 expected='skip' if response.get('answers',{}).get('relevance',{}).get('choice')=='irrelevant' else 'retain_for_review'
 assert json.loads(output.getvalue())['action']==expected
with patch.dict(os.environ,{'JEV_API_KEY':'test-placeholder'},clear=True), patch('pathlib.Path.read_text',return_value='{}'), patch('urllib.request.build_opener') as opener, contextlib.redirect_stdout(io.StringIO()) as output:
 opener.return_value.open.side_effect=urllib.error.URLError('unavailable')
 ns['main']()
 assert json.loads(output.getvalue())['action']=='retain_for_review'
print('Sample branches and failure fallback pass; no network used.')
`;
  const result = spawnSync('python3', ['-c', checks], {input:JSON.stringify(newsPython), encoding:'utf8'});
  assert.equal(result.status, 0, result.stderr);
});
