# Atlas database

Two Postgres databases per environment, hosted on RDS, named `atlas-<env>-<name>` —
staging substitutes `staging` for `prod` in every name below, and runs no replica:

| Database | Holds |
|---|---|
| `atlas-prod-db` (+ replica `atlas-prod-db-replica-1`) | The product: all OLTP tables |
| `atlas-prod-timeseries` | Device telemetry readings, partitioned by day — heavy writes, never joined to the product schema |

The application connects through PgBouncer, run as its own ECS service per environment
(transaction pooling), so Postgres connection counts stay flat as `web` and `worker`
scale — a connection-count alarm firing means something is bypassing the pooler. Instance classes and storage live
in `fieldkit/infra/rds/atlas.tf`; read current sizes there.

## How the application uses it

- Django's default connection goes to the writer. The replica serves the reporting
  endpoints and the nightly export jobs only — routed explicitly via Django's database
  router in `atlas/db/routers.py`, not automatically. Replica lag therefore affects
  reports, never the product's own read-after-write.
- Roles: `atlas_app` (the application), `atlas_migrate` (DDL, used only by the migration
  task), `atlas_readonly` (humans and the BI tool). An unfamiliar role in
  `pg_stat_activity` is a finding — either this doc has drifted or something unexpected
  is connecting; both are worth flagging.

## Migrations

Django migrations, in-repo, run as a one-off ECS task before each deploy's service
update ([deployment](./deployment.md)). Long-running DDL is the known trap: anything
that rewrites a large table goes through the online-migration checklist in the atlas
repo's `docs/migrations.md` first. Lock contention from a migration is owned by the
runbook "Postgres lock contention".

## Backup and restore

RDS automated snapshots with a 14-day window (`fieldkit/infra/rds/atlas.tf` owns the
retention — trust it over this number), plus a nightly logical dump to
`fieldkit-prod-exports/pg/`. The lever for point-in-time recovery is RDS PITR into a
new instance — a decision with hours of consequence, owned by the runbook "Restoring
Postgres from backup", never improvised.
