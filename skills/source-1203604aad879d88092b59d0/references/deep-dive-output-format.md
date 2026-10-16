---
title: Deep Dive Output Format
description: Consultant-grade Markdown output contract for GovTribe deep-dive dossiers, with profile selection, evidence rules, personalization handling, and document-readability guidance.
---

# Deep Dive Output Format

Use this reference after the target-specific deep-dive context has been gathered and the user wants a finished brief, dossier, document, or stored output.

## Goal
- Produce a senior-consultant-grade BD and capture dossier for one resolved GovTribe target.
- Use one stable Markdown contract with selected modules, not a different full template for every target type.
- Make the output useful to BD, capture, proposal, account, and leadership users who need to decide what the target means and what to do next.
- Keep source-backed facts, personalized inferences, and judgment calls visibly separate.
- Cite evidence IDs for major claims and include an evidence ledger.

## Output profile decision tree
Select modules from target attributes, lifecycle, dates, and user intent. Do not infer the profile from vague wording alone when structured fields answer it.

1. Start with the target's `govtribe_type`, notice or opportunity type, status fields, due dates, award dates, completion dates, expiration dates, and direct relationships.
2. Classify lifecycle:
   - Use `live_pursuit` when the target is an open or future opportunity, forecast, upcoming grant opportunity, or active pursuit target with a current response or action window.
   - Use `market_research_shaping` when the target is an RFI, Sources Sought, Request for Capabilities, draft PWS, or market-research Special Notice whose response date has passed and no award or active solicitation supersedes it. Treat it as follow-on RFQ shaping and capture watch, not a live submission.
   - Use `recompete_planning` when the target is awarded, expiring, has an incumbent/predecessor, or is useful mainly for planning a future recompete. A past-due market-research notice does not require a full recompete module unless predecessor or follow-on evidence materially supports it.
   - Use `account_market` for agencies, states, jurisdictions, grant programs, major defense programs, and vehicles where the user needs a market or account view.
   - Use `competitor_partner_stakeholder` for vendors and contacts, and also for opportunities where likely bidders, incumbents, teaming, or customer stakeholders are central.
   - Use `funding_eligibility` for grant opportunities, grant programs, grant awards, and funding vehicles.
   - Use `vehicle_idv_award` for federal or state/local awards, IDVs, vehicles, task-order families, contract lineage, and buying channels.
   - Use `state_local_market` for state and local opportunities, awards, IDVs, vehicles, jurisdictions, and statewide scans.
3. If multiple profiles apply, include each selected module but keep each module compact.
4. If the user explicitly asks for a narrow answer, do not force every module. State the profile used and omit irrelevant modules.
5. If the user asks for a document or shareable brief, prefer the full core structure plus the selected modules.

## Required core Markdown contract
Use these headings for every finished dossier. Keep heading text stable so validation and downstream storage remain reliable.

### Title
Use:

```markdown
# Deep Dive Dossier: {{target_name}}
```

### Target metadata
Include a compact two-column table with the target name, GovTribe type, GovTribe ID, URL, notice/opportunity type, status, owner/buyer/funder, dates, set-aside or eligibility, value, and profile selection.

### Decision snapshot
Open with a short decision table. Recommended rows:
- Current read
- Primary BD use
- Pursuit, shaping, or account posture
- Highest-value action
- Main risk or unknown
- Confidence

### Executive takeaway
Write two to four tight paragraphs that state what matters, why it matters, and what the user should do next. Cite evidence IDs for the main claims.

### Source-backed target profile
Summarize the target facts that are directly supported by GovTribe records, files, linked awards, transactions, relationships, or tool results. Do not mix in user personalization here.

### Lifecycle and user intent
State:
- selected output profiles
- lifecycle read
- current-date interpretation when dates matter
- response-window status when the target is an RFI, Sources Sought, draft PWS, or market-research notice
- intended BD/capture/proposal use
- personalization applied, if any

### BD and capture implications
Translate the evidence into business implications. Cover whether the target is a live bid, market-research shaping signal, recompete lead, account-entry signal, competitor/partner signal, pricing/vehicle signal, funding signal, or low-priority watch item.

### Selected modules
Include the module headings that match the selected profiles. Use the exact headings from the module library below.

### Consultant scoring
Provide opinionated scoring only when the evidence supports it. Scores should be decision-useful rather than decorative. Good dimensions include attractiveness, fit, urgency, access, shaping leverage, competitive intensity, risk, and confidence.

### Recommended actions
Group actions by time horizon. Use at least two of:
- next 48 hours
- next 30 days
- before bid decision
- before RFQ release
- before recompete shaping
- account plan next step
- no-action/watch trigger

