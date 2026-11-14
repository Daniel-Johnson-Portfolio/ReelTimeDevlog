---
title: Night shift two: what the crew did with "too easy"
date: 2026-11-14T05:15:00+00:00
categories: [crew, gameplay]
sessions: [director, gameplay, gameplay-2, gameplay-3, npc-ai, world, world-2, ui, audio, release, engine]
summary: I handed over at 18:38 with five notes and asked for fourteen hours of work. By 05:00 the crew had made 188 commits, answered all five, hit the 23:00 milestone early, and left me a build to play and a list of decisions to check.
cover: media/noir01-replay-dance-floor-angles.mp4
draft: false
---

At 18:38 on Friday my [playtest three](2026-11-13-1841-playtest-three.html) notes went to the Director, with one request: queue about fourteen hours of work, because I wouldn't be back until the morning. This is the second night the crew has run on its own ([the first](2026-11-13-0238-the-night-shift.html)). At 05:09 the Director wrote me a morning report. Here is what's in it.

## My five notes, and what happened

| My note | By morning |
|---|---|
| Too easy; when I stop, time basically stops | The world runs at a quarter speed when you stand still, and zombies next to you close in and swing. Shamblers take two machete hits. Take 2 now brings the whole cast back: before, it didn't, which is why retakes were a walk. |
| No guns for zombies; a ranged zombie is fine | Zombie levels are melee only, plus the spitter, which rears back with a lime glow and lobs a green glob. |
| Slide prompts, target after the slide, hit the stunt double | Done, except the Shift prompt: there's no sprint key. That's a question for me. |
| Replays better, animations not there, T-pose | No T-pose on any character, tested for every one. Blends between moves. Cameras that keep the double in frame. |
| Wall jumping not optimized | Coyote time, a jump buffer, a longer reach. Diagonal kicks work 10 times out of 10 in every level; head-on kicks were still being fixed. |

@video media/screen-test-cardboard-double-falls.mp4 "The tutorial's new last target: the cardboard stunt double."

## Also overnight

- **The milestone.** "Full run start to finish" was due at 23:00. It was [met at 21:59](2026-11-13-2213-full-run-start-to-finish.html), and at 22:43 the packaged build ran from the title through the screen test, the first scene of each film and the finale, to the wrap and back to the title.
- **Death got better.** The CUT card says what got you ("A shambler got you"), the retake comes in under a second, and the first death teaches: "Keep moving: when you stop, they don't."
- **Falling off the set** calls a CUT ("The edge of the set"), after a bot got stranded on a ledge.
- **Art.** The [second levels](2026-11-13-2113-art-pass-three.html) caught up, every level got an [opening shot](2026-11-14-0301-first-frames.html), and the sets got rain, fans and flickering lights on game time.
- **The replay cameras** got [rules](2026-11-14-0329-every-shot-sees-the-double.html).
- **Audio.** A 1.3-second freeze and silence after every ACTION! turned out to be sounds loading at the wrong moment. Fixed.

@video media/ending-thats-a-wrap-fixed.mp4 "The ending as it stands this morning."

## What went wrong

Difficulty swung both ways. After the retake fix, the bot died 27 times in the finale (partly at 8 frames a second), then 25 times in Zombie 01, nearly all to one runner who wakes while you're busy at the pumps. By 04:11 the finale was beaten in two takes without god mode, and Zombie 01 was softened at 04:40. Nobody has measured it since. The Director's note to me: "Your hands are the real test: one or two takes on Zombie 01 is the target."

And twice, other jobs on the machine spoiled the frame-rate measurements. The morning numbers need an idle machine.

## Decisions waiting for me

The Director made five calls overnight and listed them with "say if you disagree": the quarter-speed time floor, melee-only zombie levels, slide taught without a sprint, scenes numbered in shooting order, and credits as plain text with no third-party logos, because the jam rules ban them. Then a list for me to pick from, including the first drafts of the trailer and the jam video.

## The numbers

188 commits between 18:38 and 05:13. UI and Gameplay made 23 each, the second Gameplay session 20, the two World sessions 18 each.

@crew
