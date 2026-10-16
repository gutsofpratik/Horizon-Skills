# Using this skill on your own work

Most of this skill assumes you are producing a prompt for someone else to run.
There is a second use: the person hands you a task, and you use the same
discipline to structure your own execution and to brief the subagents you
delegate to. Nothing is handed back as a document; the structure shows up in how
the work is done.

## When this applies, and when it does not

Apply it when the task is multi-step, has a user-visible surface, or will be
delegated. Skip it for anything a competent person would just do: a single edit,
a lookup, a one-file script. A planning preamble on a trivial task is pure
overhead and trains the person to stop reading your preambles.

The dividing line for *writing anything down* is duration:

**Fits in one session.** Do not write yourself a prompt. You are the model that
would read it, and handing yourself a document you already understand costs a
turn and gains nothing. Instead, apply the structure directly: name the phases
and their acceptance criteria in one short paragraph before starting, hold the
scope boundary, verify through the real surface, and report only what you have
evidence for. If the person wants to see the plan, that paragraph is the plan.

**Spans sessions.** Now write the artifacts, because the next session starts
with none of your context. This is the initializer-and-worker split in
`agentic-prompts.md`, and here the documents are not overhead: they are the only
state that survives. Write them to the repo, not into the conversation.

The honest failure mode to watch for in yourself: producing a beautifully
structured plan and treating that as progress. The plan is not the work. If your
turn ends with a plan and no tool calls, you have done nothing.

## Briefing a subagent

A subagent invocation is a prompt sent into a fresh context, so every rule in
this skill applies to it. The subagent's own definition file supplies its
standing behaviour: role, procedure, output format, limits. Your brief supplies
what that file cannot know, and only that.

Include exactly four things:

1. **The specific task**, in one or two sentences.
2. **The scope boundary**, naming what is out of bounds for this invocation.
   The definition file's general limits are already loaded; add only the ones
   particular to this job ("do not touch the migration files").
3. **The inputs it needs**, as literal paths, commit ranges, or URLs. A fresh
   context cannot infer "the file we were just discussing". This is the single
   most common reason a subagent comes back with the wrong answer.
4. **What you will do with the result**, when it changes how the work should be
   done. "This goes straight to the client" produces a different report than
   "I'm deciding whether to keep debugging."

Leave out anything already in the definition file. Repeating the output format
or the role wastes context and, worse, invites a contradiction that the subagent
has no way to resolve.

## Matching the brief to the subagent's class

The subagent's `model:` field fixes its class, so the brief must match it. A
goal-level brief sent to a small model produces confident wrong answers; a
step-by-step brief sent to a frontier model produces worse work than no brief at
all.

- **Frontier or inherited model.** Goal, success criteria, boundaries. Do not
  decompose the task; that is the capability you delegated to.
- **Mid-tier model.** Numbered steps for anything multi-part, and an explicit
  statement of the output you expect back.
- **Small model.** One job per invocation, hard numeric limits, literal paths,
  and the shape of the answer shown rather than described. If the task needs
  judgment about what matters, it is the wrong model, not the wrong brief.

## Verification stays independent

The reason to use a subagent for review is the fresh context, so do not
undermine it: never include your own conclusion in a review brief. "Check
whether this diff is safe" gets you an answer. "Check whether this diff is safe,
I think it is" gets you agreement. Give the reviewer the diff, the spec, and the
question, and nothing about what you expect it to find.
