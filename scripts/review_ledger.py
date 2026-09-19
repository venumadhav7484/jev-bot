"""Record explicit editorial decisions against immutable local message evidence.

This tool never infers review decisions from model predictions. Input decisions
must be supplied after inspecting the corresponding source and its context.
"""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = ROOT / 'research/editorial'
LEDGER = ROOT / 'resource-pool/sources/editorial-review.json'


def main():
    parser = argparse.ArgumentParser(__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    show = sub.add_parser('show')
    show.add_argument('start', type=int)
    show.add_argument('stop', type=int)
    apply = sub.add_parser('apply')
    apply.add_argument('decisions', type=Path)
    args = parser.parse_args()
    queue = json.loads((DIRECTORY / 'queue.json').read_text())
    if args.command == 'show':
        for index in range(args.start, min(args.stop, len(queue))):
            row = queue[index]
            print(f'[{index}] {row["message_id"]} {row["body"]}')
            if row['quote_context']:
                print('CONTEXT:', row['quote_context'])
        return
    ledger = json.loads(LEDGER.read_text()) if LEDGER.exists() else {}
    supplied = json.loads(args.decisions.read_text())
    seen = set()
    for decision in supplied:
        assert decision['reason'].strip(), 'Every decision needs a reason'
        for index in decision['indices']:
            assert index not in seen, f'Duplicate decision for queue index {index}'
            seen.add(index)
            row = queue[index]
            entry = {k: v for k, v in decision.items() if k != 'indices'}
            entry.update(message_id=row['message_id'], source_url=row['source_url'],
                         content_hash=row['content_hash'],
                         review_method='assistant_read_body_and_available_context',
                         reviewed_at=datetime.now(timezone.utc).isoformat(),
                         decision_batch=args.decisions.name)
            ledger[row['message_id']] = entry
    LEDGER.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + '\n')
    print(f'Recorded {len(seen)} decisions; {len(ledger)} reviewed messages total')


if __name__ == '__main__':
    main()
