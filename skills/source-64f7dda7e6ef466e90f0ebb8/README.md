# Generate Data Lens Connector

Generate a fully functional Data Lens connector plugin from your external database schema.

## Install

```bash
curl -sL skil.sh | sh -s -- voxel51/fiftyone-skills
```

When prompted, select **fiftyone-generate-data-lens-connector** from the menu.

## Requirements

- [FiftyOne Enterprise](https://docs.voxel51.com/enterprise/index.html) (Data Lens is an Enterprise-only feature)
- [FiftyOne](https://docs.voxel51.com/getting_started/install.html)

## Usage

Ask your AI assistant:

```
"Generate a Data Lens connector for my PostgreSQL database"
"Create a connector that lets me browse my BigQuery image table in FiftyOne"
"Build a Data Lens plugin from this database schema"
```

Provide your database schema (table names, column types, and which columns map to image paths or labels) and the skill generates a complete `DataLensOperator` plugin ready to install.

## Example

```
"Here is my PostgreSQL schema:
  images(id, filepath, label, confidence, created_at)
Generate a Data Lens connector so I can browse this in FiftyOne."
```

## Note

> Data Lens is a FiftyOne Enterprise feature. The generated connector requires a FiftyOne Enterprise deployment to run.

## See also

- [FiftyOne Enterprise docs](https://docs.voxel51.com/enterprise/index.html)
- [Plugin development docs](https://docs.voxel51.com/plugins/developing_plugins.html)
