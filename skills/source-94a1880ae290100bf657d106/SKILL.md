---
name: creating-draft-payables
description: Create draft payables — new payment obligations to contractors — in Wingspan. Nothing is paid. Use for "log a payment", "pay [name] $500 for [work]", "record these payments", "add these payments to the [engagement] engagement", "create payables", "log 12 hours at $85 for [name]", "bill this month's work". Writes to the company's Wingspan account, so it always previews first.
---

# Creating draft payables

The shared rules for every call — ids, paging, previewing a write, what the
tools cannot do — are in the `using-wingspan-tools` skill. Apply them here.

A **payable** is one payment owed to one contractor — the row on the Payables
screen in the Wingspan app. An **engagement** is the named working arrangement
a payment is filed under. A **line item** is one priced line inside a payment.

`create_payables` records payments against contractors' engagements. **It
writes to the company's account, and everything it creates is a draft.**

## Always preview first

1. Call `create_payables` with the rows and no `mode`. It defaults to
   `mode: "preview"`, which writes nothing: it resolves each contractor and
   engagement, checks every amount and date, totals it up, and reports exactly
   what applying would do.
2. Show that preview to the user in full — the per-row amounts, the total, the
   engagement each payment lands on, every warning, and every row that cannot
   be created.
3. Wait for the user to say yes. An earlier "log these payments" is not consent
   to write; the preview is the thing being consented to.
4. Call again with `mode: "apply"`, a `requestId` you have not used before,
   and the **same rows and the same `ref` values** you previewed.

Retrying an apply with the same `requestId` and the same refs returns the
result of the original writes; nothing new is created. That is the only safe way
to retry. A genuinely new attempt gets a new `requestId`.

## Arguments

| Argument | What it does |
| --- | --- |
| `payments` | The rows. At least one, at most 50 per call. |
| `engagement` | An engagement, by name or id, for every row. Omit it and Wingspan uses each contractor's default engagement. A row's own `engagement` overrides it. |
| `dueDate` | Default due date for every row, as `YYYY-MM-DD`. Required unless every row sets its own. |
| `currency` | Currency for every row. Defaults to US dollars. |
| `mode` | `preview` (the default, writes nothing) or `apply`. |
| `requestId` | Required with `apply`. An id of your own, up to 64 printable characters with no spaces. |
| `accountId` | Write into one child account of an organization instead of the signed-in account. Only when the user names one; `who_am_i` lists them. |

Each row in `payments`:

| Field | What it does |
| --- | --- |
| `contractor` | **Required.** Their email, your external id for them, or their contractor id. |
| `ref` | Your label for this row, echoed in the result. Up to 48 printable characters, no spaces and no colon. Defaults to `row-1`, `row-2` and so on. |
| `referenceId` | Your own id for this payable, stored on it and searchable afterwards with `search_payables`' `referenceId` filter. One per payable — two cannot share one. |
| `engagement` | The engagement for this row, by name or id. Overrides the top-level one. |
| `amount` | A flat amount in dollars, for example `1200.50`. |
| `quantity` | Units worked, for example hours. Goes with `unitCost`. |
| `unitCost` | Amount per unit, in dollars. Goes with `quantity`. |
| `unit` | What a unit is: `"Hour"`, `"Unit"`, or a label of your own. Defaults to `"Unit"`. |
| `description` | What the work was. Shown as the line item's title. |
| `detail` | Longer detail underneath the line item. |
| `dueDate` | Due date for this row, as `YYYY-MM-DD`. Overrides the top-level one. |
| `notes` | A note on the payment itself. The contractor can see it. |
| `lineItems` | Several priced lines instead of the single-line fields above. |

Each entry in `lineItems` takes `description`, `amount`, `quantity`,
`unitCost`, `unit` and `detail`, with the same meanings.

**`ref` and `referenceId` are different things.** `ref` is a label for this
call: it comes back in the result, it is what the retry key is built from, and
it is gone once the call is done. `referenceId` is stored on the payable itself
and is how the user finds that payment again later. A row can carry both, and
they do not have to match. Because no two payables can share a `referenceId`,
reusing one is refused rather than attached to a second payment — which also
means a genuine retry of an apply is safe, but re-sending the same
`referenceId` under a *new* `requestId` is not.

## Amounts

**Amounts are in dollars.** `1200.50` is one thousand two hundred dollars and
fifty cents. Never send cents.

