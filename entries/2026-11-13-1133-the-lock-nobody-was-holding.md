---
title: The lock nobody was holding
date: 2026-11-13T11:33:00+00:00
categories: [fixes, crew]
sessions: [toolsmith, director, you]
summary: An empty git lock file has blocked every commit in the shared checkout at least ten times since last night. The tool that's allowed to delete it failed its first review, then starved, then learned to ask who is older.
cover: media/stale-locks-watchdog.jpg
draft: false
---

Most of the crew works in one shared copy of the game's repository. When git writes to it, it drops a small file, `index.lock`, and removes it when it's done. If the file is still there, every other git command refuses to commit.

Since Thursday 23:44 that file has been left behind at least ten times: zero bytes, no git process alive, nobody holding it. Each time, every session's commits failed until someone noticed. From the friction log:

> "stale .git/index.lock (0 bytes, 02:13, no git.exe running) blocked every commit in the shared checkout for 4+ min; removed it by hand."

![The watchdog's morning: three reviews, one failure in the field, one better rule.](media/stale-locks-watchdog.jpg)

## The suspects

One was mine. I had GitHub Desktop open on the repository, and its background refresh takes the lock. I closed it at about 07:50. The locks kept coming.

The second was the crew's own read-only commands. The Director caught itself: "a 'git lfs ls-files' held the index lock for minutes". Those now run with `GIT_OPTIONAL_LOCKS=0`, which tells git not to take the lock just to look.

The real cause of the empty ones is still open.

## A tool that deletes locks is dangerous

The toolsmith's watchdog already sent me an urgent alert when a lock went stale. (At 08:41 I told the Director "I've got the GitHub alert, you are going to have to try to deal with it". It was this.) The obvious next step was to let it delete the lock itself.

Deleting a lock that *is* in use can corrupt the repository's index for fourteen sessions at once. So it went through the crew's review floor, and failed:

- If the "is git running?" check itself errored, the code read that as "no git", and would have deleted a live lock.
- It didn't re-check that the lock it was about to delete was the one it had been watching.
- A failed removal would have spammed me with urgent alerts.

Auto-removal was switched off within two minutes. During the second review, the reviewer found a real stale lock sitting in the checkout, 0 bytes, eleven minutes old.

## Then the outage

At 10:13 another lock appeared. At 10:15 the Director went down with a sign-in error and stayed down for 22 minutes. Nobody else is allowed to delete the lock, and nobody did. Commits were blocked for 24 minutes. The Director's first line back: "Thank you for not deleting it yourselves."

The watchdog passed its third review and went live at 10:53. It needed a quiet stretch with no git process alive. It never got one, because ten sessions were each politely retrying their commits. The next lock sat there until the Director removed it by hand.

## Who is older

The fix, live at 11:02, changes the question. Not "is any git running?" but "is any git process older than this lock?" A process that started after the lock can't be the one that made it. Retries stopped mattering. Every new lock now has its creator logged too, so the next one should name the culprit.

Three reviews and 48 tests for a tool that deletes one file felt slow at the time. I'd rather that than a corrupted repository on day two.
