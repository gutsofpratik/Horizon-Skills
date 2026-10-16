---
name: find-my-buyer
description: >
  Identify the best 1–5 contacts to reach out to at a named company, ranked by Buyer Persona fit and visit identification, plus a buying-committee coverage read showing which departments are covered and which are gaps. Use this skill when the user asks "who should I reach out to at [company]?", "find my buyer at Acme", "who's the right contact at Acme", "find the decision-maker at [company]", "who do I call at [company]", "do I have the buying committee covered at [company]", or any prompt asking for a ranked contact shortlist at a specific company. Surfaces names, titles, and emails — PII exposure is intentional and consented by invocation.
metadata:
  version: "1.0.0"
---

# Find My Buyer

Load the user's configured Buyer Personas, resolve the target company, search for matching contacts, cross-reference with visit identification data, and return a ranked shortlist of 1–5 contacts. This is the only skill in the suite that intentionally surfaces contact-level PII (name, title, email) — that is its purpose.

## Language

Produce the **entire response in the language the user wrote in** — English request → English output, German request → German output, and so on. This applies to everything the skill emits: the context line, all field labels, the buyer-persona coverage, edge-case messages, and any credit-consumption warning and confirmation. Do **not** translate data values — company names, contact names, titles, URLs, email addresses, tag names, and persona names stay verbatim as the tools return them. Copy-paste follow-up prompts should also be written in the user's language (they still trigger the right skill). If the input language is unclear, default to English.

## When this skill triggers

Trigger when the user names a specific company and asks who to contact, reach out to, or call. Trigger silently. Honor any explicit persona or seniority filter in the prompt ("the CFO", "someone in RevOps", "using the Enterprise Buyer persona").

Do not trigger for company-level research — that is `visitor-company-brief`. Do not trigger for outreach drafting — that is `outreach-companion`. This skill's job is contact identification only.

## Inputs to determine before executing

Identify these from the user's prompt. Use defaults if unspecified — do not ask.

- **Company** — name, domain, or Leadfeeder company ID. Required.
- **Persona filter** — default: all configured Buyer Personas. Honor explicit overrides ("using the SDR persona", "Enterprise Buyer only").
- **Seniority filter** — default: none (all seniorities). Honor explicit overrides ("VP or above", "C-level only", "manager level").
- **Visit window** — default last 90 days for visit cross-reference. Honor overrides.

## Workflow

### Step 0 — Resolve the Leadfeeder account (before any other tool call)

Determine the `account_id` to use for every tool call in this skill, in priority order:

1. **Account named in the request (highest priority).** If the prompt or scheduled-task instruction explicitly names an account — an account ID (e.g. "account 01234") or an unambiguous account name — use that account for all tool calls. This overrides every source below and is the recommended way to make an unattended/scheduled task fully self-contained.
2. **Configured Account ID.** Otherwise, the plugin's configured Leadfeeder Account ID is: `${user_config.account_id}`. If that resolves to a real, non-empty account ID (not blank, and not the literal unsubstituted `${user_config.account_id}` token), use it for all tool calls and do **not** call `get_account_info` or ask the user.
3. **Already selected this session.** Otherwise, if an account was already chosen earlier in the session, reuse that.
4. **Fallback.** Otherwise call `get_account_info`. If exactly one account is returned, use it. If several are returned, ask the user to pick. When running unattended (e.g. a scheduled task) asking is impossible — if no account was named and none is configured, stop and report that a **Leadfeeder Account ID** must either be named in the task prompt or set in the plugin configuration for automated runs.

### Step 1 — Resolve company and load personas (parallel)

Call in parallel:
- `search_companies` with the company name or domain to resolve `company_id`. If multiple plausible matches, present the top 3 and disambiguate before continuing.
- `get_buyer_personas` to load all configured personas. If the user specified a persona by name, also call `get_buyer_persona` for that one to read its full filter criteria.

### Step 2 — Search contacts and pull visit data (parallel, once company_id is known)