**Price a line one way or the other, never both.** Either a flat `amount`, or
`quantity` together with `unitCost` — twelve hours at eighty-five dollars is
`quantity: 12, unitCost: 85, unit: "Hour"`. Sending both is refused rather than
guessed at, because it means the amount was expressed twice. A rate-priced line
needs both halves: `quantity` on its own, or `unitCost` on its own, is refused.

**Use the single-line fields or `lineItems`, never both on one row.** Same
reason.

**Every amount has to be greater than zero.** A flat `amount` of zero, a
`unitCost` of zero and a `quantity` of zero are each refused. A payment for
nothing is never what the user meant.

**A flat `amount` cannot be more precise than the currency.** US dollars are
paid to two decimal places, so `10.999` is refused. Round the figure with the
user rather than picking one for them. A per-unit `unitCost` may be finer than
that — half a cent across a thousand units is a real way to price work — and
Wingspan does the multiplication.

**A due date is required**, either on every row or once at the top level, and
it is a calendar date: `YYYY-MM-DD`, no time and no timezone.

## Engagements

The engagement decides which working arrangement the payment belongs to, and
**it is fixed the moment the payment is created.** There is no way to move a
payment to a different engagement afterwards — not from here, and not in the
app. Getting it wrong means cancelling the payment and creating a new one. So
when the engagement matters, confirm it with the user before applying.

The contractor must already be assigned to the engagement you name. If they are
not, the row fails and the preview lists which engagements they *are* assigned
to. Assigning them is app work; the `onboarding-contractors` skill covers doing
it for a new contractor.

Omit the engagement entirely and Wingspan files the payment under the
contractor's default engagement. The preview says when that is happening, so
show it — a user who cares which engagement a payment lands on needs to see
that they did not name one.

**This tool creates new payment obligations. It never moves existing ones.**
A payable's engagement is fixed when it is created, and no tool here edits a
payable. So "add these payments to an engagement" is ambiguous: if the user
means payments that already exist in Wingspan, that cannot be done from here,
and previewing a creation would propose duplicate obligations. Before calling
the tool, settle which one the user means. If they mean existing records,
check with `search_payables` and say the engagement cannot be changed. If they
mean new drafts, proceed. When the phrasing is "log", "record" or "add" a
payment that has already been paid outside Wingspan, ask as well: a draft
payable is a new obligation that Wingspan will expect to pay, not a record of
money already sent.

## Everything created here is a draft

A payment created by this tool sits at draft. The contractor cannot see it and
no payment is scheduled. Say this to the user every time, because "log a
payment" often means "and pay it" in their head.

What happens next: `open_payables` releases the draft, which is what shows it to
the contractor, and that is the one step available here. Approving it, and the
payroll run that funds and pays it, happen in the Wingspan app. Paying is also
protected by an extra identity challenge, so it cannot be reached from here
under any circumstances.

## The warning that matters most

**Eligibility is checked when a payment is opened, not when it is created.** A
draft against a contractor with outstanding requirements is created happily
and may then fail to open, if any of those requirements blocks eligibility.
Whether a given outstanding requirement blocks depends on where it was
attached, which these tools do not read, so say "may not open" rather than
"cannot open". The preview flags the situation — "onboarding requirements are
incomplete, so this payable cannot be opened or paid until they are" — and
that warning must reach the user, not be dropped as noise. Use
`get_contractor` to say what is outstanding; the `finding-contractors` skill
covers reading it.

The preview also warns when a contractor's assignment to the named engagement
is not active yet.

## Batches

Fifty rows is the hard limit for one call; over that, the tool refuses and
names the limit. Each batch is its own attempt and needs its own `requestId`.
One bad row never stops the others — each row reports its own outcome by `ref`.

## Where payments come from besides this tool

An invoice is not a payable. A payable is the payer's record of what it owes one
contractor. An invoice is a bill, and either side can raise one: a contractor
billing the company, or the company billing its own client. Payables can
originate from either kind of invoice as well as from payroll, and all of them
show up in `search_payables` alongside anything created here — the
`checking-payments` skill covers reading them. A payable that came from an
invoice is owned by Wingspan and cannot be edited here.

## Finish these in the Wingspan app

- Approving a draft, scheduling it, cancelling it and paying it. Releasing it
  so the contractor can see it is `open_payables`, not app work.
- Starting a payroll run, and funding sources.
- Moving a payment to a different engagement — impossible; cancel and recreate.
- Invoices, payment splits, deductions and accounting integrations.
- Creating engagements, and assigning a contractor to one.
