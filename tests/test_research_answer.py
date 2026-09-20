import base64
import hashlib
import io
import json
from pathlib import Path
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch
from unittest.mock import Mock
import urllib.error

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import knowledge_corpus as corpus
import research_answer as bot
import answer_writer as writer


def library():
    return corpus.assemble([
        corpus.document('docs/jev-master-guide.md', '# Master\n'+'Independent lessons and corrections.\n'*220),
        corpus.document('docs/use-cases/unusual.md', '# Unusual case\nA new workflow outside all eleven old categories.'),
        corpus.document('docs/use-cases/held.md', '# Held case\nInsufficient evidence. Do not infer validation.'),
        corpus.document('docs/community-evidence-findings.md', '# Findings\nContradictory results.'),
    ], 'local')


def provider(payload):
    answers = {}
    for key, q in payload['questions'].items():
        if q['type'] == 'noul':
            answers[key] = {'type': 'noul', 'noul': .8}
        else:
            choice = next(iter(q['criteria']))
            answers[key] = {'type': 'choice', 'choice': choice, 'confidence': .8,
                            'probabilities': {k: float(k == choice) for k in q['criteria']}}
    return {'model': 'test', 'answers': answers, 'usage': {'input_tokens': 10, 'output_tokens': 0}}, False


class FullLibrary(unittest.TestCase):
    def test_lossless_passages_and_every_document_sent(self):
        lib = library()
        rows = corpus.passages(lib)
        for doc in lib['documents']:
            self.assertEqual(''.join(r['text'] for r in rows if r['path'] == doc['path']), doc['body'])
        work = list(bot.batches('x'*6000, rows))
        self.assertEqual([r['id'] for group, _ in work for r in group], [r['id'] for r in rows])
        self.assertTrue(all(bot.bounded(payload) for _, payload in work))
        seen = set()
        def fake(payload):
            seen.update(r['path'] for r in payload['state'].get('passages', {}).values())
            return provider(payload)
        with patch.object(bot, 'request', side_effect=fake), patch.object(bot, 'api_key', return_value='test'):
            result = bot.answer('A novel workflow', corpus=lib)
        self.assertEqual(seen, {d['path'] for d in lib['documents']})
        self.assertTrue(result['coverage']['full_library_evaluated'])
        self.assertEqual(result['coverage']['documents_evaluated'], 4)
        self.assertIsNotNone(result['judgments'])

    def test_failed_scan_never_claims_full_coverage_or_generates_answer(self):
        with patch.object(bot, 'api_key', return_value='test'), patch.object(bot, 'request', side_effect=RuntimeError('private-secret')):
            result = bot.answer('A novel workflow', corpus=library())
        self.assertFalse(result['coverage']['full_library_evaluated'])
        self.assertIsNone(result['judgments'])
        self.assertNotIn('private-secret', json.dumps(result))

    def test_writer_gets_selected_evidence_and_failure_preserves_jev_result(self):
        with patch.object(bot, 'api_key', return_value='test'), patch.object(bot, 'request', side_effect=provider), patch.object(writer, 'settings', return_value='test'), patch.object(writer, 'write_answer', side_effect=RuntimeError('private-secret')) as write:
            result = bot.answer('A novel workflow', 'written', corpus=library())
        self.assertEqual(write.call_args.args[1], result['evidence'])
        self.assertTrue(result['coverage']['full_library_evaluated'])
        self.assertIsNotNone(result['judgments'])
        self.assertIsNone(result['narrative'])
        self.assertNotIn('private-secret', json.dumps(result))

    def test_missing_writer_configuration_fails_before_paid_scan(self):
        with patch.object(writer, 'settings', side_effect=ValueError('missing')), patch.object(bot, 'request') as call:
            with self.assertRaises(ValueError):
                bot.answer('A novel workflow', 'written', corpus=library())
        call.assert_not_called()

    def test_no_relevant_passage_does_not_force_a_fit(self):
        def irrelevant(payload):
            value, _ = provider(payload)
            for answer in value['answers'].values():
                answer['noul'] = .1
            return value, False
        with patch.object(bot, 'api_key', return_value='test'), patch.object(bot, 'request', side_effect=irrelevant):
            result = bot.answer('Unknown request', corpus=library())
        self.assertFalse(result['evidence'])
        self.assertIsNone(result['judgments'])

    def test_real_library_includes_all_cases_and_core_guides(self):
        lib = corpus.load()
        paths = {d['path'] for d in lib['documents']}
        published = json.loads((corpus.ROOT/'docs/bot-cases.json').read_text())
        self.assertEqual(lib['case_count'], len(published))
        self.assertEqual({d['path'] for d in lib['documents'] if d['path'].startswith('docs/use-cases/')},
                         {r['path'] for r in published})
        self.assertEqual(sum(d['default_retrieval'] is False for d in lib['documents']),
                         sum(r['default_retrieval'] is False for r in published))
        for path in ('jev-master-guide.md', 'jev-knowledge-reference.md', 'community-evidence-findings.md', 'incremental-findings.md'):
            self.assertIn('docs/'+path, paths)


