# The extensions leg

Plugins and their skills, checked end to end. Needs the incident.io connection's
extension tools (`extension_plugin_list`, `extension_skill_feedback_list`); without
them, this leg reduces to asking the user to read the dashboard's Extensions page and
the per-plugin feedback panels, and recording what they report.

Work per plugin, in this order — each check feeds the next.

## 1. Sync state

`extension_plugin_list`: check sync first, because nothing downstream of a broken
sync is current — the report still orders findings most-actionable first, wherever a
sync problem ends up ranking. A `last_synced_at` far in the past on
a plugin whose repository changes often is worth a line too: agents may be following
stale instructions. Route: the error text usually says whether it's the repository
(fix there), the tree (a skill-authoring brief), or access (a dashboard page).

Match a local tree to an account plugin by repository source, branch, and skill set,
not by display name alone. If they differ, treat them as separate versions. Account
feedback describes the mounted version; do not use it to create a brief against the
local tree unless its exact file and quote verify there.

## 2. Are the skills earning their loads?

`extension_skill_feedback_list(plugin: "…")` per plugin — but read `usage_count`
against `assessed_count` before you read the funnel at all. Three corrections first:

- **The funnel only counts loads that have been assessed.** A skill loaded but not yet
  assessed reads `{followed: 0, not_used: 0, partial: 0}`, which is what a skill nobody
  ever loaded reads too. Compare `usage_count` to tell them apart. Assessment waits on
  the run's scorecard, and a production scorecard waits on the incident closing, so a
  young skill's funnel is usually just behind.
- **These numbers cover two surfaces: investigations and chat.** A skill the team runs
  in a coding agent on their own machines records nothing here. Its zero tells you
  incident.io's agents never loaded it, and nothing more. Check what a skill is for
  before calling it unused.
- **Count the chances before you call a count low.** Take the moments the skill could
  have served in the same window, and compare it against a skill of a similar age.
  Five loads is damning beside fifty opportunities and unremarkable beside six.

Then the funnel:

- **In step 1's skill list but absent from the feedback** — never loaded. Either the
  description never matches real requests (a skill-authoring brief: rewrite the
  trigger) or the skill serves a moment that has not yet occurred; say which is
  more likely from its description, and don't manufacture urgency about a young
  skill.
- **Loaded but never assessed** (`usage_count` above zero, `assessed_count` zero) — the
  skill hasn't been graded yet. Report it that way, instead of reporting the empty
  funnel as a result. Where it persists across reviews, the loads are probably
  unassessable — a run with no check, or one whose traces have aged out. Report that
  too: a skill nobody can grade never builds up the feedback an improvement needs.
- **Loaded much, followed little** (high `not_used`) — the description over-promises.
  Brief: tighten the description to what the body delivers.
- **Followed but not helping** (`hurt` or persistent `neutral` contributions) — the
  instructions take runs the wrong way; the highest-severity skill finding there is.
  Brief with the examples the feedback carries.
- **Healthy funnels get a healthy line.** Name the skills that are working; the
  report reads as a review, not a complaint. A healthy funnel on a plugin whose sync
  is failing gets its credit with the caveat: the feedback describes the mounted
  version, not what's in the repository now.

## 3. The issues worth acting on

Issues arrive most-actionable-first, but doctor's job is triage, not transcription:

- First, check the plugin's repository for prior reports. No directory holds them: the
  skills that write one offer a dated file anywhere in the repository, or the pull
  request description. So search for the headings they use — `# Estate review`
  (doctor) and `# Estate report` (extensions) — and read the
  pull requests where the session can. They record what earlier runs proposed and what
  the team declined, and a declined issue is reported differently below. Where the
  record is kept is [report.md](report.md)'s cadence section.
- **An empty search is not evidence that nothing was declined.** Report that no prior
  record was found, and report separately that pull requests were unreadable, where
  they were. Neither supports the "previously declined" label.
- Verify each issue's anchor (`target_file`, `target_quote`) against the plugin's
  current tree before reporting it — apply the "Read the feedback with these
  corrections" section of the `skill-authoring` skill's improve reference, including its
  distrust of `likely_resolved` (the rest of that file is edit-mode material; doctor
  stops at the brief). An issue that verifies becomes one line in a brief; an issue
  that doesn't is noted as probably stale, not escalated. If either anchor is absent,
  report that the issue could not be verified; do not infer an anchor from similar
  local text.
- Cluster by skill: one brief per skill carrying its verified issues — each with its
  `issue_key`, which the improve job uses to anchor its pre-ship verification to the
  recorded problem — and the strengths that must survive the fix, ready to hand to
  skill-authoring's improve job.
- An issue the team has already declined (a dismissal recorded over
  `extension_skill_feedback_update`, or a won't-fix note in the plugin's repository
  or pull requests) is reported once as "previously declined — still recurring", not
  re-escalated every run. Dismissed issues leave the feedback by default, so make one
  pass per review with `include_dismissed` — without it, a recurrence of a declined
  issue is indistinguishable from a new one, and the report can't honestly use the
  "previously declined" label at all.

## 4. Feedback orphaned by renames

A skill whose feedback says it isn't in the current version was renamed or removed —
which one is usually undecidable from the data, so ask the user rather than guessing.
Removed and meant to be: fine, one line. Renamed: its history no longer informs the
new directory — worth a line so the team knows the rename reset the skill's track
record, and a caution against repeating it casually.

## 5. Convention drift

Spot-check each plugin's tree against the `skill-authoring` skill's format reference —
this is a sample for
the report, not a full audit:

- Every skill directory registered in the plugin README's skills table; connections
  the skills call present in its connections table. Where the repository itself says a
  directory is left out on purpose, that is not a finding — check before reporting one.
- No client-prefixed tool names or single-environment invocation syntax in skill
  bodies — these break the skill in environments the feedback may not cover.
- References that nothing links to.
- Skills with no provenance stamp (`metadata.incident-io-plugin-version` in the
  frontmatter), or stamped with a version well behind this plugin's own (skip this
  comparison when this plugin's version can't be read). A stamp of `"mcp"` counts as
  stamped and has no version to compare: never flag it as either. Plugin list
  entries report each skill's `authoring_plugin_version`, so this needs no tree read.
  An unstamped skill was written by hand or by another tool; a stale stamp means the
  authoring guidance has moved on since it was last touched. Neither is a defect on
  its own — route it as a brief for the improve job, which refreshes the stamp as it
  goes, and rank it below anything the feedback says is actually going wrong.

Drift becomes part of the per-skill brief where one exists, or a small standalone
brief where the skill is otherwise healthy.

## What this leg does not do

Edit, re-sync, or dismiss. Where a fix is obvious, the brief says exactly what to
change — and stops there.
