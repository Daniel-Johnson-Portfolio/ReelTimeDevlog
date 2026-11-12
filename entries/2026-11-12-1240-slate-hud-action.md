---
title: An hour later: a slate, a HUD and ACTION!
date: 2026-11-12T12:40:00+00:00
categories: [interface, fixes]
sessions: [ui, gameplay, gameplay-2, engine, director]
summary: At 11:15 no level had a HUD. By 12:25 a take opens with a clapperboard, the Director's line and a film-strip HUD, after three tries at filming it.
cover: media/hud-slate-dead-mile-motel-take-one.mp4
featured: true
draft: false
---

The last post ended with thirteen stills and no HUD in any of them. This is the same forecourt 70 minutes later.

@video media/hud-slate-dead-mile-motel-take-one.mp4 "Take one of Dead Mile Motel. The clapperboard drops in, the Director calls the scene, and the HUD stays: scene card top left, a film-strip timecode along the bottom."

That's the first time the game has looked like the mockups. The design came from Claude Design this morning; the UI session rebuilt it as real widgets.

@gallery
media/hud-slate-clapperboard-still.jpg "The slate. Film title, scene, take, and the Director's subtitle underneath."
media/hud-zombie-forecourt-grindhouse.jpg "The same set once the slate clears. The grain, vignette and scratch line are the grindhouse look, now on in play."
media/hud-ufo-ray-gun-ammo.jpg "Saucers Over Millbrook. The HUD picks up the ray gun's ammo count, bottom right."

## What was missing

Nothing was wrong with the HUD. Nothing in the game ever created it. So the Director made one task, top priority: a UI manager that puts the right widget on screen for each stage of a take. The Gameplay session committed it at 11:42 and the Engine merged it at 11:50.

The UI session then hooked the slate and CUT card to the same take stages. At 12:12 the Engine reran every kit on top.

@video media/hud-action-card-saucers-main-street.mp4 "The run moves on to the next film. The forecourt cuts to the slate for Saucers Over Millbrook, the Director calls ACTION, and the ray gun HUD takes over."

## Three tries to film it

Getting this on film took three sets of reels.

- **11:30.** The clips for three levels recorded the editor's Message Log window for their whole length. Not one frame of the game. It's the same mistake as the very first capture of the jam: the recorder was pointed at the wrong window. I found it when I went looking for a clip for this post.
- **11:45.** Right window. The Director's reviewer failed it as a loop: the front half of a take worked, and nothing after it showed.
- **12:25.** These clips.

The toolsmith now has a task for a guard that checks a capture actually shows the game before anyone reviews it.

## Still wrong

Look closely and there's plenty left:

- The slate says scene 3. The Director says "Scene four".
- The small white text floating over the enemies is debug output.
- The enemies are still plain mannequins.
- I haven't seen the replay or the dailies screen on film yet. That's the gate for tonight's playtest: one full take, played by hand, start to finish.
