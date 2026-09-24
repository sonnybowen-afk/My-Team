---
description: Find local businesses with no website and draft checked pitches (idea-creator → critique)
argument-hint: <town> <industry> [how many] [whatsapp|sms|email]
---
Run the lead-finding workflow for: $ARGUMENTS

1. Use the **idea-creator** subagent to find leads and draft a first message and a follow-up for each. Pass it the town, the industry, how many leads (default 8) and my preferred channel if I gave one. It saves its work to `leads/<town>-<industry>-<YYYY-MM-DD>.md`.
2. Use the **critique** subagent to review every message in that file (Mode 1: messages).
3. Replace each message the critique didn't PASS with the critique's revised version, in the leads file. If a lead still FAILs a hard rule after revision, drop it from the file and say why.
4. **Gmail drafts.** For every lead whose channel is email, use the Gmail connector's `create_draft` tool to save the final message as a draft in my Gmail: `to` is the business's email, the subject line goes in `subject`, and the body is plain text (no markdown, no quote marks). **Never send anything.** Only create drafts. If the Gmail connector isn't available, skip this step and say so.
5. **Sync the leads** to the idea-creator page as described under "Leads sync" in `CLAUDE.md` (update `leads/<name>.json` with the final messages first).
6. Show me:
   - The lead table, High priority first
   - The final ready-to-send first messages, each with its number/email/handle so I can copy it straight into my phone
   - Which leads now have a Gmail draft waiting
   - The critique's tally (e.g. "8 messages: 5 passed, 3 fixed")
   - Anything idea-creator couldn't verify

Don't touch the pipeline yet. Finish with one line telling me to tap "I sent it" on the idea-creator page (or run `/pipeline sent <numbers> from <leads file>`) once I've actually sent them.
