import test from 'node:test';
import assert from 'node:assert/strict';
import {importIdeaFile} from '../web/file-input.mjs';
const file = (name, content) => {const bytes = new TextEncoder().encode(content);return {name, size:bytes.length, arrayBuffer:async()=>bytes.buffer};};
test('Text-file input preserves existing draft and Unicode', async () => {
  assert.equal(await importIdeaFile(file('idea.md','Invoice routing ✓'),'Keep uncertain mail.'),'Keep uncertain mail.\n\nInvoice routing ✓');
});
test('Unsupported, binary, empty and oversized inputs fail without truncation', async () => {
  for (const value of [file('idea.pdf','pdf'),file('idea.txt','\0binary'),file('idea.txt',' '),file('idea.txt','x'.repeat(6001))]) await assert.rejects(importIdeaFile(value));
  await assert.rejects(importIdeaFile(file('idea.txt','x'.repeat(5999)),'abc'));
  await assert.rejects(importIdeaFile({name:'idea.txt',size:300000,arrayBuffer:async()=>{throw Error('should not read')}}),/256 KB/);
  await assert.rejects(importIdeaFile({name:'bad.txt',size:1,arrayBuffer:async()=>new Uint8Array([255]).buffer}),/UTF-8/);
});
