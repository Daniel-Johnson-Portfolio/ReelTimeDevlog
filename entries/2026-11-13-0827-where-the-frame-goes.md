---
title: Lumen is out: finding seven milliseconds a frame
date: 2026-11-13T08:27:00+00:00
categories: [fixes, pipeline]
sessions: [gameplay-3, director, you, world]
summary: My playtest ran at about 20 fps. Within the hour the feel session had measured what every graphics setting costs on Zombie 01, and the Director switched Lumen off for good.
cover: media/gpu-cost-zombie01.jpg
draft: false
---

The last note from [this morning's playtest](2026-11-13-0740-playtest-two.html) was the bluntest:

> "Performance, it's quite bad… I don't mind if we want to go for a non-Lumen approach but we need to be hitting at least 60 fps on this machine."

I'd played in the editor, at about 20 fps. The editor is slower than the game on its own, but as I told the Director, that "does seem low even for that". I can't judge how movement feels at that frame rate, so this came before any more polish.

## Measure first

At 07:36 the Director asked the feel session for a table of what each level costs the graphics card, "within 60 min". It wrote a console command, `rt.Perf.Sweep`, that stands the camera at a level's opening view, switches one setting off, waits, averages three seconds, puts it back and moves to the next. The first table, for Zombie 01, was in at 08:15.

![What each setting costs on Zombie 01. Lumen's global illumination is the biggest single item; the film look costs 1.1 ms and stays.](media/gpu-cost-zombie01.jpg)

The frame took 18.7 ms on an RTX 2060. 60 fps needs 16.7. Lumen's lighting was 3.2 ms of that, and switching Lumen from hardware to software ray tracing made it worse, not better. With Lumen off, plain shadow maps and DLSS Quality together: 11.5 ms.

## The decision

The Director took it the same minute:

- Lumen off in every preset, with screen-space reflections in its place
- virtual shadow maps off
- DLSS Quality by default on cards that have it
- volumetric fog off
- three or four shadow-casting lights per area, no more
- the film look stays. The feel session's own note on it: "Leave it, it's the look."

The World session relights the first three levels for it. I also asked for graphics presets on the main menu, Low, Medium and High, and never Unreal's lowest.

![Zombie 01's forecourt under Lumen, from last night's reel. This is the "before"; the relit set follows.](media/zombie01-forecourt-kiosk.jpg)

## What the table got wrong

Two rows were the sweep's own fault, and the session said so in the table. "DLSS Performance" measured the same as Quality because the sweep's restore step blocked the game's own resolution setting. And every row after 08:09 is void: the frame time jumped to 98 ms the moment the sweep switched one light's shadow off at runtime, and never came back. That can't happen in play, so it isn't my 20 fps, but it's being chased.

The numbers are also from an 864-line window, not 1080p. The estimate for 1080p is 12 to 13 ms. The other levels are being measured now.

## Update, 10:40: the first reel without Lumen

The engine switched Lumen off at 09:26 and the World session's fill lights went in with it. On the 09:30 reel of Zombie 01 the graphics card's share of the frame reads between 9.5 and 11 ms, where the table measured 18.7. The reel is in [the next post](2026-11-13-1037-tape-on-the-floor.html).

Two more things came out of the measuring. The game had been rendering at 864 lines and stretching to fit, because the display is scaled to 125% and the game didn't know. And UFO 01 is far worse than Zombie 01: 45 to 50 ms with its fifteen shadow-casting lights, which is the next thing to fix.

## Update, 11:25: 65 to 90 fps, and a correction

The feel session got a quiet machine and measured the game on its own, at a true 1920×1080, Medium preset, DLSS Quality. Noir 01: 8.8 ms on the graphics card at the opening view, 9.0 in a fight, 65 to 90 frames a second.

That corrects the paragraph above. The 45 to 55 ms readings on the reels weren't the levels. They were the editor, its extra viewport and the screen recorder all sharing one graphics card with the game. The session's verdict: "Nothing in the level costs 40 ms." My 20 fps this morning was the same thing, since I played inside the editor.

So there were two problems wearing one number. Lumen really was too expensive, and that's fixed. And the editor was never a fair place to judge frame rate, which is why the next playtest runs on a packaged build.

## Update, 13:40: the packaged game didn't get the memo

At 13:15 a packaged build played the whole journey from the zip for the first time: title, screen test, Zombie 01, the dailies, UFO 01, Noir 01. Ten checks out of ten.

Then the frame rate: 34 fps in Zombie 01, 13 in Noir 01, and 7.7 in UFO 01.

The first suspect was the settings: the readout said Epic quality at 1280×720, not our Medium preset. The Gameplay session found one real bug there (on a first run, Unreal's saved settings put Epic back over our preset) and fixed it.

**Update, 14:10.** That wasn't the main cause. The feel session watched the graphics card itself during the packaged run: it was held at about half its normal clock speed the whole time, by a power setting on the machine, not by the game. This morning's 8 to 10 ms runs were at full speed. So the packaged numbers above measure a throttled card, and they'll be measured again. The watchdog now warns the crew when the card is held back like this, so a slow run can't be blamed on the game again.

One more saving came out of it: switching DLSS to an older, lighter model (preset F) saves about 6 ms a frame on this card.

**Update, 14:30.** With the card back at full speed, the packaged game ran Zombie 01 at 127 frames a second: 5.85 ms on the graphics card, against 18.7 at the start of this post. The stutters people had counted dropped to about four a minute. Twenty fps this morning; 127 by the afternoon. I asked for 60.
