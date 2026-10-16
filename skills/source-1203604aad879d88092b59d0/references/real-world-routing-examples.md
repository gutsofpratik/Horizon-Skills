---
title: Real-World Deep Dive Routing Examples
description: Generic routing patterns distilled from customer deep-dive requests, including terse record prompts, capture-focused forecasts, vendor dossiers, recompete orders, chained follow-ups, and negative examples.
---

# Real-World Deep Dive Routing Examples

Use these patterns to recognize when the user wants one resolved record or entity expanded into a decision-ready dossier.

## Route here

### Capture-focused forecast deep dive

Example: "Run a deep dive on this transportation-services forecast and give me scope, timeline, set-aside, value, fit for our company, risks, and next steps."

- Resolve the exact forecast first.
- Expand related opportunities, awards, incumbent or vehicle context, files, contacts, and vendor evidence only as needed.
- Keep the target-specific dossier in Deep Dive.
- Use `govtribe-capture-workflows` for the company-fit, bid/sub/team, past-performance, or partner recommendation when that portion becomes a full capture decision.

### Comprehensive vendor dossier

Example: "Build a vendor deep dive with award history, customers, vehicles, set-aside usage, recent obligations, recompete signals, and capture implications."

- Use the vendor deep-dive reference and bounded multi-surface fan-out.
- Separate exact legal entity scope from parent, subsidiary, affiliate, and similarly named companies.
- Prioritize decision-useful findings over exhaustive row dumps.

### Recompete delivery-order deep dive

Example: "Run a recompete deep dive on this delivery order, including scope, timeline, incumbent, vehicle path, set-aside implications, related notices, and next capture actions."

- Resolve the exact order and parent lineage.
- Trace related opportunity and notice history, transactions, files, incumbent, and vehicle access.
- Preserve the resolved target when follow-ups ask about the user's past performance or position.
- Hand those follow-ups to `govtribe-capture-workflows` without making the user restate the order.

### Delivery-order portfolio and subcontract staffing

Example: "Deep dive this incumbent's delivery orders under an IDV and rank the best subcontract staffing opportunities for our company."

- Use Deep Dive to resolve the vendor, IDV, child orders, scope, value, period, buyer office, and likely labor demand.
- Use `govtribe-pricing-data` for staffing and labor assumptions when evidence supports them.
- Use `govtribe-capture-workflows` to rank company fit, teaming path, and next actions.
- Treat the combined workflow as a normal chain rather than refusing because it crosses domains.

### Terse deep-dive prompt

Example: "Deep dive this record."

If one active GovTribe record resolves cleanly, begin the matching target-specific deep dive. Use the record type, lifecycle, dates, linked records, files, and user intent to choose the output profile. Ask one bounded clarification only when multiple target records remain.

## Context to reuse

- active GovTribe record, URL, ID, or selected result
- user's company, role, capabilities, vehicles, and target market when relevant to implications
- previous target resolution and evidence gathered in the same thread
- requested perspective: capture, account, competitor, partner, pricing, grant, or state/local
- desired depth and artifact format

Personalize implications, not source facts. Do not claim the user's company is the bidder or teammate unless supported.

## Normal handoffs

- Deep Dive to Capture for company fit, past performance, competitors, partners, bid posture, and next pursuit actions
- Deep Dive to Pricing for staffing, FTE, rate, line-item, SCI, or PTW evidence beyond the exact target branch
- Deep Dive to Proposal when the resolved solicitation needs compliance extraction or a response artifact
- Market to Deep Dive when one buyer, vendor, program, vehicle, forecast, or record is selected from a broader scan

## Do not route here

- Simple award-status lookup with no request for context or implications
- Simple vendor/vehicle lookup such as whether a company holds a GSA contract
- One document fact such as a building location or stated FTE count
- Broad market sizing, shortlist discovery, or recurring monitoring without one resolved target
- Product capability or account-help questions
