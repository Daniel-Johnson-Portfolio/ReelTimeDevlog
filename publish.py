"""Publish approved posts: rebuild docs/ (approved posts only), check it for anything that
shouldn't be public, and commit it to the devlog repo.

  python publish.py            # build, check, commit
  python publish.py --push     # also push to the remote (the human runs this, or asks for it)
  python publish.py --force    # commit even if the safety check finds something (human only)

Approve a post by changing   draft: true   to   draft: false   in its entry.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build  # noqa: E402

CHECKS = [
    (r"[A-Za-z]:[\\/]+(Users|Documents and Settings)[\\/]", "a local Windows path"),
    (r"/(home|Users)/[A-Za-z0-9._-]+/", "a local home-folder path"),
    (r"discord(app)?\.com/api/webhooks/", "a Discord webhook URL"),
    (r"ntfy\.sh/[A-Za-z0-9_-]+", "an ntfy topic URL"),
    (r"(?i)\b(api[_-]?key|secret|token|password|passwd)\b\s*[:=]", "something that looks like a credential"),
    (r"\bsk-[A-Za-z0-9_-]{16,}", "something that looks like an API key"),
    (r"\bgh[pousr]_[A-Za-z0-9]{20,}", "something that looks like a GitHub token"),
    (r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "an email address"),
]


def safety_scan():
    problems = []
    for page in sorted(list(build.DOCS.rglob("*.html")) + list(build.DOCS.glob("*.js"))):
        text = page.read_text(encoding="utf-8")
        for pattern, label in CHECKS:
            for m in re.finditer(pattern, text):
                problems.append(f"{page.relative_to(HERE).as_posix()}: {label}: {m.group(0)[:60]}")
    return problems


def git(*args, check=True):
    return subprocess.run(["git", "-C", str(HERE), *args], capture_output=True, text=True, check=check)


def identity():
    has = git("config", "user.email", check=False).stdout.strip()
    return [] if has else ["-c", "user.name=devlog", "-c", "user.email=devlog@local"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--push", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("-m", "--message", default="")
    a = ap.parse_args()

    if not (HERE / ".git").exists():
        sys.exit("The devlog folder isn't a git repo yet. Run setup_neighborhood.py, or: git -C devlog init")

    n = build.build(drafts=False)
    problems = safety_scan()
    if problems and not a.force:
        print("Not published. The safety check found things that shouldn't be public:")
        for p in problems[:30]:
            print("  " + p)
        print("Fix the entries (or, if you're the human and they're fine, rerun with --force).")
        sys.exit(1)

    git("add", "-A")
    if not git("status", "--porcelain").stdout.strip():
        print("Nothing new to publish.")
    else:
        msg = a.message or f"Publish: {n} post(s) live"
        git(*identity(), "commit", "-q", "-m", msg)
        print(f"Committed: {msg}")

    if a.push:
        if not git("remote").stdout.strip():
            print("No remote yet. Add one first:  git -C devlog remote add origin <your repo URL>")
            return
        r = git("push", "-u", "origin", "HEAD", check=False)
        print("Pushed." if r.returncode == 0 else "Push failed:\n" + (r.stderr or r.stdout).strip())


if __name__ == "__main__":
    main()
