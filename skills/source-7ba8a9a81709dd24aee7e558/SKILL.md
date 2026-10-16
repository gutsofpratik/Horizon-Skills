---
name: build-sequences
description: Builds and runs email outreach sequences end to end — create a sequence, add follow-up steps and message templates, add recipients from your leads, then start, pause, resume, or check its stats. Use when the user wants to set up outreach, build an email sequence, add recipients, launch a drip, or check sequence performance.
user-invocable: true
argument-hint: Set up a 3-step outreach sequence for my fintech leads and start it
---

# Build Sequences

Create, configure, and run Hunter email sequences from chat: create the sequence, write the introduction email, add follow-up steps and message templates, add recipients, launch, and read stats. Step authoring never needs the dashboard. **Connecting a sending inbox still does** — the API only attaches an account that is already connected, so check `List-Email-Accounts` before promising a fully in-chat launch.

## Examples

- `/hunter:build-sequences Set up a 3-step outreach sequence for my fintech leads`
- `"Create a sequence called Q2 Outreach with a follow-up after 3 days"`
- `"Add the leads from my SaaS list to the Q2 Outreach sequence"`
- `"Start the Q2 Outreach sequence"`
- `"Pause my running sequence"`
- `"How is the Product Launch sequence performing?"`

## Workflow

### Step 1: Identify or create the sequence

- Existing sequence named or given by ID → call `Get-Sequence` to load its live status, sender, settings, and recipient count before acting (start/resume/archive/add-recipients should rely on this, not stale list rows). To browse, call `List-Sequences`.
- New sequence → call `Create-Sequence` with a descriptive name. Then configure it (Steps 2–3).

```
# Your Sequences

| ID | Name | Status | Recipients |
|----|------|--------|------------|
| 123 | Q2 Outreach | draft | 0 |
| 456 | Product Launch | running | 150 |
```

### Step 2: Configure steps and templates

- **Message templates** — `Create-Message-Template` (requires a `name` and `body`; `subject` optional), reusable across sequences. `List-Message-Templates` to reuse an existing one (`Get-Message-Template` to inspect); `Update-Message-Template` to edit.
- **Follow-up steps** — `Create-Sequence-Follow-Up` to append each new step (delay + template). `List-Sequence-Follow-Ups` to review the cadence (`Get-Sequence-Follow-Up` for one step). `Update-Sequence-Follow-Up` rewrites an existing step in place — subject, body, `wait_days`, or `message_format`. Two side effects to surface, both Hunter-side and neither undoable from chat: a **subject** edit also rewrites every later step still holding the old subject verbatim (and regenerates their pending messages on a started sequence) — including steps appended with no subject of their own, which is the normal build order — so always re-read the step list afterwards and report which other steps moved; and switching a step from html to **text** makes Hunter convert the stored body (images dropped, links flattened, HTML stripped) even if you send no `body`, so confirm that before doing it. `Delete-Sequence-Follow-Up` removes a step, but **only the last step** can be deleted and never step 0, so prefer an update over delete + recreate. A sequence holds at most **6 steps total** — the step-0 introduction plus up to 5 follow-ups — so longer drips aren't possible.

Use `{{first_name}}`-style merge fields in templates, but each merge field must carry a **fallback value** — both `Create-Sequence-Follow-Up` and `Update-Sequence-Follow-Up` reject bare variables, so ask for or generate fallback text for every variable. The **introduction email (step 0)** is created empty by `Create-Sequence` and cannot be targeted by `Create-Sequence-Follow-Up`: get its id from `List-Sequence-Follow-Ups`, then write its subject and body with `Update-Sequence-Follow-Up`. The whole sequence can be authored this way, and launched too when a sending inbox is already connected.

### Step 3: Add recipients

