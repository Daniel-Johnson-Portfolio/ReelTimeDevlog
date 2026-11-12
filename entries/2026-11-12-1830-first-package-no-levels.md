---
title: The first packaged build had no levels in it
date: 2026-11-12T18:30:00+00:00
categories: [pipeline, fixes]
sessions: [engine, release, director]
summary: The game built, zipped and ran with DLSS on a day ahead of the packaging milestone. Then the Release session's own check found only the menu level was inside.
cover: media/first-package-empty.jpg
draft: true
---

Everything in this devlog so far was filmed inside the Unreal editor. A jam entry is a zip that runs on someone else's PC, and plenty of jam games die at that step on the last night. So the first package was a day-one task, and I'm glad it was.

![Four steps from "won't build" to a fixed cook list, in under three hours.](media/first-package-empty.jpg)

## It wouldn't build

The editor build worked all day. The packaged game target failed. The cause was DLSS again: the plugin as installed has nothing prebuilt for a packaged game. The Engine's fix was to build DLSS and Streamline as plugins of the project.

One decision came with it. The NVIDIA plugin stays out of the game's git repo and a setup script copies it in. The Director's note on why is two words: "licence caution".

## It built, and it was fat

At 16:30 the package built: 680 MB zipped. 516 MB of that was debug files. The good news inside it: DLSS reports as on in the packaged game, which the NVIDIA prize needs.

## It was empty

The Release session then ran its own pipeline in its own checkout and got the zip down to 472 MB. It had also written a check for which levels are in the package. The answer, from the Director's log at 17:05:

> "Correction: the baseline package had no levels cooked (only L_FrontEnd)"

The game opens its levels by name at run time. Unreal's packager only includes levels something points at, and nothing pointed at them. The package would have started, shown the title screen, and had nowhere to go.

The fix is a list of maps to cook: the front end and the seven playable levels. So the 472 MB figure is wrong too. The real size comes from the next run.

## Why this is a good blooper

Nobody saw it fail. A check found it on Thursday afternoon, 80 hours before the deadline. The same bug found at Sunday's content lock would have cost the evening.
