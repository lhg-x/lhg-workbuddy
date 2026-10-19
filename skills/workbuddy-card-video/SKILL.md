---
name: workbuddy-card-video
description: 把 lhg 的真人口播录像（含露脸小窗）+ WorkBuddy 实操录屏，合成为「lhg·AI实验室」3:4 卡片讲解视频。用于每一课的录屏、剪辑、合成。
---

# 卡片讲解视频（lhg·AI实验室）

## 成片长什么样（不可改的版式）
- 画布 3:4，1080×1440，30fps。同一条片子固定一个主题 `theme` + `seed`；**不同课换主题**（`render_canvas.py --list-themes`）。
- 顶栏：W 图标 + WorkBuddy + 「从零上手 · 第 N 课」+ 右侧标签。
- 中间两种页，按口播段落来回切：
  - **A 卡片页**：讲道理/安排/总结 → 大标题、金句、要点卡（`big`/`list`/`steps`/`stats`/`compare`/`cta` 页型）。
  - **B 录屏页**：讲操作 → 16:10 录屏框（864×540 @ 108,243），**框外主题色渐变描边 + 光晕**（模板内置，只加在录屏框上）。框下「STEP N + 标题 + 实操演示」。
- 左下圆形头像窗：lhg 口播原片里的**露脸画面裁圆**（嘴型与声音同源）；下挂「lhg·AI实验室」名牌。头像圆框不加描边。
- 右侧：小标题、图标、两行重点、补充说明、页码「当前段 / 总段数」。
- 底部黄底字幕条，`[关键词]` 高亮，**按口播逐句切换**。
- 声音：只用 lhg 的口播。卡片上不放 AI 标识（发布时勾选）。

## 文案规矩（抖音 + 视频号双平台）
不提其他平台名（微信等）、不念网址、不放链接或联系方式、不用绝对化/承诺类说法（最、第一、保证、放心、免费送）。专有名词统一：WorkBuddy、Mac、Windows、Excel。

## 流程
### 1. 拆口播原片（只读，不覆盖）
1. `ffprobe` 看分辨率；截一帧，量出露脸小窗里**脸居中的正方形** → `cam_crop: [x, y, 边长]`（原片像素，留出头顶）。
2. 转写（Apple 芯片用 mlx-whisper large-v3-turbo，否则 faster-whisper；zh；**词级时间戳**）。
3. 按课程稿 `episodes/epXX/script.md` 切段：每段 `src_start/src_end` 落在词与词之间。说错/重复的句子只保留最后一遍完整的（不选进任何段即可）。
4. 每段定 A/B 页，写字幕（一句一条，`t` = 该句在段内的起始秒，≤14 字/行）。
5. **先把段落表发给 lhg 确认**，再录屏。

### 2. 录 WorkBuddy 实操（B 页素材）
- Antigravity 在 lhg 的 Mac 上：`screencapture -V <秒> -C <文件>.mov`（需屏幕录制权限；不要中途 kill，会丢文件）。一个镜头一个文件，录前退出无关窗口。
- 光标像真人：每次移动 0.7s 缓动（easeInOutQuad），每步停 1.5s。Retina 坐标：截图像素 ÷ 2 = pt。
- **按钮名称、位置以 lhg 电脑上的实际界面为准**；找不到就截图问 lhg，不许猜。
- 讲到哪个功能，光标就停在哪个按钮上；时长按对应口播段落留足（可多录，后期裁）。
- 必须停下交给 lhg：登录扫码、付费、隐私授权、「替换已安装应用」等弹窗。
- 每个镜头写 `events.jsonl`（见下），`box` 是被讲的那个按钮/菜单/输入框的外框（pt，屏幕坐标，含刘海区）；对关键帧截图量出来，量不准宁可框大一点。

### 3. 放大 + 高亮框（`scripts/zoom_highlight.py`，自动处理）
- 自动裁掉顶部 38pt 刘海黑条。
- 事件 t 开始，0.6s 平滑移镜放大到 box 中心：**单个按钮 zoom 2.0–2.2，一整块区域 1.6–1.9**；讲完一组 `{"box":null,"zoom":1}` 回全景。
- 镜头到位后 0.25s 弹出圆角高亮框：主题主色、3px 实线 + 柔光晕、外扩 6pt、1.12→1.0 倍缩入并淡入；停到下一事件，0.2s 淡出。
- **事件 t 对齐口播里说出功能名的那个词**（段内秒）。

### 4. 合成
```
python3 scripts/compose_card_video.py <segments.json> --out ~/Movies/wb/epXX/edit [--only id1,id2]
```
先用 `--only` 出 1–2 段给 lhg 看，确认后再全片。依赖：ffmpeg、Chrome/Chromium（渲染卡片）、python3 + numpy + opencv。

### 5. 交付 `~/Movies/wb/epXX/edit/`
成片 mp4、`segments.json`、各镜头 `.mov` + `events.jsonl`、`report.md`（总时长、每段素材来源、对不上稿子的地方、需 lhg 确认的点）。不发布、不改原片、不改口播内容、不加 AI 配音。

## segments.json 格式（示例：`segments.example.json`）
```json
{"source": "Area.mp4", "cam_crop": [1105, 744, 280], "theme": "mint", "seed": 7, "output": "ep01_v1.mp4",
 "host": "lhg·AI实验室", "nav": {"logo": "W", "brand": "WorkBuddy", "topic": "从零上手 · 第 01 课", "tabs": ["为什么", "安装", "实操"]},
 "segments": [
  {"id": "hook", "type": "A", "src_start": 9.1, "src_end": 20.3,
   "page": {"type": "big", "badge": "开场", "title": "…", "quote": "…[高亮]…", "note": "…", "side": {"kicker": "…", "icon": "user", "headline": "…\n…", "sub": "…"}},
   "captions": [{"t": 0, "text": "AI 现在已经能 [帮人干活] 了"}, {"t": 2.46, "text": "…"}]},
  {"id": "ui", "type": "B", "src_start": 91.9, "src_end": 102.7,
   "page": {"title": "认识主界面", "subtitle": "实操演示", "screen": {"url": "WorkBuddy · 主界面", "step": "STEP 3"}, "side": {…}},
   "screen": {"raw": "shots/ui.mov", "raw_start": 5.0, "events": "shots/ui.events.jsonl"},
   "captions": [{"t": 0, "text": "进来的界面 [就三块]"}, {"t": 9.1, "text": "点 [新建任务]"}]}
 ]}
```
- 路径相对 segments.json 所在目录（可用 `~`）。`raw_start` = 录屏里从第几秒开始用；录屏长度需 ≥ 段时长。
- `events.jsonl` 每行：`{"t": 段内秒, "box": [x, y, w, h] 或 null, "zoom": 倍数}`。
- 页型字段参考 `templates/canvas/README.md`、`templates/canvas/example.json`。

## 自检清单（交付前逐条过）
- [ ] 每段开头结尾没有半个字、没有爆音
- [ ] 字幕与口播同步，没有错字，没有敏感词
- [ ] 高亮框出现时，口播正好说到该功能，光标也在该按钮上
- [ ] 录屏没有露出二维码、手机号、头像昵称、其他平台图标（有就打码）
- [ ] 头像圆窗里脸居中、头顶不被切
