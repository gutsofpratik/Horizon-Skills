---
name: check-usage
description: Reports the Hunter account's plan, remaining credits, and usage. Use when the user asks how many credits they have left, what plan they're on, or how much of their quota they've used.
user-invocable: true
argument-hint: How many credits do I have left?
---

# Check Usage

Read-only view of the account's plan, credits, and usage. No credits consumed, no changes made.

## Examples

- `/hunter:check-usage How many credits do I have left?`
- `"What plan am I on?"`
- `"How many searches have I used this month?"`
- `"Show my account details"`

## Steps

1. **Read the account** → `Get-Account-Details` for plan and reset date; `Get-Usage` for search/verification consumption and what's remaining. Neither tool returns a team name — don't show one.

2. **Present a clear summary — show what's REMAINING, not the allowance.** Use `requests.credits.remaining` when the account has a single credits bucket; otherwise compute `available - used` per bucket. (`available` is the period allowance plus packs, not what's left.)

```
# Account Usage

| | Used | Remaining | Resets |
|--|------|-----------|--------|
| **Searches** | 320 | 180 | 2026-08-01 |
| **Verifications** | 140 | 860 | 2026-08-01 |

**Plan:** Starter
```

3. **If the user is close to a limit,** flag it: "You've used 90% of your monthly searches — they reset on [date]."

## Credit Cost

Free — reading account details and usage consumes no credits.

## Important Notes

- Read-only. This skill never creates API keys, changes the plan, or edits account settings — those stay in the Hunter dashboard.
- Handy as a pre-check before running bulk verification or enrichment.
