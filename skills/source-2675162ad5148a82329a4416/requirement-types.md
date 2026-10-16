# Kinds of requirement

A **requirement** is something a contractor must satisfy before the company can
pay them. The company configures a template — a *definition* — once; each
contractor then gets their own copy of it when they are placed on an engagement
or added to a group.

`search_requirements` reports each definition's kind as its `type`, alongside
the definition's own name. Read the kinds your company actually uses out of
that result rather than assuming: `search_requirements` also accepts an
optional `type` filter; copy the exact `type` from a result rather than typing
a label.

## What each kind asks for

The labels below are prose. The `type` filter takes the exact value a
definition's `type` field carries — one word with no spaces. Copy it from a
`search_requirements` result; never type a label from this table into the
filter.

| Kind | What has to happen |
| --- | --- |
| Registration | The contractor supplies the onboarding details the company requires and finishes setting up their Wingspan account. Accepting the invite is only the first part of it. |
| Payout method | The contractor adds a bank account or other destination so a payment has somewhere to land. |
| Tax verification | Either the contractor shares their tax information with the company, or the company records and verifies the contractor's taxpayer details itself. Wingspan checks the taxpayer identification number, and the requirement completes when a verified W-9 for that contractor is on file. |
| Signature | The contractor signs a document the company put in front of them, such as a contract or an attestation. It completes only once every expected signer has, which can include the company's own countersignature. |
| Document upload | The contractor uploads a file the company asked for, such as a licence or a certification, and the company reviews it if its review policy says to. |
| Background check | The company orders the check against a configured package, then sends the contractor to the vendor's application. The result comes back as pass or fail; the company reviews a failing result and handles any adverse-action steps outside Wingspan. |
| Identity verification | The contractor proves who they are, typically with a government ID and a selfie taken in a guided session. |
| Insurance coverage | The company sets up the coverage watch with the limits it requires. Coverage is then satisfied either by a certificate the contractor uploads or, when the coverage configuration allows it, by a Wingspan plan the contractor is enrolled in, and a lapse or expiry reopens the requirement. |
| Outside vendor | A verifier the company nominates confirms a credential at its source and reports the result back. |
| Acknowledgement | The contractor confirms they have read or agree to something the company posted. |
| Licence | A legacy kind still carried by older definitions; completion rides an external verification. |
| External completion | Something happens in the company's own system and the company reports the result. Existing definitions of this kind still report progress. |

Every one of these is finished by the contractor in their own Wingspan account,
by the company in the Wingspan app, or by Wingspan itself where it watches the
underlying record. None of them can be completed from here.

## Three properties that decide whether it matters

`search_requirements` reports all three per definition.

- **`blocking`** — what Wingspan reports for that definition: whether an
  outstanding copy stops a payment. A contractor's own copy can be blocking or
  not depending on where it was attached. `get_contractor` treats every
  incomplete requirement as blocking and does not read that setting; which
  placement merely tracks a requirement is visible only in the Wingspan app.
- **`gracePeriodDays`** — the days from when a requirement is attached to a
  contractor before an outstanding copy starts holding up a payment. Inside that
  window an unfinished requirement does not block.
- **`expiresAfterDays`** — how long a completed requirement stays valid before
  it lapses and has to be renewed; an insurance definition carries none, because
  there the expiry date comes from the policy itself. This is what makes
  `requirementState: "expiring"` and `"expired"` worth checking on a roster.

Alongside them, `actionBy` carries two separate answers — whether the
contractor has to act, and whether the company has to. Either, both, or neither
can be true; neither means Wingspan watches the underlying record itself.
Wingspan derives these from what one contractor's own copy is waiting on, so
do not treat them as fixed by the template. `reviewPolicy` says whether the company reviews
what was submitted: never, always, or only when the result fails.

## Retired definitions

A definition the company stopped using is hidden by default, and
`search_requirements` says how many were hidden on that page. Pass
`includeInactive: true` to see them: an old contractor can still be carrying a
copy of one.
