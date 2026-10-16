<div align="center">

# 📖 入戏.skill

**把一本书，变成你能玩进去的一场戏。**

一本书 → 一个双击即玩的视觉小说（galgame）。
你扮演原著里被略过的边角人物，在原文真实存在的抉择路口上，重新选一次。

**[🎮 在线试玩 →](https://swaylq.github.io/ruxi-skill/)**

[English](README_en.md) · [官网](https://swaylq.github.io/ruxi-skill/) · [MIT License](LICENSE) · 适配 Claude Code / 任何能跑 skill 的 agent · [分享到 X](https://twitter.com/intent/tweet?text=%E5%85%A5%E6%88%8F.skill%20%E2%80%94%20%E6%8A%8A%E4%B8%80%E6%9C%AC%E4%B9%A6%E5%8F%98%E6%88%90%E4%BD%A0%E8%83%BD%E7%8E%A9%E8%BF%9B%E5%8E%BB%E7%9A%84%E8%A7%86%E8%A7%89%E5%B0%8F%E8%AF%B4%EF%BC%8C%E6%AF%8F%E4%B8%AA%E9%80%89%E6%8B%A9%E9%83%BD%E6%8C%87%E5%BE%97%E5%9B%9E%E5%8E%9F%E6%96%87&url=https%3A%2F%2Fgithub.com%2Fswaylq%2Fruxi-skill)

</div>

---

> **状态**：v0.1 —— 核心流程已跑通。首个完整 demo《变形记 · 厨房这一侧》可玩：13 场 · 10 选择点 · 3 结局 · 520 条路径穷举全通 · 一周目约 15-20 分钟 · 产物 54 KB 单文件。

## 它做出来的东西长什么样

你给它《变形记》，它还你一个 `index.html`。打开：

> 你是萨姆沙家那个十六岁的帮厨女孩——原著只给了她一句话：「这个约十六岁的女孩勇敢地留了下来。」
>
> 变形当天的清晨，你跪在走廊擦地。门后传出那个声音。厨娘问你：「你说，那是个什么动静？」
>
> **▸ 「兴许是着凉了。跑外勤的人，嗓子坏了常有的事。」**
> **▸ 「不像。着凉的嗓子是哑，这个……是里头多了一个声音。」**
>
> 你选了第二个。屏幕角落浮现一行小字：
> *原文：…ein nicht zu unterdrückendes, schmerzliches Piepsen mischte…（第一章 · 嗓音的描写）*
> *你听见了。全家都只当是感冒，你听见了。*

<table><tr>
<td><img src="docs/shots/01-title.png" alt="标题页"></td>
<td><img src="docs/shots/02-dialogue.png" alt="对话：说话者高亮"></td>
<td><img src="docs/shots/03-choice.png" alt="选择点"></td>
<td><img src="docs/shots/05-settle-top.png" alt="结算：理解度判词"></td>
</tr></table>

通关时它不给你「好感度结算」，它告诉你：**这本书你读懂了多少，哪些地方你一直在误读。**

## 和「让 AI 写个 galgame」有什么区别

五条铁律，违反任何一条就会退化成同人文生成器：

| # | 铁律 | 它防住的是 |
|---|---|---|
| 1 | 不覆盖全书，只取 5-8 场戏 | 三十万字压成的流水账 |
| 2 | 玩家默认演**原著里被略过的边角人物** | 「演主角」的无悬念，「演外来者」的同人化 |
| 3 | **每个分支点指得回原文的一句话**，游戏内标注出处 | 凭空编造的选项；玩游戏因此成为一种重读 |
| 4 | 不做好感度，做**理解度**——选项是解读，不是讨好 | 「选 A 讨好她」的浅玩法；懂一个人和讨好一个人经常相反 |
| 5 | 结局里必有一条是**原著真实发生的事**（正典结局） | 所有分支等价胡编、失去参照 |

已有工具里最接近的是 novel-to-game（小说 → 任意类型游戏原型）：它不专攻视觉小说、需要选平台、不谈版权。入戏只做视觉小说这一种形态，产物零安装，版权判定是流程的第 0 步。

## 怎么用

```
你 ❯ 把《变形记》做成游戏
```

skill 会走五个阶段（细节见 [SKILL.md](SKILL.md)）：

```
0 版权判定   作者卒年 + 首发年 → 公版 / 仅限本地，写进产物
1 拆书选戏   tools/scan_scenes.py 机械算「压强」，模型只精读入选的 5-8 章
2 定角      从原文 grep 出边角人物，验三条标准，和你确认「你演谁」
3 写本      剧本 = 一个 JSON（schema 固定），每个选择点带原文出处
4 构建自测   tools/build_html.py 校验+构建；walk_script.py 穷举全部路径
```

产物：一个自包含 `index.html`（零外部请求、离线可玩、手机可玩）+ `CREDITS.md`。

美术分两档：默认零依赖（内置剪影 + 渐变背景，54 KB）；可选 AI 图档（`codex-image` 出背景与立绘，构建时内嵌，约 2 MB，仍是单文件）。《变形记》demo 是 AI 图档。

### 压强 —— 不把书喂给模型也能选对戏

```
压强 = 对白占比 × 交锋次数 ÷ 在场人数     （话密、来回多、人少 = 一场对峙）
```

《傲慢与偏见》124,116 词、67 章，压强榜前三：内瑟菲尔德客厅舌战、凯瑟琳夫人上门摊牌、达西与伊丽莎白初次交锋——正是全书最锋利的三场对手戏。这一步纯 Python 标准库，零 token。

## ⚡ 安装

```bash
git clone https://github.com/swaylq/ruxi-skill ~/.claude/skills/ruxi-skill
```

<details>
<summary>其他宿主</summary>

| 宿主 | 方法 |
|---|---|
| Claude Code（项目级） | clone 到 `<项目>/.claude/skills/ruxi-skill` |
| 其他 agent 框架 | 把 `SKILL.md` 作为系统提示装载，保持目录结构 |

依赖：Python ≥ 3.8（仅标准库）。就这些。

</details>

## 🎮 Demo

| 书 | 你演谁 | 中心问题 | 状态 |
|---|---|---|---|
| 《变形记》卡夫卡 1915 | 十六岁的帮厨女孩 | 如果你不锁那扇门呢？ | ✅ [demos/metamorphosis](demos/metamorphosis/) |
| 《傲慢与偏见》奥斯汀 1813 | 朗博恩管家 Hill 太太 | 这个家的体面，有一半锁在仆人房里 | ✅ [demos/pride](demos/pride/) |

## 版权这件事，写进流程而不是免责声明

- 改编即演绎作品——**不内嵌一字原文也可能侵权**。所以阶段 0 就做判定，三档结论写进产物；有版权的书只构建「仅限本地自娱」版（自动注水印页脚）。
- **译本有独立版权**。《变形记》demo 的全部引文取自 1915 德文初版并自译——工作时读的那个英译本（有版权）一个字没进产物。
- 仓库内完整 demo 只用公有领域的书。每个产物自带 `CREDITS.md`。
- 以上是工程约定，不是法律意见。

## 项目结构

```
ruxi-skill/
├── SKILL.md                    # 入口：五阶段工作流 + 品味守则
├── prompts/                    # 三份操作单（选戏定角 / 写本 / 自测交付）
├── tools/
│   ├── scan_scenes.py          # 选戏：EPUB/TXT → 场景压强表（零依赖）
│   ├── build_html.py           # 校验 + 构建单文件 index.html
│   ├── template.html           # 视觉小说引擎（打字机/立绘/分支/存档/结算）
│   ├── cutout.py               # 白底立绘 → 透明 WebP（连通抠图，白围裙不误杀）
│   └── walk_script.py          # 穷举全部路径：结局可达性 + 判词档覆盖
├── references/
│   ├── adaptation.md           # 改编方法论（五条铁律的操作化）
│   └── script-schema.md        # 剧本 JSON 契约
└── demos/
    ├── metamorphosis/          # 《变形记 · 厨房这一侧》完整可玩
    └── pride/                  # 《傲慢与偏见 · 下房这一侧》完整可玩
```

## Roadmap

见 [ROADMAP.md](ROADMAP.md)：v0.2《傲慢与偏见》· v0.3 Ren'Py 导出 + 中文公版书 · v1.0 发布。

## License

MIT —— 随便用，随便改，随便造。原著请尊重各自版权状态。

<div align="center">

*一本好书值得读两遍。第二遍，从里面读。*

</div>
