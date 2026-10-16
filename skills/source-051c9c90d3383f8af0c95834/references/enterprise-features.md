# Enterprise Features

Advanced features for Enterprise clusters on Zilliz Cloud.

## Table of Contents

1. [Tiered Storage](#tiered-storage)
2. [Multi-Vector Collections](#multi-vector-collections)
3. [Advanced Security](#advanced-security)
4. [Performance Optimization](#performance-optimization)
5. [Enterprise Support](#enterprise-support)

---

## Tiered Storage

Automatically optimize storage costs by tiering data based on **access recency** (not by field).

### How Tiered Storage Works

```
┌─────────────────────────────────────────────────┐
│                  Query Layer                     │
├─────────────────────────────────────────────────┤
│  Hot Tier      │  Warm Tier     │  Cold Tier    │
│  (Memory+SSD)  │  (SSD)         │  (Object)     │
│  20-40ms       │  ~100ms        │  200-1000ms   │
│  $$$           │  $$            │  $            │
└─────────────────────────────────────────────────┘

Data moves between tiers automatically based on ACCESS RECENCY.
Recently accessed data → Hot tier
Older/rarely accessed data → Cold tier
```

⚠️ **Critical Limitation**: You CANNOT manually assign specific fields to hot/cold tiers. Tiered-storage tiers **entire entities** based on when they were last accessed, not by field type.

### When to Use Tiered Storage

| Scenario | Recommended | Why |
|----------|-------------|-----|
| >200M vectors with clear hot/cold access pattern | ✓ Yes | Significant cost savings |
| Recent data accessed frequently, old data rarely | ✓ Yes | Natural fit for recency-based tiering |
| Need different fields in different tiers | ✗ No | Not supported - use separate clusters |
| Latency-critical for all data | ✗ No | Cold tier has 200-1000ms latency |

### Tiered Storage Specs

- **Minimum**: 8 Query CUs
- **Capacity**: 20M vectors per CU (768-dim)
- **Hot tier**: 100-150 QPS, 20-40ms latency
- **Cold tier**: 5-20 QPS, 200-1000ms latency

### Cost Formula (AWS us-east-1)

```
Monthly = (CUs × $0.278/hour × 730) + (Storage_GB × $0.04) + (Cold_access_GB × $0.0005)
```

### Common Misconception

❌ **Wrong**: "I'll put my 128-dim vectors in hot tier and 512-dim vectors in cold tier"
✅ **Reality**: All fields of an entity are stored together. The entire entity moves between tiers based on access recency.

**If you need true field-level separation:**
1. Create separate clusters for different access patterns
2. Accept data duplication between clusters
3. Route queries to appropriate cluster based on use case

---

## Multi-Vector Collections

Store multiple vector representations per entity for different use cases.

### Schema Design

```python
schema = MilvusClient.create_schema(auto_id=True)
schema.add_field("id", DataType.INT64, is_primary=True)

# Multiple vector fields for different purposes
schema.add_field("title_vector", DataType.FLOAT_VECTOR, dim=384)
schema.add_field("content_vector", DataType.FLOAT_VECTOR, dim=768)
schema.add_field("image_vector", DataType.FLOAT_VECTOR, dim=512)

# Sparse vector for keyword matching
schema.add_field("bm25_vector", DataType.SPARSE_FLOAT_VECTOR)
```

### Hybrid Search Across Vectors

```python
from pymilvus import AnnSearchRequest, RRFRanker

# Search title vectors
title_req = AnnSearchRequest(
    data=[title_query],
    anns_field="title_vector",
    param={"metric_type": "COSINE"},
    limit=20
)

# Search content vectors
content_req = AnnSearchRequest(
    data=[content_query],
    anns_field="content_vector",
    param={"metric_type": "COSINE"},
    limit=20
)

# Combine with RRF ranking
results = client.hybrid_search(
    collection_name="documents",
    reqs=[title_req, content_req],
    ranker=RRFRanker(k=60),
    limit=10,
    output_fields=["title", "content"]
)
```

---

## Advanced Security

### RBAC (Role-Based Access Control)

> **Note**: RBAC is available on **all plans** (Free, Serverless, Dedicated). Not an Enterprise-only feature.

```python
from pymilvus import Role, utility

# Create custom role
role = Role("analyst")
role.create()

# Grant collection-level permissions
role.grant("Collection", "reports", "Search")
role.grant("Collection", "reports", "Query")

# Assign role to user
role.add_user("analyst_user")
```

### Network Isolation

- **Private Link**: Connect via AWS PrivateLink or GCP Private Service Connect
- **IP Whitelisting**: Restrict access to specific IPs/CIDRs
- **VPC Peering**: Direct connection to your VPC

### Data Encryption

- **At rest**: AES-256 encryption (default)
- **In transit**: TLS 1.2+ (required)
- **Customer-managed keys (CMEK)**: Business Critical only

---

## Performance Optimization

### Index Tuning for Enterprise

```python
# AUTOINDEX with performance hints
index_params = MilvusClient.prepare_index_params()
index_params.add_index(
    field_name="vector",
    index_type="AUTOINDEX",
    metric_type="COSINE",
    params={
        "index_mode": "high_recall"  # or "balanced", "high_performance"
    }
)
```

### Query Optimization

```python
# Use partition key for query isolation
schema.add_field(
    "region",
    DataType.VARCHAR,
    max_length=50,
    is_partition_key=True  # Automatic partition pruning
)

# Queries automatically route to relevant partitions
results = client.search(
    collection_name="global_data",
    data=[query_vector],
    filter="region == 'us-east'",  # Only scans us-east partition
    limit=10
)
```

### Resource Scaling

- **Horizontal scaling**: Add more query nodes for throughput
- **Vertical scaling**: Increase CU for larger datasets
- **Auto-scaling**: Configure scaling policies based on metrics

---

## Enterprise Support

### SLA Guarantees

| Tier | Availability | Response Time |
|------|--------------|---------------|
| Standard | 99.9% | 24h |
| Premium | 99.95% | 4h |
| Enterprise | 99.99% | 1h (critical) |

### Support Channels

- **Dedicated Slack channel**: Real-time support
- **Priority ticket queue**: Faster resolution
- **Technical Account Manager**: Strategic guidance
- **Quarterly business reviews**: Performance optimization

### Getting Enterprise Access

1. Contact sales: https://zilliz.com/contact-sales
2. Schedule architecture review
3. Proof of concept with production-like data
4. Custom contract negotiation
