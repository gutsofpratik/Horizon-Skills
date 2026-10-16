#!/usr/bin/env python3
"""walk_script.py — 无头穷举一个入戏剧本的全部路径（零依赖）

验证三件引擎测不出的事：
1. 每个结局都有路径可达（正典结局尤其）；
2. 理解度每条轨道的极值范围；
3. verdict 的每一档判词都存在能落进去的路径——写了没人能看到的判词等于没写。

用法：
    python3 walk_script.py script.json
    python3 walk_script.py script.json --paths   # 额外列出每条路径的选择序列
"""
import sys, json, argparse
from collections import defaultdict


def walk(d):
    scenes = {s['id']: s for s in d['scenes']}
    endings = {e['id']: e for e in d['endings']}
    paths = []          # (choices taken, ending id, u totals)

    def go(sid, u, taken, depth=0):
        if depth > 200:
            raise RuntimeError(f'疑似循环：{" > ".join(t[0] for t in taken)}')
        if sid in endings:
            paths.append((list(taken), sid, dict(u)))
            return
        sc = scenes[sid]
        branched = False
        for line in sc.get('lines', []):
            if 'choice' in line:
                branched = True
                for i, o in enumerate(line['choice']['options']):
                    u2 = dict(u)
                    for k, v in (o.get('u') or {}).items():
                        u2[k] = u2.get(k, 0) + v
                    go(o['goto'], u2, taken + [(sid, i, o['text'][:18])], depth + 1)
        if not branched:
            go(sc['next'], u, taken, depth + 1)

    go(d['scenes'][0]['id'], {}, [])
    return paths, endings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('script'); ap.add_argument('--paths', action='store_true')
    a = ap.parse_args()
    d = json.load(open(a.script, encoding='utf-8'))
    paths, endings = walk(d)

    print(f'路径总数：{len(paths)}')
    by_end = defaultdict(int)
    for _, e, _ in paths:
        by_end[e] += 1
    bad = False
    for eid, e in endings.items():
        tag = '📖 正典' if e.get('canon') else '   偏离'
        n = by_end.get(eid, 0)
        if n == 0: bad = True
        print(f'  {tag}  {eid:<14} 可达路径 {n} 条{"  ← 不可达！" if n == 0 else ""}')

    print('\n理解度极值（轨道: min..max）与判词档覆盖：')
    tracks = set(k for _, _, u in paths for k in u) | set(d.get('verdict', {}))
    for t in sorted(tracks):
        vals = [u.get(t, 0) for _, _, u in paths]
        lo, hi = min(vals), max(vals)
        print(f'  {t:<10} {lo:+d}..{hi:+d}')
        for b in d.get('verdict', {}).get(t, {}).get('bands', []):
            reach = any(b['min'] <= v <= b['max'] for v in vals)
            if not reach: bad = True
            print(f'      band [{b["min"]},{b["max"]}] {"✓" if reach else "✗ 无路径可落入！"}  {b["text"][:24]}…')

    if a.paths:
        print('\n全部路径：')
        for taken, e, u in paths:
            seq = ' > '.join(f'{s}#{i}' for s, i, _ in taken)
            print(f'  [{e}] {seq}  u={u}')

    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
