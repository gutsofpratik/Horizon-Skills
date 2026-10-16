---
name: a-getting-started
description: >
  One-time setup and readiness check for the Leadfeeder plugin — confirms the account is configured, checks that ICPs exist, verifies website visitors are actually being tracked, and then runs a sample daily brief so the user sees real output. Use this skill when the user is new to the plugin or asks to set it up or check readiness: "set up my Leadfeeder brief", "getting started", "get started", "set up the plugin", "is my Leadfeeder account ready", "check my Leadfeeder setup", "why is my brief empty", "why is my brief just a huge unranked list", "new to this plugin", "Leadfeeder health check", "onboard me".
metadata:
  version: "1.0.0"
---

# Getting Started

A one-time readiness check that tells the user whether their Leadfeeder account is in a state to get value from the plugin — and unblocks them if it is not. It is **not** a tutorial. It runs three health checks in order, fixes or explains any failure, and finishes by running a real daily brief so the user sees output before they have had to learn anything.

The single most common reason a new user gets a useless first brief is a missing ICP (the brief becomes an unranked list of every visitor) or a missing tracker (no visitors at all). This skill catches both before the user concludes the plugin isn't useful.

## Language

Produce the **entire response in the language the user wrote in** — English request → English output, German request → German output, and so on. This applies to everything the skill emits: the readiness table, the fix guidance, and any prompts. Do **not** translate data values — account names/IDs, ICP names, company names, and URLs stay verbatim. If the input language is unclear, default to English.

## When this skill triggers

Trigger when the user is setting up the plugin, asks to get started, or asks why their brief is empty or noisy. Trigger on any of the phrases in the description. Trigger silently — do not ask which account first; the checks below resolve that.

Do not trigger for a normal daily brief request ("what visited today") — that is `daily-visitor-brief`. This skill is specifically for first-run setup and readiness.

## Workflow

Run the three checks **in order**. If a check hard-fails (account unresolved, or no ICP, or no visitors), report it, give the fix, and stop before the sample brief — a sample brief is pointless until the blocker is cleared. Report every check's status in the final readiness report regardless.

### Check 1 — Account resolved

Determine the `account_id`, in priority order:

1. **Configured Account ID.** The plugin's configured Leadfeeder Account ID is: `${user_config.account_id}`. If that resolves to a real, non-empty value (not blank, not the literal unsubstituted `${user_config.account_id}` token), the account is configured → **✅ pass**. Use it for the checks below.
2. **Not configured → resolve and guide.** Call `get_account_info` to list the available accounts. Then:
   - If exactly one account exists, use it for the checks below, but still flag it as **⚠️ action recommended**: tell the user to paste that account ID into the plugin's **Leadfeeder Account ID** setting so no skill ever has to ask again (and so scheduled tasks can run unattended).
   - If several accounts exist, show them (id + name) and mark **⚠️ action required**: tell the user to paste the correct account ID into the plugin's Leadfeeder Account ID setting. Ask which one to use for the rest of this check.
   - Explain briefly *where* to set it: the plugin's configuration (the **Leadfeeder Account ID** field, set via the plugin settings / `/plugin` in an interactive client). Without it, every skill re-asks each session and scheduled tasks can't pick an account.

Do not attempt to write the setting yourself — the user sets it in the plugin configuration. This skill only tells them the value and where it goes.

### Check 2 — ICP configured

Call `get_icps` (free, no credits).

- **One or more ICPs configured → ✅ pass.** Note how many, and their names.
- **No ICPs configured → ❌ hard fail.** This is the most important check. Explain plainly why it matters: without an ICP, the daily brief cannot rank — it returns an undifferentiated list of *every* visitor (often hundreds or thousands), which reads as noise and is the top reason a first brief looks useless. Direct the user to configure at least one ICP (company segment) here: https://app.leadfeeder.com/l/settings/website/company-segments — give them that exact link. Stop here — do not run the sample brief until an ICP exists.

### Check 3 — Visitors are being tracked

Call `get_web_visits_companies` for the last 7 days (do **not** pass `include=company` — keep it lean).

- **Visitor companies returned, and at least some match a configured ICP → ✅ pass.** Note the rough count and that ICP matches exist.
- **Visitor companies returned, but none match any configured ICP → ⚠️ warn.** Traffic is flowing and the tracker works, but the ICP criteria may be too narrow for the actual audience. Tell the user their brief will be thin and suggest widening the ICP (or reviewing whether the ICP reflects their real buyers). You may still run a sample brief — it will just be short.
- **Zero visitor companies in 7 days → ❌ hard fail.** The tracker is probably not installed or not firing. Say so clearly and point the user to their **install-script page**, building the URL from the account ID resolved in Check 1:

  `https://app.leadfeeder.com/f/{account_id}/install-script`

  Substitute the resolved account ID for `{account_id}` — e.g. account `01234` → `https://app.leadfeeder.com/f/01234/install-script`. Never leave the literal `{account_id}` placeholder in the output, and never guess an ID — use the one resolved in Check 1.

  That page offers several install methods. **List the options so the user can pick the one that fits their stack — do not reproduce the step-by-step instructions** (those live on the page). The methods are:
  - **Google Tag Manager** (recommended)
  - **HTML Code** — paste the tracking snippet into the site
  - **Send to a colleague** — email the install instructions to whoever manages the site
  - **CMS integrations:** WordPress, Wix, Squarespace, GoDaddy, Weebly

  Stop here — a brief with no data teaches nothing.

