---
name: setup-agent-analytics
description: >-
  Set up Pendo agent analytics in a codebase — detect the AI agent(s) and
  instrument them so prompts, responses, and reactions flow to Pendo. Reads the
  codebase to choose the best of four installation paths: the Python SDK, the
  TypeScript SDK, client-side window.pendo.trackAgent(), or the server-side
  Conversations API. Use this whenever the user wants to add, install, wire up,
  or "instrument" Pendo agent analytics / agent tracking / trackAgent, mentions
  capturing LLM or chatbot conversations for Pendo, or asks how to get their AI
  agent's data into Pendo — even if they don't name the specific method.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

You are setting up Pendo agent analytics for this codebase. There are **four instrumentation paths** and your first job is to route to the right one. Only after the path is chosen do you scan for agents and wire up tracking.

Arguments: `$ARGUMENTS` may contain one or more Pendo agent IDs (space-separated). If provided, use them when instrumenting (first ID → first agent; order detected agents stably by main-file path, and show the ID↔agent mapping when confirming Phase 1 findings). If there are fewer IDs than detected agents, use `"YOUR_AGENT_ID"` as a placeholder for the extras. If no IDs are provided, use `"YOUR_AGENT_ID"` for all agents and tell the user to replace them after creating agent IDs in the Pendo UI.

---

## Phase 0: Route to the right instrumentation path

The four paths, in priority order (prefer the earlier path when multiple could fit):

| Path | When to use | What the user imports |
|------|-------------|----------------------|
| **A. Python SDK** | Python code anywhere in the stack (FastAPI, Flask, Django, Jupyter, LangChain/LangGraph apps, standalone scripts) — including Python backends behind a web or mobile frontend | `pendo-server-sdk` (pip) |
| **B. TypeScript SDK** | Node/TypeScript backend you can modify (Express, Fastify, Nest, standalone Node, TS LangChain/LangGraph) — including TS backends behind a web or mobile frontend | `pendo-server-sdk` (npm) |
| **C. Web client-side** | Browser frontend (React, Vue, Angular, Next.js, Nuxt, SvelteKit, plain HTML/JS) when **there's no backend to instrument** (static SPA calling LLM APIs directly) or when the user explicitly wants client-only signals (prompt chips, file upload, reaction UI) on top of backend tracking | `window.pendo.trackAgent()` (no import) |
| **D. Server-side Conversations API** | Mobile apps (React Native, Flutter, iOS native, Android native, Expo) or browser extensions **with no Python/TS backend you control**; also web apps **without Pendo core installed**, via a first-party proxy endpoint (D.6) — last resort when Paths A–C all don't fit | Direct HTTPS POST to `/data/agentic` |

### Step 1: Auto-detect the path

**Priority order (prefer the earlier path when multiple fit):**

1. **Path A — Python SDK** (strongest preference)
2. **Path B — TypeScript SDK**
3. **Path C — Web client-side**
4. **Path D — Server-side Conversations API** (last resort)

Rationale: SDK paths auto-trace LLM calls and tool usage with no per-call wiring; the raw Conversations API requires manual event construction. Prefer SDKs whenever the runtime supports them.

Look at the project root and apply the priority order:

- `pyproject.toml` / `requirements.txt` / `setup.py` / `.py` files dominant → **Path A (Python SDK)**
- `package.json` with TS/Node code → **Path B (TypeScript SDK)** — even if a web frontend is present, prefer instrumenting the backend over the browser
- `package.json` with a web frontend framework (`react`, `vue`, `@angular/core`, `next`, `nuxt`, `svelte`) and **no server code you can modify** → **Path C (Web client-side)** — subject to the Pendo-core precondition below
- `package.json` with `react-native` / `expo`, `pubspec.yaml` with `flutter`, `.xcodeproj` / `AppDelegate.swift`, `build.gradle` with `com.android.application`, or `manifest.json` with `manifest_version` → **Path D (server-side Conversations API)**, unless the mobile/extension app has a Python or TS backend you control — in that case prefer Path A or B on the backend.

**Ambiguous cases — still apply the priority order, and confirm with the user:**

- **Monorepo** (`packages/`, `apps/`, or workspaces): if multiple paths apply, pick the highest-priority path that covers the agent's orchestration (usually backend). List what you found and ask the user to confirm or expand to additional surfaces.
- **Hybrid** (web frontend + Node/Python backend in same repo): default to **Path A or B** (backend SDK) — this hides agent IDs from the browser and gives richer auto-traced spans. Tell the user: "I'm instrumenting the backend so agent IDs stay server-side. If you want to capture client-only signals (prompt-chip clicks, file attachments, reaction UI state), say so and I'll add Path C on top."
- **Next.js / Nuxt / SvelteKit with server routes** (the most common web repo shape — it matches both the "TS/Node code" and "web framework" rules above): decide by *where the LLM orchestration runs*. In server code (API routes, server actions, Nitro/Node endpoints) → **Path B**, with `init()` in a Node-runtime entry point (Next.js: `instrumentation.ts`, Node runtime only — the SDK's monkey-patching and batch processor don't run on the edge runtime; for edge routes use the Path D helper instead). Only when the browser calls the LLM provider directly is this a Path C case (snippet precondition applies) or a D.6 proxy case.
- **Static/JAMstack site with no backend** (pure React/Vue/Angular SPA calling third-party LLM APIs directly from the browser): **Path C** is the only option.
- **Mobile / extension with a backend you control**: instrument the backend via Path A or B. Only fall to Path D if the mobile app calls the LLM provider directly with no intermediary.

### Path C precondition — verify Pendo core is installed

