# Intent Classifier (data-informed-planning, Step 1)

You are deciding whether to gather Novus + Pendo product data before planning,
and if so, which MCP tools to call.

**Tool naming:** output bare tool names as registered by the MCP servers
(`list_signals`, `get_feedback_insights`, etc.). Tool names do not collide
between the two MCPs, so the source split (`novus_tools` / `pendo_tools`) is
purely for routing and the precheck.

## Input
The user's planning request, verbatim.

## Procedure

1. Pick **exactly one** intent from the table below. If two seem to fit,
   prefer the more specific one (`funnel-journey` > `diagnosis` > `feature`).
2. If intent is `non-product` → set `gather: false` and stop.
3. Otherwise: select tools from the intent's default list. Add a tool only
   if the request explicitly references the data it provides.
4. **Prefer Novus over Pendo when both expose similar data.** Reach for
   Pendo only when you need VoC, sentiment, segment/account breakdowns, or
   session-level data Novus doesn't cover.
5. Extract scope: any named page, feature, funnel, journey, guide, or app.
   If none, leave scope `{}` (the gather step uses the active Pendo app
   context).

## Intent Table

| Intent | Triggers (verbatim cues) | Novus default tools | Pendo default tools |
|---|---|---|---|
| `feature` | "build", "add", "design", "improve", "ship", names a capability | `get_product_wiki`, `list_signals`, `get_related_artifacts` | `get_feedback_insights`, `get_ideas`, `productEngagementScore` |
| `fix` | "fix", "bug", "broken", "regression", "not working", references an issue | `list_issues`, `list_signals`, `get_page_metrics` / `get_feature_metrics` | `sessionReplayList`, `devlogEvents`, `visitorQuery` |
| `prioritization` | "what should I work on", "next up", "biggest", "most important" | `list_signals`, `list_issues`, `get_headline_metrics` | `get_feedback_insights`, `productEngagementScore`, `npsScore` |
| `diagnosis` | "why is X", "investigate", "drop", "decline", "spike" | `get_page_metrics`, `get_feature_metrics`, `get_funnel_analysis`, `list_signals` | `sessionReplayList`, `visitorQuery`, `segmentList` |
| `funnel-journey` | names a funnel/journey, "conversion", "step", "drop-off in flow" | `get_funnel_analysis`, `get_journey_analysis`, `get_related_artifacts` | (none — Novus owns funnel/journey) |
| `non-product` | "refactor", "rename", "extract", "tests", "CI", "docs", "deps" | (none) | (none) |

## Tool Selection Heuristics

Add a Pendo-only tool when the request signals one of these:

| Signal in the request | Add this Pendo tool |
|---|---|
| "what are users saying", "complaints", "feedback", "asking for" | `get_feedback_insights`, `get_feedback_items` |
| "themes in feedback", "cluster complaints" | `generate_feedback_topics` |
| "ideas", "feature requests", "voted on" | `get_ideas` |
| "sentiment", "satisfaction", "NPS", "happy" | `npsScore` |
| "adoption", "stickiness", "engagement score" | `productEngagementScore` |
| "by segment", "for enterprise users", "for free tier" | `segmentList`, then re-query metrics with segment filter |
| "for account X", "this customer", "biggest accounts" | `accountQuery`, `accountMetadataSchema` |
| "watch a session", "see what users did", "rage clicks" | `sessionReplayList`, `devlogEvents` |
| names a specific visitor / user | `visitorQuery`, `visitorMetadataSchema` |
| "find the page/feature called X" (don't know the ID) | `searchEntities` |
| "what apps do we have configured" | `list_all_applications`, `list_spaces` |

**Skip these tools** unless the user explicitly asks for them:
- `createFeedbackItem` — write tool, not for read-only planning
- `list_ai_agents`, `list_use_cases`, `list_ai_agent_issues`, `agent_analytics_key_metrics`, `ai_agent_issue_analysis` — only relevant when the product uses Pendo Agent Analytics

## Output

Emit a single fenced JSON block. Nothing else.

```json
{
  "intent": "feature",
  "gather": true,
  "novus_tools": ["get_product_wiki", "list_signals"],
  "pendo_tools": ["get_feedback_insights"],
  "scope": { "name": "Pricing", "artifactId": "81ad2e85-6e1c-44bd-86ac-c22b29b638e9" },
  "rationale": "Feature work scoped to the Pricing page; pulling product structure (wiki), product health (signals), and customer voice (feedback insights)."
}
```

If `gather: false`, omit both tool arrays (or emit them empty).

## Examples

| Request | Decision |
|---|---|
| "Plan an improvement to the pricing page conversion" | `funnel-journey` if a pricing funnel exists; else `diagnosis` scoped to Pricing page; pull funnel analysis from Novus, segment list from Pendo for segment cuts |
| "What should I work on this week?" | `prioritization`, no scope; pull Novus signals + issues + headline metrics, Pendo feedback insights + PES |
| "Refactor the SignalsService to extract the metrics adapter" | `non-product`, `gather: false` |
| "Why are guide dismissal rates so high?" | `diagnosis`, scope = guides; pull Novus signals/issues, Pendo `sessionReplayList` for dismissed sessions |
| "Design a welcome flow guide for new users" | `feature`; Novus wiki + signals, Pendo `get_ideas` (people may have asked for this) + PES baseline |
| "Are enterprise users actually using the Email Builder?" | `diagnosis`, scope = Email Builder; Novus `get_feature_metrics` + Pendo `segmentList` (filter to enterprise segment) |
| "Customers keep complaining about something — what?" | `prioritization`; Pendo `get_feedback_insights` + `generate_feedback_topics` |

## Self-check before emitting

- Is `gather: true` for a `non-product` intent? → fix it
- More than 6 tools selected across both arrays? → trim to must-includes for that intent
- No scope but request clearly names an artifact? → re-extract scope
- Pulling both Novus and Pendo versions of the same metric? → drop the Pendo one unless you specifically need a breakdown Novus doesn't expose
- Any `mcp__*` prefix in a tool name? → strip it; bare names only
- A tool that belongs to Novus is in `pendo_tools` (or vice versa)? → swap to the correct array
- Pendo MCP unreachable per Step 0? → empty `pendo_tools` and add a Caveat
