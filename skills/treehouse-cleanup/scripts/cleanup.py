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


def run(cmd, cwd=None):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


def pool_slots(pool_dir):
    """Status JSON for one pool, read from inside any of its worktrees."""
    for wt in sorted(pool_dir.glob("*/*/.git")):
        code, out, _ = run(["treehouse", "status", "--json"], cwd=wt.parent)
        if code == 0 and out.startswith("["):
            return json.loads(out)
    return []


def gh_repo(path):
    code, url, _ = run(["git", "remote", "get-url", "origin"], cwd=path)
    if code or "github.com" not in url:
        return None
    slug = url.split("github.com", 1)[1].lstrip(":/")
    return slug[:-4] if slug.endswith(".git") else slug


def is_ancestor(path, a, b):
    return run(["git", "merge-base", "--is-ancestor", a, b], cwd=path)[0] == 0


def processes_in(path):
    """PIDs whose cwd is inside the slot, excluding this script's own ancestry."""
    protect, pid = set(), os.getpid()
    while pid > 1:
        protect.add(pid)
        try:
            pid = int(Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()[1])
        except Exception:
            break
    found, prefix = [], str(Path(path).resolve())
    for d in Path("/proc").iterdir():
        if not d.name.isdigit() or int(d.name) in protect:
            continue
        try:
            cwd = os.readlink(d / "cwd")
            comm = (d / "comm").read_text().strip()
            args = (d / "cmdline").read_bytes().replace(b"\0", b" ").decode(errors="replace").strip()
        except (OSError, PermissionError):
            continue
        if cwd == prefix or cwd.startswith(prefix + "/"):
            found.append({"pid": int(d.name), "comm": comm, "node": comm in NODE_NAMES, "args": args[:160]})
    return found


def classify(slot):
    path, branch = slot["path"], slot.get("branch") or ""
    r = {"pool": Path(path).parent.parent.name, "name": slot["name"], "path": path,
         "branch": branch, "status": slot["status"], "lease_id": slot.get("lease_id", ""),
         "verdict": "keep", "reason": "", "pr": None}
    if slot["status"] in ("available", "damaged"):
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
    code, out, err = run(["gh", "pr", "list", "--repo", repo, "--head", branch, "--state", "all",
                          "--json", "number,state,headRefOid,url,mergedAt"])
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
    while time.time() < deadline and any(Path(f"/proc/{p['pid']}").exists() for p in procs):
        time.sleep(0.2)
    for p in procs:
        try: os.kill(p["pid"], signal.SIGKILL)
        except ProcessLookupError: pass


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true", help="kill slot processes and return reclaimable slots")
    ap.add_argument("--pool", action="append", help="limit to pool dir name(s), e.g. jarvis-8f4df2")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--grace", type=float, default=5.0, help="seconds between SIGTERM and SIGKILL")
    a = ap.parse_args()

    pools = [p for p in sorted(ROOT.iterdir()) if p.is_dir() and (not a.pool or p.name in a.pool)]
    results = []
    for pool in pools:
        for slot in pool_slots(pool):
            r = classify(slot)
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
