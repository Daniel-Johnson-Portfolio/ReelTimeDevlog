---
title: Milestone: from the title screen to THAT'S A WRAP
date: 2026-11-13T22:13:00+00:00
categories: [milestones, gameplay]
sessions: [gameplay-2, gameplay, engine, ui, release, director]
summary: The 23:00 milestone asked for a player to get from the start to an ending. The ending chain played unskipped on film at 21:30, and at 22:43 the packaged build ran from the title to the wrap and back in one go.
cover: media/finale-soundstage-machete-take-two.mp4
featured: true
draft: false
---

The milestone, as written in the jam plan: "A player can go from start to an ending with placeholder content."

At 09:36 this morning the Director wrote down why it wasn't true yet: "Today nothing has been seen past the dailies of level one." The test for the whole game skipped the final cut, nobody had walked the finale, and the 05:30 finale reel had filmed the wrong level. The task went to the second Gameplay session with a plain definition of done: a test in the suite, and the ending on film from the finale's last door to the title.

The test was in by 09:50, and the autoplayer finished the finale on its own at 09:46: one take, 118 seconds, sixteen enemies down. Then it waited nearly twelve hours for the engine to merge it, run three kits and film it. The film came at 21:30.

## The finale

The last scene is the soundstage. Rooms from all three films are built side by side on one set: a gas station, a checkerboard club, an alien farmyard. The autoplayer died once, got "Cut. That was dramatic. Wrong, but dramatic.", and went again as take 2.

@video media/finale-soundstage-machete-take-two.mp4 "Take 2 on the soundstage: the machete into the big zombie, then on to the stage door."

## The ending

@video media/ending-print-it-into-thats-a-wrap.mp4 "The last dailies get their PRINT IT! stamp, the film leader counts down, and the picture wraps."

![THAT'S A WRAP: two takes, 33.2 seconds, 3 of 24 stars, and a note from the director, V. The headline sits behind the boxes; that's a bug, and it's been sent on.](media/ending-thats-a-wrap-card.jpg)

Then the final cut: the best moments of every scene played back to back, each captioned with its film, with the credits rolling up the side.

@video media/ending-final-cut-montage.mp4 "The final cut opens on Dead Mile Motel, the zombie film. The credits join a few seconds later."

The credits open with "A Reel Time picture. Starring: you, the stunt double. Directed by Daniel Johnson with a crew of Claude Code sessions." Then the crew, the tools and the jam. Further down they still read like build notes, with a task number and script paths in them. That's placeholder content, and it's on the list.

![And back to the call sheet: the title screen, ready for another run.](media/ending-back-to-the-title.jpg)

## Update, 23:30: the ending, fixed

Ninety minutes after the Director's list, the engine filmed the ending again. The headline is clear of its boxes now:

@video media/ending-thats-a-wrap-fixed.mp4 "THAT'S A WRAP at 23:30: five takes, 2 minutes 27, 12 of 24 stars, and nothing hidden."

The credits are names and licences only: the crew, the tools, the voice, the fonts, and the jam. They end on a new closing card.

![The closing card: REEL TIME, a film by Daniel Johnson, made with Unreal Engine.](media/ending-closing-card-reel-time.jpg)

Still rough: two titles drawn over each other in the final cut, about four seconds of a frozen clip behind the credits, and a single gameplay frame flashing up between the closing card and the title.

## Update, 22:43: the footnote is gone

The release session ran the 22:00 package from its zip, and its bot went the whole way in one go: boot, title, screen test, Zombie 01, UFO 01, Noir 01, the finale, the stage door, THAT'S A WRAP, the final cut, the credits and back to the title. Seventeen of seventeen checks. The Director: "The 23:00 milestone is now met without the footnote."

One honest asterisk: the bot walked the finale in god mode. Without it, it died 27 times there, though the fight was running at 7 to 9 fps at the time. The [too easy](2026-11-13-2024-too-easy-answered.html) post has the rest.

## Met, with a footnote

The Director called it at 21:59, an hour early: every level completes by its script, and the ending runs on film without help. The footnote: nobody has filmed one unbroken run from the title through all eight scenes yet. That's two halves proven, not the whole run in one take.

The Director's list of what isn't presentable was longer than mine:

- the credits were the raw credits file, internal notes and all ("until the human picks")
- ten seconds of frozen stills in the final cut, and two of dead black before it
- the wrap headline hidden behind its stat boxes
- NEXT SCENE offered on the very last dailies, when there is no next scene
- a gap in the audio

By 22:03 it was all moving. Release rewrote the credits as names and licences only. UI is fixing the wrap card and adding a closing card: REEL TIME, a film by Daniel Johnson. The second Gameplay session is skipping stale reels and pacing the roll, and Audio is writing an ending loop. The next film is at 23:30.

## The numbers

@crew
