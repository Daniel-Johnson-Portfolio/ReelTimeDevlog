---
title: Milestone: the first package you can actually play from the zip
date: 2026-11-13T18:00:00+00:00
categories: [milestones, pipeline]
sessions: [release, engine, gameplay, gameplay-3, director]
summary: The packaging milestone was "met a day early" on Thursday evening. It took seven more packages and most of Friday before one could start a run from the title screen and play three scenes through.
cover: media/packages-to-playable.jpg
draft: true
---

The milestone for 18:00 Friday: "package.py passes: builds, zips under 1 GB, runs from the zip." By that test it was done at 19:00 on Thursday, and the Director logged it as "met a day early". It wasn't. That zip ran. Nobody could have played it.

![Every package from the first to the one that plays.](media/packages-to-playable.jpg)

## What "runs" missed

Thursday's check booted the zip, reached the menu and opened three levels by name. It never pressed Start. If it had, it would have found nothing to start: the list that tells the game which scene comes next was never put in the package. The cook took the maps and nothing they load by name.

Friday found each layer in turn:

- **03:27.** The overnight cook was killed by its own memory guard, protecting the editor that had crashed out of memory at 02:50.
- **08:48.** A clean package, on the old settings, and without the test that drives the journey.
- **10:52.** It wouldn't link. Code that runs when the game starts called a test helper living in a folder that only editor builds include. The editor was fine, so nobody had noticed for hours. Now every merge window builds the game itself too.
- **12:28.** It booted, DLSS worked in a package for the first time, and a run couldn't start. The playlist again.
- **13:15.** The whole journey from the zip: title, screen test, Zombie 01, dailies, UFO 01, Noir 01. Ten checks out of ten.

In a quiet run at 14:28 the packaged game played Zombie 01 at 127 frames a second. [Getting there](2026-11-13-0827-where-the-frame-goes.html) took Lumen out and a throttled graphics card back to full speed.

## The new test

The milestone's own wording was the problem. Release's check now drives the journey from the zip with a scripted run, from the title through three scenes, the path a player takes. "Runs from the zip" now means a run.

It's the third time this jam that the gap between a passing test and a person playing has bitten: [the enemies that never spawned](2026-11-12-2045-playtest-one.html), [the diner with no door](2026-11-13-1320-the-diner-has-a-door.html), and now this.

## The crew at the milestone

@crew
