---
name: daily-visitor-brief
description: >
  Build a prioritised daily brief of website visitor companies from Leadfeeder, ranked by ICP fit and engagement signal. Use this skill when the user asks "what should I work on today", "show me today's visitors", "daily brief", "who visited my site", "show me hot leads", "morning prospecting", "any good leads today", "Leadfeeder brief", or any morning-prospecting question grounded in Leadfeeder visitor data.
metadata:
  version: "1.0.0"
---

# Daily Visitor Brief

Produce a ranked, scannable brief of the most actionable website visitor companies for the user's outbound day. Anchor every recommendation in real visitor intent data from Leadfeeder. This is a read-only morning ritual: no writes, no enrichment jobs.

## Language

Produce the **entire response in the language the user wrote in** — English request → English output, German request → German output, and so on. This applies to everything the skill emits: the summary, the Trend line, all field labels, reasoning / why-now lines, edge-case messages, and the credit-consumption warning and confirmation. Do **not** translate data values — company names, contact names, URLs, page paths, email addresses, tag names, and ICP names stay verbatim as the tools return them. Copy-paste follow-up prompts should also be written in the user's language (they still trigger the right skill). If the input language is unclear, default to English.

## When this skill triggers

Trigger on any prompt that asks "who visited", "what should I work on", "daily brief", "morning prospecting", or "hot leads" in the context of Leadfeeder. Trigger silently — do not ask the user to confirm. Honor any explicit modifiers in the prompt (time window, ICP filter, result count).

## Inputs to determine before executing

Identify these from the user's prompt. Use defaults if unspecified — do not ask.

- **Time window** — default last 24 hours. Honor explicit overrides ("last 3 days", "this week", "since Monday", "yesterday").
- **Max results** — default top 10. Honor explicit overrides ("top 5", "top 20").
- **ICP / Persona filter** — default: use all configured ICPs and personas. Honor explicit overrides ("for my Enterprise ICP", "matching the SDR persona", "only Tech sector").

## Workflow

Execute these tool calls in order. Tools are exposed by the locally-connected Leadfeeder MCP server.

### Step 0 — Resolve the Leadfeeder account (before any other tool call)

Determine the `account_id` to use for every tool call in this skill, in priority order:

1. **Account named in the request (highest priority).** If the prompt or scheduled-task instruction explicitly names an account — an account ID (e.g. "account 01234") or an unambiguous account name — use that account for all tool calls. This overrides every source below and is the recommended way to make an unattended/scheduled task fully self-contained.
2. **Configured Account ID.** Otherwise, the plugin's configured Leadfeeder Account ID is: `${user_config.account_id}`. If that resolves to a real, non-empty account ID (not blank, and not the literal unsubstituted `${user_config.account_id}` token), use it for all tool calls and do **not** call `get_account_info` or ask the user.
3. **Already selected this session.** Otherwise, if an account was already chosen earlier in the session, reuse that.
4. **Fallback.** Otherwise call `get_account_info`. If exactly one account is returned, use it. If several are returned, ask the user to pick. When running unattended (e.g. a scheduled task) asking is impossible — if no account was named and none is configured, stop and report that a **Leadfeeder Account ID** must either be named in the task prompt or set in the plugin configuration for automated runs.

### Step 1 — Load ranking context (always re-fetch, never cache across runs)

Call `get_icps` to retrieve the user's configured ICPs. If the user is asking about a specific ICP, also call `get_icp` for that one to read its criteria. Call `get_buyer_personas` so persona context is available if relevant.

**Always re-fetch on every invocation of this skill.** Do NOT reuse ICPs or personas cached earlier in the session. Users update ICP and persona criteria in the Leadfeeder platform mid-session, and a stale cache produces incorrectly-filtered briefs (e.g. surfacing "no ICP matches" when the criteria have just been widened). The `get_icps` and `get_buyer_personas` calls do not consume credits, so re-fetching is free.

### Step 2 — Fetch visitor companies in the time window

Call `get_web_visits_companies` with the date range computed from the user's time window. Request roughly 2.5× the target result count (e.g. `page_size=25` when the user asked for top 10) so you have enough candidates to rank.

