---
name: canva-branded-presentation
description: Create branded marketing and sales presentation decks with Canva AI using the connected Canva app's list_brand_kits and direct generate-design flow. Use when the user asks to generate, create, draft, or build a Canva sales deck, marketing deck, pitch deck, product deck, or other branded slide presentation; always suggest available brand kits and ask the user to choose before generation. Do not use for Canva Docs, reports, proposals, single-page visual designs, templates, prepare-design-generation, or _prepare_design_generation flows.
---

# Canva Presentation Builder

Use the Canva app to generate presentation-type designs with Canva AI, especially branded marketing decks and sales decks. Keep the workflow focused on multi-slide decks even though the generation tool can create many other design types.

## Core Rule

For deck requests, call the Canva app `generate-design` tool directly with `design_type: "presentation"` and presentation-specific content. If the app exposes callable names, this means use `_generate_design`, not `_prepare_design_generation`. Never use `prepare-design-generation`, `_prepare_design_generation`, or outline-review helpers for this skill. Do not use `doc`, `document`, `proposal`, `report`, `infographic`, poster, social post, or other design types. If the user explicitly switches away from presentations, use a different workflow instead of this skill.

The point of this skill is to keep Canva AI generation presentation-shaped when using a broad design-generation tool. Always give `generate-design` enough deck-specific context in its `query` so it does not produce a document-like or single-page result. If direct generation cannot proceed without a prepare-design-generation step, stop and tell the user rather than calling the prepare tool.

## Deck Focus

Optimize the deck for marketing and sales outcomes:

- Audience: buyers, prospects, customers, partners, or internal go-to-market stakeholders.
- Purpose: position the brand or product, communicate value, support a campaign, enable sales, pitch an offer, or drive a next step.
- Content shape: concise messaging, crisp positioning, specific benefits, proof points, and clear calls to action.

Prefer a persuasive commercial narrative over a generic informational outline. Useful arcs include:

- Problem -> insight -> solution -> value -> proof -> next step.
- Market shift -> customer need -> product story -> differentiation -> results -> CTA.
- Audience pain -> desired outcome -> offer -> capabilities -> credibility -> buying path.



## Inputs

Use the user's brief, outline, notes, or pasted content as the source material. If important presentation parameters are missing, infer sensible defaults instead of blocking:

- Audience: infer from the brief, or use a general professional audience.
- Length: infer from the content; for a normal first draft, aim for 8-12 slides.
- Tone: match the user's language; default to clear, polished, and useful.
- Objective: derive the intended commercial outcome, such as generate interest, persuade buyers, pitch a product, enable sales, recap a campaign, or align go-to-market teams.

Ask a concise follow-up only when the missing choice would materially change the deck, such as whether the deck is for executives or customers, or whether the user needs a very specific slide count. Brand kit selection is the exception: always ask the user to choose from available brand kits before generation.

## Brand Kit Handling

For every deck request:

- Call Canva `list_brand_kits` `_list_brand_kits` when using callable names) to find available brand kits.
- Suggest the available brand kits to the user and ask them to choose one before generation.
- Do not auto-select a brand kit, even if only one kit is available or one kit seems obviously relevant.
- Pass the selected kit as `brand_kit_id` when calling `generate-design`.
- If no brand kits are available, say that none were found and ask whether to continue without a brand kit.
- If `list_brand_kits` reports missing `brandkit:read` scopes, ask the user to disconnect and reconnect the Canva app before continuing.
- If the user explicitly chooses to continue without a brand kit, keep the deck brand-aware using the supplied company, product, tone, colors, or messaging, without inventing brand rules.

Do not use Canva template tools in this skill, including `search-brand-templates`, `get-brand-template-dataset`, `autofill-design`, or `create-design-from-brand-template`. If the user asks to use, search, start from, or autofill a template, say this skill only uses brand kits with direct `generate-design` and ask whether they want to continue without templates or switch to a different Canva template workflow.

## Generation Prompt

Write the generation prompt as a deck brief, not as a generic document prompt. Include:

- Working title.
- Audience and objective.
- Desired slide count or range.
- Narrative arc.
- Brand, product, offer, category, and positioning.
- Primary customer pain points and desired outcomes.
- Key value propositions, differentiators, and proof points.
- Slide-by-slide outline with specific slide titles.
- Key bullets or talking points for each slide.
- Visual direction for each slide, such as chart, timeline, comparison table, product screenshot, diagram, or image subject.
- Speaker-note guidance when useful.
- Any brand, tone, or formatting constraints the user supplied.

Prefer concrete, outcome-oriented slide titles over vague section labels. Make slides scannable and visual; avoid dense prose, article-like sections, or report-style page structure.

For a sales deck, include the likely buyer problem, solution fit, benefits, credibility, objection-aware proof, and next step. For a marketing deck, include campaign or brand context, target audience, message hierarchy, offer, channels or use cases when relevant, and a memorable CTA.

## Candidate Finalization

If Canva AI returns design candidates, present the candidates to the user and ask which one they want to turn into an editable design. After selection, use Canva's create-from-candidate flow and return the final Canva design link.

## Boundaries

Use this skill only for creating new Canva AI presentation drafts through `list_brand_kits`, direct `generate-design`, and create-from-candidate. For editing an existing Canva design, implementing reviewer feedback, translating, resizing, brand-checking, prepare-design-generation, or template-based generation, use the more specific Canva skill or app workflow for that task.