# Auto-Scaling Reference

Three scaling modes for Dedicated clusters: Manual, Scheduled, Dynamic.

## When to Scale CU vs Replica

| Goal | Scale What | Trigger Signal |
|------|-----------|---------------|
| More capacity (data/collections) | Query CU | CU Capacity >80%, write failures |
| More throughput (QPS) | Replica | CU Computation >60%, QPS bottleneck |

Rule of thumb:
- **1-8 CUs**: Scale CU directly
- **>8 CUs**: Add replicas for throughput

## Constraints

- CU × Replica ≤ 1024 (Enterprise), ≤ 32 (Standard)
- Replica >1 requires minimum 8 CUs
- Scale-down requires: data volume < 80% of new capacity + collections within new limits
- During scaling: cluster status = "Modifying", no other operations allowed

## 1. Manual Scaling

### Console
Cluster Details → Scale → adjust CU or Replica count.

### REST API
```bash
# Scale CU
curl -X POST "${BASE_URL}/v2/clusters/${CLUSTER_ID}/modify" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"cuSize": 4}'

# Scale Replica
curl -X POST "${BASE_URL}/v2/clusters/${CLUSTER_ID}/modify" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"replica": 2}'
```

## 2. Dynamic Scaling

Auto-adjusts within a min/max range based on real-time metrics.

**Available for**: Enterprise plan Dedicated clusters.

### CU Dynamic Scaling
- **Metric**: CU Capacity
- **Scale Up**: Capacity >80% for 10 min (or >100% immediately)
- **Scale Down**: Capacity <60% for 30 min
- **Target**: Maintains ~70% capacity
- **Cooldown**: 10 min (up), 30 min (down)

### Replica Dynamic Scaling
- **Metric**: CU Computation
- **Scale Up**: Computation >60% for 2 min
- **Scale Down**: Computation <40% for 10 min
- **Target**: Maintains ~50% computation
- **Max replica**: 10

### Formula
```
Target = Current × (Current Metric / Target Metric)
# Rounded up to next valid size
```

### REST API
```bash
curl -X POST "${BASE_URL}/v2/clusters/${CLUSTER_ID}/modify" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "autoscaling": {
        "cu": {"min": 4, "max": 32},
        "replica": {"min": 1, "max": 4}
    }
}'
```

## 3. Scheduled Scaling

Cron-based rules for predictable traffic patterns.

**Available for**: Enterprise plan Dedicated clusters.

### Basic Mode
Console UI with simple time/day selector.

### Advanced Mode (Cron)
Standard cron expressions for complex schedules.

Interval between schedules must be >30 minutes.

### Examples
```bash
# Weekday peak hours: scale to 8 CU at 9am, back to 2 CU at 6pm
curl -X POST "${BASE_URL}/v2/clusters/${CLUSTER_ID}/modify" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "autoscaling": {
        "cu": {
            "schedules": [
                {"cron": "0 9 * * 1-5", "target": 8},
                {"cron": "0 18 * * 1-5", "target": 2}
            ]
        }
    }
}'
```

**Note**: `autoscaling.cu` and `cuSize` are mutually exclusive. Same for `autoscaling.replica` and `replica`.

## Decision Guide

```
Workload pattern?
├── Predictable (daily peaks, batch windows) → Scheduled Scaling
├── Unpredictable (variable traffic) → Dynamic Scaling
└── Known one-time change → Manual Scaling
```

## Important Notes

- Scaling settings are NOT included in backups — reconfigure after restore
- Scaling typically completes within a few minutes
- Multiple scaling tasks processed sequentially by trigger timestamp
- BYOC clusters support the full auto-scaling suite
- Auto-scaling operates at the **cluster level**, not at the collection level

## Docs

- [Scale Cluster Overview](https://docs.zilliz.com/docs/scale-cluster)
- [Scale Query CU](https://docs.zilliz.com/docs/scale-query-cu)
- [Scale Replica](https://docs.zilliz.com/docs/manage-replica)
- [Cron Expression](https://docs.zilliz.com/docs/cron-expression)
- [Modify Cluster API](https://docs.zilliz.com/reference/restful/modify-cluster-v2)
