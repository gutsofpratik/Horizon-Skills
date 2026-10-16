---
name: onboarding-contractors
description: Add contractors to Wingspan, assign them to an existing engagement and send their invites. Use for "add these contractors", "onboard these people", "invite [name] to Wingspan", "create contractor records", "set up these five contractors", "invite this roster", "add them to the [engagement] engagement". Writes to the company's Wingspan account, so it always previews first.
---

# Onboarding contractors

The shared rules for every call — ids, paging, previewing a write, what the
tools cannot do — are in the `using-wingspan-tools` skill. Apply them here.

A **contractor** is a person or business the company pays; Wingspan also calls
this a *payee*. An **engagement** is a named working arrangement a contractor is
assigned to. An **invite** is the email that lets the contractor claim their own
Wingspan account.

`create_contractors` does three things in one call: it creates each contractor
record, assigns each one to an existing engagement, and emails the invite to
everyone who has not come on board yet. **It writes to the company's account.**

## Always preview first

1. Call `create_contractors` with the rows and no `mode`. It defaults to
   `mode: "preview"`, which writes nothing: it looks up the engagement, checks
   every email address, and reports exactly what applying would do — including
   which rows already exist.
2. Show that preview to the user in full: how many would be created, how many
   would be skipped, which rows have problems, which engagement each one would
   be assigned to, and how many invite emails would be sent and to how many
   people.
3. Wait for the user to say yes. Do not treat an earlier "add these people" as
   consent to write; the preview is the thing being consented to.
4. Call again with `mode: "apply"`, a `requestId` you have not used before,
   and the **same rows and the same `ref` values** you previewed.

## Arguments

| Argument | What it does |
| --- | --- |
| `contractors` | The rows. At least one, at most 50 per call. |
| `engagement` | An existing engagement, by name or id, to assign every row to. A row's own `engagements` overrides it. |
| `sendInvites` | Email the invite to everyone not yet on board. Defaults to true. |
| `mode` | `preview` (the default, writes nothing) or `apply`. |
| `requestId` | Required with `apply`. An id of your own, up to 64 printable characters with no spaces. |
| `accountId` | Write into one child account of an organization instead of the signed-in account. Only when the user names one; `who_am_i` lists them. |

Each row in `contractors`:

| Field | What it does |
| --- | --- |
| `email` | **Required.** The invite goes here, and it identifies the contractor. |
| `ref` | Your label for this row, echoed in the result. Up to 48 printable characters, no spaces and no colon. Defaults to `row-1`, `row-2` and so on. |
| `name` | Full name. Split into first and last name at the first space, exactly as the Wingspan app does. |
| `company` | Business name, if they invoice as a company. |
| `externalId` | Your own id for this contractor, for reconciliation. |
| `phone` | Contact phone number. |
| `engagements` | Engagements for this row specifically, by name or id. Overrides the top-level `engagement`. |

There are no other fields. Do not invent one — custom fields and group
membership are app work.

## What `requestId` and `ref` are for

Every write carries a key built from your `requestId` and the row's `ref`. If an
apply half-succeeds and you call again with the *same* `requestId` and the same
refs, you get back the result of the original writes; nothing new is created.
That is the only safe way to retry. Change the `requestId` only when
starting a genuinely new attempt, and never renumber refs between the preview
and the apply — refs, not row order, are what the keys are built from.

Results come back by `ref`. Email addresses and names are deliberately absent
from the result, including from error messages, so keep your own mapping from
ref to person if the user needs one.

## What each row can come back as

- **created** — the contractor record was created, and the invite was sent
  unless `sendInvites` was false.
- **skipped** — the contractor already existed. Nothing was duplicated. If
  they existed but had never come on board, the invite still went out to them:
  that is what makes a retry of a half-finished batch safe.
- **failed** — that row alone failed, with a reason and often the field at
  fault. One bad row never stops the others.

A row can also report engagement problems separately from the contractor
itself: the record was created but an assignment did not stick.

## The invite, and what happens next

The invite creates a pending claim record and emails a one-time link to the
address on the row. Wingspan decides which person that address belongs to; a
caller never supplies one.

From there:

- **Pending** — waiting for the recipient.
- **Linked** — they accepted, and the contractor record is now bound to the
  Wingspan account they chose. This is permanent.
- **Rejected** — they declined. Inviting them again creates a fresh, separate
  claim, and that is done in the Wingspan app.

`search_contractors` reports this as `onboarding`, with `Pending`, `Active` and
`Inactive`. The `finding-contractors` skill covers reading it.

## Engagements

Assign contractors to an **existing** engagement. This tool never creates one:
if the user names an engagement the company does not have, the preview says so,
and creating it is app work.

A contractor created with no engagement is a real record, but it cannot be paid
until an engagement is assigned. Say that when a user asks for bare records.

## Batches

Fifty rows is the hard limit for one call; over that, the tool refuses and
names the limit rather than quietly dropping rows. Batches of roughly 25 are
easier for a person to read in a preview. Each batch is its own attempt and
needs its own `requestId`.

This is a synchronous call, not a bulk importer. A roster of several hundred
people belongs in the Wingspan app's import screen.

## Finish these in the Wingspan app

- Creating or editing engagements, worksites, groups, custom fields and rate
  cards.
- Setting a contractor's custom-field values, adding them to a group, or
  setting their rate.
- Re-sending, retargeting or cancelling an invite, and inviting again after a
  rejection.
- Attaching requirements, and approving or rejecting what a contractor
  submits.
- Everything the contractor does themselves: accepting the invite, signing up,
  signing documents, uploading certificates, verifying identity, adding a payout
  method.
- Sharing tax information, which is usually the contractor's step; a company
  that records and verifies a contractor's taxpayer details itself also does
  that in the app.
