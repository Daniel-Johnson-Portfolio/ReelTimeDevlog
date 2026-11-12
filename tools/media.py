"""Prepare web-friendly media for the devlog (needs ffmpeg). Outputs go to devlog/media/.

  python devlog/tools/media.py clip  <input.mp4> --name arena-first-fight --start 3 --seconds 8
  python devlog/tools/media.py clip  <input.mp4> --name footsteps --keep-audio   # Sound posts keep their sound
  python devlog/tools/media.py image <input.png> --name arena-dusk
  python devlog/tools/media.py still <input.mp4> --at 4.5 --name arena-still   # a still from a clip

Clips: H.264, no audio, max 1280 wide, fast-start, plus a poster still and a small thumbnail.
Images: max 1920 wide, plus a small thumbnail. Thumbnails keep cards and the gallery fast.
Prints the lines to paste into an entry.
"""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

MEDIA = Path(__file__).resolve().parent.parent / "media"
THUMB_W = 720


def run(args):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args], check=True)


def thumb(src_img, name):
    out = MEDIA / f"{name}.thumb.jpg"
    run(["-i", str(src_img), "-vf", f"scale='min({THUMB_W},iw)':-2", "-q:v", "4", str(out)])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kind", choices=["clip", "image", "still"])
    ap.add_argument("input")
    ap.add_argument("--name", required=True, help="output name without extension (lowercase-with-dashes)")
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--seconds", type=float, default=8.0)
    ap.add_argument("--at", type=float, default=1.0, help="for still: the moment to grab, in seconds")
    ap.add_argument("--width", type=int)
    ap.add_argument("--crf", type=int, default=26, help="higher = smaller file")
    ap.add_argument("--keep-audio", action="store_true", help="keep the sound (for Sound posts); clips are muted otherwise")
    a = ap.parse_args()
    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg not found on PATH.")
    MEDIA.mkdir(parents=True, exist_ok=True)

    if a.kind == "clip":
        w = a.width or 1280
        out = MEDIA / f"{a.name}.mp4"
        audio = ["-c:a", "aac", "-b:a", "128k"] if a.keep_audio else ["-an"]
        run(["-ss", str(a.start), "-t", str(a.seconds), "-i", a.input, *audio,
             "-vf", f"scale='min({w},iw)':-2,fps=30", "-c:v", "libx264", "-preset", "slow",
             "-crf", str(a.crf), "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)])
        poster = MEDIA / f"{a.name}.jpg"
        run(["-ss", str(a.start + min(1.0, a.seconds / 2)), "-i", a.input, "-frames:v", "1",
             "-vf", f"scale='min({w},iw)':-2", "-q:v", "3", str(poster)])
        thumb(poster, a.name)
        print(f"{out.name}: {out.stat().st_size / 1e6:.1f} MB (+ poster and thumbnail)")
        print(f'Paste:   @video media/{out.name} "What this shows"')
        print(f"Cover:   cover: media/{out.name}")
    elif a.kind == "image":
        w = a.width or 1920
        out = MEDIA / f"{a.name}.jpg"
        run(["-i", a.input, "-vf", f"scale='min({w},iw)':-2", "-q:v", "3", str(out)])
        thumb(out, a.name)
        print(f"{out.name}: {out.stat().st_size / 1e3:.0f} KB (+ thumbnail)")
        print(f"Paste:   ![What this shows](media/{out.name})")
        print(f'Gallery: media/{out.name} "Caption"   (one per line under @gallery)')
    else:
        w = a.width or 1920
        out = MEDIA / f"{a.name}.jpg"
        run(["-ss", str(a.at), "-i", a.input, "-frames:v", "1", "-vf", f"scale='min({w},iw)':-2", "-q:v", "3", str(out)])
        thumb(out, a.name)
        print(f"{out.name}: {out.stat().st_size / 1e3:.0f} KB (+ thumbnail)")
        print(f"Paste:   ![What this shows](media/{out.name})")
    print("Before/after: @compare media/before.jpg media/after.jpg \"Caption\"")


if __name__ == "__main__":
    main()
