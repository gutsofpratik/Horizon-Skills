# Adapt a GovTribe template

Use this workflow when the user selects a template and asks to adapt it to the conversation, a GovTribe record or a company. Combine the template's design with the relevant domain workflow and the host's authoring capability for the source format. Resolve `govtribe-file-templates` from its own installed root to select and verify bundled masters, examples and provenance; use `govtribe-govcon-writing` from its own installed root when narrative work warrants it. Use their prepared portable asset hashes and sizes, retaining canonical provenance separately; sanitized assets need not have their original binary hash.

## Resolve the handoff

- Recover the latest user request, selected template, existing draft, authorized record context, attached source documents and relevant company information before asking for more input. Explicit user corrections take precedence over earlier conversational assumptions.
- Identify the editable **blank master** and the **populated example reference** separately. Use the selected master and its supplied version/identity as the source. The example demonstrates layout and intended depth; it may contain another company's factual profile, researched government facts, or illustrative scenario data. None establishes facts about the current subject.
- Work from native DOCX, XLSX or PPTX bytes. A preview image does not supply an editable master. If the selected master cannot be retrieved or verified, resolve that missing source; do not silently substitute the example or a generic template. Preserve the pinned master/example and any supplied template provenance.
- A record-launched request already supplies the starting target when its structured identity resolves. Inspect the actual record and relevant source documents rather than relying on its title. A Files request that explicitly asks for intake still needs the user's intended use; do not invent a target from the example.
- A single opportunity or award is only initial context for a comparison, tracker or multi-record template. Resolve the intended scope from the conversation and request only material missing inputs. Keep a source-bounded draft when useful; do not fill out an apparent dataset with invented records.

## Establish subjects and evidence

Distinguish the government buyer, target opportunity/award, award recipient, user's company and any teammate. For a Company Profile about an awardee, the awardee remains the profile subject. For a fit assessment, evaluate the company or team the user actually named. A record's vendor is not automatically the user's company.

Reuse the user's stated company and available authorized profile or company files. Search prior files only when the current context is insufficient and the relevant domain skill's prior-file workflow applies. Preserve accepted user language; refresh time-sensitive government facts before presenting them as current.

Build a compact field/section map before population: intended content, supporting source or supplied company statement, and any unresolved input. Ground government requirements and deadlines in controlling notices, amendments and source documents. Keep company-provided claims distinct from independently supported facts. Route domain judgments through the relevant available skill:

| Requested substance | Owning workflow |
| --- | --- |
| Factual opportunity, company or program brief | `govtribe-deep-dive` |
| Company fit, bid/no-bid, teaming or capture decision | `govtribe-capture-workflows` |
| Award transactions, spend or market evidence | `govtribe-market-intelligence` |
| Labor, staffing or pricing model | `govtribe-pricing-data` |
| Proposal response, compliance or past-performance narrative | `govtribe-proposal-workflows` |

A factual Opportunity Brief can proceed without company information. Do not add company intake, a fit score or a bid decision unless the requested deliverable needs it. An award does not by itself prove performed scope, customer acceptance, the user's past performance or company revenue; follow the owning workflow's evidence rules.

## Populate and preserve

- Retain the selected template's sections, editable objects, tables, formulas, chart data and visual design. Follow bounded template-specific guidance available in the authorized handoff. Use the example to judge depth and presentation, not to copy scenario values or substantive claims.
- Tailor narrative and relevant fields to the actual reader, record and company. Do not carry example capabilities, certifications, personnel, pricing, dates, contacts or past performance into customer claims. Mark missing evidence or necessary inputs clearly; ask when a consequential choice prevents useful completion.
- Library masters use a title page with separate first-page and default headers and footers, and their footers carry "Page X of Y" with a total cached at authoring time. When changing a header or footer, inspect every first-page, default and even-page part of the section and change them together, or deliberately leave the cover unnumbered; do not restyle the default footer and leave the master's first-page footer behind. Use the host's supported renderer and field-update capability before delivery, and verify that the saved cached total matches the rendered page count. Do not assume rendering updates fields automatically: a viewer may show the cached value, leaving "of 3" on a six-page response. If the host cannot update or verify the required total, report the gap. Viewers can still paginate differently from the render, so replace "Page X of Y" with `PAGE` alone when the buyer does not require a total.
- Treat company branding in an example, including GovTribe branding used as sample-company identity, as example content. Use supplied approved company branding when available; otherwise retain an appropriate logo placeholder or neutral company text. Preserve unrelated template artwork and publisher attribution. Do not invent a logo or redesign a template for a content update.
- Buyer-required forms, wording and submission limits govern the response. If they conflict with the selected generic template, explain the concrete conflict and adapt the output to the controlling requirement; clarify only a material unresolved choice. Do not silently drop required content to fit a layout.
- Save a distinct populated copy, retaining the template as its source and preserving any existing user draft. Continue later edits from the selected working revision instead of restarting from the blank master.

## Verify the adapted artifact

Reconcile the saved artifact to the field/section map. Check target and company identities, current source dates, value meanings, required content, references, unresolved fields and every intended replacement of example content. Verify formulas and chart data as well as visible labels. Example content may survive only when explicitly retained and clearly labeled for that purpose.

Complete the host's exact-artifact checks and [shared revision checks](revision-checks.md). Return the editable populated file and requested exports with matching revision names. Report material missing inputs and readiness accurately; a draft with unresolved company evidence is not a submission-ready response.

If the selected editable master or host authoring capability is unavailable, keep the selected identity and provide a labeled Markdown field/section draft (or CSV for tabular content) with unresolved inputs and the precise source/capability needed to finish. Do not claim that the master was populated or substitute an example. When only rendering or inspection is unavailable, deliver the usable native draft and requested supported exports with that gap stated.
