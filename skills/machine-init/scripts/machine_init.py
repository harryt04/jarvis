#!/usr/bin/env python3
"""Initialize indexed checkouts and Bash aliases on the executing machine."""
import argparse
import datetime
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

START = '# >>> Jarvis machine-init >>>'
END = '# <<< Jarvis machine-init <<<'
ALIASES = '''alias awake="echo 'I wont go to sleep!' && setsid -f systemd-inhibit --what=handle-lid-switch:sleep:idle --mode=block sleep infinity"
alias sleepy="echo 'Feeling really sleepy...' && pkill -f 'systemd-inhibit --what=handle-lid-switch'"'''


def run(*args):
    return subprocess.run(args, text=True, capture_output=True, check=True).stdout.strip()


def identity(url):
    match = re.fullmatch(r'(?:https://github\.com/|git@github\.com:|ssh://git@github\.com/)([^/]+/[^/]+?)(?:\.git)?/?', url)
    return match.group(1).lower() if match else None


def inventory(catalog):
    retired = {p['id'] for p in catalog.get('retired_projects', [])}
    result, folders = [], set()
    for p in catalog['projects']:
        if p['id'] in retired or p.get('status') == 'deleted':
            continue
        if not re.fullmatch(r'[\w.-]+/[\w.-]+', p['id']):
            raise ValueError('Invalid repository identity')
        folder = p.get('sibling_folder_hint') or p['id'].split('/')[1]
        if folder in ('.', '..') or not re.fullmatch(r'[\w.-]+', folder) or folder in folders:
            raise ValueError('Invalid or duplicate folder: ' + folder)
        folders.add(folder)
        result.append((p['id'], folder))
    return result


def install_aliases(home):
    path = home / '.bashrc'
    original = path.read_text() if path.exists() else ''
    if original.count(START) != original.count(END) or original.count(START) > 1:
        raise ValueError('Malformed machine-init block in .bashrc')
    if START in original and original.index(END) < original.index(START):
        raise ValueError('Reversed machine-init markers')
    text = re.sub(re.escape(START) + r'.*?' + re.escape(END) + r'\n?', '', original, flags=re.S)
    # Replace these two alias definitions only, retaining all unrelated settings.
    text = re.sub(r'^\s*alias\s+(?:awake|sleepy)=.*(?:\n|$)', '', text, flags=re.M)
    updated = text.rstrip('\n') + '\n\n' + START + '\n' + ALIASES + '\n' + END + '\n'
    if original == updated:
        return 'unchanged'
    with tempfile.NamedTemporaryFile(mode='w', dir=home, delete=False) as f:
        temp = Path(f.name)
        f.write(updated)
    try:
        run('bash', '-n', str(temp))
        if path.exists():
            stamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
            shutil.copy2(path, str(path) + '.machine-init.bak.' + stamp)
            os.chmod(temp, path.stat().st_mode & 0o777)
        # Follow an existing Bash config symlink, preserving the link itself.
        os.replace(temp, path.resolve() if path.is_symlink() else path)
    finally:
        temp.unlink(missing_ok=True)
    return 'installed'


def setup(catalog, home, apply=False):
    entries = inventory(catalog)
    root = home / 'Documents' / 'git'
    if apply:
        root.mkdir(parents=True, exist_ok=True)
    results = []
    for repo, folder in entries:
        dest = root / folder
        item = {'repository': repo, 'path': str(dest)}
        try:
            if dest.exists() or dest.is_symlink():
                top = Path(run('git', '-C', str(dest), 'rev-parse', '--show-toplevel'))
                origin = run('git', '-C', str(dest), 'remote', 'get-url', 'origin')
                if top.resolve() != dest.resolve() or identity(origin) != repo.lower():
                    raise ValueError('Existing checkout identity mismatch')
                item['status'] = 'reused'
            elif not apply:
                item['status'] = 'would-clone'
            else:
                run('git', 'clone', '--', 'https://github.com/' + repo + '.git', str(dest))
                if identity(run('git', '-C', str(dest), 'remote', 'get-url', 'origin')) != repo.lower():
                    raise ValueError('Cloned origin mismatch')
                item['status'] = 'cloned'
            if item['status'] in ('reused', 'cloned'):
                try:
                    item['head'] = run('git', '-C', str(dest), 'rev-parse', '--verify', 'HEAD')
                except subprocess.CalledProcessError:
                    item['status'] = 'empty'
        except (ValueError, subprocess.CalledProcessError) as e:
            item['status'] = 'failed'
            # Do not echo Git stderr or credential-bearing existing URLs.
            item['error'] = str(e) if isinstance(e, ValueError) else 'Git operation failed; inspect access or checkout'
        results.append(item)
    aliases = install_aliases(home) if apply else 'would-install'
    report = {'projects': results, 'aliases': aliases}
    if apply:
        state = home / '.jarvis'
        state.mkdir(mode=0o700, exist_ok=True)
        (state / 'machine-init.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog', type=Path, required=True)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    report = setup(json.loads(args.catalog.read_text()), Path.home(), args.apply)
    print(json.dumps(report, indent=2))
    return int(any(p['status'] in ('failed', 'empty') for p in report['projects']))


if __name__ == '__main__':
    raise SystemExit(main())
