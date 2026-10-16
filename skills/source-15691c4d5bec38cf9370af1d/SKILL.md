---
name: visitor-company-brief
description: >
  Produce a deep, structured company brief on a single named company from Leadfeeder — firmographics, engagement history, contacts on file, recent intent signals, and a recommended next move. Use this skill when the user names a specific company and asks for research, such as "tell me about [company]", "brief me on [company]", "deep dive on [company]", "company brief for [company]", "account brief for [company]", "research [company]", "everything you have on [company]", "give me a profile of [company]", or asks for a full read on a single company they want to action.
metadata:
  version: "1.0.0"
---

# Visitor Company Brief

Produce a structured deep-dive on a single named company. Anchor every section in real Leadfeeder data. This is the depth complement to the Daily Visitor Brief (which is breadth across many companies in a 24h window).

## Language

Produce the **entire response in the language the user wrote in** — English request → English output, German request → German output, and so on. This applies to everything the skill emits: the summary, all section headings and field labels, reasoning, edge-case messages, and the credit-consumption warning and confirmation. Do **not** translate data values — company names, contact names, URLs, page paths, email addresses, tag names, and ICP names stay verbatim as the tools return them. Copy-paste follow-up prompts should also be written in the user's language (they still trigger the right skill). If the input language is unclear, default to English.

## When this skill triggers

Trigger when the user names ONE specific company and asks for research, a profile, a brief, or a deep dive. Do not trigger if the user is asking about multiple companies or a ranked list across visitors — that is the Daily Visitor Brief skill. Trigger silently. Honor explicit modifiers in the prompt (engagement window, focus area, depth).

## Inputs to determine before executing

Identify these from the user's prompt. Use defaults if unspecified — do not ask.

- **Company identifier** — the name, domain, or Leadfeeder company ID provided in the prompt. Required. If multiple candidates match, see "Disambiguation" below.
- **Engagement window** — default last 90 days. Honor explicit overrides ("last 30 days", "this quarter", "since January").
- **Focus area** — default: full brief. If the user is narrow ("focus on hiring", "just engagement", "ICP fit only"), produce a focused version that drops the other sections.

## Workflow

Execute these tool calls. Always re-fetch ICPs/personas (do not cache across runs).

### Step 0 — Resolve the Leadfeeder account (before any other tool call)

Determine the `account_id` to use for every tool call in this skill, in priority order:

1. **Account named in the request (highest priority).** If the prompt or scheduled-task instruction explicitly names an account — an account ID (e.g. "account 01234") or an unambiguous account name — use that account for all tool calls. This overrides every source below and is the recommended way to make an unattended/scheduled task fully self-contained.
2. **Configured Account ID.** Otherwise, the plugin's configured Leadfeeder Account ID is: `${user_config.account_id}`. If that resolves to a real, non-empty account ID (not blank, and not the literal unsubstituted `${user_config.account_id}` token), use it for all tool calls and do **not** call `get_account_info` or ask the user.
3. **Already selected this session.** Otherwise, if an account was already chosen earlier in the session, reuse that.
4. **Fallback.** Otherwise call `get_account_info`. If exactly one account is returned, use it. If several are returned, ask the user to pick. When running unattended (e.g. a scheduled task) asking is impossible — if no account was named and none is configured, stop and report that a **Leadfeeder Account ID** must either be named in the task prompt or set in the plugin configuration for automated runs.

### Step 1 — Resolve the company

Determine the Leadfeeder `company_id` from the user's input.

- **If the input is already a numeric company ID** (e.g. `228035150`), skip to Step 2.
- **If the input is a company name or fragment** (e.g. "Acme Corp", "Acme"), call `search_companies` with the name as the query. Pick the highest-confidence match.
- **If the input is a domain** (e.g. "acme.com"), call `search_companies` with the domain.
- **If `search_companies` returns multiple plausible matches**, present the top 3 (name, country, employee count, industry) and ask the user to disambiguate before continuing. Never silently pick when there is real ambiguity (e.g. two German companies with similar names).
- **If `search_companies` returns no matches**, tell the user clearly. Offer to expand the search (e.g. with a broader name fragment) rather than fabricating a profile.

