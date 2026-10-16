# Atlas deployment

How a merged PR becomes running production code. The short version: GitHub Actions
builds one image, staging deploys immediately, and production ships only after the
staging smoke tests pass — continuous deployment, no manual step, usually under twenty
minutes from merge (the workflow file carries current timings; trust it over any number
here).

Authoritative detail lives in `.github/workflows/deploy.yml` and the Terraform in
`fieldkit/infra`. This file is the operational shape.

## The sequence

1. **Build.** One workflow run builds the `atlas` image and pushes it to ECR in the
   `fieldkit-ci` account, tagged with the commit SHA.
2. **Staging deploys early, on purpose.** The staging ECS services update as soon as the
   image exists — before the full test matrix finishes. Staging is the canary.
3. **Migrations run before each environment's service update**, via a one-off ECS task,
   and production's migration step additionally waits for staging's — a migration never
   runs in production without having run in staging first.
4. **Production gates on everything**: the test matrix, the staging deploy, and smoke
   tests that run against the *deployed* staging.

## Rollback and hotfixes

- **Rollback** is `scripts/rollback <sha>` in the atlas repo: it re-points the ECS
  services at a previous image tag without rebuilding. It does not revert migrations —
  the runbook "Rolling back a bad deploy" owns when that matters.
- **Hotfixes** use the `hotfix` PR label: the deploy workflow skips the non-critical
  test matrix and goes straight to the gated sequence.
- **Pausing deploys** is a repository environment protection rule (the `production`
  environment in GitHub settings); when it's on, deploy runs queue rather than fail —
  a stack of queued "waiting for approval" runs is the deploys-are-paused signal.

## Reading a slow or odd deploy

ECS rolls one service at a time and drains connections, so `web` visibly lags the image
push by a few minutes; `beat` moves last (one task, stop-then-start, so the scheduler
blips — duplicate-suppression on scheduled jobs covers the gap). Two merges close
together queue as two full runs; the newer one does not preempt the older. Every deploy
posts to `#deploys` and creates a Datadog event, which is what "did something change?"
queries against — and every log line carries the `git_sha` field, so whether an error
spans a deploy boundary is answerable from logs directly.
