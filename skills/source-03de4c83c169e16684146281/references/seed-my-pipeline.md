---
title: Seed My Pipeline
description: How to seed an empty or low-signal pipeline with an initial set of opportunities, expiring awards, expiring IDVs or vehicles, and near-term demand candidates.
---

# Seed My Pipeline

Use this reference when the user wants to build the first meaningful candidate set for an empty or low-signal pipeline.

## Goal
- Resolve the target pipeline, set the market focus, derive a usable seed lane from the user's intent, and recommend the first set of pursuit candidates.
- Keep the result recommendation-first. Do not create pursuits unless the user explicitly asks.
- Use [Workspace Pipeline Operations](./workspace-pipeline-operations.md) before turning recommended candidates into pursuits, tasks, saved searches, tags, or other workspace mutations.

## Workflow

### 1. Resolve the target pipeline and stage map
- Resolve the pipeline with `Search_Pipelines`.
- If the pipeline does not resolve because no suitable pipeline exists yet, switch to [Create My Pipeline](./create-my-pipeline.md).
- If the target is still ambiguous after resolution, ask for the minimum clarification and stop. Prefer `Show_Question_Flow` or `Show_Option_List` when the remaining pipeline choice is bounded.
- Load its stages with `Search_Stages` and identify the triage stage or earliest appropriate non-terminal destination stage for new candidates.

### 2. Set the market focus up front
- Resolve whether the user wants federal contract, federal grant, state and local, or a mixed build.
- Ask whether to keep the seed in the current market focus or intentionally widen into an adjacent market surface.
- Prefer `Show_Question_Flow` or `Show_Option_List` for these structured market-surface choices.
- If the user wants cross-surface seeding, choose the nearest plausible surface instead of searching everywhere at once.

### 3. Build the seed lane from user intent
- Use the strongest available starting signals: vendor, buyer, agency, contact, NAICS, PSC, grant program, geography, vehicle, IDV, certifications, set-aside posture, prior pursuits, or a plain-language offering description.
- Resolve structured IDs when the input is specific enough to search directly.
- If the user gives several signals, keep the lane coherent instead of turning the workflow into a broad market scan.
- If the seed lane is still too vague to search well, ask for the minimum missing detail and stop. Prefer `Show_Question_Flow` when several structured seed-lane fields need to be collected together.

### 4. Pull the direct opportunity pass first
- For federal contract or federal grant seeding, lean on [Relevant Opportunities](./relevant-opportunities.md) for the deeper opportunity-retrieval pattern.
- For state and local seeding, apply the same lane-ranking logic on state and local opportunity surfaces instead of forcing a federal search shape.
- Keep the direct pass close to the resolved buyer, work pattern, geography, and timing constraints before widening.

### 5. Add expiring contract and vehicle signals
- Search for expiring or recently expired awards, IDVs, and vehicles that match the resolved lane and could create practical pursuit entries.
- Keep the expiration window near-term enough to support real capture action rather than broad historical research.
- Treat expiring awards and expiring IDVs or vehicles as a separate candidate source from open opportunities.

### 6. Add one near-term demand pass
- Look for near-term demand signals that fit the resolved lane, such as forecasts, recent pre-solicitations, or other credible forward-looking demand evidence on the chosen market surface.
- Keep the near-term demand pass subordinate to the seed lane. Do not let a weak signal source override the core market definition.

### 7. De-duplicate and shape the starter set
- Remove duplicates across opportunities, expiring awards, expiring IDVs or vehicles, and near-term demand candidates.
- Keep only candidates that are meaningfully pursuit-worthy for the resolved lane.
- If the user asked for a mixed build, make the market surface explicit so the starter set does not blur together.

### 8. Rank and stage the surviving candidates
- Rank candidates by direct lane fit, timing practicality, buyer relevance, and evidence strength.
- Label each candidate by source type, such as `open opportunity`, `expiring award`, `expiring IDV/vehicle`, or `near-term signal`.
- Recommend the triage stage or earliest appropriate non-terminal stage as the default destination unless the pipeline structure clearly calls for a different starting point.

## Output contract
- Return a short pipeline summary, a seed-lane summary, a ranked starter set, and confidence.
- For each candidate, include why it fits the lane, the source type, the market surface when relevant, and the recommended destination stage.
- Keep different source types visually clear when more than one appears.
- If the user wants the starter set turned into actual pipeline entries, the candidates can be created later with `Create_Pursuit`.
