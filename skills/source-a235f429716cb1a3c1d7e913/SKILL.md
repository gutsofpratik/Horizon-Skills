---
name: outstanding
description: List the contractors who have one named onboarding requirement outstanding, such as a W-9, a certificate of insurance or a background check. Run it with the requirement's name. It reports who has not finished the requirement; it does not confirm whose payments are blocked by it.
disable-model-invocation: true
argument-hint: "[requirement name]"
---

# Who still has this outstanding: $ARGUMENTS

A **requirement** is something a contractor must satisfy before the company can
pay them. The company configures each one once, and every contractor placed on
an engagement gets their own copy. This answers "who has not finished
$ARGUMENTS". It does not answer "whose payment is blocked": whether an
outstanding copy blocks payment depends on where it was attached, which these
tools do not read.

If no requirement was named, list the company's requirements with
`search_requirements` and ask which one the user means. Do not guess.

## Step 1 — find the requirement

Call `search_requirements`. Match `$ARGUMENTS` against the `name` of each
result, case-insensitively and in full. A partial name does not count as a
match. The result is one page; if nothing on it matches and the result carries
`pagination.nextPageArgs`, call again with those arguments and keep going until
a match appears or there is no next page. Only then is "no match" true.

- **No match on any page.** Show the names that came back and ask which one
  was meant. Do not substitute a similar-sounding one.
- **More than one match.** Show the candidates and ask. Requirement names can
  be near-identical across engagements, and answering for the wrong one is
  worse than asking.

Keep two fields from the match: its `requirementDefinitionId` and its
`blocking` value.

## Step 2 — find who has not finished it

Call `search_contractors` with `requirement` set to that
`requirementDefinitionId` and `requirementState` set to `incomplete`, which
means outstanding — the contractor has not finished it.

That returns one page. Report the page, then offer the next one using the
result's `pagination.nextPageArgs`; do not fetch further pages unasked.

## Step 3 — report

Lead with the count and the requirement's full name, worded as "have this
outstanding", not "are blocked". Then list the contractors by name, with their
onboarding state, so the user can see who has not even signed up yet versus
who signed up and has not finished.

Always add this caveat, whatever the definition's `blocking` value says:
whether an outstanding copy actually holds up a payment depends on where the
requirement was attached to that contractor. A placement that is not blocking
only tracks the copy; an engagement placement can also block eligibility while
still allowing payment. `get_contractor` does not read that setting and treats
every incomplete requirement as blocking, so the Wingspan app is the place to
confirm before telling anyone their payment is or is not blocked. If the
definition is not marked blocking, say so as well: an outstanding copy is then
usually tracked rather than holding anyone up.

Then add whichever of these applies:
- **If the user wants a different slice**, the same pair of calls answers it
  with a different `requirementState`: `pendingReview` for submitted and not
  yet reviewed, `expiring` for satisfied but about to lapse, `expired` for
  lapsed, `complete` for finished.
- **A rejected or revoked requirement reads as outstanding again.** One the
  company rejected, or one whose underlying record was revoked or failed, is
  reopened rather than failed, with a reason recorded. There is no failed
  state, so say "reopened after review" rather than "never started" about such
  a contractor.

For one contractor's full picture, `get_contractor` with their `contractorId`.

## What cannot be done from here

Nudging a contractor, approving or rejecting what they submitted, resetting or
renewing a requirement, and extending an expiry date all happen in the Wingspan
app. So does everything the contractor does themselves — signing, uploading,
verifying identity. Sharing tax information is usually the contractor's step
too, but a company can instead record and verify a contractor's taxpayer
details itself, in the app.
