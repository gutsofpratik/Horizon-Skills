# OpenClaude Skills

A public skill catalog for [OpenClaude](https://github.com/movedtodarkhaxop/OpenClaude): discover reusable instructions, inspect their source, and install the skills you need.

This repository distributes **skills**, not plugin bundles. Plugins remain connected to their upstream marketplaces. OpenClaude is an independent project and is not affiliated with or endorsed by Anthropic.

## What is here?

The current catalog contains **3,203 packaged skills**, drawn from the OpenClaude library and upstream collections. The catalog also records unavailable entries where a package cannot be redistributed; those entries are not installable downloads.

| Path | Contents |
| --- | --- |
| [`catalog.json`](catalog.json) | Machine-readable discovery entries and downloadable skill records |
| [`skills/`](skills/) | Extracted skill instructions, supporting files, and upstream license notices |
| [`packages/`](packages/) | ZIP packages used for installation |
| [`NOTICE.txt`](NOTICE.txt) | Repository scope and third-party licensing notice |
| [`LICENSE`](LICENSE) | MIT license for original OpenClaude repository contributions |

A skill typically includes a `SKILL.md` file describing when and how to perform a task. Some include scripts, templates, or other resources. Installing a skill makes its instructions available to the assistant; it does not install a model or automatically provide missing tools, dependencies, credentials, or permissions.

## Install in OpenClaude

1. Open **Customize → Skills → Discover**.
2. Search for a skill and open its details to review its instructions and requirements.
3. Click **Install skill**. Installed skills appear in **Yours** and become available for relevant tasks when enabled.

OpenClaude downloads the package from this repository. You can disable or uninstall a skill from your library. Skills that require a browser, document runtime, connector, or another dependency need that capability to be available in your app as well.

## Download or inspect a skill manually

Find its record in `catalog.json`. Each downloadable record in `skills` provides:

- `id`, `name`, and `description` for identification;
- `sourceUrl` and `sourceFamily` for provenance;
- `packagePath` for the ZIP download;
- `sha256` and `bytes` for checking the package;
- a license reference to the package's `UPSTREAM-LICENSE.txt`.

Open the matching folder under `skills/` to read the files before downloading the ZIP from `packages/`. To use a downloaded package in OpenClaude, use **Import** in the Skills library. Other assistants may use different layouts and installation procedures; compatibility is not guaranteed.

For automation, resolve `packagePath` relative to this repository. Verify the downloaded ZIP against its catalog SHA-256 before extracting it. Pin a Git commit when you need reproducible installations; the default branch can change.

## Sources and attribution

The catalog draws from:

- [Anthropic's official Claude plugin marketplace](https://github.com/anthropics/claude-plugins-official), including skills from linked upstream projects;
- [Claude Skills Collection](https://github.com/abubakarsiddik31/claude-skills-collection);
- original OpenClaude skill contributions.

Individual skill records link to their actual upstream source. Being listed through a marketplace does not mean a third-party skill was authored or audited by Anthropic or OpenClaude. Restricted packages are excluded from redistribution.

## Licensing

**There is no single blanket license for all skills in this repository.**

The root [MIT license](LICENSE) applies to original OpenClaude-authored repository material, including original documentation and catalog organization, to the extent OpenClaude contributors hold those rights. It does not relicense third-party skill instructions, scripts, templates, assets, or packages.

For each third-party skill, read its `UPSTREAM-LICENSE.txt` and any additional notices included with the skill. Those upstream terms continue to apply. Keep attribution and required license notices when using or redistributing a package. Original authors retain their rights.

## Review before use

Skills are executable guidance for an AI assistant and may include scripts. Review their contents, upstream source, and requested access before installation. A skill's instructions do not authorize external actions or override your application's permission controls. Never place API keys, passwords, or private chat data in a public skill contribution.

## Corrections and contributions

[Open an issue](https://github.com/movedtodarkhaxop/OpenClaude-Skills/issues) for a broken package, attribution error, licensing concern, or catalog correction. Include the skill ID and source URL. For a contribution, provide the skill instructions, supporting files, provenance, and an explicit redistribution license. Do not submit proprietary skill packs, credentials, or complete plugin bundles.

For the desktop and web application, visit [OpenClaude](https://github.com/movedtodarkhaxop/OpenClaude).
