---
name: call-review
description: Review the last 100 calls for an agent and surface problems. Use this whenever the user wants a call-quality audit, a QA pass over recent calls, a "what's going wrong with this agent" review, or to find failed, unresolved, dropped, or otherwise problematic calls. Trigger on phrases like "review my calls", "what's wrong with the calls", "QA the last 100 calls", "find bad calls", or "audit recent calls".
---

# Call Review

## Purpose

Pull a batch of recent calls for one agent, inspect them, and surface the problems — so issues are caught in review instead of live on customer calls. Default batch size is the **last 100 calls**.

This playbook runs on the Synthflow MCP tools, whether they come from the plugin's bundled server or the official Synthflow connector. It does not require any external API or script.

## Tools this uses

- **`list_calls`** — get the batch of recent calls for the agent.
- **`get_call_details`** — pull transcript, outcome, duration, and metadata for a specific call.
- **`get_call_analytics`** — pull aggregate metrics across the batch.
- **`list_agents`** — identify the agent when the user hasn't named one.

Recordings can't be played over MCP. When call details include a recording URL, share it so the user can listen — don't assert audio-only findings from the transcript (see Rules).

## Before starting

Confirm three things. If the user already gave them, don't re-ask — proceed.

1. **Which agent.** If not named, use `list_agents` and ask the user to pick. Never guess.
2. **Batch size and window.** Default: last 100 calls, no date filter. Honor any override ("last 50", "yesterday", "this week").
3. **Custom failure list (optional).** Ask whether this agent has known failure types to check specifically. If yes, take them as the agent-specific checklist (see "Agent-specific failures" below). If none, run generic checks only.

State any assumption you make rather than asking a second clarifying round.

## Step 1 — Pull the batch

Use `list_calls` for the chosen agent, limited to the batch size (default 100). For each call, note: call ID, timestamp, duration, direction, and outcome/status if available.

Drop and count separately any calls that are not real conversations: no-connects, voicemail, and calls under ~5 seconds. Report how many were excluded and why — don't let them dilute the problem rates.

If `list_calls` returns fewer than requested, review what exists and say so.

## Step 2 — Triage cheaply first

Before inspecting individual calls, use `get_call_analytics` for the batch to get the lay of the land: outcome/resolution rates, average and tail durations, and any built-in sentiment or success metric. Use this to prioritize which calls to open in Step 3 — don't read all 100 in full when the analytics already point at the failing slice.

## Step 3 — Inspect calls and flag problems

Pull `get_call_details` (transcript + metadata) for the prioritized calls.

Check every call against the generic problem checklist, plus the agent-specific list if one was given.

### Generic problem checklist

Flag any call exhibiting:

- **Unresolved / failed outcome** — the caller's goal was not met, or the call ended without resolution.
- **Repetition** — agent re-asks for information the caller already gave.
- **Premature interruption / barge-in** — agent cuts the caller off, especially during slow or grouped delivery (numbers, addresses).
- **Mid-call dropout** — agent stops responding or goes silent mid-conversation.
- **High latency** — long gaps before the agent responds (audio-only; flag for the user to verify against recordings).
- **Caller frustration or confusion** — escalating tone, repeated "what?", "that's not what I said", caller giving up.
- **Wrong or hallucinated output** — agent states a fact, price, or outcome that is incorrect or unsupported.
- **Mispronunciation** — names, domain terms, numbers read wrong by TTS (audio-only; flag for user verification).
- **Disengagement / early hangup** — caller drops before the goal is reached.
- **Compliance / over-disclosure** — agent shares information before verifying identity, or collects data it shouldn't. **Flag these prominently — they are the highest-severity finding regardless of frequency.**
- **Off-the-rails behavior** — agent goes outside its role, loops, or contradicts itself.

### Agent-specific failures

If the user provided a custom list, check each call against it as well. (Example, for a German invoice agent like "Pia": invoice-number capture errors, separator/Schrägstrich placement after the 6th digit, re-asking for already-provided info, premature interruption, mid-sentence dropout.) Treat these with the same rigor as the generic checks and report them as their own category.

## Step 4 — Report

Lead with the table, then the summary. Keep it scannable.

Render a markdown table with one row per flagged call:

| Call ID | Time | Duration | Problem(s) | Severity | Evidence |
|---|---|---|---|---|---|

- **Severity:** Critical (compliance/over-disclosure, wrong outcome on a consequential action, agent off the rails) · High (unresolved goal, dropout, repeated interruption) · Medium (latency, repetition, mild confusion) · Low (mispronunciation, minor polish).
- **Evidence:** a short transcript quote or a recording link with timestamp — not a paraphrase. Make it checkable.

Then a short written summary:

- Batch reviewed: N calls (X excluded as no-connect/voicemail/too-short).
- Problem rate: how many of the real calls had at least one flagged issue.
- Top 3 problem types by frequency, each with a count.
- Any Critical findings, called out first by name.
- One or two concrete recommendations (prompt, action, voice, or routing changes) tied to the most common or most severe issues.

## Rules

- **Evidence over assertion.** Every flagged problem cites a transcript quote or a recording link. If you can't point to evidence, don't flag it.
- **Don't invent metrics.** If `get_call_analytics` doesn't expose a metric (e.g. latency), say so rather than estimating.
- **Audio-only issues need the recording.** Latency, interruption, dropout, and mispronunciation can't be judged from a transcript, and recordings can't be played over MCP — report transcript-level signals as "suspected", link the recordings, and ask the user to spot-check before treating them as confirmed.
- **Surface compliance issues first** even if they appear once.
- **Don't auto-fix.** This playbook reviews and reports. After the report, ask the user whether they want help fixing the top issues (prompt edit, action change, etc.).
- **Keep it to the batch.** Don't generalize to "the agent always…" from 100 calls — report what this batch shows.

## After the report

Ask the user whether they want you to draft fixes for the top one or two issues (see the `prompt-review` skill for prompt changes), or run a simulation to reproduce a specific failure before changing anything.
