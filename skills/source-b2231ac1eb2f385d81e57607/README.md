<div align="center">

# 🧹 断舍离.skill &nbsp;[![Tweet](https://img.shields.io/badge/share%20on-Twitter%2FX-000000?style=flat-square&logo=x)](https://twitter.com/intent/tweet?text=%E6%96%AD%E8%88%8D%E7%A6%BB.skill%20%E2%80%94%20%E7%AC%AC%E4%B8%80%E4%B8%AA%E5%8A%9D%E4%BD%A0%E5%88%A0%20skill%20%E7%9A%84%20skill%E3%80%82%E5%AE%A1%E8%AE%A1%E4%BD%A0%E8%A3%85%E7%9A%84%E5%85%A8%E9%83%A8%20skill%EF%BC%8C%E7%A7%BB%E9%99%A4%E6%A8%A1%E5%9E%8B%E5%B7%B2%E7%BB%8F%E4%BC%9A%E7%9A%84%E3%80%81harness%20%E5%B7%B2%E8%87%AA%E5%B8%A6%E7%9A%84%E3%80%81MCP%20%E5%B7%B2%E6%8E%A5%E7%AE%A1%E7%9A%84%EF%BC%8C%E6%AF%8F%E8%BD%AE%E7%9C%81%E4%B8%8B%E4%B8%8A%E5%8D%83%20token%E3%80%82&url=https%3A%2F%2Fgithub.com%2Fswaylq%2Fdanshari-skill&hashtags=ClaudeCode,AIAgent,%E6%96%AD%E8%88%8D%E7%A6%BBskill,%E5%BC%80%E6%BA%90)

### 审计你装的全部 skill，把模型已经会的、harness 已自带的、MCP 已接管的 —— **移除**

> *「你的模型一直在变强，你的 skill 还停在过去。」*

