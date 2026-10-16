---
description: Fix a failing Vanta compliance test by generating code changes and opening a pull request
argument-hint: test ID or Vanta test URL
---

Fix the failing Vanta test specified in $ARGUMENTS.

## Steps

1. **Parse the test ID.** If `$ARGUMENTS` is a URL (e.g., `https://app.vanta.com/c/<slug>/tests/<testId>`), extract the test ID from the path. If it's a plain string, use it directly as the test ID.
2. **Get remediation context.** Call `getAgentRemediationPrompt` with the test ID and follow instructions. 
3. **Follow the returned prompt.** The `getAgentRemediationPrompt` response contains a system prompt and user message with test-specific remediation intelligence. Follow these instructions to scan the local repository and generate the fix.

## Edge cases

- **Test ID not found:** Call `tests` to fetch the failing tests list, fuzzy-match against the provided ID, and present the closest matches. "I couldn't find a test called `[id]`. Did you mean one of these?" Never dead-end.
- **Test is already passing:** "This test is currently passing. No remediation needed." Then show the failing tests list so the user can pick something else.
- **Malformed or non-test URL:** "I couldn't parse a test ID from that URL." Then show the failing tests list.
- **Ambiguous description (no ID):** If `$ARGUMENTS` doesn't match a test ID, call `tests` and filter by keyword. If one match, proceed. If multiple, show candidates with entity counts and ask which one. If none, show the full failing tests list.
- **No IaC files in directory:** "I have the fix for this test, but I don't see any IaC files in this directory." Offer options: open Claude Code in the right repo, generate new Terraform files, or provide CLI commands.
- **IaC files found but no matching resources:** "I found Terraform files, but none manage the failing resources." Offer: import + fix, fix in a different repo, or CLI commands.
