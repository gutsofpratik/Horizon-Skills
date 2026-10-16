# Custom UI and Frame

Read this reference only for Custom UI or browser content embedded through UI Kit `Frame`.

Confirm that the selected module supports the UI approach. Use current documentation to establish the resource and build boundary, bridge or resolver boundary, and any relevant CSP or egress requirements.

When the implementation uses Atlaskit or Atlassian Design System components, tokens, or icons, use ADS MCP as the first preference when it is available. Use official ADS documentation as fallback. Do not apply ADS or Atlaskit packages to UI Kit.

Preserve a supported existing frontend toolchain. Keep secrets and privileged operations out of browser code. Build production resources before Forge validation and ensure manifest resources point to the intended output. Retrieve current internationalization and accessibility guidance when the requested experience requires them.

Official entries:

- Custom UI: <https://developer.atlassian.com/platform/forge/custom-ui/>
- Resources: <https://developer.atlassian.com/platform/forge/manifest-reference/resources/>
- Bridge APIs: <https://developer.atlassian.com/platform/forge/apis-reference/ui-api-bridge/bridge/>
- Permissions and CSP: <https://developer.atlassian.com/platform/forge/manifest-reference/permissions/>
- Translations: <https://developer.atlassian.com/platform/forge/manifest-reference/translations/>
- Tunnelling: <https://developer.atlassian.com/platform/forge/tunneling/>