`window.pendo.trackAgent()` rides on the Pendo agent (the install snippet). If the agent never initializes on the page, every `trackAgent()` call **silently no-ops** — no error, no data, nothing to debug. Before committing to Path C:

1. **Grep the repo** for snippet markers: `pendo.initialize`, `cdn.pendo.io/agent`, `@pendo/agent`, `pendo.js`.
2. **Found** → proceed with Path C.
3. **Not found** → do not assume it's missing: many teams load Pendo via a tag manager (GTM, Segment, Adobe Launch), which never appears in a repo grep. **Ask the user:** "I can't find the Pendo install snippet in this repo — is Pendo loaded via a tag manager? If yes I'll proceed with `trackAgent()`; if Pendo isn't installed at all, I'll add the install snippet first (from Pendo → Settings → Install Settings) or instrument a backend instead if you have one."
4. **If Pendo is genuinely not installed, Path C cannot work** — do not wire up `trackAgent()` calls that can never fire. Reroute instead; agent analytics does not require Pendo core (Paths A, B, and D all post directly to Pendo's ingestion endpoints):
   - Offer to **add the install snippet** (Pendo → Settings → Install Settings) as part of this setup — smallest change, and unlocks the rest of Pendo alongside agent analytics.
   - Otherwise use the **server-side Conversations API (Path D) behind a first-party endpoint** (see D.6). Never call `/data/agentic` from browser code — the Track Event shared secret must not ship client-side — but hybrid frameworks (Next.js API routes, Nuxt server routes, SvelteKit `+server.ts`, Remix actions) can host the helper even in an otherwise "frontend-only" repo, and the client fires events at that endpoint instead of `window.pendo.trackAgent()`.
   - Only a truly static site with no server runtime anywhere (GitHub Pages, S3) and no snippet has no safe option besides installing the snippet.

### Step 2: Present the detected path and confirm

State the detected path in one line ("I'll use the **Python SDK** path — this is a FastAPI project") and ask the user to confirm or redirect before you scan for agents. Skip this only if the user already specified the path in their prompt.

---

## Phase 1: Detect AI agents

This step is the same regardless of path. Scan for conversational AI/LLM agent code — not just any use of an LLM API.

### Find LLM SDK usage

Search for imports/references to:

```
openai | @openai | anthropic | @anthropic-ai | @google/generative-ai | @google-ai
@mistralai | cohere-ai | @aws-sdk/client-bedrock-runtime | langchain | langgraph | @langchain
@ai-sdk | ai | ollama | llamaindex | @huggingface
api.openai.com | api.anthropic.com | generativelanguage.googleapis.com
```

**Match these as import/package specifiers** (`from "ai"`, `require("openai")`, `import anthropic`, `from langchain...`), not bare substrings — short names like `ai` and `openai` as raw greps over-match wildly.

**Exclude dependency and lock files from results** — they declare libraries, not usage. Filter out matches in: `pyproject.toml`, `poetry.lock`, `requirements.txt`, `Pipfile`, `Pipfile.lock`, `setup.py`, `setup.cfg`, `package.json`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `Gemfile`, `Gemfile.lock`, `go.mod`, `go.sum`, `Cargo.toml`, `Cargo.lock`, and any `__pycache__` / `node_modules` / `dist` / `build` directories. A library listed in `pyproject.toml` but never imported in code is not an agent.

### Trace to the orchestrator

For each LLM call site, follow the import chain to the **orchestration layer** — the service or component that manages the conversation. Signals:

- **Message handling**: `sendMessage`, `handleUserInput`, `processResponse`, `streamChat`, `generateResponse`, `chat_completion`, `agent.invoke`, `agent.ainvoke`, `AgentExecutor`
- **Conversation state**: arrays of messages with `role`/`content`, `conversationHistory`, `chat_history`, `messages=[...]`
- **Chat UI** (web only): `<Chat*`, `<Conversation*`, `<Assistant*`, `<MessageThread*`, `<Copilot*`
- **Streaming / feedback UI** (web/mobile): `isStreaming`, `onToken`, `handleThumbsUp`, `handleRegenerate`

### Disambiguate

**Not agents:**
- LLM client wrappers (`LLMClient`, `AIProvider`, `LangChainService`)
- Legacy/unused LLM code not imported by any live conversation path
- Prompt loaders, token counters, response parsers
- HTTP user-agent strings, service workers

If `ChatService` imports `LangChainService` which wraps OpenAI, that's **one** agent, not three.

Files named `agent.*` are only candidates if they also contain the signals above — "agent" appears in many non-AI contexts.

**Supervisor / subagent / multi-agent architectures (LangGraph, multi-agent systems, router patterns):**

Do **not** treat every subagent, every LangGraph node, or every tool-using LLM call as a separate Pendo agent. The Pendo `agent` is the **user-facing product surface** — usually one per app, sometimes a small handful (e.g. "Support Assistant", "Code Reviewer", "Onboarding Copilot") that users perceive as distinct features.

Rules of thumb:

- If the app exposes **one chat/assistant UI** backed by a supervisor routing to many subagents internally → **one** Pendo agent. Instrument at the API boundary (the handler that receives the user message). LangChain's inheritable configure hook and LangGraph's context propagation mean subagents, subchains, and nested tool calls are auto-traced without per-node instrumentation.
- If the app exposes **multiple distinct user-facing assistants** (separate UIs, separate entry points, separate Pendo agent IDs in the UI) → one Pendo agent per surface. Instrument each API boundary with its own `agent_id`.
- **Never** instrument every LangGraph node, every `AgentExecutor` call inside a supervisor tree, or every tool-using subagent as a separate Pendo agent. That produces N agent IDs for one product and breaks conversation aggregation.

When in doubt, ask the user: "This repo has a supervisor routing to N subagents behind one chat UI. I'll treat it as one Pendo agent instrumented at the API boundary — confirm, or list the separate user-facing surfaces you want to track?"

### Web-only: find CSS selectors (Path C only)

**Skip unless Path C.** For each agent identify:

1. **Input selector** — the `<textarea>`, `<input>`, or `contenteditable`
2. **Submit selector** — the send button

Priority: analytics/testid attributes → stable IDs → BEM class → ARIA roles → stable component classes. Avoid CSS-in-JS hashes (`css-1a2b3c4`, `Component_class__hash`, `sc-...`) and positional `:nth-child(n)`.

### Report and confirm

Present findings per agent (name, main file, LLM provider, orchestrator entry point, response handler, feedback handler, selectors if Path C). **Ask the user to confirm before Phase 2.** If no agents found, stop.

---

## Phase 2: Instrument

### Idempotency check (all paths)

Before writing code, grep the codebase (excluding `__pycache__`, `node_modules`, `dist`, `build`, lockfiles) for any of:

```
# Path A (Python SDK)
pendo_sdk | pendo-server-sdk | @trace_llm | @trace_tool | pendo_sdk\.(init|set_context|set_identity|langchain_turn|close_turn|record_reaction|get_tracer|flush|shutdown)

# Path B (TypeScript SDK) — check for the import first; bare API names like
# init( match every Node codebase, so only inspect call sites when the
# package is actually imported
pendo-server-sdk | pendoSdk\s*\.\s*(init|setIdentity|setContext|withContext|withLangchainTurn|langchainTurn|recordReaction|closeTurn|getTracer|flush|shutdown)\s*\( | traceLlm | traceTool

# Path C / D (Conversations API)
trackAgent | trackAgentEvent | window\.pendo\.trackAgent | /data/agentic | x-pendo-integration-key
```

If any match lands in a real source file (not a lockfile, not a commented-out sample), report what you found with the file paths and ask the user whether to **skip** (leave as-is), **update** (fill gaps, e.g. add response tracking to an agent that only has prompt tracking), or **replace** (remove existing and rewrite). Never double-instrument.

### Shared concepts (all paths)

All four paths send the same event model to Pendo. Before you start, understand these fields — they apply to every path even though the surface differs.

**Event types** (what you're tracking):

| Event | When | Content |
|-------|------|---------|
| `prompt` | User submits a message | The user's message text |
| `agent_response` | Agent finishes responding | The agent's reply text |
| `user_reaction` | User reacts (👍/👎/retry) | `"positive"`, `"negative"`, `"unreact"` (documented vocabulary); `"copy"`, `"retry"`, `"edit"` pass through |

**Core identifiers:**

- **`agentId`** — constant per agent (from Pendo UI or `$ARGUMENTS`)
- **`conversationId`** — generated **once per conversation session** and reused for every message in it. Reset on "New Chat", conversation switch, or session refresh.
- **`messageId`** — unique per message. Use existing IDs if the app has them, else `uuid`/`crypto.randomUUID()`. For `user_reaction`, use the **original message's ID**, not a new one.
- **`visitorId`** / **`accountId`** — required for server-side paths (B, D); pulled from auth/session context. Must match what Pendo uses elsewhere.

**Content length:** Do **not** add your own truncation. Paths C/D: send the complete message/response text — the `/data/agentic` ingest endpoint accepts full content. Paths A/B: the SDKs already truncate trace/turn content client-side (2048 chars) by design; don't pre-truncate on top of that.

**Optional metadata** — only include when the value is real. Never hardcode. Detection rules:

| Field | How to wire it |
|-------|----------------|
| `agentModelsUsed` | Array of model(s) from the LLM SDK `model` parameter, config variable, or response object (`response.model`), e.g. `[config.model]`. Not a hardcoded string. |
| `suggestedPrompt` | Only if the UI has prompt chips/suggestions. Set `true` on the chip click path, `false` on manual input. Omit entirely if no such UI. |
| `fileUploaded` | Only if the UI has file upload. Reference actual state (`attachments.length > 0`). Omit if no upload. |
| `toolsUsed` | Extract from the SDK response (`response.tool_calls`, `content.filter(b => b.type === "tool_use")`). Omit if no tool calling. |

Every optional field: **wire to real value or omit** — never hardcode a placeholder.

---

## Path A: Python SDK (`pendo-server-sdk`)

**Install:** `pip install pendo-server-sdk` (mention this to the user; don't run pip yourself unless they ask).

### A.1 — Initialize once at startup

Find the app's entry point (`main.py`, `app.py`, `manage.py`, FastAPI `app = FastAPI()` declaration, Django `settings.py`-adjacent init, or a module imported on boot). Add:

```python
import pendo_sdk

# Guarded so a missing env var disables analytics instead of crashing boot.
if os.environ.get("PENDO_API_KEY"):
    pendo_sdk.init(
        api_key=os.environ["PENDO_API_KEY"],
        agent_id="AGENT_ID",               # from $ARGUMENTS or "YOUR_AGENT_ID"
        project_id="support-agent",        # OTel service.name for grouping — NOT the agent identity
        # endpoint defaults to https://app.pendo.io — only set for eu/regional stacks
        # visitor_id / account_id: set per-request (A.2), not here
    )
```

- `init()` is idempotent-safe (warns on duplicate calls) and **auto-patches** Anthropic, OpenAI, OpenAI Responses API, Gemini, and LangChain when those libraries are importable (`auto_patch=True` default).
- Document the `PENDO_API_KEY` env var. Tell the user to set it.

**What auto-patching gets you varies by provider.** Pendo has two data surfaces: the **trace waterfall** (GENERATION/TOOL_REQUEST spans) and the **Conversations tab** (prompt / agent_response events). Auto-patch alone does not fill both for every provider:

| Setup | Traces | Conversations |
|-------|--------|---------------|
| LangChain/LangGraph via `set_context()` / `langchain_turn()` | ✅ auto | ✅ auto |
| Direct Gemini (patched) + `set_identity()` per request | ✅ auto | ✅ auto (turn accumulator) |
| Direct Anthropic / OpenAI (patched) alone | ✅ auto — GENERATION spans only | ❌ **none** — wrap the entry point with `@trace_llm` (A.3) |
| Raw OTel spans (no patcher) | manual | manual (A.6) |

The Anthropic/OpenAI patchers only create GENERATION spans; they never populate the turn accumulator, so with them alone the Conversations tab stays empty — no error, no warning. Always pair them with `@trace_llm` on the outermost LLM-calling function.

### A.2 — Per-request identity + conversation ID

**LangChain / LangGraph apps** — use `set_context()` in the handler that receives each user message. It creates a per-request callback handler, auto-injects it into all LangChain calls in the block, and handles the full turn lifecycle (prompt event on entry, agent_response rollup + flush on exit):

```python
with pendo_sdk.set_context(
    visitor_id=current_user.email,      # whatever Pendo uses as visitor ID
    account_id=current_user.org_id,     # optional but recommended
    conversation_id=thread_id,          # reuse across a conversation session
):
    response = agent.invoke({"input": message})
    # all LangChain calls inside this block are auto-traced
```

**Direct Anthropic / OpenAI / Gemini apps (no LangChain)** — `set_context()` is LangChain-specific; use `set_identity()` instead (call once at the top of the handler, no `with` block — propagates via contextvars):

```python
pendo_sdk.set_identity(
    visitor_id=current_user.email,
    account_id=current_user.org_id,
    conversation_id=thread_id,
)
```

- For **Gemini**, this is sufficient: the patcher accumulates the turn and the prompt/agent_response pair is emitted at the next turn boundary (`set_identity()`, `close_turn()`, `flush()`, or `shutdown()`).
- For **Anthropic/OpenAI**, `set_identity()` alone stamps identity on trace spans but produces **no conversation events** — the turn accumulator is never populated for these providers, so `flush()` has nothing to emit. You must also wrap the outermost LLM-calling function with `@trace_llm` (A.3). The conversation_id must be resolvable when that function is called (via `set_identity()` or a `conversation_id` kwarg on the function) — otherwise the decorator skips the turn and you silently get traces only.

**LangGraph, supervisor patterns, multi-agent systems:** LangGraph builds on `langchain_core`, and the SDK's LangChain patcher uses `register_configure_hook(inheritable=True)`, so callbacks propagate automatically through `StateGraph` nodes, subgraphs, supervisors, and handoff tools. **Instrument once at the API boundary**, not at each node or subagent. A single `set_context()` around the top-level `agent.invoke()` / `graph.ainvoke()` / FastAPI route handler traces the entire tree.

### A.3 — `@trace_llm` / `@trace_tool` decorators

`@trace_llm` wraps a function in a GENERATION span — **and**, when it's the outermost LLM call and a conversation_id is resolvable, it opens a `conversation.turn` root and emits the prompt + agent_response conversation events itself. This makes it the standard way to get Conversations coverage for direct Anthropic/OpenAI apps and for custom/non-patched LLM clients:

```python
@pendo_sdk.trace_llm(name="answer_user")
def answer_user(prompt: str, conversation_id: str):
    return anthropic_client.messages.create(...)  # patched call enriches this span
```

- The prompt text is auto-detected from kwargs named `llm_content` / `prompt` / `messages` / `contents` / `input` / `user_message` / `query` (override with `content_kwarg="..."`). **Both conversation_id and prompt text must resolve** — if the function's param has a different name (`text`, `message`, positional-only), the decorator opens no turn and you silently get traces only. When wrapping an existing function, check its signature and pass `content_kwarg` if the param isn't in the list. The return value's `.model` and `.usage` fields populate model and token metadata.
- **Safe to combine with auto-patching**: patched Anthropic/OpenAI clients detect the active `@trace_llm` span and enrich it instead of opening a nested duplicate GENERATION span. Do **not** hand-create GENERATION spans around a `@trace_llm`-decorated function — that path does duplicate.
- Nested `@trace_llm` calls don't open extra turns — only the outermost emits conversation events.

`@trace_tool` wraps tool functions (database lookups, vector search, third-party APIs) in a TOOL_REQUEST span — **trace waterfall only**, it never produces conversation events:

```python
@pendo_sdk.trace_tool(name="search_docs")
def search_docs(query: str) -> list[dict]:
    return db.search(query)
```

Call tools from inside the traced generation/turn so the TOOL_REQUEST span nests under the GENERATION span in the waterfall (see A.6 for why siblings break the hierarchy). `@pendo_sdk.trace_subagent` exists for subagent call boundaries in custom orchestrators.

### A.4 — Reactions (thumbs up/down, retry)

The SDK doesn't auto-detect reactions — call `record_reaction()` in the reaction handler (it's standalone: no surrounding `set_context`/turn needed, and it flushes itself):

```python
pendo_sdk.record_reaction(
    conversation_id=thread_id,
    reaction_type=pendo_sdk.ReactionType.THUMBS_UP,   # THUMBS_DOWN, UNREACT, COPY, RETRY, EDIT
    message_id=assistant_message_id,   # must match the messageId of the agent_response being reacted to
    feedback_comment=comment or None,  # optional free text
    visitor_id=current_user.email,
    account_id=current_user.org_id,
)
```

Do **not** build reaction spans by hand — the exporter keys off `pendo.span.type="REACTION"` and `reaction.type`, which `record_reaction()` sets correctly.

### A.5 — Turn boundaries and shutdown

- **Short-lived scripts / serverless:** call `pendo_sdk.shutdown()` before exit — it flushes any pending turn-anchored conversation events *and* shuts down the provider in one call. Don't combine `flush()` + `tracer_provider.force_flush()` + `tracer_provider.shutdown()` by hand — that risks double-export.
- **Long-running servers:** the BatchSpanProcessor exports on its own interval, but a Gemini-patched conversation's final turn sits in the accumulator until the next boundary. Call `pendo_sdk.close_turn(conversation_id)` at the end of each request to emit it promptly (cheap, targeted, non-blocking). `@trace_llm` and `set_context()` turns emit on exit and don't need this.

### A.6 — Raw OTel spans (only when nothing above fits)

If code must emit spans manually (no patcher, no decorator), the exporter has strict, **silent** requirements:

- **One trace per turn:** create a root span named exactly `conversation.turn` with `pendo.span.type="AGENT"` and `message.role="system"`, and create all other spans as its descendants (`start_as_current_span`). The exporter suppresses this root from the wire and promotes its children — without it, every span gets its own trace ID and the waterfall can't group them.
- **Nesting is structural:** TOOL_REQUEST spans must be *children of the GENERATION span*, not siblings — the exporter clears parent references to the suppressed root, so siblings all become top-level nodes and tools won't nest under the LLM call.
- **Conversation events key off attributes, and missing ones drop events with no error:**
  - prompt event: span needs `pendo.span.type="USER_MESSAGE"` or `message.role="user"`; set `message.content` or the prompt lands empty
  - agent_response event: span needs `message.role="assistant"` — an `ASSISTANT_RESPONSE` span type *without* that role is dropped entirely
  - `tool.name` on the ASSISTANT_RESPONSE span (comma-joined) populates the Conversations "Tools Used" widget
  - stamp `pendo.conversation_id`, `pendo.visitor_id`, `pendo.message_id` on every span

Prefer `@trace_llm` over this — it produces exactly this structure.

---

## Path B: TypeScript SDK (`pendo-server-sdk`)

**Install:** `npm install pendo-server-sdk` (tell the user; don't run it yourself unless asked).

### B.1 — Initialize once at startup

In the app's entry point (`index.ts`, `server.ts`, `app.ts`):

```typescript
import * as pendoSdk from "pendo-server-sdk";

// Guarded so a missing env var disables analytics instead of crashing boot.
if (process.env.PENDO_API_KEY) {
  pendoSdk.init({
    apiKey: process.env.PENDO_API_KEY,
    agentId: "AGENT_ID",               // from $ARGUMENTS or "YOUR_AGENT_ID"
    projectId: "support-agent",        // OTel service.name for grouping — NOT the agent identity
    // endpoint defaults to https://app.pendo.io — only set for non-prod stacks
  });
}
```

`init()` auto-patches Anthropic, OpenAI, Gemini (`@google/genai`), and LangChain when those packages are installed (`autoPatch: true` default). The same two-surface caveat as Path A applies:

| Setup | Traces | Conversations |
|-------|--------|---------------|
| LangChain/LangGraph via `setIdentity()` / `setContext()` | ✅ auto | ✅ auto |
| Direct Gemini (patched) + `setIdentity()` per request | ✅ auto | ✅ auto (turn accumulator) |
| Direct Anthropic / OpenAI (patched) alone | ✅ auto — GENERATION spans only | ❌ **none** — wrap the entry point with `traceLlm` (B.3) |
| Raw OTel spans | manual | manual (same contract as A.6) |

### B.2 — Per-request identity + conversation ID

`setIdentity()` is the primary per-request API — call it once at the top of the request handler; it propagates through the whole async chain via AsyncLocalStorage. For LangChain apps it also auto-injects a callback handler in auto-turn mode, so no wrapping is needed:

```typescript
app.post("/chat", async (req, res) => {
  pendoSdk.setIdentity({
    visitorId: req.user.email,
    accountId: req.user.orgId,
    conversationId: req.body.threadId,
  });
  const response = await agent.invoke({ input: req.body.message });
  // ...
});
```

- **LangChain**: `setIdentity()` alone is sufficient — turn boundaries (prompt event, agent_response rollup, flush) are detected from LangChain's callback lifecycle. If the auto-injection can't reach your calls (ESM/CJS split with `@langchain/core`), pass callbacks explicitly: `agent.invoke(msgs, { callbacks: pendoSdk.getCallbacks() })`, or use the explicit wrapper `setContext(opts, async (handler) => ...)` / `withLangchainTurn(opts, fn)`.
- **Direct Gemini**: `setIdentity()` is sufficient for conversations — the patcher feeds a turn accumulator; the prompt/agent_response pair is emitted at the next turn boundary. Call `pendoSdk.closeTurn(conversationId)` at the end of the request so the final turn isn't stranded until the next boundary.
- **Direct Anthropic / OpenAI**: `setIdentity()` alone stamps identity on trace spans but produces **no conversation events** — these patchers never feed the turn accumulator. Also wrap the outermost LLM-calling function with `traceLlm` (B.3). The conversationId must be resolvable when that function runs, or you silently get traces only.

**LangGraph, supervisor patterns, multi-agent systems:** LangGraph builds on `@langchain/core`, which the SDK patches via an inheritable callback hook. Callbacks propagate through `StateGraph` nodes, subgraphs, and handoff tools automatically. **Instrument once at the API boundary** (the route handler), not at each node. A single `setIdentity()` (or `setContext()` wrapper) around the top-level invocation traces the entire tree.

### B.3 — `traceLlm` / `traceTool` wrappers

`traceLlm(name, fn, options?)` wraps a function in a GENERATION span — **and**, when it's the outermost LLM call and a conversationId is resolvable (via `setIdentity()` or an arg), opens a `conversation.turn` root and emits the prompt + agent_response conversation events itself. This is the standard way to get Conversations coverage for direct Anthropic/OpenAI apps and custom LLM clients:

```typescript
import { traceLlm, traceTool } from "pendo-server-sdk";

const answerUser = traceLlm("answer_user", async (args: { prompt: string }) => {
  return anthropic.messages.create(...);  // patched call enriches this span
});
```

- The prompt text is auto-detected from a string argument or an object argument's `llmContent` / `prompt` / `messages` / `contents` / `input` / `userMessage` / `query` key (override with `{ contentKey: "..." }`). **Both conversationId and prompt text must resolve** — an unrecognized arg shape means no turn, silently. Check the wrapped function's signature and pass `contentKey` if needed. The return value's `.model` and `.usage` fields populate metadata.
- Patched clients detect the active `traceLlm` span and enrich it instead of nesting a duplicate GENERATION span — safe to combine. Don't hand-create GENERATION spans around a `traceLlm`-wrapped function.

`traceTool(name, fn)` wraps tool functions in a TOOL_REQUEST span — **trace waterfall only**, never conversation events. Call tools from inside the traced generation/turn so they nest in the waterfall. `traceSubagent(name, fn)` exists for subagent boundaries.

### B.4 — Reactions

Call `recordReaction()` in the reaction handler — standalone, no surrounding context needed:

```typescript
pendoSdk.recordReaction({
  conversationId: threadId,
  reactionType: "thumbs_up",         // thumbs_down, unreact, copy, retry, edit
  messageId: assistantMessageId,     // must match the agent_response being reacted to
  feedbackComment: comment,          // optional free text
  visitorId: req.user.email,
  accountId: req.user.orgId,
});
```

Do **not** build reaction spans by hand — the exporter keys off `pendo.span.type="REACTION"` and `reaction.type`, which `recordReaction()` sets correctly.

### B.5 — Turn boundaries and shutdown

- **Short-lived scripts:** call `pendoSdk.shutdown()` before exit — it drains pending turns and shuts down the provider in one call.
- **Serverless (Lambda, Cloud Functions):** caution — the current TS SDK's `shutdown()`/`flush()` are fire-and-forget (they don't return the export promise), and the runtime freezes at return, so events flushed on the way out can be dropped. Call `flush()` as early as possible (right after the turn completes, before building the response), and tell the user this is a known limitation until the SDK exposes an awaitable flush.
- **Long-running servers:** call `pendoSdk.closeTurn(conversationId)` at the end of each request for direct-Gemini apps (see B.2); LangChain and `traceLlm` turns emit on their own.

---

## Path C: Web client-side (`window.pendo.trackAgent`)

**Precondition (from Phase 0): the Pendo install snippet must be on the page** — verified in the repo, confirmed via tag manager, or added as part of this setup. Without it every `trackAgent()` call silently no-ops. You add a helper and fire events from client components.

### C.1 — Add the helper

Place in a shared utility file (`src/utils/pendo.ts`, `src/lib/pendo.ts`):

```typescript
declare global {
  interface Window {
    pendo?: {
      trackAgent: (eventType: string, metadata: Record<string, unknown>) => void;
    };
  }
}

let warnedMissingPendo = false;

export function trackAgentEvent(
  eventType: "prompt" | "agent_response" | "user_reaction",
  metadata: {
    agentId: string;
    conversationId: string;
    messageId: string;
    content: string;
    agentModelsUsed?: string[];
    suggestedPrompt?: boolean;
    toolsUsed?: string[];
    fileUploaded?: boolean;
  }
): void {
  try {
    if (typeof window === "undefined") return;
    if (!window.pendo?.trackAgent) {
      if (!warnedMissingPendo) {
        warnedMissingPendo = true;
        console.warn(
          "[pendo] trackAgent unavailable — agent events are being dropped. " +
            "Is the Pendo install snippet on this page?"
        );
      }
      return;
    }
    // Send full content — do not truncate client-side.
    window.pendo.trackAgent(eventType, { ...metadata });
  } catch {
    // Analytics failure must never break the product
  }
}
```

The helper is SSR-safe (`typeof window === "undefined"` no-ops) and swallows errors so analytics can't break the UI — but it warns **once** when the Pendo agent is missing, so a page without the snippet fails loudly in the console instead of silently dropping every event.

### C.2 — SSR / framework notes

- **Next.js App Router:** only instrument files with `"use client"`. If the agent logic is in a server action/route, instrument the **client-side caller**, not the server code.
- **Nuxt:** call only in browser code paths (`process.client` or `onMounted`).
- **Import the helper anywhere** — it no-ops on the server. But **call** it only from client code.

### C.3 — Fire events

**Prompt** (in the submit handler, before the API call):

```typescript
const messageId = crypto.randomUUID();
trackAgentEvent("prompt", {
  agentId: "AGENT_ID",
  conversationId,
  messageId,
  content: userInput,
  // Only if detected:
  // suggestedPrompt: fromChip,
  // fileUploaded: attachments.length > 0,
});
```

**Agent response** (streaming: inside `onFinish`/`onComplete`; non-streaming: after `await` resolves):

```typescript
trackAgentEvent("agent_response", {
  agentId: "AGENT_ID",
  conversationId,
  messageId: response.id ?? crypto.randomUUID(),
  content: fullResponseText,
  // Only if detected:
  // agentModelsUsed: [response.model ?? config.model],
  // toolsUsed: toolCalls.map(t => t.name),
});
```

**Reaction** (in thumbs/retry/regenerate handlers):

```typescript
trackAgentEvent("user_reaction", {
  agentId: "AGENT_ID",
  conversationId,
  messageId: originalMessage.id,     // the message being reacted to
  content: "positive",                // "negative", "unreact"; "copy"/"retry"/"edit" pass through
});
```

---

## Path D: Server-side Conversations API

Used for mobile apps, browser extensions, and other runtimes where Paths A–C don't fit. Fire-and-forget HTTP POST to the regional `/data/agentic` endpoint.

**The shared secret must live on a server you control — for every platform, not just web.** A mobile binary or extension bundle is client-distributed code: an embedded `PENDO_SHARED_SECRET` is extractable (unzip the APK, open `chrome://extensions`), which hands out unauthenticated event injection with arbitrary `visitor_id`. So the D.2 helper belongs on the app's backend (mobile apps almost always have one — the same API the app already talks to), called from the existing server handlers, with the client never seeing the secret. The D.6 proxy pattern applies to mobile and extensions exactly as it does to web. Only if the app genuinely has no server anywhere: **tell the user embedding the secret exposes it and enables spoofed events, and get their explicit sign-off before proceeding** — never embed it silently.

### D.1 — Configuration

The project needs two values. Find the existing config pattern (`.env`, `config.ts`, `constants.py`) and add:

1. **`PENDO_SHARED_SECRET`** — `x-pendo-integration-key` value. From **Settings → Subscription Settings → Applications → [app] → Track Event shared secret**.
2. **`PENDO_DATA_ENDPOINT`** — regional ingestion URL:

| Region | Endpoint |
|--------|----------|
| US | `https://data.pendo.io/data/agentic` |
| EU | `https://data.eu.pendo.io/data/agentic` |
| US1 | `https://us1.data.pendo.io/data/agentic` |
| JPN | `https://data.jpn.pendo.io/data/agentic` |
| AU | `https://data.au.pendo.io/data/agentic` |

Default to US and note in a comment that the user should update for other regions.

### D.2 — Helper function

**TypeScript (Node, React Native backend):**

```typescript
const PENDO_ENDPOINT = process.env.PENDO_DATA_ENDPOINT || "https://data.pendo.io/data/agentic";
const PENDO_SHARED_SECRET = process.env.PENDO_SHARED_SECRET || "";

interface TrackAgentEventOptions {
  agentId: string;
  conversationId: string;
  messageId: string;
  content: string;
  visitorId: string;
  accountId?: string;
  agentModelsUsed?: string[];
  suggestedPrompt?: boolean;
  toolsUsed?: string[];
  fileUploaded?: boolean;
  context?: { ip?: string; userAgent?: string; url?: string };
}

export async function trackAgentEvent(
  eventType: "prompt" | "agent_response" | "user_reaction",
  metadata: TrackAgentEventOptions,
): Promise<void> {
  try {
    if (!PENDO_SHARED_SECRET) return;
    const body = {
      type: eventType,
      visitor_id: metadata.visitorId,
      ...(metadata.accountId && { account_id: metadata.accountId }),
      timestamp: Date.now(),
      props: {
        agentId: metadata.agentId,
        conversationId: metadata.conversationId,
        messageId: metadata.messageId,
        content: metadata.content, // full content — no client-side truncation
        ...(metadata.agentModelsUsed && { agentModelsUsed: metadata.agentModelsUsed }),
        ...(metadata.suggestedPrompt !== undefined && { suggestedPrompt: metadata.suggestedPrompt }),
        ...(metadata.toolsUsed && { toolsUsed: metadata.toolsUsed }),
        ...(metadata.fileUploaded !== undefined && { fileUploaded: metadata.fileUploaded }),
      },
      ...(metadata.context && { context: metadata.context }),
    };
    await fetch(PENDO_ENDPOINT, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-pendo-integration-key": PENDO_SHARED_SECRET,
      },
      body: JSON.stringify(body),
    });
  } catch {
    // Analytics failure must never break the product
  }
}
```

**Python (Django, Flask, FastAPI):**

```python
import os, time
from typing import Optional
import requests

PENDO_ENDPOINT = os.getenv("PENDO_DATA_ENDPOINT", "https://data.pendo.io/data/agentic")
PENDO_SHARED_SECRET = os.getenv("PENDO_SHARED_SECRET", "")

def track_agent_event(
    event_type: str,
    *,
    agent_id: str, conversation_id: str, message_id: str,
    content: str, visitor_id: str,
    account_id: Optional[str] = None,
    agent_models_used: Optional[list[str]] = None,
    suggested_prompt: Optional[bool] = None,
    tools_used: Optional[list[str]] = None,
    file_uploaded: Optional[bool] = None,
    context: Optional[dict] = None,
) -> None:
    try:
        if not PENDO_SHARED_SECRET:
            return
        props = {
            "agentId": agent_id,
            "conversationId": conversation_id,
            "messageId": message_id,
            "content": content,  # full content — no client-side truncation
        }
        if agent_models_used is not None: props["agentModelsUsed"] = agent_models_used
        if suggested_prompt is not None: props["suggestedPrompt"] = suggested_prompt
        if tools_used is not None: props["toolsUsed"] = tools_used
        if file_uploaded is not None: props["fileUploaded"] = file_uploaded
        body = {
            "type": event_type,
            "visitor_id": visitor_id,
            "timestamp": int(time.time() * 1000),
            "props": props,
        }
        if account_id: body["account_id"] = account_id
        if context: body["context"] = context
        requests.post(
            PENDO_ENDPOINT, json=body,
            headers={
                "Content-Type": "application/json",
                "x-pendo-integration-key": PENDO_SHARED_SECRET,
            },
            timeout=5,
        )
    except Exception:
        pass
```

For **Swift, Kotlin, Dart, Go**: adapt the same pattern — fire-and-forget POST, full content (no client-side truncation), error isolation, identical JSON body.

### D.3 — Resolve `visitor_id` and `account_id`

1. If the app already uses a Pendo SDK elsewhere, find the `visitor.id` being passed and use the same identifier.
2. Otherwise look at the auth/session context (`req.user.id`, `currentUser.id`, `session.userId`). For `account_id`: `user.orgId`, `tenant.id`, etc.
3. Tell the user which identifier you mapped to `visitor_id` and ask them to confirm.

### D.4 — Resolve `context` fields

Only include `context` when values are real:
- `context.ip` — from `req.ip`, `request.remote_addr`, `X-Forwarded-For`.
- `context.userAgent` — from `req.headers["user-agent"]`.
- `context.url` — for mobile: screen/route (`myapp://chat`); for web-like: page URL.

Omit `context` entirely rather than sending empty strings.

### D.5 — Fire events

Same call sites as Path C but using the server helper, with `visitorId` and `accountId` added, and using fire-and-forget (`void trackAgentEvent(...)` or a background task queue) so tracking failures never block the user.

### D.6 — Web app without Pendo core (proxy pattern)

For a web frontend with no Pendo snippet (and no plan to add one), Path D still works — but the shared secret stays server-side:

1. **Add a small first-party endpoint** — Next.js API route (`app/api/agent-track/route.ts`), Nuxt server route (`server/api/agent-track.post.ts`), SvelteKit `+server.ts`, or a route on any existing backend. The endpoint must:
   - validate the caller's session (reject unauthenticated requests — otherwise anyone can pump events into your analytics),
   - resolve `visitor_id` / `account_id` **from the server-side session**, never from the request body (client-supplied identity is spoofable),
   - accept only the event fields the client legitimately knows (`eventType`, `conversationId`, `messageId`, `content`, optional metadata) and pass them to the D.2 helper.
2. **Fire events from the client** at the same call sites as Path C, but `fetch("/api/agent-track", { method: "POST", keepalive: true, ... })` fire-and-forget instead of `window.pendo.trackAgent()`. `keepalive: true` lets events fire during page unload.

This gives full agent analytics with no Pendo agent on the page.

---

## Verification (all paths)

After instrumentation:

1. **Grep for tracking calls:**
   - Paths A/B: `pendo_sdk` / `pendoSdk` imports, `@trace_llm` / `@trace_tool`, `set_context` / `set_identity` / `withContext`
   - Paths C/D: `trackAgentEvent` / `trackAgent`

2. **Coverage:**
   - At least one `"prompt"` call (or SDK auto-trace equivalent) per agent
   - At least one `"agent_response"` (or auto-traced GENERATION span) per agent
   - `"user_reaction"` where feedback UI exists; not required otherwise

3. **No duplicates** — each event tracked in exactly one place.

4. **`conversationId` reuse** — same variable threaded through prompt, response, and reactions within a session.

5. **Optional metadata wired dynamically:**
   - `agentModelsUsed` references a variable/config/response field (wrapped in an array), never a hardcoded model name
   - `suggestedPrompt`, `fileUploaded`, `toolsUsed` only present where the underlying capability exists, omitted otherwise

6. **Path-specific:**
   - **A/B:** `init()` is called exactly once at startup, not per-request. `visitor_id`/`account_id` set per-request via `set_context` / `set_identity` / `withContext`, not in `init()`. `PENDO_API_KEY` env var documented; `init()` guarded so a missing env var can't crash boot. Direct Anthropic/OpenAI apps have `@trace_llm` / `traceLlm` on the outermost LLM call (auto-patch alone gives traces but no conversation events); reactions use `record_reaction()` / `recordReaction()`, never hand-built spans.
   - **C:** Pendo install snippet verified present (repo grep, user-confirmed tag manager, or added during setup). Only called in client components; SSR files untouched. Selectors are stable (no CSS-in-JS hashes).
   - **D:** `PENDO_SHARED_SECRET` and `PENDO_DATA_ENDPOINT` documented; regional endpoint correct; `visitor_id` mapping confirmed with user; fire-and-forget (no `await` blocking the response). Shared secret referenced only in server-side files — never in browser bundles (D.6 proxy for web apps); proxy endpoint validates the session and resolves identity server-side.

### Summary table

Present one row per (agent, event, call site):

| Agent | Event | File | Handler | Agent ID | Path |
|-------|-------|------|---------|----------|------|
| Support Assistant | prompt | `api/chat.py` | `handle_message` | `abc123` | A (Python SDK) |
| Support Assistant | agent_response | `api/chat.py` | auto (anthropic patcher) | `abc123` | A |
| Support Assistant | user_reaction | `api/feedback.py` | `submit_feedback` | `abc123` | A |

### Final reminders

- If any agent IDs are placeholders (`"YOUR_AGENT_ID"`), tell the user to replace them with real IDs from the Pendo UI.
- **Path A:** remind user to `pip install pendo-server-sdk` and set `PENDO_API_KEY`.
- **Path B:** remind user to `npm install pendo-server-sdk` and set `PENDO_API_KEY`.
- **Path D:** remind user to set `PENDO_SHARED_SECRET` (from the Pendo UI) and `PENDO_DATA_ENDPOINT` (if not US).
