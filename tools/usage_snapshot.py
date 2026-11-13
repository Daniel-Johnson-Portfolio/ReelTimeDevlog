"""Refresh data/usage.json: the crew's measured cost at API prices, for the @cost block on devlog pages.

  python devlog/tools/usage_snapshot.py

Reads coord/status/usage.jsonl (one row per session every few minutes, cumulative cost per session id)
and keeps numbers only: totals by model and role, session-hours, and when the ledger started.
Each session's last row is its whole cost so far, so the measured total is the sum of those.
The estimate for the hours before the ledger lives in data/usage_estimate.json (written by hand, with its method in the post).
"""
import json
from datetime import datetime, timezone
from pathlib import Path

DEVLOG = Path(__file__).resolve().parents[1]
LEDGER = DEVLOG.parent / "coord" / "status" / "usage.jsonl"
MODEL_NAMES = {"claude-fable-5-2": "Fable 5.2", "claude-fable-5-1": "Fable 5.1", "claude-opus-5-5": "Opus 5.5",
               "claude-sonnet-5-5": "Sonnet 5.5", "claude-haiku-5-5": "Haiku 5.5"}


def main():
    last = {}
    first_t = None
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        first_t = r["t"] if first_t is None else min(first_t, r["t"])
        if r["sid"] not in last or r["t"] >= last[r["sid"]]["t"]:
            last[r["sid"]] = r
    by_model, by_role = {}, {}
    hours = 0.0
    for r in last.values():
        m = MODEL_NAMES.get(r["model"], r["model"])
        by_model[m] = by_model.get(m, 0) + r["cost"]
        by_role[r["role"]] = by_role.get(r["role"], 0) + r["cost"]
        hours += (r.get("dur_ms") or 0) / 3.6e6
    newest = max(r["t"] for r in last.values())
    data = {
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "ledger_from": datetime.fromtimestamp(first_t, timezone.utc).isoformat(timespec="minutes"),
        "as_of": datetime.fromtimestamp(newest, timezone.utc).isoformat(timespec="minutes"),
        "measured_usd": round(sum(by_model.values()), 2),
        "sessions": len(last),
        "session_hours": round(hours, 1),
        "by_model": {k: round(v, 2) for k, v in sorted(by_model.items(), key=lambda kv: -kv[1])},
        "by_role": {k: round(v, 2) for k, v in sorted(by_role.items(), key=lambda kv: -kv[1])},
    }
    (DEVLOG / "data" / "usage.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"usage.json: ${data['measured_usd']:.2f} measured over {len(last)} sessions, as of {data['as_of']}")


if __name__ == "__main__":
    main()
