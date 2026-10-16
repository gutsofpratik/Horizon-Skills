---
title: GAO Bid Protest Evidence
description: How to use GAO bid protest records as bounded capture-risk and protest-history evidence.
---

# GAO Bid Protest Evidence

Use this reference alongside bid / no-bid, black hat, incumbent, or likely-bidder workflows when protest history, agency protest outcomes, procurement identifiers, or protester behavior could materially change the capture-risk read.

## Goal
- Use `Search_GAO_Bid_Protests` to recover exact protest dockets, decisions, outcomes, and decision text tied to a procurement, agency, or protester.
- Treat protest records as legal and procedural history, not as proof that a vendor will bid, protest, win, or lose.
- Keep protest evidence subordinate to the main capture workflow unless it directly changes risk, counterstrategy, or confidence.

## Workflow

### 1. Start from exact anchors
- Prefer exact `federal_meta_opportunity_id` or procurement identifiers from the target opportunity, award, IDV, vehicle, file, or user input.
- Use exact GAO file numbers when the user provides them.
- Use `federal_agency_ids` when the question is about buyer protest history or outcomes.
- Use exact `protesters` only after resolving the protester name from the target context or user input.
- If the anchor is weak, do not widen into protest history just to add color.

### 2. Choose the protest search path
- Exact procurement path: call `Search_GAO_Bid_Protests` with `federal_meta_opportunity_ids` or `procurement_identifiers`.
- Protester path: call it with `protesters` plus a bounded date range or agency filter when possible.
- Agency-history path: use `federal_agency_ids`, `decision_date_range` or `filed_date_range`, and aggregations such as `top_outcomes_by_doc_count`, `top_statuses_by_doc_count`, `top_protesters_by_doc_count`, and `top_procurement_identifiers_by_doc_count`.
- Decision-text path: use `query` with keyword mode for exact phrases and identifiers, or semantic mode for concept-heavy decision-text research.
- Use the bundled [search-mode guide](./govtribe-docs-choose-a-search-mode-and-write-queries.md) for stable query guidance and call `Documentation` for the current tool schema, filters, and response fields before constructing non-trivial calls.

### 3. Request useful fields
- For row retrieval, request at least `govtribe_id`, `file_number`, `protester`, `case_type`, `status`, `outcome`, `filed_date`, `decision_date`, `available_date`, `highlights`, `decision_text`, `pdf_url`, `source_links`, `procurement_identifiers`, `federal_agency`, and `federal_meta_opportunity_id`.
- Add `federal_meta_opportunity` when the procurement-thread display context matters.
- Use `per_page: 0` when the task only needs protest-history aggregations.

### 4. Interpret conservatively
- Separate open dockets from decided protests. Open status is a timing and uncertainty signal, not an outcome.
- Interpret `outcome` as the GAO protest outcome for that record, not as a blanket judgment on the agency, protester, incumbent, or requirement.
- Prioritize exact procurement-linked protests over broad agency or protester history.
- Treat older decisions as context unless the same buyer, requirement family, legal issue, or procurement identifier makes them current.
- Do not provide legal advice. Frame findings as capture risk, procedural history, and evidence gaps.

## Output contract
- Add a short protest-history note only when the evidence changes the main workflow.
- Include file numbers, dates, outcomes, and the exact anchor used.
- State whether the evidence came from exact procurement linkage, agency history, protester history, or decision-text research.
- Carry caveats into the final risk or confidence section instead of presenting protest evidence as a standalone conclusion.
