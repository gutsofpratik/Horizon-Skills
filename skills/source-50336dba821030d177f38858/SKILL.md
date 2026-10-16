---
name: feature-adoption
description: Analyze feature adoption rates, identify power users vs laggards, and track adoption trends using Pendo analytics. Use this skill whenever someone asks about feature adoption, feature usage, who's using a feature, adoption rates, feature rollout progress, or wants to understand how a specific feature is performing. Also trigger when users mention tracking a feature launch, finding champions or power users of a feature, identifying accounts that haven't adopted a feature, comparing adoption across segments, or analyzing usage trends over time — even if they don't say "adoption" explicitly. If someone asks "who's using X" or "how is feature Y doing", this is the right skill.
---

# Feature Adoption Analysis

Analyze how features are being adopted across your user base, identify champions and laggards, and track adoption trends over time.

## Tools

This skill uses **Pendo MCP tools** exclusively. All tool references below (e.g., `searchEntities`, `activityQuery`, `segmentList`, `visitorQuery`) refer to the Pendo connector tools (prefixed `Pendo:` in the tool list).

Before starting, call `Pendo:list_all_applications` to get the available subscription IDs and app IDs. Every subsequent Pendo tool call requires a `subId` (subscription ID) and most require an `appId`. If the user hasn't specified which app or subscription to use and there are multiple options, ask them to confirm before proceeding.

## Parameters

- **feature_name**: The feature to analyze. Can be a partial name, exact name, or feature ID.
- **timeframe**: The time period for analysis (default: last 30 days).
- **comparison_period**: Optional previous period for trend analysis (defaults to the equivalent prior period).

## Step 0: Find and Confirm the Feature

Users often provide partial or ambiguous feature names. Never silently pick a feature — always confirm when there's any ambiguity.

### How to find the feature

1. Use `Pendo:searchEntities` with `itemType: ["Feature"]` and the user's search term to find matching features.

2. If the search returns **exactly one result**, confirm with the user: show the feature name, ID, and any relevant metadata, and ask "Is this the right feature?"

3. If the search returns **multiple results**, present a disambiguation list so the user can pick the right one. For each result, show:
   - Feature name and ID
   - Tagged app (if available)
   - Any description or page association

   Mark the most likely feature with a ⭐ **Recommended** tag based on:
   - Whether it belongs to the user's primary app
   - Whether it has recent activity
   - Name similarity to the search term

   Example:
   ```
   I found several features matching "dashboard". Which one are you looking for?

   1. ⭐ **Dashboard Main View** (ID: abc123) — Recommended
      - App: Web App | Last active: Feb 2026
      → *Closest name match with recent activity*

   2. **Dashboard Settings Panel** (ID: def456)
      - App: Web App | Last active: Jan 2026

   3. **Admin Dashboard** (ID: ghi789)
      - App: Admin Portal | Last active: Feb 2026
   ```

4. If **no results** are found, let the user know and suggest alternative search terms or ask them to double-check the name.

5. **Do not proceed to the adoption report until the user has confirmed which feature to analyze.**

## Step 1: Collect Adoption Metrics

Once the feature is confirmed, gather core adoption data. Run these queries together to save time:

**Tools**: `Pendo:activityQuery`

- **Unique visitors** who used this feature in the timeframe
- **Unique accounts** with users of this feature
- **Total event count** for the feature
- **Previous period metrics** for the same duration (for trend comparison)

When constructing activity queries, filter by the confirmed feature ID and use the appropriate time period. Request both `numVisitors` and `numEvents` where possible.

## Step 2: Identify User Segments

Understand who is and isn't using the feature:

**Tools**: `Pendo:activityQuery`, `Pendo:visitorQuery`

- **Power Users (Champions)**: Top 10 visitors by event count for the feature. These are your best candidates for case studies, beta testing, and internal advocacy.
- **Recent Adopters**: Visitors who first used the feature in the last 7 days. Useful for understanding current momentum.
- **Top Accounts**: Accounts with the most feature users, ranked by unique visitor count.

For each power user, try to include their account name so the data is actionable. The `Pendo:activityQuery` grouped by `visitorId` may not always return a clean account name — if needed, cross-reference by running a separate `Pendo:activityQuery` grouped by `accountId` for the same feature to get account-level context, or infer the account from the visitor's email domain.