class S3Snapshot(unittest.TestCase):
    def archive(self, path, entries):
        with tarfile.open(path, 'w:gz') as bundle:
            for name, content in entries.items():
                data = content.encode(); item = tarfile.TarInfo(name); item.size = len(data)
                bundle.addfile(item, io.BytesIO(data))

    def test_archive_loads_only_research_markdown_and_never_extracts(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'archive.tar.gz'
            self.archive(path, {'docs/guide.md': '# Guide\nEvidence.', 'research/private.txt': 'private', '.env.local': 'secret', 'docs/binary.png': 'binary'})
            lib = corpus.from_archive(path, 's3', 'test')
            self.assertEqual([d['path'] for d in lib['documents']], ['docs/guide.md'])
            self.assertFalse((Path(directory)/'docs').exists())
            self.archive(path, {'docs/../outside.md': 'bad'})
            with self.assertRaises(ValueError):
                corpus.from_archive(path, 's3', 'test')

    def test_s3_cache_checksum_and_snapshot_are_used_not_current_local_docs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); storage = root/'research/storage'; (storage/'snapshot').mkdir(parents=True)
            archive = storage/'snapshot/verified-download.tar.gz'
            self.archive(archive, {'docs/guide.md': '# Frozen\nOriginal.'})
            checksum = base64.b64encode(corpus.digest_file(archive)).decode()
            receipt = {'bucket': 'test', 'region': 'us-east-1', 'completed_at': 'test-date', 'download_and_file_hashes_verified': True,
                       'objects': [{'key': 'snapshots/snapshot/evidence.tar.gz', 'version_id': 'v1', 'sha256_base64': checksum}]}
            (storage/'latest-backup.json').write_text(json.dumps(receipt))
            (storage/'s3-config.json').write_text(json.dumps({'bucket': 'test', 'region': 'us-east-1', 'account_id': 'test'}))
            (root/'docs').mkdir(); (root/'docs/guide.md').write_text('Different live copy')
            with patch.object(corpus, 'AWS') as aws:
                lib = corpus.load('s3', root)
            aws.assert_not_called()
            self.assertEqual(lib['documents'][0]['body'], '# Frozen\nOriginal.')
            self.assertEqual(lib['snapshot'], 'test-date')


def blueprint():
    return {'title': 'Route tickets', 'summary': 'Choose a queue.',
            'flow': [{'title': name, 'detail': 'Example step.', 'owner': owner} for name, owner in [('Email', 'app'), ('Choice', 'jev'), ('Queue', 'app')]],
            'examples': [{'label': 'Invoice', 'input': 'Invoice attached.', 'output': {'queue': 'billing'}, 'state': {'text': 'Invoice attached.'}}],
            'request': {'model': 'jev-1.13.0', 'state': {'text': 'Invoice attached.'}, 'questions': {'queue': {'type': 'choice', 'instructions': 'Choose a queue for text.', 'criteria': {'billing': 'Invoice', 'review': 'Unclear'}}}},
            'impact': 'Reduce manual sorting.', 'caution': 'Review unclear mail.'}