Call in parallel:
- `search_contacts` with `company_ids: [company_id]` (note: the parameter is an array, not a scalar — passing a bare `company_id` is silently ignored and the call returns an error). Fetch up to 50 candidates (`page_size: 50`) to ensure good persona coverage. **Optimization:** pass `buyer_persona_ids` containing all loaded persona IDs — the API will pre-filter to contacts matching at least one persona, reducing noise significantly. If no personas are configured, omit `buyer_persona_ids` and fetch all contacts. Also pass `filters: {has_email: true}` to skip contacts without an email address.
- `search_web_visits` with `filters: {company_id: company_id}`, using `start_date`/`end_date` at top level for the 90-day window. Extract the set of identified contact IDs that appear in the visit records — match strictly by a contact's own ID/email appearing on a visit record. A company or one of its office locations appearing in the visit stream does **not** mean any specific contact visited; only treat a person as "identified" when that person is the identified visitor.
- `get_company` with `include=crm_connections.crm_record.crm_owner` for the resolved `company_id` — to read the company's CRM status. Plain `include=crm_connections` returns only a stub (`crm_record` = `{id, type}`, no owner); the deeper path sideloads the record and owner. A populated `relationships.crm_connections` means the company is in the CRM. Each `crm_record` is polymorphic (`crm_record.type` = `crm_organization` | `crm_contact` | `crm_lead`): read **URL** from `crm_record.attributes.crm_url`, **name** by type (`crm_organization` → `attributes.name`; `crm_contact`/`crm_lead` → `attributes.first_name` + `attributes.last_name`), **owner** from `crm_record.relationships.crm_owner.attributes.name` (say "owner not set" if only a stub). **Render as a markdown link** — record name is the clickable text, `crm_record.attributes.crm_url` the target; never print the raw URL or leave the name unlinked. This complements the contact shortlist: if the company is already in the CRM, coordinate with the owner rather than cold-outreach the contacts you surface.

**Cost note (subscription coverage).** `search_contacts` and `search_web_visits` above are free, so the ranked shortlist costs nothing. The `get_company` CRM-status read charges **1 credit only if this company hasn't been accessed in the last 12 months**. Use the `search_web_visits` result as the free coverage signal:
- **Visits in the last 12 months → COVERED.** `get_company` is free — run it for CRM status as normal.
- **No visits in 12 months → UNCOVERED.** **Skip the `get_company` CRM read** — don't spend a credit just for CRM context. Still deliver the full contact shortlist (free), and set the CRM line to "Not checked — company is outside your free 12-month window (would cost 1 credit; ask if you want it)." Only run `get_company` for an uncovered company if the user explicitly asks. Report `meta.credits.charged` if you do.

Enrichment (`create_find_contact_data_job`) is separately credit-consuming and stays behind its own Cost Guard in Step 4, regardless of coverage.

### Step 3 — Rank contacts

Apply this rubric in order:

1. **Persona match.** Score each contact against all loaded Buyer Personas. Full match (all persona filters satisfied) ranks above partial match, which ranks above no match. If the user specified a persona, only full matches for that persona qualify for the shortlist.
2. **Site visit identification.** Contacts whose ID or email appears in the `search_web_visits` results (last 90 days) receive a boost — they are warm.
3. **Seniority.** Within the same persona-match tier, higher seniority ranks higher (C-level > VP/Director > Manager > IC). Apply the user's seniority filter if specified.
4. **Recency of visit identification.** Among visit-identified contacts, more recent identification wins.

Take the top 1–5 after ranking. Never pad to 5 if fewer strong matches exist — a shortlist of 2 good matches is better than 5 weak ones.

### Step 3.5 — Assess buying committee coverage

The shortlist answers "who do I call first". Enterprise deals also need "do I have the committee covered". Compute coverage across **all** contacts returned by `search_contacts` (not just the shortlist), so a strong contact you didn't shortlist still counts toward coverage.

**Check every configured Buyer Persona — return them all, drop none.** Load every persona via `get_buyer_personas` and evaluate each one against the contacts on file. The output must list **every** configured persona explicitly, each with its verdict and a one-line reason. Never omit, merge away, or silently drop a persona — including personas with zero matches, and including cases where only one persona is configured. Each persona gets one of:

- **✅ Covered** — ≥1 contact on file fully matches the persona; state the count (e.g. "3 contacts match").
- **⚠️ Thin** — only a partial match exists; say what's missing.
- **❌ Gap** — zero contacts on file match it; say "no contacts on file matching this persona".

Every verdict must be grounded in the `search_contacts` data — never invent a contact to fill a seat.

