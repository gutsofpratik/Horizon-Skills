# Zilliz Cloud Pricing Reference

## ⚠️ CRITICAL: Pricing Verification Required

**Before mentioning ANY price**:
1. Query Inkeep MCP: `mcp__inkeep__ask-question-about-zilliz-cloud`
2. Add disclaimer with official links

**Official Resources**:
- **Calculator**: https://zilliz.com/pricing#calculator
- **Price List**: https://zilliz.com/pricing/pricing-guide

**Required Disclaimer** (include after every price quote):
> ⚠️ Prices shown are for reference only. For accurate, up-to-date pricing, please check the [Pricing Calculator](https://zilliz.com/pricing#calculator) or [Price List](https://zilliz.com/pricing/pricing-guide).

---

## Pricing Concepts (For User Education)

When users need to understand their bill or how pricing works, explain these concepts:

### Dedicated Clusters: CU-based Pricing

| Component | Description |
|-----------|-------------|
| **Compute (CU)** | Billed hourly based on CU count |
| **Storage** | Billed per GB-month |

**CU capacity by cluster type (768-dim vectors):**

| Type | Vectors/CU | Best For |
|------|------------|----------|
| Performance-optimized | 1.5M | Low latency |
| Capacity-optimized | 5M | Cost efficiency |
| Tiered-storage | 20M | Large datasets with hot/cold pattern |

**Starting Price Reference (AWS us-east-1, compute only):**

| Type | Min CU | Hourly Rate | Monthly Cost |
|------|--------|-------------|--------------|
| Performance-optimized | 1 CU | $0.185/hour | **$135/month** |
| Capacity-optimized | 1 CU | $0.185/hour | **$135/month** |
| Tiered-storage | 8 CU | $0.278/hour | **$1,623/month** |

> **Important:** 1 CU is the minimum billing unit and cannot be subdivided. Storage costs are additional.

### Serverless: vCU-based Pricing

Serverless uses virtual Compute Units (vCU) for pay-per-use billing. You only pay for what you use.

**Unit Price**: $4 per million vCUs

#### Write Operations

| Operation | vCU Cost | Notes |
|-----------|----------|-------|
| Insert | 1 KB data = 0.25 vCU | Data size includes vectors + metadata |
| Delete | 1 entity = 1 vCU | Charged even for non-existent entities |
| Upsert | Insert + Delete combined | Update size + deletion count |
| Import / Bulk Insert | **FREE** | No vCU cost for bulk operations |

**Write Cost Formula**:
```
Write vCUs = (Data_KB × 0.25) + (Delete_Count × 1)
Write Cost = Write vCUs × $4 / 1,000,000
```

**Example**: Insert 3 GB data + delete 100K entities
```
Write vCUs = (3,145,728 KB × 0.25) + (100,000 × 1) = 886,432 vCUs
Write Cost = 886,432 × $4 / 1,000,000 = $3.55
```

#### Read Operations

Read costs depend on data scale, not just request count. Each operation has a minimum of 6 vCUs.

| Factor | Impact |
|--------|--------|
| Minimum per operation | 6 vCU |
| Data scanned | More vectors in collection → more vCU |
| Data returned | More `output_fields` → more vCU |
| Partition filtering | Using `partition_key` reduces vCU |

**Read Cost Reference (1 million search requests)**:

| Collection Size | Dimensions | Approx. vCUs | Approx. Cost |
|-----------------|------------|--------------|--------------|
| 1M vectors | 128-dim | 5M vCUs | **$20** |
| 10M vectors | 768-dim | 55M vCUs | **$220** |
| 10B vectors | 1536-dim | 1,495M vCUs | **$5,980** |

**Optimization tips**:
- Use `partition_key` filter to reduce scanned data (can significantly reduce costs)
- Limit `output_fields` to only needed fields
- Use appropriate `limit` values (don't over-fetch)
- Consider data partitioning strategy for large collections

#### Storage Costs

Storage is billed separately per GB-month. Rates vary by region and cloud provider.

#### When to Choose Serverless

| Scenario | Serverless Advantage |
|----------|----------------------|
| Variable/unpredictable traffic | Pay only for actual usage |
| Development/staging | No idle costs |
| Batch workloads with idle periods | No charges when not querying |
| RAG chatbot with spiky traffic | Auto-scales, cost-efficient |

**Break-even guidance**: If your usage is consistently high (>50% of equivalent Dedicated capacity), Dedicated may be more cost-effective

---

## Add-on Features Billing

### Audit Logs

Billed based on cluster CU size and runtime, NOT log volume.

**Key behaviors**:
- Charged while enabled, even if no logs generated
- Not charged while cluster is Suspended
- Intra-region log forwarding: $0

**Availability**: Standard, Enterprise, Business Critical only

---

## Architecture Limitation

⚠️ **Tiered-storage does NOT support field-level tier assignment.**

Tiered-storage auto-tiers by access recency. All fields of an entity stay together.

**If user wants different fields in different tiers:**
→ Use separate clusters (requires data duplication)

---

## Getting Help

| Need | Resource |
|------|----------|
| Cost estimate | https://zilliz.com/pricing |
| Volume discounts | https://zilliz.com/contact-sales |
| Billing questions | https://support.zilliz.com |
