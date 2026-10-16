# Documentation routing

Read this reference when current Forge platform detail is needed. Keep volatile schemas, commands, versions, packages, limits, and lifecycle labels out of local guidance.

Use Forge MCP first whenever it is available for current Forge platform guidance. Discover the capabilities exposed in the current session rather than assuming permanent tool names. Choose the narrowest useful MCP source: general guides for orientation, module discovery for candidate extension points, domain guides for architecture, and focused search for exact implementation facts.

For Atlaskit or Atlassian Design System decisions in Custom UI, use ADS MCP first when it is available. Do not use ADS MCP as a source for UI Kit components.

The skill and its scripts still work without either MCP server. If the preferred MCP server is unavailable, fails, or does not cover the required detail, use the exact official Atlassian documentation as fallback. Report the failed or unavailable lookup and any uncertainty that still affects the implementation.

Check lifecycle, changelog, deprecation, and migration information when using non-GA features or changing observed legacy behavior. Verify critical details against the latest official page even when MCP provides an answer.

## Official entry points

- Agent-readable index: <https://developer.atlassian.com/platform/forge/llms.txt>
- Forge MCP: <https://developer.atlassian.com/platform/forge/ai-development-toolkit/forge-mcp/>
- Getting started: <https://developer.atlassian.com/platform/forge/getting-started/>
- CLI: <https://developer.atlassian.com/platform/forge/cli-reference/>
- Manifest: <https://developer.atlassian.com/platform/forge/manifest-reference/>
- Modules: <https://developer.atlassian.com/platform/forge/manifest-reference/modules/>
- UI: <https://developer.atlassian.com/platform/forge/ui-kit/overview/>
- Functions: <https://developer.atlassian.com/platform/forge/function-reference/>
- Events: <https://developer.atlassian.com/platform/forge/events/>
- Storage: <https://developer.atlassian.com/platform/forge/storage-reference/>
- Environments: <https://developer.atlassian.com/platform/forge/environments-and-versions/>
- Security: <https://developer.atlassian.com/platform/forge/security/>
- Limits: <https://developer.atlassian.com/platform/forge/platform-quotas-and-limits/>
- Changelog: <https://developer.atlassian.com/platform/forge/changelog/>
- Deprecation policy: <https://developer.atlassian.com/platform/forge/deprecation-policy/>

Prefer an official Markdown representation when available. Never imply that MCP was consulted when it was not.
