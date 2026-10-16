# Global Cluster Reference

Cross-region disaster recovery and low-latency reads for mission-critical applications.

## Prerequisites

- **Plan**: Business Critical project only
- **Role**: Project Admin required
- **Cluster**: Dedicated clusters only

## Architecture

```
Global Cluster
├── Primary Cluster (Region A) — handles all writes + reads
├── Secondary Cluster (Region B) — read-only, auto-replicated
├── Secondary Cluster (Region C) — read-only, auto-replicated
└── ... up to 5 secondaries
```

**Global Endpoint**: Single URL for your application. Routes writes → primary, reads → nearest.

## Create a Global Cluster

### Option 1: New cluster
Console → Create Cluster → Enable "Global Cluster" toggle → Name it → Add primary + secondary regions.

### Option 2: Convert existing cluster
Console → Cluster Details → Manage Cluster → "Convert to Global Cluster".

### Via REST API
See [Create Global Cluster](https://docs.zilliz.com/docs/create-global-cluster) for API details.

## Connect

```python
from pymilvus import MilvusClient

# Use the global endpoint for automatic routing
client = MilvusClient(
    uri="YOUR_GLOBAL_ENDPOINT",  # Not the public endpoint
    token="YOUR_API_KEY"
)
```

**When to use which endpoint**:
- **Global endpoint**: DR + HA scenario — automatic write/read routing
- **Public endpoint**: Data replication between environments (e.g., prod → test in same region)

## Switchover (Planned)

Promotes a secondary to primary after full sync. **Zero data loss (RPO=0)**.

Console → Global Cluster page → Click "Switchover" on target secondary.

After switchover:
- Old primary → "Fenced" status (rejects writes)
- New primary → accepts writes
- Global endpoint auto-updates routing

## Failover (Emergency)

Promotes a secondary after primary region outage. **RPO = sync latency (typically seconds)**.

Manually triggered as a recovery action.

## Comparison

| | Switchover | Failover |
|---|---|---|
| Use case | Planned rotation, compliance | Region outage recovery |
| Trigger | Manual, operational | Manual, emergency |
| RPO | 0 (no data loss) | Sync latency (~seconds) |
| RTO | Near zero | ~minutes |

## Scaling

- **CU scaling**: Scale primary → automatically syncs to all secondaries
- **Replica scaling**: Not supported for global clusters currently

## Limitations

- Max 5 secondary clusters
- Cannot suspend global cluster or its members
- Primary and all secondaries must have same: cloud provider, cluster type, CU count, replica count
- Backup policy configured on primary only (auto-migrates on switchover/failover)
- To drop: remove all secondaries first, then primary

## Billing

Each cluster (primary + each secondary) billed as regular Dedicated cluster:
- Compute costs per cluster
- Storage costs per cluster
- Data transfer costs for replication (primary → secondaries)

## Docs

- [Global Cluster Explained](https://docs.zilliz.com/docs/global-cluster-explained)
- [Create Global Cluster](https://docs.zilliz.com/docs/create-global-cluster)
- [Manage Global Cluster](https://docs.zilliz.com/docs/manage-global-cluster)
