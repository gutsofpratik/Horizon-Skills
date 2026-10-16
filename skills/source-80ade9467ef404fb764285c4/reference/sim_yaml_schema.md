# `.sim.yaml` schema

The file `postman simulation run <filepath>` reads. It lives in
`postman/simulations/NAME.sim.yaml`, beside the `postman/mocks/` folders it
composes. `postman simulation create` writes one; the Postman app writes the
same shape with `id:` fields added.

```yaml
id: 01a110fc-e3f5-77eb-af59-0a711a509960        # written by the Postman app
simulation: checkout-dev
routing: path
mocks:
  - id: 01a110fc-e344-72ca-9d0c-1bb83b99ec2a    # written by the Postman app
    routeKey: products
    path: ../mocks/products/config.yaml
    scenarios:
      - path: ../mocks/products/default.js
  - routeKey: shopping-cart
    path: ../mocks/shopping-cart/config.yaml
```

## Root

| Key | Required | Notes |
| --- | --- | --- |
| `simulation` | Yes | The simulation's name. |
| `mocks` | Yes | Non-empty list of members. |
| `routing` | No | `path` (default) or `header`. Any other value means `path`. |
| `id` | No | The simulation's id in its workspace. A local run ignores it; leave it as written. |

## Member

| Key | Required | Notes |
| --- | --- | --- |
| `path` | Yes | The mock's `config.yaml`, or a `.js` handler. Relative paths resolve from the `.sim.yaml`'s folder, then from the working directory. `file` is a legacy alias. |
| `routeKey` | No | The member's address. Lowercase letters, digits, `-` and `_`, at most 64 characters, unique per simulation. Defaults to the kebab-cased name. |
| `name` | No | Display name. Defaults to the mock's folder name for a `config.yaml`, else the file name. Must be unique. |
| `scenarios` | No | Fault conditions, below. |
| `id` | No | The mock's id in its workspace. A local run ignores it. |
| `port` | No | Ignored by `simulation run`, which gives each member an internal port. |

## Routing

- **`path`**: a member is at `http://localhost:<port>/<routeKey>`. The first
  path segment selects the member and is stripped, so `/payments/cart` reaches
  the `payments` member as `/cart`. Point the service's base URL for that
  dependency at `http://localhost:<port>/<routeKey>`.
- **`header`**: every member shares `http://localhost:<port>`, and the caller
  picks one with an `x-mock-slug: <routeKey>` header. Use it only when the
  caller can send that header.

The router answers on its own, without reaching a member:

| Response | Cause |
| --- | --- |
| `400 {"error":"Prefix the request path with the member routing token, e.g. /<routeKey>/path."}` | No routeKey under `path` routing: the path was `/`. Under `header` routing the error asks for the `x-mock-slug` header instead. |
| `404 {"error":"Unknown simulation member '<x>'.","available":[...]}` | `<x>` isn't a routeKey. Under `path` routing this is often a client that dropped the base URL's path, so `<x>` is the endpoint's own first segment. |

## `scenarios`

Each entry is a selection, and only its `overrides.conditions` inject faults:

```yaml
scenarios:
  - overrides:
      conditions:
        latency:
          delay_ms: 250              # hold each request 250 ms, then go on
        error:
          status_code: 503           # every request fails with 503
        rate_limit:
          requests_per_minute: 30    # the 31st request in a minute gets 429
        chaos:
          failure_rate: 10           # 10% of requests fail with 500
```

This example sets all four to show their fields. They run in a fixed order,
`latency`, `error`, `rate_limit`, `chaos`, whatever order you write them in,
and the first to fail a request ends it: with `error` set, `rate_limit` and
`chaos` never fire. Set one failure at a time, optionally with `latency`.

The mock's default handler always serves, and conditions run in front of it.
An entry with only `path` or `id`, as the Postman app writes, injects nothing.
Unknown condition names are ignored, so a misspelled one fails silently.
`overrides.bypass` prints a warning and is ignored.

The legacy form `- type: error` with `config: { status_code: 503 }` is still
accepted and validated strictly: an unknown `type` is an error.

| Condition | Field | Effect |
| --- | --- | --- |
| `latency` | `delay_ms` (positive number) | Holds each request that long, then serves it normally. |
| `error` | `status_code` (integer 400–599) | Every request returns that status with `{"error":{...},"scenario":"error"}`. |
| `rate_limit` | `requests_per_minute` (positive integer) | Requests over the limit return `429` with a `Retry-After` header and `"scenario":"rate_limit"`. |
| `chaos` | `failure_rate` (0–100) | That percentage of requests, chosen at random, return `500` with `"scenario":"chaos"`. |

A condition applies to every route on its member. To fail one endpoint while
its siblings succeed, split that endpoint into its own mock.

## `simulation run`

| Flag | Notes |
| --- | --- |
| `-p, --port <n\|auto>` | Port to serve on. Defaults to 3000, and silently falls back to a free port if 3000 is busy. An explicit port fails instead. |
| `--output ndjson` | One JSON event per line on stdout, instead of the default readable log; messages go to stderr: `listening` (port, url, each member's `routeKey` and `address`); `request`, one per request a member served (`routeKey`, `method`, `path`, `statusCode`, `duration` in ms, headers and bodies); and `summary` on shutdown (`requestsServed`, `requestsFailed`). The router's own `400` and `404`, and injected faults, aren't logged. |
| `-e`, `-g`, `--dataset` | Environment, globals and datasets for every member, as for `mock run`. |
| `--no-history` | Record nothing. A `.sim.yaml` linked to a workspace otherwise records each start there; an unlinked one records only with `-w` and `--simulation`. |

The argument can also be a simulation id from a workspace: the members are
fetched and served locally. All members start before the port opens, so one
`listening` event means the whole simulation is up. A member that fails to
start stops the run with `Error: ...` and exit code 1. Ctrl+C stops everything.
