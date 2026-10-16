# Saved Search to Bid / No-Bid to Annotated Outline

Use this reference when the user wants a repeatable or externally scheduled workflow that watches a saved search, qualifies new matches, and creates, drafts or recommends annotated proposal outlines according to the user-authorized run policy only for pursuit-worthy targets.

## Do not use this when
- The user wants a plain saved-search triage report. Use [Relevant Opportunities](./relevant-opportunities.md).
- The user wants a one-off qualification call for one already-selected opportunity or pursuit. Use [Conduct Bid / No-Bid Review](./conduct-bid-no-bid-review.md).
- The user wants an annotated outline for one resolved solicitation without a capture gate. Use the bundled `govtribe-proposal-workflows` and its Build Annotated Proposal Outline workflow from its own installed root.
- The user asks for proposal compliance extraction, a control workbook, or drafting support before a pursuit decision has been made. Hand off to proposal construction after qualification.

## Inputs to resolve
- Saved search, manual or host-scheduled trigger, and run context.
- New result IDs or full result records included with the run.
- User company, team, teammate, capability, vehicle, certification, geography, buyer, and past-performance context.
- Any configured fit criteria, hard gates, minimum outline threshold, source-file requirements, destination, and output format.
- Whether the user-authorized run should create or draft outlines, recommend outlines, or remain monitor/triage-only. Preserve this policy in every run and report creation only after the requested artifact exists.
- Whether the user wants the search preserved through MCP. Resolve it with `Search_Saved_Searches`, and use `Create_Saved_Search` or `Update_Saved_Search` only when the user explicitly requests that supported workspace mutation.
- This package uses the full GovTribe endpoint without GovTribe automation operations. If the external host supports scheduling, provide this workflow as the scheduled prompt and let the host own the cadence. Otherwise return a manual rerun checklist and the reusable saved search; never imply that scheduling occurred.

If the saved search, company context, or outline policy cannot be resolved well enough to make a defensible call, stop and return the missing inputs instead of guessing.

## Workflow

### 1. Read run context first
- Identify the saved search and what triggered this run.
- If the task is to schedule or revise the monitor, return the reusable prompt, cadence, saved-search identity, deduplication rule, and manual verification steps. Execute host-native scheduling only when the user requested it and the host exposes that capability, then verify the saved schedule; otherwise state that the user must rerun it manually.
- Use included record details first when the run provides full records.
- If only GovTribe IDs are provided, retrieve the records before ranking, gating, or outlining.
- Say when the saved-search result set is truncated, stale, partially inaccessible, or missing key fields.
- Deduplicate records and avoid re-processing stale results when run context, saved-search state, or host-supplied prior-run state supports that. If no state is available, disclose that deduplication is limited to the current result set.

### 2. Normalize new saved-search results
- Build one normalized row per candidate with record ID, title, buyer or agency, due date or timing, type, vehicle or access path, set-aside or eligibility, location, value signal, source-file status, and why the saved search matched it.
- Keep federal contract, federal grant, and state/local records on their correct surfaces.
- Preserve source IDs so later proposal handoff can trace the target and the retrieved files.

### 3. Filter to plausible candidates
Separate candidates before spending proposal effort:

| Bucket | Use when | Next step |
| --- | --- | --- |
| `ignore` | Obvious no-fit, duplicate, expired, inaccessible, or hard-gate failure. | Report briefly; no outline. |
| `watch` | Interesting but too early, weak, ambiguous, or missing decision-moving evidence. | Return watch reason and next research step. |
| `partner-needed` | The target may work only with a teammate, vehicle holder, local partner, or capability partner. | Run bid/no-bid with partner scenario. |
| `qualify now` | The record is plausible and has enough context for a gate decision. | Run bid/no-bid/go-no-go gate. |
| `needs more source data` | Fit may be strong but required solicitation files or context are missing. | Return outline-readiness gaps. |

Use the user's company strengths, vehicles, certifications, geography, buyer priorities, past performance, staffing capacity, and strategic preferences as the fit frame.

### 4. Apply go/no-go as bid/no-bid language
- Treat "go/no-go" and "go no go" as customer-facing wording for the same decision family as [Conduct Bid / No-Bid Review](./conduct-bid-no-bid-review.md).
- Use the existing formal outputs where possible: `BID`, "BID_WITH_PARTNER", "SUB_ONLY", "MONITOR_AND_SHAPE", and "NO_BID".
- Do not create a second scoring model unless a future product requirement proves that go/no-go means a different gate.
- Run hard gates before outline decisions: access path, vehicle, set-aside, geography, due date, source availability, company fit, past-performance fit, staffing, compliance, and economics.

