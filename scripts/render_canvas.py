#!/usr/bin/env python3
"""3:4 讲解卡片渲染器：JSON 文案 → 1080×1440 PNG（A-roll 卡片 + B-roll 录屏框）。

  python3 scripts/render_canvas.py templates/canvas/example.json --out out/ep01           # 随机主题与变体
  python3 scripts/render_canvas.py <json> --out <dir> --theme midnight --seed 42             # 锁定主题 / 复现
  python3 scripts/render_canvas.py <json> --out <dir> --hole                                 # 出镜圆窗、录屏框挖成透明
  python3 scripts/render_canvas.py --list-themes

[词] = 高亮；icon 可写内置图标名（见 templates/canvas/icons.py）或 emoji。依赖：Chrome/Chromium、Pillow。
"""
import argparse, colorsys, html, json, os, random, re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "templates/canvas"))
from icons import icon  # noqa: E402
from themes import THEMES  # noqa: E402

W, H, SCALE = 720, 960, 1.5
FX, FY, FW, FH = 36, 40, 648, 880           # 外框
CARD = (24, 84, 600, 466)                    # 主卡片（相对外框）
CAM_D, CAM_RING = 216, 5                     # 出镜圆窗
CAM_X, CAM_Y = 30, 572
SCREEN = (36, 122, 576, 360)                 # 录屏框（相对外框，16:10 = Mac 全屏去刘海）
CAM_C = (FX + CAM_X + CAM_D / 2, FY + CAM_Y + CAM_D / 2)
CAM_R = CAM_D / 2 - CAM_RING


def rgba(hexc, a):
    h = hexc.lstrip("#")
    if len(h) != 6:
        return hexc
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r},{g},{b},{a})"


def esc(s):
    return html.escape(str(s if s is not None else ""))


def hl(s):
    return re.sub(r"\[(.+?)\]", r"<em>\1</em>", esc(s)).replace("\n", "<br>")


def plain_len(s):
    return max((len(re.sub(r"[\[\]]", "", x)) for x in str(s or "").split("\n")), default=0)


GRAIN = ("url(\"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='240' height='240'>"
         "<filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' stitchTiles='stitch'/>"
         "<feColorMatrix values='0 0 0 0 0.5  0 0 0 0 0.5  0 0 0 0 0.5  0 0 0 1 0'/></filter>"
         "<rect width='100%' height='100%' filter='url(%23n)'/></svg>\")")


class Look:
    """一期的视觉抽签结果。"""

    def __init__(self, seed, theme=None):
        self.rng = random.Random(seed)
        self.seed = seed
        self.name = theme or self.rng.choice(sorted(THEMES))
        t = self.t = THEMES[self.name]
        r = self.rng
        self.hl = r.choice(t["hl"])
        self.cap = r.choice(t["cap"])
        self.pattern = r.choice(t["pattern"])
        self.ornament = r.choice(["numeral", "rings", "orb", "sparkle"])
        self.tile_r = r.choice([10, 14, 999])
        self.blobs = [(r.uniform(-15, 110), r.uniform(-10, 105), r.uniform(38, 70), c)
                      for c in r.sample(t["blobs"], 4)]
        self.angle = r.randint(110, 160)
        self.card = r.choice(["solid", "edge", "glass", "lift"])
        self.navs = r.choice(["tabs", "search", "dots"])


