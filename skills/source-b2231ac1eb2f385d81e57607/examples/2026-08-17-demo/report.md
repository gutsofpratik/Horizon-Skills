# Skill 断舍离审计报告

- 日期：2026-08-17
- 环境：**演示**（脱敏后的典型场景：一位从 2024 年开始屯 skill 的用户，刚升级到 2026 年的模型。token 数为 `tools/inventory.py` 粗估口径。）

## 环境快照

- **模型**：claude-fable-5（知识截止 2026-01）
- **harness**：Claude Code 2.x，内建：WebSearch / WebFetch、子 agent（Task）、计划模式、自动记忆、schedule 定时、内建代码评审命令
- **MCP**：slack-mcp（发消息 / 查频道）、github-mcp（PR / issue / API）、playwright-mcp（浏览器自动化）
- **skill 根**：`~/.claude/skills`（个人 ×9）、`./.claude/skills`（项目 ×3）

## 总账

- 盘点：**12 个 skill**，描述税合计 **~2,160 token/轮**
- 判决分布：✂️ 移除 ×6 · 🔧 修剪 ×1 · 🔗 合并 ×1（一对）· ⏳ 缓刑 ×1 · ✅ 保留 ×2
- 执行后：**5 个 skill**，描述税 **~735 token/轮**（省 ~1,425，**-66%**）

## 判决表

| skill | 来源 | 分类 | 描述税 | 判决 | 一句话依据 |
|---|---|---|---:|:-:|---|
| browser-scrape-cookbook | 个人 | 环境 | 310 | ✂️ | playwright-mcp 已接管（问 3），脚本先迁出 |
| company-onboarding | 项目 | 知识 | 260 | ✅ | 内部系统与流程事实，模型不可能知道 |
| web-research | 个人 | 环境 | 240 | ✂️ | 内建 WebSearch/WebFetch 已覆盖（问 2） |
| think-harder | 个人 | 能力 | 210 | ✂️ | 盲测通过：裸做质量持平（问 1） |
| code-review-checklist | 个人 | 能力 | 190 | ✂️ | 盲测通过 + 内建评审命令（问 1、2） |
| slack-notify | 个人 | 环境 | 180 | ✂️ | slack-mcp 已接管（问 3） |
| deploy-policy | 项目 | 知识 | 170 | ✅ | 政策型约定（canary 流程、发版窗口），红线 |
| pdf-tables | 个人 | 环境 | 150 | ⏳ | 模型直读 PDF 已强，复杂表格未盲测 |
| deep-search | 个人 | 环境 | 140 | 🔗 | 与 quick-search 触发词打架，留此并彼 |
| quick-search | 个人 | 环境 | 130 | 🔗 | 并入 deep-search，空壳归档 |
| remember-this | 个人 | 环境 | 120 | ✂️ | 自动记忆已内建（问 2） |
| commit-style | 项目 | 混合 | 60 | 🔧 | 通用教学删净，留本仓 trailer 约定 |

## 判决依据

### browser-scrape-cookbook — ✂️

- **五问命中**：问 3 · MCP 已接管
- **证据**：playwright-mcp 的 navigate / click / extract 工具覆盖 cookbook 全部手写流程
- **搜身**：正文埋着 3 个站点的选择器脚本仍在用 → 迁至 `scripts/browser/`，再归档

### web-research — ✂️

- **五问命中**：问 2 · harness 已自带
- **证据**：内建 WebSearch + WebFetch 覆盖其 curl 拼搜索的全部功能
- **搜身**：埋着内部 wiki URL 与查询口诀 2 行 → 迁入 company-onboarding，再归档

### think-harder — ✂️

- **五问命中**：问 1 · 模型已内化
- **证据**：盲测——拿一个真实竞态 bug 让裸 agent 排查，其自发分步、自我验证，产出与 skill 承诺标准持平
- **搜身**：无埋藏事实

### code-review-checklist — ✂️

- **五问命中**：问 1 + 问 2
- **证据**：盲测——真实 PR 评审，清单 12 项裸做全覆盖，另抓到清单外 1 个并发 bug；harness 另有内建评审命令
- **搜身**：无埋藏事实

### slack-notify — ✂️

- **五问命中**：问 3 · MCP 已接管
- **证据**：curl 拼 webhook 的全部用法被 slack-mcp 发消息工具覆盖
- **搜身**：频道 ID 对照表 4 行 → 迁入 company-onboarding，再归档

### remember-this — ✂️

- **五问命中**：问 2 · harness 已自带
- **证据**：「帮我记住 X」写文件 hack，harness 自动记忆已内建同等功能
- **搜身**：历史记忆文件不动，仅归档 skill 本体

### deep-search + quick-search — 🔗

- **五问命中**：问 4 · 重复
- **证据**：两者描述共享「search / 搜索 / 查一下」触发词，实测同一任务两边抢触发；deep-search 为超集
- **搜身**：quick-search 独有的站内搜索参数 3 行迁入 deep-search，空壳归档

### pdf-tables — ⏳

- **五问命中**：问 1 存疑
- **证据**：模型直读 PDF 能力已强，但跨页复杂表格抽取未盲测——不嘴判
- **待补**：下次审计用一份真实年报做盲测题

### commit-style — 🔧

- **五问命中**：问 1（教学部分）
- **证据**：conventional commits 教学模型早已内化；但埋着本仓专属 trailer 与 issue 关联约定
- **手术**：58 行 → 9 行，只剩事实；描述税 60 → 25

### company-onboarding / deploy-policy — ✅

- 知识型 / 政策型，红线保护，不动。二者合计 430 token/轮 的描述税是**买对了的**。

## 执行记录

- 用户确认：整批确认；点名 browser-scrape-cookbook 的选择器脚本必须保留 → 已按搜身流程迁出后归档
- 归档：`tools/archive.sh` 移入 `~/.claude/skills-archive/2026-08-17/`，共 7 个目录（6 个 ✂️ + 1 个 🔗 空壳），MANIFEST 已记
- 修剪 diff：commit-style 58 行 → 9 行

## 恢复方式

```
tools/archive.sh --list
tools/archive.sh --restore <name>
```

归档位于 `~/.claude/skills-archive/`，未做任何 rm。

## 下次审计

触发条件（先到先触发）：换模型 / harness 大版本升级 / 新接 MCP / 距本次 90 天（2026-11-15）。
本次遗留重点：pdf-tables 的复杂表格盲测。
