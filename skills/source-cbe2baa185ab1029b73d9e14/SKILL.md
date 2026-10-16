---
name: prompt-engineer
description: Write, revise, debug or migrate a prompt, system prompt, agent instruction, subagent definition or brief, or skill file, and get the test cases that prove it works. Use it when a prompt got worse after a model change, when an LLM has to do a task reliably or at volume, when drafting text for another model, and when structuring a multi-step build or briefing a subagent. Triggers even when the word "prompt" never appears.
---

# Prompt Engineer

Produce a ready-to-use prompt that maximises output quality on the target model,
plus the means to tell whether it works. A prompt nobody can test is a draft.

Aim for the smallest set of high-signal tokens that fully specifies the expected
behaviour. Minimal does not mean short. It means nothing redundant and nothing
the model already does well by default.

## Step 1: is a prompt the right artifact?

In an agent harness the same instruction can live in several places, and the
place decides whether it takes effect at all. Route before writing.

| The user needs | Produce |
|---|---|
| A one-off or parameterised task | A prompt. Continue below. |
| Something that must happen every time, no exceptions | A hook. Config files are advisory; hooks are deterministic. |
| Reusable domain or workflow knowledge across sessions | A skill. |
| Its own context window, restricted tools, or independent review | A subagent. |
| Always-on project guidance | A project config file, kept short. |
| A workflow with side effects that should only fire on request | A skill that is not model-invocable. |

Two signs the user asked for the wrong thing. They describe a rule using "always"
or "never" and want it in a config file, which means they want a hook. Or they
ask for a prompt they clearly intend to paste again next week, which means they
want a skill, and writing it as a prompt guarantees it drifts across copies.

Say which artifact you are producing and why in one line, then produce it. If it
turns out to be a skill, subagent, hook, or config file, the token economy in
this document does not apply: those are governed by progressive disclosure and
by discovery. Say so rather than writing a prompt in the shape of the wrong file.

**Routing is a decision, not a remark.** Naming the right artifact and then
building the one that was asked for is the most common way this step fails, and
it fails invisibly, because the response reads as thoughtful. Two rules close
it:

- The routed artifact is the deliverable, produced in full. Not described, not
  sketched, not left as "you could turn this into a skill by adding
  frontmatter". If a skill is the answer, write the SKILL.md.
- If the user also has a real use for the form they asked for, portability to
  another model being the usual one, that form is secondary, comes after, and is
  labelled as the export. It never replaces the routed artifact and never leads.

When the routing decision is wrong for a reason you can state, say the reason
and follow the request. Hedging by delivering both with the requested form
leading is not a decision; it hands the choice back to the user without the
information they would need to make it.

Full detail: `references/artifact-routing.md`.

## Step 2: establish the inputs

Infer anything the user did not supply, state the inference, and continue. Do not
interrogate them for values you can reasonably assume.

- **Target model and its effort or reasoning setting.** These are one input, not
  two. The setting changes the class as much as the model does. If unknown, write
  for Class 1 and note what to change for the others.
- **Output language**, if the prompt's output must be in a different language
  from the prompt itself. Models default to matching the prompt, so this has to
  be stated explicitly when they differ.
- **Mode**: `create`, `revise` (an existing prompt), `migrate` (an existing
  prompt moving to a different model), or `execute` (the person asked for the
  work itself, and you are using this skill to structure your own execution and
  to brief subagents). In `execute` mode the deliverable is the work, not a
  document about the work. See `references/self-and-subagents.md`.
- **Deployment**: chat UI, API call, or agent harness. This changes the delivery
  advice, not the prompt body.

## Step 3: work the mode

**create.** Classify the prompt type, because it determines the structure: a
reusable template that runs many times with variable inputs; an agentic build
prompt for a coding agent; or a one-off complex request. For agentic work, check
whether it fits in one context window or spans several, because multi-window work
needs a different structure entirely.

Then identify the task, the intended output, and who reads it. Choose a role only
if it meaningfully shapes the output. State assumptions rather than asking, unless
a wrong one would waste hours of agent work, in which case ask one targeted
question. Decide which sections the prompt actually needs. Omitting sections is a
quality signal, not laziness.

**revise.** Read the existing prompt against the anti-patterns and the target's
class. Produce a changelog first, one line per change, marked `removed`, `added`,
or `kept-despite-appearances`, each with its reason. Never silently rewrite: some
odd-looking lines encode a requirement learned from a failure. If a line looks
like an anti-pattern but might be load-bearing, keep it and flag it for the user
to confirm rather than deleting it.

**migrate.** Do not rewrite the prompt first. Give the user this order and say why
each step is separate: switch the model with the prompt untouched, so the
measurement isolates the model change; re-establish the effort setting on the
new model by sweeping it, because neither copying the old label nor accepting
the new default preserves depth: vendors recalibrate what each level means
between versions, and defaults move even between point releases of one model
line; run the evals for a baseline,
and ship if it holds; only on regression tune the prompt, starting with verbosity,
format, and scope; re-measure after each single change, never bundling an effort
bump with a prompt edit.

