# The progress stream

Review is the long part of a run — every sub-step of every leg the user picked, minutes
of work — and until it ends the user has nothing to read. The progress stream is what
they see meanwhile: one line per sub-step, written as that step finishes, so the run
can be followed while it happens rather than waited out.

It is not the report. The report is written at the end, restates everything the stream
said, and is the thing that gets filed; whoever reads it later never saw the stream at
all. So if deleting the stream would cost the report a fact, that fact is in the wrong
place.

## One line per sub-step, as it finishes

Each step names itself from its own heading in the leg file, so nothing else has to
know these lines exist:

```
Extensions 1/5 · sync state — 3 plugins, all synced within the day
Extensions 2/5 · skills earning loads — 7 skills, 2 funnels worth reporting
Extensions 3/5 · issues worth acting on — 11 open, 6 verified against the tree
```

What it looked at, and how many. A step that found nothing says so and moves on — "no
orphaned feedback" is a line, not a silence, for the same reason the report keeps a
Healthy section: a review that only speaks up about problems cannot be told apart from
one that only looked for them.

**It opens on its first step line.** Not on a sentence introducing itself —
"the checks are done, streaming what each found, then the report" spends a line saying
that lines are coming, which the lines then say better. The same rule the report keeps
about opening at its header, for the same reason.

## Name a step before it starts when it will take a while

Anchor verification reads the tree once per issue, and content drift walks the whole
corpus. Say what is starting, so a slow step is visibly working rather than
indistinguishable from a hang:

```
Content drift · walking 40 runbooks against the skills that own their subjects…
```

## A count is status, not a verdict

"Verify before alarming" governs the run and it governs this. A streamed count is what
the step found, before the report decides what survives. Never escalate in the stream,
never route in it, and never write a line the report will have to walk back.

## Carry step 1's answer forward

The extensions leg opens on sync because nothing downstream of a broken sync is
current. Where sync is broken, say so on that line and caveat the rest of the leg
rather than emitting confident counts underneath it:

```
Extensions 1/5 · sync state — ops failed to sync 6 days ago
Extensions 2/5 · skills earning loads — 7 skills, but this is the mounted version,
                 not what is in the repository now
```

## An unreadable step still gets its line

The same rule the report keeps: reported, not guessed. A step that could not run says
so where it would have reported, instead of going missing:

```
Connections 2/2 · query health — unreadable from this session, no incident.io
                  connection; the dashboard's Connections page has it
```

## What this depends on

These lines are the agent's own output to the user. They appear where the user reads
the agent directly, and they do not exist where mid-run text is never surfaced. That is
why the report never leans on them, and why the stream is a courtesy while the report
is the contract.
