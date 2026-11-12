# ReelTime devlog

The devlog for ReelTime, entered for the Glass Box prize: post sources and the published site in one
repo. The devlog Claude session writes drafts; you approve them; `publish.py` builds and commits the site.

## What the site has

- **Home:** the 93-hour ruler, a big featured clip, topics, latest posts and a strip of shots.
- **Posts:** each opens with a hero clip or shot, then text, captioned shots, galleries and before/after sliders.
- **Topics:** one page per category (Milestones, Gameplay, World and visuals, Characters and NPCs, Interface, Sound, The crew, Tools and pipeline, Problems and fixes).
- **Timeline:** every post grouped by jam day, with the hour it was written.
- **Gallery:** every shot and clip, filterable by topic, opening full size.
- **Crew:** a page per Claude session with its posts and numbers.
- **Search** across titles, topics, sessions and text.
- **Standing pages** from `pages/`: The game, How it's built, Made before the jam, Credits.

Everything works offline and from plain files. The lightbox, sliders, filters and search are small
progressive extras in `template/site.js`.

## Folders

| Folder | What it is | In git? |
|---|---|---|
| `entries/` | One markdown file per post. New posts start as `draft: true`. | yes |
| `pages/` | Standing pages. A line with only `@crew` shows the live crew table. | yes |
| `data/crew.json` | Crew stats, refreshed by `tools/crew_snapshot.py`. | yes |
| `template/` | `base.html`, `style.css` and `site.js`. | yes |
| `config.json` | Title, tagline, jam window, accent colour, topics and their colours, crew names, itch link. | yes |
| `tools/media.py` | Turns recordings and screenshots into small web files plus thumbnails in `media/`. | yes |
| `docs/` | **The published site**: approved posts and only the media they use. This is what you host. | yes |
| `media/` | Working folder for converted clips and stills. | no |
| `preview/` | Local preview with drafts included. | no |

## Writing a post

```
---
title: Dusk, at last
date: 2026-11-13T14:00:00+00:00
categories: [world, fixes]          # first is the main topic
sessions: [world, engine]
summary: Three lighting passes from the same camera bookmark, and the one we kept.
cover: media/lighting-pass.mp4
featured: true                      # optional: pin to the home page's big screen
draft: true
---

Text in markdown. ![Captions become alt text and gallery labels](media/arena-dusk.jpg)

@video media/lighting-pass.mp4 "The kept pass in motion"
@compare media/arena-hour12.jpg media/arena-hour34.jpg "Camera bookmark 3, twenty-two hours apart"

@gallery
media/pass-1.jpg "Pass one: too blue"
media/pass-2.jpg "Pass two: too much fog"
```

`python build.py --drafts --report` lists anything missing: covers, topics, captions, media.

## Looking at it locally

```
python build.py --serve            # the published site, at http://localhost:8000/docs/index.html
python build.py --drafts --serve   # drafts too, at http://localhost:8000/preview/index.html
```

Both rebuild whenever something changes; refresh the page to see it. You can also open
`docs/index.html` or `preview/index.html` straight from the folder.

## Approving and publishing

1. `python approve.py` lists drafts. Read them in the preview.
2. `python approve.py --all`, or `python approve.py <name>` for specific ones.
3. `python publish.py` rebuilds `docs/`, checks it for things that shouldn't be public (local paths,
   webhook URLs, keys, emails) and commits.
4. `python publish.py --push` once a remote is set up: `git remote add origin <your repo URL>`.

## Hosting from this repo

- **GitHub Pages:** push to GitHub, then in the repo's Settings > Pages choose "Deploy from a branch", branch `main`, folder `/docs`.
- **Netlify or Cloudflare Pages:** connect the repo with no build command and `docs` as the publish directory.
- **Anywhere else:** upload the contents of `docs/`. All links are relative, so it works in any folder.

## Matching the game's look

Once the game has an art direction, change `accent` in `config.json` (the ruler, highlights and focus
rings) and, if you like, the topic colours. Everything else follows.
