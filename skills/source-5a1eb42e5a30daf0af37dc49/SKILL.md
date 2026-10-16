---
name: replay-triage
description: Triage issues captured in a Pendo session replay by fetching devlogs, mapping errors to the local codebase, proposing fixes, and prompting for a pull request. Accepts either a replay URL directly or a ticket reference (e.g. Jira key or URL, GitHub issue URL, etc.) and will pull the replay link from the ticket. Use whenever someone hands off a user-reported bug — via a replay link or a ticket that contains one — and asks to investigate, diagnose, debug, triage, or fix it. Requires Pendo connector; uses whatever ticketing MCP or CLI is available (Atlassian, `gh`, etc.) when a ticket is supplied.
---

# Replay Triage

Given a Pendo session replay — supplied directly as a URL or referenced from a ticket (Jira, GitHub, etc.) — pull the devlog events (console errors and HTTP failures) captured during that session, cross-reference them against the current codebase, propose a fix, and prompt the user to open a PR.

This skill is designed for application developers triaging a user-reported issue: start from the replay that witnesses the bug, end at a proposed code change.

## Parameters

The user may supply one of:

- **replay_url**: A Pendo session replay player URL or saved clip URL. Examples:
  - `https://<hostname>/s/<subId>/replay/player/<sessionId>?startTime=...&endTime=...`
  - `https://<hostname>/s/<subId>/replay/clip/saved/<clipId>`
- **ticket**: A reference to a ticket that contains the replay URL. Can be:
  - A Jira issue key (e.g. `ABC-12345`) or full Atlassian URL
  - A GitHub issue URL (e.g. `https://github.com/org/repo/issues/123`)
- **focus** (optional): A hint about what to look at — e.g. "login fails", "500 on /orders", "UI freezes after save". If a ticket is provided, the ticket's description usually supplies this automatically.

If the user gives only a bug description with no replay URL or ticket, ask for one first. This skill is useless without a replay.

## Step 0: Resolve a Ticket (if supplied)

If the user gave a ticket reference instead of a replay URL, look it up and extract the replay URL from its description and comments. Choose the tool based on where the ticket lives and what's available in the current environment — do not hardcode one system:

- **Jira / Atlassian**: if the Atlassian MCP is available (`mcp__atlassian__getJiraIssue`), call it. If not, try `mcp__atlassian__search` or ask the user for the replay URL directly.
- **GitHub**: use `gh issue view <url-or-number> --comments` via Bash. This is almost always available.
- **Unknown host**: if you can't identify the ticket system or no matching MCP/CLI is available, tell the user and ask them to paste the replay URL directly.

When fetching, request the description **and** comments — replay links are often added in a comment after the bug was filed.

Scan the ticket content for a Pendo replay URL. Match on the shape `/replay/player/` or `/replay/clip/saved/` in the hostname path — don't just search for "pendo", which will false-match unrelated links. If you find:

- **Exactly one replay URL**: use it and continue.
- **Multiple replay URLs**: present them to the user with a one-line context snippet (e.g. the surrounding comment author/date) and ask which one to triage.
- **No replay URL**: say so, show the ticket summary, and ask the user to provide the replay URL.

Also capture from the ticket:

- The **summary / title** and **reported bug description** — feed the most specific details into `focus` so Step 3's triage can prioritize the right errors.
- Any **steps to reproduce**, **expected vs. actual behavior**, or **error messages pasted by the reporter** — these often match strings you'll search for in Step 4.

If the user supplied both a ticket and a replay URL, prefer the explicit replay URL but still pull ticket context for `focus`.

## Step 1: Parse the URL

`devlogEvents` takes the identifying fields as individual parameters. Pull them out of the replay URL yourself — the two shapes are:

- **Player URL** — `https://<hostname>/s/<subId>/replay/player/<recordingSessionId>?startTime=<ms>&endTime=<ms>&visitorId=<id>&appId=<id>&accountId=<id>`
  - `subId`: the segment after `/s/`
  - `recordingSessionId`: the segment after `/replay/player/` (strip any query string or fragment)
  - `startTime`, `endTime`: the `startTime` and `endTime` query params, as numbers in milliseconds since epoch
  - `visitorId`, `appId`, `accountId`: pull these from the query string whenever they're present. They're optional for the call, but passing them narrows the aggregation on the Pendo side and makes `devlogEvents` return noticeably faster — always include the ones you can parse. Only fall back to omitting them if the URL doesn't have them.
