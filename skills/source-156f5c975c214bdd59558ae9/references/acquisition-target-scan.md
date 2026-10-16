---
title: Acquisition Target Scan
description: Build a source-backed vendor universe and prioritized acquisition-target shortlist from a defined strategic thesis.
---

# Acquisition Target Scan

Use this reference when the user is explicitly looking for companies to acquire, invest in, partner with, or evaluate as platform/add-on candidates rather than looking for contract opportunities.

## Goal

Translate an acquisition thesis into a defensible target universe, rank the strongest candidates, and explain why each candidate fits or fails the thesis using observable government-market evidence.

## Minimum input contract

Resolve as many of these as the user provides:

- target capabilities, technologies, or mission areas
- preferred federal agencies, defense programs, SLED buyers, or geographic lanes
- desired company scale or maturity
- prime/subcontracting mix
- contract-vehicle, set-aside, clearance, certification, or customer-access preferences
- recurring-revenue, recompete, concentration, or growth characteristics
- exclusions such as public companies, very large platforms, lifestyle firms, or companies outside the target geography

If the thesis is detailed enough to search, start operating. Do not answer only with a capability disclaimer or ask the user to restate the criteria.

## Workflow

### 1. Convert the thesis into observable screening signals

Separate the user's criteria into:

- hard screens: characteristics that must be present or absent
- ranking signals: characteristics that improve fit
- unknowns: characteristics GovTribe data cannot directly verify

Use observable proxies carefully. For example, award value, customer breadth, vehicle access, recurring task-order activity, subcontract posture, and recent growth signals can inform scale or market position, but they do not prove revenue, profitability, ownership, or willingness to transact.

### 2. Build the vendor universe before selecting favorites

Use exact capability, customer, category, vehicle, geography, award, IDV, subcontract, and state/local evidence to construct a bounded candidate set. Search vendors and their award footprints rather than starting from a guessed list of recognizable companies.

Use opportunities and forecasts only as forward-demand evidence for the market lane. Do not turn the deliverable into an opportunity shortlist when the user asked for acquisition targets.

### 3. Normalize company identity and scope

- Resolve subsidiaries, parents, acquired brands, and similarly named entities before ranking.
- Keep the evaluated legal/entity scope explicit.
- Avoid combining related entities unless the user asks for a consolidated enterprise view.

### 4. Score candidates against the thesis

Use a transparent scorecard with dimensions such as:

- capability and mission fit
- customer and buyer access
- contract-vehicle and channel position
- award durability and recompete exposure
- prime/subcontracting posture
- market concentration and diversification
- observable growth or momentum
- strategic adjacency
- evidence completeness

Do not invent financial metrics. Mark unavailable dimensions as unknown rather than assigning optimistic values.

### 5. Investigate the strongest candidates

For the top candidates, add bounded evidence from awards, IDVs, vehicles, subawards, transactions, state/local activity, forecasts, and recent news when it materially changes the ranking.

Use the `govtribe-deep-dive` companion skill only after the universe and shortlist exist and one candidate warrants a target-specific dossier. If it is unavailable, preserve the shortlist and provide a source-backed dossier brief without expanding this workflow into unsupported private-company diligence.

## Output contract

Return:

1. acquisition thesis and screening interpretation
2. candidate-universe size and coverage notes
3. prioritized shortlist with fit rationale and confidence
4. disqualifiers or material concerns
5. observable evidence supporting each candidate
6. unknowns that require outside diligence
7. recommended next diligence steps

Use a concise table for the shortlist and prose for the most important target narratives.

## Guardrails

- Distinguish government-market fit from transaction attractiveness.
- Do not claim revenue, EBITDA, ownership status, valuation, or sale intent without a source.
- Do not substitute a list of open bids for a company universe.
- Do not over-rank a company merely because it has one large ceiling or one high-value award.
- State when the available evidence is too sparse to support a defensible ranking.
