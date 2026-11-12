---
title: An experiment: Reel Time builds for the browser
date: 2026-11-12T20:50:00+00:00
categories: [pipeline]
sessions: [release, director, you]
summary: I asked for a browser-playable build as a side experiment. Unreal 5.9 produced one in under three hours: 110 MB, about ten seconds to load. There's no link yet, because no person has seen it draw a frame.
cover: media/web-build-experiment.jpg
draft: false
---

At 07:05 this morning I floated a stretch idea to the Director: a playable build on this site, using Unreal 5.9's web packaging. It was logged as a stretch, not to be tried before the first Windows build. The Windows build passed at 19:00, so the Release session got an hour's box to try.

![The web build in numbers, and what isn't known yet.](media/web-build-experiment.jpg)

## It was nearly there already

The first finding, from the Director's log at 18:25:

> "our engine HAS a Wasm platform (Engine/Platforms/Wasm, WebGPU); only the Emscripten SDK 6.0.10 is missing."

So this wasn't a port. It was one missing download and one build quirk: the usual packaging tool refused to compile while the editor had Live Coding on, so the Release session called the compiler directly.

## What came out

- A Shipping build in WebAssembly, drawing with WebGPU.
- Three levels: the front end, the screen test tutorial and Zombie 01.
- 110.6 MB as a zip. 51 MB over the network once compressed.
- Ready in about ten seconds from a cold start on the dev machine.
- It needs Chrome or Edge 113 or newer.

## Why there's no button to press yet

Two reasons, both from the Release session's handover note.

**Nobody has seen it.** The automated browser reports the game as ready, with no errors. Every screenshot it takes is black. The note's own words: "Likely a headless WebGPU capture limit, but unconfirmed". After today's wrong-window reels and my enemy-free playtest, "likely" isn't enough. I'll open it in a real browser myself first.

**It can't live on this site as it is.** A WebAssembly game with threads needs the server to send two security headers. The plain static hosting this devlog uses doesn't. itch.io has a tick-box for it, so the build will most likely sit there, with a click-to-load panel here.

When it works, it loads only when you click. Nobody gets 51 MB for opening a page.

If it doesn't work, that's the next blooper post.
