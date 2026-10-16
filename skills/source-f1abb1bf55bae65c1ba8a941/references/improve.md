# Improve a skill

Edit an existing skill, driven by evidence: assessment feedback from real loads, a
brief handed over by a review, or the user's own account of a skill misbehaving. The
discipline is the same in every case — verify the complaint against the current
content, fix without breaking what works, and confirm the fix shipped.

## Where the evidence comes from

incident.io assesses skill loads retrospectively: which skills agents loaded, whether
each load was followed, and whether following it helped. The rollup per skill is
available two ways:

- **In the session**, where the incident.io connection has it:
  `extension_skill_feedback_list(plugin: "…", skill: "<dir-name>")` — the plugin by ID
  or mount name (from `extension_plugin_list`), narrowed to the skill being improved.
  Returns usage counts, a funnel — `not_used` (loaded but shelved), `not_applicable`
  (engaged with, correctly judged not to fit), `partial` (partially followed),
  `followed` — contribution verdicts, and distinct issues and strengths,
  most-actionable first. Assessment runs only once a load's run is scored, so the
  assessed count trails the usage count; the funnel covers assessed loads.
- **In the dashboard**, on the plugin's page or the skill's own page, when the session
  lacks the tool.

Without either, work from what the user can tell you — but say the edit is unverified
against usage data, and don't invent a funnel.

A user often arrives with one issue copied from the dashboard: the plugin id and skill
dir name, the issue's summary, theme, suggestion and quote, and usually its `issue_key`.
Still load the full rollup for the skill and match the copied issue to its record by
`issue_key`, or by summary and quote when the key wasn't given.

The rollup doesn't link an issue to the loads that raised it. To see the runs behind
one, ask the same tool for `include: ["examples"]` with `example_contribution: "hurt"`
or use `extension_skill_usage_list` over the issue's `first_seen_at`/`last_seen_at` 
window for every load rather than a sample. Both are per skill, not per issue, so 
which of the returned runs raised this issue is an inference; say so when you rely on it.

## Read the feedback with these corrections

The feedback is computed, and its failure modes are known. Apply all of these:

- **Distrust `likely_resolved`.** The status is a verbatim check: it flips when an
  issue's quoted text is gone from the current content. Deleting the quoted line flips
  it without fixing anything. Before treating an issue as resolved, confirm both that
  the quote is gone *and* that what the issue asked for is now true.
- **Verify each issue against the current tree before editing.** An issue's
  `target_file` and `target_quote` locate the content it was raised against — which may
  have moved or been rewritten since. An issue whose anchor no longer exists may be
  fixed, superseded, or relocated; check before acting. `target_file` is relative to
  the plugin root, not the repository root: join it to the subpath in
  `extension_plugin_list`'s `repository` field to find it in a checkout, and confirm
  the checkout is the registered plugin before editing anything in it.
- **A skill marked not-in-current-version was renamed or removed.** Its feedback is
  historical: the issues can still be valid against the renamed files, but the anchors
  won't point at editable paths. Map them across by hand.
- **Read the funnel before the issues.** Many loads but few follows points at the
  description over-promising; follows that didn't help point at the instructions. The
  funnel tells you which kind of fix the skill needs — issue text tells you where.

## Make the edits

- **Only edit plugins the user's team owns.** Feedback exists for every connected
  plugin, this one included — but a vendored plugin isn't yours to change. Report the
  finding, with the issue's file and quote, for the plugin's owner instead.
- **Keep what the strengths credit.** Strengths exist so authors don't undo working
  behavior while fixing issues. Re-read them before restructuring.
- **Group related fixes into one coherent change** rather than one edit per issue —
  issues cluster on underlying causes, and the cluster usually has one fix.
