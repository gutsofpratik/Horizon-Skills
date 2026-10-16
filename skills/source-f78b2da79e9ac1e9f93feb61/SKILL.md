---
name: postmortem
description: >
  Work with an incident's postmortem document — the write-up a team produces after an
  incident. Use when the conversation is about a postmortem, post-incident review,
  debrief or retro document: finding it, creating one, reading it, changing its text, or
  reviewing it against what actually happened. Covers rewriting a section, fixing a claim, adding a
  timeline entry or a learning, and also judging whether its claims hold up, what is
  missing, and what should become a follow-up. Not for general questions about an
  incident, which is the incidents skill.
---

# Postmortems

A postmortem is generated from a template: a set of sections, each with a title and,
often, help text telling the writer what belongs there. The help text is the standard a
section is measured against.

An incident usually has one document, but it can have several.

Everything here is one of three jobs. **Finding and reading** comes first and both other
jobs depend on it, because which rendering you read decides whether your work lands.
**Editing** changes the text. **Reviewing** judges it and changes nothing.

## 1. Finding the document

**Find it with `postmortem_list`.** Pass `incident_id` to scope it to one incident: an
ID, an external ID, or a reference like `INC-123`. Each result carries the `id` the other
tools take, with the title, status and whether it is the incident's primary document.

**Check what kind of document it is, and whether it exists yet.** Everything below works
on `in_app` documents. An `external` one lives in a provider such as Notion, named in
`provider`, and nothing here reads or edits it: give the user its `url`. A `state` of
`pending` means it is still being created and holds only a placeholder, so wait for
`created` before reading it. `failed` means it never was, with the reason in `error`:
tell the user rather than trying again unasked.

**An incident can hold several documents.** When more than one comes back and the user
said "the post-mortem", tell them what exists and let them choose. Do not take the
primary one as what they meant — working on the wrong document is silent, and they will
not find out from you.

You already have the id without calling this when `incident_show` was run with
`include: ["postmortem"]`, which carries the primary document's. That is the primary one
only, so it answers "the post-mortem" and not "which post-mortems".

**When there isn't one, `postmortem_create` makes it.** Choose a template with
`postmortem_template_list`, passing the incident to see its default. The template's
`kind` decides what you get: an `in_app` document, or an `external` one, which goes to a
destination from `postmortem_destination_list` or to the incident's default. A document
made from a template comes back `pending`: follow it with `postmortem_list` until it is
`created`. To write the post-mortem yourself, pass `content` as markdown instead of a
template, and it exists straight away.

## 2. Reading it

**There are two renderings of the same document, and they are not interchangeable.**

| | what it is | what to use it for |
|---|---|---|
| **Reader's form** — `incident_show` with `include: ["postmortem"]` | the document as a person sees it: mentions are names, and the blocks that fill themselves in from the incident are the lists they display | reading, quoting, reviewing |
| **Editable form** — `postmortem_show` | the same document with those parts as HTML tags carrying their IDs | the only valid source of anchors for an edit |

Reading the reader's form and then editing from it is the most common way to waste a
call: that text is not in the document, so nothing matches it. Read the form that fits
the job you are about to do.

**Read `format://postmortem-document`** before writing a tag you cannot copy from the
document in front of you. It lists every tag, its attributes and an example, and it is
the only place they are written down.

## 3. Editing

You change the document by describing string operations on its markdown. Read it with
`postmortem_show`, copy the exact text you want to act on out of what came back, and send
that text as the anchor for your edit. There is no cursor, no line number and no section
addressing: an anchor is a substring, and it has to match.

Everything in this section exists because that one mechanism has sharp edges.

### The loop

`postmortem_edit` takes the document ID and a list of edits, up to 50 in one call. The
call returns the whole document as markdown.

**Anchor your next edit on what came back, never on what you sent.** The returned
markdown is re-rendered from the document, so the bullet characters, blank lines and
escaping you wrote may not be the bytes now stored. A second edit built from your own
text is the single most common way to get "Found nothing matching".

Within one call, each edit applies to the result of the edit before it. If your second
edit anchors on text your first edit rewrote, anchor on the new text.

The whole call is refused if any single edit is, so nothing is ever half-applied. Fix the
edit that was named and send the batch again.

### The operations

