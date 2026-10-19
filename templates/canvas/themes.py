"""画布主题。每个主题 = 一套色彩/质感变量 + 允许的随机变体。
渲染时按 seed 抽：主题（未锁定时）、背景光斑位置、纹理、标题高亮方式、字幕样式、角标装饰。
同一期所有页共用一个 seed → 期内统一，期与期之间不重样。"""

THEMES = {
  "aurora": dict(  # 冷紫极光 · 玻璃
    dark=False, base="#eceefe", blobs=["#aebfff", "#ffd3b0", "#d8bbff", "#ffbfe0", "#b9f0ff"],
    frame="rgba(255,255,255,.80)", frame_line="rgba(255,255,255,.95)", card="linear-gradient(160deg,#ffffff 0%,#f5f6ff 100%)",
    card_line="rgba(90,100,180,.14)", tile="rgba(242,244,255,.9)", tile_line="rgba(80,100,200,.16)",
    ink="#10152a", sub="#566079", muted="#8a93ab", accent="#3d5afe", accent2="#9b51e0", on_accent="#ffffff",
    warm="#fff3e3", warm_line="#f1d9b5", shadow="70,60,150",
    hl=["grad", "ink"], cap=["plain", "pill", "under"], pattern=["none", "dots"], serif=False),
  "mint": dict(  # 薄荷工作室 · 小k 色系
    dark=False, base="#eaf8f1", blobs=["#bdeed6", "#fff1a6", "#c4efff", "#d6f7c4", "#e9fff4"],
    frame="rgba(255,255,255,.86)", frame_line="#ffffff", card="linear-gradient(170deg,#ffffff,#f3fbf7)",
    card_line="rgba(16,120,80,.14)", tile="#f1faf5", tile_line="rgba(16,150,100,.20)",
    ink="#0d1f17", sub="#4d6359", muted="#87998f", accent="#0fa36b", accent2="#f5c400", on_accent="#ffffff",
    warm="#fff8d6", warm_line="#f0dc8a", shadow="20,90,60",
    hl=["marker", "ink"], cap=["bar", "plain"], pattern=["none", "grid", "dots"], serif=False),
  "midnight": dict(  # 午夜霓虹 · 深色
    dark=True, base="#060a18", blobs=["#283094", "#0b6f8f", "#6b2a93", "#13205e", "#0b4f6b"],
    frame="rgba(14,18,38,.78)", frame_line="rgba(140,160,255,.22)", card="linear-gradient(160deg,rgba(30,36,70,.85),rgba(14,18,40,.9))",
    card_line="rgba(130,150,255,.18)", tile="rgba(255,255,255,.05)", tile_line="rgba(140,170,255,.20)",
    ink="#f2f5ff", sub="#a3aecb", muted="#6d7898", accent="#5ee7ff", accent2="#a78bfa", on_accent="#061024",
    warm="rgba(255,190,90,.10)", warm_line="rgba(255,190,90,.35)", shadow="0,0,0",
    hl=["grad", "glow"], cap=["glow", "pill"], pattern=["grid", "dots", "none"], serif=False),
  "paper": dict(  # 纸本 · 朱砂 · 宋体标题
    dark=False, base="#efe7d8", blobs=["#e6d6bb", "#f3e7d2", "#e2cfb0", "#f6ecdb", "#eadbc2"],
    frame="#fbf7ee", frame_line="#fffdf8", card="linear-gradient(180deg,#fffdf8,#f8f2e6)",
    card_line="rgba(80,60,30,.16)", tile="#f6efe1", tile_line="rgba(120,90,40,.20)",
    ink="#1c1a16", sub="#5f584c", muted="#9a917f", accent="#d4421c", accent2="#1f4fbf", on_accent="#fffaf0",
    warm="#fbe9d9", warm_line="#e9c4a2", shadow="90,70,40",
    hl=["under", "ink"], cap=["plain", "under"], pattern=["lines", "none"], serif=True),
  "sunset": dict(  # 落日橘粉
    dark=False, base="#fff0e8", blobs=["#ffae94", "#ffd59a", "#ff9cbf", "#ffc4a3", "#ffe3c2"],
    frame="rgba(255,255,255,.84)", frame_line="#ffffff", card="linear-gradient(165deg,#ffffff,#fff6f1)",
    card_line="rgba(200,80,50,.14)", tile="#fff4ee", tile_line="rgba(230,100,70,.20)",
    ink="#24110c", sub="#6b5049", muted="#a68a82", accent="#ff4f2e", accent2="#ff2d78", on_accent="#ffffff",
    warm="#fff1d6", warm_line="#f4d29a", shadow="160,60,40",
    hl=["grad", "marker"], cap=["pill", "plain"], pattern=["none", "dots"], serif=False),
  "graphite": dict(  # 石墨 · 荧光绿
    dark=True, base="#0f1012", blobs=["#2b2e35", "#1d2b19", "#33302a", "#202630", "#262a22"],
    frame="rgba(26,28,32,.90)", frame_line="rgba(255,255,255,.08)", card="linear-gradient(160deg,#1d1f24,#16181c)",
    card_line="rgba(255,255,255,.08)", tile="rgba(255,255,255,.04)", tile_line="rgba(255,255,255,.10)",
    ink="#f3f3ee", sub="#a5a8a0", muted="#6c6f68", accent="#c8f53a", accent2="#7dd3fc", on_accent="#121400",
    warm="rgba(200,245,58,.08)", warm_line="rgba(200,245,58,.35)", shadow="0,0,0",
    hl=["ink", "marker"], cap=["bar", "plain"], pattern=["grid", "none"], serif=False),
  "ocean": dict(  # 深海蓝 · 清透
    dark=False, base="#e7f0ff", blobs=["#a6c6ff", "#b5efff", "#c5cfff", "#9fe0ff", "#dbe8ff"],
    frame="rgba(255,255,255,.84)", frame_line="#ffffff", card="linear-gradient(170deg,#ffffff,#f2f7ff)",
    card_line="rgba(20,80,200,.14)", tile="#eef4ff", tile_line="rgba(30,100,240,.18)",
    ink="#0a1a33", sub="#4b5d7a", muted="#8797b0", accent="#0b63ff", accent2="#00b8f0", on_accent="#ffffff",
    warm="#fff4e0", warm_line="#f0d6a6", shadow="20,60,160",
    hl=["marker", "grad"], cap=["plain", "pill", "under"], pattern=["none", "dots", "grid"], serif=False),
}