- **Fix by the issue's `theme` field.** A `description_mismatch` lands in frontmatter; an
  `instruction_gap` in the body; a `capability_gap` needs a conditional path ("where
  the session lacks X, do Y") rather than pretending the capability exists — but first
  check `extension_connector_list` for whether the capability the issue wants is
  connected, missing, or withheld on purpose, and the issue's 
  `detail.candidate_integration` proposes what would help in the abstract without knowing. A
  `broken_reference` is either a link to remove or a missing reference to create:
  create it only from content you can verify or the user supplies — ask for that
  content when the reference was doing real work, rather than silently dropping the
  link.
- **Don't rename the skill's directory as part of an improvement.** The directory name
  keys feedback history and any allowlist — see [format.md](format.md). If a rename is
  genuinely wanted, make it its own change and call out what it resets.
- Hold every edit to [format.md](format.md) and [what-works.md](what-works.md) — an
  improvement pass is the natural moment to fix convention drift, but only where an
  issue or the funnel implicates it. Don't rewrite healthy sections for style. One
  class is always in scope: anything that breaks the skill in another environment
  (client-prefixed tool names, invocation syntax, assumed setup, one environment's
  query machinery assumed to be the only route). Fix those on sight; cosmetic
  convention drift — typography, bolding, table shapes — stays restraint-protected.
- **A corpus-wide convention pass is its own job**, distinct from improving one skill
  from feedback: apply the fix-on-sight class everywhere, hold everything else to the
  restraint rules, and where a format doc cites a skill as its model, check the
  citation still holds after your edits — exemplar references rot silently.

## Verify the fix before it ships

Where the session has the incident.io connection's `extension_verify`, test the edit
against the recorded problem before it lands. Anchor the run to the issue being
fixed: `extension_verify(plugin: …, changes: [{path, content}], reference_type:
"skill_feedback_issue", reference_id: <the issue's issue_key from the feedback
list>)`. The run mounts the issue — its summary, anchored quote, and suggestion — as
the verification's evidence, so no restated description is needed; add one only for
what the issue can't carry, like behavior that must not change. The changes are full
file contents overlaid on the synced version in memory; nothing ships. Poll
`extension_verify_show` until the status is complete.

A plugin is not the only way in. Which of the three routes you take is decided by where
the edit currently sits, so read your own state and take the one that matches.

**Pushed to a branch** — give the repository, the ref and a `mount_name`. No file
contents travel, because we read the branch ourselves, and a branch is the proposal
already so it needs no `changes` at all. A protected main makes this the common case:
merging is blocked, pushing is not.

**Uncommitted, against a plugin that already exists** — name the plugin and pass the
changed files as full contents, overlaid on its synced version in memory.

**In no repository we can read** — build the tar, call `extension_upload_url`, then pass
its `mount_name` alone. That tool's own description carries how to build the archive and
how long the URL lasts.

One case has a genuine choice rather than an answer: an edit that is *both* pushed and
has a plugin can go either way. Take the branch there, because it carries no payload.

All three anchor to a feedback issue the same way.

Read the report the way this file reads feedback — as computed evidence with known
limits:

- **A failure is the tool working.** Its `suggested_edits` are review comments
  anchored to file and quote: apply them, verify again. A round or two is normal.
- **Disagreement between identical runs is a wording defect.** When one of two runs
  of the same scenario reads your sentence differently, the sentence is ambiguous —
  fix it, don't re-roll.
- **`simulated_calls` and `real_calls` say how much the pass is worth.** A call in
  `simulated_calls` was imagined; one in `real_calls` reached a connected system and was
  really answered. A pass whose load-bearing step was simulated proves the skill routes
  to the right place, not that it works — set `live_connectors` to move reads into
  `real_calls` and find out. Writes are never made whatever you set, so a step that
  changes a system stays imagined.
- **Trims are safe to verify.** Deleting guidance the feedback's strengths credit is
  graded on whether the protection survives somewhere in the tree, not on one
  rehearsal going well — so a passing trim is meaningful, and consolidation doesn't
  have to be timid.
- **A pass proves the change does what you asked — never that you asked for the
  right thing.** Whether the fix belongs in this skill at all, and whether a claim
  it makes about an external system is true, are yours to check against the owner
  boundaries and the system itself; the verifier faithfully serves a misconceived
  intent.

Where the session lacks the tool, the fresh-reader road-test in
[create.md](create.md) step 5 is the fallback.

## Won't-fix is a valid outcome

Some issues describe accepted tradeoffs — behavior the team chose, flagged as a
problem by an assessment that couldn't know that. Don't edit the skill to appease the
metric. Where the session has `extension_skill_feedback_update`, dismiss the issue —
the plugin, the skill's dir_name, the issue's `issue_key` from the feedback list, and
the reason — and it stops resurfacing; `reopen` undoes it. Confirm with the user
before dismissing because a dismissal is permanent. Where the session lacks the tool, 
record the decision where the team will find it — the pull request, or a note the user
chooses — and say the issue will keep resurfacing until someone dismisses it.

## Ship and confirm

Before shipping, refresh the skill's provenance stamp to this plugin's current version
(the `metadata` key in [format.md](format.md)'s provenance stamp section, value read
from the plugin manifest, or `"mcp"` when you loaded this skill through the MCP server's
skill tools). A skill that never had one gains one now: the stamp records
which version of this plugin last touched the file, and this edit is that touch.

Same as [create.md](create.md) step 7, including its hand-over for review — with two
extra checks for an improve change: the verification id and issue key are recorded, and
the credited strengths survived. Land the change through the team's flow, sync (or say
a sync is needed), and re-read the feedback afterwards. Where the fix was
verified, record the verification's id in the change — the pull request or commit —
so the review can see what was tested and what the evidence was. Issues whose quoted
text your edit changed should flip to `likely_resolved`; an issue fixed without
touching its quote — a `capability_gap` answered by a new conditional path elsewhere —
stays `open` until a later assessment. Say which is which, and never edit the quoted
line just to force the flip. New feedback takes real usage to accumulate: today's edit
is assessed by next week's loads, not immediately.

## The report

End the job with a short account the team can act on, in the voice
the `talking-to-the-user` skill sets — the issue-by-issue
detail goes in the pull request description; the reply carries the headline and what
happens next: the edits made and why (issue by
issue: fixed, won't-fix with the recorded reason, or superseded), which issues you
expect to flip to `likely_resolved` and which will stay `open` despite being fixed,
anything you needed and couldn't verify (content to supply, a connection to record),
and what has to happen for the change to reach agents — landing, sync, and when
feedback will show it.

It is important to note which connector tool calls were overridden or simulated during
verification so that the user understands which parts have been fully exercised and 
which parts are not yet confirmed to be working.

When you tell the user how the tests went, pass or fail, add a one-line footnote: some
calls can't be made for real during a test, so there are limits to how much certainty it can offer, and
<https://docs.incident.io/nexus/extensions/incident-skills-plugin#limits-of-verification>
explains them.
