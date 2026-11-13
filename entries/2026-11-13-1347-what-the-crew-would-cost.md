---
title: What the crew would cost at API prices
date: 2026-11-13T13:47:00+00:00
categories: [crew, pipeline]
sessions: [toolsmith, director, devlog, you]
summary: About $1,200 so far for 33 hours of a fourteen-session crew, if it were billed per token. $577 of that is measured; the rest is an estimate with its working shown. The figure on this site now updates every time it publishes.
cover: media/crew-cost-by-session.jpg
draft: false
---

I asked the crew to work out what this game would cost if every token were paid for at API prices. It runs on a subscription, so nothing here is billed per token. But it's the number a reader would want, and nobody was recording it until late this morning.

![Each session's cost at API prices, as Claude Code reports it. The Director and the Devlog run on Fable, the builders on Opus.](media/crew-cost-by-session.jpg)

## The running total

@cost

## How it's counted

**Measured.** At 11:34 today the toolsmith had every session start writing a row to a ledger every four minutes: role, model, and the cost Claude Code itself reports for that session. Numbers only, nothing from the conversation. A session's figure covers its whole life, not just the time since 11:34. The Director has run since the first hour of the jam yesterday, and the engine and the first Gameplay session for 27 hours, so a lot of the jam is in the measured part already.

**Estimated.** Sessions that were closed or restarted before 11:34 left no figure. For those I counted the hours each role was open and multiplied by what the ledger shows each model costing per hour:

| | Session-hours | Per hour | Low | Mid | High |
|---|---|---|---|---|---|
| Opus builders | about 190 | $2.30 to $5.90 | $220 | $560 | $1,290 |
| Sonnet (audio, toolsmith) | about 60 | $0.35 to $0.60 | $10 | $20 | $40 |
| Earlier Devlog sessions, Fable | about 25 | $2 to $4 | $25 | $50 | $115 |

Low assumes half those hours were spent parked, which costs nothing, at the cheapest rate measured. Mid assumes three quarters at the median rate. High assumes every hour at the dearest rate, plus 15% in case subagents aren't included.

**Guessed.** Whether subagents (the reviewers that watch reels, the API scouts) are inside Claude Code's figure isn't confirmed. I think they are.

## What surprised me

**The Director costs the most.** $205, more than any builder. It runs on Fable, whose input and output cost two and a half times Opus's, and it reads everything: every report, review and log.

**Rereading costs more than writing.** Almost all the spend is cache reads: each turn rereads a session's whole context, at a small fraction of the input price. A session with a long memory costs more per hour than a busy one with a short memory. That's an argument for the crew's habit of starting sessions fresh with a desk note.

**Stalls cost nothing.** The three usage-limit stalls on Thursday stopped everything, so they don't add to the cost. They added hours instead.

## Per piece of work

The jam has 971 commits so far and 73 tasks closed. At about $1,200, that's roughly $1.25 a commit and $16 a finished task.

Over the last two hours the whole crew spent roughly $30 to $40 an hour. If it keeps that pace to Monday's deadline, the rest of the jam adds about $2,000.

The panel above updates every time the devlog publishes, and there's a link to this post on the home page.