def css(L):
    t = L.t
    a, a2, ink = t["accent"], t["accent2"], t["ink"]
    blobs = ",".join(f"radial-gradient(circle at {x:.0f}% {y:.0f}%, {c} 0, transparent {s:.0f}%)" for x, y, s, c in L.blobs)
    head_font = ('"Songti SC","Noto Serif CJK SC","Noto Serif SC",serif' if t["serif"]
                 else '"PingFang SC","Noto Sans SC","Noto Sans CJK SC","Microsoft YaHei",sans-serif')
    patt = {
        "none": "none",
        "dots": f"radial-gradient({rgba('#ffffff' if t['dark'] else '#000000', .10 if t['dark'] else .07)} 1px, transparent 1.2px) 0 0/18px 18px",
        "grid": (f"linear-gradient({rgba('#ffffff' if t['dark'] else '#000000', .05)} 1px, transparent 1px) 0 0/36px 36px,"
                 f"linear-gradient(90deg,{rgba('#ffffff' if t['dark'] else '#000000', .05)} 1px, transparent 1px) 0 0/36px 36px"),
        "lines": f"repeating-linear-gradient(0deg, {rgba('#6b5330', .07)} 0 1px, transparent 1px 30px)",
    }[L.pattern]
    em = {
        "ink": f"color:{a}",
        "grad": f"background:linear-gradient(100deg,{a},{a2});-webkit-background-clip:text;background-clip:text;color:transparent",
        "marker": f"background:linear-gradient(transparent 60%,{rgba(a2 if not t['dark'] else a, .45)} 60%,{rgba(a2 if not t['dark'] else a, .45)} 92%,transparent 92%);padding:0 .08em",
        "under": f"text-decoration:underline;text-decoration-color:{a};text-decoration-thickness:.14em;text-underline-offset:.18em;text-decoration-skip-ink:none",
        "glow": f"color:{a};text-shadow:0 0 22px {rgba(a, .55)}",
    }[L.hl]
    bar = a2 if not t["dark"] else a
    cap = {
        "plain": "", "glow": f".cap span{{color:{ink};text-shadow:0 0 24px {rgba(a, .35)}}}",
        "bar": f".cap span{{background:{bar};color:#15130a;padding:6px 18px;border-radius:8px;box-shadow:0 6px 18px {rgba(bar, .35)}}} .cap em{{color:#15130a;background:none;-webkit-text-fill-color:#15130a;text-shadow:none;text-decoration:none}}",
        "pill": f".cap span{{background:{ink if not t['dark'] else a};color:{'#fff' if not t['dark'] else t['on_accent']};padding:8px 22px;border-radius:999px;box-shadow:0 10px 26px rgba({t['shadow']},.25)}} .cap em{{color:{a2 if not t['dark'] else t['on_accent']};-webkit-text-fill-color:currentColor;background:none;text-shadow:none;text-decoration:none}}",
        "under": f".cap span{{background:linear-gradient(transparent 70%,{rgba(a, .28)} 70%);padding:0 6px}}",
    }[L.cap]
    sh = t["shadow"]
    return f"""
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:{W}px;height:{H}px;overflow:hidden}}
body{{font-family:"PingFang SC","Noto Sans SC","Noto Sans CJK SC","Microsoft YaHei",sans-serif;color:{ink};
  background:{t['base']};-webkit-font-smoothing:antialiased;font-feature-settings:"tnum"}}
.bg{{position:absolute;inset:0;background:{blobs},{t['base']}}}
.pat{{position:absolute;inset:0;background:{patt}}}
.grain{{position:absolute;inset:0;background:{GRAIN};opacity:{.10 if t['dark'] else .07};mix-blend-mode:{'overlay' if t['dark'] else 'multiply'};pointer-events:none}}
.frame{{position:absolute;left:{FX}px;top:{FY}px;width:{FW}px;height:{FH}px;border-radius:34px;background:{t['frame']};
  box-shadow:0 1px 0 {t['frame_line']} inset,0 0 0 1px {rgba('#ffffff', .06) if t['dark'] else rgba('#ffffff', .7)},
  0 40px 80px -20px rgba({sh},{.55 if t['dark'] else .28}),0 12px 30px -10px rgba({sh},{.4 if t['dark'] else .18});overflow:hidden}}
.frame:before{{content:"";position:absolute;inset:0;border-radius:34px;pointer-events:none;
  background:linear-gradient(180deg,{rgba('#ffffff', .07 if t['dark'] else .55)},transparent 18%)}}
.nav{{position:absolute;left:28px;right:28px;top:22px;height:44px;display:flex;align-items:center;justify-content:space-between}}
.brand{{display:flex;align-items:center;gap:12px}}
.logo{{width:32px;height:32px;border-radius:10px;background:linear-gradient({L.angle}deg,{a},{a2});color:{t['on_accent']};
  display:flex;align-items:center;justify-content:center;font-weight:900;font-size:16px;
  box-shadow:0 1px 0 rgba(255,255,255,.45) inset,0 6px 14px {rgba(a, .35)}}}
.brand b{{font-size:20px;font-weight:800;letter-spacing:.2px}}
.brand i{{font-style:normal;font-size:15px;color:{t['sub']};padding-left:12px;border-left:1.5px solid {t['card_line']}}}
.tabs{{display:flex;align-items:center;gap:8px}}
.tabs span{{font-size:13px;color:{t['sub']};padding:5px 11px;border-radius:999px;background:{t['tile']};border:1px solid {t['tile_line']}}}
.live{{width:12px;height:12px;border-radius:50%;background:#ff5a5f;margin-left:6px;box-shadow:0 0 0 5px {rgba('#ff5a5f', .16)}}}
.navline{{position:absolute;left:28px;right:28px;top:72px;height:1px;background:linear-gradient(90deg,transparent,{t['card_line']} 12%,{t['card_line']} 88%,transparent)}}
.card{{position:absolute;left:{CARD[0]}px;top:{CARD[1]}px;width:{CARD[2]}px;height:{CARD[3]}px;border-radius:24px;background:{t['card']};
  border:1px solid {t['card_line']};padding:26px 28px 22px;overflow:hidden;box-shadow:0 1px 0 {t['frame_line']} inset,0 18px 40px -24px rgba({sh},.35)}}
.card>.inner{{position:relative;z-index:2;height:100%;display:flex;flex-direction:column}}
.orn{{position:absolute;z-index:1;pointer-events:none}}
.orn.numeral{{right:-6px;top:-34px;font:900 190px/1 "Helvetica Neue",Arial,sans-serif;color:transparent;-webkit-text-stroke:1.5px {rgba(a, .16)};letter-spacing:-8px}}
.orn.rings{{right:-120px;top:-120px;width:300px;height:300px;border-radius:50%;
  background:repeating-radial-gradient(circle,transparent 0 22px,{rgba(a, .10)} 22px 23px)}}
.orn.orb{{right:-80px;top:-90px;width:260px;height:260px;border-radius:50%;background:radial-gradient(circle at 35% 35%,{rgba(a2, .35)},{rgba(a, .12)} 55%,transparent 70%);filter:blur(4px)}}
.orn.sparkle{{right:22px;top:20px;color:{rgba(a, .35)}}} .orn.sparkle .ico{{width:26px;height:26px;display:block;margin-bottom:6px}}
.orn.sparkle .ico:nth-child(2){{width:16px;height:16px;margin-left:24px}}
.badge{{display:inline-flex;align-items:center;gap:10px;font-size:15px;color:{t['sub']};font-weight:600}}
.badge b{{font:700 13px/1 "SF Mono","JetBrains Mono",Menlo,monospace;color:{t['on_accent']};background:linear-gradient({L.angle}deg,{a},{a2});
  padding:6px 9px;border-radius:7px;letter-spacing:.5px;box-shadow:0 4px 10px {rgba(a, .28)}}}
.title{{margin-top:16px;font-family:{head_font};font-weight:900;line-height:1.18;letter-spacing:{'1px' if t['serif'] else '-.5px'}}}
.t-xl{{font-size:62px}} .t-l{{font-size:50px}} .t-m{{font-size:42px}} .t-s{{font-size:35px}}
em{{font-style:normal;{em}}}
.sub{{margin-top:14px;font-size:18px;line-height:1.5;color:{t['sub']}}}
.chips{{margin-top:auto;display:flex;flex-wrap:wrap;gap:10px}}
.chip{{display:flex;align-items:center;gap:8px;font-size:15px;font-weight:600;padding:9px 14px;border-radius:999px;background:{t['tile']};border:1px solid {t['tile_line']};color:{ink}}}
.chip .ico{{width:17px;height:17px;color:{a}}}
.tileic{{flex:none;width:46px;height:46px;border-radius:{min(L.tile_r, 23)}px;display:flex;align-items:center;justify-content:center;color:{a};
  background:{'rgba(255,255,255,.06)' if t['dark'] else '#ffffff'};border:1px solid {t['tile_line']};box-shadow:0 6px 14px -6px rgba({sh},.35)}}
.tileic .ico{{width:24px;height:24px}} .glyph{{font-size:22px;line-height:1;display:flex;align-items:center;justify-content:center;font-weight:800}}
.stats{{margin-top:auto;display:grid;gap:12px}}
.stat{{position:relative;border-radius:20px;padding:20px 20px 20px;background:{t['tile']};border:1px solid {t['tile_line']};overflow:hidden}}
.stat.warm{{background:{t['warm']};border-color:{t['warm_line']}}}
.stat .tileic{{width:38px;height:38px}} .stat .tileic .ico{{width:20px;height:20px}}
.stat .num{{margin-top:22px;font:900 64px/1 "Helvetica Neue","Noto Sans SC",sans-serif;letter-spacing:-1.5px;
  background:linear-gradient(100deg,{a},{a2});-webkit-background-clip:text;background-clip:text;color:transparent}}
.stat .num small{{font-size:18px;letter-spacing:0;margin-left:3px}}
.stat .lb{{margin-top:10px;font-size:17px;color:{t['sub']};font-weight:600}}
.items{{margin-top:auto;display:flex;flex-direction:column;gap:9px}}
.item{{display:flex;align-items:center;gap:15px;border-radius:16px;padding:10px 16px;background:{t['tile']};border:1px solid {t['tile_line']}}}
.item.warm{{background:{t['warm']};border-color:{t['warm_line']}}}
.item .ix{{font:800 13px/1 "SF Mono",Menlo,monospace;color:{t['muted']};width:20px}}
.item h4{{font-size:22px;font-weight:800;line-height:1.2;color:{ink}}}
.item h4 em{{{em}}}
.item p{{font-size:14.5px;color:{t['sub']};margin-top:4px}}
.item .tag{{margin-left:auto;font:800 15px/1 "Helvetica Neue",sans-serif;color:{a};background:{rgba(a, .10)};padding:7px 10px;border-radius:8px;white-space:nowrap}}
.steps{{margin-top:auto;position:relative;padding-left:4px}}
.steps:before{{content:"";position:absolute;left:25px;top:24px;bottom:24px;width:2px;background:linear-gradient({a},{a2});opacity:.35}}
.step{{position:relative;display:flex;gap:18px;align-items:flex-start;padding:10px 0}}
.step .node{{flex:none;width:44px;height:44px;border-radius:50%;display:flex;align-items:center;justify-content:center;
  font:900 18px/1 "Helvetica Neue",sans-serif;color:{t['on_accent']};background:linear-gradient({L.angle}deg,{a},{a2});box-shadow:0 0 0 6px {t['frame'] if not t['dark'] else '#141830'},0 8px 18px {rgba(a, .35)}}}
.step h4{{font-size:25px;font-weight:800;margin-top:6px}} .step p{{font-size:15px;color:{t['sub']};margin-top:5px}}
.cmp{{margin-top:auto;display:grid;grid-template-columns:1fr 1fr;gap:14px;position:relative}}
.col{{border-radius:20px;padding:22px 20px;background:{t['tile']};border:1px solid {t['tile_line']}}}
.col.win{{background:linear-gradient(160deg,{rgba(a, .14)},{rgba(a2, .10)});border-color:{rgba(a, .45)}}}
.col h5{{font-size:15px;color:{t['sub']};font-weight:700;letter-spacing:1px}} .col.win h5{{color:{a}}}
.col h4{{font-size:30px;font-weight:900;margin-top:6px}}
.col li{{list-style:none;font-size:17px;margin-top:14px;display:flex;gap:8px;color:{t['sub']}}} .col li .ico{{width:18px;height:18px;flex:none;color:{a};margin-top:1px}}
.col:not(.win) li .ico{{color:{t['muted']}}}
.vs{{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:46px;height:46px;border-radius:50%;background:{ink};color:{t['base']};
  font:900 16px/46px "Helvetica Neue",sans-serif;text-align:center;box-shadow:0 0 0 6px {t['frame'] if not t['dark'] else '#141830'}}}
.big{{margin:auto 0;text-align:left}}
.big .huge{{font:900 128px/1 "Helvetica Neue","Noto Sans SC",sans-serif;letter-spacing:-5px;background:linear-gradient(100deg,{a},{a2});-webkit-background-clip:text;background-clip:text;color:transparent}}
.big .huge small{{font-size:40px;letter-spacing:0}}
.big .quote{{font-family:{head_font};font-size:48px;font-weight:900;line-height:1.3}}
.big .q{{font:900 90px/0.6 Georgia,serif;color:{rgba(a, .35)};display:block;height:40px}}
.cta{{margin-top:auto;border-radius:20px;padding:22px;background:linear-gradient({L.angle}deg,{a},{a2});color:{t['on_accent']};position:relative;overflow:hidden;
  box-shadow:0 18px 36px -14px {rgba(a, .6)}}}
.cta:after{{content:"";position:absolute;right:-40px;top:-60px;width:200px;height:200px;border-radius:50%;background:rgba(255,255,255,.14)}}
.cta .k{{font-size:15px;font-weight:700;opacity:.85;display:flex;align-items:center;gap:8px}} .cta .k .ico{{width:18px;height:18px}}
.cta .w{{margin-top:8px;font-size:46px;font-weight:900;letter-spacing:1px}}
.cta .w span{{display:inline-block;background:rgba(255,255,255,.22);border:1.5px dashed rgba(255,255,255,.7);padding:2px 16px;border-radius:12px;margin:0 6px}}
.cta .g{{margin-top:10px;font-size:15.5px;opacity:.92}}
.window{{position:absolute;left:{SCREEN[0] - CARD[0] - 12}px;right:{SCREEN[0] - CARD[0] - 12}px;top:-1px;height:{SCREEN[3] + 36 + 12}px}}
.chrome{{height:36px;display:flex;align-items:center;gap:7px;padding-left:4px}} .chrome i{{width:11px;height:11px;border-radius:50%;display:block}}
.chrome .u{{margin-left:14px;flex:1;height:22px;border-radius:7px;background:{t['tile']};border:1px solid {t['tile_line']};font-size:12px;color:{t['muted']};display:flex;align-items:center;padding-left:10px}}
.scr{{position:absolute;left:{SCREEN[0]}px;top:{SCREEN[1]}px;width:{SCREEN[2]}px;height:{SCREEN[3]}px;border-radius:12px;
  background:repeating-linear-gradient(45deg,{rgba(a, .06)} 0 14px,transparent 14px 28px),{t['tile']};border:1px solid {t['tile_line']};
  display:flex;align-items:center;justify-content:center;flex-direction:column;gap:10px;color:{t['muted']};font-size:15px;z-index:3}}
.scr:before{{content:"";position:absolute;inset:-4px;border-radius:16px;z-index:-1;background:linear-gradient({L.angle}deg,{a},{a2});
  box-shadow:0 0 0 6px {rgba(a, .14)},0 14px 34px -8px {rgba(a, .45)}}}
.scr .ico{{width:42px;height:42px;color:{rgba(a, .6)}}}
.scrlab{{position:absolute;left:12px;right:12px;bottom:0;display:flex;align-items:center;gap:14px}}
.scrlab .stepno{{font:900 15px/1 "SF Mono",Menlo,monospace;color:{t['on_accent']};background:linear-gradient({L.angle}deg,{a},{a2});padding:8px 10px;border-radius:8px}}
.scrlab h4{{font-size:24px;font-weight:900}} .scrlab p{{font-size:14.5px;color:{t['sub']};margin-left:auto}}
.foot{{margin-top:14px;padding-top:11px;border-top:1px dashed {t['card_line']};font-size:12.5px;color:{t['muted']}}}
.cam{{position:absolute;left:{CAM_X}px;top:{CAM_Y}px;width:{CAM_D}px;height:{CAM_D}px;border-radius:50%;padding:{CAM_RING}px;
  background:conic-gradient(from {L.angle}deg,{a},{a2},{rgba(a, .25)},{a});box-shadow:0 20px 40px -12px rgba({sh},.45),0 0 0 8px {rgba(a, .07)}}}
.cam .ph{{width:100%;height:100%;border-radius:50%;overflow:hidden;background:radial-gradient(circle at 50% 30%,{rgba(a2, .22)},transparent 70%),{'#1c2029' if t['dark'] else '#ffffff'};
  display:flex;align-items:flex-end;justify-content:center;color:{rgba(a, .35)}}}
.cam .ph .ico{{width:150px;height:150px;margin-bottom:-22px}}
.cam img{{width:100%;height:100%;object-fit:cover;border-radius:50%;display:block}}
.host{{position:absolute;left:{CAM_X + CAM_D / 2}px;top:{CAM_Y + CAM_D - 22}px;transform:translateX(-50%);white-space:nowrap;
  font-size:14px;font-weight:800;padding:6px 14px;border-radius:999px;background:{t['frame'] if not t['dark'] else '#1a1f3a'};color:{ink};
  border:1px solid {t['tile_line']};box-shadow:0 6px 16px -6px rgba({sh},.4);display:flex;align-items:center;gap:6px}}
.host:before{{content:"";width:7px;height:7px;border-radius:50%;background:#2fd36b;box-shadow:0 0 0 3px rgba(47,211,107,.2)}}
.side{{position:absolute;left:286px;right:32px;top:590px}}
.side .k{{display:flex;align-items:flex-end;justify-content:space-between}}
.side .k span{{font-size:13.5px;color:{t['muted']};font-weight:600;letter-spacing:.5px}}
.side .pg{{font:900 30px/1 "Helvetica Neue",sans-serif;color:{ink};letter-spacing:-1px}} .side .pg small{{font-size:15px;color:{t['muted']};letter-spacing:0;font-weight:700}}
.side h3{{margin-top:16px;display:flex;align-items:center;gap:12px;font-size:23px;font-weight:900;line-height:1.25}}
.side h3 .tileic{{width:40px;height:40px}} .side h3 .tileic .ico{{width:21px;height:21px}}
.side p{{margin-top:12px;font-size:16px;line-height:1.5;color:{t['sub']}}}
.prog{{margin-top:16px;display:flex;gap:6px}} .prog span{{flex:1;max-width:34px;height:5px;border-radius:3px;background:{t['tile_line']}}}
.prog span.done{{background:{rgba(a, .45)}}} .prog span.on{{background:linear-gradient(90deg,{a},{a2});max-width:52px}}
.hero{{position:absolute;right:28px;bottom:40px;width:136px;height:136px}}
.hero .halo{{position:absolute;inset:-30px;border-radius:50%;background:radial-gradient(circle,{rgba(a, .22)},transparent 65%)}}
.hero .hcore{{position:absolute;inset:18px;border-radius:38px;transform:rotate(-8deg);display:flex;align-items:center;justify-content:center;
  background:linear-gradient({L.angle}deg,{a},{a2});color:{t['on_accent']};box-shadow:0 1px 0 rgba(255,255,255,.5) inset,0 24px 40px -12px {rgba(a, .55)}}}
.hero .hcore .ico{{width:56px;height:56px;transform:rotate(8deg)}}
.bar{{margin-top:14px;height:8px;border-radius:5px;background:{rgba('#ffffff' if t['dark'] else '#000000', .07)};overflow:hidden}}
.bar i{{display:block;height:100%;border-radius:5px;background:linear-gradient(90deg,{a},{a2})}}
.card.p-cover .sub{{max-width:340px}}
.card.k-edge{{border-top:0;box-shadow:inset 0 3px 0 {a},0 18px 40px -24px rgba({sh},.35)}}
.card.k-glass{{background:{rgba('#ffffff', .05) if t['dark'] else rgba('#ffffff', .55)};backdrop-filter:blur(14px) saturate(1.4)}}
.card.k-lift{{box-shadow:0 1px 0 {t['frame_line']} inset,14px 14px 0 -2px {rgba(a, .14)},0 18px 40px -24px rgba({sh},.35)}}
.srch{{display:flex;align-items:center;gap:7px;min-width:190px}} .srch .ico{{width:14px;height:14px}}
.dt{{display:block;width:9px;height:9px;border-radius:50%;background:{t['tile_line']}}} .dt.on{{width:26px;border-radius:5px;background:linear-gradient(90deg,{a},{a2})}}
.cap{{position:absolute;left:24px;right:24px;top:{812}px;height:56px;display:flex;align-items:center;justify-content:center;text-align:center}}
.cap span{{font-weight:900;letter-spacing:.5px;line-height:1.25}}
.cap.c-l span{{font-size:31px}} .cap.c-m span{{font-size:27px}} .cap.c-s span{{font-size:23px}}
{cap}
"""


