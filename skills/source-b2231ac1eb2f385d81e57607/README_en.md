<div align="center">

# 🧹 danshari.skill &nbsp;[![Tweet](https://img.shields.io/badge/share%20on-Twitter%2FX-000000?style=flat-square&logo=x)](https://twitter.com/intent/tweet?text=danshari.skill%20%E2%80%94%20the%20first%20skill%20that%20tells%20you%20to%20delete%20skills.%20Audit%20installed%20skills%2C%20remove%20what%20your%20model%20already%20does%20natively%2C%20save%20thousands%20of%20tokens%20per%20turn.&url=https%3A%2F%2Fgithub.com%2Fswaylq%2Fdanshari-skill&hashtags=ClaudeCode,AIAgent,ClaudeSkills,OpenSource)

### Audit every skill you've installed — remove what the model already knows, the harness already ships, and MCP already covers

> *"Your model keeps getting stronger. Your skills are still stuck in 2024."*

[![Website](https://img.shields.io/badge/website-danshari--skill-1a1a1a)](https://swaylq.github.io/danshari-skill/en/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![skills.sh](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-any%20host-8A2BE2)](#-install)

<br>

The whole ecosystem plays addition —<br>
awesome lists index thousands of skills, single repos ship 300+.<br>
**Nobody plays subtraction.**

<br>

But skills are not free:<br>
every installed one charges its token tax on every single turn,<br>
and each model generation turns another batch from asset into liability.

<br>

> **danshari.skill is the first skill that tells you to delete skills —**<br>
> **delete what teaches the model things it already knows; keep what tells it things it cannot possibly know.**

<br>

[🌐 Website](https://swaylq.github.io/danshari-skill/en/) · [🚀 Install](#-install) · [✨ Demo](#-demo) · [🧮 How it judges](#-how-it-judges) · [🔍 Why it's safe](#-why-its-safe) · [⭐ Demo audit](#-demo-audit)

[**中文 README →**](README.md)

*"Danshari" (断舍离) is the Japanese decluttering philosophy: refuse, dispose, detach.*

</div>

---

> 📊 &nbsp;**v0.1** — full audit flow (3-way split + 5 questions + blind-test protocol) + zero-dependency tools (`inventory.py` tax ledger / `archive.sh` archive & restore, tested on stock macOS bash 3.2) + an end-to-end [demo audit](examples/2026-08-17-demo/report.md) (12 skills → 5, description tax **-66%**).
>
> 🧭 &nbsp;**When to run it** — model upgrade / major harness release / new MCP server / 90 days since last audit. **Every model release day is declutter day.**
>
> 🪞 &nbsp;**The self-judgment clause** — danshari itself charges ~180 tokens/turn of description tax (measured by its own `inventory.py`) and must earn that back; if your model declutters just as well bare, danshari the danshari.

---

## ✨ Demo

> Not "delete a few that look useless." Every skill stands trial against your current model, harness, and MCP — with evidence.

```
you      ❯ Just upgraded my model — declutter my skills

danshari ❯ Environment: claude-fable-5 · Claude Code (built-in search / subagents /
           auto memory / plan mode) · 3 MCP servers (slack / github / playwright)

           Inventory: 12 skills, description tax ~2,160 tokens/turn — paid every turn.

           Blind test think-harder: a bare subagent (skill unloaded) debugs a real
           race condition at equal quality → internalized. Those 210 tokens/turn buy nothing.

           Verdicts: ✂️ remove ×6 · 🔧 trim ×1 · 🔗 merge ×1 · ⏳ probation ×1 · ✅ keep ×2
           Per-verdict evidence in the report — confirm?

you      ❯ Confirmed, but keep the selector scripts inside browser-scrape

danshari ❯ Done: scripts migrated to scripts/ first, then the husk archived.
           Archived 7 (one-command restore), trimmed 1 (58 lines → 9), merged 1 pair.

           12 → 5 skills, ~1,425 tokens saved per turn (-66%).
           Restore anytime: tools/archive.sh --restore <name>
```

Full report with per-verdict evidence: [examples/2026-08-17-demo/report.md](examples/2026-08-17-demo/report.md)

---

## 💸 Skills are not free

Every installed skill charges you three ways:

| Cost | Mechanism |
|------|-----------|
| **Token tax** | Its name + description enter the system prompt of **every turn** |
| **Misfires** | Descriptions compete for triggers; a wrong fire is worse than no skill |
| **Rot** | Stale paths / APIs / model names mislead the agent every time it fires |

And **skill rosters only ever grow**: there's always a reason to install, never a moment to delete. Teaching models step-by-step thinking was essential in 2023, teaching commit style was nice in 2024 — by 2026 these are instincts, yet nobody went back to delete.

---

## 🧮 How it judges

**The three-way split** — "stronger model, useless skill" is only true for the first type:

| Type | Definition | Fate |
|------|------------|------|
| **Capability** | Teaches generic how-to-think / how-to-do | Model upgrades obsolete it — the audit focus |
| **Environment** | Wraps a tool, patches a missing harness feature | Harness & MCP evolution replace it |
| **Knowledge** | Private facts: accounts, paths, team conventions | **Never obsoleted by stronger models** (red-line protected) |

**The five questions**: ① internalized by the model? ② built into the harness? ③ taken over by MCP? ④ duplicated / absorbed? ⑤ rotten?

**The blind test** reviews every death sentence: before a capability skill gets removed, a subagent that does **not** load it performs the skill's most typical task bare — only equal-or-better bare performance confirms removal. **Evidence, not vibes.**

More than keep-or-delete:

| Verdict | Meaning |
|---------|---------|
| ✂️ Remove | Evidence conclusive → archived (restorable), never `rm` |
| 🔧 Trim | Mixed skill: delete the obsolete teaching, keep the valuable facts — 200 lines become 10 |
| 🔗 Merge | Trigger-colliding duplicates folded into the better one |
| ⏳ Probation | Insufficient evidence — no verdict without proof; flagged for next audit |
| ✅ Keep | Earns its token tax |

Full rubric with evidence standards, counter-cases, and borderline case studies: [references/rubric.md](references/rubric.md).

---

## 🔍 Why it's safe

> A tool that touches your skills directory lives or dies by its safety design.

- ✅ **Never `rm`** — removal means moving into an archive dir; `--restore` brings anything back; a MANIFEST records everything
- ✅ **Nothing moves without confirmation** — the verdict table goes to you first, veto line by line
- ✅ **Red lines protect knowledge skills** — private facts, team policy, referenced scripts survive any evidence
- ✅ **Frisk before archiving** — obsolete skills often bury still-valuable private facts (URLs / accounts / scripts); they're migrated out first
- ✅ **Every verdict carries evidence** — a blind-test record, the named replacement (which built-in tool, which MCP), or proof of rot; vibes don't convict

---

## ⚡ Install

```bash
# Claude Code
git clone https://github.com/swaylq/danshari-skill.git ~/.claude/skills/danshari-skill
```

<details>
<summary><b>🛠️ Other hosts</b></summary>

<br>

```bash
git clone https://github.com/swaylq/danshari-skill.git <TARGET>
```

| Host | `<TARGET>` path |
|------|-----------------|
| 🟣 Claude Code | `~/.claude/skills/danshari-skill` |
| 🔵 OpenClaw | `~/.openclaw/skills/danshari-skill` |
| ⚫ Codex | `~/.codex/skills/danshari-skill` |
| 🟠 Hermit | `~/.hermit/skills/danshari-skill` |

Skills in non-standard paths? Point the audit with `tools/inventory.py --root <path>`.<br>
Methodology only? Feed `SKILL.md` + `references/rubric.md` straight to your agent.

</details>

---

## 🚀 Usage

In an agent with danshari.skill installed, just say:

```
> declutter my skills               # full audit
> new model — clean up my skills    # same, the classic trigger moment
> audit the project skills          # scan ./.claude/skills only
> bring web-research back           # archiving isn't deleting; change your mind anytime
```

Both tools also run standalone:

```bash
python3 tools/inventory.py                  # who charges how much tax
bash tools/archive.sh <dir> --reason "…"    # archive by hand (move, never delete)
bash tools/archive.sh --list                # the archive ledger
bash tools/archive.sh --restore <name>      # one-command restore
```

---

## ⭐ Demo audit

| Audit | Content | Result |
|-------|---------|--------|
| [2026-08-17-demo](examples/2026-08-17-demo/report.md) | 12 typical "hoarded in 2024" skills on trial against a 2026 model — all five verdicts appear, each with evidence | 12 → 5 skills, tax 2,160 → 735 tokens/turn (**-66%**) |

> Inside: how a blind test is recorded, how a mixed skill gets trimmed (58 → 9 lines), what the pre-archive frisk found, and what evidence probation still owes.

---

## 🔬 How it works

```
0  Snapshot     ← model / harness built-ins / MCP — the baseline is who you are NOW
1  Inventory    ← inventory.py: each skill's description tax, size, last touched
2  Classify     ← capability / environment / knowledge (red line) / mixed
3  Five questions ← internalized? built-in? MCP-covered? duplicated? rotten?
4  Blind test   ← bare subagent, skill unloaded — death sentences need evidence
5  Verdicts     ← ✂️ remove · 🔧 trim · 🔗 merge · ⏳ probation · ✅ keep, each with grounds
6  Confirm & act ← veto line by line → frisk out private facts → archive.sh (never rm)
7  Before/after ← N → M skills, tokens saved per turn; set the next audit trigger
```

Details in [SKILL.md](SKILL.md), evidence standards in [references/rubric.md](references/rubric.md), report structure in [references/report-template.md](references/report-template.md).

---

## 📂 Structure

```
danshari-skill/
├── SKILL.md                    # core: 3-way split + 5 questions + blind test + archive flow
├── references/
│   ├── rubric.md               # evidence standards, counter-cases, 3 borderline case studies
│   └── report-template.md      # fixed audit-report structure (located by headers)
├── tools/
│   ├── inventory.py            # scan skills, estimate description token tax (stdlib only)
│   └── archive.sh              # archive / restore / MANIFEST ledger (never rm, bash 3.2 ok)
└── examples/
    └── 2026-08-17-demo/        # end-to-end demo audit: 12 → 5, -66%
```

---

## 📄 Roadmap

| Version | Content | Status |
|---------|---------|:------:|
| v0.1 | Audit flow + blind-test protocol + archive tooling + demo audit | ✅ |
| v0.2 | Usage stats: scan session logs, "0 fires in 90 days" as evidence | 🔲 |
| v0.3 | Trigger-collision linter across skill descriptions | 🔲 |
| v0.4 | Model-change reminder via SessionStart hook | 🔲 |
| v0.5 | Plugin & marketplace awareness | 🔲 |

See [ROADMAP.md](ROADMAP.md).

---

## 📜 License

MIT — use it, fork it, delete with it.

<div align="center">

<br>

**The whole ecosystem plays addition. danshari.skill plays subtraction — the more addition thrives, the more subtraction matters.**<br>

<br>

*Your model keeps getting stronger. Someone should finally tell you to delete things.*

<br>

MIT License © [swaylq](https://github.com/swaylq) · English README · [中文](README.md)

</div>

---

## 🧪 About the author

Built at **[Sway Lab](https://swaylab.ai)** — the agent laboratory of
[Sway (Liu Qian)](https://github.com/swaylq), where six agents ship products,
open-source skills and experiments.

- 📄 How this project came about: **[swaylab.ai/articles/danshari-skill](https://swaylab.ai/articles/danshari-skill)** (Chinese)
- 📰 A daily AI briefing, published 09:30 CST: **[swaylab.ai/articles](https://swaylab.ai/articles)** (Chinese)
- 🕸️ Everything else: **[swaylab.ai/agent-network](https://swaylab.ai/agent-network)**

---

## ⭐ Star History

<a href="https://www.star-history.com/#swaylq/danshari-skill&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=swaylq/danshari-skill&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=swaylq/danshari-skill&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=swaylq/danshari-skill&type=Date" />
 </picture>
</a>
