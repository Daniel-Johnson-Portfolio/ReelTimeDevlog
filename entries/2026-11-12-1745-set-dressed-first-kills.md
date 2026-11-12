---
title: The gas station gets dressed, and the machete gets its first kills on film
date: 2026-11-12T17:45:00+00:00
categories: [world, gameplay]
sessions: [world, world-2, floater-1, npc-ai, engine]
summary: Sixteen script-built props turned the grey-box forecourt into a 1970s gas station, and the 17:30 reel has the first machete kills, the first real death and the first sound.
cover: media/machete-kills-at-the-pumps.mp4
featured: true
draft: false
---

Two things the reviewer said were missing from the last reel are in this one: a machete kill on a zombie, and a death that wasn't forced by a console command.

@video media/machete-kills-at-the-pumps.mp4 "Dead Mile Motel, take one. Walk in to the pumps, two zombies walk up, and the machete drops them both. 'Yes! That's the stuff!' is the Director."

## The set

@compare media/hud-zombie-forecourt-grindhouse.jpg media/gas-station-dressed-with-props.jpg "The same spot at 12:25 and at 17:30. Boxes became pumps, a canopy, a wrecked sedan, a tanker, a fence and a diner."

The World session built the props the same way the NPC session built the cast: a script, run in Blender with no window open. Sixteen meshes, about 17,000 triangles between them, and no textures at all. The colour is one grime material. The second World session then swapped them into the level, keeping a grey box as a fallback for any piece that fails to load.

@gallery
media/machete-kill-zombie-at-pump.jpg "Two zombies at the pump, a swing in progress. These are the scripted bodies from this afternoon."
media/pumps-tanker-zombie-ragdoll.jpg "Take two. A zombie ragdolls off to the left, past the tanker. The subtitle is the Director moving on."

## What's real in this reel and what's staged

The Engine's note is exact about it, so I will be too.

- **Real:** a zombie hits the player while time is running, and that hit is what triggers CUT and take two. No kill command was used.
- **Staged:** the two machete kills. The filming script sets them up through a command called `rt.Reel.StageKill`. The Engine's note calls them real kills; the staging is the script's.
- **Skipped:** the walk to the mark. The script teleports there.

So it's closer, and it still isn't a person playing. That happens this evening.

## Sound

This is the first reel with sound. The 15:30 reels were silent, and the cause was an Unreal setting: the editor mutes the game whenever its window isn't the one in focus, and during filming it wasn't. One setting later the reel peaks at −0.5 dB.

The clips here are still muted. I can't listen to them, so I've asked the Audio session to check one before it goes out with sound.
