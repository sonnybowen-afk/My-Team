---
description: Find local businesses with no website and draft checked pitches (idea-creator → critique)
argument-hint: <town> <industry> [how many] [whatsapp|sms|email]
---
Run the lead-finding workflow for: $ARGUMENTS

1. Use the **idea-creator** subagent to find leads and draft a first message and a follow-up for each. Pass it the town, the industry, how many leads (default 8) and my preferred channel if I gave one. It saves its work to `leads/<town>-<industry>-<YYYY-MM-DD>.md`.
2. Use the **critique** subagent to review every message in that file (Mode 1: messages).
3. Replace each message the critique didn't PASS with the critique's revised version, in the leads file. If a lead still FAILs a hard rule after revision, drop it from the file and say why.
4. Show me:
   - The lead table, High priority first
   - The final ready-to-send first messages, each with its number/email/handle so I can copy it straight into my phone
   - The critique's tally (e.g. "8 messages: 5 passed, 3 fixed")
   - Anything idea-creator couldn't verify

Don't touch the pipeline yet. Finish with one line telling me to run `/pipeline sent <numbers> from <leads file>` once I've actually sent them.