class WriterCitations(unittest.TestCase):
    def test_fabricated_and_missing_citations_are_rejected(self):
        for citations in ([], ['invented']):
            value = {'sections': [{'heading': 'Claim', 'paragraphs': [{'text': 'A fact', 'kind': 'source_fact', 'citations': citations}]}]}
            with self.assertRaises(ValueError):
                writer.validate_narrative(value, [{'id': 'p1'}])
        value['sections'][0]['paragraphs'][0]['citations'] = ['p1']
        self.assertEqual(writer.validate_narrative(value, [{'id': 'p1'}]), value['sections'])

    def test_glm_transport_parses_cited_json_and_does_not_expose_reasoning(self):
        narrative={'sections':[{'heading':'Fit','paragraphs':[{'text':'A supported fact.','kind':'source_fact','citations':['p1']}]}]}
        narrative['blueprint'] = blueprint()
        response={'model':'glm-5.3','choices':[{'finish_reason':'stop','message':{'content':json.dumps(narrative),'reasoning_content':'not user-facing'}}], 'usage':{'prompt_tokens':20,'completion_tokens':10}}
        opener=Mock(); opener.open.return_value=io.BytesIO(json.dumps(response).encode())
        with patch.object(writer,'settings',return_value='test-secret'), patch('answer_writer.urllib.request.build_opener',return_value=opener):
            sections,metadata=writer.write_answer('An idea',[{'id':'p1','text':'A supported fact.'}],{})
        sent=json.loads(opener.open.call_args.args[0].data)
        self.assertEqual(sent['model'],'glm-5.3')
        self.assertNotIn('tools',sent)
        self.assertEqual(sections,narrative['sections'])
        self.assertTrue(metadata['citation_ids_validated'])
        self.assertNotIn('not user-facing',json.dumps([sections,metadata]))

    def test_blueprint_rejects_inconsistent_or_invalid_copyable_requests(self):
        import copy
        valid = blueprint()
        self.assertEqual(writer.validate_blueprint(valid), valid)
        mutations = [lambda b: b['request'].update(state={'wrong': 'input'}),
                     lambda b: b['request']['questions']['queue'].update(type='generate'),
                     lambda b: b['request'].update(api_key='secret'),
                     lambda b: b['flow'][0].update(owner='jev executes payments'),
                     lambda b: b['request']['questions']['queue'].update(criteria=['wrong'])]
        for mutate in mutations:
            value = copy.deepcopy(valid); mutate(value)
            with self.assertRaises(ValueError): writer.validate_blueprint(value)

    def test_useful_flow_is_not_rejected_for_minor_length_variation(self):
        value = blueprint()
        value['flow'][0]['detail'] = 'x' * 148
        self.assertEqual(writer.validate_blueprint(value)['flow'][0]['detail'], 'x' * 148)
        value['flow'][0]['detail'] = 'x' * 301
        with self.assertRaises(ValueError): writer.validate_blueprint(value)

    def test_blueprint_repairs_question_names_without_changing_decisions(self):
        value = blueprint()
        question = value['request']['questions']['queue']
        value['request']['questions'] = [question]
        value['extra_prose'] = 'This must not reach the public renderer.'
        result = writer.validate_blueprint(value)
        self.assertEqual(result['request']['questions'], {'decision_1': question})
        self.assertNotIn('extra_prose', result)

    def test_glm_balance_failure_has_fixed_safe_message(self):
        error=urllib.error.HTTPError(writer.ENDPOINT,429,'limit',{},io.BytesIO(b'{"error":{"code":"1113","message":"private-secret"}}'))
        opener=Mock(); opener.open.side_effect=error
        with patch.object(writer,'settings',return_value='test-secret'), patch('answer_writer.urllib.request.build_opener',return_value=opener):
            with self.assertRaisesRegex(writer.WriterUnavailable,'1113') as caught:
                writer.write_answer('An idea',[{'id':'p1'}],{})
        self.assertNotIn('private-secret',str(caught.exception))


if __name__ == '__main__':
    unittest.main()
