# Zilliz Cloud Developer Guide

Practical guidance for building production applications with Zilliz Cloud.

## Table of Contents

1. [Schema Design by Use Case](#schema-design-by-use-case)
2. [Framework Integrations](#framework-integrations)
3. [Migration Scripts](#migration-scripts)
4. [Debugging & Diagnostics](#debugging--diagnostics)
5. [Performance Tuning](#performance-tuning)
6. [Production Readiness Checklist](#production-readiness-checklist)

---

## Schema Design by Use Case

| Use Case | Recommended Schema | Key Decisions |
|----------|-------------------|---------------|
| RAG | `vector` + `text` + `source` + `chunk_id` | Enable `auto_id`, use `COSINE` |
| E-commerce | `vector` + `product_id` + `category` + `price` | Add scalar index on `category`, `price` |
| Multi-tenant SaaS | `vector` + `tenant_id` (partition key) + `content` | Use `partition_key` for isolation |
| Image search | `vector` + `image_url` + `tags` (array) | Use `L2` metric, add array field for tags |
| Hybrid search | `dense_vector` + `sparse_vector` + `text` | Enable BM25 for keyword matching |

### RAG Application Template

```python
from pymilvus import MilvusClient

client = MilvusClient(
    uri="YOUR_CLUSTER_ENDPOINT",
    token="YOUR_API_KEY"
)

# Create collection optimized for RAG
client.create_collection(
    collection_name="rag_knowledge_base",
    dimension=768,
    metric_type="COSINE",
    auto_id=True
)

def insert_documents(docs: list[dict]):
    """Insert documents with embeddings and metadata"""
    data = [
        {
            "vector": doc["embedding"],
            "text": doc["content"],
            "source": doc["source"],
            "chunk_id": doc["chunk_id"]
        }
        for doc in docs
    ]
    return client.insert(collection_name="rag_knowledge_base", data=data)

def search_similar(query_embedding: list[float], top_k: int = 5):
    """Retrieve relevant context for RAG"""
    return client.search(
        collection_name="rag_knowledge_base",
        data=[query_embedding],
        limit=top_k,
        output_fields=["text", "source"]
    )
```

---

## Framework Integrations

### LangChain

```python
from langchain_milvus import Milvus
from langchain_openai import OpenAIEmbeddings

vectorstore = Milvus(
    embedding_function=OpenAIEmbeddings(),
    connection_args={
        "uri": "YOUR_CLUSTER_ENDPOINT",
        "token": "YOUR_API_KEY"
    },
    collection_name="langchain_docs"
)

# Add documents
vectorstore.add_texts(["doc1", "doc2", "doc3"])

# Search
results = vectorstore.similarity_search("query", k=5)
```

### LlamaIndex

```python
from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.core import VectorStoreIndex, StorageContext

vector_store = MilvusVectorStore(
    uri="YOUR_CLUSTER_ENDPOINT",
    token="YOUR_API_KEY",
    collection_name="llamaindex_docs",
    dim=1536
)

storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)

# Query
query_engine = index.as_query_engine()
response = query_engine.query("What is...")
```

### Haystack

```python
from haystack_integrations.document_stores.milvus import MilvusDocumentStore

document_store = MilvusDocumentStore(
    connection_args={"uri": "YOUR_CLUSTER_ENDPOINT", "token": "YOUR_API_KEY"},
    collection_name="haystack_docs"
)
```

---

## Migration Scripts

### From Pinecone

```python
def migrate_from_pinecone(pinecone_index, milvus_client, batch_size=1000):
    """Migrate vectors from Pinecone to Zilliz Cloud"""
    # Get total count
    stats = pinecone_index.describe_index_stats()

    # Fetch and insert in batches
    for ids_batch in fetch_id_batches(pinecone_index, batch_size):
        vectors = pinecone_index.fetch(ids=ids_batch)

        data = [
            {
                "id": v.id,
                "vector": v.values,
                **v.metadata
            }
            for v in vectors.vectors.values()
        ]
        milvus_client.insert(collection_name="migrated", data=data)
        print(f"Migrated {len(data)} vectors")
```

### From NumPy/Pickle Files

```python
import numpy as np

def migrate_from_numpy(vectors_file: str, metadata_file: str, client, collection_name: str):
    """Migrate from numpy arrays to Zilliz Cloud"""
    vectors = np.load(vectors_file)
    metadata = np.load(metadata_file, allow_pickle=True)

    # Prepare data
    data = [
        {"vector": vectors[i].tolist(), **metadata[i]}
        for i in range(len(vectors))
    ]

    # Batch insert (5000 recommended)
    batch_size = 5000
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        client.insert(collection_name=collection_name, data=batch)
        print(f"Inserted {min(i + batch_size, len(data))}/{len(data)}")
```

### From FAISS

```python
import faiss

def migrate_from_faiss(faiss_index_path: str, metadata: list, client, collection_name: str):
    """Migrate from FAISS index to Zilliz Cloud"""
    index = faiss.read_index(faiss_index_path)
    vectors = index.reconstruct_n(0, index.ntotal)

    data = [
        {"vector": vectors[i].tolist(), **metadata[i]}
        for i in range(len(vectors))
    ]

    # Batch insert
    for i in range(0, len(data), 5000):
        client.insert(collection_name=collection_name, data=data[i:i+5000])
```

---

## Debugging & Diagnostics

### Check Collection Status

```python
def diagnose_collection(client, collection_name: str):
    """Print diagnostic information about a collection"""
    info = client.describe_collection(collection_name)

    print(f"Collection: {collection_name}")
    print(f"  Entity count: {info.get('row_count', 'N/A')}")
    print(f"  Indexes: {info.get('indexes', [])}")
    print(f"  Fields: {[f['name'] for f in info.get('fields', [])]}")

    # Check a sample vector dimension
    sample = client.query(
        collection_name=collection_name,
        filter="",
        limit=1,
        output_fields=["vector"]
    )
    if sample:
        print(f"  Vector dimension: {len(sample[0]['vector'])}")
```

### Test Connectivity

```python
def test_connection(uri: str, token: str) -> bool:
    """Test Zilliz Cloud connection"""
    try:
        from pymilvus import MilvusClient
        client = MilvusClient(uri=uri, token=token)
        collections = client.list_collections()
        print(f"Connection OK. Found {len(collections)} collections.")
        return True
    except Exception as e:
        print(f"Connection failed: {e}")
        return False
```

### Common Error Diagnostics

| Error | Likely Cause | Diagnostic Command |
|-------|--------------|-------------------|
| `dimension mismatch` | Vector size doesn't match collection | Check `len(vector)` vs collection dimension |
| `node not match` | Cluster scaling in progress | Wait 2-5s, retry with backoff |
| `collection not found` | Wrong name or not created | `client.list_collections()` |
| `rate limit exceeded` | Too many requests | Implement backoff, check quotas |

---

## Performance Tuning

### Quick Optimization Table

| Problem | Diagnosis | Solution |
|---------|-----------|----------|
| Slow search | Low `nprobe` | `search_params={"nprobe": 16}` |
| Cold start latency | Collection not loaded | `client.load_collection("name")` |
| Insert bottleneck | Small batch size | Use `batch_size=5000` |
| Memory pressure | Too many collections loaded | `client.release_collection("unused")` |
| High vCU cost (Serverless) | Full collection scan | Add `partition_key` filter |

### Search Optimization

```python
# Optimize search with proper parameters
results = client.search(
    collection_name="my_collection",
    data=[query_vector],
    limit=10,
    search_params={
        "nprobe": 16,  # Increase for better recall (default: 10)
        "radius": 0.5,  # Optional: filter by distance
    },
    output_fields=["id", "text"],  # Only fetch needed fields
)
```

### Batch Insert Best Practices

```python
def optimized_insert(client, collection_name: str, data: list):
    """Insert with optimal batch size and error handling"""
    BATCH_SIZE = 5000

    for i in range(0, len(data), BATCH_SIZE):
        batch = data[i:i + BATCH_SIZE]
        try:
            client.insert(collection_name=collection_name, data=batch)
        except Exception as e:
            print(f"Batch {i//BATCH_SIZE} failed: {e}")
            # Retry with smaller batch
            for item in batch:
                client.insert(collection_name=collection_name, data=[item])
```

---

## Production Readiness Checklist

### Security

- [ ] API key stored in environment variable (not hardcoded)
- [ ] IP whitelist configured (if using Dedicated)
- [ ] Private Link enabled (for Enterprise tier)
- [ ] RBAC configured for team access

### Performance

- [ ] Collection loaded before first query
- [ ] Index type selected (AUTOINDEX recommended)
- [ ] Batch size optimized (5000 for inserts)
- [ ] Connection pooling implemented for high concurrency
- [ ] Search parameters tuned (`nprobe`, `limit`)

### Reliability

- [ ] Retry logic with exponential backoff
- [ ] Error handling for "node not match" during scaling
- [ ] Health check endpoint configured
- [ ] Graceful degradation strategy defined

### Monitoring

- [ ] Latency metrics tracked (p50, p99)
- [ ] Error rate alerting configured
- [ ] Collection size monitoring
- [ ] vCU usage tracking (for Serverless)

### Cost Optimization

- [ ] Right-sized CU for data volume
- [ ] Tiered storage evaluated for cold data
- [ ] Unused collections cleaned up
- [ ] Partition keys used for Serverless cost reduction

### Backup & Recovery

- [ ] Automatic backup enabled
- [ ] Manual snapshot before major changes
- [ ] Recovery procedure documented and tested
