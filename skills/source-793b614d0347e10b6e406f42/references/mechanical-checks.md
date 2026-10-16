# Mechanical Checks — Detail

Objective, near-automatable checks. Run these first on any prompt review and flag every failure.

## Tool call budget

Maximum **20 tool calls** per agent. Flag any agent that exceeds it. OpenAI's broader reliability envelope is ≤100 tools and ≤20 args per tool; Synthflow caps at 20 tools. Too many tools for one workflow also causes mis-selection — recommend splitting the agent or consolidating overlapping tools.

## Prompt length (token gate)

| Tokens | Status |
|---|---|
| < 180k | Pass |
| 180k–200k | Warning |
| > 200k | **Fail — block release** |

If approaching the limit, the highest-leverage cuts are usually:
1. Redundant few-shot examples.
2. Rules repeated in 3+ places.
3. Verbose tone descriptions ("warm, friendly, conversational, approachable, helpful…" → "warm, conversational").

## Variable placement / cache discipline

**Rule:** fixed content first. In the body, reference variables **by name only — no curly braces**. Resolve them in a trailing block at the bottom.

✅ Good:

```text
[... fixed instructions, referring to caller_name, store_id, etc. by name ...]

<variables>
caller_name = {name}
store_id = {store}
appointment_time = {appointment_datetime}
</variables>
```

❌ Bad:

```text
"When the caller says hi, greet {name} and ask about their {vehicle}..."
```

**Why it matters:** the provider caches the prompt prefix that is identical to the previous call; caching stops at the first byte that differs. A `{name}` interpolated on line 3 means the entire rest of the prompt is uncached on every call — latency and cost rise. Backloading variables lets the cache cover everything up to that block, often 95%+ of the prompt. Flag any early inline `{variable}` as a Medium caching issue (or Medium regression if introduced by an edit).

## Rules placement

- ❌ Don't dump every rule into a "CRITICAL RULES — READ FIRST" block at the top.
- ✅ Put each rule next to the behavior it governs.
- ✅ Repeating the 2–3 most critical rules at the very end is fine and often helps.

If a top-of-prompt rules block runs longer than ~5 bullets, it is over-centralized — recommend distributing the rules to the steps they govern.

## Things the LLM physically cannot do

The model can't execute these, so writing them gets ignored or causes hallucinated tool calls. Flag every instance.

| ❌ Don't write | Why | What to do instead |
|---|---|---|
| "Use the knowledge base when answering about hours/products." | The KB is a **parallel process** — Synthflow runs it automatically. Restating it confuses the model and wastes tokens. | Just describe the answer behavior. The KB is wired in. |
| "Speak in a warm, friendly tone." | Tone is a TTS/voice property, not a language-model property. The system prompt can't shape it. | Put tone in the **speech instructions**, separate from the system prompt. |
| "Wait 5 seconds before responding." | The LLM has no clock and cannot pause. | Use a tool/action with a counter or timed event. |
| "Count how many times the caller interrupted." | The LLM cannot reliably count across turns. | Use a state variable updated by a tool, then reference the variable. |
| "Decide whether to end the call after thinking about it." | LLMs don't 'think' between turns; the next turn is fresh. | Use a hard gate (`IS_END_CALL_ALLOWED = ...`) that triggers an `end_call` tool. |
