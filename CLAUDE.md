# CLAUDE.md

This file gives Claude Code guidance for working in this repository.

## Project overview

The toolkit for a one-person UK freelance web design business: find local businesses with no website, pitch them (**£595 build + £50/month maintenance**), build simple one-page sites, and track every client from pitch to paid.

The work is done by four subagents in `.claude/agents/`:

| Agent | Job |
|-------|-----|
| `idea-creator` | Researches a town and industry for businesses with no website, and drafts casual pitches and follow-ups |
| `web-builder` | Builds `sites/<slug>/index.html` from a brief using the house template |
| `critique` | Reviews messages and sites (including screenshots) and gives exact fixes |
| `project-manager` | Keeps `clients/pipeline.md` up to date, says who to chase, and drafts chase messages |

## Repository structure

- `.claude/agents/`: the four subagents
- `.claude/commands/`: slash commands that chain them (`/find-leads`, `/build-site`, `/review`, `/pipeline`, `/status`)
- `business.md`: the user's name, area, pricing, what the monthly fee covers, and payment terms. Every agent reads this.
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
npm install                        # installs Playwright for the screenshot check
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

- Outreach must **never** mention a business's reviews, ratings or stars, and must quote exactly £595 + £50/month.
- Messages must sound like a real person texting: short, casual, no AI or sales-template phrasing.
- Never send messages on the user's behalf. Draft them for the user to send.
- Always run messages and sites past `critique` before calling them done.
- Keep `clients/pipeline.md` updated through `project-manager`, not by hand-editing in other workflows.
