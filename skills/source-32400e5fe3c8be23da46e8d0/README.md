# Issue Triage

Triage FiftyOne GitHub issues: validate status, categorize, and generate responses automatically.

## Install

```bash
curl -sL skil.sh | sh -s -- voxel51/fiftyone-skills
```

When prompted, select **fiftyone-issue-triage** from the menu.

## Requirements

- [FiftyOne](https://docs.voxel51.com/getting_started/install.html)
- [GitHub CLI](https://cli.github.com/) (`gh`) authenticated

## Usage

Ask your AI assistant:

```
"Triage issue #7234 in the FiftyOne repo"
"Check if this bug report has already been fixed"
"Review the last 10 open issues and categorize them"
```

The skill fetches the issue, searches related commits and issues, assesses the current status, and drafts a response.

## Categories

| Category | Description |
|---|---|
| Already Fixed | Resolved in a recent commit or release |
| Won't Fix | By design, out of scope, or external behavior |
| Not Reproducible | Cannot reproduce with provided information |
| No Longer Relevant | Stale, deprecated, or outdated version |
| Still Valid | Confirmed bug or valid feature request |

## See also

- [FiftyOne GitHub Issues](https://github.com/voxel51/fiftyone/issues)
- [Contributing guide](https://github.com/voxel51/fiftyone/blob/develop/CONTRIBUTING.md)
