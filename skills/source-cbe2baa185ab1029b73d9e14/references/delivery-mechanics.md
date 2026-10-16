# Delivery mechanics

A prompt is text plus how it is sent. Cover the relevant items here when the
deployment is an API call or an agent harness. Skip all of it for chat UI prompts.

## Which parts are provider-specific

Each section below is tagged. Check the tag before repeating a claim to a user on
a different platform, because the specifics here are the fastest-moving part of
this skill.

- **[universal]** holds across providers and is a property of how transformers
  handle context, not of any one API.
- **[anthropic]** is documented Claude API behaviour. Other providers solve the
  same problem differently, and the error codes and limits will not match.
- **[varies]** exists everywhere but with different names, defaults, and
  constraints. Verify against the target provider's current documentation.

## Turn placement [universal, caching details anthropic]

Role, instructions, constraints, and examples belong in the system prompt.
Variable input belongs in the user turn. This also makes the static portion
cacheable. Caching follows the hierarchy tools, then system, then messages, and a
change at any level invalidates that level and everything after it. So order
everything stable first and everything per-request last.

## Long input ordering [universal]

When source material exceeds roughly 20k tokens, place it *above* the
instructions and the query rather than below. Putting the query at the end can
improve response quality substantially on complex multi-document inputs. This is
one of the highest-leverage structural choices available and it costs nothing.

## Document wrapping [anthropic-flavoured, principle universal]

XML tags are the Claude convention; on other providers use Markdown headers or
explicit delimiters instead. What transfers is the principle: give each source an
addressable identity and a stated origin, so the model can cite and separate
them. With multiple sources:

    <documents>
      <document index="1">
        <source>annual_report_2023.pdf</source>
        <document_content>{{ANNUAL_REPORT}}</document_content>
      </document>
    </documents>

For long-document tasks, having the model first extract relevant quotes into a
`<quotes>` block and then work from those cuts through surrounding noise.

## Structured output [varies, limits below are anthropic]

Do not enforce a schema through prompt text when the API offers a real mechanism.
Every major provider has one, under different names. On Claude, two distinct
features exist and solve different problems: JSON outputs constrain what the
model says, and strict tool use constrains how it calls your functions. They
combine in one request. The numeric limits and failure modes below are Claude's;
the shape of the advice transfers, the numbers do not.

Strict tool use constrains the *shape* of a call, not *whether* it happens.
Forcing the call with `tool_choice` set to `any` or to a named tool returns a
400 on Claude Sonnet 5.5 per Anthropic's documentation, and OpenRouter's
migration guide reports the same for Opus 5.5 (both as of October 2026). Keep `tool_choice` at `auto`, set `strict: true`
for schema-valid input, state in the prompt when the tool applies, and check
that a call was actually made, retrying if not. When the structured result is
the deliverable rather than an action, structured outputs are the better fit:
they constrain the response itself and need no call to happen at all.

- Prefer required fields over optional ones, and mark only the tools that matter
  as strict. Optional parameters and union types are what blow up grammar
  compilation, and the limits apply per request across all schemas, not per tool.
- Unsupported schema features fail with a 400 rather than degrading gracefully:
  recursive schemas, numeric and string length constraints, external references,
  and `additionalProperties` set to anything but `false`. Constraints the schema
  cannot express belong in field descriptions and in the eval.
- Enum matching is not case-exact in the output. Compare case-insensitively, and
  never define two enum values differing only in capitalisation.
- The grammar constrains the final response only, not tool calls or thinking
  blocks, so the model still reasons freely.
- Changing the output format invalidates the prompt cache for that thread, and
  JSON outputs are incompatible with citations.

Where no API mechanism applies, examples remain the strongest lever, ahead of
describing the format in prose.

## Prefill is gone [anthropic]

On Claude, prefilling the final assistant turn is no longer supported on 4.6 and
later and returns a 400 error. Never recommend it there. Some other providers
still allow assistant-turn continuation, so check before ruling it out
elsewhere; the migrations below are better practice regardless. Migrations for the four things
people used it for:

- Forcing a format: structured outputs, a strict tool schema under
  `tool_choice: auto` (forcing the call itself is no longer accepted either), or
  simply instructing the format, which newer models match reliably, with
  retries.
- Killing preambles: "Respond directly without preamble", or wrap the answer in
  an XML tag and extract it, or strip it in post-processing.
- Continuations: move the continuation into the user turn, quoting the
  interrupted text, or just retry.
- Context re-injection in long sessions: inject into the user turn, or hydrate
  through a tool.

Prefilling extended thinking was never allowed and still is not.

## Conversation history is append-only [anthropic]

On Claude Sonnet 5.5 a thinking block is tied to everything before it, per
Anthropic's documentation as of October 2026; check the target model's own page
before assuming the same elsewhere. A request that replays such a block after the
system prompt, the tool list, or an earlier message was edited can return a 400,
and on accounts created on or after 31 August 2026 that check is on by default. Harnesses that rewrite their system prompt between turns, or that
trim old messages in place, break here first.

Keep history append-only. To change instructions or tools mid-run, send a
mid-conversation system message rather than editing what came before. This
belongs in the delivery notes of any agentic prompt whose harness edits context.

## Refusals are a stop reason, not an empty answer [anthropic]

A declined request returns HTTP 200 with `stop_reason: "refusal"` and a category
naming the policy area. A pipeline that only reads the text sees an empty or
short response and treats it as a bad answer, which sends you tuning a prompt
that was never the problem. Check the stop reason before grading or retrying,
and report refusals separately. The same applies to `stop_reason: "max_tokens"`:
on models where thinking always runs, `max_tokens` covers thinking plus the
answer, so a budget sized for the answer alone truncates it.

## Testing note [universal]

Re-test after any model, snapshot, or effort change. Prompt behaviour is
version-specific, and a prompt tuned on one snapshot can regress on the next.
