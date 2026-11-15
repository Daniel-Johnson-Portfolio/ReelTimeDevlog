---
title: "You can play the final build in your browser now"
date: 2026-11-15T19:00:00+00:00
categories: [pipeline]
sessions: [release, director, you, devlog]
summary: Thursday's browser build loaded but never drew a frame; today's, built from the same commit as the Windows entry, shows the call sheet in Chrome after one click and is now on the new Play tab.
cover: media/web-build-final-call-sheet-in-chrome.jpg
draft: false
---

@compare media/web-build-thursday-black-in-chrome.jpg media/web-build-final-call-sheet-in-chrome.jpg "The same check on both browser builds, in Chrome on this machine, served without any special headers, the way a plain web host would. Thursday's build (before) runs at 121 fps and draws nothing. Sunday's build (after) shows the call sheet."

On Thursday I asked for [an experiment](2026-11-12-2050-web-build-experiment.html): build the game for the browser. It built, and nobody had seen it draw a frame. That stayed true until today. At 17:30 the release session finally opened it in a real Chrome window. It downloaded 169 MB, started in 11 seconds with WebGPU on and no errors, and stayed pure black (the brightest pixel was 1 out of 255).

At 16:40 I asked for "a HTML build of the game (+ the ones we already have to show progress) into its own header tab in the devlog website". Release built a new one at 18:38 from 3f07edb57, the same commit as the Windows build we're submitting, once that had passed. This one starts in 6.9 seconds. It shows "Click or press a key for sound" until you click, then the title menu.

It's on the new **[Play](../play.html)** tab, along with Thursday's as a card with no button. Each build is one line in a data file and a folder, and nothing downloads until you click.

What to know before you click:

- It needs **Chrome or Edge with WebGPU** and a real graphics card. Phones won't run it.
- It's about **220 MB**, split into pieces under 50 MB to stay well inside GitHub's 100 MB file limit. A service worker joins them up in the browser.
- It holds the front end, the screen test and the first zombie scene. **The Windows download is the game we entered**, and the whole of it.

Thursday's build is still a mystery: same engine, same method, black screen. On the last day there was no time to find out why, and the one that matters works.
