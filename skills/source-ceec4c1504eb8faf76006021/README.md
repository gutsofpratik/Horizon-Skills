# Code Style

Write Python code that follows FiftyOne's official conventions: module structure, imports, logging, and API patterns.

## Install

```bash
curl -sL skil.sh | sh -s -- voxel51/fiftyone-skills
```

When prompted, select **fiftyone-code-style** from the menu.

## Requirements

- [FiftyOne](https://docs.voxel51.com/getting_started/install.html)

## Usage

Ask your AI assistant:

```
"Write a FiftyOne utility module that computes label statistics"
"Refactor this code to follow FiftyOne conventions"
"Help me write a custom dataset importer following FiftyOne patterns"
```

The skill applies FiftyOne's standard module structure, import ordering, logging setup, type hints, and docstring style.

## When to use

Use this skill when:
- Contributing code to the FiftyOne core repo
- Writing plugins that will be shared publicly
- Authoring code that integrates with FiftyOne's internal APIs
- Reviewing or refactoring existing FiftyOne-adjacent code

## See also

- [FiftyOne contributing guide](https://github.com/voxel51/fiftyone/blob/develop/CONTRIBUTING.md)
- [Plugin development docs](https://docs.voxel51.com/plugins/developing_plugins.html)
