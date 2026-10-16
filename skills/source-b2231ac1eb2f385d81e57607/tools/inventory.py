#!/usr/bin/env python3
"""断舍离 inventory — 扫描已安装的 skill，粗估每轮的描述 token 税。零依赖（仅标准库）。

用法:
  python3 tools/inventory.py                    # 扫默认根（个人 / 项目 / 插件）
  python3 tools/inventory.py --root PATH        # 追加扫描根（可重复；也接受单个 skill 目录）
  python3 tools/inventory.py --json             # JSON 输出

默认扫描根（存在才扫）:
  ~/.claude/skills/*/SKILL.md
  ./.claude/skills/*/SKILL.md
  ~/.claude/plugins/*/skills/*/SKILL.md
  ~/.claude/plugins/marketplaces/*/*/skills/*/SKILL.md

token 粗估口径: CJK 字符 ≈ 1 token/字，其余 ≈ 4 字符/token。
只用于排序与量级对比，不是计费口径。
"""

import argparse
import json
import os
import sys
import time

CJK_RANGES = (
    (0x3000, 0x303F),  # CJK 标点
    (0x3040, 0x30FF),  # 假名
    (0x3400, 0x4DBF),  # 扩展 A
    (0x4E00, 0x9FFF),  # 基本区
    (0xAC00, 0xD7AF),  # 谚文
    (0xF900, 0xFAFF),  # 兼容表意
    (0xFF00, 0xFFEF),  # 全角
)

SCRIPT_EXTS = {".py", ".sh", ".js", ".ts", ".rb", ".pl"}


def est_tokens(text):
    cjk = sum(1 for c in text if any(a <= ord(c) <= b for a, b in CJK_RANGES))
    return round(cjk + (len(text) - cjk) / 4)


def parse_frontmatter(path):
    """朴素解析 SKILL.md 的 YAML 头，取 name 与 description（支持 | / > 多行块）。"""
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            lines = f.read().splitlines()
    except OSError:
        return None, None
    if not lines or lines[0].strip() != "---":
        return None, None
    name, desc = None, None
    i = 1
    while i < len(lines):
        line = lines[i]
        if line.strip() == "---":
            break
        stripped = line.strip()
        if stripped.startswith("name:"):
            name = stripped[len("name:"):].strip().strip("\"'")
        elif stripped.startswith("description:"):
            val = stripped[len("description:"):].strip()
            if val in ("", "|", "|-", "|+", ">", ">-", ">+"):
                base_indent = len(line) - len(line.lstrip())
                block = []
                j = i + 1
                while j < len(lines):
                    nxt = lines[j]
                    if nxt.strip() == "---":
                        break
                    if nxt.strip() == "":
                        block.append("")
                        j += 1
                        continue
                    indent = len(nxt) - len(nxt.lstrip())
                    if indent <= base_indent:
                        break
                    block.append(nxt.strip())
                    j += 1
                desc = "\n".join(block).strip()
                i = j - 1
            else:
                desc = val.strip("\"'")
        i += 1
    return name, desc


def scan_skill_dir(d, origin):
    skill_md = os.path.join(d, "SKILL.md")
    if not os.path.isfile(skill_md):
        return None
    name, desc = parse_frontmatter(skill_md)
    name = name or os.path.basename(os.path.normpath(d))
    desc = desc or ""
    files = size = 0
    newest = 0.0
    has_scripts = False
    for root, _dirs, fnames in os.walk(d):
        for fn in fnames:
            fp = os.path.join(root, fn)
            try:
                st = os.stat(fp)
            except OSError:
                continue
            files += 1
            size += st.st_size
            newest = max(newest, st.st_mtime)
            if os.path.splitext(fn)[1].lower() in SCRIPT_EXTS:
                has_scripts = True
    return {
        "name": name,
        "path": os.path.abspath(d),
        "origin": origin,
        "desc": desc,
        "desc_tokens": est_tokens(name + " " + desc),
        "files": files,
        "size_kb": round(size / 1024, 1),
        "has_scripts": has_scripts,
        "age_days": round((time.time() - newest) / 86400) if newest else None,
    }


def default_roots():
    home = os.path.expanduser("~")
    roots = [
        (os.path.join(home, ".claude", "skills"), "个人"),
        (os.path.join(os.getcwd(), ".claude", "skills"), "项目"),
    ]
    plugins = os.path.join(home, ".claude", "plugins")
    if os.path.isdir(plugins):
        try:
            for p in sorted(os.listdir(plugins)):
                cand = os.path.join(plugins, p, "skills")
                if os.path.isdir(cand):
                    roots.append((cand, "插件"))
            market = os.path.join(plugins, "marketplaces")
            if os.path.isdir(market):
                for m in sorted(os.listdir(market)):
                    for p in sorted(os.listdir(os.path.join(market, m))):
                        cand = os.path.join(market, m, p, "skills")
                        if os.path.isdir(cand):
                            roots.append((cand, "插件"))
        except OSError:
            pass
    return roots


def main():
    ap = argparse.ArgumentParser(description="扫描已安装 skill，粗估描述 token 税")
    ap.add_argument("--root", action="append", default=[],
                    help="追加扫描根（含若干 skill 子目录的目录，或单个 skill 目录）")
    ap.add_argument("--json", action="store_true", help="以 JSON 输出")
    args = ap.parse_args()

    targets = [(r, "自定义") for r in args.root] or default_roots()
    rows, seen = [], set()
    for root, origin in targets:
        root = os.path.expanduser(root)
        if not os.path.isdir(root):
            continue
        # 根本身就是一个 skill 目录
        cands = [root] if os.path.isfile(os.path.join(root, "SKILL.md")) else [
            os.path.join(root, d) for d in sorted(os.listdir(root))
        ]
        for d in cands:
            real = os.path.realpath(d)
            if real in seen or not os.path.isdir(d):
                continue
            row = scan_skill_dir(d, origin)
            if row:
                seen.add(real)
                rows.append(row)

    rows.sort(key=lambda r: -r["desc_tokens"])
    total = sum(r["desc_tokens"] for r in rows)

    if args.json:
        json.dump({"skills": rows, "count": len(rows), "desc_tokens_total": total},
                  sys.stdout, ensure_ascii=False, indent=2)
        print()
        return

    if not rows:
        print("没扫到任何 skill。用 --root 指一下路径？")
        return
    print("| skill | 来源 | 描述税(token/轮) | 文件 | 大小(KB) | 最后改动 | 带脚本 |")
    print("|---|---|---:|---:|---:|---:|:-:|")
    for r in rows:
        age = f"{r['age_days']} 天前" if r["age_days"] is not None else "?"
        print(f"| {r['name']} | {r['origin']} | {r['desc_tokens']} | {r['files']} "
              f"| {r['size_kb']} | {age} | {'✓' if r['has_scripts'] else ''} |")
    print(f"\n共 {len(rows)} 个 skill，描述税合计 ~{total} token —— 每一轮对话都在付。")


if __name__ == "__main__":
    main()
