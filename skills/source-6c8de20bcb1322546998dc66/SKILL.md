---
name: ask
description: Ask natural language questions about incidents, on-call, services, and reliability data. Translates your question into Rootly API calls and returns structured answers.
argument-hint: [your question]
disable-model-invocation: true
allowed-tools:
  - mcp__rootly__*
---

# Natural Language Query

You are answering a natural language question about the user's incident, on-call, or reliability data using Rootly's MCP tools.

## Workflow

### 1. Understand the Question

Parse the user's question from `$ARGUMENTS`. Identify what data they need.

### 2. Discover Available Tools

Call `mcp__rootly__list_endpoints` to see the full list of available Rootly MCP tools and their capabilities. This helps you select the right tools for the query.

### 3. Execute Queries

Select the most appropriate tools for the question. You may need multiple calls to fully answer the question. Common patterns:

- "How many incidents last week?" -> `mcp__rootly__search_incidents` with date filters
- "Who's on call?" -> `mcp__rootly__get_oncall_handoff_summary`
- "What happened with [service]?" -> `mcp__rootly__search_incidents` filtered by service
- "Show me critical incidents" -> `mcp__rootly__search_incidents` filtered by severity
- "Any patterns in auth service failures?" -> `mcp__rootly__search_incidents` + `mcp__rootly__find_related_incidents`

### 4. Present Answer

Provide a clear, structured answer with supporting data. Include:
- Direct answer to the question
- Supporting data in tables or lists where helpful
- Source attribution (which tools/queries produced the data)

### 5. Limitations

Be explicit about what you can't answer. If the question requires data that isn't available through the Rootly MCP tools, say so clearly rather than guessing or hallucinating. For example:

- "I can't answer questions about infrastructure metrics -- Rootly tracks incidents, not system metrics."
- "This question requires data from [other system]. I can only query Rootly incident and on-call data."
