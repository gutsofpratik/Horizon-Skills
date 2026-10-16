#!/usr/bin/env python3
"""scan_scenes.py — 入戏.skill 的选戏工具（零依赖，Python ≥ 3.8 标准库）

把一本书（EPUB / TXT）机械地切成章，为每章算「压强」：

    压强 = 对白占比 × 交锋次数 ÷ 在场人数
    （话密、来回多、人少 = 一场对峙）

用途：在把任何文本喂给模型之前，先算出哪几章最有戏。模型只读入选的章。

用法：
    python3 scan_scenes.py book.epub
    python3 scan_scenes.py book.txt --names "Elizabeth,Darcy,Jane"
    python3 scan_scenes.py book.epub --json > scenes.json
    python3 scan_scenes.py book.epub --top 12

说明：
- EPUB 按 OPF spine 顺序读正文（阅读顺序，不能按文件名排）。
- 章节切分识别：CHAPTER X / 第N章·回·节 / 罗马数字或数字独行。
- 人名：--names 优先（中文书必给，无分词时自动提取不可靠）；
  英文书缺省时自动提取「大写开头且非句首高频」的候选词。
"""
import sys, re, json, zipfile, argparse
from collections import Counter
from html.parser import HTMLParser
from xml.etree import ElementTree as ET


class _Text(HTMLParser):
    def __init__(self):
        super().__init__(); self.buf = []; self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'): self.skip += 1
        if tag in ('p', 'br', 'div', 'h1', 'h2', 'h3', 'h4', 'li'): self.buf.append('\n')
    def handle_endtag(self, tag):
        if tag in ('script', 'style'): self.skip = max(0, self.skip - 1)
    def handle_data(self, d):
        if not self.skip: self.buf.append(d)
    def text(self):
        return re.sub(r'\n{3,}', '\n\n', ''.join(self.buf))


def epub_docs(path):
    """按 spine 顺序返回 (名字, 纯文本) 列表。"""
    z = zipfile.ZipFile(path)
    cont = ET.fromstring(z.read('META-INF/container.xml'))
    opf_path = cont.find('.//{*}rootfile').get('full-path')
    base = opf_path.rsplit('/', 1)[0] + '/' if '/' in opf_path else ''
    opf = ET.fromstring(z.read(opf_path))
    hrefs = {i.get('id'): i.get('href') for i in opf.findall('.//{*}manifest/{*}item')}
    out = []
    for ref in opf.findall('.//{*}spine/{*}itemref'):
        href = hrefs.get(ref.get('idref'))
        if not href: continue
        try:
            raw = z.read(base + href).decode('utf-8', 'replace')
        except KeyError:
            continue
        p = _Text(); p.feed(raw)
        out.append((href.split('/')[-1], p.text()))
    return out


# 章节标题：CHAPTER X | 第N章/回/节 | 罗马数字或纯数字独行
CHAP = re.compile(
    r'\n\s*('
    r'CHAPTER\s+[IVXLCDM\d]+[.\s]*'
    r'|第[一二三四五六七八九十百千零〇\d]+[章回节卷幕]'
    r'|[IVXLCDM]{1,7}\.?'
    r'|\d{1,3}\.?'
    r')\s*\n', re.I)

QUOTE = re.compile(r'[“"]([^”"]{2,1200})[”"]|「([^」]{2,1200})」|『([^』]{2,600})』')

STOP = {'The', 'A', 'An', 'It', 'He', 'She', 'They', 'We', 'You', 'I', 'His', 'Her', 'But', 'And',
        'If', 'In', 'On', 'At', 'As', 'So', 'Of', 'To', 'By', 'For', 'That', 'This', 'There',
        'What', 'When', 'Then', 'Now', 'Not', 'No', 'Yes', 'Oh', 'Mr', 'Mrs', 'Miss', 'Sir',
        'One', 'All', 'Was', 'Were', 'Is', 'Are', 'Had', 'Have', 'Do', 'Did', 'Chapter',
        'God', 'Project', 'Gutenberg', 'Foundation', 'License', 'United', 'States',
        'Literary', 'Archive', 'Ebook', 'Well', 'Would', 'Could', 'Should', 'Every'}