**If zero Buyer Personas are configured**, there are none to check: say "No Buyer Personas configured", suggest configuring them, and fall back to a department read of the contacts on file (which core functions are present vs. absent — only for functions plausibly relevant to the deal; don't assert a canonical committee the user never defined).

You may add, as a supplementary note *below* the persona list, a notable department gap relevant to the deal (e.g. "no IT/Security contact on file"). That is in addition to — never a replacement for — the full per-persona list. **The per-persona list is mandatory whenever ≥1 persona is configured; there is no skip condition for it.**

### Step 4 — Check for empty results → enrichment path

If Step 3 yields zero contacts (no contacts on file for this company at all, not just no persona matches):

1. Tell the user clearly: "No contacts on file for {Company}."
2. Offer to run a Find Contact Data enrichment job to discover contacts.
3. **Cost Guard — mandatory before any enrichment:**
   a. Call `estimate_find_contact_data_job` for the company and surface the estimated credit cost to the user.
   b. Wait for explicit "yes" confirmation before proceeding. Do not auto-trigger.
   c. On confirmation: call `create_find_contact_data_job`.
   d. Call `get_find_contact_data_job` to check status. If the job completes synchronously, re-run Step 2–3 with the new contacts. If it is async (still running), tell the user the job is in progress and they can re-run this skill once it completes.

If contacts exist but none match the specified persona or seniority filter, do not trigger enrichment — tell the user what is on file and suggest relaxing the filter.

## Output format

**Output contract — identical every run.** Reproduce the structure below **exactly**, on every invocation, regardless of anything earlier in this thread. If you've already run this skill in the conversation, do not vary, restyle, or "improve" the format next time — output the same template verbatim; this template is the single source of truth. Keep the exact headings, field labels, and order; don't invent new sections, don't renumber, don't rename fields, and add no decorative emoji beyond those the template already uses (✅ ⚠️ ❌).

Use this structure (the outer block is shown with four backticks so the copy blocks nest correctly — your actual output is plain markdown):

**Include a generation timestamp.** Put `*Generated {current date}*` directly under the title — use the current date (a point-in-time snapshot); it must always be present.

**Only show fields you actually have.** `search_contacts` returns a name, email, and a coarse seniority bucket — the **job title and department are often not returned**. If a contact's title or department isn't in the response, omit it from the header (`### {Full Name}`) entirely — never show a blank, "N/A", the raw seniority bucket as a title, or a guessed title/department. The real title, phone, and LinkedIn come from `get_contact` (credit-consuming) via the per-contact prompt below.

**Full-details prompt (per contact).** Give every listed contact its own copy block: `Get full contact details for {Full Name} at {Company Name}`. Running it calls the `get_contact` tool — a deep read that consumes **~1 credit** (unless that contact was accessed in the last 12 months); Claude will confirm the credit cost before fetching.

**Missing contact data is "not available", never a "gap" or a failing.** If contacts have no email (or no phone) on file, state it plainly and neutrally — e.g. "No email on file for these contacts (Leadfeeder has phone/social for some)." Do **not** call it a "data-quality gap", do **not** frame it as something Leadfeeder is failing to provide or is responsible for. If the data isn't there, it simply isn't available — report that fact without editorialising it as a shortfall. (Reserve "gap" for **persona/committee** coverage — a real absence of a matching contact — not for missing fields on the contacts you do have.)

**"Visited site" is person-level, not location-level.** This flag is strictly whether *this contact* was identified in the visit stream — i.e. their contact ID/email appears on a visit record. **Never** attach company-location or office activity to it as if the person visited: a "{Company} Switzerland office" showing up in the visit stream is not the same as identifying this contact, and phrasing like "Not identified in the last 90 days — but {Company} Switzerland office" is misleading. If location-level activity is genuinely worth noting, put it on its own line, phrased as explicitly unattributed: **"{Location} was active in the visit stream, but couldn't be attributed to this specific person."**

````markdown
## Find My Buyer — {Company Name}
*Generated {current date}*

{One-line context: ICP fit verdict + total contacts on file + how many matched.}

### Start here
{Lead with the answer so the reader never has to scroll for it. Two lines:}
{1. **The one contact to reach first** — name + one-line why (visit-identified, strongest persona fit, seniority).}
{2. **The headline read** — e.g. "3 of 8 configured personas covered." When nothing standard matches, say so plainly: "No standard sales/marketing/RevOps persona matches — this is an {type} firm; your strongest lead is behavioural: {Name}, a self-directed identified visitor."}

**CRM:** {If connected: "[{record name}]({crm_record.attributes.crm_url}) · Owner: {owner name — or 'owner not set'}" (record name derived by type per the capture rules) — coordinate with the owner before reaching out to the contacts below. If not connected: "Not found in your CRM — clean net-new company."}

---

### 1. {Full Name}{ · {Title} — only if returned}{ · {Department} — only if returned}
- **Seniority:** {C-level / VP / Director / Manager / IC}
- **Persona match:** {✅ Full match: "{Persona Name}" / ⚠️ Partial: "{Persona Name}" (missing: {criterion}) / ❌ No match}
- **Visited site:** {✅ Identified — this person appears in the visit stream, last seen {date} / ❌ Not identified in the last 90 days — this specific person hasn't been matched to a visit} {Optional, only if there was location-level activity: on the next line, "{Location} was active in the visit stream, but couldn't be attributed to this person."}
- **Email:** {email address}
- **Full details** (job title, phone, LinkedIn) — copy to fetch via `get_contact` (~1 credit):

```
Get full contact details for {Full Name} at {Company Name}
```

### 2. {Full Name}{ · {Title} if returned}{ · {Department} if returned}
- **Seniority:** ...
- **Persona match:** ...
- **Visited site:** ...
- **Email:** ...
- **Full details:**

```
Get full contact details for {Full Name} at {Company Name}
```

{Repeat for up to 5 contacts — each with its own "Get full contact details" copy block, and each omitting title/department if not returned. Stop earlier if quality drops sharply.}

---

**Buyer persona coverage** — every configured persona, checked against the contacts on file (list ALL of them, one line each; never drop a persona):
- ✅ "{Persona A}" — covered ({N} contacts match)
- ✅ "{Persona B}" — covered ({N} contacts match)
- ⚠️ "{Persona C}" — thin (1 partial match, no full match; missing {criterion})
- ❌ "{Persona D}" — gap (no contacts on file matching this persona)
{One line for EVERY configured persona — none omitted, even if all covered or all gaps. This is the detail section; the top-line read already appeared in "Start here".}
{Optional supplementary line: a notable **committee/persona** gap relevant to the deal, e.g. "No IT/Security contact on file." If contacts simply lack email/phone, state it neutrally ("no email on file for these contacts; Leadfeeder has phone/social for some") — never as a "data-quality gap" or a Leadfeeder failing.}
{Then a one-line so-what: e.g. "Strong on RevOps + Sales; the Marketing persona is thin and you have no IT/Security contact — likely a blocker for a security-sensitive deal."}
{If zero personas are configured, replace this block with "No Buyer Personas configured" + the department read.}

**Suggested next step:** phrase in plain language, outcome first (not "Run `skill`") — "Get visit-grounded talking points for {top contact name} to personalise your outreach" (`outreach-companion`), or "Tag {Company Name} and add it to a Leadfeeder list so it's tracked" (`add-to-pipeline` — writes tags/lists inside Leadfeeder; it does not create a CRM record or assign a CRM owner).{ If there is a committee gap, optionally add: " To fill the {gap} seat, re-run with a relaxed persona filter or run a Find Contact Data enrichment job."}

Copy to run the next step (fenced blocks give a one-click copy button):

```
Prep me for outreach to {top contact name} at {Company Name}
```

```
Add {Company Name} to a list in Leadfeeder
```
````

### When no contacts on file (enrichment path)

```markdown
## Find My Buyer — {Company Name}

No contacts on file for this company.

**Estimated enrichment cost:** {N} credits ({source from estimate_find_contact_data_job}).

Want me to run a Find Contact Data job to discover contacts? This will consume the credits above. Reply **yes** to confirm.
```

## Edge cases

- **Company not found.** Stop and tell the user. Offer to try a broader name or domain.
- **Multiple company matches.** Present top 3, disambiguate before continuing.
- **Contacts exist but none match persona/seniority filter.** Tell the user what is on file (total count, department/seniority breakdown). Suggest relaxing the filter or switching to a different persona. Do not trigger enrichment.
- **No Buyer Personas configured.** Tell the user and fall back to seniority-only ranking. Suggest they configure Buyer Personas in Leadfeeder for sharper results.
- **Enrichment job is async.** Tell the user the job is running and to re-run the skill once it completes. Do not poll indefinitely.
- **Enrichment job returns no new contacts.** Tell the user clearly. Do not retry automatically.

## Source citation rule

Every contact in the shortlist must come from `search_contacts` results. Visit identification flags must come from `search_web_visits` results. CRM record name, URL, and owner must come from the sideloaded `crm_record` (and its `crm_owner`) under `relationships.crm_connections` on the `get_company` response — `crm_record.attributes.crm_url`, the name from `crm_record.attributes` per record type, and `crm_record.relationships.crm_owner.attributes.name` — never assert the company is (or isn't) in the CRM without it. Buying committee coverage verdicts (covered / thin / gap) must be derived only from `search_contacts` results cross-referenced with the loaded Buyer Personas — never assert a covered seat without a matching contact on file, and never assert a gap for a persona or department the user has not configured. Do not infer or fabricate any of these.

**Internal consistency (trust).** Every restated fact — total counts, department/seniority breakdowns, the committee coverage summary vs. the per-seat lines, contact counts — must agree across the output. A stated count must equal the items you list (e.g. the "covered / thin / gap" summary line must match the per-seat verdicts below it). Re-check before finishing; two sections disagreeing about the same fact is a trust-breaker.

## What NOT to do

- **Do not call a visitor an "account" or a "hot/warm lead."** A website visitor is a **company** — "account" implies a CRM relationship this data doesn't carry. Reserve "account" for the user's Leadfeeder account (workspace/ID) or a genuine CRM record; use "high-intent", "active", "engaged", or "returning" instead of "hot"/"warm".

- **Do not trigger enrichment** (`create_find_contact_data_job`) without completing the Cost Guard flow — estimate first, explicit confirmation second.
- **Do not surface contact PII from other skills' context.** Only surface contacts resolved in this skill's own `search_contacts` call.
- **Do not rank by engagement alone** without persona scoring — persona fit is the primary signal.
- **Do not pad the shortlist** to reach 5 if fewer strong matches exist. Quality over quantity.
- **Do not handle bulk companies.** One company per invocation. For multiple companies, the user should invoke the skill once per company.

## Example: good output

````markdown
## Find My Buyer — Acme Corp
*Generated 2026-06-27*

✅ Full ICP match · 2,838 contacts on file · 3 personas matched.

### Start here
**Reach Jane Doe first** — Head of Revenue Operations, a full match for your "Revenue Operations Manager" persona, and the only contact identified in the visit stream (last seen 2026-06-20).
**Coverage:** 3 of 3 configured personas covered; strong commercial coverage, no technical (IT/Security) contact on file.

**CRM:** [Acme Corp](https://acme.lightning.force.com/lightning/r/Account/0018000000abcde/view) · Owner: Robert Roe — coordinate with Robert before reaching out to the contacts below.

---

### 1. Jane Doe · Head of Revenue Operations · Sales
- **Seniority:** Director
- **Persona match:** ✅ Full match: "Revenue Operations Manager"
- **Visited site:** ✅ Identified — this person appears in the visit stream, last seen 2026-06-20
- **Email:** jane.doe@acme.com
- **Full details** (job title, phone, LinkedIn) — copy to fetch via `get_contact` (~1 credit):

```
Get full contact details for Jane Doe at Acme Corp
```

### 2. John Sample · VP Sales EMEA · Sales
- **Seniority:** VP
- **Persona match:** ✅ Full match: "Sales Director"
- **Visited site:** ❌ Not identified in the last 90 days — this specific person hasn't been matched to a visit
  The Acme Switzerland office was active in the visit stream, but couldn't be attributed to John.
- **Email:** j.sample@acme.com
- **Full details:**

```
Get full contact details for John Sample at Acme Corp
```

### 3. Mary Major
- **Seniority:** Director
- **Persona match:** ✅ Full match: "Head of Marketing"
- **Visited site:** ❌ Not identified in the last 90 days — this specific person hasn't been matched to a visit
- **Email:** m.major@acme.com
- **Full details:**  *(title and department weren't returned by `search_contacts`, so they're omitted from the header above)*

```
Get full contact details for Mary Major at Acme Corp
```

---

**Buyer persona coverage** — every configured persona, checked against the contacts on file:
- ✅ "Head of Marketing" — covered (6 contacts match; Mary Major shortlisted)
- ✅ "Sales Director" — covered (11 contacts match; John Sample shortlisted)
- ✅ "Revenue Operations Manager" — covered (4 contacts match; Jane Doe shortlisted)

Supplementary: no IT/Security contact on file (department gap — not a configured persona).

All three configured personas are covered — you can open with Jane (RevOps, and she's visited). But there's no technical buyer on file, so if this deal touches data security or integration sign-off, that's a likely blocker.

**Suggested next step:** Get talking points for Jane Doe grounded in her recent visit to personalise your outreach, or tag Acme Corp and add it to a Leadfeeder list so it's tracked. To fill the IT / Security seat, re-run with a relaxed persona filter or run a Find Contact Data enrichment job.

Copy to run the next step:

```
Prep me for outreach to Jane Doe at Acme Corp
```

```
Add Acme Corp to a list in Leadfeeder
```
````
