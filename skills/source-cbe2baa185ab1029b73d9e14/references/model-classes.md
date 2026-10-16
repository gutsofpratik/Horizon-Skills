# Model classes

Classify by capability signature, not by model name. This file deliberately
names no models, because names go stale within months while the signatures do
not. Between two revisions of it, one vendor shipped a new flagship and renamed
the tier below it; a list of examples would already have been wrong.

To classify a target you have not met: run a short task that separates the
classes rather than looking the model up. Give it a goal with success criteria
and no steps. A Class 1 model plans its own approach and asks about the goal; a
Class 2 model asks what the steps are or invents a rigid procedure; a Class 3
model produces something shaped like the request but wrong in a way the request
did not describe. That test survives every rename.

## Class is model times effort setting

Reasoning models expose an effort or reasoning-level knob, and at the bottom of
that range they stop behaving like reasoning models. A frontier model pinned to
its lowest setting wants Class 2 prompting: explicit steps, told how rather than
what. On some current models thinking cannot be switched off at all, and the
lowest setting still reasons between tool calls; prompt it as Class 2 and verify
rather than assume.

Defaults differ between generations and even between point releases of the same
model line, and vendors recalibrate what each effort label means from one
version to the next. A setting therefore does not transfer: "high" on the new
version is not "high" on the old one. Treat an unpinned effort setting as an
unknown class and say so, and after any model change re-sweep the setting rather
than carrying it over. Where the target exposes
effort, recommend a level alongside the prompt: high or above for
intelligence-sensitive and agentic work, lower for latency-bound and mechanical
tasks, with the caveat that the top of the range can tip into overthinking.

The core trade-off: reasoning models perform best with high-level guidance, like
a senior colleague given the goal and trusted with the details. Non-reasoning and
small models perform best with explicit, precise instructions, like a junior
colleague told exactly how to produce the output.

## Class 1: internal-reasoning frontier models at meaningful effort

Signature: runs a reasoning pass before answering, follows goal-level
instructions without step decomposition, and output quality *drops* when the task
is decomposed for it.

- Goal plus success criteria plus constraints. Avoid step-by-step
  micromanagement unless the steps are domain requirements.
- Never instruct the model to reproduce or explain its internal reasoning in the
  response ("think step by step in thinking tags", "show your reasoning"). These
  models reason internally on their own; such instructions add nothing, and
  current models can decline them outright, since at least one vendor lists
  requests to reproduce internal reasoning as their own refusal category. If
  reasoning structure is needed in the
  *output*, as a rubric, a hypothesis log, or a decision record, frame it as an
  output artifact and say so.
- Do not feed a model's own extended thinking back to it in a later user turn. It
  does not improve performance and tends to degrade results.
- These models calibrate length to perceived task complexity rather than to a
  fixed verbosity, so output length varies more than it used to. If the product
  depends on a length profile, constrain it, and prefer a positive example of the
  right density over a list of things not to do.

## Class 2: no effective reasoning pass

Signature: no internal reasoning pass, either because the model has none or
because effort is pinned to its lowest setting. Strong instruction following.
Benefits from being told how, not just what.

- Precise, explicit instructions. Numbered steps for multi-part work.
- Explicit chain-of-thought instructions now help: work through the problem step
  by step, then give the final answer after a clear separator, with the answer
  after the reasoning and extractable from it. A brief summary of the approach at
  the start of the final answer also helps on harder tasks.
- 3 to 6 diverse few-shot examples, covering the normal case, an edge case, and
  a failure case. The counts across classes are one gradient; `examples.md` has
  the table and the rules for what the set must cover.
- Every prohibition needs a positive counterpart: instead of X, do Y.
- Tighter output format specs, less reliance on judgment.

## Class 3: small and open-weight models

Signature: loses instructions in long context, ignores negations, needs the shape
of the answer shown rather than described.

- Maximum explicitness: simple direct language, short sentences, one instruction
  per line, no implied context.
- Few-shot examples are the primary steering tool, 4 to 6, diverse, with classes
  mixed for classification tasks so the model learns features rather than order.
- Rigid output formats. State what to do, not what to avoid.
- Narrow scope: one job, one output shape, hard limits on length and count.
- Keep prompts short overall.

These recommendations are the least well-sourced of the three classes. Treat them
as a starting point and lean harder on evals here than elsewhere.

## If the target cannot be classified

Write for Class 1 and list the two or three lines to add for Class 2 or 3. Class 1
prompts degrade more gracefully on other classes than the reverse.

## Choosing a class, when that is still open

Pick the smallest class that does the job reliably.

- Mechanical, narrow, verifiable work such as search, extraction, or formatting
  goes to Class 3.
- Judgment inside a known frame, such as review against a spec, tests, or
  documentation, goes to Class 2.
- Open, ambiguous, or architectural work such as design, debugging of unknown
  causes, or prompt design itself goes to Class 1.

Output from the smaller classes needs a review pass. Count that cost before
downgrading; it often erases the saving.

## Provider-level formatting

- Claude: XML tags for section delineation work best.
- OpenAI: Markdown headers are the documented convention, with XML for inline
  content like examples. Context usually sits best near the end.
- Gemini and open-weight models: either convention works. Prefer Markdown headers
  plus explicit delimiters around variable input.
- Cross-provider templates: keep conventions consistent within one prompt and
  state that it must be re-tested per model. Identical prompts produce different
  results across providers, and across snapshots of the same model.