### 5. Decide whether to proceed to proposal outline
- Default threshold: create or draft annotated outlines only for `BID` or "BID_WITH_PARTNER" when the user-authorized run policy requests creation; otherwise recommend them. Use `govtribe-proposal-workflows` from its own installed root and report creation only after verifying the artifact.
- Allow configured equivalents, such as including "SUB_ONLY", only when the saved run policy explicitly says the team wants that posture outlined.
- Never create annotated outlines for every saved-search result.
- Do not outline "NO_BID", low-confidence, watch-only, missing-source, monitor-only, or hard-gate-failure records.

### 6. Check proposal readiness before handoff
Before handing off to proposal construction, confirm:

- Source package exists or can be retrieved.
- Latest solicitation, amendment, and Q&A context are available when relevant.
- Submission instructions, evaluation factors, PWS/SOW/SOO, attachments, or equivalent file content are sufficient for a meaningful outline.
- Company context and bid/no-bid rationale are specific enough for writer-facing guidance.

If readiness fails, return `outline blocked` with the exact missing files, questions, or access issues.

### 7. Hand off to proposal construction
- Use the bundled `govtribe-proposal-workflows` and its Build Annotated Proposal Outline workflow from its own installed root for qualified outline-ready targets. If the host cannot produce the requested format, retain the evidence-backed Markdown outline and a handoff identifying unsupported format or rendering steps.
- Pass target record IDs, source IDs, requirement findings, bid/no-bid rationale, company context, teammate assumptions, and configured output preferences.
- Do not duplicate the annotated-outline method in this workflow. Capture owns qualification; the proposal-construction capability owns outline creation.

## Repeatable-run report format

Return a repeatable-run report with these sections:

- `Run context`
- `New saved-search matches reviewed`
- `Qualification decisions`
- `Outline-ready opportunities`
- `Blocked or watch-only opportunities`
- `Artifacts created or recommended`
- `Next actions for capture/proposal`

Use a compact table for the decision ledger:

| Result | Target | Gate call | Why | Outline status | Next action |
| --- | --- | --- | --- | --- | --- |

Clearly explain when no outline was created and why.

## Prompt template

```text
Use Capture Workflows > Saved Search to Bid / No-Bid to Annotated Outline.

Watch the new results from this saved search and qualify them before doing any proposal work. If the run context gives you full result details, use them. If it gives you only GovTribe IDs, retrieve those records before ranking or gating. If the result set is truncated, stale, or includes duplicates, say so.

Assume we are a [business type] with strengths in [capabilities], [vehicles/certifications], [past performance], and [target buyers/geographies]. Treat go/no-go as the same decision family as bid/no-bid. Use BID, BID_WITH_PARTNER, SUB_ONLY, MONITOR_AND_SHAPE, or NO_BID where possible.

Only create, draft or recommend an annotated proposal outline according to the user-authorized run policy for targets that pass the gate as BID or BID_WITH_PARTNER, unless this run explicitly says to include another threshold. Use the bundled proposal workflow, verify the artifact and report actual creation distinctly. Do not claim outline creation for weak fits, watch-only records, NO_BID records, monitor-only runs, missing source packages, or targets with hard gate failures.

For each new match, report the gate decision, evidence, outline status, blockers, artifacts created or recommended, and the next capture or proposal action.
```

## Stop conditions
- The opportunity does not pass the bid/no-bid/go-no-go gate.
- The result is only a weak, watch-only, or ambiguous fit.
- Required source files are missing, inaccessible, or not enough for an outline.
- Company context is too thin to make a defensible qualification call.
- Access path, vehicle, set-aside, geography, due date, compliance, staffing, or economics fails a hard gate.
- The run is configured as monitor/triage-only.

## Common failure modes
- Creating an outline for every saved-search result.
- Starting proposal construction before the capture gate passes.
- Treating go/no-go as a separate skill and fragmenting routing.
- Ignoring viable partner-needed outcomes.
- Producing a full proposal artifact when the run should only recommend next steps.
- Hiding missing source files or thin company context behind a confident outline.
