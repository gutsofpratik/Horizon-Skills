# Rendering

The exact output anatomy for short route cards, link-out rows, unsupported callouts and missing-link fallbacks. Visual primitives, colours, geometry and number formats come from `design-tokens.md`; this file names the blocks and rules for this skill.

## Mechanism

Render **inline in the conversation** using the richest form the host displays there:

1. The host's own inline visualization capability — short cards, callouts or compact rows that render in the conversation itself.
2. Fallback when rich cards/charts are unavailable: markdown tables. Tables must preserve the same labels and values as the richer visual.

Capability selection is mandatory. Before writing any markdown table fallback, decide
whether the current host can render the specified inline visual mark for the block. Use
the richer mark when any inline chart, card, component, or visualization channel is
available. Use markdown tables only when no inline visual channel exists, the inline
render fails, or the host explicitly cannot display that block's richer mark. Do not
choose markdown tables for speed, familiarity, or because the fallback example is
easier to copy.

Do not render into a document, canvas, webpage, side panel, file, or download. Do not use raw HTML, raw SVG, or box-drawing art. Never describe the mechanism or fallback to the advisor.

## Page

- Keep the response short. Usually one route card or one compact table is enough.
- Use a route card only when it improves clarity or presents an Advisor Center link-out.
- Do not add analytics, estimates or alternate calculations.
- Use only returned routes, approved links, or the home-dashboard fallback from `SKILL.md`.

## Route card

Use for known Advisor Center workflows unavailable in this chat or supported handoffs.

Card anatomy:

1. **Status** — `Route available`, `Supported elsewhere`, or `Unavailable here`.
2. **Workflow** — returned or known workflow name.
3. **Next step** — one short instruction with a link when available.
4. **Context** — optional one sentence only when it distinguishes similar routes.

Fallback when rich cards/charts are unavailable:

| Status | Workflow | Next step | Context |
|---|---|---|---|
| Route available | Tax evaluator | Open Advisor Center to continue | Full workflow is in the web experience. |

When a returned Advisor Center link is available, make the next step a descriptive hyperlink using the link role from `design-tokens.md`. If no exact link is returned, use the approved home-dashboard fallback from `SKILL.md` and say the exact link was not returned.

## Link-out rows

Use when multiple route links or related destinations are returned.

| Destination | Use when | Link |
|---|---|---|
| Tax evaluator | Full tax workflow | Open in Advisor Center |
| Home dashboard | Exact link unavailable | Open dashboard |

Rules:

- Link text is descriptive; never print a bare URL unless links do not render.
- Use Advisor Center routes for workflow continuation.
- If no exact link is available, use the approved home-dashboard fallback from `SKILL.md`.
- Do not build links by pattern.

## Unsupported or unavailable callout

Use for unsupported horizons, currencies, removed metrics or workflows unavailable in this chat.

Callout anatomy:

1. **Limit** — what is unavailable.
2. **Closest supported path** — only when returned or specified in `SKILL.md`.
3. **Next step** — route or supported skill when available.

Fallback when rich cards/charts are unavailable:

| Limit | Closest supported path | Next step |
|---|---|---|
| Requested horizon is unavailable here | Returned supported horizon | Use the supported analysis path |

## Supported handoff row

Use when the request belongs to another loaded skill or direct tool.

| Request | Route |
|---|---|
| Broad portfolio review | `portfolio-review` |
| Benchmark setup | `guided-benchmark-selection` |
| Portfolio creation | `guided-portfolio-builder` |

Keep these as internal routing labels when possible; advisor-facing output should describe the workflow rather than expose unnecessary file or skill details.

## Absent data

- Missing exact link: say the exact link was not returned and use the approved dashboard fallback when appropriate.
- Unsupported metric: say it is not available in this chat.
- Unsupported currency: say Advisor Center analytics are available in USD only.
- No alternate path: state the limitation and stop.

## Posture

- Keep the answer neutral and workflow-oriented.
- Do not imply an Advisor Center workflow has been completed.
- Do not estimate unavailable metrics, currencies or horizons.
- The route or limitation is the output; avoid extra analysis.
