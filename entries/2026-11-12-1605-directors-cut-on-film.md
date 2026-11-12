---
title: The Director's Cut: the replay finally shows up on film
date: 2026-11-12T16:05:00+00:00
categories: [gameplay, fixes]
sessions: [gameplay, gameplay-2, floater-1, ui, engine]
summary: Four sets of reels failed to show a full take with its replay, the point of the game. The fifth does. The cause wasn't the game at all: the filming script was skipping it two seconds in.
cover: media/directors-cut-first-replay-on-film.mp4
featured: true
draft: false
---

Reel Time's hook is that after every scene you watch your own take back, shot from film cameras. A headless test has said it works since 08:14. Until this reel, I hadn't seen it in a full take.

@video media/directors-cut-first-replay-on-film.mp4 "The player hits the mark, the Director says 'Right on the X. Good.', and the screen cuts to DIRECTOR'S CUT: the take played back from two cameras, with a REC timecode and a skip prompt."

It's short because the take was short. The filmed take lasted 2.2 seconds, so that's all there is to replay. The figure is the player's stand-in, seen from outside for the first time.

@gallery
media/directors-cut-replay-crane-shot.jpg "The second replay camera, a high crane shot over the forecourt. Frame corners, REC light and timecode are the UI session's replay overlay."
media/hit-your-mark-lit-disc.jpg "Hitting the mark. Two zombies down by the pumps, and the Director's line at the bottom."
media/take-two-slate.jpg "Take two now gets its own slate. That was missing at 13:30."

## Why it took five reels

- **11:30**: the recorder filmed the wrong window.
- **11:45 and 12:25**: the take never ended properly. A debug "god mode" setting had stayed on between play sessions, so the player couldn't die: no CUT, and no dailies.
- **13:30**: CUT and dailies showed up, and the replay was skipped.
- **15:30**: this one.

The last cause is my favourite. The Director's log at 14:12:

> "Found why no reel showed the replay: smoke_run.py skips it 2 s in."

The script that plays the game for the camera was written as a smoke test. Smoke tests want to be fast, so it pressed skip. The replay had been working, and the thing filming it kept cutting it off. The floater session gave the script a filming mode that never skips and gets its kills through real input.

## The whole take, uncut

@video media/whole-take-slate-to-dailies-uncut.mp4 "71 seconds, nothing cut: slate, walk in, two swings, CUT, take two slate, scene cleared, the mark, the replay, dailies, and the countdown leader into the next scene."

This is every stage of the loop in one recording. The walk and the swings are simulated key presses now. The death and the scene clear are still console commands.

## Still wrong

- The replay shows the player's stand-in and not much else. The zombies and the kills aren't in shot.
- The first replay camera is nearly black.
- The dailies thumbnail is still empty.
- The reels are silent apart from a second and a half. Nobody knows yet whether that's the game or the recorder.

I play it myself this evening. That's the test that counts.
