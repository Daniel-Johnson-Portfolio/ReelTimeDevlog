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

## Seeing is the test

A test that passes isn't proof a player can do it. Twice now a playtest found what the tests missed: [no enemies at all](posts/2026-11-12-2045-playtest-one.html) on day one, [a diner with no way in](posts/2026-11-13-0740-playtest-two.html) on day two. So the crew films.

- **Filming blocks:** every two hours the engine session records reels of each level and copies them to every task they cover.
- **An independent reviewer** watches each reel cold and scores it against the last list of problems.
- **The autoplayer:** [a bot that plays each level](posts/2026-11-13-0410-a-bot-plays-the-level.html) from the title screen with real input. If it can't finish a scene by its script, a person probably can't either.
- **Playtests:** when I sit down to play, the whole crew stops starting new work until I've finished and given my notes.

## When it breaks

It breaks a lot, and those posts are filed under [Fixes](topics/fixes.html): usage stalls, [edits that undid themselves](posts/2026-11-12-2212-edits-that-undid-themselves.html), [the editor running out of memory](posts/2026-11-13-0338-out-of-memory.html), and [a lock file nobody was holding](posts/2026-11-13-1133-the-lock-nobody-was-holding.html). Most of the crew's rules were written the hour after something went wrong.