### Step 2 — Load ranking context

Call `get_icps` and `get_buyer_personas`. Always re-fetch on every invocation. The calls are free (no credits). Use the response to score the target company against ICP and persona criteria in Step 5.

### Step 2.5 — Subscription coverage & credit confirmation — before any credit-consuming call

`get_company`, `search_companies_signals`, and `get_company_financials` are credit-consuming — 1 credit per company **unless it was accessed within the last 12 months** (companies in your web-visits feed are inside that free window). First probe coverage for **free**: call `search_web_visits` filtered by `company_id` over the **last 12 months** (reuse it for Step 4 engagement).

Then, before any credit-consuming call, **do not call `get_company` or `search_companies_signals` yet** — flag it and get a single go-ahead. The target isn't guaranteed to be a visitor, so use this **conditional** wording, never the generic "1 credit per company" alarm:

> To build this brief I need **{Company}**'s firmographics and signals using `get_company` and `search_companies_signals` — credit-consuming tools. If {Company} is in your Web Visitors feed, its 12-month access window has already started, so no credits are charged for a record already unlocked within the last 12 months. If it hasn't visited in the last 12 months, this will consume about 2 credits (firmographics 1 + signals 1; +1 more only if you later ask for financials). Want me to proceed?

On a clear **yes** → proceed with Steps 3–6 and report the actual `meta.credits.charged` (0 for a covered/visitor record). On **no** → give only the free basics (name and website from `search_companies`, and "no visit activity in the last 12 months") and stop.

### Step 3 — Pull firmographics

Only proceed here once Step 2.5 is **COVERED** or the user has explicitly consented to the credit cost. Call `get_company` for the resolved `company_id` with `include=crm_connections.crm_record.crm_owner,tags`. Track `meta.credits.charged` (0 = it was in the free 12-month window; 1 = this call charged).

Capture: industry, employee_count and range, location (HQ city and country), B2B/B2C orientation, founded year, revenue/earnings/net_worth where present, **intent score and tier (from `attributes.intent.score` (0–10, may be `null`) and `attributes.intent.score_tier` — nested under `attributes`, not a top-level `intent.score`; if null, show "not yet scored"). Prefix the displayed score with a tier dot by `score_tier`: 🟢 high · 🟠 medium · ⚪️ low (omit the dot when "not yet scored")**, description, legal form, register status.

**Use one canonical figure per metric across the entire brief.** `get_company` returns both an exact `employee_count` (e.g. 382) and a coarser range/bucket. Treat the **exact `employee_count`** as the single source of truth and use that same number everywhere — the one-sentence intro, the Snapshot, and any reasoning. If you round it in prose, round the *same* number consistently (382 → "~380" or "380+" — never "230+" or a different bucket). Same rule for revenue and any other figure. Two different numbers for the same metric in one brief (e.g. intro says "230+ employees", Snapshot says "382") is a trust-breaker — the intro and Snapshot must never disagree.

**CRM connections (sideloaded).** Request `include=crm_connections.crm_record.crm_owner` (plain `include=crm_connections` returns only a stub — `crm_record` as `{id, type}` with no name, URL, or owner). A populated `relationships.crm_connections` means the company is in the CRM. Each `crm_record` is JSON:API-shaped and **polymorphic** (`crm_record.type` = `crm_organization` | `crm_contact` | `crm_lead`): read **URL** from `crm_record.attributes.crm_url`; **name** by type (`crm_organization` → `attributes.name`; `crm_contact`/`crm_lead` → `attributes.first_name` + `attributes.last_name`); **owner** from `crm_record.relationships.crm_owner.attributes.name` (say "owner not set" if only a stub). **Render as a markdown link** — the record name is the clickable text and `crm_record.attributes.crm_url` is the target; never print the raw URL or leave the name unlinked. This complements the firmographics with the company's status in the user's own CRM — surface it in the Snapshot and factor it into the recommendation.

