# Validation and release

Read this reference when validating a completed change or when deploy, install, upgrade, promotion, or production configuration was requested. Route a broad pre-deploy or release-readiness assessment to `forge-app-review`; use this reference for validation during build work and explicitly authorized release actions.

Use the repository's relevant tests and checks, and build Custom UI resources when applicable. Follow the core manifest-validation invariant. Do not deploy merely to compensate for missing local validation.

Before a consequential Forge command, retrieve its current documentation and confirm the exact app, environment, site, product, authorization, and any material version, permission, installation, migration, compatibility, licensing, or data effect. Retrieve the exact version, bulk-upgrade, rollout, sharing, or Marketplace guidance when the requested action implicates it. Never infer a live target or choose among multiple targets on the user's behalf.

For an explicitly authorized development deployment or installation, the retained helper can install dependencies, run `forge lint`, deploy, and install:

```bash
python3 -m scripts.deploy_forge_app \
  --app-dir <app-directory> \
  --site <confirmed-site> \
  --product <confirmed-product> \
  --env <confirmed-environment>
```

Run the helper from the skill directory. It checks the local Node.js, Forge CLI, authentication, and app registration state; installs dependencies unless `--skip-deps` is set; runs `forge lint`; deploys; and installs only when installation was requested. It detects Jira and Confluence requirements from manifest modules and scopes and installs on every detected product in addition to the confirmed primary product. Confirm those products before invoking an authorized installation; detection does not replace user authorization or exact-target confirmation.

The helper does not replace repository tests, type checks, or a required Custom UI production build. Run those checks before the helper when applicable.

Use `--deploy-only` when installation was not authorized. Do not use this helper for bulk upgrades, promotions, or production rollout decisions; retrieve and execute the exact current CLI workflow for those operations.

Report the validation performed and its results. For release actions, also report the exact app, environment, site, products, action, outcome, and any verification that remains.

Official entries:

- CLI: <https://developer.atlassian.com/platform/forge/cli-reference/>
- Environments and versions: <https://developer.atlassian.com/platform/forge/environments-and-versions/>
- Deploy: <https://developer.atlassian.com/platform/forge/cli-reference/deploy/>
- Install: <https://developer.atlassian.com/platform/forge/cli-reference/install/>
- Version commands: <https://developer.atlassian.com/platform/forge/cli-reference/version/>
- Distribution: <https://developer.atlassian.com/platform/forge/distribute-your-apps/>
