# Writing examples

The skill decides constantly *whether* to use examples. This file covers what to
do once the answer is yes. A weak example set costs more than none, because the
model copies its flaws faithfully.

## What examples actually control

They fix form, not judgment. Format, structure, tone, level of detail, and the
shape of an edge case all transfer well. Reasoning quality does not: a model
that cannot do the task will produce confidently wrong answers in exactly your
format. When output is wrong rather than misshapen, the fix is elsewhere.

This is why they anchor open-ended creative and analytical work. If there is no
single right shape, showing three shapes narrows the space to those three, and
the fourth idea, the one worth having, never arrives.

## Coverage before count

Three well-chosen examples beat six variations of the same case. Cover the
dimensions along which real inputs differ, not the space of things you can
imagine.

The default set for anything with a checkable output:

1. **The normal case**, the one that occurs most often.
2. **An edge case**, drawn from the canonical four in `evaluation.md`: missing
   or irrelevant input, oversized input, hostile or off-topic input, genuine
   ambiguity.
3. **A failure case**, showing what to do when the task cannot be completed.
   This is the one people leave out, and it is the one that decides whether a
   tool failure gets reported as a finding.

Add a fourth and fifth only for a dimension the first three do not touch: a
second language, a much longer input, a different output branch.

**The counts elsewhere in this skill are a gradient over model class, not a
disagreement with the above.** Coverage decides the set; class decides how much
redundancy that set needs before it holds:

| Class | Count | Why |
|---|---|---|
| 1, internal reasoning | 2 to 5 | Generalises from few. More examples narrow the space it would otherwise explore usefully. |
| 2, no reasoning pass | 3 to 6 | Needs the pattern shown more than once to hold it across a long prompt. |
| 3, small and open-weight | 4 to 6 | Examples are the primary steering tool, not a supplement to the description. |

The three-case default is the floor in every row. On Class 1 it is often the
whole set; on Class 3 it is where you start. Never pad a set to reach a number:
a fourth example that covers nothing new teaches redundancy, which shows up as
repetitive output.

For classification, this changes: cover every class at least once, mix the
order so the model learns features rather than sequence, and include at least
one genuinely borderline item with the intended label. Borderline examples do
more work than clear ones, because the clear ones were never in doubt.

## Rules that decide whether the set works

**Identical structure across all examples.** Same fields, same order, same
punctuation, same length band. Any variation reads as permission to vary. If
one example has a trailing note and the others do not, expect the note to
appear at random.

**Show only the final output, not the reasoning behind it**, unless the
reasoning is itself part of the deliverable. On a reasoning model, worked
deliberation in an example invites it back into the response, which the
model-class rules forbid. On a non-reasoning model, put the reasoning in the
instruction, keep the examples clean, and separate the answer from the
derivation so it stays extractable.

**Use realistic content.** Placeholder names, round numbers, and `foo` teach
the model that vagueness is acceptable. Concrete content in the example
produces concrete content in the output.

**Make the last example the strongest.** Recency has a visible effect on which
pattern gets copied when they conflict. Put the case closest to the real
distribution last.

**Never contradict the instructions.** When an example and a rule disagree, the
example usually wins, and the rule becomes dead text that nobody notices is
dead. On revision, read the examples against the constraints line by line: this
is a common source of behaviour nobody can explain.

The same check applies between constraints, and that pair is easier to miss
because both halves read as authoritative. Before finalising, list every value
each field may take and every value the prompt calls an error, and look for a
value in both lists. A prompt that says "return `null` for a field you cannot
determine" two lines above "never leave a field unset, a null breaks the
downstream insert" has told the model to do the thing it forbids, and the model
will pick one of the two at random per run. Where a sentinel value is genuinely
needed, name a distinct one, such as an empty string or `"unknown"`, and say
which downstream consumer expects it.

## Placement

Wrap them in `<examples>` with each in `<example>`. Put them after the task and
constraints and before the variable input, so the input is the last thing the
model reads.

Where a prompt is long and examples are many, label each with what it
demonstrates ("edge case: empty field") rather than numbering them. The label
survives editing; the number does not.

## When to cut them instead

If the output format is fully specified by a schema or a strict tool, examples
of format are redundant; keep only those showing judgment calls the schema
cannot express. If the prompt has grown past its useful length, examples are
usually the cheapest thing to cut, because one positive example of the right
density often replaces three of them.