**Do NOT pass `include=company`.** It inflates the response 10x+ (one page can exceed 75 KB) and risks hitting context limits. Always fetch firmographics separately via `get_company` in Step 4. Keep `get_web_visits_companies` lean.

**Known limitation:** `get_web_visits_companies` does not return engagement metrics on the record itself (no session count, no page depth, no dwell time). To rank by engagement depth you must chain `search_web_visits` per company.

**Subscription context (important).** The companies returned by `get_web_visits_companies` are part of the user's active record subscription. **All read endpoints against them are subscription-covered** — `get_company`, `get_company_financials`, `search_web_visits`, and `search_companies_signals`. No incremental credit cost. You may fetch deep details across all visitors in the brief, not just the top 3. Credits only apply to enrichment **jobs** (`create_company_enrichment_job`, `create_find_contact_data_job`), which this skill does not invoke.

If the API supports filtering by ICP at the query level, apply the user's ICP filter here. Otherwise filter in Step 3.

### Step 3 — Rank candidates (intent × ICP matrix)

Order the brief by **intent-score tier crossed with ICP match**, in this exact priority — this is the top-down order the reader wants:

1. **🟢 High intent + ICP match**
2. **🟠 Medium intent + ICP match**
3. **🟢 High intent + no ICP match**
4. **🟠 Medium intent + no ICP match**
5. **⚪️ Low intent + ICP match**
6. **⚪️ Low intent + no ICP match**

Within each tier, break ties by: **re-engagement** (a re-engaged company first — see "Re-engagement detection"), then **engagement** (sessions / pages / time on page), then **recency**, then **persona alignment**.

**Data dependency (important).** This ordering needs each candidate's **intent tier** and **ICP verdict**, and both come from `get_company` (`attributes.intent.score_tier` + firmographics scored against the ICPs). So run `get_company` across the **candidate pool** (the ~2.5× set from Step 2), not just the final top N — it's subscription-covered (free) for visitor companies — apply the matrix, then take the top N. This means Step 4's enrichment effectively happens here for the pool; Steps 5–6 then add visit detail and signals for the top N only.

**Not-yet-scored companies:** slot by ICP match using engagement as the proxy — an ICP-matched unscored company sits around tier 2 (medium + ICP), a non-matched unscored one around tier 4 — and label it "not yet scored" on the card rather than inventing a tier.

Take the top N after ranking.

### Re-engagement detection

A **re-engaged** company is one that visited inside the current window *after a gap of silence*. Companies that visited 30–90 days ago and are back now are textbook high-intent, returning companies — a primary intent signal. Detect it from the wider visit history pulled in Step 5:

- Find the most recent visit **before** the current window (the prior session).
- Compute the gap between that prior session and the earliest visit inside the current window.
- **Gap ≥ 30 days → flag as re-engaged.** Capture the gap length in days for the badge (e.g. "last session was 45 days ago").
- Gap < 30 days, or continuous week-over-week activity → not re-engaged; no badge.
- No prior visit at all in the history window → this is a *new* company, not a re-engagement. Do not flag (a "first-time visitor" note in Why now is fine, but that is not the re-engagement badge).

Only surface the badge when the gap is real and computed from `search_web_visits` data. Never estimate or invent a gap.

### Step 4 — Enrich every visitor in the brief

**Credit-consuming-tool flag — use this reassuring framing, not the generic alarm.** `get_company` and `search_companies_signals` are marked credit-consuming by the MCP, so acknowledge them once, up front, and get a single go-ahead for the whole batch (not per company). But for *this* skill the companies come from the Web Visitors feed — they are already inside their 12-month access window — so records already unlocked in the last 12 months incur **no charge**. Flag it accurately and reassuringly, roughly:

> To build your brief, I need to pull firmographics and signals for the {N} companies using `get_company` and `search_companies_signals`. These are credit-consuming tools. Since these companies were identified through Web Visitors, their 12-month access window has already started — no credits are charged for records already unlocked within the last 12 months.

Do **not** use the generic "may consume 1 credit per company if not accessed in the last 12 months" wording here — for visitor companies that misrepresents the reality and needlessly alarms the user. After the go-ahead, report the actual `meta.credits.charged` (expected: 0 for already-unlocked records).