## Step 3: Calculate Adoption Rate

Compare feature users against the total active user base to get a meaningful adoption percentage:

**Tools**: `Pendo:activityQuery`, `Pendo:segmentList`

1. Get total unique active visitors across the entire product in the same timeframe.
2. Calculate adoption rate: `(feature users / total active visitors) × 100`
3. If segments are available (via `Pendo:segmentList`), calculate adoption rate per segment for additional insight — this often reveals that adoption is strong in one segment but weak in another. Note: some subscriptions have thousands of segments, which will cause `Pendo:segmentList` to fail without a substring filter. If this happens, note in the report that segment-level breakdown is available if the user specifies a segment of interest, and move on — don't let this block the rest of the report.

The adoption rate relative to *active* users is more useful than against *all* visitors, since inactive users aren't a realistic adoption target.

## Step 4: Analyze Trends

Look at how adoption is changing over time:

**Tools**: `Pendo:activityQuery`

- Query daily or weekly unique visitors for the feature over the timeframe
- Identify growth or decline patterns
- Note any significant spikes (possible correlation with launches, guides, or announcements) or drops (possible bugs, UX issues)
- Compare the current period's total against the previous period to calculate percent change
- **Partial periods**: The first or last week/day in a trend may be incomplete (e.g., a 30-day range ending mid-week). Flag partial periods in the report so the user doesn't misread a shorter bucket as a decline.

If the timeframe is 14 days or less, use daily granularity. For longer periods, use weekly.

## Output Format

Generate a structured feature adoption report:

```
## Feature Adoption Report: {feature_name}
**Feature ID**: {feature_id}
**Period**: {timeframe}

### Adoption Overview
- **Total Users**: {unique_visitors} visitors across {unique_accounts} accounts
- **Adoption Rate**: {adoption_rate}% of active users ({feature_users} / {total_active_users})
- **Total Events**: {event_count} interactions
- **Trend**: {trend_direction} ({percent_change}% vs previous period)

### Power Users (Champions)
| Rank | Visitor | Account | Events |
|------|---------|---------|--------|
| 1    | {visitor_1} | {account_1} | {events} |
| 2    | {visitor_2} | {account_2} | {events} |
| ...  | ...     | ...     | ...    |

### Top Accounts by Adoption
| Rank | Account | Users | Events |
|------|---------|-------|--------|
| 1    | {account_1} | {user_count} | {events} |
| 2    | {account_2} | {user_count} | {events} |
| ...  | ...     | ...   | ...    |

### Adoption Trend
{weekly_or_daily_trend_summary — describe the trajectory in words, noting any inflection points}

### Segment Adoption (if available)
| Segment | Adoption Rate | Users |
|---------|--------------|-------|
| {segment_1} | {rate}% | {count} |
| ...     | ...          | ...   |

### Insights & Recommendations
- {insight based on the data — e.g., "Adoption is concentrated in 3 accounts, suggesting broad rollout hasn't happened yet"}
- {actionable recommendation — e.g., "Consider targeting accounts with high overall activity but zero feature usage for outreach"}
- {trend insight — e.g., "Week-over-week growth has been steady at ~5%, indicating organic discovery"}
```

## Rules

- **Never skip feature confirmation.** If the search returns more than one result, always present options with a ⭐ Recommended tag and wait for the user to choose. This is the most important rule.
- **Always explain the recommendation.** Don't just star a feature — briefly say why.
- Always pass the confirmed feature ID explicitly in all subsequent queries.
- Default timeframe is 30 days if not specified.
- Calculate adoption rate relative to total *active* users, not all visitors — this gives a more honest and useful number.
- When identifying power users, include their account name so the data is actionable for outreach.
- If a query returns no results (e.g., zero usage, no segments), note it briefly in the report rather than leaving the section blank. Zero adoption is itself a meaningful finding.
- Provide actionable recommendations based on the data — not generic advice but specific next steps tied to what the numbers show (e.g., which accounts to target, whether to invest in guides or announcements).
- If the user asks about multiple features, generate separate reports for each, with a brief comparison summary at the top.
