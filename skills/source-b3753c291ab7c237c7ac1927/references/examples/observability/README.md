# Observability

Where Fieldkit's signals go, and which tool answers which question. The estate is
Datadog and Sentry: not one deployment but the tools every system reports into, so it
gets a directory of its own rather than a place in one system's docs.

Datadog is a separate account per environment ([environments](../environments.md));
Sentry is one organization, `fieldkit`, with a project per system.

## What each tool answers

| Tool | Answers |
|---|---|
| Datadog logs | What a log line said, for one request, account, or deploy. |
| Datadog metrics | Rates and saturation over time: request duration, queue depth, worker pools. |
| Datadog APM | What one request did, span by span. |
| Sentry | Which errors are happening, in whose code. Project `atlas` for the backend, `storefront` for the site — the storefront ships errors and nothing else ([storefront](../storefront/README.md)). |

How each system ships into these — and the correlation keys to pivot between signals —
is the producer side, owned by each system's own file:
[atlas observability](../atlas/observability.md). The storefront ships errors only, so
it has no file of its own.

## Alert rules

Monitors are Terraform in `fieldkit/infra/datadog/` — the code owner for alerting;
nothing is hand-edited in the Datadog console, and a monitor with no Terraform
counterpart is a finding. Thresholds churn, so none are quoted here — the Terraform
owns them.
