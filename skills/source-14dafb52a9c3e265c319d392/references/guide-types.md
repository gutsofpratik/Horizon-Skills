# Pendo Guide Types — Reference

Full definitions, structural rules, use cases, and copy guidelines for each guide type.

---

## WALKTHROUGH
A product walkthrough (also called a product tour) is a multi-step guide designed to onboard users by
introducing them to key features, workflows, or value propositions. It consists of sequential tooltips,
modals, or highlights that guide the user through completing tasks or understanding important functionality.

**When to use:**
- Onboarding new users to key workflows
- Introducing a feature that requires multiple steps to understand
- Guiding users to their "aha moment"
- Feature sunset: show replacement feature after deprecation notice

**Key characteristics:**
- Triggered automatically for new users or after major updates
- Sequential and linear
- Designed to reduce time to value and improve adoption
- Uses progressive disclosure — don't overwhelm upfront
- Each step builds upon the previous one
- Fewer steps is better — don't use 10 when 5 are equally effective

**Step structure:**

| Step Position | Label | Buttons | Notes |
|---|---|---|---|
| First step | "Subtitle" label at top | Secondary + Primary | Introductory; sets context |
| Middle steps | "Step X of Y" progress indicator | Back + Next | Focused on specific action or info |
| Last step | None | Primary only (Finish/Done) | Concludes; no secondary button |

**Copy length:** Concise per step. Each step should focus on one idea.

---

## ANNOUNCEMENT
A one-step in-app modal used to communicate important updates, product changes, promotions, or timely
information. Best for introducing new features while users are already in the product — instant engagement
without the friction of email.

**When to use:**
- New feature releases
- Promotions or campaigns
- Policy updates
- Maintenance notices (non-critical)
- Encouraging exploration of underutilized features

**Key characteristics:**
- Always single-step. If user requests multiple steps → suggest Walkthrough.
- Shows "Announcement" label at top
- Has both Secondary and Primary buttons
- Focused on value and benefits, not instructions
- Should generate excitement and curiosity

**Copy length:** 1 paragraph. Punchy, benefit-led. No walls of text.

---

## ALERT
A high-priority, interruptive in-app guide used to immediately notify users of critical information or
required actions. More urgent than an announcement — often demands acknowledgment before the user can proceed.

**When to use:**
- Critical system events (outages, data loss risk)
- Required legal or compliance acknowledgments
- Urgent security notices
- Blocking errors that require user action

**Key characteristics:**
- Interruptive by design — modal or banner that blocks interaction
- Used sparingly to avoid alert fatigue
- Often requires acknowledgment to dismiss
- Tone: direct, clear, no fluff

**Copy length:** 1–3 sentences. State the issue and the required action immediately.

---

## POLL
An interactive in-app guide used to collect user feedback directly within the product experience.
Includes a question or short set of questions with multiple-choice or open-text responses.

**When to use:**
- NPS surveys
- Feature satisfaction feedback
- Post-interaction research prompts
- Roadmap prioritization input
- Contextual feedback after a feature is used

**Key characteristics:**
- Interactive — users respond to questions
- Can be shown contextually (e.g., after a user completes a workflow)
- Responses inform product decisions and roadmap priorities
- Can be multi-question but keep it short (1–3 questions max)

**Copy length:** 1 concise question per step. Answer options should be short labels.

---

## PROMOTION
An in-app message used to highlight a product, feature, event, or offer. Designed to drive awareness
and adoption with a clear call to action.

**When to use:**
- Promoting new or underutilized features
- Events, webinars, or launches
- Pricing plan awareness
- Campaign touchpoints

**Key characteristics:**
- Visually engaging with clear CTAs
- Can be targeted by behavior, role, or plan
- May be part of a multi-touchpoint campaign
- CTAs: "Try now", "Learn more", "Register", "See what's new"

**Copy length:** Short headline + 1–2 sentences of supporting copy. Lead with value.

---

## CROSS-SELL / UPSELL
An in-app message designed to promote additional products, features, or plans — encouraging users to
expand usage or upgrade. A specialized promotion with a revenue focus.

**When to use:**
- User hits a usage limit
- User explores a gated/premium feature
- User's behavior suggests readiness to upgrade
- Targeted by role, usage pattern, or account type

**Key characteristics:**
- Strategically placed at moments of natural upgrade consideration
- Persuasive but not pushy — lead with value, not price
- Clear CTAs: "Upgrade now", "Add this to your plan", "See plans", "Talk to sales"
- Can include comparison charts or benefit lists
- Often targeted at admins or decision-makers, not end users

**Copy length:** Short headline + 2–3 bullet benefits + CTA. Avoid pricing walls of text.

---

## Copy Length Quick Reference

| Guide Type        | Max Copy Length                          |
|-------------------|------------------------------------------|
| Walkthrough step  | 2–4 sentences per step                   |
| Announcement      | 1 paragraph (4 lines max)                |
| Alert             | 1–3 sentences                            |
| Poll              | 1 question per step; options as labels   |
| Promotion         | Headline + 1–2 sentences                 |
| Cross-sell/Upsell | Headline + 2–3 bullets + CTA            |
| Tooltip           | ~2 lines                                 |
| Banner            | 1–2 sentences                            |

---

## Guide Type Selection Helper

Use this when the user isn't sure which type to recommend:

| User goal | Recommended type |
|---|---|
| Onboard new users step by step | Walkthrough |
| Announce a new feature | Announcement |
| Notify of urgent system issue | Alert |
| Collect in-product feedback | Poll |
| Promote an event or campaign | Promotion |
| Encourage a plan upgrade | Cross-sell/Upsell |
| Provide contextual UI hint | Tooltip (via Walkthrough step) |
| Non-blocking persistent notice | Banner (via Alert or Announcement) |
