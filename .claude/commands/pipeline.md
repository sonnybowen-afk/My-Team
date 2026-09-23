---
description: Update the client pipeline (sent, replied, said yes, delivered, paid, not interested)
argument-hint: <what happened, e.g. "sent 1,3,5 from leads/stockport-barbers-2026-09-23.md" or "Dave's Barbers paid">
---
Use the **boss** subagent to update `clients/pipeline.md` with: $ARGUMENTS

If a business has said yes to a site, also:
1. Create `clients/briefs/<slug>.md` from `templates/client-brief.md` and fill in everything already known from the pipeline and the leads files.
2. List what I still need to ask them for, as one short, casual message I can send them.

Show me the rows that changed and the next action and date for each.

Then sync the pipeline to Sonny's pages as described in `CLAUDE.md`.
