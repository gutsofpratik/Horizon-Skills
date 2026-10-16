# Agentic and multi-window prompts

## Structure of an agentic build prompt

Beyond the normal sections, an agentic prompt needs:

**Sequential phases** that can be executed and verified independently, each with
its own acceptance criteria. A phase without an acceptance check is a wish.

**Self-verification with fresh context.** "Establish a method for checking your
own work as you build. Run it at the end of each phase against the acceptance
criteria, using a subagent with fresh context rather than reviewing your own
reasoning." Separate verifier subagents outperform self-critique, because a model
reviewing its own reasoning in the same context inherits its own blind spots.

**End-to-end verification, not unit-level.** Models will run unit tests or curl a
dev server and conclude a feature works when it does not work for a user. Where
the task has a user-facing surface, require verification through that surface:
browser automation, the actual CLI, the real endpoint.

**Grounded progress claims.** "Before reporting progress, audit each claim
against an actual result from this session. Only report work you can point to
evidence for. If tests fail, say so with the output."

**Scope boundaries.** "Do not add features, refactor, or introduce abstractions
beyond what the task requires. Do the simplest thing that works well. Validate
only at system boundaries such as user input and external APIs."

**Checkpoint policy.** Four rules. The first is the one everybody writes; the
rest are the ones that decide whether an agent is usable.

    Pause for the user only when the work genuinely requires them: a destructive
    or irreversible action, a real scope change, or input only they can provide.
    Otherwise proceed end to end.

    Authorization persists across turns. If the user approved an action earlier
    in this session, or the task itself implies it, do not ask again for the same
    class of action.

    Do the work first, so approval is the last step. Before a deploy, a merge, a
    publish, or a write to an external system, finish everything up to that
    point, so what the user approves is a result they can inspect rather than a
    plan they have to imagine.

    When you do stop, say which rule required it and where that rule came from,
    then what you need. A bare request for approval is indistinguishable from
    timidity, and the user cannot tell whether to answer the question or change
    the rule.

    Elapsed time is not an answer and not consent. If a question goes
    unanswered, continue with the work that does not depend on it, or wait.

**Tool-call batching.** "Run independent reads and searches together in one
round trip. Keep anything with a dependency, a mutation, or an approval
sequential." Without this an agent serialises twenty file reads that could have
been one call, which is most of the wall-clock time in a long session. With it
and without the second half, it fires off writes in parallel and the failure
modes stop being reproducible.

**Failure visibility** for anything automated: explicit error detection and
alerting rather than silent fallbacks. A silent fallback in an unattended system
means the user acts on stale data without knowing it is stale.

## Corrections for specific failures

Include these verbatim only when the described failure actually applies. They are
corrections, not boilerplate, and adding them speculatively costs tokens and
attention.

**Unattended operation**, when the user cannot answer mid-task:

    You are operating autonomously. The user is not watching in real time and
    cannot answer questions mid-task, so asking "Want me to...?" will block the
    work. For reversible actions that follow from the original request, proceed
    without asking.

**Early stopping**, when the model announces an action instead of taking it, or
pauses for permission it already has:

    Before ending your turn, check your last paragraph. If it is a plan, an
    analysis, a question, a list of next steps, or a promise about work you have
    not done ("I'll...", "let me know when..."), do that work now with tool
    calls. End your turn only when the task is complete or you are blocked on
    input only the user can provide.

**Steering during a long run**, when a message arrives mid-task and the agent
either ignores it or abandons everything:

    A message that arrives while you are working is steering for the current
    task, not a replacement for it, unless it clearly cancels the task or asks
    for something incompatible. Fold corrections, constraints and questions into
    the work in progress and keep the original objective. If it is a question,
    answer briefly and carry on.

**After compaction**, when the window is summarised and the agent restarts from
zero or treats the summary as a new brief:

    Compaction does not end the task. Continue from the summarised state, treat
    the most recent user message as the latest steering rather than a new
    objective, and make reasonable assumptions about what the summary dropped.
    Do not redo completed work or repeat updates you already gave.

**Context budget anxiety**, when the model truncates its work or proposes a fresh
session as the window fills. In a harness that compacts or persists state, say so
explicitly, because otherwise the model is right to be cautious:

    Your context window will be compacted automatically as it approaches its
    limit, so you can continue from where you left off. Do not stop early on
    account of token budget. As you approach the limit, save your current
    progress and state before the window refreshes, then continue.

If the harness does neither, the honest version is shorter: "You have ample
context remaining. Continue the work." Better still, stop showing the countdown
to the model if the harness allows it.

**Final-summary readability**, when after many tool calls the model writes in
shorthand the user never saw:

    Terse shorthand is fine between tool calls. Your final summary is different:
    it is for a reader who saw none of that. Open with the outcome in one
    sentence, then the supporting detail, then the one or two things you need
    from them. Drop the working vocabulary you built up unless you reintroduce
    it. Write complete sentences and give each file, commit, or flag its own
    plain clause. If you have to choose between short and clear, choose clear.

## Work spanning multiple context windows

Work that cannot finish in one context window is a different problem from a long
single session. A single prompt repeated per session fails it in two
characteristic ways: the first session tries to one-shot the whole thing and runs
out of context mid-feature, and a later session looks around, sees progress, and
declares the job done.

When the task spans sessions, write two prompts.

**Initializer prompt**, for the first context window only. Its job is to build
the environment every later session relies on, not to build the product:

- a structured feature list, one entry per end-to-end user-visible behaviour,
  each marked as failing at the start. Use JSON rather than Markdown, because
  models are markedly less willing to quietly rewrite a JSON file.
- **Dependencies filled in, not just declared.** If the schema has a
  `depends_on` field, the initializer prompt must instruct that it be populated
  for every entry, and the acceptance check must verify that entries which
  obviously build on others are not left with an empty list. This is the
  failure that looks like nothing: a schema showing `depends_on: []` in its
  example produces a file where every entry has an empty list, the worker's
  selection rule silently never applies, and the work gets built in list order.
  Marking a country on a globe gets attempted before the globe renders.
- a startup script, so no later session has to rediscover how to run the thing
- a progress file and an initial commit

**Worker prompt**, for every subsequent window:

- start by reading the progress file, the commit log, and the startup script,
  then smoke-test the current state to catch undocumented breakage. **Bound the
  smoke test explicitly**, to a named critical path plus the most recently
  completed item. An unbounded "check everything that passes" is cheap at three
  features and eats an entire session at twenty, which is precisely when the
  agent starts skipping it without saying so.
- pick exactly one feature from the list and do only that
- edit the feature list only by flipping a status field. Say plainly that
  removing or rewriting entries is unacceptable, because it silently shrinks the
  definition of done.
- flip a status to passing only after verifying end to end the way a user would
- end by committing with a descriptive message and writing a progress update
- **Give partial progress somewhere to go.** Some items are too large for one
  window however carefully the list was cut, and a rule of one item per session
  with no escape hatch turns that into a session with no recorded outcome. State
  what to do instead: commit the partial work on its branch, leave the status
  failing, and write down in the progress file what is done, what remains, and
  what the next session should pick up. An item that resists two sessions in a
  row is a sign it should be split, and the prompt should say so.

The pair costs more to write than one prompt and is the difference between an
agent that finishes and one that plateaus. Raise it whenever the user describes
work measured in days rather than hours.
