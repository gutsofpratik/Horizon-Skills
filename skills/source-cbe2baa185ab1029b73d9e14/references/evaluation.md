# Evaluation

This file is the one place in this skill where a count is prescribed. That is
deliberate: "write some test cases" reliably produces three that all pass, and a
prompt that looks verified and is not.

## Success criteria

Specific, measurable, achievable, relevant. Push back on "accurate" and "high
quality" by asking what number, on what set, compared to what. Even soft
dimensions quantify: instead of "safe outputs", "fewer than 0.1 percent of
10,000 outputs flagged by the content filter".

Most real use cases need several criteria at once, because task fidelity,
consistency, tone, latency, and cost trade against each other. Naming the
trade-off is part of the deliverable.

## How many cases, and of what kind

Size the set to what the prompt does and how often it runs.

| Prompt runs | Set size | Composition |
|---|---|---|
| Once, in a chat | 3 | one typical, one canonical edge case, one that stresses the main constraint |
| Occasionally, by hand | 8 to 12 | the three above, plus one per input dimension that actually varies |
| At volume, unattended | 30 to 50 seed, expanded to a few hundred | see below |
| Classification at volume | at least 20 per class, plus borderline items | see below |

Three cases is a smoke test, not an eval. It catches a prompt that is broken; it
cannot tell you a prompt is 92 percent right, and it cannot tell you whether a
change made things worse.

**Building a large set from a small one.** Hand-write 20 to 30 cases that you
are certain about, covering every class and every edge you know. Those are the
seed. Then generate the bulk from them: vary phrasing, length, formality,
language, and noise, while keeping the expected answer fixed. Generated cases
inherit the seed's coverage, so a gap in the seed is a gap in all of it, which
is why the seed is written by hand and reviewed before anything is generated.
Hold back 20 percent that is never looked at during tuning, or you will tune the
prompt to the test.

**For classification specifically.** Cover every class, including the rare one
that only appears in two percent of traffic; that is usually the one that
matters. Include deliberately borderline items with the intended label attached,
because a set of unambiguous cases measures nothing you were worried about.
Report a confusion matrix, not an accuracy figure: 94 percent accuracy hides
that every refund request is being read as a complaint, and the matrix shows it
in one glance.

## Canonical edge cases

Derive cases from this list before inventing your own. These are the four that
break prompts in production:

- irrelevant or nonexistent input data
- input far longer than expected
- hostile, harmful, or off-topic input, for anything conversational
- cases genuinely ambiguous enough that two careful humans would disagree

For anything that enforces a rule, add a fifth: an input that tries to get
around the rule. A prompt or a generated script that enforces something is only
verified by a case that attempts the bypass and is expected to fail. A rule
tested only with compliant input is untested.

## Grading ladder

Use the fastest reliable method.

1. **Code-based**: exact match, string match, schema validation, banned-word
   lists, structural checks. Fast, free, deterministic. Most format and
   constraint requirements reduce to this if you design them to.
2. **LLM-based**: where judgment is required. Write an explicit rubric with a
   hard failure condition, force a categorical or 1-to-5 verdict rather than
   prose, and grade with a different model than the one that generated the
   output. Ask for the verdict plus one sentence of evidence pointing at the
   part of the output that decided it. Do not ask the grader to write out its
   reasoning first: on a model that reasons internally that is the
   reasoning-reproduction pattern, and current models can decline it.
3. **Human**: only where nothing else works.

Calibrate an LLM grader before trusting it: run it over 20 cases you have graded
yourself and check the agreement. A grader that agrees with you 70 percent of
the time is measuring itself, not the prompt.

A useful pattern at volume: run the code-based checks first and send only the
survivors to an LLM grader. It cuts cost sharply and narrows the grader's job,
which makes it more reliable.

## Seed-set example

A set for a support-ticket classifier, showing the shape rather than describing
it. Four of a 24-case seed:

    | # | input | expected | why it is in the set |
    |---|---|---|---|
    | 1 | "Package arrived smashed, want my money back" | refund | typical, unambiguous |
    | 2 | "This is the third time. Unacceptable." | complaint | no refund words, tests that the model reads intent not keywords |
    | 3 | "Do you ship to Austria?" + 4,000 words of quoted thread | question | oversized input, answer is in the first line |
    | 4 | "I'd like a refund on my time reading your docs" | complaint | contains the trigger word with the opposite intent, borderline by design |

Row 4 is the one that earns its place. A set without rows like it reports high
accuracy and tells you nothing.

## Iteration discipline

Establish a baseline before touching the prompt. Change one thing per
measurement. Re-run after each change.

Tuning a prompt against impressions instead of a baseline is how prompts
accumulate lines nobody can justify later, and it is the most common reason a
long-lived prompt becomes unmaintainable.

## Failure signature

Alongside the test cases, name in one line what a bad output will look like.
This is what lets someone recognise a regression months later without rereading
the prompt and reconstructing its intent. Good failure signatures are concrete:
"bullets that restate the headline at three levels of abstraction", not "output
quality drops".
