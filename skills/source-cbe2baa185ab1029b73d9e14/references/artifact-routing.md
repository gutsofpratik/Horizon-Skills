# Artifact routing

## What the table in SKILL.md does not say

The decision table is in `SKILL.md`, because routing happens before anything
else and must be in the always-loaded core. This file holds only what does not
fit there.

**Why a hook is not just a firmer config line.** Hooks run at defined points in
the agent's lifecycle regardless of what the model concludes. Instructions in a
config file are advisory, and a capable model may reasonably decide against them
in a case the author did not foresee. That is usually a feature. It stops being
one the moment the rule is a guarantee someone else depends on, and a rule that
holds most of the time is worse than either alternative, because it looks
reliable.

**Why a skill's description is the whole mechanism.** Selection happens on the
description alone, before the body is ever read. It has to say what the skill
does *and* when to use it, in the words the user will actually type. A
description that only describes function under-triggers, and an under-triggering
skill is indistinguishable from a missing one: nothing errors, the work just
gets done without it.

**Why a subagent's value is the context boundary.** Its own window and tool set
are the point, not an implementation detail. A reviewer that inherits your
context inherits your blind spots, so delegating review to one is delegating
nothing.

## Two signals the user asked for the wrong artifact

They describe a rule using "always" or "never" and want it in a config file. That
is a hook. Advisory text cannot deliver an absolute guarantee, and writing it as
if it could produces a rule that holds most of the time, which is worse than
either alternative because it looks reliable.

They ask for a prompt they clearly intend to paste again next week. That is a
skill. Writing it as a prompt guarantees it drifts across copies, and the copies
diverge silently.

## Token economy does not transfer

When the right artifact is a skill, subagent, hook, or config file, the
minimalism that governs prompt writing does not apply, and applying it does
damage.

Skills use progressive disclosure: the metadata is always loaded, the body loads
when the skill triggers, and bundled reference files load only when read. That
means the description must be dense and the body can be generous. Cutting a
skill body for brevity trades away detail that costs nothing until it is needed.

Config files are the opposite: always loaded, so every line is a permanent cost
and brevity genuinely matters.

Say which regime applies rather than writing one artifact in the shape of
another.
