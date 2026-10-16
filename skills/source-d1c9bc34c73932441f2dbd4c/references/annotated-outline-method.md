# Annotated Proposal Outline Method

Use this reference when a proposal-outline workflow needs more explicit structure, taxonomy, or writer-package rules.

## Domain anchors

- The FAR Uniform Contract Format identifies common solicitation sections, including Section C for descriptions/specifications/statement of work and Section L/M equivalents in Part IV for instructions and evaluation. Use the structure when present, but map by function when solicitations use different labels.
- Source selection rules require evaluation against the stated solicitation factors/subfactors. Therefore the outline must make those factors easy to find and answer.
- Army AFARS Section L/M templates summarize the practical distinction: Section L tells offerors what to submit; Section M tells them how the proposal will be evaluated.

Useful public references:

- FAR 15.204-1 Uniform Contract Format: https://www.acquisition.gov/far/15.204-1
- FAR Subpart 15.3 Source Selection: https://www.acquisition.gov/far/subpart-15.3
- AFARS Chapter 9 Templates — Sections L & M: https://www.acquisition.gov/afars/chapter-9-templates-%E2%80%93-sections-l-m

## Requirement-shredding cues

Extract requirements from all solicitation areas, not only explicit instructions.

High-signal terms:

- `shall`, `must`, `will`, `required`, `mandatory`
- `submit`, `provide`, `include`, `describe`, `identify`, `demonstrate`, `explain`, `address`
- `not to exceed`, `page limit`, `font`, `margin`, `volume`, `tab`, `file name`
- `will evaluate`, `basis for award`, `acceptable`, `unacceptable`, `strength`, `weakness`, `risk`, `confidence`, `relevance`, `recency`
- `deliverable`, `CDRL`, `report`, `transition`, `key personnel`, `staffing`, `quality control`, `management plan`, `technical approach`, `past performance`, `pricing`

Also inspect:

- tables and attachments
- CDRL/data-item lists
- forms and representations/certifications
- pricing templates
- portal/submission instructions
- Q&A and amendments
- award-basis paragraphs
- page-limit and formatting paragraphs

## Requirement taxonomy

Use these requirement types unless the proposal team already has a house taxonomy. See `assets/annotated-proposal-requirement-types.yaml` for the canonical labels used by this workflow.

- `instruction` — proposal organization, content, format, submission, volume instructions.
- `evaluation` — factor/subfactor, adjectival/risk standard, award basis, acceptability gate.
- `work` — SOW/PWS/SOO task, performance standard, deliverable, management obligation.
- `past-performance` — recency/relevance, references, questionnaires, experience narratives.
- `pricing` — pricing volume/table, basis of estimate, rate, labor category, travel/ODC rules.
- `compliance` — certifications, representations, socioeconomic, security, facility, clearance, contract clauses affecting proposal response.
- `form-attachment` — named forms, templates, resumes, letters, reps/certs, subcontractor docs.
- `inferred` — logical response need derived from evaluation/work requirements but not explicitly instructed.
- `gap` — missing, conflicting, ambiguous, or inaccessible item.

## Outline decision rules

1. **If there is a required volume/section structure:** follow it exactly.
2. **If Section L is sparse but Section M is detailed:** create headings from evaluation factors and map each to the relevant PWS requirements.
3. **If the PWS is task-heavy:** use PWS tasks as substructure under the relevant evaluation/technical headings.
4. **If page limits are tight:** prioritize evaluated and mandatory content; move background into concise proof points, tables, or graphics.
5. **If past performance is evaluated:** create a past-performance evidence plan even if past performance is in a separate volume.
6. **If oral presentations/demos are included:** add a separate outline/work package for oral materials, scripts, slides, demos, or scenario responses.
7. **If pricing is separate:** include pricing instructions and dependencies in the compliance matrix, but do not draft pricing strategy unless asked.

## Writer-work-package rules

For each writer work package, include:

- section title and outline location
- writer/SME role
- required source requirements
- inputs needed from customer/company
- evidence/proof points needed
- graphics/tables to create
- dependencies
- reviewer focus

Default owner roles:

- Proposal Manager — outline integrity, compliance matrix, schedule, page budget.
- Capture Lead — win themes, customer knowledge, competitive strategy.
- Technical Lead — technical approach, PWS mapping, solution proof.
- Program Manager — management approach, transition, quality/risk/reporting.
- HR/Recruiting — staffing, key personnel, resumes.
- Contracts — clauses, reps/certs, submission, exceptions.
- Pricing — pricing volume, cost assumptions, BOE dependencies.
- Past Performance Lead — references, relevance narratives, questionnaires.
