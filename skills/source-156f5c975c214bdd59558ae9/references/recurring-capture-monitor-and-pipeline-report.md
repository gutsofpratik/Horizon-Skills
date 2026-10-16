---
title: Recurring Capture Monitor and Pipeline Report
description: How to run recurring or event-triggered capture monitors that summarize market, saved-search, recompete, and pipeline deltas for capture teams.
---

# Recurring Capture Monitor and Pipeline Report

Use this reference when the user wants a daily, weekly, scheduled, saved-search-triggered, pipeline-triggered, or manual "what changed?" review for a market, saved search, pipeline, recompete watch, pursuit set, buyer lane, vehicle, program, NAICS, PSC, geography, or capability lane.

## Goal
- Resolve the monitored scope and run context before searching.
- Separate true new or changed signals from stale context.
- Summarize deltas, decisions, risks, and owner actions instead of repeating broad market background.
- When the user asks to create or update a recurring monitor, persist a reusable GovTribe search with `Create_Saved_Search`, `Search_Saved_Searches`, or `Update_Saved_Search` when appropriate, then use a host-native scheduler if one is available. If scheduling is unavailable, return a manual monitor specification and state that no schedule was created.
- Keep market monitoring distinct from one-opportunity capture qualification.

## Workflow

### 1. Classify the run context
- Scheduled host run: use the host-supplied prompt, cadence, project, selected skill, prior-run context, and attached monitor context before widening the search.
- Saved-search trigger: use the saved-search result context first. If only GovTribe IDs are provided, retrieve those records before summarizing or ranking them.
- Pipeline update: use `Search_Pipelines`, `Search_Stages`, and `Search_Pursuits` to resolve the pipeline, stage map, changed pursuits, and linked records before deciding whether the output is a market monitor or a pursuit-specific cleanup report.
- Monitor setup or edit request: if a persistent GovTribe query fits the scope, call `Search_Saved_Searches` before editing an existing saved search, `Create_Saved_Search` for a new one, or `Update_Saved_Search` for the requested changes. Use the host scheduling capability for the reusable monitor prompt only when scheduling is available and requested. Before editing an existing host schedule, inspect its current definition and version where supported, and change only the user-requested fields. Otherwise provide a manual specification containing the saved-search or filter scope, cadence, delta window, output sections, and handoff rules. If the user refers to an existing automation that is not present in the supplied context and the host cannot retrieve it, request its definition or export only when changing it materially affects the result. If saved-search persistence is unavailable to the current client, include the exact reusable filters in the manual specification and state that no saved search was created or updated.
- Manual request: treat phrases like "what changed," "monitor this market," "weekly capture report," or "recompete watch" as a request for a delta report over the user's stated scope.
- First run: if there is no prior run or baseline, say that this run establishes the baseline and separate current priorities from future watch criteria.

### 2. Resolve the monitored scope
- Normalize the user request into one or more concrete scope anchors: saved search, buyer, agency, office, pipeline, pursuit set, vehicle, program, NAICS, PSC, geography, capability lane, incumbent, competitor, or known record.
- Prefer trigger context, selected saved-search filters, pipeline configuration, linked records, and explicit IDs over inferred scope.
- If multiple plausible saved searches, pipelines, buyers, or lanes match, ask one bounded clarification. Prefer `Show_Option_List` when the choice is a short candidate list.
- If the request names a broad market but also includes a pipeline or pursuit set, use the market scope to find changes and use the pipeline only to prioritize owner actions.

### 3. Establish the comparison window
- Use the host schedule cadence, saved-search trigger period, or user-stated period as the default delta window.
- For saved-search triggers, treat the trigger result set as the strongest new-item evidence and use additional retrieval to complete missing record detail.
- For scheduled or manual runs without prior state, use recent created, updated, due-date, lifecycle, and forecast windows that match the requested cadence. Do not claim something is "new since last run" unless the context supports it.
- Keep stale background records available as context, but do not list them as new or changed unless a date, status, file, amendment, stage, or linked signal actually changed.

### 4. Retrieve changed market and capture signals
- New opportunities: search the relevant opportunity surfaces for new, open, or recently updated notices in the monitored lane.
- Forecasts and early signals: use forecast and early-notice retrieval when demand may not have become a solicitation yet.
- Amendments and files: use `Search_Government_Files` to locate relevant amendments, Q&A, and attachments when the monitored lane includes live solicitations. When file contents are needed, use `Add_To_Vector_Store` followed by `Search_Vector_Store`, cite returned source metadata with the host's native citation format, and use the host's ordinary attachment or spreadsheet capability for material content that vector retrieval skips. If neither route is available, identify the uninspected file and return a labeled partial result.
- Expiring awards, IDVs, vehicles, and recompetes: use lifecycle dates and follow-on evidence to separate likely recompetes from ordinary expirations.
- Incumbent and buyer movement: review linked awards, transactions, forecasts, contacts, files, and office context when changes may affect capture posture.
- Pricing evidence: note new or changed pricing evidence only when it materially affects pursuit priority, price-to-win risk, or capture action.
- Pipeline hygiene: for pipeline-scoped runs, review stale pursuits, due-date risk, missing estimated value or award date, unclear owner, weak stage fit, and linked-record gaps.

### 5. Separate signal from stale context
- Mark a record as new only when the trigger context, created date, surfaced result set, or retrieved record supports that conclusion.
- Mark a record as changed only when returned fields, files, amendment history, due dates, stage movement, linked records, or lifecycle data show a material change.
- Treat old but still-important records as watch items, stale pipeline items, or background context rather than new changes.
- Deduplicate records that represent the same requirement across opportunity, forecast, award, IDV, vehicle, or file surfaces while preserving lifecycle progression.

### 6. Decide when to hand off
- Use `govtribe-capture-workflows` when the next step is bid / no-bid, relevant-opportunity ranking, likely bidders, incumbent recovery, pipeline review, pipeline updates, owner assignment, or pursuit-specific qualification.
- Use `govtribe-proposal-workflows` when the recurring run detects a solicitation amendment, Q&A change, attachment change, compliance requirement, proposal-file update, or other proposal-control impact.
- Use `govtribe-pricing-data` when pricing evidence needs a dedicated wage, labor-rate, awarded-line-item, or pricing-model workflow.
- Stay in Market Intelligence when the output is still a market, saved-search, recompete, buyer-lane, or early-signal monitor.

## Output contract
- Return a concise report with these sections when applicable:
  - `Scope and run context`
  - `Urgent actions`
  - `High-priority new items`
  - `Watch items`
  - `Stale pipeline items`
  - `Timing and deadline risks`
  - `Missing evidence`
  - `Recommended owner actions`
- For each action item, include the record or scope, what changed, why it matters, recommended owner action, and confidence.
- Lead with the most time-sensitive capture actions. Put background market observations after action items.
- If the user asked to create or update a monitor, name the persistence path actually used (`Create_Saved_Search`, `Search_Saved_Searches`, `Update_Saved_Search`, host-native scheduling, or manual specification), summarize the saved name or scope, trigger, cadence, skill, and prompt changes, and state explicitly whether a schedule was created.
- If the run is a first-run baseline, label it clearly and avoid pretending that baseline records are new deltas.
- If a saved-search trigger includes IDs but not full records, say records were retrieved before summarizing. If some IDs cannot be retrieved, list that as missing evidence.
- Keep the report useful to a capture team without requiring them to reconstruct tool calls.
