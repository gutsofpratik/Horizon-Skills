# Forge App Security Review Skill

Performs white-box security reviews for Atlassian Forge apps using a structured ruleset and evidence-first reporting.

## Skill Files

- `SKILL.md`: Triggering, workflow, and reporting instructions for agent hosts
- `assets/security-rules/`: Global and category Forge security rules used by the skill

## Rule Layout

- `assets/security-rules/_global-forge.mdc`
  - Global baseline for every Forge white-box review.
- `assets/security-rules/forge-*/_index-*.mdc`
  - Category index files that point to deeper subrules.
- `assets/security-rules/forge-*/*.mdc`
  - Category-specific deep checks.

Current categories:

- `forge-authn-authz/`
- `forge-injection/`
- `forge-tenant-isolation/`
- `forge-secrets-storage/`
- `forge-egress-remotes/`
- `forge-manifest-config/`
- `forge-webtrigger-entrypoints/`
- `forge-auditing/`
- `forge-rovo-agents/`
- `forge-misc/`

## Usage Flow

1. Read `manifest.yml` first.
2. Apply `assets/security-rules/_global-forge.mdc`.
3. Load only relevant category index rules under `assets/security-rules/forge-*/_index-*.mdc` based on manifest/code signals.
4. Load deep subrules only when index detection heuristics match observed code patterns.
5. Trace each finding from source to sink with evidence.
6. Report validated findings with exploitability, impact, CWE mapping, and test leads.

### Token-Efficient Rule Loading

This skill now uses a two-tier loading model:

- Tier 1: global baseline + selected category indexes
- Tier 2: on-demand deep subrules only for triggered heuristics

This avoids loading all rule files up front and reduces token usage during large reviews.

### Focused Review Mode

When the user asks for a narrow scope (for example only AuthN/AuthZ), load only:

- `assets/security-rules/_global-forge.mdc`
- the requested category index
- matching subrules in that category

Still call out obvious critical findings outside the requested category.

## Example Prompts

### 1) Full Forge app security review

```text
Perform a white-box security review of this Forge app source code.
Apply:
1) assets/security-rules/_global-forge.mdc
2) Relevant category index and subrules under assets/security-rules/forge-*/
```

### 2) Focused AuthN/AuthZ review

```text
Perform a focused AuthN/AuthZ review of this Forge app.
Apply:
- assets/security-rules/_global-forge.mdc
- assets/security-rules/forge-authn-authz/_index-authn-authz.mdc
- related forge-authn-authz subrules
```

### 3) Tenant isolation and leakage review

```text
Perform a tenant isolation and data leakage review for this Forge app.
Apply:
- assets/security-rules/_global-forge.mdc
- assets/security-rules/forge-tenant-isolation/_index-tenant-isolation.mdc
- assets/security-rules/forge-secrets-storage/_index-secrets-storage.mdc
```

### 4) Full static analysis scans

```text
Review this Forge app with FULL execution of assets/security-rules/forge-auditing/static-analysis-forge.mdc.
Requirements:
1) Apply assets/security-rules/_global-forge.mdc and all relevant forge-* index/subrules.
2) Execute the complete static-analysis workflow from the subrule, including:
   - FSRT scan
   - Semgrep (javascript/typescript/node + Forge custom rules if available)
   - npm audit
   - Snyk test
   - gitleaks detect
3) If a tool is missing, install it and continue (tell me what was installed).
```
