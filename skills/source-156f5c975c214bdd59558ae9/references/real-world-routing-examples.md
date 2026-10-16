---
title: Real-World Market Intelligence Routing Examples
description: Generic routing patterns distilled from customer market-intelligence requests, including terse prompts, mixed-market scans, lifecycle forecasts, and negative examples.
---

# Real-World Market Intelligence Routing Examples

Use these examples to recognize customer intent. They are generic patterns, not canned answers.

## Route here

### Procurement volume and timing

Example: "What is the dollar volume of this office or program over the next 24 to 36 months, and when are they expected to spend the most?"

- Treat this as a lifecycle and procurement forecast, not an opportunity search.
- Combine historical awards with forecasts, opportunity timing, vehicle or IDV context, and clearly labeled assumptions.
- Return a range, timing windows, peak-spend hypothesis, evidence, and confidence.
- For "do the same for another program," preserve the prior method and comparison frame.

### Terse buyer or account analysis

Example: "Analyze this county fire department."

- Recover the buyer or jurisdiction from the active record or phrase.
- Unless the user narrows the intent, produce a compact account view: buying patterns, active or recent demand, likely categories, incumbent/vendor signals, watch items, and a suggested monitoring lane.
- State which interpretation was used rather than asking an open-ended question when a useful default is available.

### Mixed federal and state/local market scan

Example: "Create a prioritized shortlist of federal and state/local opportunities aligned to our Data and AI capabilities."

- Use Market Intelligence to define the market slice and discover the candidate universe across requested surfaces.
- When the companion skill is available, hand the resolved candidate set to `govtribe-capture-workflows` for company-fit ranking and pursuit posture. Otherwise return the resolved market candidate set plus explicit qualification inputs and limits.
- Do not treat the cross-skill progression as a routing error.

### Acquisition target universe

Example: "I am not looking for contract opportunities; I am looking for acquisition targets in this government market."

- Use [Acquisition Target Scan](./acquisition-target-scan.md).
- Build and rank a vendor universe from public government-market evidence rather than abandoning the task because private financial data is unavailable.

## Context to reuse

- user's company, capabilities, target buyers, and preferred markets when already available
- federal versus state/local scope
- active saved search, pipeline, buyer, program, vehicle, or prior market slice
- prior comparison period and methodology in follow-ups
- requested decision horizon, such as 30/60/90 days or 24 to 36 months

Do not invent company facts or silently broaden federal-only scope into state/local scope.

## Normal handoffs

- Market shortlist to Capture for opportunity ranking or bid posture
- Market signal to Deep Dive for one buyer, vendor, program, vehicle, or record
- Market recompete set to Pricing for rate or staffing evidence
- Market monitor change to Proposal when an amendment or source-package update requires proposal action

## Do not route here

- "Has this solicitation been awarded?" Use direct award-status lookup unless pursuit implications are requested.
- "Does this company have a GSA/FSS contract?" Use vendor or vehicle lookup unless a broader market profile is requested.
- "Find one fact in this document." Use file-content retrieval.
- "Can GovTribe connect to GSA eBuy?" Use GovTribe product documentation and capability guidance.
