# The report

Every doctor run uses this shape. `## Headlines` gives the answer, the optional
situating block adds context, short findings name each problem and its route, and
briefs hold the detail. Anything said to the user around it follows
the `talking-to-the-user` skill.

## Format

```markdown
# Estate review — <date> — <scope: whole estate | plugin/area>
<owner and cadence, once a standing review has agreed them>

## Headlines

<Name the main finding in one or two sentences: what is wrong, where, and its
consequence. Do not introduce it with "Top finding" or a verdict adjective.>

<Summarize the other findings worth opening and what went unread in one sentence.>

<N> findings · <N> healthy · <N> of <N> checks unread (<N> partial)

<the situating block from orient.md, updated with verified facts. Omit it if orient
already showed it.>

## Findings, most actionable first

1. <glyph> **<the subject: the skill, file or system at fault>** — <what is wrong
   with it, one sentence>
   <"verbatim anchor"> (<file:line>) → **route:** <skill-authoring brief below |
   extensions: <the gap> | a change in the plugin's repository | dashboard: <the
   page> | previously declined, still recurring>
2. …

## Healthy

<the one-line credits: plugins synced, skills with good funnels, connections in
place — so the reader knows what was checked, not just what failed>

## Not readable from this session

<each surface the review couldn't reach, and where the answer lives>

## Briefs

<one per skill needing edits: the verified issues, the strengths to keep, ready to
hand to skill-authoring's improve job>

## Next

<Say that the run changed nothing. Route briefs to skill-authoring and structural gaps
to extensions. Acting on them is a new job.>
```

Rules the format encodes:

- **Open with `# Estate review`.** Keep working narration in the progress stream.
  Apply any final correction to the relevant finding.
- **Headlines give the answer; the situating block gives context.** A reader who
  stops after Headlines must know what the review found and which finding to open.
  Put the block after Headlines because it describes state that existed before the
  review.
- **Name the main finding.** State what is wrong, where, and its consequence.
  "Several significant issues were found" does not tell the reader what matters.
- **Include unread and partial checks in the counts.** `8 findings` can imply a
  complete review. `8 findings · 12 healthy · 6 of 11 checks unread (1 partial)`
  states its coverage. Omit the parenthesis when no check was partial; do not combine
  unread and partial checks as "incomplete". Count the numbered checks in the selected
  legs: unread means the check could not run; partial means it ran but could not
  finish.
- **Use one line for a clean result.** Write "Nothing to act on", the healthy
  summary, and the counts. Do not add urgency where none exists.
- **Print the situating block once.** Omit it from an interactive report if orient
  already showed it. Include it in scheduled reports and reports filed for readers
  who did not watch the run. Note any values the review changed.
- **Use two lines per finding.** The first line starts with the bold skill, file, or
  system and states the problem. The second gives the anchor and route. This keeps
  the list scannable by subject.
- **Put supporting detail in the brief.** Keep reasoning, related occurrences, and
  suggested edits out of the findings list.
- **File findings carry their anchor.** A `file:line` goes stale the moment the file
  is edited; pair it with a short verbatim quote of the offending line so the reader
  can still find it after the numbers drift.
- **Findings carry routes, not instructions.** The brief carries the detail; the
  finding says who acts. Purely informational findings (a deliberate removal, a
  caution) route to the Healthy section or a note line — they still appear, they
  just ask nothing.
- **Healthy and unreadable are first-class sections.** A review that only lists
  problems can't be told apart from a review that only looked for them.
- **Nothing in the report has been changed by the run.** If a sentence would start
  "I fixed", the run went past its mandate.
- **The report stands alone.** It restates everything the run reported as it went (see
  [progress.md](progress.md)), because whoever files it and whoever reads it back are
  not the person who watched it happen. A finding that only ever appeared in the
  progress stream is a finding this report is missing.

## A worked report

Use this trimmed report to check the intended format. The plugin and every finding in
it are invented, so read it for the shape and never for a real estate's state.

