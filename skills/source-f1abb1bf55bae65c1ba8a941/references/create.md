# Create a skill

Author a new skill into the user's plugin. The hard part isn't the prose — it's knowing
what the skill is for concretely enough that the description triggers and the
instructions survive contact with a real request.

## 1. Pin the skill down with concrete examples

Never draft from a topic name. Get to at least two real requests the skill should
handle — from the user directly, or proposed by you and confirmed. Useful questions,
one or two at a time:

- "What would someone say that should load this skill?"
- "Walk me through the last time a person did this by hand — what did they look at,
  in what order?"
- "What does a finished answer look like? What must it always include?"

### What a skill is for

The examples say what the skill handles; the organization's own knowledge says how.
A skill exists to give an already-capable agent the two things it can't derive:

- **Domain expertise** — the judgment an experienced responder brings: what matters,
  what to check first, how to read what comes back.
- **Organization-specific knowledge** — how this team's systems are actually
  arranged: which services report where, what maps to what, the real names of things.

"Create a skill for X" names a topic and carries neither — it is never enough to
draft from, and the gap is not yours to fill by guessing. The most common authoring
failure is drafting without it: a user asks for "a skill for using Sentry" and never
says how their organization actually uses Sentry — which services report to it, how
projects are structured, what corresponds to what. A skill written without that
context reads plausibly and helps nobody.

### Load the context before drafting

1. **The user's expertise.** How does this organization use the system? Which parts
   matter, what maps to what, what does the team know that an outsider wouldn't?
   Good looks like "checkout errors report to the `payments` project; `mobile`
   belongs to another team" — not "we use Sentry for errors".
2. **Existing reference material.** Where does written knowledge live — the
   repository, Confluence or Notion, an existing skill or runbook? Good looks like a
   page or runbook you can read directly, rather than the user retyping what they
   remember of it.
3. **Reach.** Are the systems the skill will cover behind a connection the agents can
   actually call, with the auth it needs? Good looks like a named connection whose
   tools you'll probe in step 3 — asked about now, so a missing one surfaces before
   drafting starts, not after.

### Exploration helps, but can't answer "what for"

