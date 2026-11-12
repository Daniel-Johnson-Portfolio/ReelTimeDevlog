"""Render the devlog's diagram cards (cards/*.html) to web images in media/.

  python devlog/tools/cards.py              # every card
  python devlog/tools/cards.py crew-map     # only cards whose name starts with this

Each card is a fixed 1600x900 HTML page sharing cards/cards.css. A headless Chrome or Edge takes
the screenshot; tools/media.py turns it into the jpg and thumbnail the site uses.
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
CARDS = HERE / "cards"
BROWSERS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


def browser():
    for b in BROWSERS:
        if Path(b).exists():
            return b
    for name in ("chrome", "chromium", "msedge"):
        if shutil.which(name):
            return shutil.which(name)
    sys.exit("No Chrome or Edge found to render the cards.")


def main():
    want = sys.argv[1:]
    exe = browser()
    with tempfile.TemporaryDirectory() as tmp:
        for page in sorted(CARDS.glob("*.html")):
            if want and not any(page.stem.startswith(w) for w in want):
                continue
            png = Path(tmp) / f"{page.stem}.png"
            subprocess.run([exe, "--headless", "--disable-gpu", "--hide-scrollbars",
                            "--force-device-scale-factor=1", "--window-size=1600,900",
                            f"--user-data-dir={Path(tmp) / 'profile'}",
                            f"--screenshot={png}", page.as_uri()],
                           check=True, capture_output=True, timeout=120)
            if not png.exists():
                sys.exit(f"{page.name}: the browser made no screenshot")
            subprocess.run([sys.executable, str(HERE / "tools" / "media.py"), "image", str(png),
                            "--name", page.stem], check=True, capture_output=True)
            print(f"media/{page.stem}.jpg")


if __name__ == "__main__":
    main()
