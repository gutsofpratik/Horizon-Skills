# Pricing Output Quality Checks

Use these checks before delivering pricing workbooks, pricing narratives, rate-support tables, staffing models, or pricing evidence packages.

## Workbook standards
- Use formulas for derived totals, burdens, escalation, option-year rollups, and loaded-rate calculations.
- Avoid hardcoded subtotals unless the user explicitly requests a static exhibit.
- Keep unburdened wage/rate inputs separate from burdened, loaded, or bill-rate outputs.
- Label escalation, fringe, overhead, G&A, fee, and other burden assumptions clearly.
- Include units in headers: hourly rate, annual salary, FTE, hours, quantity, option year, total price, or percentage. State currency, rate year, and period; retain source dates and disclose conversion assumptions.
- Add source notes or comments for wage, GSA Schedule, SCI, line-item, and user-provided assumptions.
- Validate formulas for `#REF!`, `#DIV/0!`, `#VALUE!`, `#N/A`, `#NAME?`, `#NUM!`, and `#NULL!`.
- Use the external host's spreadsheet capability to recalculate and render the final workbook when available. If recalculation, rendering, or visual inspection is unavailable, deliver any validated source workbook as a draft plus a Markdown or CSV model with explicit formulas; state which checks did not run. If workbook authoring itself is unavailable, deliver the model fallback without claiming a workbook was created.

## Narrative standards
- Keep the pricing conclusion scoped to the evidence type. BLS wage data is not a fully burdened bill rate, GSA Schedule rates are ceilings, awarded line items are context-specific, and SCI is a labor-footprint source.
- Distinguish evidence from recommendation. Do not present a price-to-win target as a definitive customer price without explicit assumptions.
- Explain confidence and missing evidence plainly when direct pricing documents, CLINs, labor mix, or incumbent data are absent.
- For one-page pricing narratives, use the external host's document capability to render and inspect PDF or DOCX output when available. If rendering or visual inspection is unavailable, deliver the validated source narrative plus a Markdown fallback and state what was not visually verified.

## Audience and visuals
- Carry the user's intended audience and decision into the narrative and visual brief. Honor explicit overrides; use government mission context for buyer material, internal capture decisions for internal pricing reviews, and the agreed scope for partner material.
- Use deterministic, editable charts, tables, scales, labels, and important text for pricing evidence. Conceptual artwork is optional and requires an actually available host image capability; reuse authorized supplied assets when suitable.
- Keep a self-contained visual brief covering audience, decision, evidence, style, aspect ratio, captions/alt text, and selected occurrence. Preserve source and edited image assets and inspect the final rendered artifact. Image binaries require authorized host image/file access, not vector excerpts; a host-created image does not automatically have a GovTribe User File identity.
- If image generation is unavailable, use an authorized supplied asset or deterministic diagram, or omit optional decoration. Disclose any explicitly requested illustration that could not be made and any unverified rendering without claiming the requested image or document is complete.

## GovCon-specific checks
- Confirm labor categories map to the closest available wage or Schedule evidence and name the proxy limits.
- Check burden/unburdened rate consistency across summary tabs, detail tabs, and narrative text.
- Check base and option year math for escalation, quantity changes, and period-of-performance alignment.
- Keep rate-support citations attached to the assumption or row they support.
- Do not mix federal, state/local, GSA, BLS, or SCI semantics without labeling the source and limitation.

## Delivery note
The final response should explain the pricing artifact and key assumptions in customer language. It should not expose raw validation output. When the host cannot create the requested artifact, deliver the complete Markdown or CSV fallback and explain the unavailable format without dropping the underlying analysis.