[![Website](https://img.shields.io/badge/%E5%AE%98%E7%BD%91-danshari--skill-1a1a1a)](https://swaylq.github.io/danshari-skill/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![skills.sh](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-any%20host-8A2BE2)](#-安装)

<br>

整个生态都在做加法 ——<br>
awesome 列表收录上千个 skill，单个仓库敢塞三百多个。<br>
**没人做减法。**

<br>

但 skill 不是免费的：<br>
每装一个，每一轮都在为它付出更多的 token；<br>
模型每变强一代，就有一批 skill 从增益变成拖累。

<br>

> **断舍离.skill 是一个劝你删掉 skill 的 skill ——**<br>
> **删的是「模型已经会的 skill」，留的是「模型还不知道的经验和流程」。**

<br>

[🌐 官网](https://swaylq.github.io/danshari-skill/) · [🚀 安装](#-安装) · [✨ 效果示例](#-效果示例) · [🧮 怎么判](#-怎么判) · [🔍 凭什么放心](#-凭什么放心) · [⭐ 演示审计](#-演示审计)

[**English README →**](README_en.md)

</div>

---

> 📊 &nbsp;**v0.1** — 完整审计流程（三分法 + 五问 + 盲测协议）+ 零依赖工具（`inventory.py` 盘点税表 / `archive.sh` 归档恢复，macOS 自带 bash 3.2 实测全过）+ 端到端[演示审计](examples/2026-08-17-demo/report.md)（12 个 skill → 5 个，描述税 **-66%**）。
>
> 🧭 &nbsp;**什么时候跑** — 换模型 / harness 大版本升级 / 新接 MCP / 距上次 90 天。**新模型发布日，就是 skill 断舍离日。**
>
> 🪞 &nbsp;**自我审判条款** — 断舍离自己每轮收你 ~180 token 的描述税（`inventory.py` 实测口径），得靠省下更多来挣回；若你的模型裸做审计已同样好，请把断舍离也断舍离。

---

## ✨ 效果示例

> 不是「删几个看着不顺眼的」。是对着你此刻的模型、harness、MCP，逐个过堂、拿证据判。

```
你      ❯ 换了新模型，帮我把 skill 断舍离一下

断舍离  ❯ 环境快照：claude-fable-5 · Claude Code（内建搜索 / 子 agent /
          自动记忆 / 计划模式）· MCP ×3（slack / github / playwright）

          盘点：12 个 skill，描述税 ~2,160 token/轮 —— 每一轮都在付。

          盲测 think-harder：不加载它，裸 agent 排查一个真实竞态 bug，
          质量持平 → 模型已内化，这 210 token/轮白付了。

          判决：✂️ 移除 ×6 · 🔧 修剪 ×1 · 🔗 合并 ×1 · ⏳ 缓刑 ×1 · ✅ 保留 ×2
          逐条依据在报告里 —— 确认执行？

你      ❯ 确认，但 browser-scrape 里的选择器脚本要留

断舍离  ❯ 收到：脚本先迁出到 scripts/，壳再归档。
          已归档 7 个（一键可恢复）、修剪 1 个（58 行 → 9 行）、合并 1 对。

          12 个 → 5 个，每轮省 ~1,425 token（-66%）。
          恢复：tools/archive.sh --restore <name>
```

完整报告（含每条判决的证据）：[examples/2026-08-17-demo/report.md](examples/2026-08-17-demo/report.md)

---

## 💸 skill 不是免费的

每装一个 skill，你在付三重成本：

| 成本 | 机制 |
|------|------|
| **token 税** | 它的名字 + 描述进**每一轮**的系统提示词，常驻支出 |
| **误触发** | 描述之间互相抢活，触发错一次比没有 skill 更糟 |
| **腐烂** | 里面的路径 / API / 模型名过期后，它触发一次就误导一次 |

而且 **skill 只增不减**：装的时候都有理由，删的契机永远不来。2023 年教模型分步思考是刚需，2024 年教它写 commit 是加分 —— 2026 年这些都是模型的本能，但没有人回头删。

---

## 🧮 怎么判

**三分法**定类型 —— 「模型越强 skill 越没用」只对第一类成立：

| 类型 | 定义 | 命运 |
|------|------|------|
| **能力型** | 教模型怎么想 / 怎么做的通用方法 | 模型升级会淘汰它 —— 审计重点 |
| **环境型** | 包装工具、补 harness 缺的功能 | harness 与 MCP 演进会取代它 |
| **知识型** | 私有事实：账号、路径、内部约定 | **永不因模型变强而过时**（红线保护） |

**五问**取证：① 模型已内化？② harness 已自带？③ MCP 已接管？④ 被吞并 / 重复？⑤ 已腐烂？

**盲测**复核死刑：能力型 skill 被判移除之前，先开一个**不加载它**的子 agent 裸做它最典型的任务 —— 裸做不逊色才准删。**证据，不是直觉。**

判决不止删留两档：

| 判决 | 含义 |
|------|------|
| ✂️ 移除 | 证据确凿 → 归档（可恢复），永不 rm |
| 🔧 修剪 | 混合型：删过时的说教，留值钱的事实，常见 200 行剪成 10 行 |
| 🔗 合并 | 触发词打架的重复者，并入较优者 |
| ⏳ 缓刑 | 证据不足不硬判，记为下次审计重点 |
| ✅ 保留 | 挣回了自己的 token 税 |

判据细则、典型与反例、边界案例：[references/rubric.md](references/rubric.md)。

---

## 🔍 凭什么放心

> 一个要动你 skill 目录的工具，安全设计就是它的全部信用。

- ✅ **永不 `rm`** — 一切移除都是挪进归档目录：`--restore` 一条命令恢复，MANIFEST 全程留痕
- ✅ **不确认不动手** — 判决表先给你过目，逐条可否决
- ✅ **红线保护知识型** — 私有事实、团队政策、被引用的脚本，证据再硬也不删
- ✅ **归档前搜身** — 过时 skill 正文里常埋着不过时的私有事实（URL / 账号 / 脚本），先迁出再归档
- ✅ **判决必须挂证据** — 盲测记录、指名道姓的替代者（哪个内建工具 / 哪个 MCP）、腐烂实证，嘴判无效

---

## ⚡ 安装

```bash
# Claude Code
git clone https://github.com/swaylq/danshari-skill.git ~/.claude/skills/danshari-skill
```

<details>
<summary><b>🛠️ 其他 host</b></summary>

<br>

```bash
git clone https://github.com/swaylq/danshari-skill.git <TARGET>
```

| Host | `<TARGET>` 路径 |
|------|-----------------|
| 🟣 Claude Code | `~/.claude/skills/danshari-skill` |
| 🔵 OpenClaw | `~/.openclaw/skills/danshari-skill` |
| ⚫ Codex | `~/.codex/skills/danshari-skill` |
| 🟠 Hermit | `~/.hermit/skills/danshari-skill` |

skill 装在非标准路径？审计时用 `tools/inventory.py --root <路径>` 指路。<br>
只想要方法论？把 `SKILL.md` + `references/rubric.md` 直接喂给你的 agent。

</details>

---

## 🚀 用法

装好断舍离.skill 的 agent 里，直接说：

```
> skill 断舍离                    # 全量审计
> 换了新模型，清理一下 skill        # 同上 —— 最经典的触发时机
> 审计一下项目里的 skill           # 只扫 ./.claude/skills
> 把 web-research 恢复回来        # 归档不是删除，随时反悔
```

两个工具也可以单独跑：

```bash
python3 tools/inventory.py                  # 盘点：谁在收多少税
bash tools/archive.sh <dir> --reason "…"    # 手动归档（挪走，不删）
bash tools/archive.sh --list                # 归档台账
bash tools/archive.sh --restore <name>      # 一键恢复
```

---

## ⭐ 演示审计

| 审计 | 内容 | 结果 |
|------|------|------|
| [2026-08-17-demo](examples/2026-08-17-demo/report.md) | 12 个典型「2024 年屯的」skill 在 2026 年模型上过堂，五种判决全部出现，每条挂证据 | 12 → 5 个，描述税 2,160 → 735 token/轮（**-66%**） |

> 里面能看到：盲测怎么记录、混合型怎么修剪（58 行 → 9 行）、归档前搜身搜出了什么、⏳ 缓刑欠了什么证据。

---

## 🔬 工作原理

```
0  环境快照   ← 模型 / harness 内建 / MCP —— 审计的基准是「现在的你」
1  盘点       ← inventory.py：每个 skill 的描述税、体积、最后改动
2  三分类     ← 能力型 / 环境型 / 知识型（红线）/ 混合型
3  五问审判   ← 模型已内化？harness 已自带？MCP 已接管？重复？腐烂？
4  盲测复核   ← 不加载该 skill 的子 agent 裸做典型任务 —— 死刑要证据
5  判决报告   ← ✂️ 移除 · 🔧 修剪 · 🔗 合并 · ⏳ 缓刑 · ✅ 保留，逐条挂依据
6  确认执行   ← 逐条可否决 → 搜身迁出私有事实 → archive.sh 归档（永不 rm）
7  前后对比   ← N 个 → M 个，每轮省多少 token；立下下次审计的触发条件
```

详见 [SKILL.md](SKILL.md)，判据看 [references/rubric.md](references/rubric.md)，报告结构看 [references/report-template.md](references/report-template.md)。

---

## 📂 项目结构

```
danshari-skill/
├── SKILL.md                    # 核心：三分法 + 五问 + 盲测 + 归档流程
├── references/
│   ├── rubric.md               # 判据细则：证据标准、典型与反例、边界案例三则
│   └── report-template.md      # 审计报告的固定结构（按标题定位）
├── tools/
│   ├── inventory.py            # 盘点 skill、粗估描述 token 税（纯标准库，零依赖）
│   └── archive.sh              # 归档 / 恢复 / MANIFEST 台账（永不 rm，bash 3.2 兼容）
└── examples/
    └── 2026-08-17-demo/        # 端到端演示审计：12 → 5，-66%
```

---

## 📄 路线图

| 版本 | 内容 | 状态 |
|------|------|:----:|
| v0.1 | 审计流程 + 盲测协议 + 归档工具 + 演示审计 | ✅ |
| v0.2 | 触发统计：扫会话记录，「90 天零触发」作为证据入判 | 🔲 |
| v0.3 | 触发词打架 linter：跨 skill 描述关键词冲突检测 | 🔲 |
| v0.4 | 换模型自动提醒：SessionStart hook 检测 model id 变化 | 🔲 |
| v0.5 | 插件与市场感知：审计范围覆盖 plugin / marketplace | 🔲 |

详见 [ROADMAP.md](ROADMAP.md)。

---

## 📜 许可证

MIT — 随便用，随便改，随便删。

<div align="center">

<br>

**整个生态都在做加法。断舍离.skill 做减法 —— 加法越繁荣，减法越必要。**<br>

<br>

*你的模型一直在变强。该有人劝你删点东西了。*

<br>

MIT License © [swaylq](https://github.com/swaylq) · 中文 README · [English](README_en.md)

</div>

---

## 🧪 关于作者

这个项目出自 **[Sway Lab](https://swaylab.ai)** — [Sway（刘乾）](https://github.com/swaylq)的 agent 实验室，
6 个 agent 在上面各自干活，产出产品、开源 skill 和实验。

- 📄 这个项目的来龙去脉：**[swaylab.ai/articles/danshari-skill](https://swaylab.ai/articles/danshari-skill)**
- 📰 《AI 动态日报》每天 09:30 更新：**[swaylab.ai/articles](https://swaylab.ai/articles)**
- 🕸️ 其他在做的东西：**[swaylab.ai/agent-network](https://swaylab.ai/agent-network)**

---

## ⭐ Star History

<a href="https://www.star-history.com/#swaylq/danshari-skill&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=swaylq/danshari-skill&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=swaylq/danshari-skill&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=swaylq/danshari-skill&type=Date" />
 </picture>
</a>
