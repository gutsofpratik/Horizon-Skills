---
name: catalog
description: >
  The organisation's catalog in incident.io: its types and entries (services, teams,
  components, customers, users and whatever else it models), their attributes, and the
  references between them. Use whenever you're working with any of these in any way,
  including plain reads ("who owns checkout?", "what is Atlas?", "what depends on
  search?", "who's in the platform team?") and finding an entry's ID before setting a
  field or escalating. Load it before the first catalog or team tool call: the tools
  return raw entries and references, and this skill says how to prove a match and walk a
  reference. Not for schedule rotas and shifts (the on-call skill), nor how a system works
  internally (architecture docs, but ground the subject here first).
---

# Catalog

The catalog is the organisation's structured map of itself: **types** (Service, Team,
Customer…) each with a schema of attributes, and **entries** (search-indexer, Data Platform…)
holding values for those attributes. Attributes that reference other entries render as
`Name (ID)` — the ID in parentheses is how you hop. The catalog is authoritative: when
conversation or incident context disagrees with it, the catalog wins, and you say so.

Three kinds of type, told apart by `type_name`:

- `Custom["…"]` — org-defined types, often the best match for an organisational
  question. Search these first, but do not assume their entries were added by hand.
- Native (`EscalationPath`, `Schedule`, `User`, `AlertPriority`…) — incident.io's own
  resources. Teams are not native: they live on an org-defined type, usually
  `Custom["Team"]`, so use `team_list` and `team_show` rather than guessing its name.
  Contact details for a person (email, and phone numbers where the org exposes them) live
  on their `User` entry: resolve the person, then read the entry.
- Integration-synced (`GitHubRepository`, `PagerDutyService`, `SlackChannel`…) — mirrors
  of other tools, often thousands of entries. Only search these when the user names the
  integration; "the ingest service" means the org's Service entry, not its GitHub repo.

**Where a type's entries come from.** `type_name` tells you which kind a type is, not
who maintains its entries. For that, read `registry_type` and `is_editable` from
`catalog_type_list`. A type with a `registry_type` is managed by incident.io, as its own
resources or an integration it syncs, and isn't editable. A type without one isn't
synced by incident.io, but an external job such as
catalog-importer or Terraform may still write it through the API, and these tools
can't see that: call it not integration-synced rather than hand-maintained. An
attribute's `mode` describes that one field. For provenance questions, lead with the
source and editability verdict plus that caveat; omit attribute inventories and entry
counts unless asked.

Use the incident.io connection's `catalog_type_list`, `catalog_entry_list` and
`catalog_entry_show` tools directly. Inspect a tool's input schema before first use.
If the connection is unavailable, say what could not be checked; do not invent an entry.

## Orient before you search

One `catalog_type_list` call returns every type **with its attribute schema**. Orient
once per conversation, before your first search, and plan the whole walk from it: which
types could hold the subject, which attribute chain reaches the answer. Every org's catalog is bespoke — type and attribute names here are
examples, and a guessed type_name (`Service` instead of `Custom["Service"]`) matches
nothing and looks like the entry doesn't exist.

## Finding an entry

- Let the question's own type hint set your search breadth. A typed mention ("the
  checkout *service*", "the *team* that owns billing") narrows to that type and its
  neighbours; a bare name ("what is Atlas?") tells you nothing about kind, so sweep the
  org's custom types in parallel — curated types are few — before native or integration
  ones. A single-type search is only justified when the question named the type.
- Search matches entry **names and identifiers only** — not descriptions or attribute
  values. A miss means "not in the types searched", never "doesn't exist". List a small
  type outright before concluding an entry isn't there.
- **A search hit is not an exact identifier.** An alert or field value matches an entry
  by its ID, external ID or an alias, and by its name only when the type's
  `use_name_as_identifier` is true. Prove a match with `identifier`, and never offer
  the display name as a value that will match when that flag is false.
- **Absence is type-local.** `catalog_type_list` describes schemas, not entries: a Service
  search cannot establish whether Customer has a similarly named entry. Before saying
  "no Customer entry matches", query Customer for that name or identifier and page to
  `has_more: false`; otherwise say Customer was not checked. "No schema link to this
  service" is different from "no matching Customer entries."
- When one name matches entries in several types (an "Atlas" component and an "Atlas"
  project), lead with both candidates, their types and IDs. A reference between them
  does not prove which one an alert names; ask for the alert or its identifier if the
  distinction matters. Don't headline one as the answer and mention the other later.
- A filtered search's hits are not the size of a type. Call them matches in the types
  searched; claim a type total only from an authoritative count or an unfiltered list
  paged to the end. `has_more: true` means the listing is incomplete.

## Walking relationships

**The reference lives on the entry that points, and the tools only read that direction.**
Orient every relationship question by asking: which type's schema holds the attribute?

- **Forward** (the subject holds the attribute — "who owns the search-indexer?"): read the
  `Name (ID)` straight off the entry's attribute value; `catalog_entry_show <id>` when
  you need the target's full, untruncated attributes.
