# APIs, permissions, and egress

Read this reference when calling or exposing Atlassian, Forge app, or external APIs, changing authorization context, scopes, providers, remotes, endpoints, content permissions, or egress.

Retrieve the exact current endpoint and permission documentation needed by the implementation. Choose user or app context according to whose authority the operation should use; protect app-context operations with appropriate backend authorization.

For external systems, select a supported integration pattern from current documentation. Distinguish outbound fetch or OAuth, Forge Remote, web triggers, and Forge app REST APIs; check lifecycle status and caller authentication rather than treating them as interchangeable. Account for credentials, egress, data residency, eligibility, and installation or version effects when they apply.

Use least-privilege scopes and narrowly necessary egress. Treat display conditions as presentation only. Keep tokens and runtime secrets out of manifests, frontend code, repositories, and chat.

Official entries:

- Permissions: <https://developer.atlassian.com/platform/forge/manifest-reference/permissions/>
- Atlassian app APIs: <https://developer.atlassian.com/platform/forge/apis-reference/product-rest-api-reference/>
- Forge app REST APIs: <https://developer.atlassian.com/platform/forge/app-rest-apis/>
- External authentication: <https://developer.atlassian.com/platform/forge/use-an-external-oauth-2.0-api-with-fetch/>
- Remotes: <https://developer.atlassian.com/platform/forge/manifest-reference/remotes/>
- App context security: <https://developer.atlassian.com/platform/forge/app-context-security/>
- Security: <https://developer.atlassian.com/platform/forge/security/>
