---
name: status
description: Show a compact service health overview including active incidents by severity. Use for a quick health check of your services.
argument-hint: [service-name]
disable-model-invocation: true
allowed-tools:
  - mcp__rootly__*
---

# Service Health Overview

You are showing the user a compact view of current service health based on active incidents.

## Workflow

### 1. Fetch Active Incidents

Call `mcp__rootly__search_incidents` filtered to active status (`started`).

If `$ARGUMENTS` contains a service name, filter to that service.

### 2. Present Health Dashboard

Group incidents by service and severity. Present as a compact table:

```
## Service Health

| Service | Critical | High | Medium | Low | Oldest Active |
|---------|----------|------|--------|-----|---------------|
| [name]  | [count]  | [count] | [count] | [count] | [duration] |
| ...     | ...      | ...  | ...    | ... | ...           |

**Total active incidents**: [count]
```

If no active incidents are found, report:

```
## Service Health

All clear -- no active incidents.
```

Keep the output concise. This is a quick health check, not a detailed report.