def body(p, idx, total, L):
    typ = p.get("type") or ("stats" if p.get("stats") else "list" if p.get("items") else "steps" if p.get("steps")
                            else "compare" if p.get("compare") else "cta" if p.get("cta") else "cover" if idx == 0 else "big")
    t = p.get("title", "")
    n = plain_len(t)
    tcls = "t-xl" if (typ == "cover" and n <= 9) else "t-l" if n <= 9 else "t-m" if n <= 12 else "t-s"
    head = f'<div class="badge"><b>{idx + 1:02d}</b>{hl(p.get("badge"))}</div>'
    if t and typ != "screen":
        head += f'<div class="title {tcls}">{hl(t)}</div>'
    if p.get("subtitle") and typ != "screen":
        head += f'<div class="sub">{hl(p["subtitle"])}</div>'
    x = ""
    if typ == "cover":
        x = f'<div class="hero"><div class="halo"></div><div class="hcore">{icon(p.get("hero", "spark"))}</div></div>'
        x += '<div class="chips">' + "".join(f'<div class="chip">{icon(c.get("icon", "spark"))}{hl(c.get("text"))}</div>'
                                           for c in p.get("chips", [])) + "</div>"
    elif typ == "stats":
        s = p["stats"]
        x = f'<div class="stats" style="grid-template-columns:repeat({len(s)},1fr)">' + "".join(
            f'<div class="stat {"warm" if v.get("warm") else ""}"><div class="tileic">{icon(v.get("icon", "spark"))}</div>'
            f'<div class="num">{esc(v["num"])}<small>{esc(v.get("unit", ""))}</small></div><div class="lb">{hl(v.get("label"))}</div>'
            f'<div class="bar"><i style="width:{bar_w(v, s)}%"></i></div></div>'
            for v in s) + "</div>"
    elif typ == "list":
        x = '<div class="items">' + "".join(
            f'<div class="item {"warm" if v.get("warm") else ""}"><span class="ix">{k + 1:02d}</span><div class="tileic">{icon(v.get("icon", "check"))}</div>'
            f'<div><h4>{hl(v["title"])}</h4>{f"<p>{hl(v.get(chr(100)+chr(101)+chr(115)+chr(99)))}</p>" if v.get("desc") else ""}</div>'
            f'{f"<span class=tag>{esc(v[chr(116)+chr(97)+chr(103)])}</span>" if v.get("tag") else ""}</div>'
            for k, v in enumerate(p["items"])) + "</div>"
    elif typ == "steps":
        x = '<div class="steps">' + "".join(
            f'<div class="step"><div class="node">{k + 1}</div><div><h4>{hl(v["title"])}</h4><p>{hl(v.get("desc"))}</p></div></div>'
            for k, v in enumerate(p["steps"])) + "</div>"
    elif typ == "compare":
        c = p["compare"]

        def col(side, win):
            lis = "".join(f'<li>{icon("check" if win else "arrow")}<span>{hl(b)}</span></li>' for b in side.get("points", []))
            return f'<div class="col {"win" if win else ""}"><h5>{esc(side.get("label", ""))}</h5><h4>{hl(side.get("name"))}</h4><ul>{lis}</ul></div>'
        x = f'<div class="cmp">{col(c["left"], False)}{col(c["right"], True)}<div class="vs">VS</div></div>'
    elif typ == "big":
        if p.get("number"):
            x = f'<div class="big"><div class="huge">{esc(p["number"])}<small>{esc(p.get("unit", ""))}</small></div><div class="sub">{hl(p.get("note"))}</div></div>'
        elif p.get("quote"):
            x = f'<div class="big"><span class="q">“</span><div class="quote">{hl(p["quote"])}</div><div class="sub">{hl(p.get("note"))}</div></div>'
    elif typ == "cta":
        c = p["cta"]
        x = ('<div class="chips" style="margin-top:22px">' + "".join(f'<div class="chip">{icon(g.get("icon", "check"))}{hl(g.get("text"))}</div>' for g in p.get("chips", [])) + "</div>"
             if p.get("chips") else "")
        x += (f'<div class="cta"><div class="k">{icon(c.get("icon", "chat"))}{esc(c.get("lead", "评论区扣"))}</div>'
             f'<div class="w"><span>{esc(c["word"])}</span></div><div class="g">{hl(c.get("get"))}</div></div>')
    elif typ == "screen":
        s = p.get("screen", {})
        u = esc(s.get("url", "WorkBuddy"))
        return (f'<div class="window"><div class="chrome"><i style="background:#ff5f57"></i><i style="background:#febc2e"></i>'
                f'<i style="background:#28c840"></i><div class="u">{u}</div></div></div>'
                f'<div class="scrlab"><span class="stepno">{esc(s.get("step", f"{idx + 1:02d}"))}</span><h4>{hl(t)}</h4><p>{hl(p.get("subtitle"))}</p></div>'), typ
    foot = f'<div class="foot">{hl(p["foot"])}</div>' if p.get("foot") else ""
    return head + x + foot, typ