- **Clip URL** — `https://<hostname>/s/<subId>/replay/clip/saved/<clipId>`
  - `subId`: the segment after `/s/`
  - `clipId`: the segment after `/clip/saved/` — passing this alone lets `devlogEvents` resolve `appId`, `visitorId`, `accountId`, `recordingSessionId`, and the time range internally

If the URL is malformed or missing `startTime`/`endTime` on a player link, ask the user to copy the link again from the Pendo UI — the player URL exported from Pendo always includes the time range. If you can't parse a `subId` at all (non-standard host), call `list_all_applications` and confirm the subscription with the user before continuing.

## Step 2: Fetch Devlogs

Call `devlogEvents` with the fields you extracted in Step 1.

**For a player URL**, pass:

- `subId`, `recordingSessionId`, `startTime`, `endTime` (from Step 1)
- `visitorId`, `appId`, `accountId` — include every one that was present in the URL's query string. These aren't required, but they prune the search space server-side and make the call materially faster, especially on noisy subscriptions. Omit only the ones the URL didn't contain.
- `logType`: `["console", "network"]`
- `logLevels`: `["error", "warn"]`
- `statusCodes`: `["4xx", "5xx"]`
- `limit`: `50`

**For a clip URL**, pass:

- `subId`, `clipId` (from Step 1) — the clip lookup fills in the rest
- The same `logType`, `logLevels`, `statusCodes`, and `limit` as above

`devlogEvents` is a slow-running tool. Tell the user you're pulling logs so they know what you're waiting on.

### Handling empty results

If the call returns no events, don't stop:

1. Retry with `logLevels: ["error", "warn", "info"]` in case errors were logged at a lower level.
2. Retry with `statusCodes` dropped entirely to see all network traffic.
3. If still empty, tell the user the session had no captured errors or network failures in the recorded window, and ask whether they want to look at a different replay or widen the window.

### Handling hit-the-limit results

If the call returns exactly `limit` events (50), you're almost certainly truncated — there may be more events you never saw, and the ones you got are biased toward one edge of the window. Don't just triage what you have; narrow the window and re-fetch:

1. **Shift the window** to a sub-range of `[startTime, endTime]` — e.g. split into halves or focus on the portion the user's `focus` hint points at (if they said "crash after save", target the last third of the session first).
2. **Re-call `devlogEvents`** with the narrower `startTime`/`endTime`. Keep `subId`, `recordingSessionId`, and the other identifiers the same.
3. **Repeat as needed** until a sub-window returns fewer than 50 events, or until you've covered the full original range with stitched sub-windows. Deduplicate across sub-windows before clustering in Step 3.
4. If every sub-window still saturates at 50 even when narrowed to a few seconds, tell the user the session is unusually noisy and ask whether they want to focus on a specific symptom or timestamp before continuing.

For clip URLs, the clip lookup supplies a default time range, but you can still pass explicit `startTime`/`endTime` to override it — use the same narrow-and-re-fetch loop above. If you don't know the clip's resolved range yet, do one unbounded call first to see the timestamps on the returned events, then shift the window within that span.

## Step 3: Triage the Events

Group the devlog events into candidate issues. The goal is a small set of distinct problems, not a dump of every log line.

For each event, capture:

- **Console errors**: message, stack trace, timestamp. Strip obvious noise (e.g. third-party analytics 4xx, CORS warnings from browser extensions) unless the user's `focus` points to them.
- **Network errors**: method, request URL, status code, response body snippet. Note if multiple calls to the same endpoint failed — that's usually one bug, not many.

Cluster events that share a root cause: same stack frame, same endpoint, same error message. Rank clusters by:

1. **5xx errors** — server-side failures are almost always real bugs.
2. **Unhandled JS errors** — anything with "Uncaught" or a stack trace that ends in app code.
3. **4xx errors that look client-side** — 400s with validation messages, 403s that suggest broken permission checks.
4. **Warnings that precede an error** — often the missing context.

Filter ruthlessly at this stage. If you surface 20 "issues", the user has to do the triage work themselves.

## Step 4: Map Errors to the Codebase

For the top 1–3 clusters, locate the relevant code in the current working directory.

**For JS stack traces:**

- Parse file paths out of the stack. Source maps may or may not be present — if the trace references `bundle.min.js:1:4523`, you won't get a direct file match. In that case, fall back to searching for the error message string.
- Use `Grep` to search for the error message text (quoted strings are usually copy-pasteable) and for function names from the stack.
- Use `Glob` to locate files by the basename in the stack.

