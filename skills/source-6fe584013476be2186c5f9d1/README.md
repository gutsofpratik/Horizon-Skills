# Dataset Inference

Run ML model inference on a FiftyOne dataset using Zoo models or your own. Supports detection, classification, segmentation, and embeddings.

## Install

```bash
curl -sL skil.sh | sh -s -- voxel51/fiftyone-skills
```

When prompted, select **fiftyone-dataset-inference** from the menu.

## Requirements

- [FiftyOne](https://docs.voxel51.com/getting_started/install.html)
- [FiftyOne MCP Server](https://github.com/voxel51/fiftyone-mcp-server) (optional, recommended for operator-based inference)

## Usage

Load a dataset in FiftyOne, then ask your AI assistant:

```
"Run YOLO object detection on my dataset"
"Compute CLIP embeddings for all images"
"Apply a segmentation model and store results in a new field"
```

The skill discovers available models dynamically, confirms the model and output field with you, then runs inference.

## Example

```python
import fiftyone as fo
import fiftyone.zoo as foz

dataset = foz.load_zoo_dataset("quickstart")
```

Then ask your assistant:

```
"Run object detection on the quickstart dataset using a YOLO model"
```

## See also

- [Model Zoo docs](https://docs.voxel51.com/model_zoo/index.html)
- [Applying models docs](https://docs.voxel51.com/user_guide/model_zoo/models.html)
