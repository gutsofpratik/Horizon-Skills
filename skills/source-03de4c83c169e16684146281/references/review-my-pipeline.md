---
title: Review My Pipeline
description: How to review one resolved pipeline for stale pursuits, W/L/A candidates, missing forecast data, and basic pursuit hygiene.
---

# Review My Pipeline

Use this reference when the user wants a cleanup review of one resolved pipeline.

## Goal
- Resolve one pipeline, review active pursuits first, and surface the highest-value cleanup recommendations.
- Keep the result recommendation-first. Do not move stages, mark W/L/A, or fill values unless the user explicitly asks.
- Use [Workspace Pipeline Operations](./workspace-pipeline-operations.md) before applying cleanup recommendations, stage moves, field updates, task creation, or deletes.

## Workflow

### 1. Resolve the target pipeline first
- Resolve the pipeline with `Search_Pipelines`.
- If the user names an owner, stage, or review window, carry those constraints forward.
- If multiple plausible pipelines match, ask for the minimum clarification and stop. Prefer `Show_Option_List` when the remaining choice is a short list of candidate pipelines.

### 2. Load the pipeline stage map
- Use `Search_Stages` for the resolved pipeline.
- Separate terminal stages from active stages, with explicit attention to `Won`, `Lost`, and `Abandoned`.
- Reuse the stage map later when deciding whether a pursuit looks stale, mis-staged, or ready for a W/L/A recommendation.

### 3. Pull the main cleanup worklist from active pursuits
- Use `Search_Pursuits` for the resolved pipeline.
- Default the first pass to non-terminal pursuits by excluding the resolved terminal stage IDs.
- Work from pursuit fields already surfaced in the search response: `name`, `description`, `due_date`, `estimated_award_date`, `estimated_duration`, `estimated_value`, `updated_at`, `owner`, `stage`, `associated_records`, and `contacts`.
- Treat the pursuit as the primary unit of analysis. Use linked records to complete the picture, not as stand-alone outcome signals.
- Use terminal-stage retrieval only if the user explicitly wants a full pipeline audit instead of an active-pipeline cleanup review.

### 4. Run the stale timing pass
- Flag active pursuits whose due date or estimated award date is materially in the past.
- Treat the stale signal as stronger when the pursuit also lacks recent updates, linked current opportunities, or other evidence that it is still live.
- Keep stage context in view. A pursuit in an early active stage with an old due date needs a different recommendation than one sitting near the end of the pipeline.

### 5. Run the terminal-candidate pass
- Review linked records only for pursuits that already look stale, resolved, or mis-staged.
- Form the recommendation from the whole pursuit picture: current stage, timing fields, update recency, description quality, ownership context, and the linked records that appear to represent the pursued work.
- Use linked award, opportunity, forecast, or vehicle context as supporting evidence, not as a stand-alone terminal signal.
- Lower the recommendation to manual review when the linked records are mixed, incidental, or too ambiguous to show whether the pursuit was actually won, lost, canceled, expired, or abandoned.
- Express `Won`, `Lost`, or `Abandoned` only as a recommendation backed by evidence, not as an action.

### 6. Run the forecast-data pass
- Flag active pursuits missing usable `estimated_value`, `due_date`, `estimated_award_date`, or `estimated_duration`.
- Use linked records to recommend fills only when the available evidence is specific enough to support a defensible value, date, or duration suggestion.
- If the linked evidence is too thin, keep the recommendation as "needs manual fill" instead of guessing.

### 7. Run the ownership and hygiene pass
- Flag unclear ownership, weak descriptions, or pursuits whose current stage is not well supported by the available context.
- Treat thin descriptions, no useful linked records, or no clear next step as hygiene issues when they materially weaken pipeline usability.
- Keep this pass practical. Focus on issues that affect forecast quality, pipeline reporting, or next-action clarity.

## Output contract
- Return a short pipeline summary, an active-pipeline readout, a prioritized cleanup queue, and confidence.
- For each pursuit, include the current stage, the issue, the recommended next action, and the evidence behind that recommendation.
- Keep W/L/A recommendations clearly labeled as recommendations.
- If the user wants the cleanup recommendations applied, the same recommendations can be carried forward with `Update_Pursuit`.
