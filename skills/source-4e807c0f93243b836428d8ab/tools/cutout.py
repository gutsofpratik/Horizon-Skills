#!/usr/bin/env python3
"""cutout.py — 白底立绘 → 透明底 WebP（入戏.skill 立绘管线）

gpt-image 系列没有原生透明，立绘按「纯白底」生成后用本脚本抠图：
只移除**连通到画布边缘的白色区域**（BFS），人物内部的白色（围裙、帽子、白发）保留。
边缘做 1px 羽化，裁剪到人物包围盒，统一缩放，存带 alpha 的 WebP。

用法：
    python3 cutout.py in.png out.webp [--height 900] [--thresh 235]
"""
import sys, argparse
from collections import deque
from PIL import Image, ImageFilter


def cutout(src, dst, height=900, thresh=235):
    im = Image.open(src).convert('RGBA')
    w, h = im.size
    px = im.load()

    # BFS：从四边出发，把「亮度 ≥ thresh 的近白像素」标记为背景
    bg = bytearray(w * h)
    q = deque()

    def near_white(x, y):
        r, g, b, a = px[x, y]
        return r >= thresh and g >= thresh and b >= thresh

    for x in range(w):
        for y in (0, h - 1):
            if near_white(x, y) and not bg[y * w + x]:
                bg[y * w + x] = 1; q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if near_white(x, y) and not bg[y * w + x]:
                bg[y * w + x] = 1; q.append((x, y))
    while q:
        x, y = q.popleft()
        for nx, ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if 0 <= nx < w and 0 <= ny < h and not bg[ny * w + nx] and near_white(nx, ny):
                bg[ny * w + nx] = 1; q.append((nx, ny))

    # 背景 → alpha 0；生成 mask 后羽化 1px
    mask = Image.new('L', (w, h), 255)
    mpx = mask.load()
    for y in range(h):
        base = y * w
        for x in range(w):
            if bg[base + x]:
                mpx[x, y] = 0
    mask = mask.filter(ImageFilter.GaussianBlur(1.1))
    im.putalpha(mask)

    # 裁剪到不透明包围盒（留 2% 边距），统一高度
    bbox = im.getbbox()
    if bbox:
        mx = int(w * 0.02)
        im = im.crop((max(0, bbox[0]-mx), max(0, bbox[1]-mx),
                      min(w, bbox[2]+mx), min(h, bbox[3]+mx)))
    ratio = height / im.height
    im = im.resize((max(1, int(im.width * ratio)), height), Image.LANCZOS)
    im.save(dst, 'WEBP', quality=82, method=6)
    import os
    print(f'{dst}  {im.width}x{im.height}  {os.path.getsize(dst)//1024}KB')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('src'); ap.add_argument('dst')
    ap.add_argument('--height', type=int, default=900)
    ap.add_argument('--thresh', type=int, default=235)
    a = ap.parse_args()
    cutout(a.src, a.dst, a.height, a.thresh)
