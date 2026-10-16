# Review Checklists — Detail

Detailed checklists for each review category. Work through the relevant ones while assembling findings.

## 1. Contradictions and duplicated instructions

Find instructions that can't both be true or that create inconsistent behavior, looking across the *whole* prompt:

- "Always transfer billing questions" + "Answer billing questions yourself."
- "Always upsell installation" + "Never push extras unless asked."
- "Book in available slots" + "Only book during business hours" — without defining business hours.
- "End the call after completing the task" + "Always ask if there is anything else."
- "Never collect payment information" + "Ask for the credit card number."

Also flag duplicated instructions when repetition creates risk, bloats the prompt, or places the same rule in multiple sections with slightly different wording.

For each contradiction explain: the conflicting instructions, why they conflict, the likely production failure, and a recommended resolution.

## 2. Missing business context or unclear role boundaries

Flag missing or unclear: company name, agent name, agent role, primary business goal, caller type, offer/service details, eligibility criteria, pricing policy, refund/cancellation/warranty/booking rules, business hours, service area, required fields, data retention/consent requirements, what the agent may answer, what it must not answer, and when it should defer to a human.

If the agent could reasonably interpret its role two different ways, flag it.

## 3. Tool, action, transfer, and knowledge instructions

For every tool/action instruction, check it has: a clear trigger condition; the exact tool/action name; required arguments; valid values/enums when applicable; what the tool returns; what the agent says before the call; what it says after a successful result; what it does on an empty result; what it does on failure; and whether the tool should or should not be used for similar cases.

Flag unsafe tool behavior:
- Tool calls based on guessed information.
- Booking without confirmation.
- Creating/updating/deleting records without caller confirmation.
- Transferring without explaining the reason.
- Sending SMS/email without consent when required.
- Collecting sensitive data before verifying collection is allowed.
- Calling unavailable tools or hallucinated tool names.
- Prompt instructions that conflict with the tool/action description.
- Overlapping tools without disambiguation.
- More than 20 tools.

If the list of available tools/actions is not provided, **do not invent it.** Mark the issue `Needs available-tool context`, explain what's required, and treat the tool-reliability review as incomplete.

**Prompt ↔ action-description agreement:** in Synthflow each action/transfer/KB has a UI description the model uses to decide whether to call the tool. If the prompt and the description conflict, the agent follows one inconsistently. Keep operational detail in the UI description; in the prompt, reference the tool by name and user-facing intent only. For how to write these descriptions, see `action-descriptions.md`.

## 4. Transfer, escalation, fallback, call-ending

Check for clear rules: when to transfer, which transfer action, whether to ask permission first, what to say before transferring, what to do if transfer fails, when to escalate to a human, when to offer a callback, when to create a ticket, when to end the call, what to do after repeated misunderstanding or repeated tool failure, how to handle abusive/threatening callers, and how to handle out-of-scope requests.

Replace vague rules like "End the call when appropriate." with a hard gate:

```text
Only use `end_call` after one of these is true:
1. The caller confirms they need nothing else.
2. The caller declines help twice.
3. The caller continues abusive language after one warning.
4. A transfer or ticket has completed and the caller confirms the call can end.
```

## 5. Compliance, safety, customer-specific risk

Check for risks involving: medical/legal/financial/insurance advice; employment/housing/credit decisions; payment or credit-card data, passwords, full date of birth, national IDs/SSNs, health information; minor safety; fraud/identity verification/account access; consent for calls/recordings/SMS/email/marketing; jurisdiction-specific requirements; customer-specific prohibited claims; overpromising or guarantees; disclosing internal policies; claiming to be human if the agent is AI.

Prefer 3–5 strong, operational global guardrails over long negative lists:

```text
Never collect credit card numbers, passwords, full date of birth, national IDs, or social security numbers. If the caller tries to provide them, politely interrupt and explain the agent cannot collect that information.
```

If the industry is unknown, apply general support guardrails and flag industry-specific compliance as missing context.

## 6. Regression risk (when comparing an edit)

Compare old and new. Flag: removed business context; removed tool trigger; changed transfer/escalation thresholds; changed compliance guardrail; behavior rules moved into Output; added vague instructions; added conflicting examples; tone changes that increase latency; variable-placement changes that hurt caching; removed edge-case/recovery examples; new customer-facing promises without policy support; changed call-ending rules; changed required data collection.

Classify each by severity and recommend targeted tests or simulations before deployment.

## Examples to look for in any prompt with tools

Look for at least three example types: happy path, edge case, and error recovery. Flag examples that contradict the main instructions. Examples should show tool calls and tool outcomes when tools are part of the workflow.
