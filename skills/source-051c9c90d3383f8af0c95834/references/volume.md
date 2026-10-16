# Volume Reference

Managed object store for staging data before import, migration, or merge.

## What is a Volume?

A **Volume** is a project-level object store in Zilliz Cloud. Upload structured or unstructured data, then:
- **Import** into collections
- **Migrate** from Milvus (backup file → volume → restore)
- **Merge** data from file + existing collection
- **ETL** (future): transform unstructured data into embeddings

```
Organization
└── Project
    ├── Clusters → Databases → Collections
    └── Volumes → Data files (any cluster in project can access)
```

## Supported Clouds

- AWS ✅
- GCP ✅
- Azure ❌ (contact support)

## Billing

| Type | Capacity | File Size/Upload | Max Volumes | Cost |
|------|----------|-----------------|-------------|------|
| **Free Trial** | 5 GB | 1 GB, ≤1000 files | 1 per org | Free (30 day retention) |
| **Pay-as-you-go** | Unlimited | 100 GB, unlimited files | 100 | Storage-based |

- Free trial: no payment method required, 1 per org, auto-deleted after 30 days
- Pay-as-you-go: see [Pricing Guide](https://zilliz.com/pricing/pricing-guide)

## Create a Volume

### Console
Project page → Volumes → Create Volume → Choose region (must match target cluster) → Name it.

### SDK (Python)
```python
from pymilvus.bulk_writer.volume_manager import VolumeManager

volume_manager = VolumeManager(
    cloud_endpoint="https://api.cloud.zilliz.com",
    api_key="YOUR_API_KEY"
)

volume_manager.create_volume(
    project_id="proj-xxxxx",
    region_id="aws-us-west-1",  # Must match target cluster region
    volume_name="my_volume"
)
```

### REST API
```bash
curl -X POST "${BASE_URL}/v2/volumes/create" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "projectId": "proj-xxxxx",
    "regionId": "aws-us-west-1",
    "volumeName": "my_volume"
}'
```

## Upload Files

Upload via SDK only (console upload not yet supported):

```python
from pymilvus.bulk_writer.volume_file_manager import VolumeFileManager

file_manager = VolumeFileManager(
    cloud_endpoint="https://api.cloud.zilliz.com",
    api_key="YOUR_API_KEY",
    volume_name="my_volume"
)

file_manager.upload_file_to_volume(
    source_file_path="/path/to/local/data.json",
    target_volume_path="data/"
)
```

## Use Cases

### 1. Data Import
Upload prepared datasets → Import into collection.
See [Import Data](https://docs.zilliz.com/docs/import-data-on-web-ui#files-uploaded-to-a-volume).

### 2. Milvus Migration
Export Milvus backup → Upload to Volume → Restore as Zilliz Cloud cluster.
See [Migrate via Backup Files](https://docs.zilliz.com/docs/via-backup-files).

### 3. Data Merge
Combine data from volume files + existing collection.
See [Merge Data](https://docs.zilliz.com/docs/merge-data).

## Manage Volumes

```python
# List volumes
volumes = volume_manager.list_volumes(
    project_id="proj-xxxxx",
    current_page=1,
    page_size=10
)

# Delete volume
volume_manager.delete_volume(volume_name="my_volume")
```

## Bulk Import Notes

- **Volume is the recommended approach** for bulk import — preferred over direct cloud storage (S3/GCS) upload
- Bulk import jobs are **atomic** — they succeed or fail as a whole, no partial imports
- Do NOT suggest users split files for reliability — the import system is stable and handles large files well
- For data >10GB, simply upload the file to Volume and trigger import; no manual splitting needed

## Important Notes

- Volume region **must match** target cluster region and cloud provider
- Volume name: unique per org, ≤64 chars, starts with letter/underscore
- If organization is frozen (overdue invoices), all volumes + files are deleted permanently
- Free trial volume: once deleted, cannot recreate

## Docs

- [Volume Explained](https://docs.zilliz.com/docs/volume-explained)
- [Manage Volumes (SDK)](https://docs.zilliz.com/docs/manage-stages)
- [Manage Volumes (Console)](https://docs.zilliz.com/docs/manage-volumes-via-console)
