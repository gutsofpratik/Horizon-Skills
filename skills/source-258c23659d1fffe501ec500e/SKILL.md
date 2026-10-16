---
name: outreach-companion
description: >
  Pull visit context and recent signals for a named contact or company and return structured talking points for outreach. Use this skill when the user wants to prepare a personalised message — "draft outreach to Jane at Acme", "talking points for Acme", "prep me for outreach to Acme", "what do I say to [contact/company]", "help me reach out to [company]", "personalise my opener for [company]", "write an email to [contact]". Does NOT compose the email body — returns grounded talking points for Claude to write from.
metadata:
  version: "1.0.0"
---

# Outreach Companion

Pull visit detail and recent signals for a named contact or company and return structured talking points. The talking points are the raw material — Claude composes the actual message from them. This keeps the output grounded in real data and the email voice in the user's control.

## Language

Produce the **entire response in the language the user wrote in** — English request → English output, German request → German output, and so on. This applies to everything the skill emits: the talking points, all field labels, edge-case messages, and any credit-consumption warning and confirmation. Note the talking points themselves should be drafted in the user's language so they're ready to use. Do **not** translate data values — company names, contact names, URLs, page paths, email addresses, and signal event names stay verbatim as the tools return them. Copy-paste prompts should also be written in the user's language. If the input language is unclear, default to English.

## When this skill triggers

Trigger when the user names a contact or company and asks for outreach help, talking points, or message prep. Also trigger when invoked by the Leadfeeder Agent as part of a chain (e.g. after `visitor-company-brief` surfaces a "Recommended next move" of running this skill). Trigger silently — do not ask the user to confirm.

Do not trigger on generic "write me a cold email" without a named target — that is not grounded in Leadfeeder data.

## Inputs to determine before executing

Identify these from the user's prompt. Use defaults if unspecified — do not ask.

- **Target** — a contact name + company, or a company alone. Required. Cannot proceed without at least a company.
- **Lookback window** — default last 90 days. Honor explicit overrides ("based on last week's visits", "last 30 days", "this quarter").
- **Format hint** — optional. If the user specifies a channel or length ("LinkedIn message", "cold email", "one-liner"), note it in the output so Claude can write appropriately. Do not alter the talking points structure — just surface the hint.
- **Draft language** — optional, and **independent of the chat language**. The user may work in English but want the message written in the prospect's language (e.g. German, Finnish). If they specify one ("draft in German", "in Finnish"), the drafted message must be in that language even though the rest of the response follows the chat language. If they don't specify, default the draft to the chat language and offer the option ("want this in the prospect's language instead?").

## Workflow

Once the target is resolved, `get_company`, `search_web_visits`, and `search_companies_signals` can be called in parallel. Keep total tool calls to four to stay within the 10-second budget.

### Step 0 — Resolve the Leadfeeder account (before any other tool call)

Determine the `account_id` to use for every tool call in this skill, in priority order:

1. **Account named in the request (highest priority).** If the prompt or scheduled-task instruction explicitly names an account — an account ID (e.g. "account 01234") or an unambiguous account name — use that account for all tool calls. This overrides every source below and is the recommended way to make an unattended/scheduled task fully self-contained.
2. **Configured Account ID.** Otherwise, the plugin's configured Leadfeeder Account ID is: `${user_config.account_id}`. If that resolves to a real, non-empty account ID (not blank, and not the literal unsubstituted `${user_config.account_id}` token), use it for all tool calls and do **not** call `get_account_info` or ask the user.
3. **Already selected this session.** Otherwise, if an account was already chosen earlier in the session, reuse that.
4. **Fallback.** Otherwise call `get_account_info`. If exactly one account is returned, use it. If several are returned, ask the user to pick. When running unattended (e.g. a scheduled task) asking is impossible — if no account was named and none is configured, stop and report that a **Leadfeeder Account ID** must either be named in the task prompt or set in the plugin configuration for automated runs.

### Step 1 — Resolve the target