````markdown
# Estate review — 2026-03-14 — plugin: platform-ops

## Headlines

`deploys` and `rollback` both own the rollback procedure, and the two copies now give
different instructions. `deploys` keeps a drain step that `rollback` dropped in
January, so which skill an agent happens to load decides whether a responder drains
connections before cutting traffic.

Behind it: `database` cites a step its own procedure does not contain, and `oncall`
names a tool with no path for a session that lacks it. No account-side surface was
readable from this session.

3 findings · 4 healthy · 6 of 11 checks unread

Session   platform-skills @ main, clean · ✗ no incident.io connection
This repo plugins/platform-ops — 6 skills, 6 in the README ✓ · sync state unknown
Account   unknown — no connection; the dashboard's Extensions page has it
Health    unknown — no connection; the dashboard's data sources page has it
Install   platform-ops 2.1.0, clone refreshed yesterday · ⚠ behind the tree here

## Findings, most actionable first

1. ⚠ **deploys and rollback** — both carry the rollback procedure, and the copies
   disagree on the order of the first two steps.
   "drain the connections, then cut traffic" (deploys/references/rollback.md:31) vs
   "cut traffic first" (rollback/SKILL.md:44) → **route:** a change in the plugin's
   repository
2. ⚠ **database/references/failover.md** — sends the reader to a step 5 the file does
   not have; its steps stop at 4.
   "confirm the replica caught up (step 5)" (failover.md:88) → **route:** database
   brief below
3. ℹ **oncall/references/page.md** — names `escalation_create` with no absence path,
   where `alerts` names the same tool and carries one.
   "call `escalation_create`" (page.md:24) → **route:** oncall brief below

## Healthy

Every skill directory is registered in the README's skills table. All 8 tool names the
skills reach for exist in this session's catalogue, none of them client-prefixed. Every
reference file is reachable from its SKILL.md.

## Not readable from this session

- **Sync state, and the skill count the account sees** — no `extension_plugin_list`.
  The dashboard's Extensions page has it.
- **Per-skill feedback funnels** — no `extension_skill_feedback_list`. This review
  could not assess whether these 6 skills earn their loads.

## Briefs

### `database` — repair the failover cross-reference

Verified: `references/failover.md:88` cites a step 5, and the procedure ends at step 4.
The replica check it means lives in `deploys/references/rollback.md:52`.

Strengths to keep: the verbatim signatures the routing table matches on, and the rule
to state what the run could not confirm.

### `oncall` — give `escalation_create` an absence path

Verified: `references/page.md:24` calls the tool with no fallback. `alerts` names the
same tool at `references/route.md:17` and says what to do without it.

Strengths to keep: the confirmation gate before a page goes out.

## Next

The run ends here. Nothing above has been changed. The briefs go to skill-authoring's
improve job; the diverged rollback copies are a normal pull request. The six unread
checks need a session with the incident.io connection.
````

The example shows two details the template cannot: every situating-block row fits on
one line, and every finding starts with a bold subject. Keep it in step with the rules
above — a specimen that contradicts them teaches the wrong shape.

## Cadence

Doctor is built to recur. When the user wants a standing review, agree the two
parameters and record them in the report header from then on:

- **Owner** — who reads the report and hands briefs on. A report nobody owns is
  noise.
- **Cadence** — weekly suits most estates; after each growth moment (a new
  connection, a new team's plugin) is the other natural trigger.

A scheduled run behaves exactly like an invoked one: same checks, same report,
propose-only. What accumulates between runs is the team's record — reports and
declined findings kept in the plugin's repository as a dated file or a pull request
description, the same home the extensions skill offers for its estate reports. No
directory is reserved for them, which is why the check that reads them searches for
their headings rather than a path. That record is what lets the next run say
"previously declined, still recurring" instead of re-escalating. Doctor never files it:
offer it, and on a scheduled run deliver the report and name the dated file it belongs
in — a human lands it.
