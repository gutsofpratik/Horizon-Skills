# Action / Tool Descriptions — Authoring Rules

In Synthflow, every action, transfer, or knowledge base has a UI description. **The model uses this description to decide whether to call the tool.** Treat it with the same care as the prompt itself.

## Prompt and description must agree

Tool-call instructions in the prompt and the action's UI description **must agree**. If they conflict, the agent will pick one inconsistently — sometimes the prompt, sometimes the description, depending on the turn.

**Rule of thumb:** keep operational detail (when to call, what arguments to pass, what the tool does) in the **UI action description**. In the prompt, reference the tool by name and the user-facing intent only.

- ❌ Prompt: "transfer to billing for any payment question" + description: "transfer to billing for refund or chargeback questions only" → ambiguity.
- ✅ Prompt: "If the caller has a billing question, use the `transfer_to_billing` tool." Description does the rest.

## How to write a good action description

Drawn from OpenAI's function-calling guidance:

1. **Be specific, not generic.** Say *what* the tool does and *when* to call it; disambiguate from other tools.
   - ❌ "Search the knowledge base."
   - ✅ "Search the store knowledge base for product specs, hours, or warranty terms. Use this when the caller asks about an in-store product or store policy. Do not use for inventory or pricing — use `check_inventory` instead."
2. **Lead with the trigger, then the action:** "Use this when X. It does Y."
3. **Name the tool obviously:** verb + object. `transfer_to_billing` beats `handle_customer`.
4. **State arguments and valid values.** Prefer enums: "`reason`: one of `refund`, `chargeback`, `dispute`" beats free text.
5. **Disambiguate siblings explicitly.** With `book_appointment` and `reschedule_appointment`, each description should say "do not use this for [the other case]."
6. **Keep the tool count low** (≤ 20; OpenAI envelope ≤100 tools, ≤20 args/tool).
7. **No prompt-style tone or filler.** "Please use this carefully" adds no signal — cut it.
8. **The "another human" test applies here too.** If a teammate can't read the description and tell you when the tool should fire, the model can't either.

## References

- OpenAI — Function calling guide: https://developers.openai.com/api/docs/guides/function-calling
- OpenAI Community — Prompting best practices for tool use: https://community.openai.com/t/prompting-best-practices-for-tool-use-function-calling/1123036
- OpenAI Cookbook — o-series function calling guide: https://cookbook.openai.com/examples/o-series/o3o4-mini_prompting_guide