| op | fields | what it does |
|---|---|---|
| `replace` | `old_string`, `new_string` | swaps a run of text, or one tag for another |
| `delete` | `old_string` | removes a run of text, or a whole node |
| `insert_before` | `anchor`, `text` | adds blocks before the block the anchor sits in |
| `insert_after` | `anchor`, `text` | adds blocks after the block the anchor sits in |
| `prepend` | `text` | adds blocks at the very start of the document |
| `append` | `text` | adds blocks at the very end |

`replace` works at any scale: a word, a sentence, a whole section including its heading.
Prefer one `replace` spanning a rewritten paragraph over five small ones, because every
anchor is another chance to miss.

`insert_before` and `insert_after` add **blocks**. They widen the anchor to the whole
block containing it and insert either side of that, so you cannot use them to put words
in the middle of a sentence. Use `replace` for that: make `old_string` the part of the
sentence you are changing and `new_string` the version with your words in it.

`new_string` may not be empty. Removing text is `delete`, which also tidies up the blank
lines the removed block leaves behind.

Inserted text is parsed as markdown, so headings, lists, tables and formatting all work,
and so do tags.

### Anchors

An anchor must appear **exactly once** in the document. Nothing is guessed: an anchor
matching nothing is refused, and an anchor matching several places is refused with the
surrounding text of each match so you can see what you hit.

- **Copy it. Do not retype it.** Anchors are matched against the markdown, not against
  what the text looks like on screen. A phrase that reads bold in the document is
  `**bold**` in the markdown, and an anchor without the asterisks does not match it. The
  same goes for links, inline code, list markers and heading hashes.
- **Some characters are escaped in ordinary text.** A literal underscore, asterisk,
  backtick, backslash, tilde, square bracket or angle bracket in the document is written
  with a backslash in front of it. Copying handles this; retyping does not.
- **When an anchor is ambiguous, extend it rather than shortening it.** Add the words
  before or after it, in the same string, until it names one place. For a mention that
  appears in several paragraphs, include the sentence it sits in.
- **Keep anchors as short as they can be while still unique.** A whole paragraph as an
  anchor for a one-word change means any other edit touching that paragraph invalidates
  it.

### Tags

A postmortem holds things markdown has no syntax for: mentions carrying the ID of a
person or record, blocks that fill themselves in from the incident, marks with no
markdown equivalent. These read and write as self-closing HTML tags.

```
Reported by <user id="01JOHANNA" value="Johanna Larsson" /> at <timestamp .../>.

<followups />
```

- **Leave tags alone unless you mean to remove what they point at.** Replacing
  `<user id="01JOHANNA" value="Johanna Larsson" />` with the words "Johanna Larsson"
  turns a live reference into dead text. The document stops knowing who that is.
- **To add one, copy a tag already in the document and change its attributes.** That is
  the safest route by far, because the ID is the part you cannot invent.
- **When there is nothing to copy, read `format://postmortem-document`.** Writing a tag
  from memory is how you get a tag name the document has no node for, which would be
  stored as visible markup rather than as a mention. That is refused rather than written,
  but it costs a round trip.
- **Tag names use hyphens, never underscores.** An underscore is not legal in an HTML tag
  name, so `<user_mention/>` is read as prose. The schema's internal type names use
  underscores; the tags do not.
- **Some tags are read-only.** A document that already holds one keeps it and your edits
  leave it alone, but writing a new one is refused. The format resource lists which.

Dynamic blocks like `<followups />`, `<timeline />` and `<custom-fields />` are not text
you can correct. They render from the incident's own data. If the timeline is wrong, the
incident's timeline is wrong, and the fix is there rather than in the document. To see
what one of them currently says, read the reader's form.

### When an edit is refused

The error says which edit and why. The common ones:

- **"Found nothing matching"** — the anchor is not in the document. Almost always because
  it was retyped, or taken from the reader's form, or built from the text you sent in a
  previous call rather than the text that came back. Read the document again with
  `postmortem_show` and copy from that.
- **"Found N places matching"** — extend the anchor with surrounding words. The error
  shows each match in context.
- **"The document changed while we were editing it"** — somebody typed in it between your
  read and your write. Read it again and re-apply. Do not re-send the same batch blind;
  their change may be the one you were about to make.
