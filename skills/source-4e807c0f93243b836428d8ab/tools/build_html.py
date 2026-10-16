#!/usr/bin/env python3
"""build_html.py — 校验入戏剧本 JSON，并把它注入 template.html 产出单文件游戏。

用法：
    python3 build_html.py script.json out/index.html
    python3 build_html.py script.json --check        # 只校验

校验规则见 references/script-schema.md。错误 → 非零退出；警告 → 打印后继续。
"""
import sys, os, json, argparse

SHAPES = {'tall', 'broad', 'small', 'bent', 'round'}
PD = {'public-domain-worldwide', 'public-domain-us', 'copyrighted-local-only'}
MOODS = {'calm', 'tense', 'soft', 'hard'}


def validate(d):
    errs, warns = [], []
    E, W = errs.append, warns.append

    for k in ('meta', 'cast', 'scenes', 'endings', 'verdict'):
        if k not in d: E(f'缺少顶层键 {k}')
    if errs: return errs, warns

    meta = d['meta']
    for k in ('title', 'book', 'player', 'palette', 'credits'):
        if k not in meta: E(f'meta 缺少 {k}')
    if meta.get('book', {}).get('pd_status') not in PD:
        E(f'meta.book.pd_status 必须是 {sorted(PD)} 之一')
    for k in ('bg', 'panel', 'text', 'dim', 'accent'):
        if k not in meta.get('palette', {}): E(f'palette 缺少 {k}')

    cast = d['cast']
    if 'me' not in cast: E('cast 必须包含玩家 id "me"')
    for cid, c in cast.items():
        if c.get('shape') not in SHAPES:
            E(f'cast.{cid}.shape={c.get("shape")!r} 不在五种剪影之内 {sorted(SHAPES)}')
        if not isinstance(c.get('hue'), (int, float)) or not (0 <= c['hue'] <= 360):
            E(f'cast.{cid}.hue 必须是 0-360 的数')

    ids = {s['id'] for s in d['scenes']} | {e['id'] for e in d['endings']}
    if len(ids) < len(d['scenes']) + len(d['endings']): E('场景/结局 id 有重复')

    def chk_source(src, where, need=True):
        if not src:
            if need: E(f'{where} 缺少 source')
            return
        if not src.get('loc'): E(f'{where}.source 缺少 loc')
        if not (src.get('de') or src.get('en') or src.get('quote') or src.get('zh')):
            E(f'{where}.source 缺少引文（de/en/quote/zh 至少一项）')

    targets = set()
    for s in d['scenes']:
        sid = s['id']
        chk_source(s.get('source'), f'scene {sid}')
        if 'bg' not in s or not all(k in s['bg'] for k in ('c1', 'c2', 'label')):
            E(f'scene {sid}.bg 需要 c1/c2/label')
        has_choice_last = False
        speakers = set()
        for i, l in enumerate(s.get('lines', [])):
            if 'choice' in l:
                ch = l['choice']
                if not ch.get('prompt'): E(f'scene {sid} choice 缺 prompt')
                opts = ch.get('options', [])
                if not (2 <= len(opts) <= 4): W(f'scene {sid} 选项数 {len(opts)}（建议 2-4）')
                for j, o in enumerate(opts):
                    if o.get('goto') not in ids: E(f'scene {sid} 选项{j} goto={o.get("goto")!r} 不存在')
                    targets.add(o.get('goto'))
                    chk_source(o.get('source'), f'scene {sid} 选项{j}')
                    for k in (o.get('u') or {}):
                        if k not in cast: E(f'scene {sid} 选项{j} u 键 {k} 不在 cast')
                has_choice_last = (i == len(s['lines']) - 1)
            else:
                w = l.get('who')
                if w is not None and w not in cast: E(f'scene {sid} 行{i} who={w!r} 不在 cast')
                if w: speakers.add(w)
                if l.get('mood') and l['mood'] not in MOODS: E(f'scene {sid} 行{i} mood 非法')
                if len(l.get('text', '')) > 90: W(f'scene {sid} 行{i} 超 90 字（{len(l["text"])}）')
                if not l.get('text'): E(f'scene {sid} 行{i} 缺 text')
        if not has_choice_last:
            if 'next' not in s: E(f'scene {sid} 末行非 choice 且无 next')
            elif s['next'] not in ids: E(f'scene {sid}.next={s["next"]!r} 不存在')
            else: targets.add(s['next'])
        hues = sorted(cast[c]['hue'] for c in speakers if c != 'me')
        for a, b in zip(hues, hues[1:]):
            if b - a < 40: W(f'scene {sid} 同场 hue 距 {b-a} < 40（{hues}）')

    canon = [e for e in d['endings'] if e.get('canon')]
    if len(canon) != 1: E(f'canon 结局必须恰好 1 个，现有 {len(canon)}')
    for e in d['endings']:
        chk_source(e.get('source'), f'ending {e["id"]}')
        for i, l in enumerate(e.get('lines', [])):
            w = l.get('who')
            if w is not None and w not in cast: E(f'ending {e["id"]} 行{i} who 不在 cast')

    first = d['scenes'][0]['id']
    reachable = {first} | targets
    for s in d['scenes'][1:]:
        if s['id'] not in reachable: W(f'scene {s["id"]} 不可达')
    for e in d['endings']:
        if e['id'] not in reachable: W(f'ending {e["id"]} 不可达')

    for k, v in d['verdict'].items():
        if k not in cast: E(f'verdict 键 {k} 不在 cast')
        for b in v.get('bands', []):
            if not all(x in b for x in ('min', 'max', 'text')): E(f'verdict.{k} band 缺 min/max/text')

    return errs, warns