## Step 4: write it

Use XML tags to delineate sections with distinct content types. Include only what
the task needs, in whatever order serves clarity:

- `<role>` specific and domain-contextualised, and only when it changes the
  output. Test each clause: does it tell the model something it must now do
  differently? Naming a domain does ("Next.js and PostGIS" narrows the library
  choices). Asserting experience does not. "You have built several of these
  from scratch to production", "senior", "with years of experience" are  <!-- lint-ignore -->
  flattery aimed at the model, and they survive review because they sound like
  context. Cut the clause and check whether anything about the output would
  change; if not, it was padding.
- `<context>` the larger goal, the audience, what the output enables
- `<task>` a clear imperative; numbered steps only for genuinely sequential work
- `<input>` variable data with `{{VARIABLE_NAME}}` placeholders
- `<success_criteria>` what a correct output looks like, in checkable terms
- `<constraints>` only those overriding default behaviour, each with its reason
- `<examples>` only when consistency demands them; 2 to 5 on a Class 1 target,
  more on weaker classes, see `references/examples.md` for the gradient and for
  what the set must cover
- `<output_format>` length, structure, required sections, output language

Four principles govern the wording.

**Right altitude.** Avoid brittle if-else rules on one side and vague guidance
that assumes shared context on the other. Modern models follow one short
principled instruction better than ten rules covering individual cases.

**Give the reason, not only the rule.** "Never use ellipses, because the output is
read by a text-to-speech engine." Models generalise from the why; bare rules
invite misapplication.

**Define success, not just the task.** "Good performance" is not a criterion. "The
extracted field matches the source on at least 95 percent of a 200-item holdout
set" is.

**Show the target, don't forbid the miss.** Positive examples of the desired
behaviour beat descriptions of what to avoid, and negations are unreliable on
smaller models. Use examples when format, tone, or style consistency across many
runs matters; skip them on open-ended creative or analytical work, where they
anchor. Once you have decided to use them, `references/examples.md` covers
coverage, ordering, and the rules that decide whether a set works.

For the class-specific rules, read `references/model-classes.md`. For agentic and
multi-context-window prompts, read `references/agentic-prompts.md`. For API and
harness delivery, read `references/delivery-mechanics.md`. When the task is your
own work or a subagent brief rather than a prompt for someone else, read
`references/self-and-subagents.md`.

## Unattended output needs an uncertainty signal

When a prompt's output is consumed by a system rather than read by a person,
extraction into a database, classification into a queue, routing, scoring, the
schema needs a field that says the model was unsure: `confidence`, or a boolean
`needs_review`, plus the rule for when to set it.

Without one, a wrong value is indistinguishable from a right one. At three
thousand items a day nobody re-reads the output, so an unflagged error is acted
on silently. This is the same rule as "no silent fallbacks" in
`references/agentic-prompts.md`, one layer down: a confidently wrong field is a
silent fallback wearing a schema.

State the threshold behaviour too, since the field is useless without it: what
happens to a flagged item, which queue it lands in, and who looks at it. If
nobody will look at it, say so and drop the field rather than shipping a
decoration.

## Step 5: make it testable

Every deliverable ships with a way to check it, sized to the stakes. A chat
one-off needs three inputs; a template running thousands of times a day needs a
seed set, a stated set size, and a grading method. Anything that enforces a rule
needs a case that attempts to bypass the rule and is expected to fail, because a
rule tested only with compliant input is untested.

`references/evaluation.md` has the sizing table, the method for growing a large
set from a hand-written seed, the classification rules, and a worked seed-set
example. Read it before writing test cases; the counts there are prescribed
rather than left to judgment, because "write some test cases" reliably produces
three that all pass.

## Anti-patterns

<!-- lint-disable: prefill, vague-quality, undated-model, filler-role -->
This section names anti-patterns in order to remove them, so the linter's own
checks would fire on the descriptions. That is what the waiver above is for; the
same directive is available to any prompt that legitimately needs a flagged
phrase.

Remove these on sight, including when revising someone else's prompt:

- Instructions telling a reasoning model to reproduce its reasoning in the
  response. This has moved from wasteful to failing: current models can decline
  it outright as a reasoning-extraction request. Conversely, missing
  chain-of-thought guidance on non-reasoning models for complex tasks
- Forcing a tool call (`tool_choice` set to `any` or to a named tool) as a way to
  guarantee output format. Claude Sonnet 5.5 rejects it with a 400, and Opus 5.5
  is reported to as well. Keep
  `tool_choice` at `auto`, use strict tool use for the shape, and say in the
  prompt when the tool applies
- Prefill-based tricks. On Claude these are unsupported from 4.6 onward and
  return a 400; other providers differ, so check before ruling it out elsewhere
- Prompt-text JSON enforcement where structured outputs or a strict tool schema
  exists; and conversely, schema constraints the API cannot express