**For HTTP errors:**

- Search for the request path (e.g. `/api/orders/:id`) in route definitions, controllers, API clients, and fetch/axios calls.
- Search for the response error message if the body includes one — these strings are often unique enough to find the throw site directly.

**When nothing maps:**

- If the stack is fully minified and the error message is generic (e.g. "undefined is not a function"), say so and ask the user whether they want to keep going with a best-guess search or provide a hint about which part of the app is involved.
- Don't invent a file location. If you aren't sure, say you aren't sure.

## Step 5: Propose a Fix

Once the offending code is located, read enough surrounding context to understand the bug, then propose a targeted fix.

Keep the fix minimal and scoped to the bug. Do not bundle refactors, style cleanup, or unrelated improvements — the user wants to close this ticket, not redesign the module.

Present the proposal before editing:

```
## Proposed Fix

**Issue**: {one-line description of the root cause}
**File**: {path}:{line}
**Change**: {brief summary — e.g. "Guard against null user before reading user.id"}

{short diff showing only the changed lines, with 2–3 lines of context}

**Why this fixes it**: {one or two sentences tying the change back to the devlog evidence}
```

Ask the user to confirm before applying the edit. If they approve, use `Edit` (or `Write` for new files) to make the change. If they want adjustments, iterate.

## Step 6: Verify and Prompt for PR

After applying the fix:

1. Run the project's type-checker and test suite if one exists (look for `package.json` scripts, `pytest`, `go test`, etc.). Don't guess at commands — only run ones you can see in the project config. If nothing is configured, skip this step and say so.
2. Summarize what changed and what remains untested (e.g. "the fix compiles and unit tests pass, but this code path isn't covered by a test").
3. Prompt the user to create a pull request. If the `create-pr` skill is available in their environment, suggest running it; otherwise give a brief `gh pr create` starter. If the triage started from a ticket, include the ticket reference in the suggested PR title/body so the link is preserved. Do NOT create the PR automatically — the user confirms when they're ready.

## Output Format

Structure the final report like this:

```
## Replay Triage: {sessionId or clipId}

**Session**: [View Replay]({replay_url})
**Devlog events analyzed**: {count} ({console_count} console, {network_count} network)

### Issues Found

1. **{Short title}** — {severity: Critical / Likely Bug / Warning}
   - Evidence: {console message or HTTP failure summary, with count if repeated}
   - Location: {file:line} (or "Could not locate in current codebase — see notes")
   - Fix: {proposed_fix_summary}

2. ...

### Applied Fix
{Only if the user confirmed. Show file(s) changed and a one-line description each.}

### Verification
{Type-check / test results, or a note that no checks were configured.}

### Next Step
Ready to open a PR? {suggest a PR creation skill if available, or a `gh pr create` starter}
```

Skip sections that don't apply. If no issues were located in the codebase, say so and stop at Step 4 — don't fabricate a fix.

## Rules

- **Start from a replay.** Accept either a replay URL directly or a ticket that contains one. If neither is supplied, ask before doing anything else.
- **Use whatever ticketing tool is actually available.** Don't hardcode to Jira — detect the ticket system from the reference (Jira key, GitHub issue URL, etc.) and use the matching MCP or CLI. If none is available for that system, ask the user to paste the replay URL.
- **Don't post back to the ticket.** Reading a ticket is fine. Adding comments, changing status, or transitioning it is the user's decision — never do it automatically.
- **Parse the URL yourself.** `devlogEvents` takes identifying fields as individual parameters — extract `subId`, `recordingSessionId`, `startTime`, `endTime` (or `clipId` for saved clips) out of the URL and pass them directly. Don't pass the raw URL.
- **Triage, don't dump.** Cluster events into 1–3 distinct issues, rank them, and present only the top ones. A 50-line list of raw logs is a failure.
- **Never guess at a file location.** If the stack trace is minified or the error is generic, say you can't map it rather than picking a plausible-looking file.
- **Minimal fixes only.** Scope changes to the bug in the replay. No unrelated refactors, comment cleanup, or style changes.
- **Confirm before editing.** Show the proposed diff and wait for approval. The user may want to adjust the approach or apply it themselves.
- **Don't open the PR.** Prompt the user to open it via an available skill or `gh pr create`. Opening a PR is a shared-state action that should always stay with the user.
