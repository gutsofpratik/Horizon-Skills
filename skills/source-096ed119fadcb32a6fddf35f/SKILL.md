---
name: review-document
description: Review one or more documents against a GC AI playbook and summarize the findings. Use when the user wants a contract or document checked, redlined, or run through a review playbook in their GC AI knowledge base.
---

# Review a document with a GC AI playbook

Run the user's documents through a GC AI review playbook and report the results. Do the whole chain in one turn, polling long-running jobs yourself.

## Steps

1. **Get the target files into GC AI.**
   - If the user attached documents to this conversation, call `upload_file` and let the host fill the `file` argument. Never read or construct a file path yourself.
   - If a document only exists in your own sandbox, call `start_file_upload`, PUT the bytes to the returned `upload_url`, then call `finish_file_upload`.
   - If the user is pointing at documents already in GC AI, find them with `get_files`.
   - After any upload, poll `get_files({ id })` until `status` is `ready`. Do not run a playbook against a file that is still `extracting` or `embedding`.

2. **Pick the playbook.** Call `get_playbooks`. Match the user's request to a playbook by name. If nothing clearly matches, ask which playbook to use rather than guessing.

3. **Run it.** Call `run_playbook` with the file ids and the playbook id, then poll `run_playbook_status` until `status` is `succeeded`, `failed`, or `canceled`.

4. **Summarize for the user.** Group the check results into what passed, what failed, and what needs a human look. Quote the specific clause or finding behind each flagged item, not just the check name. Close with the concrete next step (for example, which clauses to negotiate or redline).

## Notes

- One document, several playbooks, or several documents against one playbook are all valid. Confirm the scope with the user if it is ambiguous.
- Keep working until the result is ready. Never hand the turn back to the user to wait or poll.