### Risks, unknowns, and evidence gaps
List the important unknowns, what decision they affect, and how to close them. Include data limits, stale records, unresolved incumbent lineage, missing files, unclear acquisition path, unclear eligibility, and weak personalization signals.

### Evidence ledger
End with a table that maps every cited evidence ID to a source, source type, GovTribe ID or URL when available, use in analysis, and confidence note.

## Module library
Use only the modules that materially improve the dossier.

## Live pursuit module
Use for open or future opportunities, forecasts, and active bid targets with a current response or action window.
- Opportunity status, deadline, and actionability.
- Submission, compliance, evaluation, and file-derived requirements.
- Bid/no-bid posture, early win themes, and proposal-team implications.
- Customer access and clarification questions.
- Immediate capture/proposal tasks.

## Market research and RFQ shaping module
Use for RFIs, Sources Sought, Requests for Capabilities, draft PWS notices, and market-research Special Notices, especially when the response deadline has passed and no award or active solicitation supersedes the notice.
- RFI or market-research purpose, notice type, response deadline, and current response status.
- What the government appears to be testing: capability, capacity, socioeconomic strategy, vehicle access, commercial availability, pricing structure, acquisition method, or requirement maturity.
- Acquisition-path unknowns, likely next notice types, and vehicle or set-aside implications.
- Shaping themes and evidence the user should prepare before an RFQ or solicitation appears.
- Response-gap matrix: requested market-research topics versus evidence currently available.
- Likely vendor pool, analog competitors, teaming candidates, and stakeholder implications when evidence supports them.
- Future RFQ watch triggers: amendments, draft releases, forecasts, procurement notices, vehicle activity, incumbent changes, and buyer contacts.
- Recommended next actions framed as pre-RFQ positioning, not late submission activity.

## Recompete planning module
Use for awarded work, expiring awards/IDVs/vehicles, predecessor analysis, and past-due opportunities that have material incumbent or follow-on evidence.
- Incumbent/predecessor read and confidence.
- Award, IDV, vehicle, and transaction lineage.
- Recompete timing hypothesis and watch triggers.
- Buyer pain points or continuity risks implied by history.
- Pre-RFP shaping actions.

## Account and market module
Use for agencies, offices, states, jurisdictions, programs, vehicles, and market-entry views.
- Buyer mission and spend/funding pattern.
- Recurring categories, vehicles, vendors, contacts, and timing.
- Account-entry lanes and near-term opportunities.
- Relationship or access strategy.
- Market attractiveness and concentration.

## Competitor, partner, and stakeholder module
Use for vendors, contacts, incumbents, likely bidders, partners, and customer stakeholders.
- Exact identity or company-scope decision.
- Prime/sub, grant, state/local, and vehicle footprint.
- Strengths, vulnerabilities, teaming posture, and relevance to the user's employer.
- Relationship map and contact strategy.
- Where the target is a competitor, partner, buyer, or influencer.

## Funding and eligibility module
Use for grants, grant programs, grant awards, and funding-oriented opportunities.
- Funding authority, program purpose, eligibility, and applicant fit.
- Award history, recipient landscape, and likely review priorities.
- Cost-share, geography, deadline, and compliance implications.
- Grant pursuit posture and teaming/funding actions.

## Vehicle, IDV, and award module
Use for contract awards, IDVs, vehicles, task-order families, and channel analysis.
- Contract lineage, buyer, holder, ceiling/value, and ordering mechanics.
- Task-order or child-award activity.
- Pricing, labor-rate, SIN, category, or channel implications when supported.
- Recompete, on-ramp, teaming, and access implications.

## State and local market module
Use for state/local opportunities, awards, IDVs, vehicles, states, and jurisdictions.
- Buyer, geography, category, and line-item interpretation.
- File intelligence and local procurement process.
- Vendor/incumbent signals with attribution caution.
- Jurisdiction or statewide market implications.
- State/local action plan and relationship path.

## Personalization and customization rules

Resolve the intended reader and decision before drafting the executive takeaway or visual brief. A company dossier for internal partner selection should emphasize evidenced fit and gaps; a buyer-facing profile should connect supported capabilities to that buyer's mission. Honor the user's audience over either default. Tailor emphasis without hiding relevant uncertainty or presenting conceptual imagery as proof.
Use available user/company context to tailor relevance, not to overwrite facts. When GovTribe AI-injected context is absent, ask only for facts that materially change a gate, score, relevance judgment or recommendation; otherwise continue with public data and state the assumption.