**If a contact name is provided:**
- Always resolve the company first: call `search_companies` with the company name. Pick the highest-confidence match and capture the `company_id`. If the company is a group entity (role: "group"), note that contacts may be associated with subsidiary company IDs rather than the group parent — keep this in mind when cross-referencing.
- Then call `search_contacts` with the contact name as the only search term (do not pass `company_id` as a filter — the tool does not narrow results by company when used alongside name search terms). The call may return many same-name contacts across unrelated companies.
- Cross-reference manually: scan the returned contacts and match those whose `relationships.company.id` equals the resolved `company_id`. If the company is a group entity, also accept contacts whose company ID is listed as a known subsidiary if that information is available.
- If no match appears in the first page (default 25 results), paginate up to 2 additional pages (≤75 total). Stop after 3 pages regardless — do not paginate indefinitely for common names. If still no match, fall back to company-level data and inform the user: "Could not find [name] in the database for [company] — proceeding with company-level data only."
- If multiple plausible matches remain after cross-referencing, present the top 3 (name, title, company) and ask the user to disambiguate before continuing.
- **Once a contact is identified**, call `get_contact` with the contact's `id` to retrieve the full record including job title and email. Only the title and email from `get_contact` should appear in the Contact footer — `search_contacts` returns only a coarse `hierarchy_level` bucket, not the actual title.
- The `company_id` is already known from the `search_companies` call above — do not wait to extract it from the contact record.

**If company only (no contact named):**
- **If the input is already a numeric company ID**, use it directly as `company_id` and skip to Step 2.
- **If the input is a name or domain**, call `search_companies`. Pick the highest-confidence match.
- If multiple plausible matches, present the top 3 and disambiguate.
- If no match, tell the user clearly and stop.

### Step 1.5 — Subscription coverage & credit confirmation — before the deep reads in Step 2

`get_company` and `search_companies_signals` are credit-consuming — 1 credit per company **unless it was accessed within the last 12 months** (web-visits companies are inside that free window). First probe coverage for **free**: call `search_web_visits` for `company_id` over the **last 12 months** (this also supplies the visit data Step 2 needs — reuse it).

Then, before any credit-consuming call, flag it and get a single go-ahead. The target isn't guaranteed to be a visitor, so use this **conditional** wording — never the generic "1 credit per company" alarm:

> To prep your outreach I need **{Company}**'s visit detail, firmographics, and signals using `get_company` and `search_companies_signals` — credit-consuming tools. If {Company} is in your Web Visitors feed, its 12-month access window has already started, so no credits are charged for a record already unlocked within the last 12 months. If it hasn't visited in the last 12 months, this will consume about 2 credits (firmographics 1 + signals 1). Want me to proceed?

On a clear **yes** → run Step 2's deep calls and report the actual `meta.credits.charged` (0 for a covered/visitor record). On **no** → stop; if the company was uncovered, offer only the free basics (name, website) rather than the full prep.

### Step 2 — Fetch in parallel (once company_id is known)

Once Step 1.5 is **COVERED** or the user has consented to the credit cost, call all three in parallel (the `search_web_visits` call may already be done from the coverage probe — reuse it rather than repeat it):

