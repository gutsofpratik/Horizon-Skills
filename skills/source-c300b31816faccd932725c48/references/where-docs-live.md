# Where architecture docs live

The places architecture docs can live, what each is for, and how to reach it. This
skill searches these, and the `architecture-author` skill chooses a home among them
when writing. Neither describes the places itself — this file owns them.

Three facts shape everything below.

**The places are independent, and they can disagree.** The same system may be
documented in more than one. Where two accounts differ, report the difference rather
than reconciling it silently: one of them has drifted, and which one is a fact the team
needs.

**Reachability depends on what is connected, not on where the file sits.** Hosted
agents have no checkout, but that does not make a repository invisible to them: a repo
reaches them if it is connected as a documentation source, or registered as a plugin.
So "will an agent have this during an investigation" is a question about connections,
never about whether the docs happen to live in a repo.

**One document can be reachable by more than one route.** The organization's document
search is a single index over several providers, so the same content can arrive
labelled as a plugin, a repository, or a wiki page. Read the provider on each result —
it tells you which place answered. Two results for one system under different providers
are the divergence case above, and they may not even be the same revision.

## 1. The plugin index

Architecture docs inside a plugin, alongside its `skills/`.

**What it is for.** Orientation. What systems exist, what they are called, and where
the depth lives. An agent reads this first to pick up the estate's vocabulary before
searching anything else, and it is the one layer a hosted agent always has.

**Start from the plugin list the `extensions` skill mapped**, the first step under
"Where you are running" in the skill. That map is which plugins exist, where each
lives, and their sync state.

**Architecture docs inside plugins can be fetched through the document tools** — the
incident.io connection's `document_search`, then `document_show` for the full text. A
registered plugin's files are indexed: results carry `extension_plugin` as the provider
and a URL pointing into the plugin's repository, so a plugin's docs are readable even
with no local copy of its repo.

Where the session has no incident.io connection, say the plugins could not be checked
and carry on with the other places.

**The index is allowed to be incomplete.** A system missing from it is not evidence
that the system is undocumented — depth can exist in any other place with no index
entry. Absence here starts a search; it never ends one.

## 2. The code repository the session is running against

Docs in the repository you are checked out on — conventionally `architecture/` or
`docs/architecture/`.

**What it is for.** Depth, for systems whose code lives here. Docs in the repo version
with the code they describe and get reviewed like it, which is what keeps them honest.

**Reaching it.** The filesystem. Start at the corpus README's "Where do I look?" map
when there is one; it resolves most questions in one hop, so grep only when the map
misses.

**What to check before assuming reach.** Whether this repository is also connected — as
a documentation source, or as a registered plugin. If it is, the same files answer for
hosted agents too, and the indexed copy may be a different revision from your working
tree. If it is not, this corpus exists for people with a checkout and for nobody else,
which is worth saying out loud when the docs are meant for investigations.

**What you cannot see.** Other repositories. A system whose code lives elsewhere may
have a full corpus you cannot reach from here — its absence in this repo says nothing
about whether it exists.

## 3. The docs integration in incident.io

The organization's synced knowledge base: documents indexed from sources like Notion,
Confluence and GitHub.

**What it is for.** Depth, for teams whose architecture documentation already lives in
one of those sources. It is also where a system with no repository of its own tends to
be documented — a vendor product, or an estate service like observability or CI.

**Reaching it.** The incident.io connection's `document_search` — the identifier via
`keywords`, the question via `queries` — then `document_show` to read a candidate in
full. Results carry a provider and generated tags; architecture-shaped documents
describe systems and infrastructure rather than procedures. Where the session has no
incident.io connection, skip this place and say so.

**What you cannot see.** Anything not yet synced, and anything in a source the
organization has not connected. Writing here means authoring in the source —
incident.io reads its sources and never writes to them.

## 4. A provider search tool the session already has

A Notion or wiki search the session holds directly, when the user points you at one.

**What it is for.** The same documents as place 3, reached without the sync. It can see
what was never indexed, and it sees the current version rather than the last synced
one.

**Reaching it.** Whatever tool the session exposes. This place exists only when the
user names it; do not go looking.

## Reading: index first, then depth

1. Read the plugin index to learn what exists and what it is called.
2. Search the depth places with that vocabulary — the repository, the docs integration,
   and any provider tool you were pointed at.

The index earns its place by making the second step's search terms right. Skip absent
places without comment, but distinguish a place that held nothing from a place you
could not ask: those are different findings, and reporting a failed lookup as an empty
one is the worst mistake available here.
