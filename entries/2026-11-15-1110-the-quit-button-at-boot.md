---
title: "The packaged run-through caught a quit button at boot"
date: 2026-11-15T11:10:00+00:00
categories: [fixes, pipeline]
sessions: [release, director, ui, gameplay-2]
summary: Making every skip a hold of Space meant a tap no longer skipped the splash, so it went through to the title and pressed QUIT; the release session's scripted run of the zipped game caught it before I did.
cover: media/call-sheet-title-to-shooting-schedule.jpg
draft: false
---

![The title screen, from an earlier film. At boot the mouse cursor was resting where QUIT ends up, so QUIT had focus before anyone touched anything.](media/call-sheet-title-to-shooting-schedule.jpg)

Every build that goes out gets packaged, unzipped and played by a script, the same way you'd run it. The release session calls that the journey: title, every level, the credits, back to the title. At 10:57 round one went green. At 11:10 the journey on that zip failed on its first step.

The Director's log, 11:10:

> "Package ebc091152 FAILED the journey: a tap of pad A/Enter on the splash passes through to the title's focused QUIT and exits the game (since taps no longer skip)."

That came from my own note. I'd asked for every skip to be a hold of Space. So a tap on the splash no longer skipped it, and the tap carried on to the title screen. There, the mouse cursor sat where it was left at boot, over QUIT, so QUIT had focus. Press A, and the game closed.

The fix took 20 minutes and no C++: QUIT on the title now takes two presses (ui), plus a script line fix. Green at 11:30 on 7bc85e179. The journey went from 21 to 23 steps, adding "A on the splash" and "A on the title: no quit", and passed from the zip at 11:47.

This is why release runs the zip and not the editor. The editor never showed it, because in the editor nobody presses A on a splash screen. Every check since then includes those two steps.
