---
title: The night shift: how the crew works while I sleep
date: 2026-11-13T02:38:00+00:00
categories: [crew]
sessions: [director, engine, ui, gameplay, gameplay-2, gameplay-3, world, world-2, npc-ai, audio, you]
summary: I signed off at 22:30 with a playtest booked for 07:00; every two hours since, the engine has filmed every level, a reviewer has marked what's broken, and the Director has sent the fixes out before the next block.
cover: media/night-shift.jpg
draft: false
---

![The night so far, from the Director's log.](media/night-shift.jpg)

At 22:12 I told the Director I was going to sleep, and asked for a report at 07:00 of what changed. My last message, at 22:30:

> "just because it's night mode you're still the boss; if you think the UI needs to step it up a gear, bump the model; that goes for everything."

The Director's night plan to the crew was ten lines. The first one: "The human is asleep; never wait for an answer: decide, note the assumption on the task, keep going."

## The loop

The night runs on a two-hour loop. On the hour the engine merges the C++ that's ready. At the filming block it records every level from the title screen, with sound. The Director gives those reels to a separate reviewer that hasn't seen the work, so it isn't marking its own homework. Its findings go to the session that owns each one, and the fixes have to land before the next block.

The first review, at 23:58, opened with this:

> "a first-time player could not yet play L_Zombie_01 from the title to the stage door without being told."

The Director used the authority I'd given it two minutes later. It moved the UI session up to Opus for the night to wire the script page.

## Twelve items, two hours later

The second review, at 02:15, went back through the same twelve items one by one. Summed up:

| Since 23:30 | Items |
|---|---|
| Fixed | Objectives progress, script page in the levels, kill confirm |
| Mostly fixed | Replay: the red stunt double now stars, but its head and hands are still the mannequin's |
| Partly | The route, deaths that come too fast, audio, lighting, settings, the AI test rooms |
| Still there | The tutorial's ending, a white flash on the way out of a level |

Its verdict: "not yet, but close." It also caught something new. The follow spot meant to guide you to the exit fills a third of the view.

Next block 03:30. The packaged build gets tested from its zip at 03:00. I'll add the morning to this post.

## Update, 06:07: how the night ended

The 03:30 block slipped half an hour after [the out-of-memory crash](2026-11-13-0338-out-of-memory.html), and it was the first reel [played by the autoplayer](2026-11-13-0410-a-bot-plays-the-level.html) rather than staged. The 05:30 block came in early, and the fourth review, at 05:55, is the one I wanted to read before waking up:

> "Zombie 01 plays on real input from the title through death, retake, shop, keys, back door, stage door, replay … dailies with a still, NEXT."

The follow-spot cone is gone everywhere. What's left for 07:00 is mostly signposting: the back lot has no count or pointer, so the autoplayer stood there for 37 seconds. A fix for that and two others merged just after filming, so no reel shows them yet. At 05:47 the Director called the playtest hold: blocker fixes only, and the build ready by 06:45.
