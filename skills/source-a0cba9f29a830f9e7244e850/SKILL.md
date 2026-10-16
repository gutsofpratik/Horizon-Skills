---
name: portfolio-review
description: Reviews a saved portfolio, household or model with Advisor Center analytics in three sections rendered inline in the chat — portfolio snapshot, stress scenarios, then opportunities, fund health and Funds to Explore — closing with follow-ups earned by what it found. Use when asked to review a portfolio, run a portfolio review, analyse holdings, pull up a client's account, run the numbers on a portfolio, look at concentration or downside exposure, find issues or opportunities in a portfolio, check whether a client's funds are healthy, or prepare for a client review meeting. Skip this skill when the advisor already named one specific analysis — "what's the risk on this", "run the stress scenarios", "how does this compare to the model" — and call that tool directly instead of running the three-section pass.
---

# Portfolio Review

Render the three numbered sections inline in the conversation, one pass — mechanism
per `references/design-tokens.md` § Mechanism and output anatomy per
`references/rendering.md`.
Do not render into a document, canvas, webpage, side panel, file, or download.

**Sequence — call, write, then call.** Each section is written in full, visual and prose,
before the next tool call is issued. Never batch the calls and write afterwards.

```
analyze_portfolio → write header + section 1
analyze_scenarios → write section 2
get_opportunities_and_issues ‖ get_fund_health_and_ideas → write section 3
→ write closing
```

The two step-3 calls run together; nothing else runs in parallel. One visual per section,
never one for the whole review.

- **Scope check first.** If the advisor named one specific analysis, call that tool and
  stop. This skill is for the open-ended ask — "review this", "run the numbers", "pull
  up their account".
- If no saved portfolio, household, model, pasted holdings or resolvable subject exists,
  route to `guided-portfolio-builder` or the appropriate lookup path before reviewing.
- Never make the advisor name a tool or a field.

| Before | Read |
|---|---|
| laying out a section, citing, or reporting a gap | `references/rendering.md` |
| emitting any visual, or writing any number | `references/design-tokens.md` |

## Rendering minimums if references are unavailable

Do not tell the advisor a reference file was unavailable. If the host cannot load the
reference files, still follow these minimums:

- Try the richest inline visual form first; markdown tables are fallback only.
- Snapshot metrics render as same-row stat tiles, not a two-column metric/value table.
- Scenario impacts render as a chart or bar visual, not a plain percentage table.
- Fund health renders as a multi-column card grid when cards are available. Every fund
  card includes the Funds to Explore tail; if none are returned, say `No Funds to
  Explore returned`.
- Opportunity signals render as status-tinted cards with an Available path, not as a
  plain markdown table, when cards are available.
- Clear counts require returned clear checks. If the response returns only fired rules,
  state only the number flagged.
- Fund-health commentary is visual-first: the fund cards carry each flagged fund's
  drivers, status, Funds to Explore, and links. Prose after the cards is at most three
  bullets: highest-priority fund, why it outranks the others, and coverage gaps.
- For red or flagged fund-health opportunities, encourage reviewing the flagged funds in
  chat. A methodology URL is labeled `Fund health methodology`, never as a fund-details
  tab or route.
- Closest model renders as a designed comparison prompt: model card, split-match note,
  and primary call-to-action `Run side-by-side comparison in this chat`. The match is on
  equity/fixed-income split only, not holdings. Do not render closest model as plain
  prose plus a markdown table when cards are available.
- Surface returned Advisor Center links. If any section returns `comparison_url`,
  `methodology_url`, fund URL, product URL, or route, include the relevant link near the
  block it supports.
- Never show tool names, field names, ids, or missing-reference commentary in the
  advisor-facing answer.

## Links this domain carries

| Field | Present on |
|---|---|
| `comparison_url` | every analysis tool — opens the same subject in the comparison view |
| `methodology_url` | fund health, ESG, wealth projection |
| `closest_model.comparison_url` | `analyze_portfolio` — opens the subject against its closest model. The only link in the closing. |

Cite them per `references/rendering.md` § Citing. The comparison view renders live under
its own analysis date and fee settings, so its figures can differ from the review.

## Step 0 — Resolve the subject

Every analysis tool takes `subject: {type, id}`. Both members required. No inline
positions.

| `type` | Addresses | Id from |
|---|---|---|
| `PROSPECT_ID` | one saved portfolio | `list_portfolios`, `create_portfolio` |
| `AW_AGGREGATE` | one household | `list_household_portfolios`, `create_household_portfolio` |
| `MODEL_ID` | a BlackRock model | `list_models`, `get_model` |
| `ENTITLED_MODEL_ID` | a third-party model | `list_models`, `get_model` |

Route on what the advisor gave:

- **Id already in context** — use it. Do not re-list.
- **A name, or nothing** — call `list_portfolios` and `list_household_portfolios`,
  present the candidates, let the advisor pick. Never guess between two subjects sharing
  a name; `total_market_value` and `holding_count` tell them apart.
- **A model** — `list_models`, then pair `model_id` with its group's
  `comparison_id_type`.
- **Pasted holdings or a spreadsheet** — save first, see below.

Take `comparison_id_type` off whatever read or created the subject. Never build a
`TYPE:id` string or comma-join ids.

