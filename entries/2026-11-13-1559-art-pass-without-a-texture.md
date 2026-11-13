---
title: An art pass without downloading a texture
date: 2026-11-13T15:59:00+00:00
categories: [world, characters]
sessions: [world, world-2, npc-ai, engine, you]
summary: At 11:26 I put "art passes, possibly new art" on the plan. By 15:30 every set had new surfaces, decals, posters and props, all made by script, with no downloaded textures. The stunt double finally has a helmet that reads on film.
cover: media/zombie01-art-pass-forecourt-into-shop.mp4
draft: false
---

@video media/zombie01-art-pass-forecourt-into-shop.mp4 "15:30, Zombie 01 after the art pass: oil stains and tyre marks on the forecourt, then the shop's new checkered floor."

After the first playtest on Thursday I said the art "doesn't obviously need a big art pass". By lunchtime the core worked, so I changed my mind. At 11:26 the Director logged my words: "art pass also means possibly new art". Five sessions took a piece of it.

## Surfaces from code

The World session's rule for itself, written into its task log: "No textures: procedural HLSL only (no licensing/credits, rerunnable)." Every surface is a material made of maths: plywood, concrete, tarmac, canvas flats. The oil stains, cracks and tyre skids are 31 procedural decals placed by a kit.

![The gas station forecourt after the pass. The ground reads as concrete and tarmac now, not grey boxes.](media/zombie01-forecourt-art-pass.jpg)

## Posters from Blender

The posters needed pictures, so the World session drove Blender with no window open, rendered twelve of them to image files, and closed it again. The brands are invented, because the jam rules don't allow anyone else's: Fizz-O Cola, Brasscap motor oil, a "Missing" flyer, and a poster for each of the game's own films.

@gallery
media/noir01-jazz-club-art-pass.jpg "Noir 01, the jazz club. Tables, bar and stage in black and white."
media/zombie02-motel-art-pass.jpg "Zombie 02, the motel, with its sign and set dressing."
media/ufo02-backlot-art-pass.jpg "UFO 02 in the film's Technicolor look: a picket fence, lamps and a green glow on the lawn."

The second World session did the same for props: shop fronts, a bandshell, finned cars, a police car, a crashed saucer, a camera dolly and lighting truss, each built in Blender by script and previewed from front and back before it went in.

## The double and the weapons

![The stunt double, red colourway, front, back and side. The helmet is buff with a red stripe down the back now; cream blew out to plain white on film.](media/stunt-double-turnaround-red.jpg)

The NPC session builds every body from MakeHuman, an open-source human model, through a Blender plugin, all scripted. Its fix this afternoon was the helmet. On the 12:30 reel it read as a bald white head. The colours were working. The cream was simply too bright for the film look, so it went buff, with a wider stripe.

![The NPC session's models for the weapons the levels will place, three views each.](media/in-level-weapons-sheet.jpg)

## Still to do

The finale is too dark to show yet. The UFO 01 posters went on the walls sideways. The barrel that should explode didn't. Most of these are booked for the 17:30 block.