For every candidate company (the pool from Step 2 — needed for the intent × ICP ranking in Step 3), call `get_company` with `include=crm_connections.crm_record.crm_owner,tags` to retrieve firmographics, full CRM connection detail (if any), and assigned tags. These companies are subscription-covered — fetch freely across all candidates, not just the top 3.

**Capture from the response:**

- Firmographics: industry, employee count, location, B2B/B2C, founded year, revenue.
- **Intent score and tier** — read from the `get_company` (`CompanyV1`) response at **`attributes.intent.score`** (0–10 decimal, may be `null`) and **`attributes.intent.score_tier`** (`high` / `medium` / `low`). It is nested under `attributes` — not a top-level `intent.score` — so read the full path or you'll get nothing. This field exists **only** on `get_company`; the `get_web_visits_companies` list (Step 2) returns lightweight `company_location` records with no intent, so you must have called `get_company` (Step 4) to have it. If `attributes.intent.score` is `null`, the company isn't scored yet — show "Intent score: not yet scored" rather than dropping the line. These are first-class signals — surface them on every card. **Prefix the displayed score with a tier dot by `score_tier`: 🟢 high · 🟠 medium · ⚪️ low** (omit the dot when "not yet scored").

  **You already have the payload — read it, don't default.** The Firmographics line comes from this same `get_company` response, so if you filled Firmographics in, the response is in hand and `attributes.intent.score` is right there. Extract it. Only write "not yet scored" when that exact field is genuinely `null`/absent in the payload — never as a fallback because the path wasn't checked. (Whole-account "not yet scored" across every card is a red flag that the path is being read wrong, not that no company is scored.)
- **CRM connections (sideloaded)**: use `include=crm_connections.crm_record.crm_owner` (plain `include=crm_connections` returns only a stub — `crm_record` as `{id, type}` with no name, URL, or owner). A populated `relationships.crm_connections` means the company is in the CRM. Each `crm_record` is JSON:API-shaped and **polymorphic** (`crm_record.type` = `crm_organization` | `crm_contact` | `crm_lead`): read **URL** from `crm_record.attributes.crm_url`; **name** by type (`crm_organization` → `attributes.name`; `crm_contact`/`crm_lead` → `attributes.first_name` + `attributes.last_name`); **owner** from `crm_record.relationships.crm_owner.attributes.name` (say "owner not set" if only a stub). **Render as a markdown link** — the record name is the clickable text and `crm_record.attributes.crm_url` is the target (e.g. `[Acme Corp](https://…crm_url…)`); never print the raw URL or leave the name unlinked. Surface this on the card.

- **ICP match — capture the exact ICP name(s).** When scoring a company against the configured ICPs (from Step 1), record *which* ICP(s) it matched by name (e.g. "DACH-Enterprise"), not just yes/no. Surface the exact name on the card — when several ICPs are configured, this tells the rep which motion the account belongs to and who should own it. If it matches more than one, list them; if none, it's "No ICP match".
- **Tags (sideloaded via `include=tags`)**: capture each assigned tag's `attributes.name` and `attributes.color`. Note: `color` is an integer palette **index** (0–N), not a hex code — the API doesn't expose the hex, and a plain markdown brief can't render background-filled chips anyway. So surface tags as plain-text chips (backtick `` `Hot Lead` `` style) using their **names**; do not invent a colour. Show tags because customers use them to prioritise accounts, so they inform the next best action.

**Ignore `web_engagement.last_visit_date` on the company profile.** This field lags the actual visits stream and was observed to be stale by days vs. real visits surfaced through `search_web_visits`. Treat the visits stream (Step 5) as the source of truth for visit timing. Use `get_company` only for firmographics, intent score, and CRM data — not for visit recency.

`get_company_financials` is subscription-covered for visitor companies — no incremental credit charge. Don't call it by default not because of cost, but because `get_company` already returns the headline revenue figure (sufficient for a morning brief). Call it on explicit request ("include financials", "balance sheet").

### Step 5 — Pull visit detail for every visitor in the brief

Call `search_web_visits` filtered by `company_id` for every company in the brief. Visitor companies are subscription-covered — `search_web_visits` is a free read. Use the response to populate the "Visit" line in each card with top landing pages, traffic sources, and timing.

