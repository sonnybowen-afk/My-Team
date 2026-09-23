---
description: Teach an agent something new, like a rule, a preference or an example, so every future job uses it
argument-hint: <agent or "everyone"> <what it should do differently>
---
Train the team with this feedback: $ARGUMENTS

1. **Decide where the lesson belongs:**
   - A **preference or example** (a style Sonny likes, a message that worked, something a client said) goes in `playbook.md`, under the right heading. Every agent reads this file.
   - A **rule about how an agent does its job** (a new check, a step, a limit, something it must always or never do) goes in that agent's file in `.claude/agents/`, in the section it fits best. For "everyone", or a rule several agents share, add it to `playbook.md` under "Sonny's preferences".
2. **Keep it consistent.** Read the file first. If the new lesson contradicts an existing rule, replace the old rule rather than leaving both. Keep the wording short and specific, in the same style as the rest of the file. Never change the pricing (£595 + £50 a month) unless Sonny says so explicitly.
3. **Show me** exactly what changed, as before and after, in plain words.
4. **Save it** so future sessions use it: commit and push the change. If this session works on its own branch, open a pull request into the default branch and tell me it needs merging, unless I've said to merge it myself.
