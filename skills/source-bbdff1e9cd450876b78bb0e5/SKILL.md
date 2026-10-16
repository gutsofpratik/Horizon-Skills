---
name: telemetry
description: >
  Query an organization's observability data — logs, metrics, traces, profiles, dashboards,
  Kubernetes, SQL databases — with the incident.io telemetry tools. Use when answering a
  question that needs evidence from its monitoring: what errors fired, when latency moved,
  which pod restarted, what a dashboard showed, what its databases hold. Not for questions
  the incident record already answers, and not for querying incident.io's own data.
---

# Telemetry

An organization's observability data lives in datasources it connected — a Loki, a
Prometheus, a Honeycomb, a Postgres. Each holds different signals and speaks a different
query language. You reach all of them through two sets of tools: the native telemetry tools,
and the extension connector tools where there are any. The next section says how to call
them; the rest of this skill applies however you call them.

## How you reach telemetry

### Native telemetry

```
telemetry_guidance_show(path: "data-sources.yaml")
log_query(datasource_id: "…", purpose: "…", expression: "…", time_from: "…", time_to: "…")
```

The telemetry tools are on the incident.io connection. Each tool's description is the
authority on it: what it does, the arguments it takes, and how to read what it returns.

Where the session has no `telemetry_guidance_show`, say the incident.io connection has no
telemetry tools rather than guessing an answer.

#### Running queries together

Run queries that do not depend on each other as parallel tool calls, in one turn.

### Extension connector

Connector tools are on the incident.io connection, named `<connector>__<tool>`. If there are
no such tools, there are no connectors.

### Docs

Read the datasource index, `data-sources.yaml`, and each file its `docs` fields list with
`telemetry_guidance_show`, passing each path exactly as listed. Read each one whole, in one
turn of parallel calls. If your client cuts a result short or saves it to a file, read on
from where it stopped before you query.

### Times

Put the window in `time_from` and `time_to` as RFC3339: leave them out and the query covers
only the last hour. Convert anything a person expressed as a wall-clock time from the current
date in the conversation, rather than from your own sense of now.

### Errors

Read the error message, not the error code: the message says what went wrong. An internal
error with no detail means the call failed, not that the data is empty. A product error
means the organization cannot query telemetry here — say so. A datasource that cannot be
reached is a fact about the monitoring, not an answer to the question.

## Connectors

Some sources of telemetry data are made available through a connector rather than a native
telemetry data source. Connectors are not listed in `data-sources.yaml`.

When picking where a signal lives, consider both the telemetry datasources and the
connectors, then query the one that holds it. Native telemetry wins when both hold the same
data; do not query both to confirm. Note that some vendors will be available through both
native telemetry (e.g. for logs and metrics) and a connector (e.g. for inspecting ingestion
configuration). When the native datasource for a signal errors or returns nothing, check the
connectors before reporting the signal as unavailable.

Use your judgement to decide whether a connector is appropriate to use to answer a telemetry
query - not all connectors, or tools within a connector, expose telemetry data. E.g. a
connector called `production operations` with a tool `read_service_restart_logs` would be
appropriate for a telemetry query, whereas a connector called `linear` with a tool
`fetch_project_updates` would not be.

## The loop

1. **Read `data-sources.yaml`**, then **the connectors**, to pick a datasource.
   `data-sources.yaml` lists each one with its ID, type, what it holds and the earliest data
   it still keeps — and, under `docs`, the paths of its query-language reference and its own
   guidance. Match the question to a datasource that holds that signal: a metrics source
   cannot answer a question about log text. Then check the window you need against that
   datasource's earliest timestamp, rather than learning it from a refusal later.
2. **Check `memory_recall` first**, where it is available. It returns expressions already
   proven on this account for that datasource — adapt one, or replay it exactly with
   `from_query_id`, rather than writing from scratch.
3. **Read the tool's description**, and the connector tool's if you have decided to use a
   connector, then run it.
4. **Drill into what came back.** A telemetry query returns a `result_id`, and the drill-down
   tools narrow that stored result without re-querying the source.
5. **Cite what you used.** A finding without the query behind it cannot be checked.

## Ask more than one question at a time

