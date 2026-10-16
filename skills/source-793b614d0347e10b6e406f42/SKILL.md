---
name: prompt-review
description: Review AI voice-agent prompts, especially Synthflow Single-Prompt, for contradictions, missing context, unsafe tool/action behavior, escalation gaps, compliance risk, and regression risk. Use this when the user asks to review, audit, validate, improve, or compare a prompt before deployment.
---

# Prompt Review Skill

## Purpose

Review an AI agent prompt before it is tested, deployed, or edited in production. Focus on whether the prompt is reliable, specific, safe, aligned with available tools/actions, and suitable for real customer conversations.

Especially useful for Synthflow voice agents, Single-Prompt agents, Flow Designer node prompts, transfer flows, escalation logic, support/sales/qualification/booking agents, and any prompt that controls call behavior.

## Getting the material over MCP

When the prompt lives in a Synthflow workspace rather than in the conversation, pull it with the Synthflow MCP tools: `get_agent` for the live prompt and settings, `get_agent_actions` / `get_action` for the action descriptions the prompt must agree with, and `list_agent_versions` / `get_agent_version_diff` when comparing an edit for regression risk. To check how a Synthflow feature actually works, search the official docs with `search_docs`, or with the `searchDocs` tool on the `synthflow-docs` server if the workspace tools aren't connected yet.

## Core Review Philosophy

A good prompt is understandable by a human operator with no hidden context.

**The "another human" test** (OpenAI's recommended check): read the prompt aloud to a teammate. If they can't restate what the agent should do in plain English, the LLM won't reliably do it either.

Write so an **18-year-old with zero context** could execute it the same way twice. Prefer concrete behavioral instructions over vague personality instructions.

- Bad: `Be helpful and professional.`
- Better: `Use one or two sentences per turn. Ask one question at a time. If the caller asks about pricing, give the approved price range and ask whether they want to book a consultation.`

Replace vague verbs with specific, testable behavior:

| ❌ Vague | ✅ Specific |
|---|---|
| "Handle the caller professionally" | "One sentence per turn, mirror their tone, no slang" |
| "Help them find the right battery" | "Ask year/make/model/trim, then present 2 in-stock SKUs with price + warranty" |
| "Verify the customer" | "Collect name, phone, order ref. Read each back. Ask 'is that correct, yes or no?'" |
| "Be helpful" | (delete — not actionable) |

## Background / Behavior / Output structure

A Synthflow prompt should split cleanly into three sections, **in this order, with headers**:

| Section | Contains |
|---|---|
| **Background** | Who the agent is, company, situation, store/account context, policies, role, goal, caller context, variables, customer-specific restrictions |
| **Behavior** | Conditional logic, flows, "if X then Y", tool/action triggers, booking/transfer/escalation/fallback/end-call rules, objection and error handling |
| **Output** | Sentence length, format, language, spoken forms for numbers/dates/money — formatting only |

Common misplacements to flag: conditional rules inside Output ("if commercial caller, transfer"); a "Critical Rules" block at the top mixing all three. If a flow's "output" is a tool call, that lives in **Behavior**, not Output.

**Caveat — deterministic step-by-step flows:** many enterprise customers write "step 1, 2, 7" prompts. The split still applies, but Output collapses to formatting/styling only. State this assumption rather than forcing a restructure.

## Run the mechanical checks first

These are objective and near-automatable. Flag any failure.

- **Tool budget:** ≤ 20 tool calls per agent.
- **Token length:** < 180k pass · 180k–200k warning · > 200k **fail, block release**.
- **Variable / cache discipline:** fixed content first; reference variables **by name only, no curly braces** in the body; resolve them in a trailing block. Early inline `{vars}` break prompt caching (Medium regression).
- **Rules placement:** no fat "CRITICAL RULES — READ FIRST" block; put each rule next to the behavior it governs; repeating only the 2–3 most critical at the end is fine.
- **Physically-impossible instructions:** the LLM has no clock, can't count across turns, can't "think" between turns, and shouldn't be told to "use the knowledge base" (it's a parallel process Synthflow runs automatically) or to adopt a tone (tone lives in speech instructions, not the system prompt).

Full detail and the fix-it table: **`references/mechanical-checks.md`**.

