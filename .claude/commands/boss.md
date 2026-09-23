---
description: Tell the boss (project-manager) what you want. It plans the job, and Claude runs the agents it picks.
argument-hint: <anything, e.g. "what should I do today?", "Annie's Nails said yes", "find work in Telford">
---
The request for project-manager, the master agent: $ARGUMENTS

If no request was given above, use: "What should I do today?"

1. **Plan.** Use the **project-manager** subagent in master mode and pass it the request word for word. It replies with a plan, or makes a pipeline update itself if that's all the request needs.
2. **Check.** If the plan lists anything under **Needs Sonny**, stop and ask me those questions before running any step.
3. **Run the plan.** Carry out each step in order with the named subagent (**idea-creator**, **web-builder** or **critique**), passing each step the previous step's output. Apply critique's revised messages, and give web-builder critique's fixes, as the plan says. Stick to the plan and don't add steps. If a step fails or turns up a problem the plan didn't expect, stop and tell me.
4. **Gmail.** Save the messages listed under **Gmail drafts** using the Gmail connector's `create_draft` tool. **Never send anything.**
5. **Report back.** Give **project-manager** what it asked for under **Report back to me with**, so it can update the pipeline. If the pipeline changed, sync the pipeline to Sonny's pages as described in `CLAUDE.md`.
6. **Tell me**, briefly:
   - What was done, and by which agent
   - The finished messages ready to send (with each number, email or handle) or the site path, whichever applies
   - Which Gmail drafts are waiting
   - What project-manager says happens next, and when
