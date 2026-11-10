#!/usr/bin/env python3
"""Render per-repository Lighthouse audit prompts from the Jarvis catalog."""
import argparse
import datetime
import json
from pathlib import Path
import re
import sys

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE.parent / 'references' / 'worker-prompt.md'
RUNS = HERE.parent / 'runs.json'
# Cataloged repositories with no browser-rendered UI. Workers still check
# applicability, so a stale entry here only costs one short session.
NOT_WEB = {'harryt04/jarvis', 'harryt04/utility-scripts', 'harryt04/agent-skills',
           'harryt04/prompts', 'harryt04/lighthouse'}


def template():
    text = TEMPLATE.read_text()
    match = re.search(r'<!-- BEGIN TEMPLATE -->\n(.*)<!-- END TEMPLATE -->', text, re.S)
    if not match:
        sys.exit(f'template markers missing in {TEMPLATE}')
    return match.group(1).strip()


def targets(catalog, skip, include_unavailable):
    retired = {p['id'] for p in catalog.get('retired_projects', [])}
    skip = {s.lower() for s in skip}
    chosen, skipped = [], []
    for p in catalog['projects']:
        pid = p['id']
        names = {pid.lower(), pid.split('/')[-1].lower(), p['name'].lower(),
                 (p.get('sibling_folder_hint') or '').lower(), *(a.lower() for a in p.get('aliases', []))}
        status = p.get('availability', {}).get('status')
        if pid in retired or p.get('archived'):
            reason = 'retired/archived'
        elif pid in NOT_WEB:
            reason = 'no web UI'
        elif status == 'unavailable' and not include_unavailable:
            reason = 'unavailable in catalog'
        elif names & skip:
            reason = 'skipped by user'
        else:
            chosen.append(p)
            continue
        skipped.append((pid, reason))
    return chosen, skipped


def last_runs(path):
    """Map repo id to the most recent run date recorded in runs.json."""
    if not path.exists():
        return {}
    last = {}
    for run in json.loads(path.read_text()).get('runs', []):
        for pid in run.get('repos', []):
            last[pid] = max(last.get(pid, ''), run['date'])
    return last


def render(p, date):
    slug = p['id'].split('/')[-1]
    brief = (p.get('learning_review') or {}).get('brief') or f'briefs/{slug}.md'
    fields = {'NAME': p['name'], 'REPO_ID': p['id'], 'FOLDER': p.get('sibling_folder_hint') or slug,
              'BRIEF': brief, 'SLUG': slug, 'DATE': date}
    text = template()
    for key, value in fields.items():
        text = text.replace('{{' + key + '}}', value)
    return text


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--catalog', required=True, help='Jarvis projects/catalog.json')
    ap.add_argument('--skip', nargs='*', default=[], help='ids, names, folders, or aliases to skip')
    ap.add_argument('--include-unavailable', action='store_true')
    ap.add_argument('--date', default=datetime.date.today().isoformat())
    ap.add_argument('--format', choices=['markdown', 'json', 'list'], default='markdown')
    ap.add_argument('--runs', type=Path, default=RUNS, help='run log (default: skill runs.json)')
    args = ap.parse_args()
    catalog = json.loads(Path(args.catalog).read_text())
    chosen, skipped = targets(catalog, args.skip, args.include_unavailable)
    last = last_runs(args.runs)
    if args.format == 'list':
        for p in chosen:
            ran = last.get(p['id'], 'not recorded')
            print(f"{p['id']}\t{p.get('sibling_folder_hint') or p['id'].split('/')[-1]}\t{p['name']}\tlast run: {ran}")
        for pid, reason in skipped:
            print(f'# excluded {pid}: {reason}')
        return
    items = [{'id': p['id'], 'name': p['name'], 'folder': p.get('sibling_folder_hint'),
              'last_run': last.get(p['id']),
              'title': f"Lighthouse audit: {p['name']}", 'prompt': render(p, args.date)} for p in chosen]
    if args.format == 'json':
        print(json.dumps({'targets': items, 'excluded': skipped}, indent=2))
        return
    for item in items:
        print(f"## {item['name']} (`{item['id']}`)\n\n````markdown\n{item['prompt']}\n````\n")
    if skipped:
        print('Excluded: ' + ', '.join(f'{pid} ({reason})' for pid, reason in skipped))


if __name__ == '__main__':
    main()
