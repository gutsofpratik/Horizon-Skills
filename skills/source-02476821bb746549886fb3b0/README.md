# Create Notebook

Generate Jupyter notebooks for FiftyOne workflows: getting-started guides, tutorials, recipes, and full ML pipelines.

## Install

```bash
curl -sL skil.sh | sh -s -- voxel51/fiftyone-skills
```

When prompted, select **fiftyone-create-notebook** from the menu.

## Requirements

- [FiftyOne](https://docs.voxel51.com/getting_started/install.html)
- Jupyter (`pip install jupyter`)

## Usage

Ask your AI assistant:

```
"Create a getting-started notebook for FiftyOne"
"Write a tutorial notebook on how to evaluate object detection models"
"Generate a quick recipe for loading a COCO dataset and filtering by label"
"Build an end-to-end ML pipeline notebook from data import to evaluation"
```

The skill classifies your request (getting-started, tutorial, recipe, or full pipeline) and generates a structured, runnable notebook.

## Example

```
"Create a tutorial notebook that shows how to find duplicates using FiftyOne Brain"
```

The notebook will include:
- Setup and installation cells
- Dataset loading with the FiftyOne Zoo
- Step-by-step workflow with explanations
- Visualization in the FiftyOne App

## See also

- [FiftyOne tutorials](https://docs.voxel51.com/tutorials/index.html)
- [FiftyOne recipes](https://docs.voxel51.com/recipes/index.html)
