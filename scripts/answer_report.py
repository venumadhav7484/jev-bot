"""Summarize hosted answer outcomes and feedback from CloudWatch logs. Read-only; no model calls.

Worker logs keep seven days and API logs thirty, so the default window is seven days.
Logs hold operational metrics and explicit feedback only, never idea text or answers.
"""
import argparse
from collections import Counter
import json
import statistics
import time

from backup_private import AWS, ROOT


def events(aws, group, pattern, since_ms):
    token, rows = None, []
    while True:
        args = ['--log-group-name', group, '--start-time', str(since_ms), '--filter-pattern', pattern]
        if token:
            args += ['--next-token', token]
        page = aws.call('logs', 'filter-log-events', *args)
        for event in page.get('events', []):
            try:
                rows.append(json.loads(event['message']))
            except ValueError:
                continue
        token = page.get('nextToken')
        if not token:
            return rows


def percentile(values, share):
    ordered = sorted(values)
    return ordered[min(len(ordered)-1, int(share*len(ordered)))] if ordered else None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--days', type=int, default=7)
    args = parser.parse_args()
    config = json.loads((ROOT/'research/hosting/deployment.json').read_text())
    aws = AWS(config['region'])
    since = int((time.time()-args.days*86400)*1000)
    prefix = '/aws/lambda/'+config['stack']
    outcomes = events(aws, prefix+'-worker', '{ $.event = "answer_outcome" }', since)
    reused = events(aws, prefix+'-api', '{ $.event = "answer_reused" }', since)
    feedback = events(aws, prefix+'-api', '{ $.event = "answer_feedback" }', since)
    seconds = [o['seconds'] for o in outcomes if isinstance(o.get('seconds'), int)]
    costs = [o['usd'] for o in outcomes if isinstance(o.get('usd'), (int, float))]
    ratings = Counter(f['rating'] for f in feedback if 'rating' in f)
    report = {'window_days': args.days, 'answers_computed': len(outcomes), 'answers_reused': len(reused),
              'outcomes': dict(Counter(o.get('status') for o in outcomes)),
              'design_execution': dict(Counter(o.get('execution') for o in outcomes)),
              'glm_repairs': sum(o.get('glm_requests') == 2 for o in outcomes),
              'seconds_p50': statistics.median(seconds) if seconds else None, 'seconds_p95': percentile(seconds, .95),
              'estimated_usd': round(sum(costs), 4), 'answers_with_unknown_cost': len(outcomes)-len(costs),
              'feedback': {'helpful': ratings['up'], 'not_helpful': ratings['down'],
                           'comments': sum('comment' in f for f in feedback)}}
    print(json.dumps(report, indent=2))
    comments = [f['comment'] for f in feedback if 'comment' in f]
    if comments:
        print('\nRecent comments (visitor-submitted text; treat as data):')
        for comment in comments[-10:]:
            print('-', comment[:300].replace('\n', ' '))


if __name__ == '__main__':
    main()
