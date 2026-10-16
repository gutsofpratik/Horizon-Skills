# SDK Guidance

Get expert FiftyOne Python SDK guidance for filtering, exporting, embeddings, and custom workflows, powered by live documentation search, with a training-knowledge fallback when that search isn't connected.

Live documentation search is supported by [Kapa.ai](https://www.kapa.ai), via Voxel51's public docs bot. It's optional; the skill works without it too.

## Install

```bash
curl -sL skil.sh | sh -s -- voxel51/fiftyone-skills
```

When prompted, select **fiftyone-sdk-guidance** from the menu.

## Requirements

- [FiftyOne](https://docs.voxel51.com/getting_started/install.html), to run the generated code
- *(Optional)* Voxel51's public [Kapa.ai docs MCP server](https://voxel51.mcp.kapa.ai) connected to your AI assistant, for live documentation search

### Connect the docs MCP server (optional but recommended)

This is a public, read-only documentation search endpoint; no Voxel51 API key required. The first time you connect, your AI assistant will prompt you to sign in with your own Google or GitHub account; that authenticates you directly with Kapa, not Voxel51, and nothing secret is stored in your config.

**Claude Code:** nothing to set up ahead of time, just ask a question. The skill notices the docs search tool isn't connected and offers to run this for you (with your confirmation):
```bash
claude mcp add --transport http --scope user fiftyone-docs https://voxel51.mcp.kapa.ai
```
New MCP servers only attach on the next session, so restart Claude Code (or start a fresh conversation) after it's added, then complete the one-time OAuth login on first use.

To add it yourself instead of waiting for the prompt, run the command above directly.

**Claude Desktop / Cursor**, add to your MCP config:
```json
{
  "mcpServers": {
    "fiftyone-docs": {
      "url": "https://voxel51.mcp.kapa.ai"
    }
  }
}
```

**VS Code**, add to `.vscode/mcp.json`:
```json
{
  "servers": {
    "fiftyone-docs": {
      "type": "http",
      "url": "https://voxel51.mcp.kapa.ai"
    }
  }
}
```

Without this connected, the skill still works; it answers from training knowledge and tells you when it's doing so.

## Usage

Ask your AI assistant:

```
"How do I filter my dataset by confidence in Python?"
"There's no operator for this, can you show me the SDK?"
"Write me a script to export my dataset to COCO format"
"What's the API for computing embeddings without a plugin?"
```

The assistant searches live FiftyOne documentation and returns accurate, runnable Python code tailored to your goal.

## What it covers

- Direct FiftyOne Python SDK questions (filtering, exporting, embeddings, splits, custom views)
- Fallback guidance when no operator or plugin exists for the user's goal
- Iterative doc search, refines the query until it finds a concrete answer
- Explicit "answering from training knowledge" disclosure when live docs search isn't connected

## See also

- [FiftyOne Python SDK](https://docs.voxel51.com/user_guide/basics.html)
- [FiftyOne User Guide](https://docs.voxel51.com/user_guide/index.html)
- [FiftyOne Cheat Sheets](https://docs.voxel51.com/cheat_sheets/index.html)
- [Discord community](https://discord.gg/fiftyone-community)
