# 剧本 JSON 结构 — 引擎与生成的共同契约

一个入戏游戏 = 一个符合本结构的 JSON。`tools/build_html.py` 把它内联进模板产出单文件
`index.html`。生成剧本的 agent 按本文件逐字段填；引擎按本文件逐字段渲染。两边都不得私自加字段。

## 顶层

```json
{
  "meta":    { … },
  "cast":    { … },
  "scenes":  [ … ],
  "endings": [ … ],
  "verdict": { … }
}
```

## meta — 书、玩家、全局观感

```json
{
  "title":   "入戏 · 变形记",
  "book": {
    "title": "Die Verwandlung（变形记）",
    "author": "Franz Kafka",
    "year": 1915,
    "author_died": 1924,
    "lang": "de",
    "pd_status": "public-domain-worldwide",
    "translation_note": "剧本文字为原创改编；原文引用取自德文初版（公有领域）"
  },
  "player": { "name": "安娜", "role": "萨姆沙家的女仆", "note": "原著里只有几行字的人" },
  "palette": { "bg": "#17130f", "panel": "#211b15", "text": "#d8cfc0", "dim": "#7a6f5f", "accent": "#b98a4e" },
  "credits": "本作品为改编，非原著。原著：… 改编：入戏.skill"
}
```

- `palette` 五色从**书的调性**来（卡夫卡＝昏褐；奥斯汀＝奶油与墨绿）。引擎全部配色只用这五个值。
- `pd_status` 取 `public-domain-worldwide` / `public-domain-us` / `copyrighted-local-only` 之一，
  最后一档时构建工具在产物里注入「仅限本地自娱」水印页。

## cast — 出场角色（含玩家）

```json
"grete": { "name": "葛蕾特", "short": "妹", "hue": 28, "shape": "small", "note": "十七岁，妹妹" }
```

- key 用小写拉丁 id，剧本里 `who` 引用它。玩家固定 id `me`，没有立绘。
- `hue` 0-360：该角色剪影与名牌的主色相。同场角色色相差 ≥ 40。
- `shape` 五选一：`tall` 瘦高 · `broad` 宽厚 · `small` 纤小 · `bent` 佝偻 · `round` 圆钝。
  引擎内置这五种抽象人形剪影，**没有第六种**——素材零下载的代价就是这个约束。

## scenes — 场景（游戏的基本单位）

```json
{
  "id": "s1",
  "title": "第一场 · 锁着的门",
  "bg": { "c1": "#1c1712", "c2": "#3a2d1e", "label": "萨姆沙家走廊 · 清晨" },
  "source": { "loc": "第一章 ¶1-¶20", "de": "Als Gregor Samsa eines Morgens…", "zh": "一天早晨，格里高尔·萨姆沙从不安的梦中醒来……" },
  "lines": [ …见下… ],
  "next": "s2"
}
```

- `bg` 是双色纵向渐变加一行场景标签，没有背景图。
- `source` 是**本场的原文锚**：这场戏改编自原文哪里。`loc` 人类可读（章＋段落），
  `de`/`zh`（或 `en`/`zh`）是原文短句及译文，各 ≤ 60 字。
- `next`：lines 走完后的去向（场景 id 或结局 id）。若 lines 以 choice 结尾则不用 next。

### lines 的两种元素

**台词/旁白：**
```json
{ "who": "grete", "mood": "tense", "text": "妈妈，别过去——让我来。" }
```
- `who: null` ＝ 旁白；`who: "me"` ＝ 玩家的内心或话。
- `mood` 四选一 `calm | tense | soft | hard`，控制剪影姿态与亮度的微变。省略＝calm。
- 一条 `text` ≤ 90 字。长段拆多条——视觉小说的节奏是一次一口。

**选择点：**
```json
{ "choice": {
    "prompt": "太太在发抖。这个时候，你——",
    "options": [
      { "text": "跪下来，求她放你走。",
        "goto": "s3-leave",
        "u": { "grete": 0 },
        "source": { "loc": "第一章 ¶34", "de": "…bat sie kniefällig um sofortige Entlassung…", "zh": "她跪着请求立刻辞工" },
        "echo": "原著里，你就是这么做的。" },
      { "text": "留下。总得有人给这家人做饭。",
        "goto": "s3-stay",
        "u": { "grete": 1 },
        "source": { "loc": "同上——她本可以不走", "de": "…", "zh": "…" },
        "echo": "从这一刻起，你离开了书页。" }
    ]
} }
```

- **每个 option 必须带 `source`**——这个选择点长在原文哪句话上。找不到出处的选项不许存在。
- `u`：理解度增量，键为 cast id，值 -1/0/+1。理解度**不开门、不锁路线**，只进结算——
  它衡量「你看懂这个人没有」，不是好感度。加分的选项必须是贴着原著人物逻辑的那个解读。
- `echo`：选完后屏幕角落浮现的一行小字（≤ 40 字），通常是 source 的引文或一句冷静的旁注。可空。

## endings — 结局

```json
{ "id": "end-canon", "canon": true, "title": "书页合上的地方",
  "lines": [ { "who": null, "text": "…" } ],
  "source": { "loc": "第三章 ¶…", "de": "…", "zh": "…" } }
```

- **必须有且只有一个 `canon: true`**——原著真实发生的事。玩家走到它时，引擎明确标出
  「这就是书里写的」。其余结局是偏离，`canon: false`。
- 结局数 2-4 个。多于 4 个说明分支在乱长。

## verdict — 结算（理解度 → 判词）

```json
"grete": { "bands": [
  { "min": -9, "max": 0, "text": "你始终把她当成那个会拉小提琴的小姑娘。她不是。" },
  { "min": 1,  "max": 2, "text": "你看到了她的累，没看到她的狠。这本书你读了一半。" },
  { "min": 3,  "max": 9, "text": "你看懂了：最先放弃他的，是最爱他的那个。" }
] }
```

- 每个主要角色一组判词。判词是**对玩家阅读的判定**，口吻冷静、贴原文，不奉承。
- 结算页顺序：各角色判词 → 你抵达的结局（正典与否）→ 全部原文出处列表（loc + 引文）。

## 体量红线（v1 实测前的暂定值，打通《变形记》后回填）

- 场景 5-8 个；每场 lines 12-30 条；选择点全游戏 5-9 个；一周目 15-30 分钟。
- 剧本总字数 4,000-8,000 字。低于下限没有戏，高于上限是在抄书。

## 可选：AI 背景图（v0.1.1 增补）

- `meta.cover`：标题页主视觉，本地图片路径（相对 script.json）。构建时 base64 内嵌，产物仍是单文件。
- `scenes[].bg.img`：该场背景图路径。有图时渐变层自动降为半透明叠色（multiply），保持全局调性；`c1/c2/label` 仍然必填——没有图的场景和图加载失败时靠它们兜底。
- 构建器对 >400KB 的图自动压缩（sips，宽 900 jpeg）。美术默认档仍是纯 CSS/SVG：这两个字段是可选升级，不是要求。
- `cast.<id>.img`：可选，人物立绘图路径（**带透明底**的 png/webp；用 `tools/cutout.py` 从白底生成图抠出）。
  有图时替代内置剪影；`hue`/`shape` 仍必填（名牌颜色 + 无图/加载失败时的兜底）。png/webp 不会被转 jpg（保透明）。
