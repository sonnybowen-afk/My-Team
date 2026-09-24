---
description: Today's briefing: everything Sonny needs to know and do today
---
Give Sonny today's briefing.

1. Run `date +%Y-%m-%d`. Read the newest file in `briefings/`.
2. **If it's from today:** use it, but first add anything new since it was written. That means Gmail replies since then (search as in `daily-run.md` step 3), anything logged on the pages (the inbox steps in `CLAUDE.md`), and anything in `clients/pipeline.md` now due today.
3. **If there's no briefing for today:** ask **boss** for a status update, check Gmail for replies, and build the briefing fresh in the same sections as `daily-run.md` step 7. Don't research new leads unless Sonny asks.
4. Show it to Sonny in this order. Leave out any empty section, except Money.
   - **Headline:** one line
   - **Needs you:** decisions and replies to answer
   - **Send today:** each message in full, with the number, email or handle to send it to
   - **Gmail drafts waiting**
   - **Follow-ups and chasers due**
   - **Money:** owed, due this week, and level progress
   - **Coming up this week**
5. Leave out anything Sonny has already ticked off on the HQ page (`briefing_done/<date>`, see "Briefing ticks" in `CLAUDE.md`). If you rewrite today's briefing, keep the wording of items he hasn't ticked exactly the same, so their tick boxes stay matched.
6. If anything changed, update `briefings/<date>.md` and the HQ page briefing (`ArtifactData` `set`, collection `briefing`, doc id `today`) so the page matches.