def bar_w(v, s):
    try:
        mx = max(float(re.sub(r"[^\d.]", "", str(x["num"])) or 0) for x in s)
        return max(6, round(float(re.sub(r"[^\d.]", "", str(v["num"]))) / mx * 100))
    except (ValueError, ZeroDivisionError):
        return 60


def ornament(L, idx):
    if L.ornament == "numeral":
        return f'<div class="orn numeral">{idx + 1:02d}</div>'
    if L.ornament == "sparkle":
        return f'<div class="orn sparkle">{icon("spark")}{icon("spark")}</div>'
    return f'<div class="orn {L.ornament}"></div>'


def page_html(cfg, p, idx, total, L, avatar, base):
    nav = cfg.get("nav", {})
    tabs = "".join(f"<span>{esc(x)}</span>" for x in nav.get("tabs", []))
    inner, typ = body(p, idx, total, L)
    side = p.get("side", {})
    prog = "".join(f'<span class="{"on" if i == idx else "done" if i < idx else ""}"></span>' for i in range(total))
    if avatar:
        cam = f'<img src="{(base / avatar).resolve().as_uri()}">'
    else:
        cam = f'<div class="ph">{icon("user")}</div>'
    host = f'<div class="host">{esc(cfg["host"])}</div>' if cfg.get("host") else ""
    cap = p.get("caption", "")
    ccls = "c-l" if plain_len(cap) <= 14 else "c-m" if plain_len(cap) <= 18 else "c-s"
    card_inner = (f'{ornament(L, idx) if typ != "screen" else ""}<div class="inner">{inner}</div>')
    scr = ""
    if typ == "screen":
        scr = f'<div class="scr">{icon("play")}<span>B-roll · 实操录屏放这里</span></div>'
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{css(L)}</style></head><body>
<div class="bg"></div><div class="pat"></div>
<div class="frame">
 <div class="nav"><div class="brand"><span class="logo">{esc(nav.get("logo", "W"))}</span><b>{esc(nav.get("brand", ""))}</b><i>{esc(nav.get("topic", ""))}</i></div>
 {nav_right(L, tabs, nav)}</div>
 <div class="navline"></div>
 <div class="card p-{typ} k-{L.card}">{card_inner}</div>{scr}
 <div class="cam">{cam}</div>{host}
 <div class="side"><div class="k"><span>{esc(side.get("kicker", nav.get("topic", "")))}</span><div class="pg">{idx + 1:02d}<small> / {total:02d}</small></div></div>
  <h3><span class="tileic">{icon(side.get("icon", "spark"))}</span><span>{hl(side.get("headline", ""))}</span></h3>
  <p>{hl(side.get("sub", ""))}</p><div class="prog">{prog}</div></div>
 <div class="cap {ccls}"><span>{hl(cap)}</span></div>
