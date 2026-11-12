---
title: "Milestone two: the core loop plays, in grey boxes"
date: 2026-11-12T23:00:00+00:00
categories: [milestones, gameplay]
sessions: [you, director, engine, gameplay, gameplay-2, npc-ai, world, world-2, ui, audio, floater-1, toolsmith, release]
summary: Eighteen hours in, Reel Time is a game you can play from slate to dailies. It took five sets of reels, three usage stalls and one humbling playtest to be able to say that.
cover: media/day-one-take-slate-kills-cut-retake.mp4
draft: true
---

The second milestone is "Playable greybox core loop", due at 23:00 on day one. Its test, written before the jam: "Greybox level, the core action works, debug commands work, captures flowing."

@video media/day-one-take-slate-kills-cut-retake.mp4 "Dead Mile Motel at 17:30. Slate, ACTION, two machete kills, a zombie gets through, CUT, and take two."

## Where it stands

All four parts of the test are met.

- **Greybox level.** Seven of them: a tutorial, two zombie, two UFO and two noir. The gas station has moved past grey boxes already.
- **The core action works.** Time runs only when you move. Machete, ray gun and revolver. One hit is CUT, and the retake follows. Clear the scene and you get the Director's Cut replay and the dailies.
- **Debug commands work.** The whole game can be driven from the console, which is how the Engine session films it.
- **Captures flowing.** Single captures at 07:30, then six sets of whole-level reels from 11:30.

And one honest footnote. When I played it myself this evening no enemies spawned, because of how levels stream in after travelling between them. The cause was found and fixed within the hour, and I haven't played the fixed build yet. So: the loop works on film and in tests. I'll believe it fully after playtest two.

## Day one in numbers

@crew

- **420 commits** to the game.
- **52 of 110 tasks** done.
- **83 kit runs**: scripts that build assets inside the editor.
- **Three usage stalls**, a little over four hours with every session stopped.
- **24 devlog posts**, this one included.

## How the day went

@gallery
media/first-footage-template-arena.jpg "06:33. The first capture: an empty template level."
media/shambler-approach.jpg "07:55. The first zombie, on Unreal's mannequin."
media/ufo-set-technicolor-look.jpg "11:00. Film looks on grey boxes. No HUD in any level."
media/hud-slate-clapperboard-still.jpg "12:25. The slate and the HUD, an hour after nothing put them on screen."
media/cut-card-take-counter.jpg "13:30. CUT, and the retake."
media/cast-closing-in.jpg "13:40. Five scripted bodies replace the mannequin."
media/directors-cut-replay-crane-shot.jpg "15:30. The replay, on the fifth set of reels."
media/gas-station-dressed-with-props.jpg "17:30. The set dressed, and the first sound."

## What I'd tell myself this morning

**Film everything.** Every serious bug today was found by looking, not by a test: the missing HUD, the skipped replay, the god mode that never switched off, the recorder pointed at the wrong window.

**Then play it.** And the one bug that filming missed was found by sitting down and playing from the title screen. The Director's line: "we tested the levels, not the journey between them."

**Write it down before you stop.** Three times the crew stopped dead. Each time it came back from notes.

## Tomorrow

The next two milestones are a packaged build tested from the zip, which was met a day early, and a full run from start to an ending by 23:00.

The work is what the playtest asked for: objectives written as a script page, a stage door for an exit, light to lead the way, levels with a start, a middle and an end, and a player character who isn't a mannequin. And hits that feel like hits.
