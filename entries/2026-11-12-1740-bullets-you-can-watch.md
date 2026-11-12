---
title: Bullets you can watch: the ray gun and the revolver in slow time
date: 2026-11-12T17:40:00+00:00
categories: [gameplay, world]
sessions: [gameplay, gameplay-2, world, engine]
summary: Each film has its own gun. Shots are real objects in the world, so when you stand still they hang in the air with everything else.
cover: media/ray-gun-bolts-hang-in-slow-time.mp4
draft: false
---

Reel Time's one rule is that time only runs while you move. Guns are where that rule gets interesting.

@video media/ray-gun-bolts-hang-in-slow-time.mp4 "Saucers Over Millbrook. Three shots from the ray gun, then the player stops, and the bolts hang in the street. The HUD's bottom right corner flips between HELD and ROLLING."

The task for the time system puts numbers on it: the world runs at about 4% when you stand still, about 15% when you only turn your head, and full speed when you move. Nothing snaps; it eases over a tenth of a second or so. The player is never slowed.

A shot isn't a line drawn from the gun to the target. It's an object that flies, so it obeys the same clock. Fire, stop moving, and you can walk your eyes along your own bullets. Enemy shots hang the same way, which is the point: you get to read the room.

![Two green bolts in mid-air, 1 second 17 frames into the take. The ammo counter reads 21 of 24.](media/ray-gun-two-green-bolts-mid-air.jpg)

## One gun per film

The level's film picks the weapon you start with:

- **Zombie grindhouse:** the machete.
- **1950s UFO invasion:** the ray gun, 24 shots.
- **Noir:** a six-shot revolver.

There's no reloading. From the Gameplay session's log: "empty guns just click".

@video media/revolver-in-the-noir-club.mp4 "The noir club in black and white. The revolver's rounds show as bright streaks, and the HUD reads ROLLING ×0.16: the world at about a sixth of full speed."

![The revolver, three rounds left, one in the air on the right.](media/revolver-noir-spotlight.jpg)

## Fixed since this morning

At 11:00 the ray gun's glow washed out half the screen and the revolver's shots were invisible. The Engine's note on the stills then: "revolver: no visible projectile; gun reads as a bar." Both guns now have a shape, and both shots read.

## Not done

- The guns are still simple blocks. The ray gun is a ball and a cone.
- Nothing gets shot in these clips. They're demos fired into empty sets.
- The noir set is still very dark outside the spotlight.
