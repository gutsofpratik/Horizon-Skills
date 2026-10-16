---
name: job
description: Use when the user wants to check the status of an async Cloud Job (backup, restore, migration, import, or clone). Also use when the user wants to wait for a long-running operation to complete.
---

## Prerequisites

1. CLI installed and logged in (see setup skill).
2. A job ID from a previous async operation (backup create, import start, etc.).

## Commands Reference

### Describe a Job

```bash
zilliz job describe --job-id <job-id>
```

## Wait for Completion

The `job describe` command supports a `--wait` flag to poll until the job finishes:

```bash
# Poll until done (default: 5s interval, 30min timeout)
zilliz job describe --job-id <job-id> --wait

# Custom timeout and interval
zilliz job describe --job-id <job-id> --wait --timeout 600 --interval 10
```

## Job Types

| Type             | Triggered By                                          |
| ---------------- | ----------------------------------------------------- |
| BACKUP           | `backup create`                                       |
| RESTORE          | `backup restore-cluster`, `backup restore-collection` |
| IMPORT           | `import start`                                        |
| MIGRATION        | Cloud migration operations                            |
| CLONE_COLLECTION | Collection clone operations                           |

## Job Statuses

| Status      | Meaning                           |
| ----------- | --------------------------------- |
| PENDING     | Job is queued                     |
| IN_PROGRESS | Job is running                    |
| SUCCESSFUL  | Job completed successfully        |
| FAILED      | Job failed (check `reason` field) |
| CANCELING   | Job is being cancelled            |
| CANCELED    | Job was cancelled                 |

## Guidance

- Many control-plane operations are **asynchronous** and return a `jobId`. Suggest using `job describe` to track progress.
- When a job fails, the `reason` field contains the error message. Display it to the user.
- For long-running operations (cluster creation, data migration), suggest using `--wait` so the user doesn't have to poll manually.
- The `--wait` flag shows a live progress spinner. Users can press Ctrl+C to stop waiting without cancelling the job itself.
