# Wingspan glossary

Every term the Wingspan tools use, in the order a payer meets them.

## People and companies

**Payer** — the company that pays. In Wingspan the payer holds a record for
each counterparty it pays, and every tool in this plugin reads or writes from
the payer's side. These tools answer only for the company doing the paying. If
you want to know what someone owes you, they cannot answer it.

**Payee** — the payer's record of a counterparty it pays. The tools call this a
**contractor**, because that is the word the Wingspan app uses on screen. Payee
and contractor mean the same thing.

**Person** — the human being who receives an invite email and is allowed to
claim a contractor record. A payer never chooses which person that is;
Wingspan resolves the person from the email address, because the invite link
has to belong to exactly one human.

**Account** — the business, tax and payment identity a person selects or
creates when they accept an invite. A contractor record starts with no account
attached, and is bound to one only when the invited person accepts.

## The invite

**Invite** — the durable record Wingspan keeps of one invitation. It begins as
`Pending` and ends as either `Linked` or `Rejected`.

- No such record at all means nobody has been invited yet.
- `Pending` means an invite exists and is waiting for the recipient.
- `Linked` is permanent: the contractor record is bound to an account.
- `Rejected` is final for that invite. Inviting again creates a fresh, separate
  invite, and that is done in the Wingspan app.

`search_contractors` reports the relationship as `onboarding`: `Active` (they
accepted an invite and are not archived), `Inactive` (archived, or the invite
was rejected), `Pending` (everything else — an invite is out and unanswered, or
nobody has been invited at all). Filtering on `onboarding: "Pending"` is
narrower than the value a row reports: the filter matches only contractors with
an outstanding invite, so a contractor created without one is reported as
`Pending` but not returned by that filter.

## Work and pay

**Engagement** — a named working arrangement the payer defines once, such as
"Q3 copywriting" or "Design retainer". Requirements can be attached
to an engagement, and payments are filed under one. Engagements are created in
the Wingspan app.

**Assignment** (called a *payee engagement* inside Wingspan) — the pairing of
one contractor with one engagement. It carries that contractor's rate for that
engagement and their own copies of the engagement's requirements. A contractor
can hold several assignments.

**Payable** — one payment owed to one contractor. It is the row on the
Payables screen in the Wingspan app.

**Line item** — one priced line inside a payable: either a flat amount, or a
quantity multiplied by a cost per unit. Amounts are in dollars.

**Payroll run** — a batch that funds and pays a set of approved payables.
`get_payroll_preview` reads the next one before it goes out, as today's records
would settle it; it does not model anything that changes between now and the run
itself. Runs that have already happened, and the funding source behind any of
them, are not read here.

## Compliance

**Requirement definition** — a template the payer configures once: "W-9",
"Certificate of insurance", "Background check". It carries the `blocking` value
Wingspan holds for it, its grace period, and how often it expires. `search_requirements` lists these.

**Requirement instance** — one contractor's own copy of a definition, created
when they are placed on an engagement or added to a group. It carries their
progress. `get_contractor` returns these.

**Blocking** — what Wingspan reports for one requirement definition. An
outstanding requirement that is not marked blocking is tracked but does not
hold up a payment. A contractor's own copy can be blocking or not depending on
where it was attached. `get_contractor` treats every incomplete requirement as
blocking and does not read that setting; which placement merely tracks a
requirement is visible only in the Wingspan app. A group placement is blocking or not. An engagement placement has a
third setting that blocks eligibility while still allowing payment.

**Grace period** — the days from when a requirement is attached to a
contractor before an outstanding copy starts holding up a payment. Inside that
window an unfinished requirement does not block. `search_requirements` reports
it as `gracePeriodDays`.

**Group** — a named set of contractors that carries its own requirements, for
rules that apply regardless of engagement, such as a state licence. Groups are
managed in the Wingspan app.

**Eligibility** — whether an assignment's requirements are satisfied well
enough for a payment to be opened and paid. It is checked when a payable is
opened, not when it is created.