**Tags (sideloaded via `include=tags`).** Capture each assigned tag's `attributes.name` and `attributes.color`. Note: `color` is an integer palette **index** (0–N), not a hex code — the API doesn't expose the hex, and a plain markdown brief can't render background-filled chips anyway. So surface tags as plain-text chips (backtick `` `Hot Lead` `` style) using their **names**; do not invent a colour. Show them in the Snapshot because customers use tags to prioritise accounts, so they inform the recommended next move.

**Ignore `web_engagement.last_visit_date`** — it lags the real visits stream. Use Step 4 as the source of truth for visit timing.

**Flag register status `out_of_business` or `non_company` immediately** and stop the brief. Tell the user the company is not actionable and skip the rest of the workflow.

Do not call `get_company_financials` by default. It charges per call. Only call it if the user explicitly asks for "financials", "company financials", "balance sheet", or similar.

### Step 4 — Pull engagement history

Call `search_web_visits` with `filters.company_id` set to the resolved company. Use the user's engagement window (default last 90 days).

Aggregate the response to produce:

- **Total sessions** in the window
- **First seen** and **last seen** timestamps in the window
- **Top landing pages** by visit count (deduplicate paths, show top 5)
- **Top traffic sources** (Direct, Google organic, Bing organic, Google CPC, LinkedIn, etc.)
- **Trend** — qualitative read: accelerating, stable, declining, dormant. Compare the most recent 30 days vs the 30 days before.
- **Identified visits** — count only. Do NOT expose contact names or emails. Note the number of distinct identified contacts.
- **Deep visits** — flag any session with `page_depth >= 3` or `visit_length >= 60s` as a "deep visit" worth calling out. **In the output use plain language** (this brief is read by sales reps too): "viewed 3 pages", "spent 71 seconds" — never "page depth 3" or "dwell". `page_depth`/`visit_length` are internal API fields; translate them into plain page counts and seconds, never print the field name or the word "depth".

### Step 5 — Pull contacts on file

Call `search_contacts` filtered by the company ID. Use the response to produce a **non-PII summary**:

