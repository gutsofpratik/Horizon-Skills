# The content-drift leg

Operational content drifts apart: a runbook restates tool mechanics a skill owns and
the copies diverge; a procedure names a lever that was replaced; a doc points at
another doc that no longer carries the fact. Each copy looked right when written. This
leg finds the drift across every content pair — runbook↔skill, skill↔skill,
architecture↔runbook — and routes each finding, without editing anything.

It reads whatever corpora the session can reach: the workspace's runbooks,
architecture docs, and plugin skill trees, plus plugins via `extension_plugin_list`.
Where a corpus is out of reach, the report says which pairs went unchecked.

## The checks

Work per system (the pipeline, the database, the queue), pairing every artifact that
speaks about it. Where the session can delegate, fan the systems out to sub-agents —
one per system keeps each reviewer's reading load honest; otherwise work them
serially.

1. **Restated subjects.** A runbook or doc explaining a skill's subject — how to call
   its tools, what null versus zero means, a generic flow — holds a second copy that
   drifts. The jurisdiction test is the runbooks skill's format ("a skill owns one
   system's tools and result semantics; the runbook owns the symptom, thresholds, and
   decision"); apply it, don't restate it. Compare the copies before reporting: where
   they already disagree, say which is current — the divergence, not the duplication,
   is the finding's severity.
2. **Dead levers.** Every flag, gate, tool, and command that procedural content tells
   a responder to reach for, verified against what exists: search the codebase where
   the session has one, check tool listings, ask the user for what neither can reach.
   A lever that no longer exists is the leg's highest-severity finding — someone
   reaches for it mid-incident and finds nothing. Report what replaced it when the
   verification turned it up; never guess a replacement.
3. **Stale pointers.** Ownership disclaimers ("X is owned by <doc>") verified that the
   named home actually carries the content; format docs that cite a file as their
   worked model verified that the exemplar still models the rule. A pointer to a home
   that doesn't hold the content strands the only real copy wherever it happens to
   live.
4. **Orphaned generic content.** Skill-shaped content — one system's tool contract,
   result semantics, a generic interrogation flow — living inside a runbook, where no
   skill owns the system at all. That's an extraction candidate: a brief proposing the
   new skill and what the runbook keeps, never an extraction performed here.

## Routes

| Finding | Route |
|---|---|
| Restated subject, copies agree | trim-and-chain brief → the `runbooks-author` skill's maintain job (or the owning doc's editor) |
| Restated subject, copies disagree | same brief, led by which copy is current — severity from the disagreement |
| Dead lever | a correction brief naming the verified replacement, or "replacement unknown — verify before editing" |
| Stale pointer | fix brief for whichever end is wrong: repoint, or move the content home |
| Orphaned generic content | extraction brief → the `skill-authoring` skill's create job |
| Pair unverifiable from this session | reported in "Not readable from this session" |

## Rules

- **Propose-only, like every leg.** The report carries briefs; nothing is trimmed,
  repointed, or extracted in this run.
- **Verify both copies before alarming.** A passage that looks like a restatement may
  be a deliberate one-clause use of a neighbouring fact — the runbooks format
  sanctions those. Quote what you compared.
- **Verify against what agents actually receive.** A local checkout can lag the
  branch the plugin syncs from; verify anchors and levers against that branch and the
  live tool listings, and say so when the checkout you read from is behind it.
- **Scale to the estate.** A first run on a large corpus reports the worst systems and
  says what it didn't cover; "checked everything, found nothing" from a run that
  plainly couldn't have checked everything is the report style this skill exists to
  prevent.