def auto_names(text, k=12):
    """英文启发：非句首的大写开头词，取高频前 k 个。中文书请用 --names。"""
    cand = Counter()
    for m in re.finditer(r'(?<![.!?"“”]\s)(?<!^)\b([A-Z][a-z]{2,15})\b', text):
        w = m.group(1)
        if w not in STOP:
            cand[w] += 1
    return [w for w, n in cand.most_common(k) if n >= 5]


def wordcount(s):
    """混合词数：英文按空格，CJK 按字。"""
    cjk = len(re.findall(r'[一-鿿]', s))
    latin = len(re.findall(r'[A-Za-z]+(?:\'[a-z]+)?', s))
    return cjk + latin


GB_START = re.compile(r'\*{3}\s*START OF (THE|THIS) PROJECT GUTENBERG.*?\*{3}', re.I | re.S)
GB_END = re.compile(r'\*{3}\s*END OF (THE|THIS) PROJECT GUTENBERG.*', re.I | re.S)


def strip_boilerplate(text):
    """剥掉 Project Gutenberg 的头尾声明，避免许可证文本污染统计。"""
    m = GB_START.search(text)
    if m: text = text[m.end():]
    m = GB_END.search(text)
    if m: text = text[:m.start()]
    return text


def split_chapters(docs):
    """把 spine 文档流切成 (标题, 正文) 章节序列。"""
    chapters = []
    for name, text in docs:
        text = strip_boilerplate(text)
        parts = CHAP.split(text)
        if len(parts) == 1:                      # 整个文件没有章标题
            if wordcount(text) >= 300:
                chapters.append((name, text))
            continue
        # split 交替返回 [前言, 标题, 正文, 标题, 正文…]
        if wordcount(parts[0]) >= 300:
            chapters.append((f'{name}·前言', parts[0]))
        for i in range(1, len(parts), 2):
            title, body = parts[i].strip(), parts[i + 1]
            if wordcount(body) >= 300:
                chapters.append((title, body))
    return chapters


def scan(chapters, names):
    rows = []
    for idx, (title, body) in enumerate(chapters):
        w = wordcount(body)
        quotes = [next(g for g in m.groups() if g) for m in QUOTE.finditer(body)]
        dlg = sum(wordcount(q) for q in quotes)
        cast = sorted({n for n in names if n in body}, key=lambda n: -body.count(n))
        ratio = dlg / w if w else 0.0
        heat = ratio * len(quotes) / max(1, len(cast[:8]))
        rows.append({
            'no': idx + 1, 'title': title, 'words': w,
            'dialogue_ratio': round(ratio, 3), 'turns': len(quotes),
            'cast': cast[:6], 'heat': round(heat, 2),
            'opening': ' '.join(body.split())[:60],
        })
    return rows


def main():
    ap = argparse.ArgumentParser(description='为一本书生成「场景压强表」')
    ap.add_argument('book', help='EPUB 或 TXT 文件')
    ap.add_argument('--names', help='逗号分隔的人物名单（中文书必给）')
    ap.add_argument('--top', type=int, default=10, help='表格模式显示前 N 行')
    ap.add_argument('--json', action='store_true', help='输出全量 JSON（给 agent 消费）')
    a = ap.parse_args()

    if a.book.lower().endswith('.epub'):
        docs = epub_docs(a.book)
    else:
        docs = [(a.book, open(a.book, encoding='utf-8', errors='replace').read())]

    chapters = split_chapters(docs)
    full = '\n'.join(b for _, b in chapters)
    names = [n.strip() for n in a.names.split(',')] if a.names else auto_names(full)
    rows = scan(chapters, names)

    if a.json:
        print(json.dumps({'names': names, 'chapters': rows}, ensure_ascii=False, indent=1))
        return

    total = sum(r['words'] for r in rows)
    print(f'章节 {len(rows)} 个 · 总词数 {total:,} · 人物{"（自动提取，中文书请用 --names）" if not a.names else ""}：{", ".join(names[:10])}\n')
    print(f'{"#":>3} {"章":<18}{"词数":>7}{"对白":>6}{"交锋":>5}{"压强":>7}  在场')
    for r in sorted(rows, key=lambda r: -r['heat'])[:a.top]:
        print(f'{r["no"]:>3} {r["title"][:17]:<18}{r["words"]:>7}{r["dialogue_ratio"]:>6.0%}{r["turns"]:>5}{r["heat"]:>7.1f}  {", ".join(r["cast"][:4])}')
        print(f'{"":>4}└─ {r["opening"]}')


if __name__ == '__main__':
    main()