**Plain-language metrics — no analytics jargon (this brief is read by sales reps too, not only marketers).** In the output, describe engagement in everyday words: say "**3 pages**" or "viewed 3 pages in one session" — never "page depth 3". Say "**14 seconds** on the page" or "spent 14s" — never "dwell". `page_depth` and `visit_length` are internal API fields: translate them into plain counts and seconds, never print the raw field name or the word "depth".

**Pull a wider lookback than the brief's time window** — request the last 90 days (not just the 24h window) so you can detect re-engagement (Step 3). The current-window visits populate the "Visit" line; the older visits are only used to find the prior session and compute the silence gap. If 90 days is expensive or the user set a longer window, pull at least `max(90 days, the brief window)`.

`search_web_visits` is the **source of truth for visit timing and engagement** in this skill. Do not cite `web_engagement.last_visit_date` from `get_company` — that field is stale. If `search_web_visits` returns no visit in the window for a company, say so transparently.

### Step 6 — Pull signals for every visitor in the brief

Call `search_companies_signals` for every visitor company in the brief. Signals are subscription-covered for visitor companies — fetch freely. Do not cap at top 3.

**Signal language — plain, and always explain relevance.** The category filtering below is an internal mechanic — **never surface it in the output.** Do not write "non-job-ad signals", category names, "excluding regulatory", or "90-day window" jargon. When nothing relevant is found, say exactly **"No notable signals in the last 90 days."** (or omit the line). When a signal *is* present, add a short plain-language reason it matters in this context — a raw event with no "so what" isn't useful. E.g. "Hiring 3 SDRs in EMEA — a growing outbound team, a fit for visitor intelligence"; "Raised Series B — fresh budget, likely expanding tooling".

**Default filters — always apply unless the user explicitly overrides:**

- **Recency window:** Pass `event_date.from` set to today minus 90 days. Older signals are usually stale and clutter the brief.
- **Exclude regulatory noise:** Pass an explicit `categories` array containing every category EXCEPT `regulatory_compliance_updates`. Regulatory filings (annual financial statements, register notices) dominate the raw signal feed but are rarely action-relevant for a morning sales brief.

The full default `categories` array to pass:

```
["business_expansion", "competitive_landscape", "event_participation", "industry_recognition", "leadership_changes", "corporate_challenges", "mergers_and_acquisitions", "customer_acquisition", "investment_activity", "product_and_service_development", "partnerships_and_collaborations", "financial_struggles", "job_ads", "register_updates"]
```

**User overrides:**

- "Include all signals" or "show regulatory signals" → drop the categories filter (pass none) so everything comes back.
- "Signals from this year" / "last 6 months" / specific date phrasing → use that window instead of the 90-day default.
- "Just hiring signals" / "only funding news" → narrow the categories array to just the matching ones (e.g. `["job_ads"]` or `["investment_activity"]`).

### Step 7 — Day-over-day trend (new vs. returning, vs. the prior window)

Give the reader a one-glance sense of momentum. This skill is stateless — there is no stored "yesterday's brief" — so derive the trend from the visit data, never from memory of a past run. Compute two things:

1. **New vs. returning (this window).** Classify each company in the brief using its 90-day visit history from Step 5:
   - **New** — first-ever visit in the history window (no visit before the current window).
   - **Returning** — visited before the current window. A subset are **re-engaged** (back after a ≥30-day gap, per the re-engagement detection).
2. **Vs. the prior window.** Call `get_web_visits_companies` once more for the immediately-preceding equal-length window (e.g. the previous 24 h) — subscription-covered, free — and compare the total company count: ↑ up, ↓ down, or → flat.

Render this as a single **Trend** line in the preamble (see Output format). Ground every number in the tool data. If the prior-window call fails or returns nothing, show the new/returning split and say "no prior-window data" — never invent a comparison.

## Output format

