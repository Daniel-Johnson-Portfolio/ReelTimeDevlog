"""Build the devlog site.

  python build.py                    # approved posts -> docs/  (the folder you commit and host)
  python build.py --drafts           # drafts too    -> preview/ (local only, never committed)
  python build.py --serve            # build docs/, open it at http://localhost:8000, rebuild on changes
  python build.py --drafts --serve   # the same for the preview

Run from anywhere (python devlog/build.py works from the project root). You can also open
docs/index.html or preview/index.html straight from the folder.

The site: home, one page per post, topic pages, a timeline by day, a gallery of every shot and
clip, a page per crew session, search, and standing pages from pages/.

Writing entries (entries/*.md, front matter then markdown):
  categories: [gameplay, crew]       first one is the main topic; slugs from config.json
  sessions: [gameplay, engine]       crew sessions involved
  cover: media/clip.mp4              the post's hero (a clip or a still)
  featured: true                     pin to the home page's big screen (optional)

Special lines in the markdown body:
  @video media/clip.mp4 "Caption"                     a looping clip
  @film media/trailer.mp4 "Caption"                  a film with sound that plays only on click (big files)
  @compare media/before.jpg media/after.jpg "Caption"  a before/after slider
  @gallery                                           a grid of shots, one per line after it:
  media/a.jpg "Caption"
  @crew                                              the live crew table (data/crew.json)
  @play                                              "play in your browser", if links.play_web is set
  @builds                                            every browser build in data/web_builds.json, oldest first,
                                                     each loading only on click (files in play/<id>/, copied to docs/play/)
Plain markdown images ![caption](media/shot.jpg) become captioned figures that open full size.

media/ is the local working folder (tools/media.py writes there, not committed). The build copies
only the files approved posts use into docs/media/, so drafts never leak into the published site.
Uses the 'markdown' package if installed (pip install markdown), otherwise a built-in converter.
"""
import argparse
import html
import json
import re
import shutil
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
MEDIA = HERE / "media"
DOCS = HERE / "docs"
PREVIEW = HERE / "preview"
FRONT = re.compile(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*\r?\n?", re.S)
MEDIA_REF = re.compile(r"media/[^\s\"'()<>]+")
VIDEO_EXT = (".mp4", ".webm")
esc = html.escape


# ---------- reading ----------

def parse_front(text):
    m = FRONT.match(text)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        k, v = line.split(":", 1)
        v = v.strip()
        if v.startswith("[") and v.endswith("]"):
            meta[k.strip()] = [x.strip().strip("\"'") for x in v[1:-1].split(",") if x.strip()]
        else:
            meta[k.strip()] = v.strip("\"'")
    return meta, text[m.end():]


def parse_time(value):
    try:
        dt = datetime.fromisoformat(str(value).strip())
    except (TypeError, ValueError):
        return None
    return dt if dt.tzinfo else dt.astimezone()


def as_list(value):
    if isinstance(value, list):
        return value
    return [v.strip() for v in str(value or "").split(",") if v.strip()]


def is_true(value):
    return str(value).strip().lower() in ("true", "yes", "1")


# ---------- media ----------

def is_video(src):
    return src.lower().endswith(VIDEO_EXT)


def media_exists(name):
    return (MEDIA / name).exists() or (DOCS / "media" / name).exists()


def poster_for(src):
    """media/x.mp4 -> media/x.jpg if media.py made a poster for it."""
    if not src.startswith("media/") or not is_video(src):
        return ""
    jpg = Path(src[6:]).with_suffix(".jpg").as_posix()
    return f"media/{jpg}" if media_exists(jpg) else ""


def thumb_for(src):
    """A small image for cards and grids: x.thumb.jpg if media.py made one, else the poster or the image."""
    if not src or not src.startswith("media/"):
        return ""
    name = src[6:]
    stem = Path(name).with_suffix("").as_posix()
    for cand in (f"{stem}.thumb.jpg", f"{stem}.jpg" if is_video(src) else name):
        if media_exists(cand):
            return f"media/{cand}"
    return ""


# ---------- markdown ----------

BULLET = re.compile(r"^\s*[-*]\s+")
NUMBERED = re.compile(r"^\s*\d+\.\s+")
FILM = re.compile(r'^@film\s+(\S+)(?:\s+"([^"]*)")?\s*$', re.M)
VIDEO = re.compile(r'^@video\s+(\S+)(?:\s+"([^"]*)")?\s*$', re.M)
COMPARE = re.compile(r'^@compare\s+(\S+)\s+(\S+)(?:\s+"([^"]*)")?\s*$', re.M)
GALLERY = re.compile(r'^@gallery[ \t]*\n((?:[ \t]*media/\S+(?:[ \t]+"[^"]*")?[ \t]*(?:\n|$))+)', re.M)
GALLERY_ITEM = re.compile(r'^[ \t]*(media/\S+)(?:[ \t]+"([^"]*)")?', re.M)
CREW_LINE = re.compile(r"^@crew\s*$", re.M)
PLAY_LINE = re.compile(r"^@play\s*$", re.M)
BUILDS_LINE = re.compile(r"^@builds\s*$", re.M)
PLAY = {"url": "", "embed": ""}  # set from config.json links by Site


def play_block():
    """The 'play it in your browser' panel, if a web build is linked in config.json (links.play_web)."""
    if not PLAY["url"] and not PLAY["embed"]:
        return ""
    label = "Play on itch.io" if "itch.io" in PLAY["url"] else "Play now"
    actions = f'<a class="play-btn" href="{esc(PLAY["url"])}">{label}</a>' if PLAY["url"] else ""
    embed = (f'<div class="play-embed" data-src="{esc(PLAY["embed"])}"><button type="button" class="play-load">'
             f'Load the game on this page</button></div>') if PLAY["embed"] else ""
    return ('<figure class="play-panel"><div class="play-inner"><p class="play-title">Play it in your browser</p>'
            '<p class="play-note">An experimental web build: best in Chrome or Edge, and a big download. '
            'The Windows build is the full game.</p>'
            f'<div class="play-actions">{actions}</div>{embed}</div></figure>')
def web_builds():
    f = HERE / "data" / "web_builds.json"
    if not f.exists():
        return []
    return sorted(json.loads(f.read_text(encoding="utf-8")), key=lambda b: b.get("date", ""))


def submitted_info():
    """data/submitted.json: {"time": ISO with offset, "build": "short text"}. Empty time = not submitted yet."""
    f = HERE / "data" / "submitted.json"
    if not f.exists():
        return None
    d = json.loads(f.read_text(encoding="utf-8"))
    if not d.get("time"):
        return None
    d["dt"] = datetime.fromisoformat(d["time"])
    return d


def builds_block():
    """One card per browser build, oldest first. Nothing loads until the reader clicks."""
    builds = web_builds()
    if not builds:
        return ('<figure class="play-panel"><div class="play-inner"><p class="play-title">Browser builds</p>'
                '<p class="play-note">None yet. The first one is being made and will appear here.</p></div></figure>')
    cards = []
    for i, b in enumerate(builds, 1):
        meta = " &middot; ".join(esc(x) for x in (b.get("when", ""), b.get("commit", ""), b.get("size", "")) if x)
        src = b.get("url") or f'play/{b["id"]}/{b.get("entry", "index.html")}'
        if b.get("pending"):
            action = f'<p class="play-note">{esc(b.get("pending_note", "Not online yet: it goes up once it has been checked in a real browser."))}</p>'
        else:
            action = (f'<div class="play-actions"><a class="play-btn" href="{esc(src)}" target="_blank" rel="noopener">'
                      f'Play build {i} in a new tab ({esc(b.get("download", b.get("size", "")))})</a></div>')
        cards.append(
            f'<figure class="play-panel build-card" id="build-{esc(b["id"])}"><div class="play-inner">'
            f'<p class="play-title">Build {i}: {esc(b.get("title", b["id"]))}</p>'
            f'<p class="play-note">{meta}</p><p class="build-desc">{esc(b.get("description", ""))}</p>{action}</div></figure>')
    return "\n".join(cards)


IMG_MD = re.compile(r"!\[([^\]]*)\]\((media/[^)\s]+)\)")
IMG_PARA = re.compile(r"<p>\s*(<img\b[^>]*>)\s*</p>")
ATTR = re.compile(r'(\w[\w-]*)="([^"]*)"')


def inline(text):
    codes = []

    def keep(m):
        codes.append(f"<code>{esc(m.group(1))}</code>")
        return f"\x00{len(codes) - 1}\x00"

    text = re.sub(r"`([^`]+)`", keep, text)
    text = esc(text, quote=False)
    text = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", r'<img src="\2" alt="\1" loading="lazy">', text)
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?!\w)", r"<em>\1</em>", text)
    return re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], text)


