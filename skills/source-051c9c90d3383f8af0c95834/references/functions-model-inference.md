# Functions & Model Inference Reference

Built-in processing pipeline — send raw text, get search results. No external embedding service needed.

## Concept: What is a Function?

A **Function** is a configurable unit that runs at a specific stage of the search workflow:

- **Pre-search functions**: Convert text → vectors (used for retrieval)
- **Post-search functions**: Rerank retrieved candidates (refine ordering)

```
Request → [Pre-search Function] → Vector Search → [Post-search Function] → Results
              (Embedding/BM25)                        (Rerank)
```

## Function Types

| Type | Stage | Input → Output | Use Case |
|------|-------|---------------|----------|
| **TextEmbedding** | Pre-search | Text → Dense vector | Semantic search |
| **BM25** | Pre-search | Text → Sparse vector | Full-text/keyword search |
| **Rerank** | Post-search | Candidates → Reordered | Improve relevance |

## 1. Embedding Functions (TextEmbedding)

Let Zilliz Cloud generate dense embeddings from raw text automatically.

### Supported Providers
OpenAI, Azure OpenAI, DashScope, Amazon Bedrock, Google Vertex AI, Voyage AI, Cohere, SiliconFlow, Hugging Face TEI, Zilliz Hosted Models

### Setup

```python
from pymilvus import MilvusClient, DataType, Function, FunctionType

client = MilvusClient(uri="YOUR_ENDPOINT", token="YOUR_TOKEN")

schema = client.create_schema()
schema.add_field("id", DataType.INT64, is_primary=True, auto_id=True)
schema.add_field("text", DataType.VARCHAR, max_length=65535)
schema.add_field("vector", DataType.FLOAT_VECTOR, dim=1024)

# Add embedding function
schema.add_function(Function(
    name="text_embedding",
    function_type=FunctionType.TEXTEMBEDDING,
    input_field_names=["text"],
    output_field_names=["vector"],
    params={
        "provider": "siliconflow",  # or "openai", "voyageai", etc.
        "model_name": "BAAI/bge-large-en-v1.5",
        "credential": "your-api-key"  # or credential label from milvus.yaml
    }
))
```

### Insert — just text, no vectors needed
```python
client.insert("my_collection", [
    {"text": "Machine learning transforms data into insights"},
    {"text": "Vector databases power semantic search"},
])
```

### Search — query with text directly
```python
results = client.search(
    collection_name="my_collection",
    data=["how does semantic search work?"],
    anns_field="vector",
    limit=5,
    output_fields=["text"]
)
```

## 2. BM25 Function (Full-Text Search)

Transforms raw text into sparse vectors for lexical/keyword search.

### Setup

```python
schema = client.create_schema()
schema.add_field("id", DataType.INT64, is_primary=True, auto_id=True)
schema.add_field("text", DataType.VARCHAR, max_length=1000, enable_analyzer=True)
schema.add_field("sparse", DataType.SPARSE_FLOAT_VECTOR)

schema.add_function(Function(
    name="text_bm25",
    function_type=FunctionType.BM25,
    input_field_names=["text"],
    output_field_names=["sparse"]
))

# Index with BM25 metric
index_params = client.prepare_index_params()
index_params.add_index(
    field_name="sparse",
    index_type="AUTOINDEX",
    metric_type="BM25"
)

client.create_collection("bm25_collection", schema=schema, index_params=index_params)
```

### Search
```python
results = client.search(
    collection_name="bm25_collection",
    data=["information retrieval techniques"],
    anns_field="sparse",
    limit=5,
    output_fields=["text"]
)
```

## 3. Hybrid Search (Dense + BM25)

Combine semantic and keyword search for best results.

```python
from pymilvus import AnnSearchRequest, RRFRanker, WeightedRanker

# Dense search
dense_req = AnnSearchRequest(
    data=[query_dense_vector],
    anns_field="dense_vector",
    param={},
    limit=10
)

# Sparse (BM25) search — pass raw text, BM25 function handles tokenization
sparse_req = AnnSearchRequest(
    data=["renewable energy developments"],
    anns_field="sparse_vector",
    param={},
    limit=10
)

# Combine with RRF ranking
results = client.hybrid_search(
    "my_collection",
    [dense_req, sparse_req],
    ranker=RRFRanker(k=60),
    limit=5,
    output_fields=["text"]
)

# Alternative: Weighted ranking (70% semantic, 30% keyword)
results = client.hybrid_search(
    "my_collection",
    [dense_req, sparse_req],
    ranker=WeightedRanker(0.7, 0.3),  # weights correspond to reqs order
    limit=5,
    output_fields=["text"]
)
```

## 4. Rerank Functions

### Built-in Rankers

> **IMPORTANT**: Use `RRFRanker` and `WeightedRanker` classes from `pymilvus`, NOT `Function(FunctionType.RERANK)`.

| Ranker | Class | Usage |
|--------|-------|-------|
| **RRF** | `RRFRanker(k=60)` | Equal treatment of multiple search paths (recommended default) |
| **Weighted** | `WeightedRanker(0.7, 0.3)` | Known importance of each search path, weights match reqs order |
| **Decay** | Time-based or distance-based ranking | `function`, `origin`, `scale`, `offset`, `decay` |
| **Model** | Cross-encoder reranking for max precision | `provider`, `model_name`, `queries` |

### Model-based Rerankers (Providers)
- **Cohere**: `rerank-english-v3.0`
- **Voyage AI**: `rerank-2.5`
- **SiliconFlow**: `BAAI/bge-reranker-v2-m3`
- **TEI**: Self-hosted Hugging Face models
- **vLLM**: Self-hosted rerankers

## 5. Hosted Models (Private Preview)

Deploy fully managed model instances on Zilliz infrastructure:
- Zero data transfer fees
- Data stays within private network
- Ultra-low latency

Contact Support for access.

## 6. Third-Party Model Provider Integration

Manage AI model credentials within Zilliz Cloud:
- Rotate API keys without code changes
- Centralized credential management

See [Integrate with Model Providers](https://docs.zilliz.com/docs/integrate-with-model-providers).

## Docs

- [Function Overview](https://docs.zilliz.com/docs/function-and-model-inference-overview)
- [BM25 Function](https://docs.zilliz.com/docs/bm25-function)
- [Embedding Functions](https://docs.zilliz.com/docs/model-based-functions)
- [Rerank Functions](https://docs.zilliz.com/docs/reranking)
- [Hosted Models](https://docs.zilliz.com/docs/hosted-models)
