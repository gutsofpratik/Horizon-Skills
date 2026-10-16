---
name: using-wingspan-tools
description: >-
  The shared rules every Wingspan tool call follows: ids, paging, previewing a write, and what the tools cannot do. Load this before any Wingspan tool call, and whenever someone asks about the people they pay through Wingspan, what they owe, onboarding paperwork, invites, invoices or payments — for example "who do we pay", "what do we owe this month", "is this contractor ready to be paid", "add these contractors", "log a payment", "why has this not been paid".
---

# Using the Wingspan tools

Wingspan is a payments platform. A company that pays people uses it to bring
those people on board, collect their tax and compliance paperwork, and pay
them. This plugin gives Claude read access to that company's own records, plus
two carefully limited write actions.

## Words used throughout

- **Payer** — the company doing the paying. Everything here is written from
  the payer's side.
- **Contractor** (called a *payee* inside Wingspan) — a person or business the
  payer pays.
- **Engagement** — a named working arrangement a contractor is assigned to,
  such as "Q3 copywriting" or "Design retainer". Payments are filed under an
  engagement, and requirements can be attached to one.
- **Requirement** — something a contractor must satisfy before the payer can
  pay them: a tax form, a signature, an insurance certificate, a background
  check. A requirement the payer configured is a *definition*; one contractor's
  copy of it is an *instance*.
- **Payable** — one payment owed to one contractor. In the Wingspan app this is
  a row on the Payables screen.

These tools answer only for the company doing the paying. If you want to know
what someone owes you, they cannot answer it.

Longer definitions: `${CLAUDE_PLUGIN_ROOT}/skills/using-wingspan-tools/glossary.md`

## The ten tools

| Tool | What it answers | Reads or writes |
| --- | --- | --- |
| `who_am_i` | Does the connection work, and which account is it reading? | Reads |
| `search_contractors` | Who do we pay? Who matches this name? Who is held up? | Reads |
| `get_contractor` | Can we pay this one contractor, and if not, why? | Reads |
| `search_requirements` | What must a contractor satisfy before we can pay them? | Reads |
| `search_payables` | What do we owe, and what have we paid? | Reads |
| `get_payable` | What happened to this one payment? | Reads |
| `get_payroll_preview` | What would the next payroll run pay, as things stand today? | Reads |
| `create_contractors` | Create contractors, assign an engagement, send invites. | **Writes** |
| `create_payables` | Log payments as drafts. | **Writes** |
| `open_payables` | Release drafts so contractors can see them. | **Writes** |

In a tool list these appear as `mcp__plugin_wingspan_wingspan__who_am_i` and so
on. Reason about the short names above.

## Rules for every call

**Use the id the search gave you.** Each row from `search_contractors` carries
a `contractorId`, and each row from `search_payables` carries a `payableId`.
Those are the ids `get_contractor` and `get_payable` accept. Ids copied from
anywhere else — a spreadsheet, a URL, another system — will usually be
rejected.

**One page per call.** `search_contractors` and `search_payables` return a
single page, then hand back `pagination.nextPageArgs`: the complete set of
arguments for the next call. Show the page to the user and offer to fetch the
next one. Do not loop through pages unasked. A page token only works with the
exact same filters and sort that produced it, so pass `nextPageArgs` back
unchanged.

**Read the `note`.** Every list result carries a plain-sentence `note` saying
how many rows came back, how the list was sorted, and what to do next. It also
warns about things that are easy to misread, such as a filter that cannot
return what the user expects. Pass that on rather than dropping it.

**Preview, show, confirm, then apply.** All three write tools default to
`mode: "preview"`, which changes nothing: it looks up every id, checks every
row, and reports exactly what applying would do. Always preview first, show
that preview to the user in full, and wait for them to say yes. Only then call
again with `mode: "apply"` and a `requestId` you have not used before. Never
apply on your own initiative, and never apply without having previewed the same
rows.

**Reuse `ref`, and pick a fresh `requestId` per attempt.** Each row in a
`create_contractors` or `create_payables` call has a `ref`, your own label for
that row. Results come back by `ref`, and the safety mechanism that stops a
retry from creating duplicates is built from `ref` plus `requestId` — so send
the *same* refs on apply that you sent on preview. Retrying an apply with the
same `requestId` and the same refs returns the result of the original writes;
nothing new is created. A genuinely new attempt gets a new `requestId`.

`open_payables` works the same way but has no `ref`: its rows are payments that
already exist, so it reports each one by `payableId`, and that id is what its
retry key is built from. Listing the same `payableId` twice in one call is
refused.

**Amounts are in dollars.** `1200.50` means one thousand two hundred dollars
and fifty cents. Never send cents.

**Payments are created as drafts.** `create_payables` stops at a draft the
contractor cannot see, with no payment scheduled. `open_payables` releases it,
which is what shows it to the contractor. Approving it and paying it happen in
the Wingspan app.

**Some things are deliberately out of reach.** Any action Wingspan protects with
an extra identity challenge — paying a payable, paying an invoice, moving money
between accounts, creating or rotating an API key — cannot be done from here at
all, because there is nowhere in this conversation to complete that challenge.
Say so plainly and point the user at the Wingspan app rather than looking for a
workaround.

**Child accounts.** Nine of the ten tools take an optional `accountId`,
which acts as one child account of an organization instead of the signed-in
account. `who_am_i` takes no arguments at all. Only use `accountId` when the
user names a specific child account; `who_am_i` lists the ones reachable.

## Do not confuse these

- **An invoice is not a payable.** A payable is the payer's record of what it
  owes one contractor. An invoice is a bill, and either side can raise one: a
  contractor billing the company, or the company billing its own client.
  Payables can originate from either kind of invoice as well as from payroll,
  and all of them show up in `search_payables` — the individual payments from a
  payroll run appear there, the payroll batch total itself does not. A payable
  that came from an invoice is owned by Wingspan and cannot be edited here.
- **A requirement definition is not one contractor's progress.**
  `search_requirements` lists the payer's templates. One contractor's progress
  against them comes from `get_contractor`.
- **A relationship id is not an account id.** A `contractorId` identifies the
  payer's record of that contractor, not the Wingspan account the contractor
  signed in to. Only `accountId` takes an account id.

## Finish these in the Wingspan app

The tools cannot do any of the following, and no combination of them adds up to
it. Tell the user which screen to go to instead.

- Creating or editing engagements, worksites, groups, custom fields, rate cards
  or requirement definitions.
- Attaching a requirement to an engagement or a group, and approving,
  rejecting, resetting or renewing one contractor's requirement.
- Approving, scheduling, cancelling or paying a payable; funding sources;
  starting a payroll run; invoices; payment splits; accounting integrations.
  Releasing a draft is the one step here that is not app work — that is
  `open_payables`.
- Re-sending, retargeting or cancelling an invite.
- Everything the contractor does themselves: signing up, signing a document,
  uploading a certificate, verifying their identity, adding a payout method.
- Sharing tax information, which is usually the contractor's step; a company
  that records and verifies a contractor's taxpayer details itself also does
  that in the app.

## Where to go next

- Finding and filtering contractors, and who is held up:
  the `finding-contractors` skill.
- What is owed, and what happened to one payment: the `checking-payments` skill.
- Adding contractors: the `onboarding-contractors` skill.
- Creating draft payables: the `creating-draft-payables` skill.
- Connection problems and wrong-account answers: the
  `troubleshooting-connection` skill.
