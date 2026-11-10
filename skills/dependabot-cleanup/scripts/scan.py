#!/usr/bin/env python3
"""Scan an owner's live GitHub repositories for open Dependabot PRs.

Read-only. Uses the authenticated `gh` CLI. Each PR is classified so the
coordinator can decide what to merge, fix, or wait on:

  ready         mergeable, no failing or pending checks, CI ran
  ready-no-ci   mergeable, but the repository reported no checks at all
  ci-pending    checks still running (or mergeability still computing)
  ci-failing    at least one check failed, was cancelled, or timed out
  conflicting   GitHub reports merge conflicts with the base branch
  blocked       draft, or GitHub reports BLOCKED for another reason

`--seen FILE` remembers PR URLs across scans in one cleanup run: PRs absent
from the file are marked `new`, and the file is updated with every URL seen.

`--root DIR` (default: the folder that holds the Jarvis checkout named by
`--catalog`) is searched for each repository's local checkout. A folder counts
only when its `origin` names the repository; catalog folder hints can be stale.

Each row also lists `missing_required_checks`: branch-protection contexts that
no check on the PR reports. A non-empty list means the PR stays BLOCKED even
when every job passes, usually because a workflow job was renamed or split.
"""
import argparse
import concurrent.futures
import json
from pathlib import Path
import re
import subprocess
import sys

DEPENDABOT = 'app/dependabot'
FAILING = {'FAILURE', 'CANCELLED', 'TIMED_OUT', 'ACTION_REQUIRED', 'ERROR', 'STARTUP_FAILURE'}
PASSING = {'SUCCESS', 'SKIPPED', 'NEUTRAL'}
PR_FIELDS = ('number,title,url,headRefName,baseRefName,isDraft,mergeable,'
             'mergeStateStatus,statusCheckRollup,createdAt,headRefOid')


def gh(*args):
    result = subprocess.run(['gh', *args], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f'gh {args[0]} failed')
    return json.loads(result.stdout or 'null')


def retired_ids(catalog_path):
    if not catalog_path or not Path(catalog_path).exists():
        return set(), {}
    catalog = json.loads(Path(catalog_path).read_text())
    retired = {p['id'] for p in catalog.get('retired_projects', [])}
    folders = {p['id']: p.get('sibling_folder_hint') or p['id'].split('/')[-1]
               for p in catalog.get('projects', [])}
    return retired, folders


