---
name: plan-zoom-integration
description: Turn a Zoom integration idea into an implementation plan with architecture, auth, and delivery milestones. Use when you need a practical build plan, phased delivery sequence, risk list, and next-step recommendation.
argument-hint: "<what you want to build>"
user-invocable: false
---

# /plan-zoom-integration

> If you see unfamiliar placeholders or need to check which tools are connected, see [CONNECTORS.md](../../CONNECTORS.md).

Create a practical build plan for a Zoom integration or app.

## Usage

```text
/plan-zoom-integration $ARGUMENTS
```

## Workflow

1. Capture the target user flow and success criteria.
2. Choose the correct Zoom surface and supporting services.
3. Select the Marketplace app model and template, including ownership, scopes, products, events, callback URLs, and post-create setup. If the user asks to execute the plan, chain through [setup-zoom-marketplace-app](../setup-zoom-marketplace-app/SKILL.md) before OAuth or product implementation.
4. Define auth requirements, token lifecycle, and account assumptions.
5. Break implementation into phases: app registration, prototype, core integration, reliability, and launch.
6. Call out hard risks early: manifest drift, master-scope access, OAuth setup, webhook verification, SDK environment limits, marketplace review, or MCP client constraints.
7. End with the smallest deliverable that proves the architecture.

## Output

- Architecture summary
- Zoom products and APIs required
- Auth and scope checklist
- Delivery phases
- Risks, open questions, and immediate next action

## Related Skills

- [start](../start/SKILL.md)
- [setup-zoom-marketplace-app](../setup-zoom-marketplace-app/SKILL.md)
- [setup-zoom-oauth](../setup-zoom-oauth/SKILL.md)
- [build-zoom-meeting-app](../build-zoom-meeting-app/SKILL.md)
- [build-zoom-bot](../build-zoom-bot/SKILL.md)
