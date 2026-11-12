---
title: Run, slide, wall kick: the player moves
date: 2026-11-12T07:50:00+00:00
categories: [gameplay]
sessions: [gameplay, engine]
summary: The Gameplay session's first-person character runs, slides under a gap and kicks off a wall, with the camera feel driven by one data asset. Filmed in the 07:30 block.
cover: media/movement-run-slide-wall-kick.mp4
draft: false
---

Movement was the top-priority task of day one. Reel Time's world only runs while you move, so moving has to feel good before anything else matters.

@video media/movement-run-slide-wall-kick.mp4 "Five seconds on the soundstage: run, slide under the lintel, run at the checker wall, jump, kick off it. The yellow line is the debug readout: speed, state, kicks used, field of view, camera roll."

This is our own character, not the template one. The Gameplay session had it written and passing headless tests 32 minutes after the task was created. It then waited for the Engine session to merge it and film it, which is how every piece of the game reaches the screen.

@gallery
media/movement-slide-under-lintel.jpg "Mid-slide under the lintel. The field of view widens and the camera rolls into the slide."
media/movement-run-at-checker-wall.jpg "Full run at the checker wall the demo spawns, 8.2 metres a second."
media/movement-wall-kick-roll.jpg "Just after the kick. The camera rolls away from the wall, then settles."

## Every number in one place

The task asked for a camera that feels "heavy but never nauseating", with every value in a data asset. A kit script writes that asset, so tuning needs no rebuild. Some of what's in it now:

- **Run:** 8.2 m/s.
- **Slide:** needs 4.5 m/s to start, adds a boost up to 14.5 m/s, lasts a second at most.
- **Wall kick:** pushes away and up, three per jump, and never twice in a row off the same wall.
- **Camera:** field of view 95°, up to 14° wider with speed and 8° more in a slide. Roll of 7° into a slide and 11° away from a kicked wall.

Every camera effect is multiplied by a comfort scale from 0 to 1, which the settings menu will drive.

## What you're not seeing yet

Nobody is holding the controller. The clip is a debug command, `rt.Debug.MoveDemo`, that plays the same inputs each time so the Engine can film it unattended. I get my hands on it in tonight's playtest, and that's when the numbers above start changing.

The Engine also had to move the shoot. Its capture note:

> "The template arena has a yellow cylinder or block ~10 m ahead of the PlayerStart in every direction (tried yaw 0, 45, 90, 180, 270), so the demo ran into it and stalled."

So it filmed on our own soundstage, which is why the first movement footage already has the grindhouse look on it.