**Output contract — identical every run.** Reproduce the structure below **exactly**, on every invocation, no matter what appeared earlier in this thread. If you have already produced a brief in this conversation, do **not** vary, restyle, "improve", or summarise the format differently the second time — output the same template verbatim. This template is the single source of truth. Specifically, every run:
- Title exactly `# Daily Visitor Brief — {Date}, last {N} hours` — `{Date}` is a concrete date (e.g. `2026-07-16`), never "early morning", a weekday phrase, or an account ID.
- Cards numbered `## 1.`, `## 2.` — not `#1`, not `Tier 1 — …`. The Step 3 intent × ICP matrix controls the **order** of cards only; it does **not** become section headings in the output.
- Exact field labels in the exact order shown: **ICP**, **Intent score**, **Why now**, **Visit**, **Firmographics**, **Signals**, **Tags**, **CRM**, **Company website**, **Next**. Never rename them (it's **Next:**, not "Suggested action:"; **CRM:**, not "CRM status:").
- Use only the emoji in the template — ✅ ❌ ⚠️ ↩ and the 🟢 / 🟠 / ⚪️ intent dots. Do **not** add decorative emoji (📍 🎯 🗓️ 📅 or similar) to headings, labels, or lines.

Render as a ranked list of cards, top of brief = most actionable. Use ✅ / ⚠️ / ❌ status flags honestly — a card that doesn't fit shows "❌ No ICP match", and gaps (not in CRM, thin visit) read as plainly as wins. One flag per label. Use this exact structure:

````markdown
# Daily Visitor Brief — {Date}, last {N} hours

{One-sentence summary: e.g. "5 ICP-matched visits, 2 new companies, top signal: pricing-page deep dive at Acme Corp."}

**Trend:** {N} companies today ({↑ / ↓ / →} vs. {M} in the prior {window}) · {X} new · {Y} returning ({Z} re-engaged) {— or "no prior-window data" if the comparison couldn't be fetched}

---

## 1. {Company Name} · {✅ {exact ICP name}, or "❌ No ICP match"} {· ↩ Re-engaged — last session was {N} days ago  ← include this segment ONLY when re-engagement is detected}

- **ICP:** {The exact configured ICP name(s) this company matches — e.g. "DACH-Enterprise". If it matches more than one, list each; if none, "No ICP match". When several ICPs are configured, naming the exact one tells the rep which motion the account belongs to and who should own it.}
- **Intent score:** {🟢 high / 🟠 medium / ⚪️ low} {score}/10 ({tier}) — {one-line reasoning grounded in visit/signal data, e.g. "driven by 5 sessions in 2 days, deep visit to /pricing, returning identified contact"}
- **Why now:** {Most action-relevant reason in one line — "deep visit to /pricing", "second session this week", "matches Enterprise ICP and just opened the API docs"}
- **Visit:** {N sessions · M pages · last seen {date} · top landing pages: /pricing, /integrations, /docs/api}
- **Firmographics:** {Industry · Employee size · Location}
- **Signals:** {If any — each with a short plain "why it matters", e.g. "Hiring 3 SDRs in EMEA — growing outbound team, a fit for visitor intelligence". If none: "No notable signals in the last 90 days." Never expose filter mechanics ("non-job-ad", category names, "regulatory excluded").}
- **Tags:** {Assigned tags as plain-text chips by name — e.g. `` `Hot Lead` ``, `` `DACH` ``. Omit the line if none. Tag colours are configured in Leadfeeder but can't render as background-filled chips in this markdown brief, so show names only.}
- **CRM:** {If connected: "[{record name}]({crm_record.attributes.crm_url}) · Owner: {owner name — or 'owner not set'}" (record name derived by type per the capture rules) — if more than one record is linked, list each on its own line. If NOT connected: "Not found in your CRM".}
- **Company website:** {company.url from get_company response}
- **Next:** {One suggested follow-on in plain language, outcome first — NOT "Run `skill`". Describe what the user gets: "Deep-dive this company", "See who to contact — names, titles, emails", "Get talking points to personalise outreach", or "Tag it and add it to a Leadfeeder list to track it". Pick the most relevant given the why-now reason.}

```
{ready-to-send prompt for the chosen next step, e.g. Give me a company brief for {Company Name}}
```

## 2. {Company Name} · {✅ {exact ICP name} or "❌ No ICP match"}

- **ICP:** ...
- **Intent score:** ...
- **Why now:** ...
- **Visit:** ...
- **Firmographics:** ...
- **Signals:** {Omit if none.}
- **Tags:** {Omit if none.}
- **CRM:** ...
- **Company website:** ...
- **Next:** {plain-language recommendation}

```
Who should I reach out to at {Company Name}?
```

## 3. {Next Company} ...
````

Sort by your ranking. The first card is the most actionable lead.

**Copy-block convention (one per card).** Every card ends with a single fenced code block containing the ready-to-send follow-on prompt — fenced blocks render a one-click **Copy** button in the client, so the user copies, pastes, and sends. Pick the one prompt that matches the card's `Next:` recommendation:

- Deep-dive the company → `Give me a company brief for {Company Name}`
- Find who to contact → `Who should I reach out to at {Company Name}?`
- Prep outreach → `Prep me for outreach to {Company Name}`
- Track it → `Add {Company Name} to a list in Leadfeeder`

One block per card, one prompt per block (the single most relevant action). This is markdown, not a widget — do not try to render buttons; the fenced block itself gives the copy affordance.

## Intent score reasoning

The Intent score line is one of the most important on the card. Construct the one-line reasoning from the data the skill already pulled:

- **Engagement signals** (plain language — no "page depth"/"dwell"): "deep visit to /pricing", "5 sessions in 2 days", "12 pages in one session", "71 seconds on /pricing"
- **Recency signals**: "returning today", "second session this week", "first visit in 3 weeks", "re-engaged after 45 days quiet"
- **Identification signals**: "identified contact returning", "single visitor across multiple sessions"
- **Source signals**: "branded paid-search visit", "direct traffic with bookmark pattern", "organic search on competitor terms"
- **Signal data**: "hiring spike correlates", "post-funding visit"

If the intent score is HIGH but the visit data is thin, say so plainly: "High intent score but limited visible activity in the window. Worth investigating in the Leadfeeder app."

If the intent score is LOW, do not invent justification. Just note it: "Low intent score (1.9). Single short visit."

If `attributes.intent.score` is null / not returned, do not force a number — show "Intent score: not yet scored" and rank the card on engagement depth, recency, and re-engagement instead.

## CRM connection treatment

Surface CRM info clearly because it changes the action:

- **Connected with an owner:** de-emphasise "outreach now" and instead suggest "loop in {owner name}" or "check {owner}'s pipeline before reaching out". Put this nuance in the Why now line.
- **Connected but no owner (orphaned):** flag this — it's a routing problem. Note in Why now: "In your CRM but no owner assigned. Worth routing."
- **Not in CRM:** flag this — it's a missed-routing gap. Note in Why now: "Not found in your CRM. Consider adding before outreach."

The **CRM** field itself is purely factual (platform, owner, link). The action interpretation belongs in Why now.

## Edge cases

- **No visitors in the time window.** Tell the user clearly. Offer to expand to 7 days. Do not pad the brief with stale data.
- **No ICPs configured.** Fall back to ranking by engagement depth alone. Mention in the preamble: "No ICPs configured — ranking by engagement only." Suggest the user configure ICPs in Leadfeeder for sharper recommendations.
- **More than 20 ICP matches in the window.** Show the top 10 by engagement. In the preamble, offer alternative cuts ("Want this re-ranked by industry vertical, or by deepest pages-per-session?").
- **Single strong match, nothing else.** Surface it normally, but flag it: "Only one ICP match today, but a strong one."
- **Tool errors or empty responses.** Report the error transparently. Do not invent data to fill the brief.

## Source citation rule

Every claim in the brief must be grounded in data returned by the Leadfeeder MCP tools. Use the company's website (`company.url` field from `get_company`) as the actionable link on each card — that field is reliably populated. Never invent a URL. Only use links returned by the MCP tools.

**Internal consistency (trust).** Within each card and the summary line, every restated fact — session/page counts, dates, page paths, the re-engagement gap, employee size, locations — must match across the fields. A stated count must equal the items you list, and a figure or location must read the same wherever it appears on the card. Two lines disagreeing about the same fact is a trust-breaker.

**Known gap:** The MCP `get_company` response does not currently include a Leadfeeder app deeplink (e.g. `app.leadfeeder.com/...`). Until the MCP adds this, the cards link out to the prospect's own website, not to the Leadfeeder app record. If a future MCP version returns an app URL field, update this skill to add an "Open in Leadfeeder" line below the "Company website" line.

## What NOT to do

- **Do not call a visitor an "account" or a "hot/warm lead."** A website visitor is a **company** — "account" implies a CRM relationship this data doesn't carry. Reserve "account" for the user's Leadfeeder account (workspace/ID) or a genuine CRM record; use "high-intent", "active", "engaged", or "returning" instead of "hot"/"warm". (User phrases like "hot leads" may still be honored as triggers — this governs *our* output wording.)

- **Do not trigger enrichment jobs** (`create_company_enrichment_job`, `create_find_contact_data_job`). Those cost credits per company and break the "morning ritual" cost model.
- **Do not call `get_company_financials` by default.** Not a cost reason (it's subscription-covered for visitor companies) but a brevity one — `get_company` already returns headline revenue. Only call it on explicit request ("include financials", "balance sheet").
- **Do not expose contact-level PII** (names, emails, phone numbers) in the brief. Keep it company-level. Contact details belong in the separate Find My Buyer skill.
- **Do not invent data.** ICP match status, signals, page views — only report what the tools return.
- **Do not chain to outreach drafting, CRM writes, or list management** on direct user invocation unless the user explicitly asks. Exception: if invoked by the Leadfeeder Agent as part of a declared multi-step chain, the agent may proceed with follow-on skills (`visitor-company-brief`, `find-my-buyer`, `outreach-companion`, `add-to-pipeline`) without waiting for user confirmation.
- **Do not ask the user to confirm before running.** If they triggered this skill, they want the brief now.

## Example: good output

````markdown
# Daily Visitor Brief — 2026-05-29, last 24 hours

7 visitor companies, 4 ICP-matched, 1 re-engaged after 45 days of silence. Strongest signal: Acme Corp is back for a 12-page session focused on pricing and integrations after going quiet in April.

**Trend:** 7 companies today (↑ vs. 5 yesterday) · 3 new · 4 returning (1 re-engaged)

---

## 1. Acme Corp · ✅ DACH-Enterprise · ↩ Re-engaged — last session was 45 days ago

- **ICP:** DACH-Enterprise
- **Intent score:** 🟢 10/10 (high) — driven by 12-page pricing+integrations deep dive, re-engaged after 45 days quiet, identified contact returning
- **Why now:** Back after 45 days of silence and went straight to /pricing and /integrations/salesforce — a warm re-engagement worth actioning today. Existing CRM owner should be looped in.
- **Visit:** 1 session · 12 pages · last seen 2026-05-29 · top landing pages: /pricing, /integrations/salesforce, /docs/api
- **Firmographics:** SaaS · 250–500 employees · Berlin, DE
- **Signals:** Hiring 3 SDRs in EMEA — a growing outbound team, a strong fit for visitor intelligence
- **Tags:** `Hot Lead` · `DACH`
- **CRM:** [Acme Corp](https://app.hubspot.com/contacts/12345/company/67890) · Owner: Jane Doe
- **Company website:** https://acme.com
- **Next:** Deep-dive this company for the full picture, then get talking points grounded in the pricing visit + hiring signal to personalise your opener.

```
Give me a company brief for Acme Corp
```

## 2. Acme GmbH · ✅ Mid-Market DACH

- **ICP:** Mid-Market DACH
- **Intent score:** 🟠 6.4/10 (medium) — first-time visitor, 5-page demo flow, paid LinkedIn campaign attribution
- **Why now:** First-time visitor matching the Mid-Market DACH ICP. Not in CRM yet — worth adding before outreach.
- **Visit:** 1 session · 5 pages · last seen 2026-05-29 · top landing pages: /features, /case-studies/saas, /demo
- **Firmographics:** Fintech · 50–250 employees · Munich, DE
- **Tags:** `Q3 Target`
- **CRM:** Not found in your CRM
- **Company website:** https://acme.de
- **Next:** See who to contact — a ranked shortlist with names, titles, and emails — before reaching out.

```
Who should I reach out to at Acme GmbH?
```

## 3. ...
````

Keep cards tight. Long brief = unread brief.
