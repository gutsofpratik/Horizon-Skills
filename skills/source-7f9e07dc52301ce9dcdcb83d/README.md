# Dataset Export

Export FiftyOne datasets to standard formats for training, sharing, or publishing.

## Install

```bash
curl -sL skil.sh | sh -s -- voxel51/fiftyone-skills
```

When prompted, select **fiftyone-dataset-export** from the menu.

## Requirements

- [FiftyOne](https://docs.voxel51.com/getting_started/install.html)
- [FiftyOne MCP Server](https://github.com/voxel51/fiftyone-mcp-server) (optional, recommended for App control)

## Usage

Load a dataset in FiftyOne, then ask your AI assistant:

```
"Export my dataset to COCO format at /tmp/export"
"Save this dataset to Hugging Face Hub as my-org/my-dataset"
"Export the current view as a YOLO dataset"
```

The skill confirms the dataset, label fields, and export path with you before writing anything.

## Example

```python
import fiftyone as fo
import fiftyone.zoo as foz

# Load a dataset to export
dataset = foz.load_zoo_dataset("quickstart")
```

Then ask your assistant:

```
"Export quickstart to COCO detection format at /tmp/quickstart-coco"
```

## Supported formats

COCO, YOLO, VOC, CVAT, Open Images, CSV, TFRecords, and Hugging Face Hub.

## See also

- [Dataset Export docs](https://docs.voxel51.com/user_guide/export_datasets.html)
- [Hugging Face Hub export](https://docs.voxel51.com/integrations/huggingface.html)
