---
name: feedback-analysis
description: Analyze customer feedback using Pendo's feedback tools — cluster themes, extract insights, and surface churn/frustration risks. Use whenever the user asks about feedback trends, top complaints, feature requests, Voice of the Customer, churn risks, or what customers are saying about a topic or account. Triggers on phrases like "feedback report", "what are customers asking for", "any red flags in sentiment", or "what's the feedback looking like". Requires Pendo connector.
---

# Feedback Deep Dive

Analyze customer feedback using Pendo's feedback tools to discover themes, extract actionable insights, and identify at-risk customers. This skill orchestrates three Pendo feedback tools — `Pendo:generate_feedback_topics`, `Pendo:get_feedback_insights`, and `Pendo:get_feedback_items` — into a comprehensive analysis. It also uses `Pendo:list_all_applications` to resolve subscription IDs and `Pendo:searchEntities` to look up account IDs by name.

## When to Use This Skill

Any time the user wants to understand customer feedback: broad themes, specific topic deep-dives, risk identification, account-level feedback, or feedback filtered by type/alert/timeframe.

## Parameters

The user's request may include any combination of these filters. If they don't specify, use sensible defaults (last 90 days, no filters).

- **search_term**: A topic to search for (e.g., "onboarding", "performance", "mobile app"). Uses semantic similarity matching, not exact string matching, so conceptual matches will be found.
- **account_id**: Narrow to a specific account's feedback
- **feedback_type**: One of: Product Enhancement Request, Product Issues, Pain Point, Positive Product Feedback, Competitor Weakness, Competitor Strength
- **alerts**: Filter by alert flags: Churn Risk, High Frustration, Blocker to Sale
- **account_type**: Customer, Prospect, or Churned
- **timeframe**: Date range to analyze (default: last 90 days — startDate 90 days ago, endDate today)

## Prerequisites

Before running feedback queries, you need the user's Pendo subscription ID. Use `Pendo:list_all_applications` to get it. If the user has multiple subscriptions, ask which one to use.

## Workflow

### Step 1: Resolve Filters

Parse the user's request into concrete filter values. Calculate startDate/endDate from any timeframe mention (e.g., "last quarter" → startDate: 2025-10-01, endDate: 2025-12-31). If the user mentions an account by name but you don't have the ID, use `Pendo:searchEntities` with itemType ["Account"] to find it.

Build a `feedbackFilters` object that will be reused across all three feedback tools:

```json
{
  "startDate": "YYYY-MM-DD",
  "endDate": "YYYY-MM-DD",
  "similaritySearchTerms": ["topic if provided"],
  "accountIds": ["id if provided"],
  "feedbackTypes": ["type if provided"],
  "alerts": ["alert if provided"],
  "accountTypes": ["type if provided"]
}
```

Key distinction on search terms:
- Use `similaritySearchTerms` when the user describes a topic conceptually (e.g., "feedback about performance" → `["performance"]`). This does semantic matching and will find related feedback even if it doesn't contain the exact word.
- Use `exactMatchSearchTerms` only when the user explicitly wants exact phrase matching (e.g., "feedback that mentions the word 'latency' exactly").

### Step 2: Generate Feedback Topics

Call `Pendo:generate_feedback_topics` with the feedbackFilters. This clusters all matching feedback into AI-generated themes and returns topic names, descriptions, and counts. This gives you the high-level landscape of what customers are talking about.

This is a slow-running tool — let the user know you're working on it.

### Step 3: Get Insights and Raw Feedback (Parallel)

Run these in parallel since they're independent:

**Insights**: Call `Pendo:get_feedback_insights` with the same feedbackFilters. Returns distilled, actionable insights — each with a summary, explanation of why it matters, and a supporting quote from actual feedback.

**Raw Feedback**: Call `Pendo:get_feedback_items` with the same feedbackFilters. Returns up to 30 actual feedback items with titles, descriptions, account/visitor info, types, and alerts.

**Risk Signals**: Call `Pendo:get_feedback_items` again, but add alert filters for ["Churn Risk", "High Frustration", "Blocker to Sale"] (merged with any existing filters). This surfaces the most urgent feedback that needs attention. Skip this call if the user already filtered to a specific alert type, since it would be redundant.

### Step 4: Synthesize the Analysis

Combine all results into a coherent report. The structure below is a guide — adapt it based on what data came back and what the user asked for. If the user asked a narrow question (e.g., "any churn risk feedback?"), don't pad the response with irrelevant sections.

## Output Format

### Feedback Analysis Report

**Scope**: Summarize what filters were applied (e.g., "All customer feedback about onboarding, last 90 days")
**Period**: The date range analyzed
**Total Feedback**: Count from raw feedback results (note if capped at 30)

#### Top Themes

Present the topic clusters from generate_feedback_topics as a table:

| # | Theme | Description | Count |
|---|-------|-------------|-------|
| 1 | {topic} | {description} | {count} |

#### Key Insights

For each insight, present:

**{insight summary}**
> "{supporting quote}"

{Why this matters / explanation}

#### Risk Alerts

Group the risk-flagged feedback by alert type. For each, show the account name, a brief summary of their feedback, and the date. This section is critical — churn risks and high frustration should be immediately visible. If there are no risk alerts, say so (that's good news worth reporting).

#### Feedback Breakdown by Type

Summarize counts by feedback type (Product Enhancement Request, Product Issues, Pain Points, Positive Feedback, Competitor mentions) based on the raw items retrieved.

#### Recommendations

Based on the themes, insights, and risk signals, provide 2-4 actionable recommendations. Connect each recommendation to specific evidence from the feedback. For example, if multiple accounts mention slow report generation, recommend investigating performance and name the accounts affected.

## Tips for Great Analysis

- If searching for a topic returns no results, suggest the user broaden their search or try related terms. Semantic search is forgiving, but very niche terms might not match.
- When presenting quotes from feedback, keep them brief and impactful — they add credibility to insights.
- If a specific account appears across multiple risk categories, call that out explicitly — it's a strong signal.
- For account-specific analysis, consider mentioning the account type (Customer vs Prospect) since the appropriate response differs.
- The raw feedback endpoint caps at 30 items. If 30 items are returned, note that there may be more matching feedback beyond what's shown.
