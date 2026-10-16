# The connections and telemetry leg

The estate beyond plugins — connections, telemetry datasources, and how well agents'
queries against them are doing — read through the incident.io connection's health
tools, with honest lines for whatever this session can't reach.

## Connections

`extension_connector_list`, where the session has it — each connection with its type,
enabled state, capabilities, the tools it exposes, and its connection status:

- **A connection needing re-authentication is a finding**, routed to the dashboard's
  data sources page.
- **Cross-check dependencies**: a telemetry dependency in a plugin's README
  connections table that is absent or disabled is a real gap, routed to extensions or
  the dashboard. A README row for a team's own tool (an internal MCP, a warehouse) may
  legitimately not appear here — its absence alone is not a finding; and when a
  dependency is missing, name the question the team must answer ("is this actually
  consulted during incidents?") rather than answering it for them.
- **Read the tools field carefully**: absent means nothing is callable there;
  `tools_unlisted: true` means callable but not named — report "tools unlisted",
  never "no tools".

Without the tool, the `telemetry://datasources` resource gives the same inventory
without health; without either, ask the user to read the dashboard's data sources
page and record what they report as user-reported.

## Query health

`nexus_health_show`, where the session has it — the same rollup the dashboard
computes, so the report can never disagree with it: per-source status, query
statistics over the stats window (total, failed, empty, useful), attention reasons,
and usage counts. Read it with one correction: **its telemetry children cover only
sources that ran queries in the stats window** — a connected source that has never
been queried appears in `extension_connector_list` but not here, and "absent from
health" must not be read as "unhealthy" or "healthy". Cross-reference the two lists
and report never-queried sources as exactly that.

Where the session lacks the tool, the honest report line is:

> Datasource query health isn't readable from this session — check the dashboard's
> data sources page.

Don't infer health from silence, and don't turn "I can't read it" into "it's
probably fine".
