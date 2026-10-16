# Orient

Every run starts here: a fast pass, cheap reads only, that answers the questions below
and ends in a situating block. Nothing in this phase verifies an anchor, pulls feedback
issues, or reads a runbook — the point is that the user sees something true and useful
within seconds, and the expensive review runs only after they've chosen it.

## The questions

1. **Where is this session?** The working directory; whether it's a git checkout and of
   what (the remote names the repository); whether the checkout lags the branch the
   plugin syncs from — a lagging checkout changes what the review verifies against
   (see content-drift's rules). And whether a plugin tree lives here: an
   `incident.yaml`, a skills directory, a runbooks corpus.
2. **Does what's here correspond to a plugin the account knows?**
   `extension_plugin_list`, matched against the local tree. Three outcomes, each a
   line in the block: this checkout carries a synced plugin (name it, with sync state
   and skill count); the account has plugins whose trees aren't in this checkout
   (name them — they're reviewable through feedback and account data, not through
   their files); or there's no incident.io connection at all (say so, and offer only
   what files alone can support).
3. **What does the account's own rollup already know?** `extension_connector_list`
   and `nexus_health_show`, one call each: connections with status, sources with
   query statistics. This is the same rollup the dashboard computes, so the block can
   never disagree with what the user sees there.
4. **Is the agent's own install current?** Skills go stale silently. Nothing tells an
   agent that the copy it just read is several versions behind, so it follows month-old
   instructions with full confidence and no way to notice. Two local reads answer it,
   and neither touches the network: `known_marketplaces.json` records when each
   marketplace clone last refreshed, and `installed_plugins.json` records the version
   mounted. Where the session can't read them — a hosted agent has no plugin state of
   its own — skip the question rather than guess at it.

## The situating block

Compact, one line per fact, status glyphs doing the summarizing — ✓ healthy, ⚠
degraded, ✗ failing, ℹ true and worth knowing but asking nothing:

```markdown
# Doctor — where you are

Session   <repo and checkout state> · <incident.io connection ✓ | no incident.io connection>
This repo <plugin dir → synced as "<name>", <last sync>, <n> skills | no plugin tree>
Account   plugins: <name ✓|⚠ per plugin, trees-not-here noted> | <none>
Health    <n> connections — <n> ✓ · <each degraded one: name, glyph, one-phrase reason>
Install   <plugin> <version> ✓ | ⚠ <what is stale, and the command that refreshes it>
```

These rules keep it honest:

- **Keep each fact on one output line.** Use one label, one glyph, and one fact, and
  aim for no more than 100 characters. Do not insert a line break; client-side
  wrapping is outside the report's control. Move overflow into a finding.
- Every line is sourced from a tool this pass actually called, or reads
  `unknown — <how to find out>`.
- Glyphs come from the rollup's own judgments (attention reasons, reconnection
  needed, low success rate), never recomputed here — orientation summarizes, the
  review verifies.
- A connection with no queries in the stats window is "never queried", not healthy
  and not unhealthy — the same correction telemetry.md applies.
- **A matching version is not evidence of being current.** A clone that hasn't
  refreshed offers the version it fetched last time, so the installed version and the
  clone's own agree while both sit behind the published one. The refresh age is the
  signal; the version gap only opens up once someone fetches. Report the age, and read
  "current" as "current as far as this machine has looked".

## The offer

After the block, offer the runs that make sense *from here* — built from what
orientation found, never a fixed list — each with an honest cost signal:

- **Deep review of <the local plugin>** — feedback, anchor verification, content
  drift. The thorough one: minutes, and where the verified findings come from.
- **Estate health snapshot** — the block above expanded with per-source query
  statistics and per-plugin feedback funnels, nothing verified. Moments.
- **Feedback triage** — open issues across every synced plugin, verified against
  their anchors and clustered into briefs. Between the two.
- **Everything** — all applicable legs, the full report.

Mark one as recommended — whichever the rollup flagged; the local plugin's deep review
where nothing did — and end with `**Next step:** pick a review — <recommended> is
what I'd run`. Then stop: the block plus the menu is the reply, and the user's pick
starts the review. Don't start gathering while they decide.

## When to skip the offer

- **The invocation already carries a scope** ("doctor for the ops plugin", a skill
  argument) — show the block, skip only the menu, and go straight to that review.
  Someone is watching a scoped run; they have already said what they want, which is a
  reason to skip the question and not a reason to skip the answer. It is the cheapest
  true thing the run can put in front of them, and withholding it leaves the longest
  stretch of any run with nothing in it.
- **Scheduled runs** — nobody is there to read a block or pick from a menu. Orient
  silently, run the agreed scope, and let the block open the report.
- **The snapshot answers the question by itself** ("is anything failing right now?")
  — answer it from the block and offer the deeper runs in one line. That can be the
  whole run.
