# Cluster Selection Guide

Help users choose the right Zilliz Cloud plan based on their requirements.

## Table of Contents

1. [Plan Hierarchy](#plan-hierarchy)
2. [Quick Selection Decision Tree](#quick-selection-decision-tree)
3. [Plan Comparison Matrix](#plan-comparison-matrix-official)
4. [Cluster Types](#cluster-types-within-dedicated-plans)
5. [Scenario-based Recommendations](#scenario-based-recommendations)
6. [Feature Availability](#feature-availability)
7. [Cost Optimization Tips](#cost-optimization-tips)

## Plan Hierarchy

Zilliz Cloud offers 6 service plans:

| Plan | Description |
|------|-------------|
| **Free** | Learning, prototyping (5GB, GCP only, 1 per org) |
| **Serverless** | Variable traffic, pay-per-use, auto-scale |
| **Dedicated Standard** | Non-critical workloads, testing environments |
| **Dedicated Enterprise** | Production applications, enterprise-grade reliability |
| **Business Critical** | Regulated industries (healthcare, finance), maximum resilience |
| **BYOC** | Custom infrastructure in user's VPC |

## Quick Selection Decision Tree

```
Start Here
│
├── Learning/Prototyping? → Free
│
├── Variable/unpredictable traffic? → Serverless
│
├── Production workload?
│   │
│   ├── Non-critical / testing → Dedicated Standard
│   │
│   ├── Mission-critical?
│   │   ├── Standard compliance → Dedicated Enterprise
│   │   └── HIPAA/regulated → Business Critical
│   │
│   └── Data must stay in user's VPC → BYOC
│
└── Need tiered storage for large datasets?
    └── Dedicated Enterprise or Business Critical with Tiered-storage cluster type
```

---

## Plan Comparison Matrix (Official)

### Deployment & Infrastructure

| Feature | Free | Serverless | Standard | Enterprise | Business Critical | BYOC |
|---------|------|------------|----------|------------|-------------------|------|
| Environment | Shared | Shared | Dedicated | Dedicated | Dedicated | User VPC |
| Cloud Providers | AWS, GCP | AWS, GCP | AWS, GCP, Azure | AWS, GCP, Azure | AWS, GCP, Azure | User choice |
| Max Query CUs | Single | Auto-scale | 32 | 1,024 | 256 | Customizable |
| Max Collections | 5 | 10/cluster | Per limits | Per limits | Per limits | Customizable |

### High Availability

| Feature | Free | Serverless | Standard | Enterprise | Business Critical | BYOC |
|---------|------|------------|----------|------------|-------------------|------|
| Multiple AZs | ✗ | ✗ | ✓ | ✓ | ✓ | ✓ |
| Replica Support | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Snapshots | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Global Cluster | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ |
| Uptime SLA | 99.95% | 99.99%* | 99.95% | Standard terms | Standard terms | Per agreement |

*Multi-replica

### Security & Compliance

| Feature | Free | Serverless | Standard | Enterprise | Business Critical | BYOC |
|---------|------|------------|----------|------------|-------------------|------|
| OAuth 2.0 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| MFA | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Data Encryption | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| SOC 2 / ISO 27001 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Audit Logs | ✗ | ✗ | ✓ | ✓ | ✓ | ✓ |
| IP Whitelist | ✗ | ✗ | ✓ | ✓ | ✓ | ✓ |
| Enterprise SSO | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ |
| CMEK | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ |
| Private Link | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ |
| HIPAA Ready | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ |

### Support & Response

| Feature | Free | Serverless | Standard | Enterprise | Business Critical | BYOC |
|---------|------|------------|----------|------------|-------------------|------|
| On-call | Business hours | Business hours | 24/7/365 | 24/7/365 | 24/7/365 | 24/7/365 |
| Emergency Response | 30 min | 4 hours | 1 hour | 1 hour | 1 hour | 1 hour |
| Email/Ticket | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Slack Channel | ✗ | ✗ | ✓ | ✓ | ✓ | ✓ |
| Assigned Engineer | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ |

### Data Resilience & Backup

| Feature | Free | Serverless | Standard | Enterprise | Business Critical | BYOC |
|---------|------|------------|----------|------------|-------------------|------|
| Automatic Backup | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Manual Snapshot | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Cross-Region Backup | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ |

**RPO (Recovery Point Objective):**

| Tier | Backup Type | RPO | Write Strategy |
|------|-------------|-----|----------------|
| Standard | Local backup | Hourly | Single AZ, WAL Quorum replicated |
| Enterprise | Local backup | Hourly | Cross-AZ writes, WAL Quorum replicated |
| Enterprise Multi-Replica | Local + Cross-region | Hourly | Cross-AZ writes |
| Cross-Region HA | Multi-region replicated | ≤10 seconds | Multi-region sync |

**RTO (Recovery Time Objective):**
- Full backup restore: Minutes to hours (depends on data size)
- Automatic failover (node/AZ failure): ≤1 minute

**Data Durability:**
- Object storage inherits native HA from cloud provider
- Multi-replica architecture with primary/standby at shard level

---

## Cluster Types (within Dedicated Plans)

Within Dedicated plans (Standard, Enterprise, Business Critical), choose a cluster type.

> **Pricing Note:** 1 CU is the minimum billing unit and cannot be subdivided. All pricing is calculated in whole CU increments.

### Performance-optimized

**Choose when:**
- Latency is critical (<20ms)
- High QPS requirements (500-1500 QPS)
- Smaller datasets (<50M vectors)
- Real-time applications

**Specs per CU:**
- 1.5M vectors (768-dim)
- 500-1,500 QPS
- ~10ms latency

**Cost formula:**
```
Monthly = CUs × $0.185/hour × 730 + Storage_GB × $0.025
```

**Starting price:** 1 CU × $0.185 × 730 = **$135/month** (compute only)

### Capacity-optimized

**Choose when:**
- Cost efficiency is priority
- Moderate latency acceptable (50-100ms)
- Large datasets (50M-200M vectors)
- Batch processing or analytics

**Specs per CU:**
- 5M vectors (768-dim)
- 100-300 QPS
- 50-100ms latency

**Cost formula:**
```
Monthly = CUs × $0.185/hour × 730 + Storage_GB × $0.025
```

**Starting price:** 1 CU × $0.185 × 730 = **$135/month** (compute only)

### Tiered-storage (Enterprise / Business Critical)

**Choose when:**
- Very large datasets (>200M vectors)
- Clear hot/cold access pattern by recency
- Cost optimization is critical
- Can tolerate higher latency for cold data

**Specs per CU:**
- 20M vectors (768-dim)
- Hot: 100-150 QPS, 20-40ms
- Cold: 5-20 QPS, 200-1000ms

**Minimum requirement:** 8 Query CUs

**Cost formula (AWS us-east-1):**
```
Monthly = CUs × $0.278/hour × 730 + Storage_GB × $0.04 + Cold_access × $0.0005/GB
```

**Starting price:** 8 CU × $0.278 × 730 = **$1,623/month** (compute only, minimum 8 CUs required)

⚠️ **Important**: Tiered-storage tiers data by **access recency**, NOT by field. You cannot manually assign specific fields to hot/cold tiers.

---

## Scenario-based Recommendations

### Scenario 1: RAG Chatbot (Startup)

**Requirements:**
- 1M documents
- 768-dim vectors
- Production use
- Budget-conscious

**Recommendation:** `Dedicated Enterprise` (Performance-optimized)
- 1 CU handles 1.5M vectors — perfect fit for 1M docs
- Auto-scaling available for traffic spikes
- Full enterprise features (Private Link, CMEK, auto-scaling)
- Est. cost: ~$135/month (1 CU)
- Start with Free cluster + trial credits to validate, then upgrade to Dedicated

### Scenario 2: E-commerce Search

**Requirements:**
- 10M products
- Low latency (<30ms)
- Steady traffic
- 1000 QPS peak

**Recommendation:** `Dedicated Performance-optimized`
- 7 CUs (10M ÷ 1.5M/CU)
- Est. cost: ~$950/month

### Scenario 3: Document Archive

**Requirements:**
- 500M documents
- 768-dim vectors
- 80% rarely accessed
- Cost is primary concern

**Recommendation:** `Dedicated Enterprise` with Tiered-storage cluster
- 25 CUs (500M ÷ 20M/CU)
- Est. cost: ~$5,100/month (list price)
- Savings vs Performance: ~75%

### Scenario 4: Multi-modal Search

**Requirements:**
- 100M items
- Multiple vector fields (image + text)
- Total 2048 dimensions (512 + 1536)
- Mixed access patterns

**Recommendation:** `Dedicated Enterprise` with Tiered-storage cluster
- All fields stored together (tiered-storage auto-tiers by access recency, NOT by field)
- Effective vectors: 100M × (2048/768) = 267M equivalent 768-dim vectors
- CUs needed: ~14 CUs
- Est. cost: ~$3,000/month (list price)

> ⚠️ **Note:** You cannot store image vectors in hot tier and text vectors in cold tier separately. Tiered-storage tiers entire entities based on access pattern. If you need true field-level separation, consider separate clusters.

### Scenario 5: Healthcare Application

**Requirements:**
- HIPAA compliance required
- Production-critical
- Private network access

**Recommendation:** `Business Critical` or `BYOC`
- HIPAA Ready certification
- Private Link for network isolation
- CMEK for encryption key control
- Contact Sales for compliance documentation

---

## Cost Optimization Tips

### 1. Right-size your cluster

```
Required CUs = Total_vectors / Vectors_per_CU

# Adjust for dimensions
If dims ≠ 768:
  Effective_vectors = Actual_vectors × (dims / 768)
```

### 2. Use tiered storage for hot/cold data

If >30% of data is rarely accessed, tiered-storage often saves money:

| Scenario | Performance | Tiered-storage | Savings |
|----------|-------------|----------------|---------|
| 100M vectors, all hot | $4,333/mo | $1,421/mo | - |
| 100M vectors, 70% cold | $4,333/mo | $1,421/mo | 67% |

### 3. Consider Serverless for variable workloads

Serverless wins when:
- Usage <50% of provisioned capacity
- Traffic is highly variable
- Development/staging environments

### 4. Optimize vector dimensions

| Dimension | Storage/vector | Impact |
|-----------|----------------|--------|
| 384 | 1.5 KB | 50% of 768-dim cost |
| 768 | 3 KB | Baseline |
| 1536 | 6 KB | 2x cost |

Consider dimensionality reduction (PCA, Matryoshka) for cost savings.

---

## Migration Path

```
Free → Serverless → Dedicated Standard → Dedicated Enterprise → Business Critical
  ↑        ↑              ↑                    ↑                      ↑
Learning  Variable    Non-critical        Production             Regulated
          traffic      workloads         applications           industries
```

Migrations between plans are supported. Contact Support for assistance.

---

## Quick Reference: When to Use Each

| Use Case | Plan |
|----------|------|
| POC / Demo | Free cluster + trial credits |
| Hackathon / Side project | Free or Serverless |
| Dev / Staging | Serverless or Dedicated Standard |
| SaaS MVP | Dedicated Enterprise |
| Production API | Dedicated Enterprise |
| Enterprise SaaS | Dedicated Enterprise |
| Large-scale (>200M vectors) | Dedicated Enterprise + Tiered-storage |
| HIPAA / Compliance | Business Critical |
| Data in user's VPC | BYOC |

---

---

## Feature Availability

Features have different maturity stages:

| Stage | Description | Access |
|-------|-------------|--------|
| **GA** | Production-ready, fully supported | Default |
| **Public Preview** | Close to production-ready | Upgrade cluster version |
| **Private Preview** | Under active development | Contact Support |
| **Deprecation Notice** | No longer actively developed | Migrate to alternatives |

### Current Feature Status

**Private Preview** (Contact Support to request access):
- ETL (Extract, Transform & Load)
- Zero downtime migration
- Export backup files
- Hosted models

**Public Preview** (Upgrade cluster Milvus version):
- Embedding and Rerank Functions

**Deprecation Notice** (Migrate to alternatives):
- Import Data from NumPy Files
- RESTful APIs V1
- ~~Pipelines~~ — **DEPRECATED**. Replaced by hosted models and third-party model API key integrations. NEVER mention Pipelines to users.

### How to Request Access

For **Private Preview** features:
1. Submit request at https://support.zilliz.com/hc/en-us/requests/new
2. Include: Feature name, use case, expected usage volume
3. Zilliz team will review and enable if approved

For **Public Preview** features:
1. Upgrade cluster to latest Milvus version in Console
2. If unable to upgrade, contact Support

---

## Pricing Note

All cost estimates in this document are based on **public list prices**.

For personalized pricing options (volume discounts, committed use, enterprise agreements), the Sales team can help tailor a solution: https://zilliz.com/contact-sales
