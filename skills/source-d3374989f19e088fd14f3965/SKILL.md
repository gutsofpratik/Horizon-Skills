---
name: privatelink
description: Use when the user wants to list available PrivateLink endpoint services, list/create/delete PrivateLink endpoints for a project, or manage the endpoint whitelist on Zilliz Cloud.
---

## Prerequisites

1. CLI installed and logged in (see setup skill).
2. A project to attach endpoints to (see project-region skill).

## Commands Reference

### List available PrivateLink endpoint services

```bash
zilliz privatelink list-services
# Optional: --region-id <filter-by-cloud-region>
```

### List Privatelinks

```bash
zilliz privatelink list --project-id <project-id>
```

### Create a Privatelink

```bash
zilliz privatelink create \
  --project-id <project-id> \
  --region-id <cloud-region> \
  --endpoint-id <vpc-endpoint-id>
# Optional: --gcp-project-id <gcp-project-id>
```

### Delete a Privatelink

```bash
zilliz privatelink delete --project-id <project-id> --endpoint-id <endpoint-id-to-delete>
```

### Add region to PrivateLink endpoint whitelist

```bash
zilliz privatelink add-whitelist --project-id <project-id> --region-id <cloud-region-to-whitelist>
```

## Guidance

- PrivateLink lets a cluster be reached over a cloud-provider private network (AWS PrivateLink, GCP Private Service Connect, Azure Private Link) instead of the public internet. Endpoints are scoped to a project and a region.
- Workflow for a new endpoint:
  1. `zilliz privatelink list-services --region-id <region>` to find the `endpointService` value for that region (and whether `whitelistRequired` is true).
  2. If `whitelistRequired` is true, call `zilliz privatelink add-whitelist --project-id <id> --region-id <region>` first so the project is allowed to attach an endpoint in that region.
  3. Create the VPC endpoint in your own cloud account (out-of-band, in the AWS/GCP/Azure console or via IaC) and capture its endpoint ID (e.g. `vpce-xxxx`).
  4. Register it with `zilliz privatelink create --project-id <id> --region-id <region> --endpoint-id <vpce-id>`. For GCP, also pass `--gcp-project-id <gcp-project>`.
- `list` is per-project: `zilliz privatelink list --project-id <id>`. There is no global listing.
- `delete` is irreversible -- always confirm with the user, especially in production. Existing connections from that endpoint stop working immediately.
- After enabling PrivateLink for a cluster, the cluster's endpoint URL switches to the private DNS form. Re-run `zilliz cluster describe --cluster-id <id>` to fetch the updated endpoint and update any consumer config.
