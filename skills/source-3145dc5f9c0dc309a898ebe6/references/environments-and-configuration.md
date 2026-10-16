# Environments and configuration

Read this reference when selecting or creating an environment, changing runtime variables or secrets, using manifest interpolation, or making configuration environment-specific.

Distinguish manifest variables resolved by the CLI from runtime environment variables read by app code. Retrieve the current syntax, environment behavior, and deployment requirements before implementation.

Keep secrets out of source, manifests, frontend bundles, logs, command history, and chat. Use supported encrypted variables or secret storage according to the consumer and lifecycle. Do not set or replace a production value without explicit authorization and a confirmed app, environment, key, and impact.

Remember that environment configuration is scoped and may not be copied by deployment. Validate that every target environment has the required non-secret configuration, and report secret names or presence without exposing values.

Official entries:

- Environments and versions: <https://developer.atlassian.com/platform/forge/environments-and-versions/>
- Environment variables: <https://developer.atlassian.com/platform/forge/environments-and-versions/#environment-variables>
- Manifest variables: <https://developer.atlassian.com/platform/forge/manifest-reference/variables/>
- CLI variables: <https://developer.atlassian.com/platform/forge/cli-reference/variables/>
