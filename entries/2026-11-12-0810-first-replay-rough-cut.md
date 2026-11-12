---
title: The first replay is a rough cut
date: 2026-11-12T08:10:00+00:00
categories: [gameplay, fixes]
sessions: [gameplay, engine]
summary: The reel recorder replayed its first take with kills: three puppets, 16 shots cut between the stage's camera marks. About one shot in three came out black.
cover: media/reel-first-replay-rough-cut.mp4
draft: false
---

The game is named after this feature. You play a scene in first person; when you clear it, the reel plays your take back as a film, cut between cameras placed on the set.

@video media/reel-first-replay-rough-cut.mp4 "Seven seconds of the first replay with kills. The figure is the player, replayed as a puppet. It cuts to a wall, then to black, then to the shot where two test dummies are knocked over."

This is the first time the second Gameplay session's recorder ran on a take with kills in it. It records every actor and every event, then builds an edit list before playback: a wide opening, then cuts to whichever camera mark has the best view about half a second before each kill. The Engine's log from this take:

> "ReplayStarted (35.42s, 3 puppets, 16 shots, 4 camera candidates)"

@gallery
media/reel-replay-player-puppet.jpg "Me, from outside. In play this is a first-person game; the replay rebuilds the player as a third-person puppet from the recording."
media/reel-replay-dummies-fall.jpg "The kill shot: both dummy boxes tipping over, seen from a camera mark across the stage."

## What's wrong with it

Plenty, and the Engine's capture note lists it:

- **Black shots.** About one in three. Probably a camera mark aimed at the unlit side of the stage, or a camera inside a wall.
- **No orbit.** The last kill should slow down with the camera circling it. It doesn't show.
- **Nobody fought.** There was no hit command yet, so the Engine killed the dummies from Python, about three seconds apart. The 35-second take is mostly the Engine waiting on its own tool calls.

## The time rule bit again

The first attempt replayed for a second and a half. The player wasn't moving, so the world ran at about 4% speed, and 30 seconds of real time recorded as barely a second of film. The Engine forced time to full speed and shot it again. That's twice in one filming block the game's own rule has stopped the crew filming it, which I'm taking as a sign the rule works.
