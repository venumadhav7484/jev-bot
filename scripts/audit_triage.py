"""Evaluate a small editorial development sample; never certify the full corpus."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / 'research/triage'
samples = json.loads((WORK/'review-sample.json').read_text())
predictions = {r['message_id']:r for r in map(json.loads,(WORK/'predictions.jsonl').read_text().splitlines())}
evaluated = []
for sample in samples['samples']:
    prediction = predictions.get(sample['message_id'])
    if not prediction:
        continue
    assert prediction['content_hash'] == sample['content_hash'], 'Sample source changed; re-review required'
    evaluated.append({'message_id':sample['message_id'], 'source_url':sample['source_url'],
        'kind_matches':prediction['primary_kind'] in sample['acceptable_kinds'],
        'relation_matches':prediction['jev_relation']==sample['expected_relation'],
        'predicted_kind':prediction['primary_kind'], 'predicted_relation':prediction['jev_relation'],
        'expected_kinds':sample['acceptable_kinds'], 'expected_relation':sample['expected_relation'],
        'rationale':sample['rationale']})
result={'scope':samples['scope'],'sample_count':len(evaluated),'missing_predictions':len(samples['samples'])-len(evaluated),
        'kind_matches':sum(r['kind_matches'] for r in evaluated), 'relation_matches':sum(r['relation_matches'] for r in evaluated),
        'automated_exclusion_approved':False,'records':evaluated}
(WORK/'sample-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))
