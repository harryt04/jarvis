#!/usr/bin/env python3
"""Find Treehouse slots whose PR has merged, and optionally reclaim them.

Dry run by default. With --apply, for each reclaimable slot it terminates
processes running inside the slot (SIGTERM, then SIGKILL after a grace period)
and runs `treehouse return <path> --if-lease-id <id>`. Slots that are dirty,
ahead of the merged PR head, unmerged, or unverifiable are never touched.
"""
import argparse, json, os, signal, subprocess, sys, time
from pathlib import Path

ROOT = Path(os.environ.get("TREEHOUSE_ROOT", Path.home() / ".treehouse"))
NODE_NAMES = {"node", "npm", "npx", "pnpm", "yarn", "bun", "deno", "next-server", "tsx", "vite"}


def run(cmd, cwd=None, env=None):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                       env={**os.environ, **env} if env else None)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def pool_slots(pool_dir):
    """Status JSON for one pool, read from inside any of its worktrees.

    Treehouse reports the slot it runs from as "you're here", without its lease
    state or branch, so that entry is filled in from the pool's state file.
    """
    for wt in sorted(pool_dir.glob("*/*/.git")):
        code, out, _ = run(["treehouse", "status", "--json"], cwd=wt.parent)
        if code == 0 and out.startswith("["):
            slots = json.loads(out)
            break
    else:
        return []
    try:
        state = {w["path"]: w for w in json.loads((pool_dir / "treehouse-state.json").read_text())["worktrees"]}
    except (OSError, ValueError, KeyError):
        state = {}
    for slot in slots:
        if slot["status"] in ("leased", "available", "dirty", "in-use", "damaged"):
            continue
        saved = state.get(slot["path"])
        if saved is None:
            slot["status"] = "unknown"
            continue
        slot["status"] = "leased" if saved.get("leased") else "available"
        slot["lease_id"] = saved.get("lease_id", "")
        slot["branch"] = run(["git", "branch", "--show-current"], cwd=slot["path"])[1]
    return slots


def gh_repo(path):
    """owner/repo for origin. Reads the configured URL, before any insteadOf
    rewrite to an SSH host alias such as git@github-<user>:owner/repo."""
    code, url, _ = run(["git", "config", "--get", "remote.origin.url"], cwd=path)
    if code:
        return None
    if "github.com" in url:
        slug = url.split("github.com", 1)[1].lstrip(":/")
    elif url.startswith("git@github") and ":" in url:
        slug = url.split(":", 1)[1]
    else:
        return None
    slug = slug.rstrip("/")
    return slug[:-4] if slug.endswith(".git") else slug


def is_ancestor(path, a, b):
    return run(["git", "merge-base", "--is-ancestor", a, b], cwd=path)[0] == 0


def _ppid(pid):
    if Path("/proc").is_dir():
        return int(Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()[1])
    return int(run(["ps", "-o", "ppid=", "-p", str(pid)])[1])


def _cwds():
    """Yield (pid, cwd, comm, args_fn) for every readable process."""
    if Path("/proc").is_dir():
        for d in Path("/proc").iterdir():
            if not d.name.isdigit():
                continue
            try:
                yield int(d.name), os.readlink(d / "cwd"), (d / "comm").read_text().strip(), \
                    lambda d=d: (d / "cmdline").read_bytes().replace(b"\0", b" ").decode(errors="replace").strip()
            except (OSError, PermissionError):
                continue
        return
    # macOS has no /proc. lsof reports each process's cwd and command name.
    _, out, _ = run(["lsof", "-n", "-w", "-d", "cwd", "-F", "pcn"])
    pid = comm = None
    for line in out.splitlines():
        tag, val = line[:1], line[1:]
        if tag == "p":
            pid, comm = int(val), ""
        elif tag == "c":
            comm = val
        elif tag == "n" and pid is not None:
            yield pid, val, comm, lambda pid=pid: run(["ps", "-o", "args=", "-p", str(pid)])[1]


def _alive(pid):
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True


def processes_in(path):
    """PIDs whose cwd is inside the slot, excluding this script's own ancestry."""
    protect, pid = set(), os.getpid()
    while pid > 1:
        protect.add(pid)
        try:
            pid = _ppid(pid)
        except Exception:
            break
    found, prefix = [], str(Path(path).resolve())
    for pid, cwd, comm, args in _cwds():
        if pid in protect:
            continue
        if cwd == prefix or cwd.startswith(prefix + "/"):
            found.append({"pid": pid, "comm": comm, "node": comm in NODE_NAMES, "args": args()[:160]})
    return found


