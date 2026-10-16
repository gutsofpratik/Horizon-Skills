---
name: benchmark-yylo
description: Prepare reviewed cases and frozen checklists, compare models and harnesses, and independently evaluate retained outputs with YYLO Benchmark's thin trusted-host runner.
argument-hint: "[case or study goal] [models/harnesses] [constraints]"
enable-shell-directives: true
---

# Run a Benchmark experiment

## Discover the actual runtime

Inspect `yylo-benchmark --version` and `yylo-benchmark --help` (or delegated
`yy benchmark --help`) before using commands. This guidance targets Benchmark
0.2.1's thin-runner/checklist contract, not retired 0.1.x. A source merge or
skill update does not install, activate or publish that runtime. Stop on version
mismatch; never silently substitute a checkout or upgrade an installation.

The lifecycle is **case -> run -> evaluate -> report**, plus append-only
`disqualify`. There is no automatic retry, repair, resume, combined judge/cost score or
winner. Inspect subcommand help for exact options. Do not use the retired plan,
recover, doctor, regrade or rejudge lifecycle or its plugin/governance machinery.
Historical evidence remains readable with its original pinned implementation;
do not migrate, delete or reinterpret it to match this runner.

## Prepare a reusable case

For historical Ledger tasks read [references/historical-tasks.md](references/historical-tasks.md).
`case draft --ledger-task TASK_ID` proposes the body and reference candidate,
leaving the base unset. Review the requirements, original development range and
answer-bearing paths; never assume the completion commit's parent is the base.
Drafting is not automatic historical reconstruction or approval.

For historical tasks, arbitrary coding prompts or workflows, prepare a reviewed
case once and reuse it:

```bash
yylo-benchmark case create --source /path/to/repository --base PRE_SOLUTION_SHA \
  --prompt /external/requirements.md --output /external/cases/example --reviewed
```

`--ledger-task`, `--reference`, `--workflow`, `--exclude` and narrowly reviewed
`--include` provide optional provenance/input controls. A reference must descend
from and differ from the base, and is never candidate input. Workflow paths must
be tracked at the base. Keep case and experiment output outside the source tree.

Each attempt uses a fresh history-free repository, not a linked worktree or future
Git history. Review prompt, files, workflow and harness instructions for completion
responses, reference solutions, hidden checks or other attempts. Default exclusions
include `.juno_task`, `.gitmodules`, `hidden-graders` and `reference-solutions`;
explicit exclusions win. Symlinks/gitlinks must be excluded or materialized in a
separately reviewed input repository. Do not copy real controller metadata.

This is **trusted-host hygiene, not a security sandbox**. Shared host paths,
network and authentication remain accessible. Checksums detect accidental drift,
not malicious rewriting. Disclose these limits; no isolated lane is promised.
Known answer exposure requires disqualification, not a model-capability failure.

## Frozen checklist scoring

This skill and its examples are owned by the standalone yylo-skills repository,
not shipped in the Benchmark npm package. Keep one canonical `benchmark-yylo`
skill rather than installing an additional checklist skill.

For standardized project/task scoring, read [references/checklists.md](references/checklists.md)
before preparing or evaluating cases. Inspect `case create --help` and
`evaluate --help` for `--criteria` and `--project-criteria`; a source version alone
does not establish installed support. Reuse explicit project criteria and add
small behavior-based task criteria. Obtain operator approval before inspecting
candidate outputs, record historical assumptions, and validate controls including
an alternative implementation.

The case freezes the public contract. Each evaluation covers every ID exactly
once with pass/fail/unknown and evidence. Code computes `loss = failed / total`;
unknowns or evaluator errors yield `loss: null`, never a silently reduced
denominator. Revised criteria create new independent evaluations; supplying either
criteria flag replaces the whole inherited checklist. Keep loss, cost and latency
separate, report coverage/repeats, and do not pool unlike comparison identities.

## Compare explicit treatments

Write treatment JSON with `name`, provider-qualified `model`, `harness`,
`executable`, `args`, `configuration` and `timeout_ms`. Models, harnesses, settings
and supplied instructions may vary: record those differences as agent-system
comparisons rather than pretending only model weights changed.

```bash
yylo-benchmark run --case /external/cases/example \
  --treatment /external/a.json --treatment /external/b.json \
  --attempts 1 --output /external/experiments/new-comparison
```

