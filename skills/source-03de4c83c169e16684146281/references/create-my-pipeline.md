---
title: Create My Pipeline
description: How to create a new pipeline shell when no suitable pipeline exists yet, then shape it for the intended market and capture process.
---

# Create My Pipeline

Use this reference when the user has no suitable pipeline yet and wants a new one created.

## Goal
- Decide whether a new pipeline is actually needed, resolve the intended market focus and process depth, and create a usable pipeline shell when the user explicitly wants it created.
- Keep the workflow recommendation-first until the user confirms they want the new pipeline created.
- Use [Workspace Pipeline Operations](./workspace-pipeline-operations.md) before applying creates, stage updates, or other workspace mutations.

## Workflow

### 1. Confirm that a new pipeline is needed
- Use `Search_Pipelines` to check whether the user already has a pipeline that matches the intended market, buyer, or process.
- If an existing pipeline already fits, switch to [Seed My Pipeline](./seed-my-pipeline.md), [Review My Pipeline](./review-my-pipeline.md), or [Expand My Pipeline](./expand-my-pipeline.md) instead of creating a duplicate.
- If the user still wants a separate net-new pipeline, continue.

### 2. Set the market focus up front
- Resolve whether the new pipeline is for federal contract, federal grant, state and local, or a mixed market.
- Decide whether cross-surface work should live in this same pipeline or in a separate pipeline.
- When these are still open structured choices, prefer `Show_Question_Flow` or `Show_Option_List` to collect them instead of a free-text back-and-forth.
- Keep the market focus explicit so the stage design and later seeding workflow stay coherent.

### 3. Choose the pipeline shape
- Resolve the pipeline name and one-sentence description first.
- Choose the smallest `stageCount` that fits the intended process:
  - `3-4` stages for light tracking and simple bid organization
  - `5-7` stages for qualification, response development, and submitted-work separation
  - `8+` stages only when the user wants a highly managed capture or proposal-development process
- Prefer `Show_Preferences_Panel` when the user needs to review or submit the pipeline name, market focus, cross-surface choice, and `stageCount` together.
- Remember that `Create_Pipeline` creates a shell with numbered user stages. Plan any follow-on renaming or extra stages explicitly instead of assuming a richer template will appear automatically.

### 4. Create the pipeline shell only when asked
- If the user explicitly wants the pipeline created now, call `Create_Pipeline` with the resolved `name`, optional `description`, and `stageCount`.
- When the only missing decision is `create now` versus `planning only`, prefer `Show_Option_List` instead of a free-text confirmation.
- If the user is only planning setup, return the proposed pipeline configuration and stop.

### 5. Shape the stage map after creation when needed
- Use `Search_Stages` for the newly created pipeline.
- Use `Update_Stage` to rename or describe the numbered stages into practical capture lanes.
- Use `Create_Stage` only when the user needs additional stages beyond the initial `stageCount`.
- If `Show_Preferences_Panel` was used to collect configuration, use `Interaction_State` to read or persist the submitted pipeline-shape choices before applying them.
- Keep at least one early non-terminal stage suitable for seeding new pursuits.

### 6. Hand off to seeding when the shell is ready
- If the user wants the first set of opportunities, expiring awards, expiring IDVs or vehicles, or near-term demand candidates next, switch to [Seed My Pipeline](./seed-my-pipeline.md).

## Output contract
- Return a short setup summary, the proposed or created pipeline configuration, any recommended stage-map shaping, and the next step.
- If the pipeline is created, include the created pipeline and whether further stage shaping is still needed.
- Keep the recommendation to create or not create a new pipeline explicit when a similar existing pipeline was found.
