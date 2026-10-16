# Cloud Regions & Connection Reference

Quick reference for supported regions, endpoints, and connection details.

---

## Table of Contents

1. [Supported Regions](#supported-regions)
2. [Connection Ports by Cloud](#connection-ports-by-cloud)
3. [Endpoint Format](#endpoint-format)
4. [Region Request](#region-request)

---

## Supported Regions

### AWS Regions

| Region Code | Location | Serverless | Dedicated |
|-------------|----------|------------|-----------|
| us-east-1 | N. Virginia | ✓ | ✓ |
| us-east-2 | Ohio | ✓ | ✓ |
| us-west-2 | Oregon | ✓ | ✓ |
| ca-central-1 | Canada | ✓ | ✓ |
| eu-central-1 | Frankfurt | ✓ | ✓ |
| eu-west-1 | Ireland | ✓ | ✓ |
| ap-northeast-1 | Tokyo | ✓ | ✓ |
| ap-southeast-1 | Singapore | ✓ | ✓ |
| ap-southeast-2 | Sydney | ✓ | ✓ |

**Not supported**: ap-northeast-2 (Seoul), ap-south-1 (Mumbai), sa-east-1 (Sao Paulo)

### GCP Regions

| Region Code | Location | Serverless | Dedicated |
|-------------|----------|------------|-----------|
| gcp-us-west1 | Oregon | ✓ | ✓ |
| gcp-us-east4 | N. Virginia | ✓ | ✓ |
| gcp-europe-west4 | Netherlands | ✓ | ✓ |
| gcp-asia-southeast1 | Singapore | ✓ | ✓ |

### Azure Regions

| Region Code | Location | Serverless | Dedicated |
|-------------|----------|------------|-----------|
| azure-eastus | East US | - | ✓ |
| azure-eastus2 | East US 2 | - | ✓ |
| azure-westus2 | West US 2 | - | ✓ |
| azure-westeurope | West Europe | - | ✓ |

> **Note**: Azure does not support Serverless clusters currently.

---

## Connection Ports by Cloud

**IMPORTANT**: Different cloud providers use different port configurations.

| Cloud Provider | gRPC Port | Protocol |
|----------------|-----------|----------|
| **AWS** | 19530-19550 | HTTPS |
| **GCP** | 443 | HTTPS |
| **Azure** | 19530 | HTTPS |

### Why This Matters

- **SDK connections**: Most SDKs auto-detect port from endpoint URI
- **Firewall rules**: Ensure outbound traffic allowed on correct port
- **Load balancers**: Configure health checks on correct port

### Connection Examples

**AWS Cluster**:
```python
uri = "https://in03-xxxxx.api.aws-us-east-1.zillizcloud.com:19530"
```

**GCP Cluster**:
```python
uri = "https://in03-xxxxx.api.gcp-us-west1.zillizcloud.com:443"
# Or without port (443 is default for HTTPS)
uri = "https://in03-xxxxx.api.gcp-us-west1.zillizcloud.com"
```

**Azure Cluster**:
```python
uri = "https://in03-xxxxx.api.azure-eastus.zillizcloud.com:19530"
```

---

## Endpoint Format

### Public Endpoint

```
https://{cluster-id}.api.{cloud-region}.zillizcloud.com:{port}
```

Components:
- `cluster-id`: e.g., `in03-xxxxxxxx`
- `cloud-region`: e.g., `aws-us-east-1`, `gcp-us-west1`, `azure-eastus`
- `port`: See [Connection Ports by Cloud](#connection-ports-by-cloud)

### Private Endpoint (Private Link)

Available for Enterprise/Business Critical plans:
- AWS: VPC Endpoint
- GCP: Private Service Connect
- Azure: Private Endpoint

Format varies by cloud; get from Console → Cluster → Private Endpoint.

---

## Region Request

### Request a New Region

If your required region is not supported:

1. Submit request at: https://zilliz.com/cloud-region-request
2. Include:
   - Desired cloud provider and region
   - Use case and expected scale
   - Timeline requirements

### Alternative Options

If region is not available:

| Option | When to Use |
|--------|-------------|
| Nearest available region | Latency tolerance OK |
| BYOC (Bring Your Own Cloud) | Must be in specific region, Enterprise plan |
| Contact Sales | Strategic partnership or large deployment |

---

## Quick Reference

### How to Find Your Endpoint

1. Zilliz Cloud Console
2. Select your cluster
3. **Cluster Details** → **Connect** card
4. Copy **Public Endpoint**

### Connection Troubleshooting

| Issue | Check |
|-------|-------|
| Connection timeout | Firewall allows outbound to correct port |
| SSL/TLS error | Endpoint starts with `https://` |
| Authentication failed | API key has correct permissions |
| Port error | Using correct port for cloud provider |