- Long source documents placed below the instructions
- Roles asserting experience, seniority, or excellence rather than domain
  ("you have built several of these", "world-class", "senior"), and any other
  motivational padding
- Constraints restating model defaults ("be accurate", "be helpful")
- Verbosity control written entirely as prohibitions
- Exhaustive rule lists where one principled instruction suffices
- Sections included because a skeleton has them
- Examples that anchor open-ended creative work
- Vague quality words without measurable criteria
- Personal details about the requester that do not change the work (age,
  location, employer) in a prompt that will be committed or pasted repeatedly.
  Keep what constrains the build, such as skill gaps that change what to
  recommend, and drop the rest.
- Model versions hardcoded into reusable templates without a date
- An unpinned effort setting on a model that exposes one
- Prompt edits proposed before a baseline exists, or several changes bundled into
  one measurement

## Bundled scripts

Two optional scripts, both plain Python with no dependencies.

`scripts/lint_prompt.py <file>` checks a prompt against the mechanically
detectable anti-patterns above: reasoning-reproduction instructions, prefill
patterns, prompt-text JSON enforcement, roles asserting seniority or experience,
vague quality words, undated model names, prohibition-heavy phrasing, and a
sentinel value that is permitted in one line and called an error in another. Run it
before reviewing a prompt by hand, because the grading ladder puts code before
judgment and every finding it catches is one you no longer have to spend
attention on. It sees only what a regex can see; altitude, whether constraints
carry their reasons, and whether examples anchor creative work stay with you.
Pass `--class 2` or `--class 3` to enable the class-specific checks.

Fenced code blocks are scanned by default, because a prompt handed over for
review is nearly always pasted inside one; stripping them lints the prose
around the prompt instead of the prompt. `--docs` inverts that, since fenced
blocks in documentation are quoted examples of the patterns being explained.
`--scan-code` and `--skip-code` override either default.

Pass `--docs` when the file is documentation *about* prompting rather than a
prompt: six of the checks fire on merely naming a pattern, and linting prose
about an anti-pattern as if it were one is a category error. Do not reach for it
to quiet a real finding; it disables those checks wholesale. The model-name
check stays live in both modes, because documentation is the first thing to go
stale, and it is satisfied by recording a date rather than by an exemption.

`scripts/lint_all.sh` runs every prose file the skill ships in the mode that
fits it, and validates the two JSON files structurally.

`evals/run_evals.py` runs the cases in `evals/evals.json` against the API and
grades each output in two layers: regex assertions for structure, and a rubric
graded by a second model for anything that needs judgment. Two of the cases test
triggering, which no API call can reproduce, so it prints those as a manual
checklist instead of pretending to run them.

`scripts/build_system_prompt.py` flattens this skill into a single system prompt
for platforms that genuinely have no skill mechanism. ChatGPT and Codex are not
among them: they read the same agent-skills format, with the same progressive
disclosure, so the skill directory works there unchanged. Reach for the
flattener for plain chat interfaces, Gemini, local models, and any client that
cannot load skills. `--provider openai` drops the reference sections tagged for
Claude. It does not rewrite this file, so the provider-specific statements here,
such as the 400 errors in the anti-pattern list, survive the filter; each names
its scope inline.

## Response format

In `execute` mode none of the below applies: the person asked for the work, so
deliver the work. State the phases and their acceptance criteria in one short
paragraph before starting, then build. A structured plan is not progress; if
your turn ends with a plan and no tool calls, nothing happened.

For the other three modes:

1. **Analysis** (omit entirely for simple requests, and say nothing about having
   omitted it): prompt type, target class, effort recommendation, assumptions,
   and what you deliberately left out. This is an artifact for the user to review,
   not a reasoning trace.
2. **Changelog**: revise and migrate modes only.
3. **The prompt**: the deliverable.
4. **Test cases**, sized to how the prompt will run, per the table in
   `references/evaluation.md`. Three cases is the chat-one-off floor: one
   typical, one canonical edge case, one stressing the main constraint. A prompt
   that runs at volume needs a seed set and a stated set size instead, and a
   classifier needs per-class coverage with borderline items and a confusion
   matrix. Say plainly which of the two you are delivering; three cases is a
   smoke test, not a measurement. Then a one-line **failure signature** naming
   what a bad output looks like.
5. **Usage notes**: variables to fill, effort setting, delivery mechanics if
   relevant, and what to adjust first if results miss.

Keep analysis and usage notes short. The prompt is the product.

## Before finalising

Check that the result is the right artifact and not a prompt standing in for a
hook or a skill; that it matches its type in structure; that no two constraints
contradict each other, in particular over sentinel values such as `null`; that
machine-consumed output carries an uncertainty signal with a stated threshold
behaviour; that it states measurable success criteria; that it matches the target class and effort setting; that every
placeholder is a `{{VARIABLE}}`; that constraints carry their reasons; that it
ships with test cases; and that it would work for a capable new colleague with no
prior context.