- **Reverse** (other entries point at the subject — "what calls the message-bus?",
  "what does the Data Platform team own?"): the reference lives on the entries that
  point, never on the subject's own outgoing attributes. Find the referencing type and
  attribute ID in the schema, then call `catalog_entry_list` with `attribute_filters`:
  `[{ "attribute_id": "<referencing-attribute-id>", "operator": "one_of", "entry_ids": ["<subject-id>"] }]`.
  It matches the target's ID, external ID and aliases and pages only the matching
  entries. An unknown or archived target is an error, not proof it has no dependents.
- **Unowned or unset** ("which services have no Owner?"): filter the referencing type
  with `operator: "is_blank"` on the stored reference attribute. A reference to an
  archived owner reads `Name (Archived) (ID)` and counts as set, so `is_blank` never
  returns it: report those apart from the empty ones, not as unset.
- **Combined conditions** ("unowned tier-1 services"): put one filter per attribute in
  the same `attribute_filters` list; they AND together, so no manual intersection.
- **Current state, not history:** an `is_blank` or `is_set` scan only shows what is set
  now. Say "currently unset"; do not say "never set" without a historical read.
- **Complete owner breakdown:** page both `is_blank` and `is_set` for the same stored
  reference attribute to `has_more: false`.
  Together they partition active entries, so their counts give the total without
  listing the entire type again. On the set side, list `(Archived)` references
  separately: a stored value is not necessarily a working owner.
- **Multi-hop** ("which customers are affected if X goes down?"): chain the filtered
  reverse hops deliberately — to X's dependents, then from services to the type that
  references them. Check the schema at each hop, and name what the chain did and did
  not establish.

For a count alone, request `include_total_count: true` without an attribute filter;
a small `page_size` avoids pulling a whole page just for that figure. The count is
optional and can time out; when absent, page to `has_more: false` before claiming a
total. A count from `search` is only for that search, not the type.

## Team membership

`team_show.members.items` holds direct members with user IDs and names from the
configured team attribute. Follow `members.pagination.next_cursor` until `has_more`
is false for a full roster; `members.configured: false` is not an empty team. These
are direct members, not everyone inherited through child teams. For a person's
teams, find their User entry and filter the configured Team type by its members
attribute with a `catalog_entry_list` `one_of` attribute filter; don't substitute a
job title or Slack group for a Team entry. `team_show.resources.items` lists linked
operational resources, not catalog entries pointing at the team: an empty list
never proves the team owns no services. Use the reverse lookup above before making that claim.

For a team hierarchy, remember the parent reference is stored on the child: reading
it forward from a team gives its ancestors. For descendants, filter the Team type
with a `one_of` attribute filter on the parent attribute for the starting team,
then repeat for each team found, paging each level to `has_more: false`. The
starting team is not its own descendant: list the
distinct teams below it with IDs. Give a descendant count only if asked,
and only after excluding the starting team's ID from the complete set.

## Finding a service's escalation path

"Who gets paged for *a service or component*" begins with a catalog walk: schedules
know about people and shifts, not service ownership.

1. Find the service entry and follow its owner reference (check the schema for the
   attribute linking to a Team or `EscalationPath`).
2. Name the team and path backed by that reference. `team_show` can list a team's paths;
   `escalation_path_list` searches by name, but a similarly named path is not proof that
   the service uses it.
3. If the Owner reference reads `(Archived)`, lead with that: the team is archived and
   is not a current owner to contact. If the reference does not resolve at all, say so.
   Without a live owner, say no path for this service was verified, and send the user
   to confirm and update the Owner.
   Do not suggest a former parent, lead, successor, default path or platform on-call
   unless a read links it to this service.
4. If the team resolves but has no linked path, say so. Members and similarly named
   paths do not establish routing; do not offer to page them.
5. If the user asked for the current person or a future shift, hand the identified path
   to the on-call skill. The catalog's job ends at naming the path.

## Resolving values for writes

This read skill cannot edit catalog entries or types. Explain the needed change, but do not offer to set Owner or edit
a catalog entry. An incident custom-field write through another available tool
is a separate action.

Before setting a catalog-typed custom field or escalating: resolve the name to an
identifier with a catalog read, and pass the identifier, never the display name — names
are ambiguous and case-drifted, and a write against the wrong entry lands on a real
incident or pages a real person. If the resolution was fuzzy (several candidates, or a
weak match), confirm with the user before the write, not after.

## Answering

- Asked to describe an org resource ("tell me about X", "what is X"), the catalog is the
  grounding: what X is in *this* org, who owns it, what it connects to. Documentation
  can add how it works — it never substitutes, because docs found by keyword may
  describe a different X than the entry the org actually operates.
- Include IDs alongside names (`Data Platform (01ABC…)`) for anything the user might act
  on next — the next step, yours or theirs, needs the ID and shouldn't re-resolve it.
- When asked for a **complete list**, deliver every matching entry's name and
  catalog ID after paging. Do not compress rows into a range or offer to give
  IDs later. If output is partial, state what is missing; count-only answers
  need not print entries.