def mini_markdown(md):
    out, lines, i = [], md.splitlines(), 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("```"):
            i += 1
            code = []
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(lines[i])
                i += 1
            out.append(f"<pre><code>{esc(chr(10).join(code))}</code></pre>")
            i += 1
            continue
        block = []
        while i < len(lines) and lines[i].strip() and not lines[i].startswith("```"):
            block.append(lines[i])
            i += 1
        first = block[0]
        heading = re.match(r"(#{1,6})\s+(.*)", first)
        if first.lstrip().startswith("<"):
            out.append("\n".join(block))
        elif heading:
            level = len(heading.group(1))
            out.append(f"<h{level}>{inline(heading.group(2))}</h{level}>")
            if block[1:]:
                out.append(f"<p>{inline(' '.join(block[1:]))}</p>")
        elif all(BULLET.match(b) for b in block):
            out.append("<ul>" + "".join("<li>" + inline(BULLET.sub("", b)) + "</li>" for b in block) + "</ul>")
        elif all(NUMBERED.match(b) for b in block):
            out.append("<ol>" + "".join("<li>" + inline(NUMBERED.sub("", b)) + "</li>" for b in block) + "</ol>")
        elif all(b.startswith(">") for b in block):
            out.append(f"<blockquote><p>{inline(' '.join(b.lstrip('> ') for b in block))}</p></blockquote>")
        else:
            out.append(f"<p>{inline(' '.join(block))}</p>")
    return "\n".join(out)


def video_tag(src, attrs='autoplay muted loop playsinline controls preload="metadata"'):
    poster = poster_for(src)
    poster_attr = f' poster="{esc(poster)}"' if poster else ""
    return f'<video src="{esc(src)}"{poster_attr} {attrs}></video>'


def lightbox_link(src, caption, inner):
    return f'<a href="{esc(src)}" data-lightbox data-caption="{esc(caption)}">{inner}</a>'


def expand_directives(md, names, collected):
    """Turn @video, @compare, @gallery and @crew lines into HTML, and collect every piece of media."""
    def video(m):
        src, cap = m.group(1), m.group(2) or ""
        collected.append({"src": src, "caption": cap})
        figcap = f"<figcaption>{esc(cap)}</figcaption>" if cap else ""
        return f'\n<figure class="clip">{video_tag(src)}{figcap}</figure>\n'

    def compare(m):
        a, b, cap = m.group(1), m.group(2), m.group(3) or ""
        collected.append({"src": a, "caption": f"Before: {cap}" if cap else "Before"})
        collected.append({"src": b, "caption": f"After: {cap}" if cap else "After"})
        figcap = f"<figcaption>{esc(cap)}</figcaption>" if cap else ""
        return ('\n<figure class="compare" style="--pos:50%"><div class="compare-frame">'
                f'<img class="compare-before" src="{esc(a)}" alt="Before{": " + esc(cap) if cap else ""}">'
                f'<img class="compare-after" src="{esc(b)}" alt="After{": " + esc(cap) if cap else ""}">'
                '<span class="compare-tag compare-tag-before">Before</span><span class="compare-tag compare-tag-after">After</span>'
                '</div><input type="range" min="0" max="100" value="50" aria-label="Drag to compare before and after">'
                f"{figcap}</figure>\n")

    def gallery(m):
        items = []
        for g in GALLERY_ITEM.finditer(m.group(1)):
            src, cap = g.group(1), g.group(2) or ""
            collected.append({"src": src, "caption": cap})
            thumb = thumb_for(src) or (src if not is_video(src) else "")
            img = f'<img src="{esc(thumb)}" alt="{esc(cap)}" loading="lazy">' if thumb else video_tag(src, 'muted preload="metadata"')
            badge = '<span class="play" aria-hidden="true"></span>' if is_video(src) else ""
            figcap = f'<span class="pg-cap">{esc(cap)}</span>' if cap else ""
            items.append(f"<li>{lightbox_link(src, cap, img + badge)}{figcap}</li>")
        return f'\n<figure class="post-gallery"><ul>{"".join(items)}</ul></figure>\n'

    md = CREW_LINE.sub(lambda m: "\n" + crew_block(names, link=True) + "\n", md)
    md = COST_LINE.sub(lambda m: "\n" + cost_block() + "\n", md)
    md = PLAY_LINE.sub(lambda m: "\n" + play_block() + "\n", md)
    md = BUILDS_LINE.sub(lambda m: "\n" + builds_block() + "\n", md)
    def film(m):
        src, cap = m.group(1), m.group(2) or ""
        collected.append({"src": src, "caption": cap})
        figcap = f"<figcaption>{esc(cap)}</figcaption>" if cap else ""
        tag = video_tag(src, 'controls playsinline preload="none"')
        return "\n" + f'<figure class="clip film">{tag}{figcap}</figure>' + "\n"

    md = FILM.sub(film, md)
    md = VIDEO.sub(video, md)
    md = COMPARE.sub(compare, md)
    md = GALLERY.sub(gallery, md)
    for alt, src in IMG_MD.findall(md):
        collected.append({"src": src, "caption": alt})
    return md


