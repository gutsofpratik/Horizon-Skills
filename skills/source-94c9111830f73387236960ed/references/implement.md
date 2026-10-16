---
description: Implement exactly one assigned Kanban task in its admitted Bolt product worktree and stop after queueing it.
---

# Bolt implementation worker contract

An implementation worker owns one explicitly assigned task. It does not select
other work, mutate the product target, merge, release, deploy, or clean another
task's workspace.

## Execution boundary

The external agent performs implementation, tests and commits. The CLI owns
workspace preparation, deterministic finish and safe integration, not model
implementation or automatic retry/repair. Task run/resume and implementation
budget recovery are retired. `yy watch status|await|follow RUN_ID` is an optional
read-only observer of existing evidence; it never launches or cancels producers.
A process exit or captured answer does not prove task completion. Continue an
existing admitted workspace only after verifying current ownership; preserve
historical runs and never replay/reset them automatically.

## 1. Resolve and preserve admission

1. Read `AGENTS.md` and the complete assigned task from the canonical controller.
2. Run `yy task start TASK_ID` unless the handoff already contains the matching
   active Bolt task record. Verify the returned worktree, branch, full target ref,
   and exact base SHA before editing; stop on missing or contradictory evidence.
   Retain the returned fencing token privately for manual gated commands.
   Confirm passed, current exact-lock hydration before editing or testing; stop
   if hydration is missing, stale, failed, or leaves the worktree dirty.
3. Work only in that product worktree. Never edit product files in the controller
   or copy controller ledgers, specs, state, or artifacts into a task worktree.
4. Preserve controller identity and workspace-role checks. Controller checkpoints
   are best-effort local durability warnings after terminal metadata is durable;
   they are not product inputs or lifecycle gates.

## 2. Implement

1. Edit only requested product paths and preserve project sources of truth.
2. Use focused affected tests in the edit loop. Other feature worktrees may run
   concurrently; do not wait for or modify them.
3. Tests and semantic reviews are explicit project checks outside merge. Follow
   the project's authorized validation policy; native delivery launches no models,
   selects no reviewers, schedules no suites, and owns no repair loop. Never
   claim checks occurred merely because a task was queued or landed.
4. If blocked, record bounded truthful state and stop without claiming success.
   Durable diagnostic output belongs in a verified Ledger Artifact Record when
   the installed API supports it; otherwise preserve an external draft and stop,
   never fall back to product documentation or direct controller-store edits.

## 3. Queue and hand off

1. Run focused tests, required dangerous-path checks, parity checks, and
   `git diff --check`.
2. Stage only task-owned paths, commit coherently, and leave the worktree clean.
3. Optional read-only `yy task preflight TASK_ID` diagnoses admission; it is not
   a prerequisite. Repair admission, generated-output, runtime, or closure
   refusals while the task is still `WORKING`.
4. Run `yy task finish TASK_ID --lease-token <current-token>` directly after the
   clean commit. Finish independently enforces admission and configured validation
   of the immutable tip, then records `QUEUED`. Never log the token; expiry alone
   does not grant takeover authority.
5. Record the commit and bounded response in Kanban. A lifecycle finalizer may
   attempt a controller checkpoint after terminal metadata is durable; checkpoint
   failure remains a warning and must not change the task or merge outcome.

Stop after queueing. Read-only delivery observation uses `yy merge status TASK_ID`.
Only the target owner runs `yy merge land TASK_ID`, which uses native Git and an
expected-old ref update, then projects Ledger automatically. If Git integration
succeeded but Ledger projection did not, retry only `yy merge project TASK_ID`;
Git stays integrated and projection recovery does not repeat integration.
Recompose and recheck after target movement; preserve private conflicts.
Implementation agents do not poll, steal authority, discard dirty bytes, or
mutate the target. Historical task bodies and acceptance records are evidence,
not current execution policy.

Release-version changes use this same ordinary task/merge lifecycle. Package
preparation is maintainer-only and outside `yy`. Never create a tag, push,
publish, deploy, mutate production, restart services, run post-deploy E2E, or
clean worktrees without separate authority.
