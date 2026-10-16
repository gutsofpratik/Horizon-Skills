---
name: finding-contractors
description: Find, filter and inspect the contractors a company pays through Wingspan, including who still has onboarding paperwork outstanding. Use for "who do we pay", "list our contractors", "find [name]", "who has not signed up yet", "who is missing their W-9", "who is blocked by the certificate of insurance", "can we pay [name]", "what is [name]'s status", "who is on this engagement".
---

# Finding contractors

The shared rules for every call — ids, paging, previewing a write, what the
tools cannot do — are in the `using-wingspan-tools` skill. Apply them here.

A **contractor** is a person or business the company pays; Wingspan also calls
this a *payee*. An **engagement** is a named working arrangement a contractor
is assigned to. A **requirement** is something a contractor must satisfy before
they can be paid, such as a tax form or an insurance certificate.

Two tools cover this: `search_contractors` lists and filters, and
`get_contractor` reads one contractor in full. Every row a search returns
carries a `contractorId`, and that is the id `get_contractor` takes.

## Listing and searching

`search_contractors` with no arguments lists active contractors, newest first,
25 to a page.

| Argument | What it does |
| --- | --- |
| `query` | Free-text search over name, email, company and your own external id. At least two characters. Results come back by relevance. |
| `status` | Which screen tab to read: `active`, `notSignedUp`, `incomplete`, `complete`, `archived`. |
| `onboarding` | Where the working relationship stands: `Pending`, `Active`, `Inactive`. |
| `engagement` | Only contractors assigned to this engagement, by name or id. |
| `batch` | Only contractors loaded by one bulk import in the Wingspan app, by that import's batch id. |
| `requirement` | Only contractors whose copy of this requirement is in `requirementState`. |
| `requirementState` | Which state that requirement is in. Defaults to `incomplete`. |
| `sortBy` | `createdAt` or `updatedAt`. One field per call. |
| `sortDirection` | `asc` or `desc`. Defaults to `desc`. Refused without `sortBy`. |
| `limit` | Rows per page, 1 to 100. Defaults to 25. |
| `pageToken` | Continue a previous page. Pass the previous result's `pagination.nextPageArgs` back unchanged. |
| `accountId` | Read one child account of an organization instead of the signed-in account. Only when the user names one; `who_am_i` lists them. |

There are no other filters. Do not invent one.

## Two separate questions, two separate arguments

`status` is the tab strip from the Wingspan app, and it mixes the working
relationship with paperwork: `incomplete` and `complete` are a summary of
requirements, while `notSignedUp` and `archived` are about the relationship.

`onboarding` is the relationship on its own, and every row reports it whatever
you filtered on.

The two combine, so `status: "notSignedUp"` with `onboarding: "Pending"` means
"invited, has not signed up". One pair is refused rather than answered:
`onboarding: "Inactive"` together with `status: "active"`, because `active`
excludes archived contractors and `Inactive` requires them. `status` defaults
to `active`, so leaving it out is the same pair — send `onboarding: "Inactive"`
with `status: "archived"`.

One more thing worth passing on: `onboarding: "Inactive"` matches archived
contractors, but a contractor who only rejected their invite is not matched.
The underlying search cannot express "archived or rejected" in one query, and
the result's `note` says so.

**One kind of contractor no filter finds:** someone archived before any
engagement was assigned to them. Every `status` tab except `active` needs a
paperwork or engagement summary they never got, and `active` excludes anyone
archived — so no combination of `status` and `onboarding` returns them. Read one
with `get_contractor` if you have their `contractorId`; its headline reads
Archived. Every row that does come back carries its own `archived` field,
whatever you filtered on.

## Who still has a named requirement outstanding

Two calls, in this order.

1. `search_requirements` lists the requirements the company has configured.
   Each carries a `requirementDefinitionId`, the `blocking` value Wingspan
   holds for it, its grace period and how often it expires. Pick the one the
   user named. With no arguments it lists the ones still in use; it also takes
   `type` (one kind of requirement), `includeInactive` (show retired ones too),
   `limit`, `pageToken` and `accountId`, and nothing else.
2. `search_contractors` with `requirement` set to that id; its exact name also
   works, matched case-insensitively and in full, so a partial name will not
   resolve. Set `requirementState` to the state you want.

