---
name: organize-matter
description: Group documents into a GC AI project (matter) so later review and questions are scoped to it. Use when the user is starting a new matter, deal, or case, or wants a set of files kept and worked on together.
---

# Organize a matter in GC AI

Set up a GC AI project around a matter and attach its documents, so later playbook runs and questions can be scoped to just that matter.

## Steps

1. **Create the project.** Call `create_project` with a clear, specific name (for example the counterparty and deal, or the matter name the user gave). If a fitting project may already exist, check `get_projects` first and reuse it instead of making a duplicate.

2. **Bring the documents in.** For each file the user wants in the matter, upload it (`upload_file`, or `start_file_upload` plus `finish_file_upload` for a sandbox file) and poll `get_files({ id })` until `ready`.

3. **Attach them.** Call `attach_to_project` for each ready file. Use `detach_from_project` if the user wants something removed.

4. **Confirm the matter.** Report back what the project now contains, and offer the natural next step: run a review playbook against the matter, or ask a question scoped to it.

## Notes

- A project is the unit that later review and Q&A scope to, so name it for how the user thinks about the matter, not the file names.
- Do the uploads and attachments in one turn; poll uploads to `ready` before attaching.
