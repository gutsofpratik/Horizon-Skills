---
name: ui-theme-designer-help
description: "Provides customer-facing UI theme designer help from help.sap.com (BTP / Cloud Foundry edition). Use whenever you need to check what is — or is not — documented for customers about UI theme designer: setup, user/role management, themes and theme sets (creating, editing, publishing, transporting, fallback), quick/detailed/expert theming, writing themeable CSS for custom UI5 controls, best practices for custom control theme files, theming integrations with Build Work Zone / S/4HANA / SAPUI5 / SAP GUI, UI theme designer service constraints (rate limits, size limits, theming-specific security and permissions, accessibility), theming error messages and troubleshooting, what's-new. Also use for 'is X documented?' or 'what does the help say about Y?' questions. SKIP: questions about which themes or parameters exist or what values they have (use ui-theme-designer-design-tokens). SKIP: tenant-specific operational questions about a running system (\"which themes do we have?\", \"which users are assigned?\")."
allowed-tools: Bash(curl *) Bash(jq *)
---

# UI theme designer help

## Context

The UI theme designer documentation is served by `https://help.sap.com` via a JSON HTTP API:

- **Deliverable metadata** — resolves human-readable identifiers to internal IDs and provides the flat readable-URL-to-loio mapping:
  `GET https://help.sap.com/http.svc/deliverableMetadata?product_url=btp&deliverable_url=ui-theme-designer&version=LATEST`
  Returns `data.deliverable.id` (`deliverable_id`), `data.deliverable.buildNo`, and `data.filePath` (landing page file path).

- **Page content** — fetches the HTML body of a single topic, and optionally the full hierarchical TOC:
  `GET https://help.sap.com/http.svc/pagecontent?deliverable_id={id}&buildNo={buildNo}&file_path={loio}.html`
  Returns `data.body` (HTML). With the extra param `deliverableInfo=1` also returns `data.deliverable.fullToc` — a recursive tree of `{t: title, u: filename, c: children[]}` nodes covering all 80+ topics.

## Procedure

Use `curl -s` to call all API endpoints, and `jq` to parse the JSON responses.

1. Fetch deliverable metadata to obtain `deliverable_id` and `buildNo`:
   ```sh
   curl -s "https://help.sap.com/http.svc/deliverableMetadata?product_url=btp&deliverable_url=ui-theme-designer&version=LATEST" | jq '{id: .data.deliverable.id, buildNo: .data.deliverable.buildNo, filePath: .data.filePath}'
   ```
2. Fetch the landing page with `deliverableInfo=1` to get the full TOC tree:
   ```sh
   curl -s "https://help.sap.com/http.svc/pagecontent?deliverableInfo=1&deliverable_id={id}&buildNo={buildNo}&file_path={filePath}" | jq '.data.deliverable.fullToc'
   ```
3. From the TOC, identify the topic(s) whose title best matches the user's question. If uncertain, pick 2–3 candidates.
4. For each candidate, fetch its page content and strip HTML tags:
   ```sh
   curl -s "https://help.sap.com/http.svc/pagecontent?deliverable_id={id}&buildNo={buildNo}&file_path={loio}.html" | jq -r '.data.body' | sed 's/<[^>]*>//g' | tr -s '\n'
   ```
5. Answer based on the retrieved content.
