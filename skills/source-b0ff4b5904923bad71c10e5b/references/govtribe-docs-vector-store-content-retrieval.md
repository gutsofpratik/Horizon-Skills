<!-- GovTribe Skills generated documentation reference. Do not edit; regenerate from the canonical public GovTribe Docs page. -->

# Vector-store content retrieval

- Canonical GovTribe Docs page: [https://govtribe.com/docs/govtribe-for-agents/guides/vector-store-content-retrieval](https://govtribe.com/docs/govtribe-for-agents/guides/vector-store-content-retrieval)

## External MCP examples

External MCP clients can use this sequence when full file text is needed:

1. Resolve the target record. Use `Search_GovTribe` or the relevant typed search tool to identify the opportunity or file-bearing record.
2. Find the attached files with `Search_Government_Files` or `Search_User_Files`, and choose the smallest set that answers the question.
3. Call `Add_To_Vector_Store` with the chosen items. Omit `govtribe_vector_store_id` for a new standalone store, or pass an existing ID to add to that store.
4. While Add reports `in_progress`, call it again later with the same items and its returned `govtribe_vector_store_id`. Review skipped and failed files before treating a package as complete.
5. When the requested files are ready, call `Search_Vector_Store` with the returned store ID and focused source questions. Treat chunks as evidence, and disclose any missing attachment or incomplete coverage.

Find candidate government files before staging a package:

Tool: `Search_Government_Files`

```json
{
  "query": "PWS SOW Section L Section M proposal instructions evaluation factors",
  "federal_contract_opportunity_ids": ["<FEDERAL_CONTRACT_OPPORTUNITY_ID>"],
  "fields_to_return": [
    "govtribe_id",
    "govtribe_url",
    "name",
    "govtribe_ai_summary",
    "posted_date",
    "download_url"
  ],
  "per_page": 10
}
```

Stage an entire opportunity package when the user asks for a full solicitation package review:

Tool: `Add_To_Vector_Store`

```json
{
  "items": [
    {
      "govtribe_type": "federal_contract_opportunity",
      "govtribe_id": "<FEDERAL_CONTRACT_OPPORTUNITY_ID>"
    }
  ]
}
```

Retrieve source evidence for submission and evaluation rules:

Tool: `Search_Vector_Store`

```json
{
  "query": "Extract proposal volume requirements, page limits, required forms, submission method, and evaluation factors.",
  "govtribe_vector_store_id": "<VECTOR_STORE_ID>",
  "max_num_results": 10,
  "rewrite_query": false
}
```

Stage one file when the question is limited to a specific attachment:

Tool: `Add_To_Vector_Store`

```json
{
  "items": [
    {
      "govtribe_type": "government_file",
      "govtribe_id": "<GOVERNMENT_FILE_ID>"
    }
  ]
}
```

Retrieve clause-level evidence from that file:

Tool: `Search_Vector_Store`

```json
{
  "query": "What cybersecurity reporting, incident response, and access control requirements appear in this attachment?",
  "govtribe_vector_store_id": "<VECTOR_STORE_ID>",
  "max_num_results": 6,
  "rewrite_query": true
}
```

## When not to use it

Do not stage files just because vector retrieval is available. Prefer the normal MCP search path when:

- the question is about record metadata, not file text
- `content_snippet` already answers the question
- the user needs a list of files, not semantic chunks from file contents
- the selected `govtribe_type` is not supported by `Add_To_Vector_Store`

## Related articles

- [Add to vector store MCP tool](https://govtribe.com/docs/govtribe-for-agents/tools/add-to-vector-store-mcp-tool): Review supported item types and staging arguments.
- [Search vector store MCP tool](https://govtribe.com/docs/govtribe-for-agents/tools/search-vector-store-mcp-tool): Review semantic retrieval arguments.
- [Search vector store MCP response](https://govtribe.com/docs/govtribe-for-agents/mcp-tool-responses/search-vector-store-mcp-tool-response): Interpret returned structured results, snippets, and readiness messages.
- [Search government files](https://govtribe.com/docs/govtribe-for-agents/tools/search-government-files-mcp-tool): Search government-file metadata and snippets before staging full text.
- [Search user files](https://govtribe.com/docs/govtribe-for-agents/tools/search-user-files-mcp-tool): Search team-uploaded file metadata and snippets before staging full text.
- [Proposal Workflows with MCP](https://govtribe.com/docs/govtribe-user-guide/govtribe-mcp/govcon-workflows-with-mcp/proposal-workflows): Use the generated Solicitation Package Review prompt as a copy-ready workflow in connected MCP clients.

---

For current tool schemas, parameters, response fields, or freshness-sensitive behavior, call the live `Documentation` MCP tool instead of inferring details from this bundled reference.
