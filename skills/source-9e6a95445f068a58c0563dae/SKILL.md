---
name: deploy-check
description: "[experimental] Evaluate deployment risk by analyzing code changes against incident history, active incidents, and on-call readiness. Forked-subagent flow may not have MCP access in all Claude Code contexts."
argument-hint: [branch-name]
disable-model-invocation: true
context: fork
agent: rootly:deploy-guardian
allowed-tools:
  - Bash
  - mcp__rootly__*
---

# Pre-Deploy Safety Check (experimental)

> **Experimental**: this skill uses `context: fork` to delegate to the `deploy-guardian` agent. In some Claude Code contexts the forked subagent does not inherit the plugin's MCP tools. If the agent reports MCP tools unavailable, run `/rootly:status` to manually check active incidents before deploying.

You are evaluating whether it is safe to deploy the current code changes. Follow this workflow carefully.

## Current changes
!`git diff --stat HEAD`

## Current branch
!`git branch --show-current`

## Recent commits
!`git log --oneline -5`

## Workflow

### 1. Assess Changes

Review the git diff output above. If the diff is empty (no changes), report "No changes to evaluate -- working tree is clean" and stop.

Identify which files and components are affected by the changes.

### 2. Resolve Affected Services

Determine which Rootly service(s) these changes map to, using this resolution chain (in priority order):

1. **Check `.claude/rootly-config.json`** in the project root -- if it exists, use the `services` field
2. **Match repo name**: Use the git repo name (from `basename $(git rev-parse --show-toplevel)`) to search for matching Rootly services via `mcp__rootly__search_incidents`
3. **Ask the user**: If neither method works, ask which service(s) this repo maps to

### 3. Search Incident History

Call `mcp__rootly__search_incidents` for the identified services, looking at the last 90 days. Note any patterns in frequency, severity, or root causes.

### 4. Find Related Incidents

Call `mcp__rootly__find_related_incidents` with a summary of the current changes (based on the diff). This uses TF-IDF similarity matching to find historically similar incidents.

If results have confidence scores below 0.3, flag them as low confidence and note that manual review may be needed.

### 5. Check Active Incidents

Call `mcp__rootly__search_incidents` filtered to active (`started`) status for the affected services. Pay special attention to P1/P2 (critical/high severity) incidents.

### 6. Check On-Call Readiness

Call `mcp__rootly__get_oncall_handoff_summary` to verify:
- Who is currently on-call
- When the next handoff is
- Whether there are any on-call gaps

### 7. Synthesize Deployment Brief

Present a structured deployment brief:

```
## Deployment Safety Brief

**Risk Level**: [LOW / MEDIUM / HIGH / CRITICAL]
**Branch**: [branch name]
**Changed files**: [count]

### Active Incidents
[List any active incidents on affected services, or "None"]

### On-Call Status
- **Current**: [name] (since [time])
- **Next handoff**: [time]
- **Status**: [Available / Gap detected / High fatigue]

### Similar Past Incidents
[Top 3 similar incidents with what happened and how they were resolved]

### Risk Factors
[Bullet list of specific risks identified]

### Recommendation
**[GO / CAUTION / NO-GO]**: [1-2 sentence reasoning]
```

**Risk level criteria**:
- **LOW**: No active incidents, no similar past incidents, on-call is healthy
- **MEDIUM**: Minor past incidents found, or on-call handoff is imminent
- **HIGH**: Active incidents on related services, or recurring pattern of similar incidents
- **CRITICAL**: Active P1/P2 incident on the affected service, or significant on-call gaps
