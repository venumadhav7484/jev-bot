import io
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import model_costs as costs
import answer_writer as writer
import research_answer as bot
from test_research_answer import library, provider


class TokenCosts(unittest.TestCase):
    def test_verified_rates_and_cached_glm_input(self):
        jev = costs.normalized('jev', {'input_tokens': 300822, 'output_tokens': 23282})
        self.assertAlmostEqual(costs.estimate('jev', 'jev-1.13.0', jev)['usd'], .012634524)
        glm = costs.normalized('glm', {'prompt_tokens': 1000000, 'completion_tokens': 100000,
                                      'prompt_tokens_details': {'cached_tokens': 250000}})
        self.assertAlmostEqual(costs.estimate('glm', 'glm-5.3', glm)['usd'], 1.555)
        self.assertEqual(glm['total_tokens'], 1100000)

    def test_missing_invalid_usage_and_unknown_models_are_not_free(self):
        for raw in ({}, {'prompt_tokens': True, 'completion_tokens': 1},
                    {'prompt_tokens': -1, 'completion_tokens': 2},
                    {'prompt_tokens': 5, 'completion_tokens': 2, 'prompt_tokens_details': {'cached_tokens': 6}}):
            self.assertIsNone(costs.estimate('glm', 'glm-5.3', costs.normalized('glm', raw))['usd'])
        self.assertIsNone(costs.estimate('glm', 'future-model', {'input_tokens': 1, 'output_tokens': 1})['usd'])
        known = costs.estimate('glm', 'glm-5.3', costs.normalized('glm', {'prompt_tokens': 10, 'completion_tokens': 1}))
        self.assertIn('uncached', known['assumption'])

    def test_cached_jev_work_adds_zero_new_tokens_and_cost(self):
        def cached(payload):
            result, _ = provider(payload)
            return result, True
        with patch.object(bot, 'api_key', return_value='test'), patch.object(bot, 'request', side_effect=cached):
            result = bot.answer('An idea', corpus=library())
        row = result['comparison']['rows'][0]
        self.assertGreater(row['cached_requests'], 0)
        self.assertEqual(row['tokens']['total_tokens'], 0)
        self.assertEqual(row['cost']['usd'], 0)

    def test_successful_written_run_combines_reported_usage_without_extra_calls(self):
        def jev(payload):
            result, cached = provider(payload)
            result['model'] = 'jev-1.13.0'
            return result, cached
        tokens = costs.normalized('glm', {'prompt_tokens': 100, 'completion_tokens': 20})
        metadata = {'model': 'glm-5.3', 'tokens': tokens, 'cost': costs.estimate('glm', 'glm-5.3', tokens)}
        with patch.object(bot, 'api_key', return_value='test'), patch.object(bot, 'request', side_effect=jev), patch.object(writer, 'settings', return_value='test'), patch.object(writer, 'write_answer', return_value=([], metadata)) as call:
            result = bot.answer('An idea', mode='written', corpus=library())
        call.assert_called_once()
        rows = result['comparison']['rows']
        self.assertEqual([r['provider'] for r in rows], ['jev', 'glm'])
        self.assertEqual([r['status'] for r in rows], ['success', 'success'])
        self.assertAlmostEqual(result['comparison']['total_estimated_usd'], sum(r['cost']['usd'] for r in rows))

    def test_failed_or_retried_requests_keep_total_unknown(self):
        def retried(payload):
            result, cached = provider(payload)
            result.update(model='jev-1.13.0', _unreported_attempts=1)
            return result, cached
        with patch.object(bot, 'api_key', return_value='test'), patch.object(bot, 'request', side_effect=retried):
            result = bot.answer('An idea', corpus=library())
        self.assertIsNone(result['comparison']['total_estimated_usd'])
        self.assertGreater(result['comparison']['rows'][0]['cost']['known_usage_usd'], 0)
        with patch.object(bot, 'api_key', return_value='test'), patch.object(bot, 'request', side_effect=RuntimeError('hidden')):
            result = bot.answer('An idea', corpus=library())
        self.assertIsNone(result['comparison']['rows'][0]['cost']['usd'])

    def test_glm_failure_preserves_jev_usage_without_zero_charge(self):
        with patch.object(bot, 'api_key', return_value='test'), patch.object(bot, 'request', side_effect=provider), patch.object(writer, 'settings', return_value='test'), patch.object(writer, 'write_answer', side_effect=writer.WriterUnavailable('GLM account error 1113')):
            result = bot.answer('An idea', mode='written', corpus=library())
        self.assertIsNone(result['comparison']['total_estimated_usd'])
        row = result['comparison']['rows'][1]
        self.assertEqual(row['status'], 'failed')
        self.assertIsNone(row['tokens']['input_tokens'])
        self.assertIsNone(row['cost']['usd'])

    def test_invalid_answer_retains_usage_and_estimate(self):
        response = {'model': 'glm-5.3', 'usage': {'prompt_tokens': 20, 'completion_tokens': 10},
                    'choices': [{'finish_reason': 'length', 'message': {'content': ''}}]}
        opener = Mock(); opener.open.return_value = io.BytesIO(json.dumps(response).encode())
        with patch.object(writer, 'settings', return_value='test'), patch('answer_writer.urllib.request.build_opener', return_value=opener):
            with self.assertRaises(writer.WriterOutputError) as caught:
                writer.write_answer('An idea', [], {})
        self.assertEqual(caught.exception.metadata['tokens']['output_tokens'], 10)
        self.assertGreater(caught.exception.metadata['cost']['usd'], 0)


if __name__ == '__main__':
    unittest.main()
