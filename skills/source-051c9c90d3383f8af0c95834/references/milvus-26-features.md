# Milvus 2.6 Features on Zilliz Cloud

New capabilities available with Milvus v2.6.x clusters. GA since December 2025.

## How to Enable

Upgrade cluster to Milvus v2.6.x on Cluster Overview page → "Try Preview Features" (before GA) or create new cluster (after GA).

## 1. New Data Types

### Geometry (GEOMETRY)

Store and query spatial shapes — POINT, LINESTRING, POLYGON (and Multi variants). Uses WKT format for input, WKB internally. Coordinates use SRID 4326 (WGS 84) — longitude first, latitude second.

**Use cases**: LBS ("find similar POIs within this city block"), geofencing, routing, map-based apps.

**Spatial operators**: `ST_WITHIN`, `ST_CONTAINS`, `ST_INTERSECTS`, `ST_DWITHIN` (distance in meters)

```python
from pymilvus import MilvusClient, DataType

schema = MilvusClient.create_schema()
schema.add_field("id", DataType.INT64, is_primary=True, auto_id=True)
schema.add_field("vector", DataType.FLOAT_VECTOR, dim=768)
schema.add_field("location", DataType.GEOMETRY)

# Insert with WKT format
client.insert("geo_collection", [
    {"vector": [...], "location": "POINT(13.403683 52.520711)"},
    {"vector": [...], "location": "POLYGON((13.3 52.5, 13.4 52.5, 13.4 52.6, 13.3 52.6, 13.3 52.5))"},
])

# Spatial filter: point-in-polygon
results = client.search(
    collection_name="geo_collection",
    data=[query_vector],
    filter="st_within(location, 'POLYGON((13.3 52.5, 13.5 52.5, 13.5 52.6, 13.3 52.6, 13.3 52.5))')",
    limit=10
)

# Distance-based: within 1000 meters
results = client.query("geo_collection",
    filter="st_dwithin(location, 'POINT(13.403683 52.520711)', 1000.0)",
    output_fields=["id", "location"])
```

