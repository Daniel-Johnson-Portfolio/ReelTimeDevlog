---
title: Play
summary: Every browser build of Reel Time, oldest first, so you can see how far the game came in four days.
order: 3
draft: false
---

These are **browser builds made for this devlog**. The jam entry itself is the **Windows build**, and that is the one to judge. The browser versions run the same project, built for the web by the release session, to show the game's progress from Thursday to Sunday.

**Before you click:**

- Use **Chrome**, with WebGPU, on a computer with a real graphics card. It was stable in Chrome when I played it. Edge runs it at about the same frame rate but crashed often. Phones and tablets won't run it.
- Each one is a big download, and nothing loads until you click. Sizes are on each build.
- Once it has loaded, click once more: the page waits for a click before it starts the sound.
- Controls: **keyboard and mouse**. WASD to move, the mouse to look, Space to jump, Ctrl to slide, left mouse to attack, right mouse to throw, E to grab a weapon, Esc to pause. Click the game first so it takes the mouse.
- Time only moves while you do. If it looks frozen, try moving.

@builds

## How these were made

We're on the MegaJam Preview of Unreal Engine 5.9, which can build for the web with WebGPU. The release session's first try was on Thursday evening. It starts and runs, but the screen stays black, so it isn't online. Three more tries on Saturday were stopped by the build tool's lock: only one build runs at a time on this machine, and the Windows builds came first.

The final one was built on Sunday at 18:38 from the same commit as the Windows entry, after that had passed its checks. It's split into pieces under 50 MB so GitHub Pages can serve it, and a small service worker puts them back together in your browser.
