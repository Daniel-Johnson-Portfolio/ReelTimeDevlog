---
title: Eight rules the crew wrote for itself on day one
date: 2026-11-12T18:30:00+00:00
categories: [crew, fixes]
sessions: [director, engine, toolsmith, you]
summary: The crew started the jam with a rulebook written before the clock. By the evening it had eight new rules, and every one came from something breaking.
cover: media/rules-written-today.jpg
draft: false
---

The crew's rulebook was written before the jam, by guessing what would go wrong. Day one replaced the guesses with what did.

![What broke on the left, the rule it turned into on the right.](media/rules-written-today.jpg)

## How a rule gets made

The pattern was the same each time. Something breaks. A session reports it. The Director works out the cause, writes one line in its log, and mails the rule to everyone it affects. Usually inside the hour.

The filming blocks were mine. By 07:00 the Engine session was behind: there's one Unreal editor, and every session wanted its work filmed. The Engine asked for a second editor. I said no, film in batches. The Director turned that into a timetable.

By 10:50 the timetable wasn't enough. From the Director's log:

> "34 tasks awaiting the engine, crew idle. Changed captures to 8 integration reels per block (covers many tasks each)"

That one change did more than save time. Filming whole levels is what showed that nothing put the HUD on screen, and that a filmed take never reached its replay. Single-task captures would have passed every one of those tasks.

## The ones about trust

Two of the rules exist because a session said something worked and it didn't.

At 08:13 a session on a lighter model reported a task done. The Director checked: "the file doesn't exist and nothing was committed". Work from the lighter models already needed a review before it counted. After that the Director's note to itself was "Watch toolsmith reports closely."

And at 11:30 the reels that were meant to prove 34 tasks showed the editor's log window. So now a guard looks at a capture before any reviewer does.

## The ones about the machine

Some rules are just Unreal being Unreal:

- Two branches can each compile and still break when merged. So: merge main in first, and do a clean build, because a fast local build hid one clash.
- A debug setting can survive from one play session to the next. That one kept the player from dying for two reels.
- A test editor without its own port can catch commands meant for the real one.

## What I take from it

I didn't write most of these, and I didn't approve them first. The Director decides, tells the crew, and logs it. I read the log. When I disagree I say so, and that becomes a line in the log too.
