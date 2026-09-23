# CLAUDE.md

This file gives Claude Code guidance for working in this repository.

## Project overview

The toolkit for a one-person UK freelance web design business: find local businesses with no website, pitch them (**£595 build + £50/month maintenance**), build simple one-page sites, and track every client from pitch to paid.

The work is done by four subagents in `.claude/agents/`. **project-manager is the master**: every job starts and ends with it.

| Agent | Job |
|-------|-----|
| `idea-creator` | Researches a town and industry for businesses with no website, and drafts casual pitches and follow-ups |
| `web-builder` | Builds `sites/<slug>/index.html` from a brief using the house template |
| `critique` | Reviews messages and sites (including screenshots) and gives exact fixes |
| `project-manager` | **Master.** Plans each job and picks the agents, keeps `clients/pipeline.md` up to date, says who to chase, and drafts chase messages |

## Repository structure

- `.claude/agents/`: the four subagents
- `.claude/commands/`: slash commands that chain them (`/boss`, `/find-leads`, `/build-site`, `/review`, `/pipeline`, `/status`, `/email-drafts`, `/train`)
- `business.md`: the user's name, area, pricing, what the monthly fee covers, and payment terms. Every agent reads this.
- `playbook.md`: what the team has learned: Sonny's preferences, pitches that got replies, and client feedback. The agents read it, project-manager adds real results, and `/train` adds lessons.
- `templates/site-template.html`: the house site template. Every client site starts as a copy of it.
- `templates/client-brief.md`: the brief layout
- `clients/pipeline.md`: the pipeline and single source of truth
- `clients/briefs/<slug>.md`: one brief per client
- `leads/<town>-<industry>-<date>.md`: idea-creator output
- `sites/<slug>/`: client sites (`index.html` and `images/`; `screenshots/` is git-ignored)
- `scripts/screenshot.mjs`: phone and desktop screenshots plus layout checks for a site

## Development

### Setup

```bash
npm install                        # installs Playwright for the screenshot check (runs automatically in cloud sessions via .claude/settings.json)
npx playwright install chromium    # only needed on a machine without a browser already installed
```

### Common commands

```bash
node scripts/screenshot.mjs sites/<slug>/index.html   # screenshots + layout check
```

## Conventions

- `<slug>` is the business name in lowercase with hyphens (`daves-barbers`).
- Dates are `YYYY-MM-DD`. British English everywhere.
- Client sites are single self-contained HTML files built from the template. Change colours via `:root` variables only, and keep the structure and class names.
- Missing client info stays as `[PLACEHOLDER: …]`. Never invent prices, hours, contact details or testimonials.

## Notes for Claude

- **project-manager is the master.** When Sonny asks for anything about the business in plain words (not a specific slash command), follow `.claude/commands/boss.md`: ask project-manager for a plan, run that plan with the agents it names, then report back to project-manager so it updates the pipeline. Subagents can't call each other, so the main session carries out project-manager's plan.

- Outreach must **never** mention a business's reviews, ratings or stars, and must quote exactly £595 + £50/month.
- Messages must sound like a real person texting: short, casual, no AI or sales-template phrasing.
- Never send messages on the user's behalf. Draft them for the user to send. For email, save them as Gmail drafts with the Gmail connector's `create_draft` tool, and never use `send_message` or reply tools.
- Don't automate Instagram or LinkedIn messages. The user sends DMs by hand.
- Always run messages and sites past `critique` before calling them done.
- Keep `clients/pipeline.md` updated through `project-manager`, not by hand-editing in other workflows.

## Web Crew HQ page (pipeline sync)

Sonny's HQ page at https://claude.ai/artifact/TVDxQLvtJLazHwpoArFq1r shows the pipeline live. **Whenever `clients/pipeline.md` changes**, sync the page straight afterwards with the `ArtifactData` tool (load it with ToolSearch if needed): action `set`, that url, collection `pipeline`, doc id `current`, with this body built from the whole of `clients/pipeline.md`:

```json
{
  "updated": "YYYY-MM-DD",
  "clients": [
    { "business": "Annie's Nails", "stage": "pitched", "contact": "07700 900000", "channel": "WhatsApp",
      "next_action": "Follow-up message", "due": "YYYY-MM-DD", "notes": "short note" }
  ]
}
```

- `stage` is one of: `pitched`, `replied`, `in_progress`, `delivered`, `maintenance`, `closed` ("Paid / Maintenance" is `maintenance`).
- `due` is the row's follow-up, fee or next-£50 date, or `""` if there isn't one. `next_action` says what's due then, in a few words.
- Always send the full list (it replaces the whole document). An empty pipeline is `"clients": []`.
- If the `ArtifactData` tool isn't available in the session, skip the sync and tell Sonny the page is out of date.