**Hold the subject's record** before step 1 — the `list_*` entry, or the `create_*` /
`get_model` response. An id that arrived with no record: call the matching `list_*`
once and take its entry. The header and stat row read from this record.

**Benchmark** — only when the advisor named a model or benchmark in the ask. Resolve it
through `list_models` to its own `{type, id}` and thread that one through steps 1 and 2.
Never choose a benchmark for them.

### Saving unsaved holdings

`create_portfolio` **writes real data**. State that, wait for an explicit yes. Then:

- Resolve identifiers first. CUSIP → `cusip`, ISIN → `isin`. A CUSIP in `isin` returns
  "no such security".
- Tickers and names go through `search_securities`. On `resolution: ambiguous`, present
  candidates and ask — never pick a share class for them.
- Spreadsheet: state the inferred column mapping, get confirmation. A blank or
  unparseable identifier — name the row and stop, never drop it silently.
- `portfolio_type` is required by rule though schema-optional. Ask; do not default.

Review the returned id as `PROSPECT_ID`.

## Step 1 — Portfolio snapshot · `analyze_portfolio`

- `nav` absent = a model. Percentages only, no dollars.
- Household: `account_contributions` renders as `Risk by account` between allocation and
  equity geography, and leads the prose — which account carries the risk is the story.
- Benchmark named: call `analyze_portfolio` on the benchmark too for the benchmark tile
  row. Otherwise no benchmark row.
- Closest model — when the response carries closest_model, call list_models and take the row whose model_id matches its id. Hold that row and the subject's equity and fixed-income slice figures from asset_allocation. Nothing renders in section 1; both are carried to the closing. No closest_model: no closing block, and never substitute the named benchmark for it.

**Write section 1 now**, before calling `analyze_scenarios`.

## Step 2 — Scenarios · `analyze_scenarios`

- Pass `initial_investment` only when the subject has no `nav` and the advisor named an
  amount.
- Pass `benchmark` only when one was resolved in step 0. Never pass
  `include_contributors` or `include_all_scenarios` — both are follow-ups.
- Display order and dollar basis per `references/rendering.md` § 2. Impacts are
  modelled, not forecast: never call one a prediction, a probability or a
  likelihood.

**Observations** — take each of these in order whose data is present, stop at five;
write fewer than three only when fewer are present, never pad:

1. The worst case and its cost.
2. Whether the response's own worst scenarios are materially worse than the
   shortlist this deployment always reports — only when the response
   distinguishes the two.
3. The spread between worst and mildest.
4. Rate sensitivity on its own — only when a Treasury scenario is present.
5. Benchmark-relative direction — only when `relative_impact` exists.

Each bullet cites a figure.

**Write section 2 now**, before calling the step-3 tools.

## Step 3 — Opportunities, fund health, Funds to Explore · `get_opportunities_and_issues` + `get_fund_health_and_ideas`

- Empty `signals` = nothing flagged. Say that; never omit the section.
- **Flagged fund** = one or more `drivers` fired. `status` is rendered as given, as a
  dot and words, and orders the cards; flag count orders within a status.
- Name `non_fund_holdings` and `unknown_holdings` by count. No position vanishes
  silently.

**Commentary** — point form, after the cards. Signals and fund-level drivers already sit
in visual cards per `references/rendering.md` § 3; do not restate each card in prose.
Write at most three bullets: which opportunity or fund to inspect first · why it outranks
the others, citing the separating metric · coverage gaps such as non-fund or unresolved
holdings. No paragraph per flagged fund.

**Write section 3 now**, then the closing.

## Closing

- **Caveats** — inferred column mapping, resolved identifier, placeholder investment
  amount, equity-sleeve scope, benchmark assumed. Only those that applied.
- Closest model — only when step 1 carried one. Render the comparison prompt in
  `references/rendering.md` § Closest model, filled from the held `list_models` row and
  allocation figures. The primary next step is to run the side-by-side comparison in
  chat. The Advisor Center link is secondary when returned, not the main action. The
  match is on equity/fixed-income split only, not holdings — say so.
- **Follow-ups** — three to five, each one a tool this domain actually carries
  and each earned by something this review found: a model or benchmark
  comparison when a closest model was named, deeper risk, ESG or carbon,
  simulated performance, wealth projection, style factors, the full scenario
  set, or scenario contributors. Never offer one the findings do not motivate.
- Report/PDF handoff is reactive only. Do not proactively mention report generation in
  the closing. If the advisor asks for a report or PDF, route through
  `ac360-capability-router`.

## Throughout

- **Cite, attribute and report gaps per `references/rendering.md`** — every section.
  The advisor decides; this skill organises what came back.
- **Links are part of the output.** When a returned Advisor Center, comparison,
  methodology, fund or product link supports a rendered block, surface it near that
  block. Do not finish a review with no links if any returned link exists.
- **Never drop a section.** Within a section, lead with its most material finding. The
  closing names the most material finding of the whole review.
- **Read-only.** `create_portfolio`, `update_portfolio`, `clone_portfolio`, the
  household writes and `update_advisory_fee` write real data. Ask first, every time, and
  say what will be written.
- **One subject, all three sections.** Never switch mid-review.
- **Credential and gate failures are plumbing**, not findings about the portfolio.
- **Advisor-facing, not client-ready.** Concise and analytical working material. No
  talking points, no reassuring framing, no marketing tone.
- **No tool names, field names or ids** in anything the advisor reads.
