---
title: Workspace Pipeline Operations
description: How to apply explicit user requests to create, update, or delete workspace pipeline objects while preserving user control around risky actions.
---

# Workspace Pipeline Operations

Use this reference when the user clearly asks GovTribe AI to mutate workspace capture objects, such as creating a pipeline, adding pursuits, moving stages, creating tasks, saving a search, or cleaning up pipeline records.

## Goal
- Resolve the workspace objects and public records that will be changed.
- Recommend first unless the user clearly requested a create, update, or delete action.
- Apply only supported and well-scoped changes, then summarize exactly what changed and what still needs review.

## Workspace scope
- Supported workspace objects include pipelines, pursuits, stages, tasks, saved searches, and tags.
- Use custom fields only when the active tool schema or GovTribe Docs exposes the relevant custom-field inputs for the object being changed.
- Do not invent unavailable tool fields, hidden workspace metadata, or unsupported tag/custom-field behavior.

## Permission boundaries
- Recommendation-first default: when the user asks for analysis, review, prioritization, cleanup ideas, or a suggested pipeline, return proposed actions without mutating records.
- Clear-action default: when the user says to create, add, save, update, move, rename, assign, or create tasks, treat that as permission to perform the requested reversible action after resolving the target objects.
- Explicit confirmation required: ask before destructive deletes, bulk updates, overwrites, ambiguous pipeline or stage selection, moving pursuits into terminal stages, changing W/L/A status, changing reporting-impacting stage/status fields, or applying a cleanup plan that affects more records than the user named.
- If the remaining choice is bounded, prefer `Show_Option_List`, `Show_Question_Flow`, or `Show_Preferences_Panel` over a free-text question. Use `Interaction_State` when a submitted app payload needs to be read or carried into the tool calls.

## Resolution before mutation
- Use the logged-in user's workspace context supplied by the active tools. Do not ask the user to choose among workspaces or accept a user-supplied workspace ID.
- Resolve the target pipeline with `Search_Pipelines`; if several match, ask the user to choose.
- Resolve the stage map with `Search_Stages` before creating pursuits, moving pursuits, or creating stages.
- Resolve pursuit targets before creation. Prefer exact public-record IDs and linked-item creation when a candidate comes from a GovTribe opportunity, award, forecast, vehicle, grant, or state/local record.
- Resolve owners with `Search_Users` when the user names a person, role, or email. Do not assign ownership from a guessed name.
- Resolve saved searches with `Search_Saved_Searches` before creating or updating one, and require a current search persistence ID before calling `Create_Saved_Search`.
- Search existing pursuits before adding candidates so duplicates are skipped or presented for confirmation.
- Search existing tags with `Search_Tags` before creating tags or applying tag IDs.

## Allowed reversible actions
- Create a pipeline shell with `Create_Pipeline` after name, description, owner context, and `stageCount` are resolved.
- Shape stages with `Search_Stages`, `Update_Stage`, and `Create_Stage` when the user asked for a named stage map or agreed to one.
- Create pursuits with `Create_Pursuit` when each target has a resolved destination stage and either a linked item or a clear pursuit name.
- Update non-reporting pursuit fields with `Update_Pursuit` when the user asked for those edits and the target pursuit is resolved.
- Create tasks with `Create_Task` when the title, associated pipeline or pursuit, owner when needed, priority, and due date are resolved well enough for the tool schema.
- Create saved searches with `Create_Saved_Search` when a search persistence ID, name, scope, and notification preference are resolved.
- Create or update tags with `Create_Tag` or `Update_Tag` only when tag behavior is exposed in the active toolset and the intended tag is resolved.

## High-risk actions
- Do not call `Delete_Pipeline`, `Delete_Pursuit`, `Delete_Stage`, `Delete_Task`, `Delete_Saved_Search`, or `Delete_Tag` without explicit user confirmation naming the object or confirming a proposed delete list.
- Do not bulk move pursuits, reorder stages, rewrite stage maps, or apply cleanup recommendations without first summarizing the proposed mutation list and asking for approval.
- Do not move pursuits to `Won`, `Lost`, or `Abandoned` unless the user explicitly confirms that reporting-impacting change after seeing the evidence.
- Do not overwrite saved-search criteria, notification settings, tags, owners, descriptions, or task details when the current value is ambiguous or user-owned context may be lost.

## Workflow

### 1. Classify intent
- If the user asks what should change, run the relevant recommendation workflow and stop with proposed actions.
- If the user asks to apply changes, continue with object resolution and tool calls.
- If the request mixes recommendation and mutation, present a short proposed mutation list first when risk is material.

### 2. Resolve all targets
- Load the pipeline, stages, pursuits, saved searches, tags, owners, and public records needed for the requested action.
- Stop and ask a bounded clarification when a required target is missing, ambiguous, or not visible to the logged-in user.
- If permission or plan limits block an action, report the blocked item and continue only with independent safe items.

### 3. Prepare the mutation list
- Summarize the object, action, destination, owner, due date, linked record, saved-search cadence, tag, or field value that will change.
- Ask for confirmation only for the high-risk cases above or when the proposed list materially exceeds what the user named.
- Keep unchanged recommendations separate from actions that will be applied.

### 4. Apply changes
- Call the narrowest tool that performs the requested action.
- Apply creates before dependent updates, such as creating a pipeline before creating its stages and pursuits.
- Preserve stable IDs from tool responses so follow-on calls target the created or updated records.
- If a duplicate pursuit or saved search is found, skip it unless the user explicitly wants a duplicate.

### 5. Report outcome
- Return a post-action summary with created, updated, skipped, failed, and needs-confirmation sections as applicable.
- Include the target pipeline, stage, owner, linked record, due date, saved-search cadence, or tag when it helps the user verify the result.
- For partial success, state exactly which records changed and which did not, then recommend the next safe action.

## Error handling
- Unavailable object ID: stop for that item, say it is not visible to the logged-in user, and ask for the correct object if needed.
- Missing permission or plan limit: report the blocked operation and do not retry with another object.
- Duplicate pursuit or saved search: skip by default and identify the existing record.
- Ambiguous pipeline, stage, owner, or saved search: ask with `Show_Option_List` or `Show_Question_Flow`.
- Missing stage definitions: create or rename stages only after the stage map is confirmed or clearly requested.
- Partial success: continue only with independent safe actions, then list completed and incomplete operations separately.

## Output contracts

### Pre-action recommendation
- Summarize the proposed changes in a compact list or table.
- Label actions that need confirmation.
- Include the exact question or option set needed to proceed.

### Post-action summary
- Start with the count and type of records created, updated, skipped, or blocked.
- List each changed record with the action taken and important destination fields.
- End with the next step only when additional user input or confirmation is needed.