- Custom instructions: follow response-style or role preferences unless they conflict with higher-priority instructions.
- Memories: use stable user facts or preferences to tune emphasis.
- Employer/vendor context: treat as the user's likely company only when available; do not claim it is the bidder unless the user says so.
- GovTribe interests: use inferred federal contract, grant, and state/local interests to prioritize implications.
- Recent views/searches: use as weak intent signals for which modules or examples to emphasize.
- Timezone/current date: use for deadline and lifecycle interpretation.
- Past conversation snippets: use only when directly relevant.
- Label personalization separately, for example: `Personalized inference: based on employer context and recent searches...`

## Evidence and citation layers
Keep these three layers distinct:

1. **Retrieved GovTribe and source-file evidence.** GovTribe tool records, URLs, identifiers, fields, and staged-file passages support the analysis. Preserve enough provenance to build the artifact ledger.
2. **Chat-rendered citations.** When the answer in chat summarizes passages returned by `Search_Vector_Store` or another supported retrieval path, cite the returned source metadata through the external host's native citation format. Use normal tool/source citations for other retrieved records when the host supports them. Do not replace chat citations with document-internal evidence IDs.
3. **Artifact-internal evidence IDs.** In generated Markdown, DOCX, or PDF artifacts, use human-readable IDs such as `SRC-01`, `FILE-01`, `OPP-01`, `AWD-01`, `IDV-01`, `VEH-01`, `VND-01`, `CNT-01`, `GRANT-01`, `NEWS-01`, `USER-01`, `MEM-01`, and `GAP-01`, then resolve every cited ID in the evidence ledger.

Do not expose raw internal source labels, tool tokens, placeholder citation text, connector IDs, or file-search implementation details inside the customer-facing artifact. Do not cite personalized user context as if it were GovTribe source evidence. If evidence conflicts, state the conflict and explain which source is weighted more heavily.

## Document readability rules
- Keep rendered Markdown, Word, and PDF outputs readable in portrait orientation.
- Prefer compact two-to-five-column tables.
- Move long analysis into prose or bullets instead of wide table cells.
- Do not include every raw row in the rendered document. Put exhaustive raw tables in companion CSV or JSON only when needed.
- Keep the first page focused on the decision snapshot, executive takeaway, and the first material implication.
- For DOCX output, use `scripts/deep_dive_markdown_to_docx.py` when available, then validate and visually inspect through the external host's document capability. If rendering is unavailable, deliver the validated Markdown or DOCX plus the Markdown fallback and state that visual QA was not performed.

## Optional company and system illustrations

Use conceptual imagery only when requested or when it explains the dossier's company/system context. Build a self-contained visual brief: intended reader and decision, supported company/system facts, mission context for government-facing material, evidenced fit/gaps for internal capture or partners, established palette/type style, composition, aspect ratio, placement, caption and alt text. Honor explicit audience overrides. Reuse approved customer assets when appropriate. Generate or edit conceptual artwork only through an actually available host image capability; it is not a GovTribe MCP tool. Distinguish proposed concepts from verified assets or past performance; artwork is not a source for factual claims or a substitute for the evidence ledger.

Keep a caption and informative alt text with the selected image. The Markdown-to-DOCX converter supports text/tables, not image embedding: convert the validated dossier text first, then insert figures through the host's document-authoring capability before its final render/QA loop. Do not pass Markdown image syntax through the converter and assume it became a picture. Retain source Markdown, selected image bytes and page/section placement information for rebuilding.

Keep important facts, citations, labels, tables, data marks, scales and precise diagrams editable/deterministic; do not bake important text or quantitative charts into conceptual art. Reuse the image for text-only edits; for a requested image change replace its selected occurrence and compare approved text, layout and unaffected images. Inspect the completed DOCX and any exported PDF at final size and refresh their QA evidence.

Use actual image bytes from an authorized attachment/download or the host's generation result. Vector retrieval is not an image-access path. Preserve original and edited assets, aspect ratio, selected occurrence and placement; inspect the saved asset before insertion. A host-created image has no automatic GovTribe User File ID. If generation is unavailable, reuse an authorized supplied asset, use an appropriate deterministic diagram, or omit optional decoration. Disclose an explicitly requested illustration that could not be created. If the original image or document revision is unavailable, request that exact attachment when needed; do not silently rebuild from extracted text. When final rendering is unavailable, retain the editable source and Markdown fallback and report the unverified visuals separately from structural checks.

## Validation
When execution is available, validate generated Markdown before final delivery:

```bash
python3 scripts/validate_deep_dive_markdown.py path/to/deep-dive.md --target-type federal_contract_opportunity --profile market_research_shaping,competitor_partner_stakeholder --pretty
```

Use `--profile` with one or more comma-separated profiles:
- `live_pursuit`
- `market_research_shaping`
- `recompete_planning`
- `account_market`
- `competitor_partner_stakeholder`
- `funding_eligibility`
- `vehicle_idv_award`
- `state_local_market`
