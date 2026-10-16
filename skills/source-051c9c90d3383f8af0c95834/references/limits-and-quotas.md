# Zilliz Cloud Limits and Quotas

Quick reference for resource limits across different cluster types.

## Organization & Project Limits

| Resource | Limit |
|----------|-------|
| Organizations per user | 1 (auto-created) |
| Projects per organization | 100 |
| Users per organization | 100 |
| Users per cluster | 100 |
| Customized API keys per org | 100 |

## Cluster Limits by Type

| Limit | Free | Serverless | Dedicated (Standard) | Dedicated (Enterprise) |
|-------|------|------------|----------------------|------------------------|
| Storage | 5 GB | Unlimited | Unlimited | Unlimited |
| Max CUs | N/A | N/A | 32 | 1,024 |
| Collections/Partitions per CU | N/A | N/A | 1,024 / 4,096 | 1,024 / 4,096 |
| Max partitions per collection | 1,024 | 1,024 | 1,024 | 1,024 |

## Operation Limits

| Operation | Free/Serverless | Dedicated |
|-----------|-----------------|-----------|
| Insert/Upsert request size | 64 MB | 64 MB |
| Search nq (number of queries) | ≤ 10 | ≤ 16,384 |
| Search/Query response entities | ≤ 1,024 | ≤ 16,384 |

> **Note**: For results exceeding 16,384 entities, use Search Iterators.

## Import Limits

| Source | Limit |
|--------|-------|
| Local file upload | 1 GB |
| Cloud storage (S3/GCS/Azure) total | 1 TB |
| Single file from cloud storage | 10 GB |

## Backup & Retention

| Type | Retention |
|------|-----------|
| Manual backups | Permanent |
| Automatic backups | Max 30 days |

## Index Constraints

- Only **one index per field** allowed
- Must release index before dropping
- Supported metric types: `COSINE`, `L2`, `IP`, `JACCARD`, `HAMMING`

## API Key Permissions

| Role | Scope |
|------|-------|
| Organization Owner | Full admin access to all resources |
| Project Admin | Full control of assigned projects |
| Project Read-Write | Read/write on assigned projects |
| Project Read-Only | View-only on assigned projects |

## Multi-Tenancy with Partition Key

For multi-tenant applications:
- Designate a scalar field as partition key with `is_partition_key=True`
- Default: 16 partitions (customizable via `num_partitions`)
- Partition key values cannot be empty or null
- Enable `partitionkey.isolation=true` for better performance (requires single-value filter)

---

## Quick Troubleshooting

| Issue | Likely Cause | Solution |
|-------|--------------|----------|
| "nq too large" | Exceeded search batch limit | Split into smaller batches (≤10 for Free/Serverless) |
| "too many entities" | Response limit exceeded | Use pagination or iterators |
| "insert failed" | Request > 64MB | Split data into smaller batches |
| "partition limit" | >1024 partitions | Consolidate or use partition key |