- **Total contacts** on file (count)
- **Department breakdown** (e.g. 12 in Engineering, 8 in Sales, 5 in Marketing)
- **Seniority breakdown** (e.g. 2 C-level, 4 VPs, 10 managers, 15 ICs)
- **Buyer Persona matches** — for each configured persona, count how many contacts match; flag ✅ when ≥1 and ❌ when zero (an honest gap callout — surface the empty personas, don't hide them)
- **Decision-maker availability** — ✅ Yes / ⚠️ Limited / ❌ No: are there senior-enough contacts (top management, VP/Director level, etc.) on file to make outreach worth doing?

**Do NOT list individual contact names, emails, phone numbers, or LinkedIn URLs** in the brief output. Contact detail belongs in the separate Find My Buyer skill, which is invoked explicitly. This brief is a research overview, not a contact list.

### Step 6 — Pull recent signals

For a **COVERED** company (visited in the last 12 months) this is free — always run it; do not gate or skip it on cost grounds. For an **UNCOVERED** company it charges 1 credit (if the company has signals), so only run it under the consent obtained in Step 2.5. Call `search_companies_signals` for the single `company_id`. Apply the same default filters as the Daily Visitor Brief:

- **Recency window:** `event_date.from` = today minus 90 days (or override the user's engagement window if longer).
- **Exclude regulatory noise:** Pass an explicit `categories` array containing every category EXCEPT `regulatory_compliance_updates`. Full default categories:

```
["business_expansion", "competitive_landscape", "event_participation", "industry_recognition", "leadership_changes", "corporate_challenges", "mergers_and_acquisitions", "customer_acquisition", "investment_activity", "product_and_service_development", "partnerships_and_collaborations", "financial_struggles", "job_ads", "register_updates"]
```

Group the returned signals by category. Highlight the ones that move the recommended action (hiring spikes, funding events, leadership changes, M&A activity, financial stress).

**Signal language — plain, and always explain relevance.** The category filtering is an internal mechanic — **never surface it in the output** (no "non-job-ad", no category names, no "excluding regulatory", no "90-day window" jargon). When nothing relevant is found, say exactly **"No notable signals in the last 90 days."** When a signal *is* present, pair it with a short plain-language reason it matters in this context — a raw event with no "so what" isn't useful (e.g. "Hiring 3 SDRs in EMEA — a growing outbound team, a fit for visitor intelligence"; "Raised Series B — fresh budget, likely expanding tooling").

### Step 7 — Compute ICP match and synthesise recommendation

Score the company against each configured ICP from Step 2:

- **Full match** — all filters satisfied (location, employee count, industry, B2B/B2C orientation as applicable).
- **Partial match** — some filters satisfied. Call out which dimensions match and which don't (e.g. "DE + Pro Services match, employee count under threshold").
- **No match** — none of the configured ICPs apply.

Then synthesise a **Recommended next move** section. This is the one part of the brief where the skill takes a position. Base the recommendation on:
- ICP fit (sales-worthy or not)
- Engagement signal strength
- Recent signals that suggest a moment of opportunity (hiring HR roles, raised funding, lost a key exec, etc.)
- Decision-maker availability
- **CRM status** — this changes the action:
  - *Connected with an owner* → do not recommend cold outreach; recommend coordinating with / looping in the owner and checking their pipeline first.
  - *Connected but no owner (orphaned)* → flag it as a routing gap worth resolving.
  - *Not in CRM* → flag it as a missed-routing gap; consider adding it (via `add-to-pipeline`) before outreach.

Surface 1–3 next-step actions. **Phrase each in plain language, outcome first — describe what it does for the user, then the copy-paste prompt. Never a bare "Run `skill`".** The follow-ons and their honest outcomes:

- **Find who to contact** — a ranked shortlist of the right people with names, titles, and emails. (`find-my-buyer`)
- **Prep outreach** — visit-grounded talking points for a personalised opener. (`outreach-companion`)
- **Add to your pipeline** — tags the company and adds it to a Leadfeeder list so it's tracked. (`add-to-pipeline`) Say exactly that — it writes tags and lists **inside Leadfeeder**; it does **not** create a CRM record or assign a CRM owner. (If the company should also live in the user's CRM, that's a separate manual step — don't imply `add-to-pipeline` does it.)

Pick the 1–3 most relevant given the ICP verdict, engagement signal, and available contacts. This is what makes the brief actionable.

## Output format

**Output contract — identical every run.** Reproduce the structure below **exactly**, on every invocation, regardless of anything earlier in this thread. If you've already run this skill in the conversation, do not vary, restyle, or "improve" the format next time — output the same template verbatim; this template is the single source of truth. Keep the exact headings, field labels, and order; don't invent new sections or tiers, don't renumber, don't rename fields, and add no decorative emoji beyond those the template already uses (✅ ❌ ⚠️ ↩ and the 🟢 / 🟠 / ⚪️ intent dots).

**Status flags — be honest about gaps.** On coverage/availability/status lines use ✅ (present/strong), ⚠️ (partial/thin), ❌ (gap/missing), and surface gaps as prominently as strengths — an honest ❌ ("no contacts on file for this persona") builds trust more than only showing wins. One flag per line; don't over-decorate.

**Stamp the brief with a generation timestamp.** The line directly under the title is `*Generated {current date} · engagement window: last {N} days*` — use the **current date** (the brief is a point-in-time snapshot). This is the *generation* timestamp ("as of" date); it is distinct from visit dates and must always be present, even when visit data is sparse. Do not substitute a visit date for it.

Render as a single structured brief. Use this exact structure (the outer block is shown with four backticks so the copy blocks nest correctly — your actual output is plain markdown):

````markdown
# Company Brief — {Company Name}
*Generated {current date} · engagement window: last {N} days*

{One-sentence positioning: what they do, key size signal, ICP verdict in one line. The size signal must use the SAME exact employee_count/revenue shown in the Snapshot below — never a different figure or bucket.}

## Snapshot
- **Industry:** {primary + secondary industries}
- **Size:** {employee count} · {revenue if present}
- **Location:** {city, country} (HQ)
- **Legal form / founded:** {legal form} · founded {year}
- **Intent score:** {🟢 high / 🟠 medium / ⚪️ low} {score} ({tier})
- **ICP match:** {✅ Full / ⚠️ Partial / ❌ No match} — {one-line reason}
- **Tags:** {Assigned tags as plain-text chips by name — e.g. `` `Hot Lead` ``, `` `DACH` ``. Omit the line if none. Tag colours are configured in Leadfeeder but can't render as background-filled chips in this markdown brief, so show names only.}
- **CRM:** {If connected: "[{record name}]({crm_record.attributes.crm_url}) · Owner: {owner name — or 'owner not set'}" (record name derived by type per the capture rules) — one line per record if more than one is linked. If not: "Not found in your CRM".}

## Engagement (last {N} days)
- **Total sessions:** {N}
- **First seen / Last seen:** {date} / {date}
- **Top landing pages:** {/path1, /path2, /path3}
- **Top sources:** {Direct, Google CPC, Bing organic}
- **Deep visits:** {count and short description of the deepest one, e.g. "1 deep visit yesterday — 3 pages, 71s, hit /pricing"}
- **Trend:** {accelerating / stable / declining / dormant} — {one-line interpretation}
- **Identified visits:** {N sessions from {M} distinct identified contacts} (names withheld; see Find My Buyer skill)

## People on file ({N} contacts)
- **Departments:** {top 3 departments with counts}
- **Seniority:** {C-level: X, VP/Director: Y, Manager: Z, IC: W}
- **Buyer Persona matches:** (flag each — ✅ if ≥1 match, ❌ if zero)
  - ✅ "{Persona name}" → {N matching contacts}
  - ❌ "{Persona name}" → 0 (gap: no contacts on file)
- **Decision-maker availability:** {✅ Yes / ⚠️ Limited / ❌ No} — {one-line on what's there}

## Recent signals (last 90 days)
{Group by category. Use a sub-heading per non-empty category. Omit empty categories entirely. Each grouping's cluster gets a one-line "why it matters"; never expose filter mechanics. If nothing relevant: replace this whole section with the single line "No notable signals in the last 90 days."}

### Hiring ({N} ads)
- {Role 1} — {date}
- {Role 2} — {date}
- ... (cap at 5, summarise the rest as "+N more")
*Why it matters: {one plain line, e.g. "hiring across HR + IT Security suggests an org rebuild — a fit for our RevOps narrative"}.*

### Leadership changes ({N})
- {Event} — {date}
*Why it matters: {e.g. "new decision-maker settling in — a natural moment to introduce a new approach"}.*

### Funding / Investment ({N})
- {Event} — {date}
*Why it matters: {e.g. "fresh capital — expansion mode, likely evaluating new tooling"}.*

(Other categories as relevant, each with its own "why it matters" line.)

## Recommended next move

{One short paragraph synthesising the read. Then 1–3 actions, formatted as a list.}

- **{Action 1}** — {short rationale, e.g. "Find who to contact — a ranked shortlist of the right people."}
- **{Action 2}** — {short rationale}
- **{Action 3}** — {short rationale}

Copy any of these to run the next step (each is a ready-to-send prompt with a one-click copy button):

```
Who should I reach out to at {Company Name}?
```

```
Prep me for outreach to {Company Name}
```

---

**Company website:** {company.url from get_company}
````

**Copy-block convention.** Emit one fenced code block per recommended action above — fenced blocks give the user a one-click **Copy** button. Map each action to its ready-to-send prompt: `find-my-buyer` → `Who should I reach out to at {Company Name}?`; `outreach-companion` → `Prep me for outreach to {Company Name}`; `add-to-pipeline` → `Add {Company Name} to a list in Leadfeeder`. Only include the blocks for the actions you actually recommended.

## Edge cases

- **Company not found by `search_companies`.** Tell the user clearly. Offer to expand search ("try a different name fragment or a domain"). Do not fabricate a profile.
- **Multiple plausible matches.** Present top 3 with disambiguation criteria (country, employee count, industry). Wait for user input before continuing.
- **Register status is `out_of_business` or `non_company`.** Stop the brief immediately. Tell the user and offer an alternative ("Did you mean a different entity?"). Do not waste tokens on a dead company.
- **No web visits in the engagement window.** Say so clearly. Optionally offer to expand the window. Do not invent visits.
- **No contacts on file.** Say so. Flag this as a gap — recommend running enrichment ("Want me to find contacts via the Find Contact Data job?") but do not auto-trigger it (cost).
- **No signals in the 90d window.** Say "No notable signals in the last 90 days." Move on. This is not unusual for smaller or quieter companies.
- **ICP mismatch.** Surface the verdict honestly. Do not pad with "but they could still be interesting" unless the engagement signal is unusually strong (e.g. deep pricing visits).
- **User asks for financials.** Then and only then call `get_company_financials`. Quote the credit cost in the response.
- **Tool errors.** Report transparently. Do not silently substitute stale data.

## Source citation rule

Every claim in the brief must be grounded in data returned by the Leadfeeder MCP tools. Use the company's website (`company.url` field from `get_company`) as the actionable link in the footer. CRM record name, URL, and owner must come from the sideloaded `crm_record` (and its `crm_owner`) under `relationships.crm_connections` — `crm_record.attributes.crm_url`, the name from `crm_record.attributes` per record type, and `crm_record.relationships.crm_owner.attributes.name` — never infer that a company is (or isn't) in the CRM without that data; if no connection is returned, treat it as "Not found in your CRM". Do not invent URLs.

**Internal consistency (trust).** Beyond the canonical-figure rule in Step 3, every fact restated across sections — counts, country/city lists, dates, page paths — must match exactly. A stated count must equal the items you list, and a location set must be the same set wherever it appears (cities and countries resolving to the same places). The intro, Snapshot, Engagement, People, and Recommended-next-move sections must never disagree about the same fact. Re-check before finishing.

**Known gap (same as Daily Visitor Brief):** The MCP `get_company` response does not currently include a Leadfeeder app deeplink. Until the MCP adds this, the brief footer links out to the prospect's own website only. If a future MCP version returns an app URL field, update this skill to add an "Open in Leadfeeder" line below the "Company website" line.

## What NOT to do

- **Do not call a visitor an "account" or a "hot/warm lead."** A website visitor is a **company** — "account" implies a CRM relationship this data doesn't carry. Reserve "account" for the user's Leadfeeder account (workspace/ID) or a genuine CRM record; use "high-intent", "active", "engaged", or "returning" instead of "hot"/"warm".

- **Do not expose individual contact PII** (names, emails, phone numbers, LinkedIn URLs). Counts, departments, seniority levels, and persona-match counts are fine. Identifying detail is not.
- **Do not trigger enrichment jobs** (`create_company_enrichment_job`, `create_find_contact_data_job`). This brief is research, not action. Offer to invoke them as a "Recommended next move" only.
- **Do not call `get_company_financials` by default.** It charges per call. Only on explicit request.
- **Do not invent data.** ICP match, signal counts, page views, contact counts — only report what the tools return.
- **Do not chain to outreach drafting, CRM writes, or list management** on direct user invocation without explicit opt-in. Recommend them as next moves using the skill names above. Exception: if invoked by the Leadfeeder Agent as part of a declared multi-step chain, the agent may proceed with `find-my-buyer`, `outreach-companion`, or `add-to-pipeline` without waiting for confirmation.
- **Do not produce a brief for an `out_of_business` company.** Stop and notify the user instead.

## Example: good output

````markdown
# Company Brief — Acme Corp
*Generated 2026-05-29 · engagement window: last 90 days*

European technical inspection, testing, certification, and training group. €1.58B revenue, 14,271 employees across 70+ countries. ✅ Full ICP match — DE · Pro Services · enterprise size · B2B.

## Snapshot
- **Industry:** Technical Testing & Analysis · Management Consultancy · Educational Support
- **Size:** 14,271 employees · €1.58B revenue (2023)
- **Location:** Hannover, DE (HQ) · 70+ country presence
- **Legal form / founded:** GmbH
- **Intent score:** 🟢 10 (HIGH)
- **ICP match:** ✅ Full — DE location, Pro Services industry, 10000+ employee bucket, B2B
- **Tags:** `Tier-1 Pro Services` · `DACH`
- **CRM:** Not found in your CRM

## Engagement (last 90 days)
- **Total sessions:** 4
- **First seen / Last seen:** 2026-03-12 / 2026-05-29
- **Top landing pages:** /
- **Top sources:** Bing organic, Direct
- **Deep visits:** None — all sessions were single-page
- **Trend:** Stable, single visits across the window. Today's visit is the first in 2 weeks.
- **Identified visits:** 1 session from 1 distinct identified contact (names withheld; see Find My Buyer skill)

## People on file (2,838 contacts)
- **Departments:** Engineering (612), IT (487), Operations (340), HR (210)
- **Seniority:** C-level: 14 · VP/Director: 87 · Manager: 412 · IC: 2,325
- **Buyer Persona matches:**
  - ✅ "Head of Marketing" → 6 matching contacts
  - ✅ "Sales Director" → 11 matching contacts
  - ✅ "Revenue Operations Manager" → 4 matching contacts
  - ❌ "IT Security Lead" → 0 (gap: no contacts on file)
- **Decision-maker availability:** ✅ Yes — strong senior coverage across HR, IT, Sales

## Recent signals (last 90 days)

### Hiring (13 ads)
- Strategic HR Business Partner — 2026-04-22
- IT Security Specialist (Cloud & Web) — 2026-04-08
- SAP Frontend Engineer — 2026-05-20
- HR Controlling / People Analytics Manager — 2026-05-06
- Working Student Finance — 2026-05-26
- +8 more across HR, Engineering, IT Security
*Why it matters: hiring is concentrated in strategic HR functions, IT Security, and SAP front-end — an org rebuild that aligns with our visitor-intent / RevOps narrative.*

## Recommended next move

Active expansion signal: 13 open roles in 90 days concentrated in HR strategic functions, IT Security, and SAP front-end. Combined with full ICP fit and 2,800+ contacts on file, this is a Tier-1 outbound target. The hiring pattern suggests org-design or function-rebuild work that aligns with our visitor-intent / RevOps narrative.

- **`find-my-buyer`** — surface the Strategic HR Business Partner and Head of Marketing contacts to lead with
- **`outreach-companion`** — draft a personalised opener grounded in the hiring spike + today's visit
- **Add to your pipeline** — not in your CRM yet (missed-routing gap): tag it "Tier-1 Pro Services" and add it to your DACH enterprise list in Leadfeeder so it's tracked. (`add-to-pipeline` — writes tags/lists in Leadfeeder; getting it into your CRM is a separate manual step.)

Copy any of these to run the next step:

```
Who should I reach out to at Acme Corp?
```

```
Prep me for outreach to Acme Corp
```

---

**Company website:** http://www.acme.com
````

Keep briefs tight and actionable. The reader is deciding "do I open this company today or not." The Recommended next move section is what converts the brief into work.
