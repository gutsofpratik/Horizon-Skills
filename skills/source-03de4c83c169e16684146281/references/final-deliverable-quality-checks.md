# Final Capture Deliverable Quality Checks

Use these checks before delivering capture artifacts such as acquisition briefs, market research white papers, bidder lists, subcontractor/contact research, gap analyses, PTW briefs, pipeline summaries, and pursuit memos.

## Evidence and recommendation separation
- Separate retrieved evidence from interpretation and recommendation.
- Label low-confidence assumptions, missing source documents, weak incumbent lineage, and thin comparable sets.
- Keep direct evidence near the recommendation it supports.
- Do not overstate a vendor's fit, buyer intent, likely bidders, or price posture when evidence is only directional.

## Executive-ready format
- Confirm the intended reader and decision before polishing. Internal capture briefs support contractor pursuit decisions with candid risks and economics; partner material explains complementary roles and a supported teaming case. Keep internal competitive assessments out of partner/buyer-facing copy unless explicitly intended for that audience; preserve relevant caveats. A government-facing request takes precedence over the internal default.
- Open document-style outputs with the decision, ranking, or action the customer can use.
- Use narrow tables for rendered briefs. Move full evidence universes, raw scorecards, long contact lists, and normalization details to CSV/XLSX/JSON companions.
- Prefer XLSX over raw CSV for customer-facing contact, subcontractor, or comparable lists when formatting, source notes, filtering, or multiple tabs improve usability.
- Keep charts and visuals labeled, readable, and tied to the story. Prefer `Show_Chart` for supported inline charts; otherwise use a provider-neutral host chart capability or a labeled Markdown table with CSV/JSON companion data.
- Remove placeholders, internal paths, debug text, model/tool identifiers, and raw prompt or tool dumps.

## Deliverable-specific checks
- Acquisition briefs and market white papers should have clear scope, key takeaways, evidence tables, implications, and next actions.
- Subcontractor and contact lists should include source basis, role fit, relevant past work or buyer connection, and outreach caveats.
- Gap analyses should distinguish missing evidence from actual capability gaps.
- Bid/no-bid, black-hat, and likely-bidder briefs should avoid raw scoring dumps in the rendered memo.
- PTW outputs should carry pricing confidence and missing-price-document caveats.

## Selective mission and context imagery

- Use conceptual illustrations only when requested or when they make the pursuit easier to understand. Write a self-contained visual brief: intended reader, actual mission, decision to support, medium, aspect ratio, placement, important labels, source assets, caption/alt text and reuse constraints. Use the external host's image capability only when actually available; it is not a GovTribe MCP tool.
- Brief any illustration with the intended reader, actual mission context and pursuit/teaming decision. Use relevant operational imagery rather than generic government symbolism.
- Preserve the recommendation-first layout and existing customer theme. Keep rankings, evidence, owner/action tables and measured comparisons native/deterministic; decoration must not displace decision content.
- Label conceptual mission depictions when readers could mistake them for installed capability, a verified configuration or actual past performance. Do not invent company/customer logos or infer endorsement.
- Obtain image binaries and exact document revisions through the host's authorized attachment/download workflow or ordinary file/shell access to a caller-supplied original, never through vector retrieval as a substitute. Preserve both source and edited assets, aspect ratio, crop and the selected occurrence. A generated image has no GovTribe file identity unless separately persisted and verified.
- Embed through the host's format authoring capability, add useful captions/alt text, and inspect at final size. Reuse approved images for text-only revisions and compare unaffected content after selected-image edits.
- If image generation is unavailable, reuse an authorized supplied asset, use an appropriate editable diagram, or omit optional decoration. Identify an explicitly requested illustration that could not be made; deliver useful editable content and state any unverified rendering. Do not claim the requested image or document is complete merely because a fallback exists.

## File-specific QA
- Use the external host's rendering and visual-inspection capability for PDF, Word, presentation and spreadsheet outputs. Use the bundled `govtribe-file-templates` and `govtribe-document-editing` workflows from their own installed skill roots when selecting a template or editing an existing file.
- Preserve source templates, source identity, links, headings, table widths, repeated headers, page flow, formulas and workbook checks. Render the exact final file and inspect every page or sheet, including continuation pages.
- When rendering or visual inspection is unavailable, deliver the validated source artifact plus a Markdown or CSV fallback and state exactly what was not visually verified. If format authoring or an optional Office dependency is unavailable, retain the validated Markdown/CSV result and identify the unproduced format; never install dependencies.
- Declare delivery state and report checks actually executed, remaining source gaps and unfinished work separately from structural validity.

## Delivery note
The final response should describe the customer-facing artifact, confidence, and next action. It should not expose internal QA mechanics.
