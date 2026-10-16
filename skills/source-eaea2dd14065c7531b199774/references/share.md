# Share findings

Reached when the operator selects "Share findings" from the closing offer.

Use `AskUserQuestion` with two questions each session — no config is saved:

**Question 1** — `question: "Where should these findings go?"`, `header: "Destination"`, `multiSelect: true`, options: PDF, Email, Slack, Notion.

**Question 2** — `question: "What should be included? (Summary is always included.)"`, `header: "Include"`, `multiSelect: true`, options: Cause (Recommended), Fix (Recommended), Technical details.

**Per-destination follow-up** (check config for saved values first; collect all missing details before sending anything):
- PDF → no follow-up; save and confirm path
- Email → if not connected, trigger `suggest_connectors` (search registry for "gmail"); then "What email address?" (skip if saved)
- Slack → if not connected, trigger `suggest_connectors` UUID `597f662f-36de-437e-836e-5a81013cbfbe`; then "Which channel?" (skip if saved)
- Notion → if not connected, trigger `suggest_connectors` UUID `69f3a300-cc60-48c4-b237-dfac56530dbf`; then "Which page or database?" (skip if saved)

Once all details are confirmed, **write config via shell tool immediately** (merge into `share` key), then process all selected destinations in parallel.

---

## Generating the artifact

Content order: Summary → Technical details (if selected) → Cause (if selected) → Fix (if selected).

**Static-document rewrite required:**
- No "let me know if" / "want me to walk through" hooks
- No pause-for-direction text
- Alternative-fix mentions become static: "If the primary fix doesn't resolve, the alternative is [X]"
- Reasoning disclaimer becomes a single-line caveat at the top

**Per-channel:**
- **PDF** — `tech-diagnosis-[domain]-[date].pdf`. Confirm path after saving.
- **Email** — subject: `Tech findings for [domain] — [N] items to investigate`. HTML body, scannable.
- **Slack** — lead-in: `*Tech findings for [domain]* — [N] items, last [window].` One mrkdwn section per finding.
- **Notion** — title: `Tech findings for [domain] — [date]`. Sectioned page.

No console/replay URLs in any shared content. Issue IDs as plain identifiers are fine. Links only on explicit request.
