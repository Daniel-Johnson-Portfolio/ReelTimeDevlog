---
title: Play In Browser
summary: The final build of Reel Time running in your browser, through Unreal Engine 5.9's new web export. Very experimental; the jam entry is the Windows build.
order: 3
draft: false
---

> **VERY EXPERIMENTAL.** This is Unreal Engine 5.9's new web export (WebAssembly and WebGPU), a preview feature, running our final build in the browser. Expect a long first load, and expect crashes. **The jam entry is the Windows build**, and that's the one to judge.

## An Unreal Engine 5.9 feature, working

Unreal Engine 5.9 can export a game to run in a web page. Ours is a Shipping build of game commit 3f07edb57, the final build as of 18:00 on Sunday. The Windows entry (0ad3f1e62) came two hours later with three small fixes: the saucer sparing its own aliens, and two controller fixes. The export took 26 minutes and comes to about 220 MB. After the download, it reaches the title in about 7 seconds once you click.

I played it at 19:35 on Sunday: "significantly more stable in Chrome, frame rates are similar but Edge crashes a lot, Chrome is yet to crash in my testing". So **use Chrome**. If you open it in another browser, the "plays best in Chrome" line you see while it loads is Unreal's own notice.

**Before you click:**

- Use **Chrome**, with WebGPU, on a computer with a real graphics card. Phones and tablets won't run it.
- It's a big download, and nothing loads until you click. The size is on each build.
- Once it has loaded, click once more: the page waits for a click before it starts the sound.
- The game plays with a **mouse and keyboard or a controller**, and the controller rumbles on hits, kills and shots. That's in the Windows build. In the browser we've only tested mouse and keyboard. Keyboard and mouse controls: WASD to move, the mouse to look, Space to jump, Ctrl to slide, left mouse to attack, right mouse to throw, E to grab a weapon, Esc to pause. Click the game first so it takes the mouse.
- Time only moves while you do. If it looks frozen, try moving.

## The builds, oldest first

@builds

## How these were made

The release session's first try was on Thursday evening. It starts and runs, but the screen stays black, so it's listed here as a card with no button: it shows where we started. Three more tries on Saturday were stopped by the build tool's lock. Only one build can run at a time on this machine, and the Windows builds came first.

The final one was built on Sunday at 18:38, from the Shipping build I'd just passed in a playtest. It's split into pieces under 50 MB to stay well inside GitHub's file limit, and a service worker puts them back together in your browser.