def git_origin(path):
    result = subprocess.run(['git', '-C', str(path), 'remote', 'get-url', 'origin'],
                            capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else ''


def find_checkout(root, repo, hint):
    """Return the sibling folder whose origin is `repo`, trying the hint first."""
    if not root or not Path(root).is_dir():
        return None
    short = repo.split('/')[-1]
    candidates = [hint, short] + sorted(p.name for p in Path(root).iterdir() if p.is_dir())
    for name in dict.fromkeys(c for c in candidates if c):
        origin = git_origin(Path(root) / name).removesuffix('.git')
        if origin.lower().endswith(repo.lower()):
            return str(Path(root) / name)
    return None


def primary_parent(catalog):
    """Folder holding the primary Jarvis checkout, even when run from a worktree."""
    result = subprocess.run(['git', '-C', str(Path(catalog).resolve().parent), 'rev-parse',
                             '--path-format=absolute', '--git-common-dir'],
                            capture_output=True, text=True)
    if result.returncode != 0:
        return str(Path(catalog).resolve().parents[2])
    return str(Path(result.stdout.strip()).parent.parent)


def required_checks(repo, branch):
    try:
        protection = gh('api', f'repos/{repo}/branches/{branch}/protection')
    except RuntimeError:
        return []  # unprotected, or no permission to read protection
    return ((protection or {}).get('required_status_checks') or {}).get('contexts') or []


def check_state(rollup):
    """Summarize statusCheckRollup into (state, failing check names)."""
    states, failing = [], []
    for check in rollup or []:
        # CheckRun has status/conclusion; StatusContext has state.
        value = (check.get('conclusion') or check.get('state') or '').upper()
        if not value or check.get('status', 'COMPLETED').upper() != 'COMPLETED':
            value = value if value in FAILING | PASSING else 'PENDING'
        states.append(value)
        if value in FAILING:
            failing.append(check.get('name') or check.get('context') or '?')
    if failing:
        return 'failing', failing
    if any(s not in PASSING for s in states):
        return 'pending', []
    return ('passing' if states else 'none'), []


def classify(pr):
    checks, failing = check_state(pr.get('statusCheckRollup'))
    if pr.get('isDraft'):
        return 'blocked', failing
    if pr.get('mergeable') == 'CONFLICTING' or pr.get('mergeStateStatus') == 'DIRTY':
        return 'conflicting', failing
    if checks == 'failing':
        return 'ci-failing', failing
    if checks == 'pending' or pr.get('mergeable') == 'UNKNOWN':
        return 'ci-pending', failing
    if pr.get('mergeStateStatus') == 'BLOCKED':
        return 'blocked', failing
    return ('ready' if checks == 'passing' else 'ready-no-ci'), failing


def is_major(title):
    match = re.search(r'from v?(\d+)[^ ]* to v?(\d+)', title)
    return bool(match) and match.group(1) != match.group(2)


def scan_repo(repo):
    prs = gh('pr', 'list', '-R', repo['nameWithOwner'], '--author', DEPENDABOT,
             '--state', 'open', '--limit', '200', '--json', PR_FIELDS)
    branch = (repo.get('defaultBranchRef') or {}).get('name')
    required = required_checks(repo['nameWithOwner'], branch) if prs else []
    rows = []
    for pr in prs:
        state, failing = classify(pr)
        reported = {c.get('name') or c.get('context') for c in pr.get('statusCheckRollup') or []}
        rows.append({
            'repo': repo['nameWithOwner'],
            'default_branch': (repo.get('defaultBranchRef') or {}).get('name'),
            'number': pr['number'],
            'title': pr['title'],
            'url': pr['url'],
            'head': pr['headRefName'],
            'head_sha': pr['headRefOid'],
            'base': pr['baseRefName'],
            'state': state,
            'failing_checks': failing,
            'major': is_major(pr['title']),
            'created_at': pr['createdAt'],
            'missing_required_checks': [c for c in required if c not in reported],
        })
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--owner', default='harryt04')
    parser.add_argument('--catalog', help='Jarvis projects/catalog.json, to drop retired ids and map folders')
    parser.add_argument('--repos', nargs='*', default=[], help='limit to these repo names')
    parser.add_argument('--skip', nargs='*', default=[], help='repo names to leave out')
    parser.add_argument('--include-forks', action='store_true')
    parser.add_argument('--seen', help='JSON file of PR URLs already seen this run')
    parser.add_argument('--root', help='folder holding local checkouts (default: parent of the Jarvis checkout)')
    parser.add_argument('--format', choices=['json', 'table'], default='table')
    args = parser.parse_args()

    retired, folders = retired_ids(args.catalog)
    root = args.root or (primary_parent(args.catalog) if args.catalog else None)
    wanted = {r.split('/')[-1].lower() for r in args.repos}
    skip = {r.split('/')[-1].lower() for r in args.skip}
    repos = gh('repo', 'list', args.owner, '--limit', '500', '--json',
               'nameWithOwner,isArchived,isFork,defaultBranchRef')
    excluded, targets = [], []
    for repo in repos:
        name = repo['nameWithOwner']
        short = name.split('/')[-1].lower()
        if repo['isArchived']:
            excluded.append((name, 'archived'))
        elif repo['isFork'] and not args.include_forks:
            excluded.append((name, 'fork'))
        elif name in retired:
            excluded.append((name, 'retired in Jarvis catalog'))
        elif short in skip or (wanted and short not in wanted):
            excluded.append((name, 'not requested'))
        else:
            targets.append(repo)

    rows, errors = [], []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(scan_repo, r): r['nameWithOwner'] for r in targets}
        for future in concurrent.futures.as_completed(futures):
            try:
                rows.extend(future.result())
            except RuntimeError as exc:
                errors.append((futures[future], str(exc)))

    seen = set()
    if args.seen and Path(args.seen).exists():
        seen = set(json.loads(Path(args.seen).read_text()))
    for row in rows:
        row['new'] = bool(args.seen) and row['url'] not in seen
        row['local_folder'] = folders.get(row['repo'], row['repo'].split('/')[-1])
    paths = {}
    for repo in {r['repo'] for r in rows}:
        hint = folders.get(repo, repo.split('/')[-1])
        paths[repo] = find_checkout(root, repo, hint)
    for row in rows:
        row['local_path'] = paths[row['repo']]
    if args.seen:
        Path(args.seen).parent.mkdir(parents=True, exist_ok=True)
        Path(args.seen).write_text(json.dumps(sorted(seen | {r['url'] for r in rows}), indent=1))

    rows.sort(key=lambda r: (r['repo'], r['number']))
    counts = {}
    for row in rows:
        counts[row['state']] = counts.get(row['state'], 0) + 1

    if args.format == 'json':
        json.dump({'owner': args.owner, 'scanned_repos': len(targets), 'counts': counts,
                   'prs': rows, 'excluded': excluded, 'errors': errors}, sys.stdout, indent=1)
        print()
        return
    print(f'{len(rows)} open Dependabot PRs in {len({r["repo"] for r in rows})} of '
          f'{len(targets)} scanned repos: ' + ', '.join(f'{k}={v}' for k, v in sorted(counts.items())))
    for row in rows:
        flags = ' MAJOR' if row['major'] else ''
        flags += ' NEW' if row['new'] else ''
        fail = f' [{", ".join(row["failing_checks"])}]' if row['failing_checks'] else ''
        if row['missing_required_checks']:
            fail += f' (required check never reports: {", ".join(row["missing_required_checks"])})'
        print(f'{row["state"]:<12} {row["repo"]}#{row["number"]:<4} {row["title"][:70]}{flags}{fail}')
    for repo in sorted(r for r, p in paths.items() if not p):
        print(f'NO CHECKOUT {repo}: no folder under {root} has this origin')
    for name, reason in errors:
        print(f'ERROR       {name}: {reason}')
    if excluded:
        print('Excluded: ' + '; '.join(f'{n} ({r})' for n, r in excluded))


if __name__ == '__main__':
    main()