Pull recipients from a leads list (`List-Leads` with `leads_list_id` — page through **all** results with `offset`, 100 per page, so leads past the first page aren't dropped), from specific emails/lead IDs, or from a prior search, then call `Add-Sequence-Recipients` with the sequence ID and the emails or lead IDs. Max 50 per call — batch larger lists automatically and report progress ("Adding batch 1 of 3…"). Use `List-Sequence-Recipients` to see who is already in.

### Step 4: Pre-flight and start

Before calling `Start-Sequence`, verify the launch preconditions and surface any gap instead of letting the start fail:

- The **introduction email (step 0)** has a subject and body. Verify with `List-Sequence-Follow-Ups` (`Get-Sequence` only reports step counts, not their contents); if step 0 is blank, write it with `Update-Sequence-Follow-Up` rather than sending the user to the dashboard. `Start-Sequence` fails validation while step 0 is blank.
- The sequence has a **sender attached** — the sender is a per-sequence field set via `email_account_ids` on `Create-Sequence` / `Update-Sequence`, not merely "some connected account." Use `List-Email-Accounts` to pick one (`Get-Email-Account` for its details) and `Update-Sequence` to attach it if the sequence has none; `Start-Sequence` validates the sequence's own sender.

If a precondition is missing, say exactly what to fix. Once clear, call `Start-Sequence`.

### Step 5: Run controls and stats

- `Pause-Sequence` / `Resume-Sequence` to hold or continue.
- `Archive-Sequence` to retire a finished sequence.
- `Get-Sequence-Stats` for sent / open / reply / bounce numbers.
- `Update-Sequence` to rename or adjust settings — but once a sequence has **started**, only the name (and unsubscribe-link toggle) stay editable; sender, schedule, BCC, and tracking lock on start, so set those while it's still a draft.

```
# Sequence: Q2 Outreach

**Status:** running | **Recipients:** 120
**Sent:** 118 | **Opened:** 74 (63%) | **Replied:** 19 (16%) | **Bounced:** 2

View: https://hunter.io/sequences/{sequence_id}
```

## Guardrails

Confirm before any destructive, irreversible, or email-sending action — state the operation, the affected count, and the target, then wait for an explicit "yes":

- `Delete-Sequence` — only **draft** sequences can be deleted; a started or archived sequence returns an error (archive/stop it instead). For a draft: "This permanently deletes the '[name]' sequence. Confirm?"
- `Archive-Sequence` — stops a running sequence and can't be undone through the API: "This archives '[name]' and can't be reversed. Confirm?"
- `Remove-Sequence-Recipients` — echo how many recipients and from which sequence; max 50 per call, so batch larger removals in groups of 50 and report progress.
- `Delete-Message-Template`, `Delete-Sequence-Follow-Up` — name what is being removed.
- `Update-Message-Template` — overwrites a saved template's fields with no way to recover the old version; confirm before editing a reusable team template.
- `Update-Sequence-Follow-Up` — overwrites a step's subject and body with no way to recover the previous copy; show the current wording and the replacement before writing. A **subject** change also propagates to later steps that still share the old subject, so name those steps in the confirmation, not just the one being edited. Filling in a blank step 0 overwrites nothing, so it needs no confirmation — but it still **propagates**: steps you appended without a subject of their own were stored empty, and authoring step 0 fills them all in. Re-read `List-Sequence-Follow-Ups` afterwards and report every step that changed.

**Anything that can send email — confirm first.** `Start-Sequence`, `Resume-Sequence`, and `Add-Sequence-Recipients` on an already-started sequence all schedule real outbound email (Resume and Add-Recipients need no separate start call). Always confirm the recipient count and sending account before any of them.

## Credit Cost

Free — creating, configuring, and running sequences does not consume search or verification credits. (Finding and verifying the recipient emails beforehand does.)

## Important Notes

- A sequence cannot start until the step-0 introduction email (subject + body, written with `Update-Sequence-Follow-Up`) and a connected sending account are both in place. Check before calling `Start-Sequence`.
- Max 50 recipients per `Add-Sequence-Recipients` call — batch larger lists.
- Message templates are reusable across sequences — prefer reusing over recreating.
- `List-Email-Account-Sequences` shows which sequences a given sending account is running.