Some of this can be worked out rather than asked for: exploring the connected surface
(step 3's probing) can turn up real organization-specific facts — which projects
exist, undocumented states, traps in the data. Offer that exploration, and bring what
it finds back as proposals to confirm ("there's one pipeline and it deploys production
from master — is that the one this skill is about?"). But exploration only reveals
what the systems are. What the skill is *for* — the situations it must handle, the
procedure the team actually follows, the judgment an experienced responder would
bring — only the user can supply. Probe findings feed the conversation; they never
replace it.

### Confirm the scope before drafting

Conclude when you can state — and say where each part came from:

- the trigger phrases
- the procedure's shape
- the tools it calls
- what the output must contain
- the organization-specific knowledge the skill will carry

Anything sourced from your own exploration rather than the user is unconfirmed. Then
propose the scope back — what the skill will handle, what it won't, what it leans
on — and draft only on a yes.

If the requests turn out to be two unrelated jobs, that's two skills — say so now,
not after drafting. And when the user can't or won't supply the context, say plainly
that the result will be generic and unlikely to help, and prefer not drafting over
shipping it — a skill that adds nothing still costs selection every time it
competes.

Context the user supplies often contains facts about what a system *is* — where it
runs, what it depends on, its real names. Those belong in the team's architecture
docs, not buried in the skill: write them through the `architecture-author` skill
in the same change, and let the skill lean on the docs.

## 2. Check it doesn't already exist

Search the plugin's skills table and any other plugins in the session for a skill that
owns this job or a neighboring one. Extending an existing skill beats writing a
sibling; two skills triggering on the same phrases split every future selection between
them. When extending, keep the existing skill's identity: same directory, description
grown rather than replaced.

## 3. Plan the resources

For each concrete example, work out what an agent executing it repeatedly would want on
hand:

- Knowledge it can't derive — schemas, decision tables, error-code cribs →
  `references/`.
- A fragile operation it would rewrite each time → `scripts/` (rare; most skills need
  none).
- Everything else stays out. A skill carries what the job needs, not what the author
  knows.

Then probe every surface the skill will name, before drafting against it. For each tool,
datasource, store or index, run the cheapest real call that answers four questions:

- **Can you call it, and read what comes back?** What a connection advertises is not what
  it serves — tool sets are allowlisted, fields restricted, scopes narrower than the
  product offers. Most of it surfaces only when a call is refused.
- **Does it cover what you think it covers?** A name that resolves may be populated by one
  environment only, or carry nothing to filter the subject you care about. A surface that
  answers a fleet-wide question can be worthless for a single-subject one — and it will
  answer anyway, in the same shape, from the wrong population.
- **Does it represent what the job needs?** A surface can be exactly what its name says
  and still model something other than the question being asked. Something called
  `connections` may hold every connection ever made, when the job needs whether one is
  live now. A "last successful connection" timestamp may be honest and still record a
  different event than the one you want to date. The test is not whether the name is
  fair, but whether the values answer the question the skill will put to them.
- **How much comes back per thing you ask about?** One-per-subject and many-per-subject
  need different instructions. Guessing this is how a skill silently merges two subjects.

Reading the schema, the docs or the source is not probing: each describes what exists, not
what this session can reach or what it returns here. And a surface that fails any of these
questions is a design input, not a bug to fix later — it changes what the skill can
honestly promise.

Keep the answers as a claims list — every fact the skill will state about an external
system, and how each one was checked. Facts that survive get written; the rest are dropped
or generalized to their pattern form per [format.md](format.md). Carry the list into the
change, so a reviewer sees what was verified instead of taking it on trust.

A surface this session can't reach at all is not a pass. Record the claim as unverified,
and put the question to the user — the absence path's second class, answered by them and
recorded as user-reported — rather than writing it as though it were checked.

## 4. Draft to the format

Write SKILL.md and its references per [format.md](format.md) — or the plugin's own
conventions where it has them — with [example.md](example.md) open as the target
picture. The rules that matter most for a new skill:

- **Shape it as a utility, not a task script**: teach the system (model, vocabulary,
  tool surface, how to read results), then the flows — per the anatomy in
  [what-works.md](what-works.md). The concrete requests from step 1 become its common
  flows, and stay answerable when the next question is one the author never wrote
  down.
- Spend the most care on the frontmatter description: it's the only part an agent sees
  before choosing. Lead with the subject stated broadly ("use whenever you're working
  with X"), add the two or three signals from step 1 that only this skill matches, and
  keep it to a few sentences — activation comes from the subject, not from enumerating
  phrasings.
- Stamp the frontmatter with this plugin's version under `metadata`, per the provenance
  stamp section of [format.md](format.md): read the version from the plugin manifest
  (or write `"mcp"` when you loaded this skill through the MCP server's skill tools),
  quote it, never type it from memory. This is how incident.io knows the skill came
  through this flow.
- Name connections and bare tools, arguments as data — never an invocation syntax;
  telemetry names its datasource, never the tool that runs the query.
- Write the abstention path: what the skill says when the tools come back empty or the
  question falls outside it.

## 5. Road-test it with fresh eyes

The author knows too much to read their own instructions cold, so before shipping,
someone who didn't write the skill has to execute it. Three ways to get that, in order
of preference:

**Where the session has the incident.io connection's `extension_verify`**, verify the
draft before anything lands. How you point it at the tree depends on what exists:

- **The plugin already syncs.** Give the plugin and the changed files as full contents
  (`changes: [{path, content}]`, plugin-root-relative — new files included; they are
  overlaid on the synced version in memory, so nothing ships).
- **A plugin's first skill, or no plugin at all.** There is no synced version to overlay
  onto, so send the tree itself: `extension_upload_url` returns a URL, upload the plugin
  as a `.tar.gz`, then call `extension_verify` with the `mount_name` you uploaded to and
  no changes. The uploaded tree is what gets checked. Mount it under the name you intend
  to register the plugin as, or paths inside your skills resolve differently here than
  they will in production.
- **The content is on a branch.** Give the repository, the ref and a `mount_name`, and
  the run reads that branch — which is how you check work you have pushed but not
  merged.

Whichever route, give it a `description` built from step 1 — the requests the skill
should handle, and what a right answer contains. A verification agent writes concrete
expectations, hands realistic requests to a fresh agent that has the tree and no
knowledge of your intent, and grades the expectations on what that agent actually did —
which skills it loaded, what it read, what it answered. Poll `extension_verify_show`
with the returned id; runs take a few minutes.

Read the result as evidence, not a verdict light. Each expectation carries the
behavior that decided it. `simulated_calls` lists every external call the fresh agent
imagined rather than made; `real_calls` lists the ones that reached a connected system
and were really answered. Find your load-bearing step in one of those two lists: in
`simulated_calls` a pass proves the skill routes to the right place, and only in
`real_calls` does it prove the skill works. Set `live_connectors` to move reads from the
first list to the second — writes are never made whatever you set. Failures come with
`suggested_edits` anchored to file and quote: apply them locally and verify again —
a round or two is normal, and the wording that survives is the wording to ship. When
two identical scenario runs disagree, your instruction reads two ways; that is a
defect in the sentence, not noise in the sampler.

**Where it doesn't**, have a fresh session execute the skill by hand: a new agent,
given one of step 1's realistic requests and nothing else — no drafting context, no
explanation of intent. Its calls are real, not imagined — and so are a rehearsal's when
you set `live_connectors`, so this is no longer the only route that reaches a real
system. Reach for a fresh session when you want to watch a reader stumble in the open;
reach for the rehearsal when you want expectations graded against what the reader did.
Watch where it stumbles:
a wrong tool call, a guessed value, a step it interpreted two ways, an ending short of
the output contract. Every stumble is a missing sentence in the skill, not a failing of
the reader — fix the skill and re-run.

**Where the session can't spawn a fresh reader either**, hand the draft and a request
to the user to try in a new session, and ship after their run rather than before.

## 6. Register it

In the same change: add the skill's row to the plugin README's skills table, and a
connections-table row for any new connection it calls, per the registration rules in
[format.md](format.md). This step is not optional polish. Before proposing the change,
check the provenance stamp is present and carries the version you read from the
manifest — a road test that rewrote the frontmatter can drop it.

## 7. Ship it and confirm it arrived

How the skill reaches agents depends on the session:

- **Working in the plugin's repository** (the common case): commit on a branch and
  propose a pull request per the team's flow. The plugin syncs from the repository's
  default branch, so the skill goes live when the change lands there. Where the checkout
  can't be committed from this session, edit in place and tell the user exactly what
  to land and how.
- **The session has the incident.io connection's extension tools**: after the change
  lands, `extension_plugin_sync` (with the plugin's id from `extension_plugin_list`)
  pulls it immediately rather than waiting for the next scheduled sync. Then confirm
  the new skill appears in the plugin's skill list.
- **Neither**: hand the user the files and say what to do — where they go, and that
  the plugin needs a sync after they land.

If the plugin uses a skill allowlist rather than automatic selection (a setting on the
plugin's page in the incident.io dashboard), a new skill also needs enabling there —
say so rather than assuming automatic pickup.

### Hand over for review

When you hand over the pull request, say in a few lines what to check — in the voice
the `talking-to-the-user` skill sets:

- **Facts, not wording.** Give them step 3's claims list to tick off — every name,
  tool, data source, number and owner the skill states, and how each was checked. Edit a
  sentence only when it reads two ways or is false; the reader is an agent.
- **The description, as the trigger it is.** Would they want this skill used in the
  situations it names, and only those?
- **The procedure, as if on call.** A step that makes them ask "which one?" or "how?"
  is where the agent will guess — fix the line.

Once they've checked those, they merge. For a first skill, the plugin is added to
incident.io after the merge — the `extensions` skill's job, and it says why the order
matters.

## 8. Say how you'll know it worked

End by telling the user what happens after the merge, in their words: the skill's page
in the incident.io dashboard (and the plugin's, across all its skills) shows each time
an incident used it, whether it helped, and what went wrong — empty until a matching
incident happens, which is normal in the first days. To fix a problem, they bring it
back to a session with the incident.io skills loaded; the [improve](improve.md) job
edits the skill from that evidence.

Say too what you couldn't verify: any surface this session couldn't reach, and the claim
resting on it. That makes the gap a decision the team takes rather than an assumption
buried in the skill.

It is important to note which connector tool calls were overridden or simulated during
verification so that the user understands which parts have been fully exercised and 
which parts are not yet confirmed to be working.

When you tell the user how the tests went, pass or fail, add a one-line footnote: some
calls can't be made for real during a test, so there are limits to how much certainty it can offer, and
<https://docs.incident.io/nexus/extensions/incident-skills-plugin#limits-of-verification>
explains them.
