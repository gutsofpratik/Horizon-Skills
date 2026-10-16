---
name: account-health
description: Prepare for a customer call by synthesizing engagement, sentiment, and feedback from Pendo analytics. Use this skill whenever someone asks about account health, wants to prepare for a customer call, needs an account health report, asks about engagement or usage for a specific customer, or wants a summary of how an account is doing. Also trigger when users mention preparing for a QBR, checking on a customer, or reviewing an account before a meeting — even if they don't say "account health" explicitly.
---

# Account Health Analysis

Synthesize engagement metrics, feature usage, feedback, and NPS data to prepare for customer conversations.

## Parameters

- **account_name_or_id**: What the user provides — could be a partial name, full name, or exact account ID.
- **timeframe**: The time period for analysis (default: last 90 days).

## Step 0: Find and Confirm the Account

This is the most important step. Users often provide partial or ambiguous account names, and there may be many accounts with similar names. Never silently pick an account — always confirm with the user when there's any ambiguity.

### How to find the account

1. Use `searchEntities` with `itemType: ["Account"]` and the user's search term to find matching accounts.
2. If the search returns **exactly one result**, confirm with the user: show the account name and ID, plus a couple of key metadata fields, and ask "Is this the right account?"
3. If the search returns **multiple results**, present a disambiguation table so the user can pick the right one. For each result, fetch metadata using `accountQuery` to help the user tell them apart.

   **First, check what metadata is available** by calling `accountMetadataSchema` for the subscription. Then select the most useful fields from whatever is available, prioritizing these categories:

   **Always available (Pendo core):**
   - `metadata.auto.lastvisit` (last activity date)
   - `metadata.auto.firstvisit` (first activity date)

   **Agent metadata (usually available):**
   - `metadata.agent.is_paying` (paying status)
   - `metadata.agent.industry` (industry)
   - `metadata.agent.planname` or `metadata.agent.planlevel` (plan info)
   - `metadata.agent.name` (account display name)

   **Custom metadata (varies by customer):**
   - `metadata.custom.arr` (ARR)
   - `metadata.custom.da_visitors30` (visitors last 30 days)
   - `metadata.custom.csmassigned` (CSM)
   - `metadata.custom.da_subscriptiontype` (subscription type)

   **Salesforce metadata (only if Salesforce integration is active):**
   - `metadata.salesforce.account_name__c` (Salesforce account name)
   - `metadata.salesforce.arr__c` (ARR from Salesforce)
   - `metadata.salesforce.industry` (industry)
   - `metadata.salesforce.account_segment__c` (segment)
   - `metadata.salesforce.csm_assigned__c` (CSM)

   The goal is to show **3–5 meaningful fields per account** regardless of which integrations are active. If Salesforce fields are empty or unavailable, lean on agent and custom metadata instead — there's almost always enough there to differentiate accounts. The key signals for disambiguation are: paying status, visitor activity, recency, plan/tier info, and any identifying name or domain.

### Recommending the best match

Mark the most likely account with a ⭐ **Recommended** tag and include a brief explanation of why. Use these signals to determine the recommendation (in rough priority order):

- **Paying status**: Paying accounts are almost always the ones users care about. Check `metadata.agent.is_paying` or `metadata.custom.ispaying`.
- **Visitor count (30d)**: Higher recent activity indicates this is a real, active production account — not a test or legacy duplicate. Check `metadata.custom.da_visitors30` or similar fields.
- **Last active date**: More recent activity is better. Accounts last active years ago are probably stale. Use `metadata.auto.lastvisit`.
- **Has rich metadata**: Accounts with more populated metadata fields (whether from Salesforce, agent, or custom sources) are more likely to be the "real" account vs. orphaned duplicates.

When multiple signals agree (e.g., paying + high visitors + recent activity + rich metadata), the recommendation is strong. When signals conflict, explain the tradeoff so the user can make the call.

Example (with Salesforce integration):

```
I found several accounts matching "Acme". Which one(s) are you looking for?

1. ⭐ **Acme_Corp_Production** (ID: Acme_Corp_Production) — Recommended
   - SF Name: Acme Corporation | Paying: Yes | CSM: Jane Smith
   - Last Active: Feb 2026 | Visitors (30d): 1,200
   → *Recommended: paying account with by far the most active users*

2. **Acme_Corp_Staging** (ID: Acme_Corp_Staging)
   - SF Name: Acme Corporation | Paying: Yes | CSM: Jane Smith
   - Last Active: Feb 2026 | Visitors (30d): 16

3. **Acme_Corp** (ID: Acme_Corp)
   - Paying: No | No Salesforce data
   - Last Active: Jan 2026 | Visitors (30d): 0
```

Example (without Salesforce — using agent/custom metadata):

```
I found several accounts matching "Acme". Which one(s) are you looking for?

1. ⭐ **Acme_Corp_Production** (ID: Acme_Corp_Production) — Recommended
   - Paying: Yes | Plan: Enterprise | Industry: Technology
   - Last Active: Feb 2026 | Visitors (30d): 1,200
   → *Recommended: paying enterprise account with the most active users*

2. **Acme_Corp_Staging** (ID: Acme_Corp_Staging)
   - Paying: Yes | Plan: Enterprise
   - Last Active: Feb 2026 | Visitors (30d): 16

3. **Acme_Corp** (ID: Acme_Corp)
   - Paying: No | Plan: Free
   - Last Active: Jan 2026 | Visitors (30d): 0
```