def figure_images(body):
    """Standalone images become captioned figures that open full size."""
    def rep(m):
        attrs = dict(ATTR.findall(m.group(1)))
        src, alt = attrs.get("src", ""), html.unescape(attrs.get("alt", ""))
        img = f'<img src="{esc(src)}" alt="{esc(alt)}" loading="lazy">'
        cap = f"<figcaption>{esc(alt)}</figcaption>" if alt else ""
        return f'<figure class="shot">{lightbox_link(src, alt, img)}{cap}</figure>'
    return IMG_PARA.sub(rep, body)


def to_html(md, names, collected):
    md = expand_directives(md, names, collected)
    try:
        import markdown
        body = markdown.markdown(md, extensions=["fenced_code", "tables"])
    except ImportError:
        body = mini_markdown(md)
    return figure_images(body)


def with_media_prefix(text, prefix):
    return re.sub(r'(src|href|poster)="media/', lambda m: f'{m.group(1)}="{prefix}', text)


def plain_text(body_html):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", body_html))).strip()


# ---------- cost panel ----------

COST_LINE = re.compile(r"^@cost\s*$", re.M)


def usd(v):
    return f"${v:,.0f}"


def cost_figures():
    """Measured (data/usage.json) plus the hand-made band for the hours before the ledger (data/usage_estimate.json)."""
    mp, ep = HERE / "data" / "usage.json", HERE / "data" / "usage_estimate.json"
    if not mp.exists():
        return None
    m = json.loads(mp.read_text(encoding="utf-8"))
    e = json.loads(ep.read_text(encoding="utf-8")) if ep.exists() else {"low": 0, "mid": 0, "high": 0}
    return m, e


def cost_block():
    figs = cost_figures()
    if not figs:
        return '<p class="note">Cost figures appear here once tools/usage_snapshot.py has run.</p>'
    m, e = figs
    total = {k: m["measured_usd"] + e.get(k, 0) for k in ("low", "mid", "high")}
    as_of = m["as_of"][:16].replace("T", " ")
    models = "".join(f"<tr><td>{esc(k)}</td><td>{usd(v)}</td></tr>" for k, v in m["by_model"].items())
    roles = "".join(f"<tr><td>{esc(k)}</td><td>{usd(v)}</td></tr>" for k, v in list(m["by_role"].items())[:8])
    return ('<figure class="crew-table cost-panel"><table>'
            f'<caption>At API prices, as of {esc(as_of)} UTC. Measured: {usd(m["measured_usd"])} over {m["sessions"]} sessions. '
            f'With the estimate for the hours before the ledger: {usd(total["low"])} to {usd(total["high"])}, '
            f'most likely about {usd(total["mid"])}.</caption>'
            f'<thead><tr><th>Model (measured)</th><th>Cost</th></tr></thead><tbody>{models}</tbody></table>'
            f'<table><thead><tr><th>Session (measured)</th><th>Cost</th></tr></thead><tbody>{roles}</tbody></table>'
            '<figcaption>Updated every time the devlog publishes. The crew runs on a subscription; nothing here was billed per token.</figcaption>'
            '</figure>')


# ---------- crew table ----------

def crew_block(names, root="", link=False):
    path = HERE / "data" / "crew.json"
    if not path.exists():
        return '<p class="note">Crew stats appear here once tools/crew_snapshot.py has run.</p>'
    data = json.loads(path.read_text(encoding="utf-8"))
    t = data.get("totals", {})

    def n(key, one, many):
        v = t.get(key, 0)
        return f"{v} {one if v == 1 else many}"

    rows = []
    for r in data.get("crew", []):
        role = r["role"]
        name = esc(names.get(role, role))
        label = f'<a href="crew/{esc(role)}.html">{name}</a>' if link else name
        rows.append(f'<tr><th scope="row"><span class="dot crew-{esc(role)}"></span>{label}</th>'
                    f'<td>{esc(r.get("about", ""))}</td><td class="num">{r.get("tasks_done", 0)}</td>'
                    f'<td class="num">{r.get("commits", 0)}</td></tr>')
    when = parse_time(data.get("generated"))
    stamp = f" Updated {when.strftime('%a %d %b, %H:%M')}." if when else ""
    summary = (f'{n("tasks_done", "task", "tasks")} done, {n("kits_run", "kit", "kits")} run by the engine, '
               f'{n("commits", "commit", "commits")}, {n("decisions", "decision", "decisions")} '
               f'({t.get("assumptions", 0)} made as assumptions), {n("friction_fixed", "tool problem", "tool problems")} fixed.')
    return (f'<figure class="crew-table"><p class="crew-summary">{esc(summary)}{esc(stamp)}</p>'
            f'<div class="table-wrap"><table><thead><tr><th scope="col">Session</th><th scope="col">What it does</th>'
            f'<th scope="col" class="num">Tasks done</th><th scope="col" class="num">Commits</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table></div></figure>')


# ---------- site model ----------

