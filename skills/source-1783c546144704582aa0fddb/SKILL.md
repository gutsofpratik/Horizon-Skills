---
name: add-to-pipeline
description: >
  Tag a company and/or add it to a list in Leadfeeder. Use this skill when the user wants to action a company — "tag Acme as Hot Lead", "add Acme to my DACH-Enterprise list", "mark Acme as Tier-1", "put Acme in the Enterprise Q3 list", "add [company] to [list]", "tag [company] as [tag]". Always confirms the exact writes before executing. The only write skill in the suite.
metadata:
  version: "1.0.0"
---

# Add to Pipeline

Tag a company and/or add it to a Leadfeeder list. This is the only write skill in the suite — all others are read-only. **All writes go to Leadfeeder only (tags and lists); this skill never adds to or updates the user's CRM.** State that explicitly in the confirmation and the outcome so no one assumes the company has synced to their CRM. Always show the user exactly what will be written and wait for confirmation before executing. Report success or failure per write transparently.

## Language

Produce the **entire response in the language the user wrote in** — English request → English output, German request → German output, and so on. This applies to everything the skill emits: the confirmation plan, the CRM heads-up and Leadfeeder-only disclaimer, the outcome report, and any follow-up prompts. Do **not** translate data values — company names, tag names, list names, CRM record names, owner names, and URLs stay verbatim as the tools return them (and the exact tag/list to create must be the user's literal wording). If the input language is unclear, default to English.

## When this skill triggers

Trigger when the user explicitly asks to tag, label, add, or categorise a company. Trigger silently on detection — but always pause for confirmation before executing writes. Honor multiple operations in a single prompt ("tag Acme as Hot Lead AND add it to the DACH list").

Do not trigger on read-only questions about tags or lists — surface that information inline and stop.

## Inputs to determine before executing

Identify these from the user's prompt. Use defaults if unspecified — do not ask.

- **Company** — name, domain, or Leadfeeder company ID. Required.
- **Tag(s)** — name of one or more tags to assign. Optional if a list is specified.
- **List(s)** — name of one or more lists to add the company to. Optional if a tag is specified.

At least one tag or one list must be specified. If neither is mentioned, ask the user what they want to do before proceeding.

## Workflow

### Step 0 — Resolve the Leadfeeder account (before any other tool call)

Determine the `account_id` to use for every tool call in this skill, in priority order:

1. **Account named in the request (highest priority).** If the prompt or scheduled-task instruction explicitly names an account — an account ID (e.g. "account 01234") or an unambiguous account name — use that account for all tool calls. This overrides every source below and is the recommended way to make an unattended/scheduled task fully self-contained.
2. **Configured Account ID.** Otherwise, the plugin's configured Leadfeeder Account ID is: `${user_config.account_id}`. If that resolves to a real, non-empty account ID (not blank, and not the literal unsubstituted `${user_config.account_id}` token), use it for all tool calls and do **not** call `get_account_info` or ask the user.
3. **Already selected this session.** Otherwise, if an account was already chosen earlier in the session, reuse that.
4. **Fallback.** Otherwise call `get_account_info`. If exactly one account is returned, use it. If several are returned, ask the user to pick. When running unattended (e.g. a scheduled task) asking is impossible — if no account was named and none is configured, stop and report that a **Leadfeeder Account ID** must either be named in the task prompt or set in the plugin configuration for automated runs.

Note: resolving the account does **not** relax the write-confirmation gate in Step 4 — a configured account ID skips *account selection*, never write confirmation.

### Step 1 — Resolve company and existing tags/lists (parallel)

Call in parallel:
- `search_companies` with the company name or domain to resolve `company_id`. If multiple plausible matches, present the top 3 and disambiguate before continuing.
- `get_tags` with `page_size: 100` to load all existing tags in one call. If `meta.pagination.total_count` exceeds 100, paginate with `page_num` until all pages are fetched.
- `get_lists` with `filter_scope: "company"` and `page_size: 100` to load all existing company lists. The `filter_scope` parameter is required — omitting it causes an error. Paginate if `total_count` exceeds 100.

Once `company_id` is resolved, decide whether to fetch CRM context based on **subscription coverage** — the tag/list writes are free, but the `get_company` CRM read charges **1 credit if the company hasn't been accessed in the last 12 months**, and it's not worth a credit just for a confirmation heads-up. Probe coverage for free: call `search_web_visits` for `company_id` over the **last 12 months**.

- **Visits found → COVERED.** Call `get_company` with `include=crm_connections.crm_record.crm_owner` (free) to read the company's CRM status. Read from each connection's `crm_record` (polymorphic — `crm_record.type` = `crm_organization` | `crm_contact` | `crm_lead`): **name** by type (`crm_organization` → `attributes.name`; `crm_contact`/`crm_lead` → `attributes.first_name` + `attributes.last_name`), **URL** from `crm_record.attributes.crm_url`, **owner** from `crm_record.relationships.crm_owner.attributes.name`. Surface it in the confirmation (Step 4) as a markdown link (record name → `crm_url`).
- **No visits in 12 months → UNCOVERED.** **Skip `get_company`.** Omit the CRM line from the confirmation (or note "CRM status not checked — company is outside your free 12-month window"). Do not spend a credit for context on a write.

Either way the writes proceed normally — coverage only affects whether the optional CRM context is fetched.

### Step 2 — Match tags and lists

For each tag and list the user named:
- **Exact match found** → resolved, ready to assign.
- **Close match found** (name differs by capitalisation, spacing, or minor typo) → present the match and confirm it is the right one before using it.
- **No match found** → tell the user the tag or list does not exist and ask whether to create it. Do not create anything without explicit "yes".

### Step 3 — Create missing tags or lists (if confirmed)

For each confirmed "create new" item:
- For a new tag: call `create_tag` with the user-supplied name.
- For a new list: call `create_list` with the user-supplied name.

This step requires its own confirmation before any writes from Step 4 begin. If the user confirms creation in the same message as the overall write, treat that as a combined confirmation and proceed.

### Step 4 — Confirm all writes

Before executing any assignment, show the user the complete write plan and wait for explicit confirmation:

```
I'm about to make the following changes:

  • Assign tag "{Tag Name}" → {Company Name}
  • Add {Company Name} → list "{List Name}"

Confirm? (yes / no)
```

Do not proceed until the user replies with a clear affirmative. A non-answer or topic change is not a confirmation — ask again once, then abort.

### Step 5 — Execute writes (parallel where possible)

On confirmation, call in parallel:
- `assign_tags_to_company` for each tag (one call per tag if the API requires it).
- `add_company_to_lists` for each list (one call per list if the API requires it).

### Step 6 — Report outcomes

Report the result of every write individually:

- **Success:** "✅ Tagged {Company} as '{Tag}'"
- **Failure:** "❌ Failed to add {Company} to '{List}' — {error reason if available}"

If one write fails and another succeeds, report both. Never suppress a partial failure. Offer to retry failed writes if the error is transient.

## Output format

**Output contract — identical every run.** Reproduce the confirmation and outcome blocks below **exactly**, on every invocation, regardless of anything earlier in this thread. If you've already run this skill in the conversation, do not vary, restyle, or "improve" the format next time — output the same templates verbatim; these are the single source of truth. Keep the exact wording, labels, and the Leadfeeder-only disclaimer; don't rename fields and add no decorative emoji beyond those the templates already use (✅ ❌ ℹ️).

### Confirmation step (Step 4)

```markdown
I'm about to make the following changes to **{Company Name}**:

{For each tag} · Assign tag **"{Tag Name}"**
{For each list} · Add to list **"{List Name}"**

{CRM context line — include if CRM-connected: "ℹ️ Heads up: this company is already in your CRM as **[{record name}]({crm_record.attributes.crm_url})**, owned by **{owner name — or 'owner not set'}**. Coordinate with the owner if this changes what you want to do." Omit entirely if not connected.}

_This updates Leadfeeder only (tags and lists). It does **not** add the company to, or change anything in, your CRM._

Confirm? Reply **yes** to proceed.
```

### Outcome report (Step 6)

````markdown
Done. Here's what happened:

✅ Tagged **{Company Name}** as **"{Tag Name}"**
✅ Added **{Company Name}** to list **"{List Name}"**

{If any failures:}
❌ Could not assign tag **"{Tag Name}"** — {reason}

_Leadfeeder only — nothing was added to or changed in your CRM._

---

**Next move on {Company Name}** — copy to run:

```
Who should I reach out to at {Company Name}?
```

```
Prep me for outreach to {Company Name}
```
````

Show the follow-up copy blocks only after a successful write on an interactive run — omit them if the write failed or on unattended runs.

### When a tag or list needs to be created

```markdown
The tag **"{Tag Name}"** doesn't exist yet.

Create it and then assign it to **{Company Name}**? Reply **yes** to confirm.
```

## Source citation rule

Every company, tag, and list name in the confirmation and outcome report must come from MCP tool responses — `search_companies` for the resolved company, `get_tags` and `get_lists` for existing tags and lists. The CRM context line must come from the sideloaded `crm_record` (and its `crm_owner`) under `relationships.crm_connections` on the `get_company` response — `crm_record.attributes.crm_url`, the name from `crm_record.attributes` per record type, and `crm_record.relationships.crm_owner.attributes.name` — never assert a company is in the CRM (or name an owner) without it. Never invent or assume that a tag or list exists. If a tag or list is being created, the exact name to create must come from the user's prompt, not fabricated.

## Edge cases

- **Company not found.** Stop and tell the user. Offer to try a broader name or domain. Do not proceed.
- **Multiple company matches.** Present top 3, disambiguate. Do not proceed until resolved.
- **Tag or list not found, user declines creation.** Abort that specific operation. If other operations remain, confirm and execute those.
- **User names both a tag and a list, one doesn't exist.** Handle each independently — ask about creation for the missing one while confirming the existing one.
- **User aborts at confirmation.** Acknowledge clearly ("Cancelled — nothing was changed.") and stop.
- **Partial failure on execute.** Report each outcome individually. Never report overall success if any write failed.
- **Agent-invoked as part of a chain.** The agent must still respect the confirmation step — do not bypass it even in a multi-skill chain. The confirmation is a hard gate for any write operation.

## What NOT to do

- **Do not call a visitor an "account" or a "hot/warm lead."** A website visitor is a **company** — "account" implies a CRM relationship this data doesn't carry. Reserve "account" for the user's Leadfeeder account (workspace/ID) or a genuine CRM record; use "high-intent", "active", "engaged", or "returning" instead of "hot"/"warm".

- **Do not execute any write without explicit user confirmation.** The confirmation step is mandatory, even when invoked by the Leadfeeder Agent.
- **Do not delete, rename, or modify existing tags or lists.** Only assign tags to companies and add companies to lists.
- **Do not create tags or lists speculatively.** Only create if the user explicitly confirms creation.
- **Do not operate on more than one company per invocation.** One company at a time.
- **Do not suppress partial failures.** Every write outcome must be reported.
- **Do not call `assign_tags_to_company` or `add_company_to_lists` before the user confirms.** Showing the plan and waiting for "yes" is not optional.
- **Do not imply the CRM is updated.** Every confirmation and outcome must state that the change is Leadfeeder-only (tags/lists) and does not add to or change the user's CRM — a customer must never assume tagging synced the company into their CRM.

## Example: good output

*Scenario: "tag Acme as Tier-1 and add it to the DACH Enterprise list" — both tag and list already exist.*

```markdown
I'm about to make the following changes to **Acme Corp**:

· Assign tag **"Tier-1"**
· Add to list **"DACH Enterprise"**

ℹ️ Heads up: this company is already in your CRM as **[Acme Corp](https://acme.lightning.force.com/lightning/r/Account/0018000000abcde/view)**, owned by **Robert Roe**. Coordinate with the owner if this changes what you want to do.

_This updates Leadfeeder only (tags and lists). It does **not** add the company to, or change anything in, your CRM._

Confirm? Reply **yes** to proceed.
```

*User replies: yes*

````markdown
Done. Here's what happened:

✅ Tagged **Acme Corp** as **"Tier-1"**
✅ Added **Acme Corp** to list **"DACH Enterprise"**

_Leadfeeder only — nothing was added to or changed in your CRM._

---

**Next move on Acme Corp** — copy to run:

```
Who should I reach out to at Acme Corp?
```

```
Prep me for outreach to Acme Corp
```
````

---

*Scenario: "add Acme to my Q3 Targets list" — list does not exist.*

```markdown
The list **"Q3 Targets"** doesn't exist yet.

Create it and then add **Acme Corp** to it? Reply **yes** to confirm.
```

*User replies: yes*

```markdown
I'm about to make the following changes to **Acme Corp**:

· Add to list **"Q3 Targets"** (new list, will be created)

_This updates Leadfeeder only (tags and lists). It does **not** add the company to, or change anything in, your CRM._

Confirm? Reply **yes** to proceed.
```

*User replies: yes*

```markdown
Done. Here's what happened:

✅ Created list **"Q3 Targets"**
✅ Added **Acme Corp** to list **"Q3 Targets"**

_Leadfeeder only — nothing was added to or changed in your CRM._
```
