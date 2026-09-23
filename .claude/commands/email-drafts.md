---
description: Save the email pitches or chasers from a leads file as Gmail drafts (never sends)
argument-hint: <leads file, or business names>
---
Save email messages as Gmail drafts for: $ARGUMENTS

1. Find the messages. If I gave a leads file, use every lead in it whose channel is email. If I named businesses, find their latest checked message in `leads/`.
2. Only use messages the **critique** has passed or revised. If a message hasn't been checked yet, run it past **critique** first and use the revised version.
3. For each one, use the Gmail connector's `create_draft` tool: `to` is the business email, `subject` is the subject line, and `body` is the plain-text message.
4. **Never send.** Don't use any send or reply tool. I review and send every draft myself.
5. Show me a list of the drafts you created (business, email, subject), plus anything you skipped and why.
