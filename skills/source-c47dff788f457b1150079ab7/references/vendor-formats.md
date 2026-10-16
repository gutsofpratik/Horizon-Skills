# What the existing routes actually do

Reference for Step 0. These routes disagree on every structural key, because
each vendor specified its own — so this table is a record of what was verified
per vendor, never a template to copy from. The disagreement extends to whether a
vendor has a manifest at all.

| | Claude Code | Cursor | Kimi Code | Codex | OpenCode | Pi | Factory Droid |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Route kind | manifest | manifest | manifest | manifest | **package** — installed from this repo with `opencode plugin add github:postmanlabs/postman-plugin` | **package** (npm) — the installer's own | manifest |
| Manifest | `.claude-plugin/plugin.json` | `.cursor-plugin/plugin.json` | `.kimi-plugin/plugin.json` | `.codex-plugin/plugin.json` | `opencode/package.json`, whose version the root `package.json` repeats; that root file names the entrypoint `opencode plugin add` loads — no plugin-manifest format exists | the `pi` key in `installer/package.json` | `.factory-plugin/plugin.json`, metadata only — Droid installs by marketplace entry, from `.factory-plugin/marketplace.json` |
| Skills pointer | *(implicit — no key)* | `"skills": "skills"` | `"skills": ["./skills"]` | `"skills": "./skills/"` | plugin code: v1 appends the packaged dir to `skills.paths`, v2 calls `skill.transform` | `"pi": { "skills": ["./skills"] }`, staged into the tarball at pack time | *(implicit — `skills/` at the plugin root)* |
| MCP config | `"mcpServers": "./mcp.claude-code.json"` | `"mcpServers": "./mcp.cursor.json"` | inline object | `"mcpServers": "./mcp.codex.json"` | `mcp.opencode.json`, read by the plugin at runtime | `mcp.pi.json`, registered by the extension with `pi.registerMcpServer()` | `mcp.json` at the plugin root — no manifest key |
| MCP header key | `headers` | `headers` | `headers` | `http_headers` | `headers` | `headers` | `headers` |
| Transport key | `"type": "http"` | *(none)* | `"transport": "http"`, `"auth": "oauth"` | `"type": "http"` | `"type": "remote"`, `"enabled": true` (v2 takes `"disabled": false`) | `"type": "http"` | `"type": "http"` |
| URL mode segment | `/mcp` | `/mcp` | `/minimal` | `/mcp` | `/minimal` | `/mcp` | `/mcp` |
| `version` key | yes | yes | yes | yes | `version` in `opencode/package.json` | `version` in `installer/package.json` | yes, metadata only — a git install is tracked by commit |
| Hooks | `hooks/hooks.json` discovered | manifest `hooks`, falls back to `hooks/hooks.json` | inline `hooks` array only — **no file discovery** | manifest `hooks`, falls back to `hooks/hooks.json` | **no `hooks.json`** — the plugin pushes the mandate into the system prompt | **no hooks file** — the extension adds the mandate as a prompt section on `before_agent_start` | `hooks/hooks.json` discovered, in Claude Code's `hooks`-wrapped shape |
| Published schema | SchemaStore | `cursor/plugins` repo | none | none — prose docs only | `opencode.ai/config.json`, draft2020, `$ref`s `models.dev` — validates `mcp.opencode.json` | none | none — prose docs only |
| Extras | `$schema` | — | `interface` block | `interface` block | no host-version gate for a local plugin; the minimum is documented | `pi-package` keyword lists it in the gallery; `pi.image` is the card's preview | the marketplace is named after the repo or directory, not the file's `name` |

## Per-route notes worth knowing before you add another

**Codex falls back to other routes' manifests.** Its
`DISCOVERABLE_PLUGIN_MANIFEST_PATHS` is `.codex-plugin`, `.claude-plugin`,
`.cursor-plugin`, in that order, so it loaded this repo before it had a route of
its own. That fallback is not a substitute for one: it would read
`mcp.claude-code.json`, whose `headers` key Codex does not understand, and the
traffic arrives with no `X-Source` at all.

**`http_headers` is the sharpest edge in the repo.** Codex deserializes a
plugin's MCP config into its own `RawMcpServerConfig`, which has only
`http_headers` and carries `#[schemars(deny_unknown_fields)]` — schemars, for
schema generation, not serde. So serde ignores unknown keys: a `headers` block
in `mcp.codex.json` is dropped without an error, the server still connects, and
every request goes out unattributed. It looks exactly like success. `headers` is
right for every other route; do not normalize Codex to it.

**Cursor's `mcpServers` pointer is load-bearing.** Without it Cursor discovers
root `mcp.json`, which is Factory Droid's, and its traffic arrives as
`postman-factory-plugin`. The pointer replaces that discovery rather than adding
to it. `defaultMcpConfig` in `scripts/routes.js` makes the guard fail on a
manifest that drops it. Claude Code is the opposite: its pointer loads alongside
a root `.mcp.json`, so that file must not exist.

**Kimi's `interface` block and Codex's are not the same thing** even though they
share a name — each vendor defines its own fields. Check the vendor's docs
rather than copying the block.

**OpenCode loads plugins as code, never from a manifest.** A checked-in
`opencode.json` only ever reached users who ran OpenCode inside a clone. The
route is a local plugin instead: a clone of this repo plus a one-line file in
OpenCode's `plugins/` directory that re-exports `opencode/src/index.ts`. OpenCode
runs the TypeScript directly and the source has only type imports, so nothing
is built or installed, and nothing is published to npm.

**OpenCode's `skills.paths` is in its schema but not its docs.** A docs-only pass
concludes no pointer exists and discovery is fixed-path only. It does exist:
relative entries are joined to the directory OpenCode started in, with no walk
up to the project root; `~/` is expanded; a missing directory logs "skill path
not found" and continues; each entry is scanned for `**/SKILL.md`. v1's config
hook appends the packaged directory as an absolute path, which sidesteps the
start-directory rule. Enumerate the schema's properties; do not infer absence
from prose.

**No route expands `${...}` inside an MCP URL.** `claude plugin list --json`
reports the registered URL with any placeholder still in the path, Cursor has no
such plugin variable in a URL, and the Agent Plugins spec is explicit that only
`${PLUGIN_ROOT}`/`${PLUGIN_DATA}` expand and never in a URL. If the mode ever
needs to be configurable, resolve it at build time or behind a stdio wrapper.
