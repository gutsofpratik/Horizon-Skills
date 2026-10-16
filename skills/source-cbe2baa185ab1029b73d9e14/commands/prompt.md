---
description: Draft, revise, or migrate a prompt using the prompt-engineer skill
argument-hint: [create|revise|migrate] <description or existing prompt>
---

Use the `prompt-engineer` skill for this request.

Arguments: $ARGUMENTS

If the first argument is `revise` or `migrate`, run that mode. Otherwise run
`create`. If a target model is named anywhere in the arguments, treat it as the
target and pin the effort setting explicitly. If no target is named, write for
Class 1 and note what to change for the other classes.
