# benchmark-yylo

Prepare reviewed historical-task, prompt and workflow cases; compare models,
harnesses and configurations; independently evaluate retained outputs using
YYLO Benchmark 0.2.1's thin trusted-host runner.

Read [SKILL.md](SKILL.md), the [historical preparation guide](references/historical-tasks.md),
and the [checklist scoring guide](references/checklists.md). Reusable
[project](examples/project.yaml) and [task](examples/task.yaml) criteria and a
[synthetic assessment](examples/assessment.json) live here with the skill—not in
the Benchmark npm package. Keep one canonical `benchmark-yylo` skill for YYLO
Benchmark, independently acquired/released through `yylo-dev/yylo-skills`.
The lifecycle is case -> run -> evaluate -> report, plus append-only disqualify.
Workflow step comparisons measure prefixes, not isolated steps. Execution, checks,
judge opinions and errors remain separate; there is no automatic winner.

Inspect installed help/version first. Skills 2.1.1 and Benchmark 0.2.1 source changes
do not imply a published release or installed upgrade. No security sandbox,
automatic repair, session translation or mandatory pilot ceremony is promised.
Study-specific approval gates still apply. Publication and live provider calls
require separate authority. Discover checklist support through installed
`case create --help` and `evaluate --help`, not just a version number. Checklist
loss is `failed / total`; unknowns/errors are unscored. Costs and latency remain
separate, and retrospective criteria revisions never rewrite earlier evidence.