| `requirementState` | Means |
| --- | --- |
| `incomplete` | Outstanding — the contractor has not finished it. This is the default. |
| `pendingReview` | The contractor submitted something and the company has not reviewed it. |
| `complete` | Satisfied, whether the contractor or the company finished it. |
| `expiring` | Satisfied, but the expiry date is approaching. |
| `expired` | It lapsed and has to be renewed. |

A requirement the company rejected, or one whose underlying record was revoked
or failed, is reopened rather than failed — it reads as outstanding again, with
a reason recorded. There is no failed state. Say "reopened after review" rather
than "never started" when reporting one.

`requirementState` on its own is refused: it needs `requirement`.

Two things to say out loud when reporting the answer:

- **Not every outstanding requirement blocks a payment.** `blocking` on a
  definition is what Wingspan reports for that definition. A contractor's own
  copy can be blocking or not depending on where it was attached.
  `get_contractor` treats every incomplete requirement as blocking and does
  not read that setting; which placement merely tracks a requirement is visible
  only in the Wingspan app.
- **`gracePeriodDays` is a delay on the definition**, not a verdict about a
  person: it is the days from when a requirement is attached to a contractor
  before an outstanding copy starts holding up a payment. Inside that window an
  unfinished requirement does not block.

The catalogue of requirement kinds, and what has to happen for each:
`${CLAUDE_PLUGIN_ROOT}/skills/finding-contractors/requirement-types.md`

## When to read one contractor in full

Move to `get_contractor` once the question is about one person: "can we pay
them", "what is their status", "what is missing". It returns what the
Contractors detail screen shows, and the field to lead with is `alert` — the
screen's single verdict, with exactly one of these outcomes:

| `alert` says | Means |
| --- | --- |
| Contractor invited | Invited, has not signed up yet. |
| Tax information not shared | Signed up, but has not shared tax information with the company. |
| Archived | Someone at the company archived them. |
| Contractor is all set for now | Ready to be paid. |
| Payments eligibility pending | Signed up with nothing outstanding, but at least one active assignment is not cleared for payment. |
| Requirements expired | Something already satisfied has lapsed and needs renewing. |
| Requirements expiring soon | Something already satisfied is about to lapse. |
| Requirements incomplete | Something is outstanding. |

Only one applies, and the order above decides which. A contractor who is both
archived and missing tax information reads "Tax information not shared",
because that check comes first. There is no single "can I pay this person"
field anywhere in Wingspan; this verdict is the closest thing to one.

"Tax information not shared" does not always mean the contractor must act — a
payer can supply and verify the details itself, in the Wingspan app.

`alert` can also be empty, when none of the checks above fire. Report that as
"nothing flagged" and fall back to the assignments and requirement list in the
same result rather than declaring the contractor payable.

`get_contractor` also returns their tax information and its verification
status, every engagement assignment with a count of outstanding requirements,
the full requirement list with expiry dates, whether they have a payout method
set up (somewhere for the money to land), and your own id for them.

## Two results to read carefully

**A contractor with no engagement assignment has no paperwork summary at all.**
Their requirements, tax-ID and engagement status are not recorded rather than
empty, and the `notSignedUp`, `incomplete` and `complete` tabs will not return
them. The result's `note` says so when it applies. Assigning an engagement is
what gives them a status worth reading, and that is app work.

**An assignment with no requirements shows "None required".** It also shows
whatever eligibility Wingspan reports. Do not infer from it. If such a
contractor cannot be paid, the fix is to attach one requirement in the Wingspan
app and have it completed; nothing else re-evaluates eligibility.

## A search that finds nobody

If a name search returns no rows and archived contractors were excluded, the
result reports how many archived contractors do match. Offer to look there
before telling the user the person does not exist.

## Finish these in the Wingspan app

- Creating or editing engagements, groups, worksites, custom fields and rate
  cards.
- Writing a requirement definition, and attaching one to an engagement or a
  group.
- Approving, rejecting, resetting or renewing one contractor's requirement, and
  extending an expiry date.
- Archiving or restoring a contractor.
- Everything the contractor does themselves: signing up, signing, uploading a
  document, verifying identity, adding a payout method.
- Sharing tax information, which is usually the contractor's step; a company
  that records and verifies a contractor's taxpayer details itself also does
  that in the app.
