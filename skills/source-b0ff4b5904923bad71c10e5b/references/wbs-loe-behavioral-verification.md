# WBS/LOE models and controlled revisions

Start with a task contract and an independent source inventory. Identify the requested delivery state and the person responsible for unresolved assumptions. Use the host's spreadsheet capability for modeling, recalculation, and rendering when available. Before building, declare the authoritative inputs, selected revision, required sheets and output ranges, allowed changes, expected behavior, and acceptance checks. Use `govtribe-document-editing` for controlled revisions and `govtribe-file-templates` for an approved master, each from its own installed root. Preserve buyer-required forms and user-selected revisions.

## Cost chain

Map each WBS and labor category through volume → productivity → hours → rates → direct costs → escalation/reserve → summary → CLINs. Retain units (participants, sessions/participant, sessions/hour, dollars/hour), source date, rate basis, period, and assumption owner. Separate compensation from labor and distinguish fixed, variable, and conditional fees. Apply escalation to its declared cost basis once. Label reserves rather than burying them in rates. Reconcile every rollup independently; a workbook's own `OK` label is not independent evidence.

For synthetic ORBIT: 10 participants × 2 sessions ÷ 4 sessions/hour = 5 hours; labor $500, compensation $200; 10% escalation on those costs plus a conditional $50 fee yields $820. Raising labor rate to $120 changes total by $110. Raising compensation to $30 changes it by $110. Zero participants produces zero hours, dependent compensation, and conditional fee. A genuinely unconditional fixed charge may remain only when the task declares it.

## Behavioral gate

Declare independent scratch-copy scenarios for every material class: volume, productivity, rates, compensation, fees, escalation. Include zero volume and a deliberate broken CLIN reconciliation. State expected values/deltas and absolute/relative tolerances before running the host-supported calculation or test routine. Use source math as the oracle; never copy expected values from the current workbook caches or self-reported status. Run print preparation, then recalculate the final XLSX, then render and validate that exact file. Confirm formula caches exist in the delivered binary.

## Revision gate

Keep the prior deliverable immutable. For a rate-only revision, declare the specific editable rate cells; compare complete formula maps, input validation, sheets, approved columns and required output ranges. Changing an upstream volume/productivity formula is a failure even if current totals happen to match. Preserve supplied formulas and table identity. If a business-logic correction is necessary, disclose it and revise the allowed contract before changing it. Recalculate, rerun sensitivities, reconcile, and issue a new hash-bound receipt after every binary change.

Distinguish operational data tabs from print-focused summaries. Wide operational exports may span pages; never shrink a useful table into unreadable text merely to satisfy one-page width. For print sheets, ensure required populated ranges are in the print area, continuation headers remain visible, and rendered type stays readable.

## Delivery state and unavailable host capabilities

Keep an independent inventory of source files, versions, source locations, units, assumptions, and owners. Report source coverage separately from file structure. A valid XLSX structure or a workbook's own status cell does not prove the model behaves correctly.

Use the host's authorized file access for the exact input and output binary. Operate only in host-supplied input and output locations and preserve the prior deliverable. If the host can create a workbook but cannot recalculate, render, or inspect it, deliver the source workbook as a draft plus a Markdown or CSV model with explicit formulas; identify missing cache, behavioral, or visual checks. If no workbook authoring capability exists, provide that model fallback without claiming an XLSX was created. Never install dependencies or claim a check ran when it did not.

Report the declared delivery state, checks actually run, expected and observed results, tolerances, independent reconciliation, and unresolved assumptions or checks. Record the delivered file's hash when binary access permits so the verification is tied to that exact revision; otherwise state that binary identity was not verified. Only claim the requested readiness when its required checks pass. A changed binary requires recalculation, sensitivities, reconciliation, rendering checks, and a new hash-bound verification record; unavailable checks remain explicit limitations.
