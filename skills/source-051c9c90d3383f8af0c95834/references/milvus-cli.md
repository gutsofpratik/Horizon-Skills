# Milvus CLI Reference

Command-line tool for managing Milvus/Zilliz Cloud instances.

## Installation

```bash
pip install milvus-cli
```

## Connect to Zilliz Cloud

```bash
# Interactive connection
milvus_cli

# Then in CLI:
connect -uri https://xxx.api.region.zillizcloud.com:19530 -token <your-api-key>
```

## Common Commands

### Collection Management

```bash
# List collections
list collections

# Create collection
create collection -c my_collection -s '{"fields": [...]}'

# Describe collection
describe collection -c my_collection

# Drop collection
delete collection -c my_collection
```

### Data Operations

```bash
# Insert data from file
insert -c my_collection -p /path/to/data.csv

# Query data
query -c my_collection -q "id in [1, 2, 3]"

# Search
search -c my_collection -d [[0.1, 0.2, ...]] -n 10
```

### Index Management

```bash
# Create index
create index -c my_collection -f vector -i AUTOINDEX -m COSINE

# Describe index
describe index -c my_collection -f vector

# Drop index
delete index -c my_collection -f vector
```

### Partition Operations

```bash
# List partitions
list partitions -c my_collection

# Create partition
create partition -c my_collection -p partition_name

# Load partition
load partition -c my_collection -p partition_name
```

## Useful Workflows

### Export Collection Schema

```bash
describe collection -c source_collection
# Copy output to create same schema on target
```

### Bulk Data Check

```bash
# Count entities
query -c my_collection -q "" --count

# Sample data
query -c my_collection -q "" -l 5 -o ["*"]
```

### Health Check

```bash
# Check connection
show connection

# List all collections with stats
list collections
```

## Tips

- Use `exit` or `quit` to leave CLI
- Tab completion available for commands
- Use `help <command>` for detailed usage
- Supports both Milvus and Zilliz Cloud connections