import base64, subprocess, tempfile


def _embed_image(path_rel, base_dir, warns):
    """本地图片 → data URI。>400KB 先用 sips 压成宽 900 的 jpeg。"""
    p = path_rel if os.path.isabs(path_rel) else os.path.join(base_dir, path_rel)
    if not os.path.isfile(p):
        return None, f'图片不存在：{path_rel}'
    ext0 = os.path.splitext(p)[1].lower()
    if os.path.getsize(p) > 400 * 1024 and ext0 not in ('.webp', '.png'):
        tmp = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False).name
        r = subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', '72',
                            '--resampleWidth', '900', p, '--out', tmp],
                           capture_output=True)
        if r.returncode == 0:
            p = tmp
        else:
            warns.append(f'sips 压缩失败，原样内嵌：{path_rel}')
    elif os.path.getsize(p) > 400 * 1024:
        warns.append(f'{path_rel} 超 400KB 且为 png/webp（保透明不转 jpg），请先自行压缩')
    ext = os.path.splitext(p)[1].lower().lstrip('.') or 'png'
    mime = 'jpeg' if ext in ('jpg', 'jpeg') else ext
    data = base64.b64encode(open(p, 'rb').read()).decode()
    return f'data:image/{mime};base64,{data}', None


def build(script_path, out_path):
    d = json.load(open(script_path, encoding='utf-8'))
    errs, warns = validate(d)
    base_dir = os.path.dirname(os.path.abspath(script_path))
    if d['meta'].get('cover'):
        uri, err = _embed_image(d['meta']['cover'], base_dir, warns)
        if err: errs.append(err)
        else: d['meta']['cover'] = uri
    for sc in d['scenes']:
        img = sc.get('bg', {}).get('img')
        if img:
            uri, err = _embed_image(img, base_dir, warns)
            if err: errs.append(err)
            else: sc['bg']['img'] = uri
    for cid, c in d['cast'].items():
        if c.get('img'):
            uri, err = _embed_image(c['img'], base_dir, warns)
            if err: errs.append(err)
            else: c['img'] = uri
    for w in warns: print(f'⚠ {w}')
    if errs:
        for e in errs: print(f'✗ {e}')
        sys.exit(1)
    tpl_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'template.html')
    tpl = open(tpl_path, encoding='utf-8').read()
    payload = json.dumps(d, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    if '/*__SCRIPT_JSON__*/' not in tpl:
        print('✗ template.html 缺少占位符 /*__SCRIPT_JSON__*/'); sys.exit(1)
    html = tpl.replace('/*__SCRIPT_JSON__*/null', payload) if '/*__SCRIPT_JSON__*/null' in tpl \
        else tpl.replace('/*__SCRIPT_JSON__*/', payload)
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    open(out_path, 'w', encoding='utf-8').write(html)
    kb = os.path.getsize(out_path) / 1024
    print(f'✓ {out_path}（{kb:.0f} KB，零错误，{len(warns)} 警告）')
    if d['meta']['book']['pd_status'] == 'copyrighted-local-only':
        print('ℹ 有版权档：产物含「仅限本地自娱」页脚，请勿公开分发')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('script'); ap.add_argument('out', nargs='?')
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    if a.check or not a.out:
        d = json.load(open(a.script, encoding='utf-8'))
        errs, warns = validate(d)
        for w in warns: print(f'⚠ {w}')
        for e in errs: print(f'✗ {e}')
        print('✓ 校验通过' if not errs else f'✗ {len(errs)} 个错误')
        sys.exit(1 if errs else 0)
    build(a.script, a.out)


if __name__ == '__main__':
    main()
