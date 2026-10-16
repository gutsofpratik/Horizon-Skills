# Troubleshoot

Diagnose and fix common FiftyOne issues: dataset persistence, App connectivity, MongoDB errors, video codecs, and more.

## Install

```bash
curl -sL skil.sh | sh -s -- voxel51/fiftyone-skills
```

When prompted, select **fiftyone-troubleshoot** from the menu.

## Requirements

- [FiftyOne](https://docs.voxel51.com/getting_started/install.html)

## Usage

Ask your AI assistant:

```
"My dataset disappeared after restarting, how do I get it back?"
"The FiftyOne App won't open, it just hangs"
"I'm getting a MongoDB connection error"
"Video samples show a codec error in the App"
"My operator is registered but not showing up in the App"
```

The skill identifies the root cause, explains what went wrong and why, proposes a fix, and waits for your confirmation before applying anything.

## Covered issues

- Dataset persistence and MongoDB connectivity
- App launch failures and port conflicts
- Plugin and operator not appearing
- Video codec incompatibilities
- Notebook connectivity (`fo.launch_app` in Jupyter)
- Performance issues with large datasets

## See also

- [FiftyOne FAQ](https://docs.voxel51.com/faq/index.html)
- [Discord community](https://discord.gg/fiftyone-community)
