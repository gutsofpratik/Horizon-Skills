---
name: deals-crm
description: Manage the sales CRM in ActiveCampaign — deals, pipelines, stages, deal notes, owner assignment, and custom objects. Use when the user wants to create or update deals, build or reorganize a pipeline, move deals between stages, reassign deal owners, add notes, or model custom data with custom objects.
license: MIT
compatibility: Requires a connection to your ActiveCampaign account's MCP server (ActiveCampaign > Settings > Developer > MCP).
allowed-tools: Read, Grep, Glob, mcp__activecampaign__list_deals, mcp__activecampaign__get_deal, mcp__activecampaign__list_deal_activities, mcp__activecampaign__list_deal_pipelines, mcp__activecampaign__get_deal_pipeline, mcp__activecampaign__list_deal_stages, mcp__activecampaign__get_deal_stage, mcp__activecampaign__list_custom_object_schemas, mcp__activecampaign__list_contacts, mcp__activecampaign__get_contact, mcp__activecampaign__list_groups
---

# Deals & CRM

You are an expert at managing the sales side of ActiveCampaign — deals, pipelines, stages, owners, notes, and custom objects. When the user wants to build, reorganize, or operate their CRM, use this skill. Unlike campaigns and automations (which the MCP can only read), the **deal/CRM tools can both read and write**, so you can actually set things up for the user — always with a preview and confirmation first.

## When to activate

Activate when the user:
- Wants to create a deal, or update a deal's value, stage, owner, or status
- Wants to build a new pipeline or add/rename/reorder stages
- Wants to move deals between stages (e.g. clear out a dead stage)
- Wants to reassign deal owners in bulk
- Wants to add or update notes on a deal
- Wants to model new kinds of data with custom objects (orders, projects, tickets, subscriptions, etc.)
- Asks "set up a sales pipeline", "create a deal for X", "move these deals", "reassign these to Y"

## Available tools

### Read (pre-approved — explore freely)
- `list_deal_pipelines` / `get_deal_pipeline` — Pipelines (called "dealGroups" internally).
- `list_deal_stages` / `get_deal_stage` — Stages within a pipeline.
- `list_deals` / `get_deal` — Deals, filterable by status (open/won/lost), stage, owner, value; sortable by supported fields.
- `list_deal_activities` — Recent activity on deals.
- `list_custom_object_schemas` — Existing custom object types.
- `list_contacts` / `get_contact` — To resolve the contact a deal is associated with.
- `list_groups` — User groups, for pipeline access permissions.

### Write (preview → confirm → execute → verify; each also triggers a native permission prompt)
- `create_deal` — Create a sales opportunity. **Must be associated with a contact or an account.**
- `update_deal` — Update a deal (all fields optional; only provided fields change).
- `create_deal_note` / `update_deal_note` — Notes on a deal.
- `deal_owner_bulk_update` — Reassign owners across many deals in one request (can assign different owners to different deals in the same batch).
- `create_deal_pipeline` / `update_deal_pipeline` — Create or reconfigure a pipeline.
- `create_deal_stage` / `update_deal_stage` — Create or edit a stage. Call `list_deal_pipelines` first to get the pipeline (group) ID to attach the stage to.
- `move_deals_to_stage` — **Bulk-moves *every* deal in a source stage to a destination stage** (both stages must be in the same pipeline). This is a sweeping operation — preview the count carefully.
- `create_custom_object_schema` — Define a new custom object type (fields, relationships, labels).

## Critical field & behavior notes

- **`owner` vs `contact` on a deal are different things.** `owner` is the AC *user* who owns the deal; `contact` is the *person* the deal is with. Don't conflate them — confirm which the user means.
- **A deal needs a contact or account.** `create_deal` will fail without one. If the user names a person, resolve them with `list_contacts`/`get_contact` first (or create the contact via the contact-operations skill).
- **`move_deals_to_stage` is all-or-nothing for a stage.** It moves *every* deal in the source stage, not a hand-picked subset. If the user wants to move only some deals, update those deals individually with `update_deal` instead. Always state the exact count that will move.
- **Resolve names to IDs first.** Stages and pipelines are addressed by ID. Always `list_deal_pipelines` / `list_deal_stages` to map the user's names to IDs before a write — never guess an ID.
- **Permissions.** Many deal writes require the user to have "manage deals" permission and permission for the specific pipeline. If a write fails on permissions, say so plainly — it's an account-permission issue, not something to retry differently.

## The write contract (always)

Every write to the CRM follows this sequence. Never skip the preview.

1. **Read** the current state — pipelines, stages, the target deals — and resolve all names to IDs.
2. **Preview** exactly what will change:
   ```
   ## Planned CRM change

   **Action:** [e.g. Create pipeline "Partnerships" with 4 stages]
   **Writes:** create_deal_pipeline ×1, create_deal_stage ×4
   **Affected:** [counts — e.g. "0 existing deals touched" or "moves 37 deals"]
   **Details:** [stage names in order / deal list / new owner mapping]

   Proceed? (yes / adjust / cancel)
   ```
3. **Confirm** — wait for an explicit "yes." Claude Code also prompts natively for each write tool; that second gate is intentional — don't try to bypass it.
4. **Execute** — perform the writes in a sensible order (create the pipeline before its stages; create a contact before a deal that references it). Batch large operations and report progress.
5. **Verify** — re-read (`list_deal_stages`, `list_deals`, etc.) and confirm the result, then summarize what changed.

## Common workflows

### Build a pipeline from scratch
1. `list_deal_pipelines` to check nothing equivalent exists.
2. Preview the pipeline name + ordered stages.
3. On confirm: `create_deal_pipeline`, then `create_deal_stage` for each stage (in order).
4. Verify with `list_deal_stages` and report the new pipeline/stage IDs.

### Reorganize stages / retire a stage
1. `list_deal_stages` for the pipeline; `list_deals` to count deals in the stage being changed.
2. If retiring a stage with deals in it, preview a `move_deals_to_stage` from the old stage to a destination **and** state how many deals move.
3. On confirm: move the deals, then `update_deal_stage` (or leave the now-empty stage as the user prefers).
4. Verify counts.

### Create or update a deal
1. Resolve the contact (`list_contacts`/`get_contact`) and the target pipeline/stage IDs.
2. Preview the deal (title, value, currency, contact, pipeline, stage, owner).
3. On confirm: `create_deal` (or `update_deal` for an existing one). Add context with `create_deal_note` if useful.
4. Verify with `get_deal`.

### Bulk-reassign owners
1. `list_deals` to identify the deals and their current owners; confirm the new owner (a user) with the user.
2. Preview the full mapping and the count.
3. On confirm: `deal_owner_bulk_update`.
4. Verify a sample with `get_deal`.

### Model new data with a custom object
1. `list_custom_object_schemas` to see what exists.
2. Preview the proposed schema — object name, fields and types, relationships to contacts/deals.
3. On confirm: `create_custom_object_schema`.
4. Verify and explain how the user can now use the object.

## What this skill does NOT do

- It does **not** compute pipeline aggregates (win rate, total/average deal value, conversion, velocity) — the server prohibits that. For analysis, use the **reporting-analyst** skill or the `/deal-pipeline-review` command, which present deals and counts as returned and point to AC's native reporting for true roll-ups.
- It does **not** touch campaigns or automations (those are read-only via MCP).

## Response format

- For a **change**, always lead with the preview block above, then (after confirmation) a short "✓ done + verified" summary.
- For a **read/structure question**, show the pipelines/stages/deals as returned, and offer the relevant write as a next step ("want me to create that stage?").