### Multi-account selection

The user may want to analyze more than one account — for instance, a parent company with multiple sub-accounts (like "Acme_Corp_Production" and "Acme_Corp_Staging"). When presenting the disambiguation list:

- Let the user know they can **select multiple accounts** by listing the numbers (e.g., "1, 2, and 4").
- If they select multiple, generate a **single report with separate sections per account**. Each account gets its own full health analysis (engagement, usage, feedback, etc.), clearly labeled with the account name and ID.
- Add a brief **cross-account summary** at the top if multiple accounts are selected, highlighting any notable differences (e.g., "Acme_Corp_Production has 75x more active visitors than Acme_Corp_Staging").

   Only show metadata fields that actually have values — skip empty or null fields to keep it clean. The goal is to give the user enough context to confidently pick the right account(s) without overwhelming them.

4. If **no results** are found, let the user know and suggest alternative search terms or ask them to double-check the name.
5. **Do not proceed to the health report until the user has confirmed which account(s) to analyze.**

### Tips for disambiguation

- Show at most 10 results. If there are more, ask the user to narrow their search.
- Fields that are most useful for telling accounts apart: ARR, industry, segment, CSM name, and recent activity. Paying status also helps distinguish production accounts from test/demo ones.
- If the user provides what looks like an exact account ID (a long numeric string), you can skip the search and go directly to the report — but still show the account name for confirmation.

## Step 1: Collect Engagement Metrics

Once the account is confirmed, use Pendo tools to gather engagement data:

**Tools**: `activityQuery`, `productEngagementScore`

- Get the count of unique visitors for the account in the timeframe
- Get the count of unique visitors in the previous equivalent timeframe (for comparison)
- Identify the top 3 visitors by days active from this account
- Calculate PES (Product Engagement Score) if available

## Step 2: Collect Feature Usage Data

**Tools**: `activityQuery`, `searchEntities`

- Get top 3 pages by number of visitors from this account
- Get top 3 features by number of visitors from this account
- Identify any growth or decline trends

## Step 3: Collect Feedback Data

**Tools**: `generate_feedback_topics`, `get_feedback_insights`, `get_feedback_items`

- Group feedback from the account into topics
- Extract key insights and themes
- Note any alerts (Churn Risk, High Frustration, Blocker to Sale)

## Step 4: Collect NPS Scores

If NPS data is available, gather sentiment metrics:

**Tools**: `activityQuery` (with poll entity type)

- Get NPS score for the account in the timeframe
- Compare with previous period if available

## Output Format

### Single account report

Generate a structured account health report:

```
## Account Health Summary: {account_name}
**Account ID**: {account_id}
**Period**: {timeframe}

### Engagement Overview
- **Unique Visitors**: {count} (vs {previous_count} previous period) {↑/↓ % change}
- **Top Active Users**:
  1. {visitor_1} — {days_active} days active
  2. {visitor_2} — {days_active} days active
  3. {visitor_3} — {days_active} days active
- **PES Score**: {score}/100

### Feature & Page Usage
**Top Pages**:
1. {page_1} — {visitor_count} visitors
2. {page_2} — {visitor_count} visitors
3. {page_3} — {visitor_count} visitors

**Top Features**:
1. {feature_1} — {visitor_count} visitors
2. {feature_2} — {visitor_count} visitors
3. {feature_3} — {visitor_count} visitors

### Customer Feedback Themes
{feedback_topics_summary}

### Alerts & Risks
{any_flagged_items}

### Recommendations for Customer Call
{synthesized_recommendations}
```

### Multi-account report

When the user selects multiple accounts, produce a single report with this structure:

```
## Combined Account Health Report
**Accounts analyzed**: {account_1}, {account_2}, ...
**Period**: {timeframe}

### Cross-Account Summary
{Brief comparison highlighting notable differences — e.g., relative visitor counts, which accounts are most/least active, any shared feedback themes or divergent trends. Keep this to 3-5 sentences.}

---

## {account_1_name} (ID: {account_1_id})

### Engagement Overview
{... same structure as single account ...}

### Feature & Page Usage
{...}

### Customer Feedback Themes
{...}

### Alerts & Risks
{...}

---

## {account_2_name} (ID: {account_2_id})

{... repeat for each account ...}

---

### Combined Recommendations for Customer Call
{Synthesize recommendations across all accounts. Note which are account-specific vs. common themes.}
```

The cross-account summary at the top is important — it gives the user a quick read before diving into details, and helps them spot patterns across sub-accounts that they might miss looking at each one individually.

## Rules

- **Never skip account confirmation.** If the user's search returns more than one result, always present the options with a ⭐ Recommended tag and wait for them to choose. This is the single most important rule.
- **Always explain the recommendation.** Don't just star an account — briefly say why (e.g., "paying account with the most active users").
- **Support multi-account selection.** Let the user pick multiple accounts. When they do, produce separate report sections per account with a cross-account summary at the top and combined recommendations at the bottom.
- Always pass the confirmed `account_id` explicitly in all subsequent queries.
- Execute steps 1–4 in parallel when possible to save time. When analyzing multiple accounts, run all accounts' data collection in parallel too.
- Keep user-facing responses minimal outside the report — let the report speak for itself.
- Default timeframe is 90 days if not specified.
- If a data source returns no results (e.g., no feedback, no NPS), note it briefly in the report rather than leaving the section blank.