</div><div class="grain"></div></body></html>""", typ


def nav_right(L, tabs, nav):
    if L.navs == "search":
        return f'<div class="tabs"><span class="srch">{icon("target")}{esc(nav.get("search", "搜索技巧、skill…"))}</span><span class="live" style="padding:0;border:0"></span></div>'
    if L.navs == "dots":
        return '<div class="tabs"><i class="dt"></i><i class="dt"></i><i class="dt on"></i></div>'
    return f'<div class="tabs">{tabs}<span class="live" style="padding:0;border:0"></span></div>'


def chrome_bin():
    for c in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable",
              "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              "/Applications/Chromium.app/Contents/MacOS/Chromium"):
        p = shutil.which(c) or (c if os.path.exists(c) else None)
        if p:
            return p
    sys.exit("找不到 Chrome / Chromium")


def cut_holes(png, typ, host=None):
    from PIL import Image, ImageDraw
    im = Image.open(png).convert("RGBA")
    k = im.width / W
    big = Image.new("L", (im.width * 4, im.height * 4), 255)   # 4x 超采样，边缘不锯齿
    d = ImageDraw.Draw(big)
    cx, cy, r = CAM_C[0] * k * 4, CAM_C[1] * k * 4, CAM_R * k * 4
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=0)
    if typ == "screen":
        x, y, w, h = ((FX + SCREEN[0]) * k * 4, (FY + SCREEN[1]) * k * 4, SCREEN[2] * k * 4, SCREEN[3] * k * 4)
        d.rounded_rectangle((x, y, x + w, y + h), radius=12 * k * 4, fill=0)
    if host:   # 主播名牌压在圆窗边上，保留不挖
        wpx = sum(14 if ord(ch) > 255 else 8 for ch in host) + 28 + 13
        hx, hy = CAM_X + FX + CAM_D / 2, FY + CAM_Y + CAM_D - 22
        d.rounded_rectangle(((hx - wpx / 2 - 2) * k * 4, (hy - 1) * k * 4, (hx + wpx / 2 + 2) * k * 4, (hy + 30) * k * 4),
                            radius=15 * k * 4, fill=255)
    im.putalpha(big.resize(im.size, Image.LANCZOS))
    im.save(png)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json", nargs="?")
    ap.add_argument("--out")
    ap.add_argument("--theme", choices=sorted(THEMES))
    ap.add_argument("--seed", type=int)
    ap.add_argument("--hole", action="store_true", help="出镜圆窗 + 录屏框挖成透明")
    ap.add_argument("--keep-html", action="store_true")
    ap.add_argument("--list-themes", action="store_true")
    a = ap.parse_args()
    if a.list_themes:
        print("\n".join(sorted(THEMES)))
        return
    if not (a.json and a.out):
        ap.error("需要 json 和 --out")
    src = Path(a.json)
    cfg = json.loads(src.read_text(encoding="utf-8"))
    seed = a.seed if a.seed is not None else cfg.get("seed", random.randrange(1, 10 ** 6))
    L = Look(seed, a.theme or cfg.get("theme"))
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    pages = cfg["pages"]
    avs = list(cfg.get("avatars", []))
    random.Random(seed).shuffle(avs)
    chrome = chrome_bin()
    meta = {"seed": seed, "theme": L.name, "card": L.card, "nav": L.navs, "highlight": L.hl, "caption": L.cap, "pattern": L.pattern, "ornament": L.ornament,
            "size": [int(W * SCALE), int(H * SCALE)],
            "cam_circle": {"cx": CAM_C[0] * SCALE, "cy": CAM_C[1] * SCALE, "r": CAM_R * SCALE},
            "screen_rect": {"x": (FX + SCREEN[0]) * SCALE, "y": (FY + SCREEN[1]) * SCALE, "w": SCREEN[2] * SCALE, "h": SCREEN[3] * SCALE},
            "pages": []}
    for i, p in enumerate(pages):
        av = p.get("avatar") or (avs[i % len(avs)] if avs and not a.hole else None)
        doc, typ = page_html(cfg, p, i, len(pages), L, av, src.parent)
        h = out / f"page_{i + 1:02d}.html"
        png = out / f"page_{i + 1:02d}.png"
        h.write_text(doc, encoding="utf-8")
        subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-sandbox", "--allow-file-access-from-files",
                        f"--force-device-scale-factor={SCALE}", f"--window-size={W},{H}", f"--screenshot={png.resolve()}",
                        h.resolve().as_uri()], check=True, capture_output=True)
        if a.hole:
            cut_holes(png, typ, cfg.get("host"))
        if not a.keep_html:
            h.unlink()
        meta["pages"].append({"file": png.name, "type": typ, "avatar": av})
        print("✓", png, typ)
    (out / "layout.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"theme={L.name} card={L.card} nav={L.navs} seed={seed} hl={L.hl} cap={L.cap} pattern={L.pattern} ornament={L.ornament}")


if __name__ == "__main__":
    main()