Queries that do not depend on each other should run together rather than one after another,
as [Running queries together](#running-queries-together) shows. An incident rarely turns on a
single query, and running them in sequence spends an engineer's time for no reason.

Batch different questions, not copies of one query you have not proven yet. A batch returns
when its slowest query finishes, so it costs whatever its worst member costs, and a shape
that is too broad — or that a source has already turned down once — fails once per copy:
slicing one unproven query across a dozen windows is a dozen ways to be told the same no.
Run it once, read what came back, and fan out from there.

A datasource serves every query from one shared budget. Queries that each read a lot — a
selector the guidance says covers most of the data, a range of hours — slow each other down
when they run together, and a batch of them can all time out where each alone would have
finished. Your first query against a selector and range runs on its own. Batch queries you
have seen come back in a few seconds. Run the expensive ones at
most two at a time against one datasource, and one at a time once one of them has timed out.

Different phrases over the same selector and range are the same scan repeated. Ask for them
in one query where the language allows it — the query-language reference shows how — rather
than one query per phrase.

## Writing a query

`log_query`, `metric_query` and `span_query` take `expression`: a query in the
datasource's own language, run exactly as written. A failed or empty query is yours to fix
and resubmit. The remaining query tools, and connector tools, vary — some take a query you
wrote, others take a plain-English description. Read each tool's description for its contract.

Before your first query against a datasource, read every file its `data-sources.yaml`
entry lists under `docs`, as [Docs](#docs) says: the query-language reference under
`/telemetry/references/`, and the datasource's own guidance under `/telemetry/guidance/` —
its real labels, fields, metric names and worked examples. What a query costs and how to
size its range are further down each file, so read it to the end.

Use only names you can source from the guidance, a result, or the incident: a guessed label or metric matches nothing, and nothing warns you that it
could not have matched. When none of those covers the label, label value or metric name
you need, read it off the datasource with `telemetry_inspect` rather than guessing.

You own query cost, and the datasource will time out or refuse expensive scans. Anchor
every filter to real values; a match-anything selector scans the whole estate. In many query
languages only some parts of a query decide how much the source reads — an indexed selector
and the range — while filters applied after reading make it no cheaper. The query-language
reference says which parts those are. When a query times out, narrow those parts rather than
fanning out variants of the same expensive scan.

Set `purpose` to what the query is trying to establish — it is recorded with the query and
shown to the responder beside your expression.

Times are UTC. [Times](#times) says how to give one a person expressed on a wall clock.

Every result carries the expression it executed, so changing one filter on a query that
worked means copying that expression and editing it, not rewriting it from memory.

When the question is who or which — which job wrote these rows, which caller sent the
failing requests, which tenant's traffic dominated — count by the field that names the
job, caller or tenant over the whole window rather than listing lines. Filter on what you
already know — the table, message or resource that was touched, and the window — not on
the values you expect the answer to take. A filter built from expected answers can only
return those answers.

## When a query comes back empty

Empty is a result, not a failure, and two very different things produce it: the data
genuinely shows nothing, or your query matched nothing it could have matched.

Do not guess between them. An empty result may carry a `diagnostics` block saying what the
datasource could establish about which it was — read that first, and follow what the
tool's description says it means. Where there is no diagnostic to read, widen the query: drop
the narrowest filter, or stretch the window, and see whether rows appear. Rows on the wider
query mean your filter was wrong.

When you report an absence, say what you established and how. "No matching errors in the
last hour on this datasource" is a finding. "There were no errors" is a claim you have not
earned.

## When a source refuses

A refusal is the other kind of non-answer. The source declined to run your query rather
than running it and finding nothing, so what it tells you is about the query: it asked for
more than the source will scan, grouped into more series than the source will hold, or
reached back past what the source still keeps. Re-running the same shape is the one
response that cannot work.

Step down instead of dropping the question, and step down on the axis the refusal names:

- **Too many series** ("maximum number of series", "too many series", a cardinality
  limit): the grouping is too fine. Drop the grouping field with the most distinct values
  first — IDs such as organisation or user before names, names before the field that says
  who did the work, such as subscriber, job or pool — and keep the field that answers the
  question. Add the ID back only once you know which of those matter.
- **Too much scanned** ("timed out", "deadline exceeded"): shorten the window, or narrow the
  part of the query that decides what the source reads (see the reference). A timeout inside
  a batch may be the batch: re-run that query on its own before concluding the shape is too
  broad. If the shorter window also times out on its own,
  the window was not the problem: change the filter or aggregate by a field instead.
- **Capped listing** ("Result truncated", a line or entry cap): the source ran the query and
  returned only the newest lines. A thousand-line cap over thirty minutes can be the last
  few seconds. Nothing before the first returned line has been read. If the moment you want
  is earlier, end the window at that moment and shrink it until the result fits, or count
  by a field instead of listing.
- **Rate limited** ("too many outstanding requests"): your own batch is keeping the source
  busy. Re-run only the queries that were refused, at most two at a time. Re-running the
  whole batch after a pause meets the same limit.
- **Past retention**: another datasource may hold the same signal for longer;
  `data-sources.yaml` says which, and an identifier you already have carries the question
  across to it.

Never narrow what you are asking about to recover from a refusal. A filter drawn from the
values you expect the answer to take — a particular event, job or caller — makes the query
cheaper by excluding everything else, and if the answer lies outside those values the empty
result then looks like an answer. Narrow the window, the stream or the grouping instead.
Note the refusal on your way past: a retention wall does not move, and one run should only
meet it once.

## Reporting

Say what the data shows and cite the queries that showed it. Where it cannot answer the
question, say that plainly — a confident wrong answer costs an engineer more than an
honest gap, because they will stop looking.

A query that failed searched nothing. When you split a question across windows or streams
and some of them timed out, were refused or did not parse, do not report a total or a zero
for the whole: give the figure for what did run, and name the windows or streams it does not
cover. If you searched fewer streams than the question asked about, say which ones; a zero
there is not a zero for the question.

Describe what you searched from what the queries ran, not from what you meant to run: read
each result's time range and selector back before you name them. Never give the requested
range as the one you searched when only part of it ran, and never attribute a record to an
organisation, service or caller its own fields don't name.

Before you conclude, check that the result holds the value your conclusion turns on. A
summary across a family of series does not give you any one series' number, and a total
does not give you the split inside it. Where the deciding value is missing, say the result
cannot tell you. Do not read it as a yes or a no, and do not let it outweigh a more
precise measurement you already hold. Query the one series you need, or report the gap as
a gap.
