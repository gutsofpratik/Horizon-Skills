---
title: Federal Buyer Expansion Plan
description: How to build a one-office federal buyer expansion plan for a target vendor and buyer office.
---

# Federal Buyer Expansion Plan

Use this reference when the user wants a buyer-specific federal pursuit plan for one vendor and one federal office, not a general vendor deep dive or a market scan.

## Goal
- Resolve the target vendor and buyer office, analyze the office's recent buying pattern, judge the vendor's access and fit, surface evidence-backed contacts, and identify near-term demand.
- Keep the answer office-specific and tied to the last 24 months of buying behavior.
- For a document-style deliverable, prefer the structure in `assets/federal-buyer-expansion-plan-template.md` from the skill root.
- Before delivering a customer-facing brief, contact list, or companion artifact, read [Final Capture Deliverable Quality Checks](./final-deliverable-quality-checks.md).

## Workflow

### 1. Resolve the vendor and the office first
- Resolve the target vendor with `Search_Vendors`.
- Resolve the target buyer office with `Search_Federal_Agencies`.
- Do not proceed until both sides resolve cleanly enough to search.

### 2. Derive the vendor's lane focus
- Use `Search_Federal_Contract_Awards` for the resolved vendor as an aggregation-first vendor-history pass over the last 24 months.
- Reuse dominant NAICS, PSC, set-aside, vehicle, and IDV patterns as the vendor's most credible lane focus.
- If the vendor-history pass is too thin to support a defensible lane focus, ask for the minimum NAICS, PSC, or work-category clarification and stop.

### 3. Build the office buying profile in both roles
- Run aggregation-first office buying passes with `Search_Federal_Contract_Awards` for the resolved office as both:
  - `contracting_federal_agency`
  - `funding_federal_agency`
- Keep the same 24-month window in both passes.
- Use the vendor-derived lane focus to interpret which office lanes matter most.
- Follow with row-level retrieval to select representative recent buys for each role.

### 4. Judge vendor access and ordering-path fit
- Use `Search_Federal_Contract_Awards` to check for direct vendor overlap with the office.
- If direct overlap is sparse or absent, run one careful adjacent-evidence pass against the office's dominant lanes, value bands, and ordering patterns.
- Keep direct evidence separate from adjacent or inferred evidence.
- If office award evidence shows meaningful IDV or vehicle concentration, run one targeted `Search_Federal_Contract_IDVs` or `Search_Federal_Contract_Vehicles` follow-on lookup to explain the ordering path.
- If direct office overlap is sparse and teaming with an established office incumbent is a credible access path, use `references/team-on-an-opportunity.md` to identify and coordinate with potential partners on live opportunities in the office.

### 5. Pull evidence-backed contacts and live demand
- Use `Search_Contacts` against the office, narrowing with representative award IDs when needed.
- If no usable contacts remain after narrowing, say so clearly and do not invent outreach targets.
- Run a current-demand check with `Search_Federal_Contract_Opportunities`:
  - active solicitations
  - recent pre-solicitations
- Keep live demand subordinate to the historical office buying pattern. Do not let a sparse live cohort override the core office profile.

### 6. Verify and trim
- Remove obvious outliers, weak adjacent-evidence claims, and redundant office rows.
- Lower confidence when the plan depends on sparse office history, one-off vehicle signals, or one-record contact evidence.
- If the evidence is too thin for a credible office plan, say so clearly and stop.

## Output contract
- Return vendor and office resolution, search approach, office buying profile, representative recent buys, evidence-backed contacts, ordering-path and access assessment, office-specific pursuit angles, current open and near-term opportunities, next actions, and confidence.
- Make rendered briefs read like pursuit memos, not raw market-scan notes. Open with an expansion call that states pursuit posture, best entry lane, access path, primary 90-day action, confidence, and the critical caveat.
- Use compact markdown tables for buying-profile facts, representative buys, contacts, and live opportunities.
- Keep resolved scope as a short note or short bullet list when the document is already table-heavy; avoid a full scope table if it causes an early page split.
- Keep tables narrow enough for portrait Markdown/PDF output. Prefer three-column evidence digests over wide tables that expose role, vendor, value, vehicle, and implication as separate columns.
- Use three-column entry-route tables like `Route`, `How to use it`, and `Watch item`; fit labels can be folded into the route name or route text.
- In the brief, summarize representative buys as `Buy`, `Signal`, and `Capture implication`. Put full award identifiers, vendors, values, roles, vehicles, and row-level evidence in companion CSV or JSON when needed.
- Summarize contacts as `Contact`, `Use`, and `Caveat`; do not over-format every returned contact field into the rendered plan.
- Summarize live demand as `Opportunity`, `Timing`, and `Capture action`.
- Include a short 90-day pursuit playbook so the output ends with an executable capture plan rather than only analysis.
- If companion artifact links create a trailing blank page in a rendered PDF, omit them from the rendered brief and provide them in the final response instead.
- Keep pursuit angles short and tied directly to observed buying evidence.
- Do not turn the answer into a full offer packet or long outreach draft unless the user asks for that separately.
