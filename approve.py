"""Approve drafts for publishing (the human's step). Then run publish.py.

  python approve.py                 # list drafts
  python approve.py --all           # approve every draft
  python approve.py <name> [...]    # approve specific entries or pages (file name, or the start of it)
"""
import argparse
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
FRONT = re.compile(r"\A---[ \t]*\r?\n(.*?)\r?\n---", re.S)


def drafts():
    out = []
    for folder in ("entries", "pages"):
        for p in sorted((HERE / folder).glob("*.md")):
            m = FRONT.match(p.read_text(encoding="utf-8"))
            if m and re.search(r"^draft:\s*true\s*$", m.group(1), re.M):
                title = re.search(r"^title:\s*(.*)$", m.group(1), re.M)
                out.append((p, title.group(1).strip() if title else p.stem))
    return out


def approve(path):
    text = path.read_text(encoding="utf-8")
    m = FRONT.match(text)
    head = re.sub(r"^draft:\s*true\s*$", "draft: false", m.group(1), count=1, flags=re.M)
    path.write_text(text[:m.start(1)] + head + text[m.end(1):], encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="*")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    pending = drafts()
    if not a.names and not a.all:
        if not pending:
            print("No drafts waiting.")
        for p, title in pending:
            print(f"{p.parent.name}/{p.stem}\n    {title}")
        print("\nPreview them: python build.py --drafts --serve")
        return
    chosen = pending if a.all else [(p, t) for p, t in pending if any(p.stem.startswith(n) for n in a.names)]
    for p, title in chosen:
        approve(p)
        print(f"approved: {title}")
    if chosen:
        print("\nNow publish: python publish.py")


if __name__ == "__main__":
    main()
