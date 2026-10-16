---
name: project-region
description: Use when the user wants to manage Zilliz Cloud projects or storage volumes. For cloud regions and providers, see the cluster skill.
---

## Prerequisites

1. CLI installed and logged in (see setup skill).

## Commands Reference

### Projects

#### Create a Project

```bash
zilliz project create --name <project-name> --plan <Standard|Enterprise|BusinessCritical>
# Optional: --region '[...]'
```

#### List Projects

```bash
zilliz project list
```

#### Describe a Project

```bash
zilliz project describe --project-id <project-id>
```

#### Delete a Project

```bash
zilliz project delete --project-id <project-id>
```

#### Upgrade a Project

```bash
zilliz project upgrade --project-id <project-id> --plan <Standard|Enterprise|BusinessCritical>
```

#### Bind additional regions to an existing project

```bash
zilliz project add-regions --project-id <project-id> --region '[...]'
```

### Volumes

#### Create a Volume

```bash
zilliz volume create \
  --project-id <project-id> \
  --region <cloud-region> \
  --name <volume-name>
```

#### List Volumes

```bash
zilliz volume list --project-id <project-id>
# Pagination: --page-size <n> --page <n>
# Fetch all pages: --all
```

#### Delete a Volume

```bash
zilliz volume delete --name <volume-name-to-delete>
```

#### Describe a Volume

```bash
zilliz volume describe --name <volume-name>
```

#### Apply

```bash
zilliz volume apply --name <volume-name>
# Optional: --project-id <project-id>
```

## Guidance

- When the user wants to create a cluster, they need a project ID and region ID first. Guide them through `zilliz project list` and `zilliz cluster regions` (see cluster skill).
- Project `upgrade` does not include `Free` as a valid target plan -- only Serverless, Standard, and Enterprise.
- Before deleting a volume, confirm with the user.