def classify(slot):
    path, branch = slot["path"], slot.get("branch") or ""
    r = {"pool": Path(path).parent.parent.name, "name": slot["name"], "path": path,
         "branch": branch, "status": slot["status"], "lease_id": slot.get("lease_id", ""),
         "verdict": "keep", "reason": "", "pr": None}
    if slot["status"] != "leased":
        r["reason"] = f"slot is {slot['status']}"
        return r
    if not branch or branch == "HEAD":
        r["reason"] = "detached HEAD; no branch to match"
        return r
    if run(["git", "status", "--porcelain"], cwd=path)[1]:
        r["reason"] = "uncommitted or untracked changes"
        return r
    repo = gh_repo(path)
    if not repo:
        r["reason"] = "origin is not a GitHub remote"
        return r
    cmd = ["gh", "pr", "list", "--repo", repo, "--head", branch, "--state", "all",
           "--json", "number,state,headRefOid,url,mergedAt"]
    code, out, err = run(cmd)
    if code and "Could not resolve to a Repository" in err:
        # A private repo may need another logged-in gh account, e.g. the owner's.
        tcode, token, _ = run(["gh", "auth", "token", "--user", repo.split("/")[0]])
        if tcode == 0 and token:
            code, out, err = run(cmd, env={"GH_TOKEN": token})
    if code:
        r["verdict"], r["reason"] = "unknown", f"gh failed: {err[:120]}"
        return r
    prs = json.loads(out or "[]")
    if any(p["state"] == "OPEN" for p in prs):
        r["reason"], r["pr"] = "PR still open", next(p["url"] for p in prs if p["state"] == "OPEN")
        return r
    merged = [p for p in prs if p["state"] == "MERGED"]
    if not merged:
        r["reason"] = "no merged PR for branch" + (" (closed unmerged)" if prs else "")
        return r
    head = run(["git", "rev-parse", "HEAD"], cwd=path)[1]
    run(["git", "fetch", "-q", "origin", f"refs/pull/{merged[0]['number']}/head"], cwd=path)
    for p in merged:
        if head == p["headRefOid"] or is_ancestor(path, head, p["headRefOid"]):
            r["verdict"], r["pr"], r["reason"] = "reclaim", p["url"], f"merged {p['mergedAt'][:10]}"
            return r
    r["pr"] = merged[0]["url"]
    r["reason"] = "local HEAD has commits not in the merged PR"
    return r


def terminate(procs, grace):
    for p in procs:
        try: os.kill(p["pid"], signal.SIGTERM)
        except ProcessLookupError: pass
    deadline = time.time() + grace
    while time.time() < deadline and any(_alive(p["pid"]) for p in procs):
        time.sleep(0.2)
    for p in procs:
        try: os.kill(p["pid"], signal.SIGKILL)
        except ProcessLookupError: pass


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true", help="kill slot processes and return reclaimable slots")
    ap.add_argument("--pool", action="append", help="limit to pool dir name(s), e.g. jarvis-8f4df2")
    ap.add_argument("--skip", action="append", default=[], metavar="POOL/NAME",
                    help="keep this slot even if reclaimable, e.g. dexter-d89663/10")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--grace", type=float, default=5.0, help="seconds between SIGTERM and SIGKILL")
    a = ap.parse_args()

    pools = [p for p in sorted(ROOT.iterdir()) if p.is_dir() and (not a.pool or p.name in a.pool)]
    results = []
    for pool in pools:
        for slot in pool_slots(pool):
            r = classify(slot)
            if r["verdict"] == "reclaim" and f"{r['pool']}/{r['name']}" in a.skip:
                r["verdict"], r["reason"] = "keep", f"skipped by --skip ({r['reason']})"
            r["processes"] = processes_in(r["path"]) if Path(r["path"]).exists() else []
            results.append(r)

    if a.apply:
        for r in results:
            if r["verdict"] != "reclaim":
                continue
            terminate(r["processes"], a.grace)
            cmd = ["treehouse", "return", r["path"]]
            if r["lease_id"]:
                cmd += ["--if-lease-id", r["lease_id"]]
            code, out, err = run(cmd, cwd=r["path"])
            r["applied"] = "returned" if code == 0 else f"return failed: {(err or out)[-200:]}"

    if a.json:
        print(json.dumps(results, indent=2))
        return
    for verdict in ("reclaim", "unknown", "keep"):
        rows = [r for r in results if r["verdict"] == verdict]
        if not rows:
            continue
        print(f"\n== {verdict.upper()} ({len(rows)})")
        for r in rows:
            procs = ", ".join(f"{p['comm']}:{p['pid']}" for p in r["processes"]) or "-"
            extra = f"  [{r['applied']}]" if "applied" in r else ""
            print(f"{r['pool']}/{r['name']:<3} {r['branch'] or '-':<40} {r['reason']:<45} procs={procs} {r['pr'] or ''}{extra}")
    held = sum(r["status"] not in ("available",) for r in results)
    print(f"\n{len(results)} slots, {held} held, {sum(r['verdict']=='reclaim' for r in results)} reclaimable"
          + ("" if a.apply else " (dry run; pass --apply to reclaim)"))


if __name__ == "__main__":
    sys.exit(main())
