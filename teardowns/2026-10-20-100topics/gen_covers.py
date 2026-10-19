#!/usr/bin/env python3
"""100 封面批量生成：深色科技风 + PIL 中文排版
用法: python3 gen_covers.py <start> <end>
  start/end: 1-based 编号，如 1 25 生成 001-025
输入: /home/hatch/lhg-workbuddy/episodes/topics100/NNN.md 的 "# 口播稿："标题
输出: /home/hatch/lhg-workbuddy/teardowns/2026-10-20-100topics/covers_gen/NNN.jpg (1080x1440)
"""
import sys, os, re
from PIL import Image, ImageDraw, ImageFont

BASE = "/home/hatch/lhg-workbuddy"
BG = f"{BASE}/episodes/ep01-install/media-generation-ep01-cover-bg-0-f1c90b68-bde4-4182-9ce9-6a4ada26fcba.webp"
FONT_BOLD = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
FONT_SANS = "/home/hatch/workspace/projects/lhg-vibe-knowledge/engine/fonts/NotoSansSC-VF.ttf"
OUT = f"{BASE}/teardowns/2026-10-20-100topics/covers_gen"
W, H = 1080, 1440  # 3:4

def get_title(n):
    p = f"{BASE}/episodes/topics100/{n:03d}.md"
    t = open(p).read()
    m = re.search(r'^# 口播稿：(.+?)（', t, re.M)
    title = m.group(1).strip() if m else f"第{n}期"
    # 压缩到 14 字以内
    if len(title) > 14:
        title = title[:14]
    return title

def draw_center(draw, y, text, font, fill, stroke=0, sw=0):
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=sw)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, y), text, font=font, fill=fill,
              stroke_width=sw, stroke_fill=(0, 0, 0) if sw else None)

def gen_one(n):
    bg = Image.open(BG).convert("RGB").resize((W, H))
    # 压暗上部保证文字可读
    overlay = Image.new("RGB", (W, H), (0, 0, 0))
    bg = Image.blend(bg, overlay, 0.25)
    d = ImageDraw.Draw(bg)
    title = get_title(n)

    # 顶部系列徽章
    f_small = ImageFont.truetype(FONT_SANS, 44)
    draw_center(d, 90, "把 AI 养成你的员工", f_small, (120, 220, 255))
    # 装饰线
    d.line([(W//2 - 160, 160), (W//2 + 160, 160)], fill=(120, 220, 255), width=3)

    # 主标题（黄字黑描边，自动换行，最多2行）
    f_title = ImageFont.truetype(FONT_BOLD, 110)
    # 简单二分行
    if len(title) > 7:
        mid = len(title) // 2
        # 尽量在标点处断
        for i in range(mid, 0, -1):
            if title[i] in "，。！？、：":
                mid = i + 1; break
        l1, l2 = title[:mid], title[mid:]
    else:
        l1, l2 = title, ""
    draw_center(d, 480, l1, f_title, (255, 210, 60), stroke=2, sw=3)
    if l2:
        draw_center(d, 620, l2, f_title, (255, 210, 60), stroke=2, sw=3)

    # 底部期数徽章
    f_num = ImageFont.truetype(FONT_BOLD, 72)
    # 徽章底
    bx, by, bw, bh = W//2 - 170, H - 260, 340, 110
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=20, fill=(20, 40, 70), outline=(120, 220, 255), width=3)
    draw_center(d, by + 18, f"第 {n:03d} 期", f_num, (255, 255, 255))

    # 底部小字
    f_tiny = ImageFont.truetype(FONT_SANS, 36)
    draw_center(d, H - 120, "每天一个小技巧", f_tiny, (150, 170, 190))

    os.makedirs(OUT, exist_ok=True)
    bg.save(f"{OUT}/{n:03d}.jpg", quality=92)
    print(f"{n:03d}: {title}")

if __name__ == "__main__":
    s, e = int(sys.argv[1]), int(sys.argv[2])
    for n in range(s, e + 1):
        gen_one(n)
    print(f"done {s}-{e}")
