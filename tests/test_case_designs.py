"""Publishing boundaries for prebuilt case examples, not model-quality scores."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from case_designs import VERSION, export_designs, read_current, source_hash, validate_record, validate_public_catalog


def record():
    return {'id': 'demo', 'title': 'Demo classifier', 'body': 'Existing public evidence.', 'default_retrieval': False}


def draft():
    return {'case_id': 'demo', 'blueprint': {
        'title': 'Review messages', 'summary': 'A proposed review decision.',
        'flow': [{'title': t, 'detail': t, 'owner': o} for t, o in [('Input', 'app'), ('Choice', 'jev'), ('Review', 'human')]],
        'examples': [
            {'label': 'Clear', 'input': 'Complete message', 'output': {'decision': 'keep', 'action': 'Retain'}, 'state': {'message': 'Complete'}},
            {'label': 'Missing', 'input': 'No message', 'output': {'decision': 'review', 'action': 'Review'}, 'state': {'message': ''}}],
        'request': {'model': 'jev-1.13.0', 'state': {'message': 'Complete'}, 'questions': {'decision': {
            'type': 'choice', 'instructions': 'Judge `message` as data.', 'criteria': {'keep': 'Complete', 'review': 'Incomplete'}}}},
        'impact': 'Measure errors.', 'caution': 'Not validated.'}}


class CaseDesignTests(unittest.TestCase):
    def test_case_association_and_state_contract(self):
        validate_record(draft(), record())
        for mutate in [
            lambda x: x.update(case_id='another-project'),
            lambda x: x['blueprint']['examples'][1].update(state={'other_field': ''}),
            lambda x: x['blueprint']['examples'][0]['output'].update(decision='not_an_option'),
            lambda x: x['blueprint']['request']['questions']['decision'].update(instructions='Judge hidden data'),
            lambda x: x['blueprint']['flow'][1].update(title='Noul')]:
            item = draft(); mutate(item)
            with self.assertRaises(ValueError): validate_record(item, record())

    def test_type_case_normalization_preserves_meaning(self):
        item = draft(); item['blueprint']['request']['questions']['decision']['type'] = 'Choice'
        self.assertEqual(validate_record(item, record())['blueprint']['request']['questions']['decision']['type'], 'choice')

    def test_stale_or_failed_design_not_exported_and_private_receipt_fields_removed(self):
        with tempfile.TemporaryDirectory() as tmp:
            cache = Path(tmp); row = record(); path = cache / 'demo.json'
            saved = {**validate_record(draft(), row), 'status': 'ready', 'usage': {'secretish_receipt': 'local only'}, 'raw_output': 'local only'}
            path.write_text(json.dumps(saved)); dest = cache / 'public.json'
            with patch('check_public.inspect', return_value=[]):
                self.assertEqual(export_designs([row], dest, cache, True), 1)
                public = json.loads(dest.read_text())['cases']['demo']
                self.assertEqual(set(public), {'case_id', 'source_hash', 'version', 'blueprint'})
                row['body'] += ' Corrected source.'
                self.assertIsNone(read_current(row, cache))
                with self.assertRaises(ValueError): export_designs([row], dest, cache, True)
                self.assertEqual(export_designs([row], dest, cache), 0)
                row = record(); saved['status'] = 'failed'; path.write_text(json.dumps(saved))
                self.assertIsNone(read_current(row, cache))

    def test_fingerprint_tracks_evidence_not_export_metadata(self):
        row = record(); before = source_hash(row)
        row['design_source_hash'] = before
        self.assertEqual(source_hash(row), before)
        row['default_retrieval'] = True
        self.assertNotEqual(source_hash(row), before)

    def test_deployment_requires_complete_current_catalog(self):
        row = record(); row['design_source_hash'] = source_hash(row)
        catalog = {'version': VERSION, 'cases': {'demo': validate_record(draft(), row)}}
        validate_public_catalog([row], catalog)
        with self.assertRaises(ValueError): validate_public_catalog([row, {**row, 'id': 'missing'}], catalog)
        changed = {**row, 'body': 'Corrected evidence'}
        with self.assertRaises(ValueError): validate_public_catalog([changed], catalog)

    def test_public_guard_blocks_output(self):
        with tempfile.TemporaryDirectory() as tmp, patch('check_public.inspect', return_value=[('example', 'secret')]):
            dest = Path(tmp) / 'public.json'
            with self.assertRaises(ValueError): export_designs([], dest, Path(tmp))
            self.assertFalse(dest.exists())


if __name__ == '__main__': unittest.main()