- `get_company` with `include=crm_connections.crm_record.crm_owner` — firmographics: industry, employee count, location, intent score (read `attributes.intent.score` / `attributes.intent.score_tier` — nested under `attributes`, may be `null`), description. Also read CRM status: plain `include=crm_connections` returns only a stub (`crm_record` = `{id, type}`, no owner); the deeper path sideloads the record and owner. A populated `relationships.crm_connections` means the company is in the CRM. Each `crm_record` is polymorphic (`crm_record.type` = `crm_organization` | `crm_contact` | `crm_lead`): read **URL** from `crm_record.attributes.crm_url`, **name** by type (`crm_organization` → `attributes.name`; `crm_contact`/`crm_lead` → `attributes.first_name` + `attributes.last_name`), **owner** from `crm_record.relationships.crm_owner.attributes.name` (say "owner not set" if only a stub). **Render as a markdown link** — record name is the clickable text, `crm_record.attributes.crm_url` the target; never print the raw URL or leave the name unlinked. Do not call `get_company_financials`.
- `search_web_visits` — filtered by `company_id`, using the user's lookback window. Aggregate the same fields the Visit context section renders (keep terminology identical to `visitor-company-brief`): **total sessions**, **first seen and last seen**, **top landing pages** by frequency (use `landing_page_path` — the `engagements` array within each visit record is typically empty and cannot be used for per-page path analysis), **top sources** (`source` + `medium`), **deep visits** (`page_depth >= 3` or `visit_length >= 60s`), and the identified-vs-anonymous breakdown. **In the output, describe deep visits in plain language** (sales reps read this too): "viewed 4 pages", "spent 83 seconds" — never "page depth 4" or "dwell". `page_depth`/`visit_length` are internal fields; translate them into plain page counts and seconds.
- `search_companies_signals` — filtered by `company_id`. Apply default filters:
  - **Recency:** `event_date.from` = today minus 90 days (or the user's lookback if longer).
  - **Exclude regulatory noise:** Pass the full default `categories` array, omitting `regulatory_compliance_updates`:
    ```
    ["business_expansion", "competitive_landscape", "event_participation", "industry_recognition", "leadership_changes", "corporate_challenges", "mergers_and_acquisitions", "customer_acquisition", "investment_activity", "product_and_service_development", "partnerships_and_collaborations", "financial_struggles", "job_ads", "register_updates"]
    ```

### Step 3 — Synthesise talking points

Derive 2–4 talking points from the data. A talking point is not raw data — it is an interpreted angle the user can open with or reference in their message. Each point should say what to mention and why it resonates.

Prioritise talking points that connect visit behaviour to a business signal:
- A deep pricing visit + active hiring → buying evaluation + org growth
- A return visit to /integrations after a gap → re-engagement, specific use-case interest
- A leadership change + first visit → new decision-maker warming up
- A first visit from a LinkedIn ad → paid intent, already aware of the product

If visit data is thin or absent, fall back to signals-only talking points. If both are absent, tell the user plainly — do not pad with generic outreach advice.

**Factor in CRM status.** If the company is already owned in the CRM by someone else, the talking points still stand, but flag that outreach should be coordinated with the owner rather than sent cold. If it is not found in your CRM, that is a clean net-new outreach — worth tagging it and adding it to a Leadfeeder list to track it (`add-to-pipeline`; that writes tags/lists inside Leadfeeder, it does not create a CRM record).

**Keep talking points consistent with the data above.** A talking point restates facts from the Visit context / Recent signals sections — it must use the *exact same* values: the same set of countries/cities, the same counts, the same dates. If the Identified line says "5 contacts across DE, CH, AT, SE, FR", a talking point about geography must name that same set and count — do not re-derive it, mix cities with countries, or drop/add locations (e.g. don't turn "DE, CH, AT, SE, FR" into "Munich, Düsseldorf, Frankfurt, Sweden, Austria", which is 3 German cities + 2 countries and silently loses CH and FR). A count you assert ("five countries") must equal the items you list.

## Output format

**Output contract — identical every run.** Reproduce the structure below **exactly**, on every invocation, regardless of anything earlier in this thread. If you've already run this skill in the conversation, do not vary, restyle, or "improve" the format next time — output the same template verbatim; this template is the single source of truth. Keep the exact headings, field labels, and order; don't invent new sections, don't rename fields, and add no decorative emoji beyond those the template already uses (✅ ⚠️ ❌).

**Status flags — be honest about gaps.** Use ✅ (strong), ⚠️ (thin/caution), ❌ (missing) on the data-quality lines — flag "❌ no visits in the window" or "⚠️ all anonymous" as plainly as a strong signal, so the user knows how solid the grounding is. One flag per line.

The outer block below is shown with four backticks so the copy blocks nest correctly — your actual output is plain markdown.

````markdown
## Outreach Companion — {Contact Name at Company Name / Company Name}

**Why reach out now:** {One sentence — the single strongest reason to reach out today, grounded in data.}

---

### Visit context (last {N} days)
- **Total sessions:** {N}
- **First seen / Last seen:** {date} / {date}
- **Top landing pages:** {/path1, /path2, /path3}
- **Top sources:** {Direct, LinkedIn CPC, Google organic}
- **Deep visits:** {e.g. "1 deep visit — 4 pages, 83s, hit /pricing and /integrations/salesforce" or "All sessions single-page"}
- **Identified:** {e.g. "✅ 1 of 3 sessions identified" or "⚠️ All anonymous — no identified contact yet"}

{If no visit data in the window: "❌ No visits recorded in the last {N} days. Talking points are signals-only."}

### Recent signals
- {Signal 1 — date — plus a short plain line on why it's relevant to this outreach} *(most outreach-relevant first)*
- {Signal 2 — date — why it matters}
- {If none: omit this section, or if you mention the absence say plainly "No notable signals in the last 90 days." Never expose filter mechanics ("non-job-ad", category names, "regulatory excluded", "90-day window" jargon).}

### Talking points
1. **{Angle}** — {One sentence: what to say and why it lands. Ground it in the data above.}
2. **{Angle}** — ...
3. **{Angle}** — ...
{2–4 points max. Quality over quantity.}

---

{If contact was resolved} **Contact:** {Name} · {Title} · {Company}
{Email line: include ONLY if the user explicitly named the contact in the prompt} **Email:** {email}
{CRM line: if CRM-connected} **CRM:** [{record name}]({crm_record.attributes.crm_url}) · Owner: {owner name — or 'owner not set'} — coordinate with the owner before sending. {Record name derived by type per Step 2. If not connected, omit this line, or note "Not in CRM — clean net-new outreach."}
{If format hint provided} **Format hint:** {e.g. "LinkedIn message — keep it under 300 characters"}

---

**Draft it in one click** — copy the prompt for the channel you want (if a format hint was given, keep only the matching one; append a language if you want the message in the prospect's language, e.g. "… in German"). When the message is drafted, it must follow the **Drafting guardrails** below.

```
Write this as a cold email using the talking points above
```

```
Write this as a LinkedIn message using the talking points above
```
````

## Drafting guardrails (apply when the message is written from the talking points)

The talking points are internal prep. The **drafted message goes to the prospect**, so it must never read as surveillance ("spooky"). When you write the cold email / LinkedIn message from the points:

- **Never recite tracking specifics to the prospect.** No exact session durations ("you spent 23 minutes"), no page-by-page paths ("you looked at /pricing, /integrations, /demo"), no visit counts or cadence ("your 14th session", "a second deep visit last week"). Reciting exactly what someone did and for how long is what makes it creepy — it's the single thing to avoid.
- **Reference interest softly and at a high level** — "noticed your team's been exploring how we help with {topic}", "thought the timing might be right" — grounded in the signal without exposing the raw analytics behind it.
- **Lead with value and relevance to their world** (their hiring, expansion, use case, industry), not with what your tracker observed.
- The talking points may hold specifics for *your* understanding; the message must translate them into a natural, non-invasive opener. If a talking point can only be expressed by quoting tracking detail, drop it from the message rather than make it creepy.
- **Language:** write the message in the requested **Draft language** if one was given (it can differ from the chat language — e.g. English chat, German message); otherwise use the chat language.

## Edge cases

- **No visit data in the lookback window.** Say so clearly. Still produce signals-based talking points if signals exist. If neither exists, tell the user the company is cold and suggest running `visitor-company-brief` to see the broader engagement history.
- **Contact not found after 3 pages.** Common names (e.g. "Stefan Koch") return hundreds of results. Paginate up to 3 pages of `search_contacts`, cross-reference each page against the resolved `company_id`. If still no match, tell the user and proceed with company-level data only. Do not keep paginating indefinitely.
- **Contact not found — group company.** If the resolved company is a group entity, the contact may be stored under a subsidiary company ID rather than the group parent. Note this to the user if cross-referencing fails: "ATOSS is a group entity — the contact may be on a subsidiary record not captured here."
- **Multiple contact matches.** Present top 3 (name, title, company) and wait for disambiguation. Do not silently pick.
- **Company not found.** Stop and tell the user. Offer to try a broader name fragment or a domain.
- **No signals in the window.** Omit the signals section (or state it plainly as "No notable signals in the last 90 days"). Never expose the category filter — no "non-job-ad", category names, "regulatory excluded", or "90-day window" jargon. Do not fabricate events.
- **Agent-invoked with prior brief context.** If this skill is invoked by the Leadfeeder Agent after `visitor-company-brief`, the company_id is already known — skip Step 1 entirely and proceed to Step 2 directly.

## Source citation rule

Every talking point must be traceable to a specific tool response — a page URL, a signal event, a visit date. CRM record name, URL, and owner must come from the sideloaded `crm_record` (and its `crm_owner`) under `relationships.crm_connections` on the `get_company` response — `crm_record.attributes.crm_url`, the name from `crm_record.attributes` per record type, and `crm_record.relationships.crm_owner.attributes.name` — never assert a company is (or isn't) in the CRM without it. Do not invent angles. If the data is thin, fewer talking points is correct.

**Internal consistency (trust).** Derive each fact — counts, country/city lists, dates, page paths, numbers — once from the tool data and restate it identically everywhere in the output. A stated count must equal the items you actually list, and a location set must be the same set wherever it appears (cities and countries must resolve to the same places). Before finishing, re-read the talking points against the Visit context / signals sections and fix any mismatch — two sections disagreeing about the same fact is a trust-breaker.

## What NOT to do

- **Do not call a visitor an "account" or a "hot/warm lead."** A website visitor is a **company** — "account" implies a CRM relationship this data doesn't carry. Reserve "account" for the user's Leadfeeder account (workspace/ID) or a genuine CRM record; use "high-intent", "active", "engaged", or "returning" instead of "hot"/"warm".

- **Do not compose the email or message body.** Return talking points only. Claude writes the message from them.
- **Do not expose the contact's email** unless the user explicitly named the contact in their prompt (e.g. "draft outreach to jane.doe@acme.com" or "talking points for Jane Doe at Acme"). Company-level or agent-chained invocations do not qualify.
- **Do not trigger enrichment jobs** (`create_company_enrichment_job`, `create_find_contact_data_job`). This skill is free and read-only.
- **Do not call `get_company_financials`.** It charges per call and is not needed for outreach prep.
- **Do not fabricate visit pages, signal events, or contact details.** If data is absent, say so.
- **Do not pad with generic cold outreach advice** when Leadfeeder data is thin. Less is more.
- **Do not recite visitor-tracking specifics in a drafted message to the prospect** — exact session durations, page-by-page paths, or visit counts read as surveillance ("spooky"). Reference interest softly instead (see Drafting guardrails).

## Example: good output

````markdown
## Outreach Companion — Jane Doe at Acme Corp

**Why reach out now:** Acme returned for a third pricing-page session this week while actively hiring SDRs in EMEA — active evaluation with a growing sales team is a strong entry point.

---

### Visit context (last 90 days)
- **Total sessions:** 4
- **First seen / Last seen:** 2026-04-15 / 2026-06-23
- **Top landing pages:** /pricing, /integrations/salesforce, /docs/api, /case-studies/saas
- **Top sources:** LinkedIn CPC, Direct
- **Deep visits:** 2 deep visits — longest was 5 pages, 97s, concentrated on /pricing and /integrations/salesforce
- **Identified:** ✅ 1 of 4 sessions identified

### Recent signals
- Hiring: SDR EMEA (3 open roles) — 2026-06-10 — growing outbound team, a fit for visitor intelligence
- Hiring: Revenue Operations Manager — 2026-06-18 — building out RevOps, our core buyer
- Investment: Series B announced — 2026-05-14 — fresh budget, expansion mode

### Talking points
1. **Pricing evaluation in progress** — Three sessions on /pricing in the last week suggests active comparison or internal approval prep. Reference it without being creepy: "noticed companies like yours often come back to pricing when they're building the business case."
2. **SDR team expansion** — Three open SDR roles in EMEA means a growing outbound motion. Connect the product to the new headcount: "as you scale the team, visitor intelligence helps reps prioritise accounts before the first dial."
3. **Post-Series B timing** — Fresh capital and hiring momentum is a classic expansion window. Opening line: "congrats on the Series B — a lot of our best conversations happen right after a round, when pipeline pressure starts showing up."

---

**Contact:** Jane Doe · Head of Revenue Operations · Acme Corp
**Email:** jane.doe@acme.com
**CRM:** [Acme Corp](https://app.hubspot.com/contacts/12345/company/67890) · Owner: John Doe — coordinate with John before sending.

---

**Draft it in one click:**

```
Write this as a cold email using the talking points above
```

```
Write this as a LinkedIn message using the talking points above
```
````
