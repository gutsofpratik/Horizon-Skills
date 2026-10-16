# Choosing a mechanism

Users describe problems and wishes, not mechanisms: "investigations don't know about
our feature flags", "I want these steps run when checkout breaks". This file maps a
stated problem to the right piece of the platform — and most real requests decompose
into more than one piece. Note that a user saying "skill" doesn't settle anything:
people call everything a skill. Map the need, not the word.

The output here is the mechanism choice, stated with the reason — not a detailed plan
of what to build. Planning and drafting the content belong to the owning skills the
hand-off section names.

Ground the recommendation before making it: read the estate
([estate.md](estate.md)) first. A mechanism that leans on a connection nobody has made
can't work — recommend the connection alongside, and say which parts wait on it.

## The mechanisms

- **Connector** — gives agents *access* to a system they can't currently reach.
  Prefer a native integration where one exists (see
  [extensions-product.md](extensions-product.md)).
- **Skill** — teaches agents to understand and navigate the organization's systems and
  data: the knowledge an experienced responder holds implicitly. Loaded inline by the
  agent reasoning about the incident.
- **Triage skill** — a skill that describes itself as owning a system's or incident
  class's opening procedure. Investigations identify these and run them at the start,
  alongside the initial searches, so their findings shape the first hypothesis.
- **Architecture doc** — facts about a system: what it is, where it runs, what it
  depends on, the real names of things.

## Diagnose the need

Ask, in order — the first question that fits usually names the mechanism:

1. **Can agents reach the data at all?** A source of information nothing is connected
   to — feature flags, deployments, an internal admin system — is an access problem.
   → a **connector** (or a native integration where one exists). A connector alone is
   rarely enough: pair it with a skill that says when to call it and what its results
   mean.
2. **Is the gap what a system *is*?** Agents that don't know where something runs,
   what it depends on, or what its real names are need facts, not procedure.
   → an **architecture doc**.
3. **Is the data reachable but misread?** The connection exists, but agents use it
   badly in this organization's context — misreading the Sentry setup, misinterpreting
   deploy events across services, not knowing which of a connector's tools matters.
   → a **skill**.
4. **Should it happen at the start of every matching investigation?** Custom triage —
   where to look first for a class of incident, so the first hypothesis is faster and
   more accurate. → a **triage skill**.

## Worked examples

From statement to recommendation — note most real requests decompose into more than
one mechanism:

- *"I want these steps run at the start of an investigation."* → a **triage skill**
  carrying the procedure. If the steps read data through a connector whose use is
  non-obvious in this organization, add a **skill** that teaches that navigation — the
  triage skill leans on it. If the data isn't reachable at all, a **connector** comes
  first.
- *"Investigations don't know anything about our feature flags."* → a **connector**
  to the flag system (native integration first if one exists), plus a **skill** on
  reading this organization's flags — which projects matter, how targeting is
  structured.
- *"The agent didn't know what service X even was."* → an **architecture doc** for
  that system. If the confusion recurs across incidents, that's a corpus gap, not a
  skill gap.

## Hand off

Once the mechanism is chosen, the work belongs to its owner:

- **Skill or triage skill** → the `skill-authoring` skill's create job; for triage
  skills it carries a dedicated reference on authoring for an automated caller.
- **Architecture doc** → the `architecture-author` skill.
- **Connector** → the dashboard's Extensions page; the companion skill, once it's
  connected, goes through `skill-authoring`.

Name every piece of the decomposition up front, then hand each to its owner in
dependency order — connections before the content that leans on them.

Hand over context, not just a mechanism name. Carry the user's description, the
organization-specific knowledge gathered on the way, and where their reference
material lives. The owning skills demand this before drafting anyway — arriving with
it is the difference between content drafted from the team's expertise and content
drafted from a topic name.
