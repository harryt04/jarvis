#!/usr/bin/env python3
"""Record a lighthouse-audit run (date and repos) in the skill's runs.json."""
import argparse
import datetime
import json
from pathlib import Path

RUNS = Path(__file__).resolve().parent.parent / 'runs.json'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repos', nargs='+', required=True, help='repo ids launched or printed, e.g. harryt04/wiki')
    ap.add_argument('--skipped', nargs='*', default=[], help='repo ids Harry chose to skip')
    ap.add_argument('--mode', choices=['t3', 'printed'], required=True)
    ap.add_argument('--date', default=datetime.date.today().isoformat())
    ap.add_argument('--runs', type=Path, default=RUNS)
    args = ap.parse_args()
    data = json.loads(args.runs.read_text())
    # A second launch on the same date (for example, retrying failed launches)
    # extends that day's entry instead of adding a duplicate.
    run = next((r for r in data['runs'] if r['date'] == args.date), None)
    if run is None:
        run = {'date': args.date, 'mode': args.mode, 'repos': [], 'skipped': []}
        data['runs'].append(run)
    run['repos'] = sorted(set(run['repos']) | set(args.repos))
    run['skipped'] = sorted((set(run.get('skipped', [])) | set(args.skipped)) - set(run['repos']))
    data['runs'].sort(key=lambda r: r['date'])
    args.runs.write_text(json.dumps(data, indent=2) + '\n')
    print(f"recorded {args.date}: {len(run['repos'])} repos, {len(run['skipped'])} skipped -> {args.runs}")


if __name__ == '__main__':
    main()
