---
title: "Milestone: the final build is a Shipping build, and it passed"
date: 2026-11-15T18:15:00+00:00
categories: [milestones, pipeline]
sessions: [you, director, engine, release, gameplay, gameplay-2, gameplay-3, world, ui]
summary: The last window went green at 17:45 on 3f07edb57 and release packaged it in Shipping (456 MB); I played it at six and wrote "Perfect shipping passed all tests, and gained a good chunk of FPS". That's the build we submit.
cover: media/screen-test-cutout-then-gunman-final.mp4
featured: true
draft: false
---

![The gas station in the final Shipping build. Where the debug "FEEL" readout used to show after pressing F7, there's nothing now: F7 is gone from the game.](media/z1-after-f7-no-feel-text.jpg)

> "Perfect shipping passed all tests, and gained a good chunk of FPS"

That was my verdict at about 18:10, after playing the final build. It's the one we submit: **game commit 3f07edb57, packaged in Shipping, a 456 MB zip.**

## Why Shipping

All jam long we packaged in Development, the configuration the jam recommends. At about half past five I read the updated submission page: Shipping is accepted for Windows too. Shipping strips the debug tools and runs faster, so I asked for it: "can the next playtest be a shipping build, can we get rid of that F7 UI for the movement mode. Also gets us some FPS back".

F7 was a key the crew used to flip between movement presets while tuning. gameplay-3 took it out of the code, ui took the inert row out of Settings, and the engine set the default in one ini line (T-0228).

## The bug only Shipping could find

The first Shipping compile failed with about 200 errors. Two test files, `RTEnemyTests.cpp` and `RTReelEDLTests.cpp`, had tests sitting after their `#endif` guard. Development builds include the test framework, so those stray tests compiled fine. Shipping leaves the framework out, and everything outside the guard broke. gameplay-3 moved them inside the guard (125397fd9). Editor, Development and Shipping all built, and the Director called it the final green at 17:45.

## The last fixes

My 16:40 notes went into that window. The tutorial now has you hit the cardboard stand-in before the noir gunman appears (T-0225). The saucer is silent in replays (T-0226). Plus world's lights and signs at the gunman station, and more light on the Blue Parrot stairs.

@video media/screen-test-cutout-then-gunman-final.mp4 "The screen test in the final build, played by the demo bot: the cardboard stand-in first, then the gunman steps out into the light and goes down to the machete."

@gallery
media/tutorial-cutout-first-final.jpg "Final build, screen test: the cardboard cut-out comes first now. Swing at it, and acting moves time too."
media/tutorial-gunman-after-cutout-final.jpg "With the cut-out crossed off, the next note is the gunman: 'A gunman steps out. The DOUBLE keeps moving, closes in and takes him down.'"

## The day

Today was three playtests from me, three fix rounds, a content lock at 16:00, and this. 122 commits landed on main between 07:30 and 18:00. The release session's scripted run of the zip caught a quit-at-boot bug I'd have shipped. A compile error hid behind Development builds until the last few hours.

@crew

Still to come tonight: a Development build as a fallback, the browser build for the [Play In Browser](../play.html) tab, and the submission.
