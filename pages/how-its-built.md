---
title: How it's built
summary: The crew of Claude Code sessions behind this game, and how they work together.
order: 10
draft: false
---

One person and a crew of Claude Code sessions, each with its own job, its own folders and its own inbox. I talk to two of them. The Director turns what I want into tasks, hands them out, checks the results, and tells me when something's ready to look at. The Devlog writes this site.

![Who talks to whom. Every arrow is a file dropped in an inbox folder.](media/crew-map.jpg)

## The crew

@crew

## How work moves

![A task's journey, from a request to something a player can see.](media/task-journey.jpg)

- **Tasks:** every piece of work is a small file with an owner, the folders it may touch, and a definition of done.
- **Kits:** only the engine session touches the Unreal editor. Everyone else hands it a "kit", a script that builds their assets, so their work stays readable and can be rebuilt from scratch.
- **Reports:** when a session finishes, the Director hears about it automatically and has a reviewer check the screenshots against the definition of done.

## Models

Every session is Claude Code. By day the Director and the Devlog run on Claude Fable 5.2 and most of the builders on Opus 5.5, with Sonnet 5.5 on the lighter jobs. Nothing done on a model below Opus counts as done until an Opus-level model has reviewed it.

## Decide, don't wait

Sessions make reasonable assumptions instead of waiting for answers, and write them down. I look over the assumptions later, not before.

## Day and night

At night the crew keeps working. The Director fills every queue before I go to bed, nobody waits for me, and I get a digest in the morning: what got done, which assumptions were made, and what broke.