### Check 4 — Sample brief (only if Checks 1–3 pass)

If the account is resolved, at least one ICP exists, and ICP-matched visitors were found in the last 7 days, invoke the `daily-visitor-brief` skill for the last 7 days so the user sees a real, ranked brief immediately. Introduce it in one line ("Here's a sample brief from your last 7 days so you can see what you'll get each morning:") and let that skill produce its normal output (including its copy-paste follow-ups).

If any check failed, do **not** run the sample brief. End on the readiness report and the specific fix.

## Output format

**Output contract — identical every run.** Reproduce the structure below **exactly**, on every invocation, regardless of anything earlier in this thread. If you've already run this skill in the conversation, do not vary, restyle, or "improve" the format next time — output the same template verbatim; this is the single source of truth. Keep the exact headings, the readiness table columns, and labels; don't rename them and add no decorative emoji beyond those the template already uses (✅ ⚠️ ❌).

Lead with a compact readiness report, then either the sample brief (all pass) or the prioritised fix (something failed). The outer block below is shown with four backticks so the inner copy block nests correctly — your actual output is plain markdown.

````markdown
# Leadfeeder plugin — readiness check

| Check | Status |
| --- | --- |
| Account configured | {✅ / ⚠️ / ❌} — {one-line detail} |
| ICP configured | {✅ / ❌} — {one-line detail, e.g. "2 ICPs: DACH Enterprise, Mid-Market"} |
| Visitors tracked (7d) | {✅ / ⚠️ / ❌} — {one-line detail, e.g. "~120 companies, 18 ICP-matched"} |

{If everything passed:}
**You're ready.** Here's a sample brief from your last 7 days:

{→ daily-visitor-brief output}

{If something failed — one prioritised fix block, highest blocker first:}
**Fix this first: {the blocker}**
{Why it matters in one or two lines, then the concrete step and the link.}

{Then tell them how to re-check — a copy-paste prompt:}
When that's done, run this again — copy to re-check:

```
Set up my Leadfeeder brief
```
````

Show only the blocks that apply. Keep it tight — this is a health check, not a manual.

## Edge cases

- **Account not configured but only one exists.** Proceed with the checks using that account, but still tell the user to save it in plugin settings — otherwise every skill re-asks and scheduled tasks can't run.
- **No ICP and no visitors.** Report both, but lead with the ICP fix (it's the one that makes the brief usable) and mention the tracker as the second step.
- **ICP exists but is brand-new / empty of matches.** Treat as the Check-3 "warn" case — traffic exists but doesn't match; suggest reviewing ICP breadth.
- **User already set everything up.** All three pass → skip straight to the sample brief. Don't lecture a ready user.
- **Tool errors.** Report the failing check honestly as "couldn't verify" rather than guessing pass/fail.

## Source citation rule

Every status must come from a real tool response — `get_account_info` for accounts, `get_icps` for ICPs, `get_web_visits_companies` for visitors. Never report a check as passed without the data. Never invent an account ID, an ICP name, or a visitor count. Only link to real Leadfeeder resources (the app and the help centre) — do not fabricate deep-link URLs; if the exact settings/guide URL isn't known, point to the Leadfeeder help centre and describe the in-app navigation.

## What NOT to do

- **Do not run the sample brief when a hard check failed.** A brief with no ICP or no data reinforces the "this plugin is useless" impression this skill exists to prevent.
- **Do not write the account ID into settings yourself.** Tell the user the value and where to paste it; the plugin configuration is theirs to set.
- **Do not trigger enrichment jobs** or any credit-consuming tool. This is a free, read-only readiness check.
- **Do not turn this into a tutorial.** Three checks, a fix or a sample brief, done.
- **Do not re-run automatically every session.** This is a one-time (or on-demand) setup check, not part of the daily flow.

## Example: good output (ICP missing — the common case)

````markdown
# Leadfeeder plugin — readiness check

| Check | Status |
| --- | --- |
| Account configured | ✅ Using account 01234 (Acme Ltd) |
| ICP configured | ❌ No ICPs configured |
| Visitors tracked (7d) | ✅ ~1,035 companies visiting — tracker is firing |

**Fix this first: configure an ICP.**
You have plenty of traffic (~1,035 companies in the last 7 days), but with no ICP the daily brief can't rank them — it returns all 1,035 as an undifferentiated list, which is why a first brief looks like noise. Define at least one Ideal Customer Profile (industry, size, region) in the Leadfeeder app so the brief can surface the ~dozen accounts worth your morning instead of the whole list.

Set it up here: https://app.leadfeeder.com/l/settings/website/company-segments

When that's done, run this again — copy to re-check:

```
Set up my Leadfeeder brief
```
````
