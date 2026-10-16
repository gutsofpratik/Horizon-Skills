---
title: Expand My Pipeline
description: How to expand one resolved pipeline with missed same-lane opportunities first and adjacent adds second.
---

# Expand My Pipeline

Use this reference when the user wants to grow one resolved pipeline with net-new pursuit candidates.

## Goal
- Resolve one pipeline, infer its current lane and market focus from active pursuits, and recommend net-new adds that fit the pipeline.
- Run the same-lane, same-surface pass first. Widen into adjacent buyers, work dimensions, or market surfaces only after the direct pass.
- Use [Workspace Pipeline Operations](./workspace-pipeline-operations.md) before turning recommended adds into pursuits, tasks, saved searches, tags, or other workspace mutations.

## Workflow

### 1. Resolve the target pipeline and active stage map
- Resolve the pipeline with `Search_Pipelines`.
- Load its stages with `Search_Stages` and identify the triage stage or earliest appropriate non-terminal destination stage for new adds.
- If the pipeline does not resolve cleanly enough to search, ask for the minimum clarification and stop. Prefer `Show_Question_Flow` or `Show_Option_List` when the remaining pipeline choice is bounded.

### 2. Pull the active-pursuit baseline
- Use `Search_Pursuits` for the resolved pipeline.
- Default to non-terminal pursuits so the baseline reflects the pipeline's live lane rather than historical residue.
- Reuse surfaced pursuit fields and linked records before broadening into larger market search.
- If the pipeline has too few meaningful active pursuits to infer a lane or market focus, switch to [Seed My Pipeline](./seed-my-pipeline.md).

### 3. Set the market focus before broad retrieval
- Infer whether the pipeline is primarily federal contract, federal grant, state and local, or mixed from repeated evidence in active pursuits and their linked records.
- If the user wants to keep the pipeline in its current market, stay on the dominant surface for the first pass.
- If the user explicitly wants expansion beyond the current market, add one adjacent-surface pass only after the direct pass.
- When cross-surface expansion is allowed, choose the nearest plausible surface instead of widening everywhere at once. A traditionally state and local lane may justify a federal contract or federal grant pass, and a federal lane may justify a state and local pass when the work pattern travels well.
- If the pipeline is mixed or the user intent is unclear, ask whether to keep the current market focus or expand it before broad search. Prefer `Show_Option_List` when the choice is simply `stay current` versus `expand`.

### 4. Infer the current lane from repeated signals
- Derive the dominant buyer and work-pattern signals from repeated evidence across active pursuits and their linked records.
- Reuse buyers such as agencies or contacts, plus work dimensions such as NAICS, PSC, vehicle, IDV, geography, and set-aside posture.
- Do not overfit the lane from one noisy pursuit.
- If the pipeline is clearly heterogeneous, either cluster it into a small number of lanes or ask the user to narrow the scope before broad market retrieval. Prefer `Show_Question_Flow` when a small number of narrowing choices can be collected cleanly.

### 5. Run the same-lane expansion pass first
- Use the resolved lane to find missed opportunities that fit the pipeline's dominant buyer and work patterns on the current market surface.
- Lean on [Relevant Opportunities](./relevant-opportunities.md) for deeper federal contract or federal grant open-market retrieval patterns instead of re-documenting them here.
- For state and local pipelines, apply the same lane-ranking logic on state and local opportunity surfaces instead of forcing a federal search shape.
- Reuse [Federal Buyer Expansion Plan](./federal-buyer-expansion-plan.md) only for buyer-centered federal contract lanes where a one-office federal pattern is actually the right lens.
- Keep the first pass close to the current lane and current market before widening.

### 6. Run the adjacent pass second
- Widen one step outward only after the same-lane, same-surface pass.
- Prefer adjacent buyers, adjacent work dimensions, closely related vehicles, or one adjacent market surface over a broad market scan.
- Use [Past Performance Match](./past-performance-match.md) only when the user frames expansion around a specific vendor capability or past-performance profile.
- Lower confidence when the case for adjacency depends on weak overlap or sparse historical evidence.

### 7. De-duplicate against the current pipeline
- Remove candidates already represented by existing pursuits or obvious duplicates of active work already in the pipeline.
- Keep only genuinely net-new adds.
- If a candidate overlaps an existing pursuit but still suggests a better adjacent angle, explain that distinction explicitly instead of listing it as a new add.

### 8. Rank and stage the surviving adds
- Rank candidates by direct fit to the current lane, timing practicality, buyer relevance, and evidence strength.
- Label each candidate as `core lane` or `adjacent lane`.
- Make the market surface explicit when the add comes from a different surface than the current pipeline.
- Recommend the triage stage or earliest appropriate non-terminal stage as the default destination unless the pipeline structure clearly calls for a different starting point.

## Output contract
- Return a short pipeline summary, a current-lane summary, a ranked add list, and confidence.
- For each candidate, include why it fits the pipeline, why it is net-new, whether it is `core lane` or `adjacent lane`, its market surface when relevant, and the recommended destination stage.
- Keep same-lane and adjacent recommendations visually separate if both appear.
- If the user wants the ranked add list turned into actual pipeline entries, the candidates can be created later with `Create_Pursuit`.