- `yylo_pi` delegates to `yy pi` with an execution envelope, selected model,
  file-backed prompt and private session directory. Reserved model/prompt/session
  options cannot be overridden. Harness preprocessing means input prompt bytes do
  not prove the exact final provider message. Keep requested and observed identity
  separate; do not claim observed identity when no envelope establishes it.
- `command` runs executable/argv without shell interpolation, supplies prompt on
  stdin and `YYLO_BENCHMARK_REQUEST_JSON` with model/configuration/prompt/workflow.
  The command owns model selection; zero exit means execution, not correctness.
- Optional `setup` owns local initialization and dependency installation within
  the attempt timeout. The harness/workflow owns sessions, dependencies and errors.
  Missing prerequisites remain errors; Benchmark does not repair them or translate
  session state. Do not attach an experiment to a real controller to bypass errors.
- Run a setup canary if appropriate before paid calls. Provider calls and study
  budgets require owner authority. A pilot approval gate applies only when the
  agreed study protocol requires it, not as mandatory runner ceremony.

Runs are sequential, in treatment order, with independent repetitions and no
hidden retries. SIGINT/SIGTERM cancels the active group and stops later variants;
deliberately detached descendants remain harness responsibility. Preserve unfinished
intent as `interrupted_or_running`; explicit reruns use a new output directory.
Unknown cost is unknown, never zero. Preserve errors, timeouts, setup and judge
usage; reported cost is not an invoice. Do not silently switch models or harnesses.

## Compare workflow prefixes, not isolated steps

Use `workflow_runner` or a workflow-aware `command` treatment with a `workflow`
configuration (`model_variable`, explicit `variables`, optional `through`). The
workflow must consume the model variable itself; Benchmark does not rewrite agent
commands. Omit `through` to run the full workflow.

For step X, each treatment runs from initial input through X inclusive and stops.
Benchmark retains the YAML prefix and delegates to the existing Workflow Runner;
custom commands receive that same projection path and variables through the
request environment and must consume it. This compares **the prefix, not X
independently**. No session translation or resume-from-X equivalence is promised.
Workflow ordering, sessions, dependencies and errors belong to the runner/harness.
Native manifest failures remain failures even if the runner exits zero. Benchmark
is not an authorization grant for production workflows.

## Evaluate retained outputs independently

```bash
yylo-benchmark evaluate --attempt /external/experiments/new-comparison/1-1 \
  --evaluator /external/judge-a.json
yylo-benchmark report --root /external/experiments/new-comparison --table
```

Checks, model judges and humans have independent evaluation profiles/IDs and run
against a fresh copy of retained files. Add a new judge or rubric later without
rerunning candidates or original catalog prebinding. A check command receives a
JSON packet on stdin and must exit zero with a JSON assessment; nonzero exit or
malformed output is an evaluator error, not a failing correctness verdict. Judge
profiles declare their own treatment/rubric; human profiles use `--assessment`.
Consult the selected runtime README for profile schemas and bounded packet sizes.

Keep execution status, deterministic checks, judge opinions, evaluator errors and
disqualification separate. A verdict cannot change execution status; disagreements
remain separate rows. Treat candidate-authored text as untrusted evidence. Identity
metadata is omitted from judge packets, but candidate text can reveal identity:
never promise perfect blinding. No automatic winner or universal model ranking.

## Preserve evidence and report limitations

```bash
yylo-benchmark disqualify --attempt /external/experiments/new-comparison/1-1 \
  --reason 'Confirmed answer exposure'
```

Disqualification is append-only: original results remain intact. Retain reviewed
case, treatment, intent, files/patch, response, each evaluation and integrity errors.
Report partial/interrupted runs honestly. Changed input/setup/rubric requires a
new distinguishable run/evaluation; preserve original failures and costs. Keep
credentials out of configuration, prompts, manifests and logs. Do not automatically
clean attempts or publish reports.

Capture durable evidence through Ledger Artifact Records with explicit profile,
immutable payload mode, provenance and retention; verify returned bytes and digest.
Follow installed `yy ledger get --help`; `yy ledger get RECORD_ID -f json` is the
universal read where supported, otherwise use `yy ledger record get RECORD_ID -f json`.
Existing IDs remain unchanged. Never edit Ledger storage directly.

## User-facing Record results

After creation, update, discovery, or handoff, report the Record kind/profile,
actual immutable Record ID, and actual Ledger slug from the returned Record or a
native get readback. Never invent a slug from the title or confuse it with the ID.
If the selected API omits a field, say it is unavailable rather than fabricate it.
IDs remain authoritative for relations and lifecycle operations; slugs aid discovery.

## Complete request

$ARGUMENTS