## Review scope

Review every prompt for these categories. Detailed checklists per category are in **`references/review-checklists.md`** — read it when working through findings.

1. **Contradictions / duplicated instructions** — instructions that can't both be true, across the whole prompt.
2. **Missing business context / unclear role boundaries** — does the agent know enough to do the job safely and consistently?
3. **Tool, action, transfer, knowledge instructions** — trigger, exact name, arguments/enums, return/empty/error handling, sibling disambiguation, confirmation before writes. **Prompt and the Synthflow UI action-description must agree.** If tools/descriptions aren't provided, mark the review `Needs available-tool context` and incomplete — do not invent them. Action-description authoring rules: see **`references/action-descriptions.md`**.
4. **Transfer / escalation / fallback / call-ending** — every such path needs a trigger and a safe confirmation point. Replace "end the call when appropriate" with a hard gate.
5. **Compliance, safety, customer-specific risk** — regulated advice, sensitive data, consent, guarantees, AI-identity disclosure. Prefer 3–5 strong operational guardrails over long negative lists.
6. **Regression risk** (when comparing an edit) — removed context/triggers/guardrails, changed thresholds, behavior moved into Output, weakened examples, variable changes that hurt caching.

## Severity levels

- **Critical** — unsafe behavior, compliance exposure, unauthorized data collection, wrong transfers, hallucinated tool calls, production-breaking. (e.g. collects card numbers; regulated advice when disallowed; non-existent tool in core workflow; books without confirmation; contradictory core-workflow instructions; no fallback for a failed critical tool; can end call before completion; > 200k tokens.)
- **High** — likely inconsistent or fails in common scenarios. (missing business hours for booking; ambiguous trigger; unclear transfer path; undefined required fields; prompt/description conflict; missing objection handling; no recovery for empty results.)
- **Medium** — works but reliability/maintainability/UX issues. (vague instructions; duplicated rules; long tone descriptions; misplaced rules; behavior in Output; missing spoken-formatting; early inline `{vars}`; physically-impossible instruction.)
- **Low** — minor polish.

## Review method

1. **Identify the agent type** (Single-Prompt, Flow node, transfer node, tool instruction, KB-heavy, booking, qualification, support, sales, receptionist, internal QA). State assumptions if unclear.
2. **Extract the intended workflow** in plain English. If you can't, flag missing context.
3. **Map content** into Background / Behavior / Output / Guardrails / Variables / Examples / Tool descriptions. Flag misplacements.
4. **Run the mechanical checks** (above).
5. **Check specificity** — for each vague instruction: could the agent do it two ways? Is there a trigger, a success condition, a failure path? Rewrite into concrete behavior.
6. **Check tool/action alignment** against available tools and their UI descriptions. Flag prompt-vs-description conflicts. Incomplete without descriptions.
7. **Check transfer and end-call gates.**
8. **Check compliance and safety** for the industry; if unknown, apply general support guardrails and flag industry compliance as missing.
9. **Check examples** — happy path, edge case, error recovery; flag examples that contradict instructions.
10. **Check regression risk** if old and new versions are provided; recommend simulations.

## Output format

Produce the review using the structure in **`references/output-template.md`** (executive summary → findings → missing information → regression risks → recommended tests → optional improved prompt). That file also contains the scoring rubric and a worked example finding.

Keep findings actionable — every finding includes a concrete recommendation, not "make this clearer."

## Special rules

- **Do not invent business logic** — no invented pricing, policies, legal requirements, transfer targets, or tools. Flag missing info and give a safe placeholder.
- **Do not over-rewrite** — default is review, not rewrite. Only rewrite if the user asks, or the fix is small and local and doesn't require inventing policy.
- **Preserve intent** — business goal, agent identity, tone, workflow, tool names, compliance constraints, still-valid examples.
- **Prefer small, testable changes** — one behavior at a time; recommend simulations/test calls before deploying production prompts.

## Final reminder

A review is complete only when it answers: (1) what could go wrong in a real call, (2) why, based on the prompt, (3) how the prompt should change, (4) what to test before deployment.

Give a **maximum of 5** improvement suggestions. After the final report, ask the user whether they want you to apply the changes.
