# Output Template, Scoring Rubric, Worked Example

## Required review output structure

```markdown
# Prompt Review

## Executive Summary

- Overall status: Ready / Needs revision / Do not deploy
- Main risk
- Highest-severity issue
- Confidence level

## Findings

### 1. [Severity] Issue title

**Category:** Contradiction / Missing context / Tool-action / Transfer-escalation / Compliance-safety / Regression risk / Output quality / Prompt structure / Mechanical limit

**What I found:** ...
**Why it matters:** (likely failure in a real call) ...
**Recommendation:** (exact fix or rewrite direction) ...
**Suggested replacement text:** (when useful) ...

## Missing Information

List what's needed to complete the review: available tools/actions and their UI descriptions, transfer targets, business policies, compliance rules, old prompt (if reviewing an edit), target language/market, example calls, token count.

## Regression Risks

(Use when reviewing edits.)

| Risk | Severity | Why it matters | Suggested test |
|---|---:|---|---|

## Recommended Tests

At least: 1) happy path, 2) edge case, 3) tool empty-result, 4) tool failure, 5) escalation/transfer, 6) out-of-scope request, 7) compliance-sensitive request.

## Suggested Improved Prompt

Only when the user asks or fixes are small and safe. Preserve intent and business logic.
```

## Optional scoring rubric

| Dimension | Score | Notes |
|---|---:|---|
| Business context | 1-5 | Is the agent role and business context clear? |
| Behavioral specificity | 1-5 | Are steps, conditions, and success states clear? |
| Tool/action safety | 1-5 | Are triggers, arguments, descriptions, and failures handled? |
| Escalation/fallback readiness | 1-5 | Are transfer, fallback, and end-call paths safe? |
| Compliance/safety | 1-5 | Are industry and data risks controlled? |
| Voice output quality | 1-5 | Is the agent concise and natural for calls? |
| Mechanical hygiene | 1-5 | Tool count, token length, variable/cache discipline, rules placement. |
| Regression safety | 1-5 | Are edits safe and testable? |

Use scores to support the review, not replace findings.

## Worked example finding

```markdown
### 1. [High] Booking tool can be called before the caller confirms details

**Category:** Tool-action

**What I found:**
The prompt uses `book_appointment` after the caller gives a preferred time, but never requires reading back date, time, service type, and name before booking.

**Why it matters:**
The agent may create incorrect appointments, especially when speech recognition mishears dates or times.

**Recommendation:**
Require explicit confirmation immediately before the booking tool call.

**Suggested replacement text:**
Before using `book_appointment`, read back the caller's name, service type, date, and time. Ask: "Is that correct?" Only call `book_appointment` after the caller confirms.
```
