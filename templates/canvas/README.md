# 3:4 讲解卡片模板 v2

框架沿用 leviiii2026 的版式：**顶部导航条 / 主卡片 / 左下圆形出镜窗 / 右侧信息区 / 底部字幕**。
视觉是重新设计的，没有照搬参考号，也**不带"AI 生成"水印**（发布时在抖音勾选 AI 标识即可）。

## 一条命令出一期

```bash
python3 scripts/render_canvas.py templates/canvas/example.json --out out/ep07              # 随机抽一套视觉
python3 scripts/render_canvas.py <json> --out out/ep07 --seed 4821                          # 用同一个 seed 复现
python3 scripts/render_canvas.py <json> --out out/ep07 --theme paper                        # 锁定主题，其余仍随机
python3 scripts/render_canvas.py <json> --out out/ep07 --hole                               # 圆窗 + 录屏框挖透明，给剪映叠层
python3 scripts/render_canvas.py --list-themes
```

依赖：Python 3 + Pillow + Chrome/Chromium（macOS 装了 Chrome 就行）。输出 `page_01.png …`（1080×1440）+ `layout.json`。

## 每期都不重样

一期 = 一个 seed，期内所有页风格统一，期与期之间自动换。seed 决定：

| 维度 | 可选 |
| --- | --- |
| 主题 | aurora 冷紫极光 · mint 薄荷 · midnight 午夜霓虹（深色）· paper 纸本朱砂（宋体标题）· sunset 落日 · graphite 石墨荧光（深色）· ocean 深海蓝 |
| 标题高亮 | 纯色 / 渐变字 / 马克笔 / 下划线 / 发光（每个主题只开放适合它的几种） |
| 字幕 | 纯字 / 黄条 / 胶囊 / 下划线 / 发光 |
| 主卡片 | 实底 / 顶部色边 / 毛玻璃 / 错位投影 |
| 导航右侧 | 标签 / 搜索框 / 页码点 |
| 背景 | 4 团光斑随机位置 + 点阵 / 网格 / 横线纹理 + 胶片颗粒 |
| 角标装饰 | 描边大页码 / 同心环 / 光球 / 星芒 |

渲染完终端会打印本期组合，`layout.json` 里也有，喜欢哪期就记下 seed。想加主题：在 `themes.py` 里复制一段改颜色。

## 文案 JSON

见 `example.json`。全局字段：

- `host`：出镜窗下方的名牌（如"lhg·AI实验室"）
- `avatars`：照片列表（相对 JSON 的路径）。**按 seed 打乱后每页轮换一张**，不挖洞模式下直接嵌进圆窗；单页也可以写 `"avatar"` 指定
- `nav`：`logo` 单字、`brand`、`topic`（建议写"一天一个小技巧 · 第 N 期"做系列识别）、`tabs`
- `[词]` = 高亮；`\n` = 换行；`icon` 填 `icons.py` 里的名字（spark bolt gift clock coin check layers cursor chat rocket gear folder globe wand chart lock phone target book play star link cpu calendar video doc fire key heart arrow user skill）

每页都有 `side`（右侧：kicker / icon / headline / sub）和 `caption`（底部字幕）。页型：

| type | 用途 | 关键字段 |
| --- | --- | --- |
| `cover` | 封面 / 开头钩子 | `title` `subtitle` `chips` `hero`（右下大图标） |
| `stats` | 数据对比 | `stats: [{num, unit, label, icon, warm}]`，自动画比例条 |
| `list` | 清单（≤4 条/页，多了拆页） | `items: [{title, desc, icon, tag, warm}]` |
| `steps` | 步骤 | `steps: [{title, desc}]`（≤3） |
| `compare` | 前后 / A vs B | `compare: {left:{label,name,points}, right:{…}}`（右边是赢家） |
| `big` | 一句话 / 大数字 | `quote` 或 `number`+`unit`，`note` |
| `screen` | **B-roll 实操录屏框** | `title` `subtitle` `screen:{url, step}` |
| `cta` | 结尾评论钩子 | `cta:{lead, word, get, icon}` + 可选 `chips`（领什么） |

## A-roll / B-roll 怎么拼

你的结构：**卡片讲解（A-roll）↔ 实操录屏（B-roll）交替**，出镜窗里放几张照片随机轮换，配克隆声。

1. 写 JSON：讲概念的页用 cover / stats / list / steps / compare / big，要演示的地方插一页 `screen`
2. `--hole` 出图：圆窗和录屏框都是透明的
3. 剪映（或 ffmpeg）里三层：
   - 底层：照片轮换轨（每 2–4 秒换一张，加轻微推拉 / 交叉淡化），放在 `layout.json` → `cam_circle` 的位置；后面接 talking-head 时直接换成数字人视频
   - 中层：录屏素材，缩放到 `screen_rect`（只在 `screen` 页出现）
   - 顶层：卡片 PNG，按口播时长排
4. 录屏也可以整屏全屏播放（更清楚），切回卡片页时继续讲解 —— 两种节奏都行，建议 1 分钟内 A/B 交替 2–3 次
5. 不挖洞模式（不加 `--hole`）会把 `avatars` 直接烤进圆窗，适合做封面图 / 图文笔记

> 声音克隆 + 照片轮换的自动合成脚本放在后面做（等你的照片和干声）。
