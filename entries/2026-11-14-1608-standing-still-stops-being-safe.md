---
title: Standing still stops being safe
date: 2026-11-14T16:08:00+00:00
categories: [gameplay, characters]
sessions: [npc-ai, gameplay-2, director, engine, release]
summary: In a game where time slows when you stop, stopping was the winning move. The Enemies session added idle pressure, the first film of it failed on the real levels, and the 14:45 reel shows a player who stands still dying in every level filmed.
cover: media/still-player-shamblers-walk-up-and-cut.mp4
draft: false
---

Reel Time's rule is that the world moves when you move. The cheap way to beat that is to not move. On Friday I called the game too easy because time all but stopped when I did, and the crew answered by making the world run at quarter speed when you stand still. That wasn't enough.

@video media/still-player-shamblers-walk-up-and-cut.mp4 "14:45 today, the gas station. The player is not touching the controls. Two shamblers walk in from the forecourt, one swings, the take is cut, and take two opens with the objective and the line 'Keep moving: when you stop, they don't.'"

## What the film showed this morning

The Director's review of the 05:30 reels, which was the same code I played at 10:00, had two findings under "still open":

- standing still at the start of a level is safe, because nothing comes for you
- a shambler three metres from a still player hovered off screen for more than 25 seconds

Enemies only woke up when you walked into their area, and the ones that were awake waited for a turn that never came. The decision at 09:50 was a new rule called idle pressure, described in the log as "the director gets impatient". If you stand around, the director sends them in, and says so.

## It failed first

The Enemies session had it written by 10:07 and it was merged at 11:50. The 12:14 film on the real levels failed. The log line lists three reasons: the player's start mark sat outside the enemies' area, the code that frees a stuck enemy ran on a clock that stops when the player stops, and some of the places enemies were told to walk to were off the walkable floor. None of that shows until you run it in the real levels.

@video media/still-player-aliens-close-in-landing-field.mp4 "The second UFO level, same test: stand at the gate and wait. The aliens come across the yard toward the gate, and the take is cut. The small white labels over their heads are debug text showing what each one is thinking."

## Now

The fixed version was filmed at 14:45 and the engine's reviewer passed all three clips. On the gas station a still player died three times in 70 seconds. In the UFO level, twice in 56. The target is a first hit within 10 to 15 seconds of standing still.

The best evidence came from somewhere else. The Release session's packaged-build test scored 19 out of 21 this afternoon, and both failures were the test's own fault: its bot stands still between steps, and it kept getting killed.

Still open from the same review: the gunmen in the first UFO level never fire, and some shamblers walk straight past you. Both are due before tonight's playtest.
