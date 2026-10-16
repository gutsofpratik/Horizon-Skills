# Zilliz Cloud API Patterns

Advanced patterns and examples for Zilliz Cloud development.

## Table of Contents

1. [Schema Design](#schema-design)
2. [Embedding Integration](#embedding-integration)
3. [RAG Pipeline](#rag-pipeline)
4. [Multi-tenancy](#multi-tenancy)
5. [Performance Optimization](#performance-optimization)
6. [Error Handling](#error-handling)

---

## Schema Design

### Custom Schema with Index

```python
from pymilvus import MilvusClient, DataType

schema = MilvusClient.create_schema(auto_id=True, enable_dynamic_field=True)
schema.add_field("id", DataType.INT64, is_primary=True)
schema.add_field("vector", DataType.FLOAT_VECTOR, dim=768)
schema.add_field("category", DataType.VARCHAR, max_length=100)

index_params = MilvusClient.prepare_index_params()
index_params.add_index(field_name="vector", index_type="AUTOINDEX", metric_type="COSINE")

client.create_collection("my_collection", schema=schema, index_params=index_params)
```

### Field Types Reference

| Type | Use Case | Notes |
|------|----------|-------|
| `FLOAT_VECTOR` | Dense embeddings (OpenAI, etc.) | Specify `dim` |
| `SPARSE_FLOAT_VECTOR` | Sparse embeddings (BM25) | Variable length |
| `VARCHAR` | Text, IDs | Specify `max_length` |
| `INT64` | Timestamps, counts | Primary key candidate |
| `JSON` | Flexible metadata | Dynamic structure |
| `BOOL` | Flags | - |
| `FLOAT` / `DOUBLE` | Numeric values | - |
| `ARRAY` | Lists of primitives | Specify `element_type`, `max_capacity` |

### Metric Types for Vector Index

| Metric | Use Case | Notes |
|--------|----------|-------|
| `COSINE` | Text embeddings | Most common, normalized |
| `L2` | Image embeddings | Euclidean distance |
| `IP` | Pre-normalized vectors | Inner product |
| `JACCARD` | Set similarity | Binary vectors |
| `HAMMING` | Binary vectors | Bit difference |

---

## Embedding Integration

### OpenAI Embeddings

```python
from openai import OpenAI
from pymilvus import MilvusClient

openai_client = OpenAI()
milvus_client = MilvusClient(uri="...", token="...")

def get_embedding(text: str) -> list[float]:
    response = openai_client.embeddings.create(
        input=text,
        model="text-embedding-3-small"  # 1536 dimensions
    )
    return response.data[0].embedding

# Insert with embeddings
docs = ["AI is transforming industries", "Vector databases enable semantic search"]
data = [
    {"vector": get_embedding(doc), "text": doc}
    for doc in docs
]
milvus_client.insert(collection_name="docs", data=data)
```

### Sentence Transformers

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')  # 384 dimensions

def get_embeddings(texts: list[str]) -> list[list[float]]:
    return model.encode(texts).tolist()

# Batch embedding for efficiency
texts = ["doc1", "doc2", "doc3"]
vectors = get_embeddings(texts)
```

---

## RAG Pipeline

### Basic RAG with Context Retrieval

```python
from pymilvus import MilvusClient
from openai import OpenAI

milvus = MilvusClient(uri="...", token="...")
openai = OpenAI()

def rag_query(question: str, collection: str = "knowledge_base") -> str:
    # 1. Embed the question
    q_embedding = openai.embeddings.create(
        input=question,
        model="text-embedding-3-small"
    ).data[0].embedding

    # 2. Search for relevant context
    results = milvus.search(
        collection_name=collection,
        data=[q_embedding],
        limit=5,
        output_fields=["text", "source"]
    )

    # 3. Build context from results
    context = "\n\n".join([
        f"[{hit['entity']['source']}]: {hit['entity']['text']}"
        for hit in results[0]
    ])

    # 4. Generate answer with context
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Answer based on the provided context."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
        ]
    )

    return response.choices[0].message.content
```

### RAG with Reranking

```python
from pymilvus import MilvusClient, RRFRanker

def rag_with_rerank(question: str) -> str:
    # Get more candidates, then rerank
    results = milvus.search(
        collection_name="knowledge_base",
        data=[get_embedding(question)],
        limit=20,  # Fetch more for reranking
        output_fields=["text", "source"]
    )

    # Rerank using cross-encoder or LLM
    candidates = [hit['entity']['text'] for hit in results[0]]
    reranked = rerank_with_llm(question, candidates, top_k=5)

    # Use top reranked results as context
    return generate_answer(question, reranked)
```

---

## Multi-tenancy

### Partition-based Isolation

```python
# Create collection with partition key
schema = MilvusClient.create_schema()
schema.add_field("id", DataType.INT64, is_primary=True)
schema.add_field("tenant_id", DataType.VARCHAR, max_length=50, is_partition_key=True)
schema.add_field("vector", DataType.FLOAT_VECTOR, dim=768)
schema.add_field("content", DataType.VARCHAR, max_length=5000)

# Insert with tenant_id
data = [
    {"tenant_id": "tenant_A", "vector": [...], "content": "..."},
    {"tenant_id": "tenant_B", "vector": [...], "content": "..."},
]
client.insert(collection_name="multi_tenant", data=data)

# Search within tenant (automatic partition pruning)
results = client.search(
    collection_name="multi_tenant",
    data=[query_vector],
    filter="tenant_id == 'tenant_A'",
    limit=10
)
```

### Collection-per-tenant

```python
def get_tenant_collection(tenant_id: str) -> str:
    collection_name = f"tenant_{tenant_id}"

    if not client.has_collection(collection_name):
        client.create_collection(
            collection_name=collection_name,
            dimension=768,
            metric_type="COSINE"
        )

    return collection_name

# Usage
collection = get_tenant_collection("acme_corp")
client.insert(collection_name=collection, data=data)
```

---

## Performance Optimization

### Async Operations

```python
import asyncio
from pymilvus import MilvusClient

async def parallel_search(queries: list[list[float]]) -> list:
    """Search multiple queries in parallel"""
    tasks = [
        asyncio.to_thread(
            client.search,
            collection_name="my_collection",
            data=[q],
            limit=10
        )
        for q in queries
    ]
    return await asyncio.gather(*tasks)
```

### Connection Pooling

```python
from contextlib import contextmanager
from queue import Queue

class MilvusPool:
    def __init__(self, uri: str, token: str, size: int = 5):
        self.pool = Queue(maxsize=size)
        for _ in range(size):
            client = MilvusClient(uri=uri, token=token)
            self.pool.put(client)

    @contextmanager
    def get_client(self):
        client = self.pool.get()
        try:
            yield client
        finally:
            self.pool.put(client)

# Usage
pool = MilvusPool(uri="...", token="...", size=10)

with pool.get_client() as client:
    results = client.search(...)
```

### Batch Processing

```python
def process_large_dataset(data: list, batch_size: int = 5000):
    """Insert large datasets efficiently"""
    total = len(data)

    for i in range(0, total, batch_size):
        batch = data[i:i + batch_size]
        client.insert(collection_name="my_collection", data=batch)
        print(f"Inserted {min(i + batch_size, total)}/{total}")
```

---

## Iterator Safety

### Safe Query Iterator with Retry

```python
import time
from pymilvus import Collection
from pymilvus.exceptions import MilvusException

def safe_query_iterator(collection: Collection, batch_size: int = 1000,
                        max_retries: int = 3, **kwargs) -> list:
    """Query iterator with automatic retry on node mismatch errors"""
    for attempt in range(max_retries):
        try:
            iterator = collection.query_iterator(batch_size=batch_size, **kwargs)
            results = []
            while True:
                batch = iterator.next()
                if not batch:
                    break
                results.extend(batch)
            return results
        except MilvusException as e:
            if "node not match" in str(e) and attempt < max_retries - 1:
                print(f"Node mismatch, retrying ({attempt + 1}/{max_retries})...")
                time.sleep(2 * (attempt + 1))  # Exponential backoff
                continue
            raise
    return []
```

### Pagination Alternative (More Stable)

For serverless clusters or long-running operations, pagination is more reliable than iterators:

```python
def paginated_query(client, collection_name: str, expr: str = "",
                    output_fields: list = None, batch_size: int = 1000) -> list:
    """Stable pagination using offset-based queries"""
    output_fields = output_fields or ["*"]
    all_results = []
    offset = 0

    while True:
        results = client.query(
            collection_name=collection_name,
            filter=expr if expr else "",
            output_fields=output_fields,
            limit=batch_size,
            offset=offset
        )
        if not results:
            break
        all_results.extend(results)
        offset += len(results)

        if len(results) < batch_size:
            break

    return all_results
```

---

## Error Handling

### Retry with Backoff

```python
import time
from functools import wraps

def retry_with_backoff(max_retries: int = 3, base_delay: float = 1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    delay = base_delay * (2 ** attempt)
                    print(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry_with_backoff(max_retries=3)
def safe_search(query_vector):
    return client.search(
        collection_name="my_collection",
        data=[query_vector],
        limit=10
    )
```

### Graceful Degradation

```python
def search_with_fallback(query_vector, collection: str):
    """Search with fallback to cached results"""
    try:
        return client.search(
            collection_name=collection,
            data=[query_vector],
            limit=10
        )
    except ConnectionError:
        # Fall back to cached popular results
        return get_cached_results(collection)
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return []
```

### Validation Helpers

```python
def validate_vector(vector: list, expected_dim: int) -> bool:
    """Validate vector before insert"""
    if not isinstance(vector, list):
        raise ValueError("Vector must be a list")
    if len(vector) != expected_dim:
        raise ValueError(f"Expected {expected_dim} dimensions, got {len(vector)}")
    if not all(isinstance(x, (int, float)) for x in vector):
        raise ValueError("Vector must contain only numbers")
    return True

def safe_insert(data: list, collection: str, dim: int):
    """Insert with validation"""
    for item in data:
        validate_vector(item["vector"], dim)
    return client.insert(collection_name=collection, data=data)
```
