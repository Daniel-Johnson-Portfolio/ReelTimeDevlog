"""Refresh data/crew.json: the crew and its numbers, for the @crew table on devlog pages.
Reads the coord folder and the game repo's history. Only counts and role descriptions are
written, nothing private.

  python devlog/tools/crew_snapshot.py
"""
import json
import os
import re
import subprocess
from collections import Counter
from datetime import datetime
from pathlib import Path

DEVLOG = Path(__file__).resolve().parents[1]
PROJECT = DEVLOG.parent
COORD = Path(os.environ.get("COORD_DIR") or PROJECT / "coord")
FRONT = re.compile(r"\A---[ \t]*\r?\n(.*?)\r?\n---", re.S)


def front(path):
    m = FRONT.match(path.read_text(encoding="utf-8"))
    meta = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
    return meta


def main():
    config = json.loads((COORD / "config.json").read_text(encoding="utf-8"))
    jam = json.loads((COORD / "jam.json").read_text(encoding="utf-8")) if (COORD / "jam.json").exists() else {}

    done, total = Counter(), Counter()
    for p in (COORD / "tasks").glob("T-*.md"):
        meta = front(p)
        owner = meta.get("owner", "")
        total[owner] += 1
        if meta.get("status") == "done":
            done[owner] += 1

    commits = Counter()
    since = jam.get("start", "")
    r = subprocess.run(["git", "-C", str(PROJECT), "log", "--all", "--pretty=%s"] + ([f"--since={since}"] if since else []),
                       capture_output=True, text=True)
    for subject in r.stdout.splitlines():
        m = re.match(r"^\[([a-z0-9-]+)\]", subject.strip())
        if m:
            commits[m.group(1)] += 1

    kit_dir = COORD / "inbox" / "engine" / "done"
    kits = merges = 0
    for p in kit_dir.glob("*.md") if kit_dir.exists() else []:
        t = front(p).get("type")
        kits += t == "kit"
        merges += t == "merge"

    friction = (COORD / "FRICTION.md").read_text(encoding="utf-8") if (COORD / "FRICTION.md").exists() else ""
    decisions = (COORD / "DECISIONS.md").read_text(encoding="utf-8") if (COORD / "DECISIONS.md").exists() else ""
    dec_lines = [l for l in decisions.splitlines() if re.match(r"^- \d{4}-", l.strip())]

    crew = []
    for role, info in config.get("roles", {}).items():
        if not info.get("enabled", True):
            continue
        crew.append({"role": role, "about": info.get("about", ""), "mode": info.get("mode", ""),
                     "tasks_done": done[role], "tasks_total": total[role], "commits": commits[role]})

    data = {
        "generated": datetime.now().astimezone().isoformat(timespec="seconds"),
        "crew": crew,
        "totals": {
            "tasks_done": sum(done.values()), "tasks_total": sum(total.values()),
            "commits": sum(commits.values()), "kits_run": kits, "merges": merges,
            "decisions": len(dec_lines), "assumptions": sum("[assumed]" in l for l in dec_lines),
            "friction_open": friction.count("- [open]"), "friction_fixed": friction.count("- [fixed]"),
            "review_folders": sum(1 for p in (COORD / "review").glob("T-*") if p.is_dir()) if (COORD / "review").exists() else 0,
        },
    }
    (DEVLOG / "data").mkdir(exist_ok=True)
    (DEVLOG / "data" / "crew.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    t = data["totals"]
    print(f"crew.json: {len(crew)} sessions, {t['tasks_done']}/{t['tasks_total']} tasks done, "
          f"{t['commits']} commits, {t['kits_run']} kits, {t['decisions']} decisions")


if __name__ == "__main__":
    main()