class Site:
    def __init__(self, drafts):
        self.drafts = drafts
        self.out = PREVIEW if drafts else DOCS
        self.cfg = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
        self.names = self.cfg.get("crew", {})
        self.cats = {c["slug"]: c for c in self.cfg.get("categories", [])}
        links = self.cfg.get("links", {})
        PLAY.update({"url": links.get("play_web", ""), "embed": links.get("play_web_embed", "")})
        self.start = parse_time(self.cfg.get("sprint_start"))
        self.hours = int(self.cfg.get("sprint_hours", 93))
        self.days = max(1, -(-self.hours // 24))
        self.tpl = (HERE / "template" / "base.html").read_text(encoding="utf-8")
        self.refs, self.warnings = set(), []
        self.entries = self.load("entries")
        self.pages = self.load("pages")
        self.entries.sort(key=lambda e: e["date"], reverse=True)
        self.pages.sort(key=lambda p: (int(p["meta"].get("order", 50)) if str(p["meta"].get("order", "")).isdigit() else 50, p["slug"]))
        self.page_slugs = {p["slug"] for p in self.pages}
        self.gallery = []
        seen = set()
        for e in self.entries:
            for item in e["media"]:
                if item["src"] not in seen:
                    seen.add(item["src"])
                    self.gallery.append({**item, "entry": e})

    def media_prefix(self, root):
        return root + ("../media/" if self.drafts else "media/")

    def load(self, folder):
        items = []
        d = HERE / folder
        for p in sorted(d.glob("*.md")) if d.exists() else []:
            meta, body = parse_front(p.read_text(encoding="utf-8"))
            draft = str(meta.get("draft", "true")).lower() != "false"
            if draft and not self.drafts:
                continue
            item = {"slug": p.stem, "meta": meta, "draft": draft, "title": meta.get("title", p.stem),
                    "summary": meta.get("summary", ""), "media": []}
            item["html"] = to_html(body, self.names, item["media"])
            self.refs.update(MEDIA_REF.findall(body))
            if folder == "entries":
                self.prepare_entry(item, p)
            items.append(item)
        return items

    def prepare_entry(self, e, path):
        m = e["meta"]
        e["date"] = parse_time(m.get("date")) or datetime.fromtimestamp(path.stat().st_mtime).astimezone()
        e["categories"] = as_list(m.get("categories"))
        e["sessions"] = as_list(m.get("sessions"))
        e["featured"] = is_true(m.get("featured"))
        e["cover"] = m.get("cover", "")
        if e["cover"].startswith("media/"):
            self.refs.add(e["cover"])
            if not any(x["src"] == e["cover"] for x in e["media"]):
                e["media"].insert(0, {"src": e["cover"], "caption": e["summary"] or e["title"]})
        e["hour"], e["day"], e["day_num"] = self.when(e["date"])
        thumb_src = e["cover"] or next((x["src"] for x in e["media"]), "")
        e["thumb"] = thumb_for(thumb_src)
        e["thumb_video"] = thumb_src if (not e["thumb"] and thumb_src and is_video(thumb_src)) else ""
        for x in e["media"]:
            for extra in (thumb_for(x["src"]), poster_for(x["src"])):
                if extra:
                    self.refs.add(extra)
        if not e["categories"]:
            self.warnings.append(f"{e['slug']}: no categories")
        for c in e["categories"]:
            if c not in self.cats:
                self.warnings.append(f"{e['slug']}: unknown category '{c}' (see categories in config.json)")
        if not e["cover"]:
            self.warnings.append(f"{e['slug']}: no cover (every post should lead with a clip or a shot)")
        for x in e["media"]:
            if not x["caption"]:
                self.warnings.append(f"{e['slug']}: {x['src']} has no caption")

    def when(self, dt):
        if not self.start:
            return "", "", 1
        h = (dt - self.start).total_seconds() / 3600
        if h < 0:
            return "Before", "Before the jam", 0
        if h >= self.hours:
            return "After", "After the jam", self.days + 1
        hour = int(h) + 1
        return f"Hour {hour}", f"Day {(hour - 1) // 24 + 1}", (hour - 1) // 24 + 1

    def day_title(self, n):
        if n == 0:
            return "Before the jam"
        if n > self.days:
            return "After the jam"
        date = (self.start + timedelta(hours=24 * (n - 1))) if self.start else None
        return f"Day {n}" + (f", {date.strftime('%a')} {date.day} {date.strftime('%b')}" if date else "")

    def current_hour(self):
        if not self.start or not self.entries:
            return 0
        latest = max(e["date"] for e in self.entries)
        return max(0, min(self.hours, int((latest - self.start).total_seconds() // 3600) + 1))

    # ---------- pieces ----------

    def chip(self, slug, root, link=True):
        c = self.cats.get(slug, {"name": slug, "color": "#8a96a3"})
        inner = f'<span class="dot" style="--c:{esc(c.get("color", "#8a96a3"))}"></span>{esc(c["name"])}'
        if link and slug in self.cats:
            return f'<a class="chip" href="{root}topics/{esc(slug)}.html">{inner}</a>'
        return f'<span class="chip">{inner}</span>'

    def chips(self, cats, root, link=True):
        if not cats:
            return ""
        return '<ul class="chips">' + "".join(f"<li>{self.chip(c, root, link)}</li>" for c in cats) + "</ul>"

    def crew_list(self, sessions, root):
        if not sessions:
            return ""
        items = "".join(f'<li><a href="{root}crew/{esc(s)}.html"><span class="dot crew-{esc(s)}"></span>'
                        f'{esc(self.names.get(s, s))}</a></li>' for s in sessions)
        return f'<ul class="crew" aria-label="Crew sessions involved">{items}</ul>'

    def when_short(self, e):
        if e["day_num"] == 0:
            return "Before the jam"
        if e["day_num"] > self.days:
            return "After the jam"
        return f'{e["day"]}, {e["hour"].lower()}'

    def when_html(self, e):
        return f'<p class="when"><span class="hour">{e["hour"]}</span><span class="day">{e["day"]}</span></p>'

    def thumb_html(self, e, root):
        mp = self.media_prefix(root)
        if e["thumb"]:
            return f'<img src="{esc(mp + e["thumb"][6:])}" alt="" loading="lazy">'
        if e["thumb_video"]:
            return f'<video src="{esc(mp + e["thumb_video"][6:])}" muted preload="metadata"></video>'
        return '<span class="no-media">No shot yet</span>'

    def card(self, e, root):
        has_video = any(is_video(x["src"]) for x in e["media"][:1]) or is_video(e["cover"])
        badge = '<span class="play" aria-hidden="true"></span>' if has_video else ""
        title = esc(e["title"]) + (' <span class="draft">draft</span>' if e["draft"] else "")
        main_cat = self.chip(e["categories"][0], root) if e["categories"] else ""
        return (f'<article class="card"><a class="card-media" href="{root}posts/{e["slug"]}.html" tabindex="-1" aria-hidden="true">'
                f'{self.thumb_html(e, root)}{badge}</a><div class="card-body">'
                f'<div class="card-meta">{main_cat}<span class="card-when">{self.when_short(e)}</span></div>'
                f'<h3><a href="{root}posts/{e["slug"]}.html">{title}</a></h3>'
                f'<p class="summary">{esc(e["summary"])}</p></div></article>')

    def cards(self, entries, root, empty="No posts here yet."):
        if not entries:
            return f'<p class="empty">{esc(empty)}</p>'
        return '<div class="cards">' + "".join(self.card(e, root) for e in entries) + "</div>"

    def ruler(self, current, compact=False):
        blocks = []
        for d in range(self.days):
            ticks = "".join(f'<li{" class=on" if d * 24 + t + 1 <= current else ""} style="--i:{d * 24 + t + 1}"></li>'
                            for t in range(min(24, self.hours - d * 24)))
            blocks.append(f'<div class="ruler-day"><ol class="ticks" aria-hidden="true">{ticks}</ol>'
                          f'<span class="ruler-label">Day {d + 1}</span></div>')
        if current <= 0:
            caption = f"Starts {self.start.day} {self.start.strftime('%B')}" if self.start else "Not started"
        elif current >= self.hours:
            caption = f"Finished: all {self.hours} hours"
        else:
            caption = f"Hour {current} of {self.hours}"
        cls = "ruler compact" if compact else "ruler"
        sub = submitted_info()
        sub_html = ""
        if sub and self.start:
            sh = int((sub["dt"] - self.start).total_seconds() // 3600) + 1
            if 1 <= sh <= self.hours:
                blocks_html = "".join(blocks).replace(f'style="--i:{sh}"></li>', f'style="--i:{sh}" class="submitted"></li>', 1)
                blocks = [blocks_html]
            sub_html = (f'<p class="ruler-submitted"><span class="sub-dot" aria-hidden="true"></span>'
                        f'Submitted {esc(sub["dt"].strftime("%a %H:%M"))} UK, hour {sh}'
                        + (f' &middot; {esc(sub["build"])}' if sub.get("build") else "") + '</p>')
        return (f'<figure class="{cls}" aria-label="{esc(caption)}"><div class="ruler-days" style="--days:{self.days}">'
                f'{"".join(blocks)}</div><figcaption>{esc(caption)}</figcaption>{sub_html}</figure>')

    def header(self, root, active):
        links = []
        if "the-game" in self.page_slugs:
            links.append(("the-game", "The game"))
        if "play" in self.page_slugs:
            links.append(("play", "Play In Browser"))
        links += [("topics", "Topics"), ("timeline", "Timeline"), ("gallery", "Gallery")]
        if "how-its-built" in self.page_slugs:
            links.append(("how-its-built", "How it's built"))
        items = "".join(f'<li><a href="{root}{slug}.html"{" aria-current=page" if slug == active else ""}>{label}</a></li>'
                        for slug, label in links)
        return (f'<header class="site-head"><div class="wrap head-inner">'
                f'<a class="brand" href="{root}index.html">{esc(self.cfg["site_title"])}</a>'
                f'<nav class="site-nav" aria-label="Main"><ul>{items}</ul></nav>'
                f'<form class="site-search" action="{root}search.html" role="search">'
                f'<label class="sr-only" for="q-top">Search the devlog</label>'
                f'<input id="q-top" name="q" type="search" placeholder="Search posts"></form>'
                f"</div></header>")

    def footer(self, root):
        pages = "".join(f'<li><a href="{root}{p["slug"]}.html">{esc(p["title"])}</a></li>' for p in self.pages)
        links = self.cfg.get("links", {})
        itch = f'<li><a href="{esc(links["itch"])}">Play it on itch.io</a></li>' if links.get("itch") else ""
        return (f'<footer class="site-foot"><div class="wrap foot-inner"><ul class="foot-links">'
                f'<li><a href="{root}index.html">Home</a></li><li><a href="{root}topics.html">Topics</a></li>'
                f'<li><a href="{root}timeline.html">Timeline</a></li><li><a href="{root}gallery.html">Gallery</a></li>'
                f'<li><a href="{root}search.html">Search</a></li>{pages}{itch}</ul>'
                f'<p>{esc(self.cfg.get("footer", ""))}</p></div></footer>')

    def page(self, rel, title, description, content, active="", body_class=""):
        root = "../" * rel.count("/")
        full_title = esc(self.cfg["site_title"]) if rel == "index.html" else f"{esc(title)} | {esc(self.cfg['site_title'])}"
        text = (self.tpl.replace("{{page_title}}", full_title).replace("{{description}}", esc(description))
                .replace("{{accent}}", esc(self.cfg.get("accent", "#f2b705"))).replace("{{body_class}}", body_class)
                .replace("{{header}}", self.header(root, active)).replace("{{footer}}", self.footer(root))
                .replace("{{content}}", content).replace("{{root}}", root))
        path = self.out / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def by_category(self, slug):
        return [e for e in self.entries if slug in e["categories"]]

    def by_session(self, role):
        return [e for e in self.entries if role in e["sessions"]]

    # ---------- pages ----------

    def build_home(self):
        root, mp = "", self.media_prefix("")
        featured = next((e for e in self.entries if e["featured"]), None) or \
            next((e for e in self.entries if is_video(e["cover"])), None) or (self.entries[0] if self.entries else None)
        start_links = []
        if PLAY["url"]:
            start_links.append((PLAY["url"], "Play it now", "In your browser: no download needed"))
        if "the-game" in self.page_slugs:
            start_links.append(("the-game.html", "The game", "What it is, how it plays, where to get it"))
        if "how-its-built" in self.page_slugs:
            start_links.append(("how-its-built.html", "How it's built", "The crew of Claude sessions and how they work"))
        figs, cost_post = cost_figures(), self.cfg.get("links", {}).get("cost_post", "")
        if figs and cost_post:
            mid = figs[0]["measured_usd"] + figs[1].get("mid", 0)
            start_links.append((f"posts/{cost_post}.html", "What it costs", f"About {usd(mid)} at API prices so far"))
        start_links += [("timeline.html", "Timeline", "Every post, hour by hour"),
                        ("gallery.html", "Gallery", f"{len(self.gallery)} shots and clips from the build")]
        start = "".join(f'<li><a href="{u}"><span class="start-title">{t}</span><span class="start-desc">{esc(d)}</span></a></li>'
                        for u, t, d in start_links)
        out = [f'<section class="masthead wrap"><h1 class="site-title">{esc(self.cfg["site_title"])}</h1>'
               f'<p class="tagline">{esc(self.cfg.get("tagline", ""))}</p>{self.ruler(self.current_hour())}'
               f'<ul class="start">{start}</ul></section>']

        if featured:
            f = featured
            cover = f["cover"] or (f["media"][0]["src"] if f["media"] else "")
            if cover and is_video(cover):
                media = with_media_prefix(video_tag(cover, 'autoplay muted loop playsinline preload="metadata"'), mp)
            elif cover:
                media = f'<img src="{esc(mp + cover[6:])}" alt="{esc(f["summary"])}">'
            else:
                media = ""
            hero_film = self.cfg.get("hero_film", "")
            if hero_film:
                # a film with sound in the home page's big slot: plays only on click, so it isn't wrapped in a link
                film = with_media_prefix(video_tag(hero_film, 'controls playsinline preload="none"'), mp)
                media_html = f'<div class="featured-media">{film}</div>'
            else:
                media_html = f'<a class="featured-media" href="posts/{f["slug"]}.html" tabindex="-1" aria-hidden="true">{media}</a>'
            out.append(f'<section class="screen featured" aria-label="Latest from the build"><div class="wrap featured-inner">'
                       f'{media_html}'
                       f'<div class="featured-text">{self.chips(f["categories"], root)}'
                       f'<h2><a href="posts/{f["slug"]}.html">{esc(f["title"])}</a></h2>'
                       f'<p>{esc(f["summary"])}</p>{self.when_html(f)}{self.crew_list(f["sessions"], root)}</div></div></section>')

        tiles = []
        for slug, c in self.cats.items():
            posts = self.by_category(slug)
            if not posts:
                continue
            thumb = next((p for p in posts if p["thumb"]), None)
            img = f'<img src="{esc(mp + thumb["thumb"][6:])}" alt="" loading="lazy">' if thumb else '<span class="no-media"></span>'
            tiles.append(f'<li class="tile" style="--c:{esc(c.get("color", "#8a96a3"))}"><a href="topics/{slug}.html">'
                         f'<span class="tile-media">{img}</span><span class="tile-name">{esc(c["name"])}</span>'
                         f'<span class="tile-count">{len(posts)} {"post" if len(posts) == 1 else "posts"}</span>'
                         f'<span class="tile-desc">{esc(c.get("description", ""))}</span></a></li>')
        if tiles:
            out.append(f'<section class="block wrap"><div class="block-head"><h2>Browse by topic</h2>'
                       f'<a href="topics.html">All topics</a></div><ul class="tiles">{"".join(tiles)}</ul></section>')

        rest = [e for e in self.entries if e is not featured][:9]
        out.append(f'<section class="block wrap"><div class="block-head"><h2>Latest posts</h2>'
                   f'<a href="timeline.html">Every post, by day</a></div>'
                   f'{self.cards(rest, root, "The first post goes up when the clock starts.")}</section>')

        if self.gallery:
            items = "".join(self.gallery_item(g, root) for g in self.gallery[:8])
            out.append(f'<section class="block wrap"><div class="block-head"><h2>From the build</h2>'
                       f'<a href="gallery.html">Open the gallery</a></div><ul class="strip">{items}</ul></section>')
        self.page("index.html", self.cfg["site_title"], self.cfg.get("tagline", ""), "".join(out), "home", "home")

    def gallery_item(self, g, root, with_post=False):
        mp = self.media_prefix(root)
        src = g["src"]
        thumb = thumb_for(src) or ("" if is_video(src) else src)
        inner = (f'<img src="{esc(mp + thumb[6:])}" alt="{esc(g["caption"])}" loading="lazy">' if thumb
                 else f'<video src="{esc(mp + src[6:])}" muted preload="metadata"></video>')
        badge = '<span class="play" aria-hidden="true"></span>' if is_video(src) else ""
        e = g["entry"]
        post_url = f'{root}posts/{e["slug"]}.html'
        link = (f'<a href="{esc(mp + src[6:])}" data-lightbox data-caption="{esc(g["caption"])}" data-post="{post_url}">'
                f"{inner}{badge}</a>")
        cats = " ".join(e["categories"])
        cap = ""
        if with_post:
            cap = (f'<p class="g-cap">{esc(g["caption"])}</p>'
                   f'<p class="g-from"><a href="{post_url}">{esc(e["title"])}</a> <span>{self.when_short(e)}</span></p>')
        return f'<li data-cats="{esc(cats)}">{link}{cap}</li>'

    def build_posts(self):
        chrono = sorted(self.entries, key=lambda e: e["date"])
        for i, e in enumerate(chrono):
            root = "../"
            mp = self.media_prefix(root)
            cover = e["cover"]
            hero = ""
            if cover.startswith("media/"):
                if is_video(cover):
                    tag = with_media_prefix(video_tag(cover), mp)
                else:
                    tag = lightbox_link(mp + cover[6:], e["summary"], f'<img src="{esc(mp + cover[6:])}" alt="{esc(e["summary"])}">')
                hero = f'<div class="screen post-hero"><div class="wrap hero-inner">{tag}</div></div>'
            body = with_media_prefix(e["html"], mp).replace('href="crew/', 'href="../crew/')
            date_text = e["date"].strftime("%H:%M")
            prev_e = chrono[i - 1] if i > 0 else None
            next_e = chrono[i + 1] if i + 1 < len(chrono) else None
            nav = '<nav class="post-nav wrap" aria-label="More posts">'
            nav += (f'<a class="prev" href="{prev_e["slug"]}.html"><span>Previous</span>{esc(prev_e["title"])}</a>' if prev_e else "<span></span>")
            nav += (f'<a class="next" href="{next_e["slug"]}.html"><span>Next</span>{esc(next_e["title"])}</a>' if next_e else "<span></span>")
            nav += "</nav>"
            related = []
            for c in e["categories"]:
                related += [x for x in self.by_category(c) if x is not e and x not in related]
            related = related[:3]
            more = ""
            if related:
                name = self.cats.get(e["categories"][0], {}).get("name", "this topic") if e["categories"] else "this topic"
                more = (f'<section class="block wrap related"><div class="block-head"><h2>More in {esc(name)}</h2>'
                        + (f'<a href="../topics/{e["categories"][0]}.html">All of them</a>' if e["categories"] and e["categories"][0] in self.cats else "")
                        + f"</div>{self.cards(related, root)}</section>")
            draft = '<p class="draft-note">Draft: not published yet.</p>' if e["draft"] else ""
            content = (f'<article class="post"><header class="post-head wrap-narrow">{draft}{self.chips(e["categories"], root)}'
                       f'<h1>{esc(e["title"])}</h1><p class="standfirst">{esc(e["summary"])}</p>'
                       f'<p class="post-when"><span class="day">{self.day_title(e["day_num"])}</span>'
                       f'<span class="hour">{e["hour"]}</span><time datetime="{e["date"].isoformat()}">{date_text}</time></p>'
                       f'{self.crew_list(e["sessions"], root)}</header>{hero}'
                       f'<div class="prose wrap-narrow">{body}</div></article>{nav}{more}')
            self.page(f"posts/{e['slug']}.html", e["title"], e["summary"], content, "", "post-page")

    def build_topics(self):
        tiles = []
        mp = self.media_prefix("")
        for slug, c in self.cats.items():
            posts = self.by_category(slug)
            thumb = next((p for p in posts if p["thumb"]), None)
            img = f'<img src="{esc(mp + thumb["thumb"][6:])}" alt="" loading="lazy">' if thumb else '<span class="no-media"></span>'
            count = f'{len(posts)} {"post" if len(posts) == 1 else "posts"}' if posts else "Nothing yet"
            tiles.append(f'<li class="tile{"" if posts else " is-empty"}" style="--c:{esc(c.get("color", "#8a96a3"))}">'
                         f'<a href="topics/{slug}.html"><span class="tile-media">{img}</span>'
                         f'<span class="tile-name">{esc(c["name"])}</span><span class="tile-count">{count}</span>'
                         f'<span class="tile-desc">{esc(c.get("description", ""))}</span></a></li>')
            root = "../"
            head = (f'<header class="page-head wrap" style="--c:{esc(c.get("color", "#8a96a3"))}"><p class="crumbs"><a href="../topics.html">Topics</a></p>'
                    f'<h1 class="topic-title">{esc(c["name"])}</h1><p class="standfirst">{esc(c.get("description", ""))}</p>'
                    f'<p class="count">{count}</p></header>')
            self.page(f"topics/{slug}.html", c["name"], c.get("description", ""),
                      head + f'<section class="block wrap">{self.cards(posts, root, "Nothing in this topic yet.")}</section>', "topics")
        content = (f'<header class="page-head wrap"><h1>Topics</h1><p class="standfirst">Every post has a main topic. '
                   f'Pick one to see everything about it, newest first.</p></header>'
                   f'<section class="block wrap"><ul class="tiles">{"".join(tiles)}</ul></section>')
        self.page("topics.html", "Topics", "Browse the devlog by topic.", content, "topics")

    def build_timeline(self):
        root, mp = "", self.media_prefix("")
        sections = []
        for n in range(0, self.days + 2):
            posts = sorted([e for e in self.entries if e["day_num"] == n], key=lambda e: e["date"])
            if not posts:
                continue
            rows = []
            sub = submitted_info()
            sub_row = ""
            if sub and self.when(sub["dt"])[2] == n:
                sub_row = (f'<li class="t-row t-submitted"><span class="t-hour">{self.when(sub["dt"])[0]}</span>'
                           f'<span class="t-sub-badge">SUBMITTED</span><div class="t-text"><h3>Submitted at '
                           f'{esc(sub["dt"].strftime("%H:%M"))} UK, {esc(sub["dt"].strftime("%A %d %B"))}</h3>'
                           f'<p>{esc(sub.get("build", ""))}</p></div></li>')
            for e in posts:
                if sub_row and e["date"] > sub["dt"]:
                    rows.append(sub_row)
                    sub_row = ""
                thumb = (f'<img src="{esc(mp + e["thumb"][6:])}" alt="" loading="lazy">' if e["thumb"] else '<span class="no-media"></span>')
                cat = self.chip(e["categories"][0], root) if e["categories"] else ""
                rows.append(f'<li class="t-row"><span class="t-hour">{e["hour"]}</span>'
                            f'<a class="t-thumb" href="posts/{e["slug"]}.html" tabindex="-1" aria-hidden="true">{thumb}</a>'
                            f'<div class="t-text"><h3><a href="posts/{e["slug"]}.html">{esc(e["title"])}</a></h3>'
                            f'<p>{esc(e["summary"])}</p>{cat}</div></li>')
            if sub_row:
                rows.append(sub_row)
            count = f'{len(posts)} {"post" if len(posts) == 1 else "posts"}'
            sections.append(f'<section class="t-day wrap" id="day-{n}"><div class="t-day-head"><h2>{esc(self.day_title(n))}</h2>'
                            f'<span class="count">{count}</span></div><ol class="t-list">{"".join(rows)}</ol></section>')
        jump = "".join(f'<li><a href="#day-{n}">{esc(self.day_title(n).split(",")[0])}</a></li>'
                       for n in range(0, self.days + 2) if any(e["day_num"] == n for e in self.entries))
        content = (f'<header class="page-head wrap"><h1>Timeline</h1><p class="standfirst">Every post in order, '
                   f'grouped by jam day, with the hour it was written.</p>{self.ruler(self.current_hour(), compact=True)}'
                   + (f'<ul class="jump" aria-label="Jump to a day">{jump}</ul>' if jump else "") + "</header>"
                   + ("".join(sections) or '<p class="empty wrap">The first post goes up when the clock starts.</p>'))
        self.page("timeline.html", "Timeline", "Every devlog post, hour by hour.", content, "timeline")

    def build_gallery(self):
        root = ""
        used = [s for s in self.cats if any(s in g["entry"]["categories"] for g in self.gallery)]
        buttons = '<button type="button" data-filter="all" aria-pressed="true">Everything</button>' + "".join(
            f'<button type="button" data-filter="{s}" aria-pressed="false"><span class="dot" style="--c:{esc(self.cats[s].get("color", "#8a96a3"))}"></span>'
            f'{esc(self.cats[s]["name"])}</button>' for s in used)
        items = "".join(self.gallery_item(g, root, with_post=True) for g in self.gallery)
        clips = sum(1 for g in self.gallery if is_video(g["src"]))
        content = (f'<header class="page-head wrap"><h1>Gallery</h1><p class="standfirst">{len(self.gallery) - clips} shots and '
                   f'{clips} clips from the build, newest first. Select one to see it full size.</p>'
                   f'<div class="filter" hidden role="group" aria-label="Show only">{buttons}</div></header>'
                   + (f'<section class="block wrap"><ul class="masonry">{items}</ul></section>' if items
                      else '<p class="empty wrap">Shots and clips appear here as posts go up.</p>'))
        self.page("gallery.html", "Gallery", "Every shot and clip from the build.", content, "gallery")

    def build_crew(self):
        data = {}
        path = HERE / "data" / "crew.json"
        if path.exists():
            data = {r["role"]: r for r in json.loads(path.read_text(encoding="utf-8")).get("crew", [])}
        roles = list(dict.fromkeys(list(data) + [s for e in self.entries for s in e["sessions"]]))
        for role in roles:
            r = data.get(role, {})
            posts = self.by_session(role)
            stats = ""
            if r:
                stats = (f'<p class="count">{r.get("tasks_done", 0)} tasks done, {r.get("commits", 0)} commits, '
                         f'{len(posts)} {"post" if len(posts) == 1 else "posts"}</p>')
            back = '<a href="../how-its-built.html">How it\'s built</a>' if "how-its-built" in self.page_slugs else '<a href="../index.html">Home</a>'
            head = (f'<header class="page-head wrap"><p class="crumbs">{back}</p>'
                    f'<h1><span class="dot big crew-{esc(role)}"></span>{esc(self.names.get(role, role))}</h1>'
                    f'<p class="standfirst">{esc(r.get("about", "A member of the crew."))}</p>{stats}</header>')
            self.page(f"crew/{role}.html", self.names.get(role, role), r.get("about", ""),
                      head + f'<section class="block wrap"><h2 class="sr-only">Posts</h2>{self.cards(posts, "../", "No posts credit this session yet.")}</section>')

    def build_search(self):
        index = []
        for e in self.entries:
            thumb = e["thumb"]
            index.append({"t": e["title"], "s": e["summary"], "u": f"posts/{e['slug']}.html",
                          "c": [self.cats.get(c, {"name": c})["name"] for c in e["categories"]],
                          "w": [self.names.get(s, s) for s in e["sessions"]],
                          "d": self.when_short(e), "o": e["date"].timestamp(),
                          "i": (self.media_prefix("") + thumb[6:]) if thumb else "",
                          "x": plain_text(e["html"])[:1500]})
        (self.out / "search-index.js").write_text("window.DEVLOG_INDEX = " + json.dumps(index, ensure_ascii=False) + ";\n", encoding="utf-8")
        content = ('<section class="page-head wrap"><h1>Search</h1>'
                   '<form class="search-form" action="search.html" role="search"><label for="q">Search titles, topics, sessions and text</label>'
                   '<input id="q" name="q" type="search" autocomplete="off"></form><p class="search-count" aria-live="polite"></p>'
                   '<noscript><p>Search needs JavaScript. Browse by <a href="topics.html">topic</a> or the <a href="timeline.html">timeline</a> instead.</p></noscript>'
                   '</section><section class="block wrap"><div class="cards search-results"></div></section>'
                   '<script src="search-index.js"></script>')
        self.page("search.html", "Search", "Search the devlog.", content, "search")

    def build_pages(self):
        for p in self.pages:
            root = ""
            body = with_media_prefix(p["html"], self.media_prefix(root))
            draft = '<p class="draft-note">Draft: not published yet.</p>' if p["draft"] else ""
            content = (f'<header class="page-head wrap-narrow">{draft}<h1>{esc(p["title"])}</h1>'
                       f'<p class="standfirst">{esc(p["summary"])}</p></header><div class="prose wrap-narrow">{body}</div>')
            self.page(f"{p['slug']}.html", p["title"], p["summary"], content, p["slug"], "standing")

    # ---------- output ----------

    def clean(self):
        for sub in ("posts", "topics", "crew"):
            if (self.out / sub).exists():
                shutil.rmtree(self.out / sub)
        if self.out.exists():
            for f in self.out.glob("*.html"):
                f.unlink()
        self.out.mkdir(parents=True, exist_ok=True)

    def build(self):
        self.clean()
        self.build_home()
        self.build_posts()
        self.build_topics()
        self.build_timeline()
        self.build_gallery()
        self.build_crew()
        self.build_search()
        self.build_pages()
        shutil.copy2(HERE / "template" / "style.css", self.out / "style.css")
        shutil.copy2(HERE / "template" / "site.js", self.out / "site.js")
        for b in web_builds():
            if b.get("url") or b.get("pending"):
                continue
            src, dst = HERE / "play" / b["id"], self.out / "play" / b["id"]
            if src.exists():
                shutil.copytree(src, dst, dirs_exist_ok=True)
            elif not dst.exists():
                self.warnings.append(f"play/{b['id']} is listed in data/web_builds.json but missing")
        if not self.drafts:
            (self.out / ".nojekyll").write_text("", encoding="utf-8")  # lets GitHub Pages serve the folder as-is
            for name in sync_media(self.refs):
                self.warnings.append(f"media/{name} is used but missing")
        else:
            for r in sorted(self.refs):
                if not (MEDIA / r[6:]).exists():
                    self.warnings.append(f"{r} is used but missing")


def sync_media(refs):
    """Make docs/media hold exactly the files approved posts use. Copies new or changed files from
    media/, keeps files already published even if media/ is missing (fresh clone), removes the rest."""
    dest = DOCS / "media"
    dest.mkdir(parents=True, exist_ok=True)
    wanted = {ref[6:] for ref in refs}
    missing = []
    for name in sorted(wanted):
        src, dst = MEDIA / name, dest / name
        if src.exists():
            if not dst.exists() or src.stat().st_size != dst.stat().st_size or src.stat().st_mtime > dst.stat().st_mtime:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
        elif not dst.exists():
            missing.append(name)
    for p in sorted(dest.rglob("*"), reverse=True):
        if p.is_file() and p.relative_to(dest).as_posix() not in wanted:
            p.unlink()
        elif p.is_dir() and not any(p.iterdir()):
            p.rmdir()
    return missing


def build(drafts=False, quiet=False, report=False):
    site = Site(drafts)
    site.build()
    if not quiet:
        where = site.out.relative_to(HERE).as_posix()
        clips = sum(1 for g in site.gallery if is_video(g["src"]))
        empty = [c["name"] for s, c in site.cats.items() if not site.by_category(s)]
        print(f"Built {len(site.entries)} post(s), {len(site.gallery) - clips} shots and {clips} clips into {where}/"
              + (" (drafts included)" if drafts else ""))
        if empty:
            print(f"  topics with no posts yet: {', '.join(empty)}")
        shown = site.warnings if report else site.warnings[:8]
        for w in shown:
            print(f"  warning: {w}")
        if len(site.warnings) > len(shown):
            print(f"  ...and {len(site.warnings) - len(shown)} more (run with --report)")
    return len(site.entries)


def watched_files():
    paths = [HERE / "config.json"]
    for folder in ("entries", "pages", "template", "media", "data"):
        d = HERE / folder
        if d.exists():
            paths.extend(p for p in d.rglob("*") if p.is_file())
    return {str(p): p.stat().st_mtime for p in paths if p.exists()}


def serve(drafts, port, open_browser):
    import http.server
    import threading
    import webbrowser

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(HERE), **kwargs)

        def log_message(self, *args):
            pass

    httpd = None
    for p in range(port, port + 20):
        try:
            httpd = http.server.ThreadingHTTPServer(("127.0.0.1", p), Handler)
            port = p
            break
        except OSError:
            continue
    if httpd is None:
        sys.exit(f"No free port between {port} and {port + 19}.")
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    url = f"http://localhost:{port}/{'preview' if drafts else 'docs'}/index.html"
    print(f"Serving {url}\nRebuilds when entries, pages, media, templates or config change; refresh the page. Ctrl+C to stop.")
    if open_browser:
        webbrowser.open(url)
    last = watched_files()
    try:
        while True:
            time.sleep(1)
            now = watched_files()
            if now != last:
                last = now
                try:
                    build(drafts)
                except Exception as e:  # keep serving while an entry is half-written
                    print(f"build failed: {e}")
    except KeyboardInterrupt:
        httpd.shutdown()
        print("stopped")


def main():
    ap = argparse.ArgumentParser(description="Build the devlog site.")
    ap.add_argument("--drafts", action="store_true", help="include drafts and build into preview/")
    ap.add_argument("--serve", action="store_true", help="serve locally and rebuild on changes")
    ap.add_argument("--report", action="store_true", help="list every quality warning")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--no-open", action="store_true", help="don't open a browser")
    a = ap.parse_args()
    build(a.drafts, report=a.report)
    if a.serve:
        serve(a.drafts, a.port, not a.no_open)


if __name__ == "__main__":
    main()
