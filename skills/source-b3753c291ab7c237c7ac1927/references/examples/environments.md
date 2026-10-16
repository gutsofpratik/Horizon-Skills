# Environments

Two runtime environments, production and staging, each an AWS account of its own — the
account boundary is the isolation model, so a credential for one cannot touch the
other — plus a third account, `fieldkit-ci`, that runs no workloads. Authoritative
infrastructure config is Terraform in the `fieldkit/infra` repo; anything here that
sounds like a current value (instance sizes, desired counts) lives there.

The account directory (an account that isn't listed here means this doc has drifted —
flag it):

| Environment | AWS account | Atlas runs as | Storefront |
|---|---|---|---|
| production | `fieldkit-prod` | ECS cluster `atlas-prod`, services `web` / `worker` / `beat` | `fieldkit.com` on Vercel, from `main` |
| staging | `fieldkit-staging` | ECS cluster `atlas-staging`, same services | Vercel preview deployments, per PR |
| ci | `fieldkit-ci` | no workloads — GitHub Actions runners and the ECR registry both environments pull from | — |

AWS runtime names follow `<system>-<env>` across clusters, databases, and queues
(`atlas-prod`, `atlas-prod-db`); S3 buckets are `fieldkit-<env>-*`. Substituting
`staging` for `prod` usually derives a name's sibling — the database replica is the
known exception ([database](./atlas/database.md)).

How each system participates:

- **atlas** runs in both accounts with the same topology; staging deploys first on every
  merge and is the canary ([deployment](./atlas/deployment.md)). Staging data is a
  scrubbed weekly snapshot of production — real shape, no customer PII.
- **storefront** has no staging account: Vercel preview deployments per PR are its
  staging, and production is the `main` branch. It holds no customer data of its own.

Telling environments apart: staging URLs carry the `staging.` prefix
(`app.staging.fieldkit.com`), staging ECS clusters carry the `-staging` suffix, and
every atlas log line carries an `env` field. Dashboards don't span the two: Datadog is
a separate account per environment, so each account sees only its own.
