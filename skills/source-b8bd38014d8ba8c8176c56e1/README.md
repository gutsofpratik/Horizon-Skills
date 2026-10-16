# Eval Plugin

Evaluate any FiftyOne plugin for quality, security, and agent-readiness. Get a structured report with scores and actionable recommendations.

## Install

```bash
curl -sL skil.sh | sh -s -- voxel51/fiftyone-skills
```

When prompted, select **fiftyone-eval-plugin** from the menu.

## Requirements

- [FiftyOne](https://docs.voxel51.com/getting_started/install.html)

## Usage

Ask your AI assistant:

```
"Evaluate the @voxel51/brain plugin"
"Audit this plugin I just built before I share it"
"Check this community plugin for security issues"
"Review my plugin for agent-readiness"
```

The skill reads every source and configuration file in the plugin, checks for security patterns, code quality, and operator design, then produces a structured report with a score and specific recommendations.

## What gets checked

- Security: dangerous code patterns, input validation, secret handling
- Code quality: operator structure, error handling, schema definitions
- Agent-readiness: operator descriptions, input/output clarity, executability

## See also

- [Plugin development docs](https://docs.voxel51.com/plugins/developing_plugins.html)
- [FiftyOne Plugins](https://github.com/voxel51/fiftyone-plugins)