Docs: [Geometry Field](https://docs.zilliz.com/docs/use-geometry-field)

### Struct (Array of Structs)

Model nested, multi-attribute records. Key use case: document chunking (one entity holds multiple chunks, each with text + vector). Uses `MAX_SIM` metric family for "late interaction" search.

```python
from pymilvus import MilvusClient, DataType
from pymilvus.client.embedding_list import EmbeddingList

# Define struct schema
struct_schema = client.create_struct_field_schema()
struct_schema.add_field("text", DataType.VARCHAR, max_length=65535)
struct_schema.add_field("text_vector", DataType.FLOAT_VECTOR, dim=768)

schema.add_field("chunks", DataType.ARRAY,
    element_type=DataType.STRUCT,
    struct_schema=struct_schema,
    max_capacity=1000)

# Index on embedded vector — must use MAX_SIM metric
index_params.add_index(field_name="chunks[text_vector]",
    index_type="AUTOINDEX", metric_type="MAX_SIM_COSINE")

# Search with EmbeddingList (multi-vector query)
el = EmbeddingList()
el.add([0.2, 0.9, 0.4, -0.3, 0.2, ...])
results = client.search("docs", data=[el],
    anns_field="chunks[text_vector]",
    search_params={"metric_type": "MAX_SIM_COSINE"},
    limit=3)
```

**Limitations**: max 1000 elements per struct array; metric must be `MAX_SIM_COSINE`/`MAX_SIM_IP`/`MAX_SIM_L2`; scalar fields inside structs not filterable.

Docs: [Array of Structs](https://docs.zilliz.com/docs/use-array-of-structs)

### TimestampTz (TIMESTAMPTZ)

Time-zone-aware timestamps. Accepts ISO 8601 strings, stores internally as UTC.

**Parsing rules**:
- With offset (`2024-12-31T22:00:00+08:00`) → absolute time
- Without offset (`2024-12-31 22:00:00`) → interpreted using collection's configured timezone

```python
schema.add_field("created_at", DataType.TIMESTAMPTZ)

# Insert with ISO 8601
client.insert("events", [
    {"vector": [...], "created_at": "2024-12-31T22:00:00+08:00"},
    {"vector": [...], "created_at": "2024-12-31T22:00:00Z"},
])

# Filter — use ISO '...' syntax for timestamp literals
results = client.search(
    collection_name="events",
    data=[query_vector],
    filter="created_at >= ISO '2024-12-01T00:00:00Z' AND created_at < ISO '2025-01-01T00:00:00Z'",
    limit=10
)

# INTERVAL arithmetic (ISO 8601 Duration: P3D = 3 days, PT2H = 2 hours)
results = client.query("events",
    filter="created_at + INTERVAL 'P3D' > ISO '2025-01-05T00:00:00+08:00'",
    output_fields=["id", "created_at"])
```

Docs: [TIMESTAMPTZ Field](https://docs.zilliz.com/docs/use-timestamptz-field)

### INT8 Vector (INT8_VECTOR)

Store quantized 8-bit integer vectors — lower memory footprint for lightweight inference.

```python
schema.add_field("vector", DataType.INT8_VECTOR, dim=768)
```

Docs: [Dense Vector](https://docs.zilliz.com/docs/use-dense-vector)

## 2. Partial Upserts (Merge Mode)

Update specific fields without rewriting entire records. Unspecified fields keep their original values.

```python
# Only update "issue" field — "title" and "vec" unchanged
client.upsert(
    collection_name="my_collection",
    data=[
        {"id": 1, "issue": "vol.14"},
        {"id": 2, "issue": "vol.7"},
    ],
    partial_update=True  # Key flag: enables merge mode
)
```

**Limitations**: must include primary key; JSON fields always fully overwritten (no merge); if PK doesn't exist, behaves as insert (all required fields needed).

Docs: [Upsert Entities (Merge Mode)](https://docs.zilliz.com/docs/upsert-entities#upsert-in-merge-mode)

## 3. MINHASH_LSH Index

Efficient large-scale deduplication and set similarity using MinHash + Locality-Sensitive Hashing. Data stored as BINARY_VECTOR with metric `MHJACCARD`.

```python
# Requires datasketch library for MinHash generation
from datasketch import MinHash

MINHASH_DIM = 256
HASH_BIT_WIDTH = 64

def generate_minhash(text, num_perm=MINHASH_DIM) -> bytes:
    m = MinHash(num_perm=num_perm)
    for token in text.lower().split():
        m.update(token.encode("utf8"))
    return m.hashvalues.astype('>u8').tobytes()

# Schema: MinHash stored as BINARY_VECTOR
schema.add_field("minhash_sig", DataType.BINARY_VECTOR, dim=MINHASH_DIM * HASH_BIT_WIDTH)

# Index
index_params.add_index(
    field_name="minhash_sig",
    index_type="MINHASH_LSH",
    metric_type="MHJACCARD",
    params={"mh_element_bit_width": HASH_BIT_WIDTH, "mh_lsh_band": 16, "with_raw_data": True}
)

# Search with refined Jaccard
results = client.search("dedup",
    data=[generate_minhash("quick brown fox")],
    anns_field="minhash_sig",
    search_params={"metric_type": "MHJACCARD",
                   "params": {"mh_search_with_jaccard": True, "refine_k": 5}},
    limit=5)
```

**Key params**: `mh_element_bit_width` (32 or 64), `mh_lsh_band` (8-32, higher = more precise), `mh_search_with_jaccard` (enable exact Jaccard refinement).

Docs: [MINHASH_LSH](https://docs.zilliz.com/docs/minhash-lsh)

## 4. Tiered Storage (GA)

Smart data management with hot/warm/cold tiers based on access patterns.

| Tier | Storage | Use Case |
|------|---------|----------|
| **Hot** | Memory (DRAM) | Active queries, lowest latency |
| **Warm** | SSD | Moderate access frequency |
| **Cold** | Object storage (S3/GCS) | Archival, infrequent access |

**Key improvements**:
- >90% cache hit rates
- 25% compute cost reduction
- 87% storage cost reduction ($0.30 → $0.04/GB/month)
- Cold data access billing applies (see [Storage Cost](https://docs.zilliz.com/docs/storage-cost#cold-data-access))

Available on: Tiered-Storage cluster type (Enterprise/Business Critical).

## 5. Schema Evolution

### Add Fields Without Downtime

Add new fields to existing collections on the fly — no need to recreate.

Docs: [Add Fields to an Existing Collection](https://docs.zilliz.com/docs/add-fields-to-an-existing-collection)

### Enable Dynamic Field on Existing Collections

Turn on dynamic field support without recreating the collection.

Docs: [Modify Collection](https://docs.zilliz.com/docs/modify-collections#example-4-enable-dynamic-field)

## 6. Enhanced Full-Text Search

- **4× faster** than Elasticsearch
- **Multi-language analyzers**: Chinese, Japanese, Korean, and more
- **Phrase match**: exact phrase queries within full-text search
- **Analyzer GUI**: configure and test analyzers in the console

Docs: [Multi-language Analyzers](https://docs.zilliz.com/docs/multi-language-analyzers) | [Phrase Match](https://docs.zilliz.com/docs/phrase-match)

## 7. Accelerated JSON Filtering

- **JSON Indexing**: inverted index on specific JSON paths — up to 100× faster
- **JSON Shredding**: automatic optimization of nested JSON queries

Docs: [JSON Indexing](https://docs.zilliz.com/docs/json-indexing) | [JSON Shredding](https://docs.zilliz.com/docs/json-shredding)

## 8. New Reranking Functions

| Ranker | What It Does |
|--------|-------------|
| **Boost Ranker** | Combine semantic similarity with field-based boosting |
| **Decay Ranker** | Time/distance-based decay for recency or proximity weighting |

Docs: [Boost Ranker](https://docs.zilliz.com/docs/boost-ranker) | [Decay Ranker](https://docs.zilliz.com/docs/decay-ranker)

## 9. Index Build Level

Fine-tune recall vs. capacity trade-off:

| Level | Best For |
|-------|---------|
| **Precision-first** | Mission-critical apps where recall is paramount |
| **Balanced** (default) | Most use cases |
| **Capacity-first** | Maximum data density, lower recall acceptable |

Docs: [Tune Index Build Level](https://docs.zilliz.com/docs/tune-index-build-level)

## 10. Search Enhancements

### Primary-Key Search

Perform ANN search using a primary key instead of a raw vector — no need to retrieve vectors first.

Docs: [Primary-Key Search](https://docs.zilliz.com/docs/primary-key-search)

### Semantic Highlighter

Identifies and highlights relevant text segments based on query intent (not just keyword matches). Powered by Zilliz's open-source model.

Docs: [Semantic Highlighter](https://docs.zilliz.com/docs/semantic-highlighter)

### Lexical Highlighter

Annotates matched terms with customizable tags and fragment-level context for full-text search results.

Docs: [Lexical Highlighter](https://docs.zilliz.com/docs/text-highlighter)

## Feature Availability Summary

| Feature | Status |
|---------|--------|
| Geometry, Struct, TimestampTz | GA |
| INT8 Vector | GA |
| Partial Upserts | GA |
| Tiered Storage | GA (billing active) |
| Field Addition | GA |
| Full-Text Search Enhancements | GA |
| JSON Indexing & Shredding | GA |
| Boost/Decay Rankers | GA |
| Index Build Level | GA |
| Primary-Key Search | GA |
| Semantic/Lexical Highlighter | GA |
| MINHASH_LSH | Private Preview |

## Docs

- [October 2025 Release Notes](https://docs.zilliz.com/docs/release-notes-2510)
- [November 2025 Release Notes](https://docs.zilliz.com/docs/release-notes-2511)
- [December 2025 Release Notes (GA)](https://docs.zilliz.com/docs/release-notes-2512)
- [January 2026 Release Notes](https://docs.zilliz.com/docs/release-notes-2601)
- [Feature Availability](https://docs.zilliz.com/docs/feature-availability)
