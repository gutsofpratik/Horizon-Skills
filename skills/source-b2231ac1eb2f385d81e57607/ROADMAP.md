# ROADMAP

## v0.1 — 能用（✅ 2026-08-17）

- 三分法 + 五问 + 盲测协议 + 五种判决的完整审计流程（SKILL.md / rubric.md）
- `tools/inventory.py`：扫描默认与自定义 skill 根，粗估描述 token 税
- `tools/archive.sh`：归档 / 恢复 / MANIFEST 留痕，永不 rm
- 报告模板 + 端到端演示审计

## v0.2 — 触发统计

- 扫 harness 的会话记录（如 Claude Code 的 `~/.claude/projects/*/`JSONL），统计每个 skill 近 N 天的实际触发次数
- 「90 天零触发」进入五问证据链：不删证据，删猜测
- inventory 表新增「最近触发」列

## v0.3 — 触发词打架 linter

- 跨 skill 的描述关键词冲突检测：同一触发词被几个 skill 认领
- 输出冲突矩阵，作为问 4（重复 / 吞并）的自动证据

## v0.4 — 换模型自动提醒

- 提供一个可选的 SessionStart hook：检测 model id 相比上次记录发生变化时，提示「新模型上线，该断舍离了」
- 附带 90 天到期提醒的 schedule 示例

## v0.5 — 插件与市场感知

- 审计范围覆盖 plugin / marketplace 安装的 skill（只判不动，给出「去哪卸载」的指引）
- 对市场 skill 输出「装它不如用内建」的替代建议

## 长期原则

- 工具永远零依赖（stdlib Python + POSIX bash）
- 判决永远要证据（盲测 / 指名道姓的替代者 / 腐烂实证）
- 永不 rm
