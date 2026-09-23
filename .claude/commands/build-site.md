---
description: Build and polish a client site draft (web-builder → critique → web-builder → critique → project-manager)
argument-hint: <business name or brief path> [any brief details]
---
Build a site draft for: $ARGUMENTS

1. **Brief.** Use the brief path if I gave one. Otherwise use `clients/briefs/<slug>.md` if it exists. Otherwise pass the details I've typed to the web-builder, which will save them as a brief.
2. **Build.** Use the **web-builder** subagent to build `sites/<slug>/index.html` from the house template and run its screenshot check.
3. **Review.** Use the **critique** subagent to review the site (Mode 2).
4. **Fix.** If the verdict is NEEDS CHANGES, send the full review to the **web-builder** to apply, then have the **critique** review again. Do at most 2 fix rounds. If it's still not ready after that, stop and show me what's outstanding.
5. **Track.** Use the **project-manager** subagent to put the business in **In progress** (move it if it's already in the pipeline) with the site folder, the target delivery from the turnaround in `business.md` (default 5 working days), and "Waiting on: client info" if placeholders remain. Then sync the HQ page as described in `CLAUDE.md`.
6. **Report back** with:
   - The site path, plus how to preview it: open `sites/<slug>/index.html` in a browser, or look at `sites/<slug>/screenshots/mobile.png` and `desktop.png`
   - The critique's final verdict and how many fix rounds it took
   - The critique's "questions to send the client", merged into **one** short, casual WhatsApp message I can send them (sign it with my name from `business.md`)