- **"is not something this document can hold"** — a tag name or attribute that is not in
  the vocabulary. Check `format://postmortem-document`.
- **"refers to something on an incident you cannot see"** — an image, follow-up or scribe
  tag whose ID belongs elsewhere. Copy the tag from this document rather than writing an
  ID.
- **"this document cannot be read as markdown"** or **"would change a part of it nobody
  asked to change"** — this particular document cannot go through the tool safely, so
  nothing was touched. Say so and point the user at the dashboard. This is about the
  document, not about your edit, and retrying will not help.

### Working with the user

The document is live and shared. Someone may have it open while you write to it, and
there is no draft and no review step, so treat every call as publishing.

- **Edit what was asked and nothing else.** Do not tidy wording, fix headings or
  restructure sections you were not asked about. It is their document and their voice.
- **For anything beyond a small correction, say what you are about to write and get
  agreement first.** Rewriting a section is not a small correction.
- **Say what you changed, in their words rather than in anchors.** "Rewrote the root
  cause paragraph" is useful; a diff of markdown is not.
- **Do not invent facts to fill a gap.** If a section is thin because nobody knows what
  happened, writing something plausible into the document is worse than leaving it thin.
  Check the incident's own record first, and say what you could not establish.

## 4. Reviewing

A review judges the document and changes nothing. Answer what is asked: a question gets
an answer, a request to create a follow-up creates one. Offer a review only when the user
asks for one.

When the user asks for a review, settle four things first:

- **Scope** — the whole document, or one section (timeline, root cause, action items)?
- **Focus** — factual accuracy, structure and clarity, learning value, or all three?
- **Audience** — the team, the whole organisation, or leadership?
- **Concerns** — anything they are already unsure about?

If they decline to answer, or tell you to get on with it: review all three dimensions,
assume an organisation-wide audience, and cover every section.

### The three dimensions

Use these as a guide for what to ask. Do not recite the framework at the user.

**Factual quality** — is it comprehensive and accurate?

- Are critical events, decisions or timeline entries missing?
- Do the timeline entries match the incident data?
- Were important contributing factors or context left out?
- Is anyone claiming something happened that did not, or the reverse?
- Are contributing factors evidenced?
- Does it cover both what enabled the incident and what limited the damage?
- Are there gaps in the narrative that leave a reader with questions?
- Are timestamps and durations right?

**Structure and tone** — can a reader who was not there follow it?

- Does each section meet the expectation its help text sets?
- Is the timeline a narrative of key moments and turning points, rather than an
  exhaustive audit trail?
- Is it clear what happened, and when?
- Is there jargon or assumed knowledge that blocks understanding?
- Is it blameless?

**Learning value** — will it prevent the next incident?

- Are the learnings specific and actionable, or vague and generic?
- Are action items identified, owned and achievable?
- Does it name systemic risks — key-person dependencies, process gaps, architectural
  problems — or only surface symptoms?
- Do the lessons reflect what the data shows?
- Would a reader gain something that applies to other incidents?

### Checking a claim against what happened

The incident's own record is what a claim is checked against: `incident_show`,
`incident_update_list` for how the response unfolded, and `action_list` and
`follow_up_list` for what came out of it. Where telemetry is connected, a claim about
system behaviour — "the error rate increased tenfold" — can be checked against it rather
than taken on trust.

Some incidents have no telemetry. That is not a finding.

### How to give the feedback

- Point at specific problems, with evidence from the incident data.
- **Quote the document** so every point lands somewhere concrete, and quote it
  verbatim rather than paraphrasing. Never invent a quote.
- Say what is missing or wrong, and why it matters.
- Give an actionable suggestion, not a verdict.
- Drop feedback the user cannot act on. If a section is simply fine, say nothing about it.
- Do not be pedantic about numbers unless the difference is material. "About 200" against
  a true 220 is not worth a comment.
- When you dispute a fact, say what makes you think it is wrong.

### Turning a review into changes

A review suggests; it does not write. When the user asks you to make the change rather
than describe it, go back to **Editing** above — and read the document with
`postmortem_show` first, because the text you quoted in the review came from the reader's
form and will not match.

A gap the review exposes — missing monitoring, a process that did not work — is worth a
follow-up rather than a sentence in the document. Create one when the user asks, or offer
when the gap is clear.
