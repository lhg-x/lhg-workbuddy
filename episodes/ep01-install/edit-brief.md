# 第1课 成片任务书 v2（给 Antigravity）

> v1 理解错了，作废。正确理解如下：

## 0. 这条片子长什么样
- 成片 = **卡片视频**（3:4，1080×1440），不是直接剪原片。
- 每一段画面二选一：
  - **A 卡片页**：讲道理、讲安排的段落 → 用 `scripts/render_canvas.py` 出卡片 PNG（格式见 `templates/canvas/README.md`、示例 `templates/canvas/example.json`）。
  - **B 录屏页**：讲操作的段落 → 卡片里挖出 16:10 录屏框（输出像素 `x=108, y=243, 864×540`，带主题色描边），框里放 WorkBuddy 真实操作录屏，用 `scripts/zoom_follow.py` 跟随点击放大。
- 左下圆形头像窗：放 `Area.mp4` 右下角露脸画面裁成的圆（嘴型与口播同源）；以后可换成即梦数字人视频。
- **声音**：全片只用 lhg 的口播。
- 参考稿：`episodes/ep01-install/script.md`；录屏规范：`playbook/recording-sop.md`；样片参数参考：`episodes/ep01-install/sample/`。

## 1. 处理 `/Users/kanshan28/Movies/wb/ep01/Area.mp4`（只读，不覆盖）
工作目录 `~/Movies/wb/ep01/edit/`。
1. `ffprobe` 看时长/分辨率；每 10 秒抽 1 帧拼 `contact.jpg`。
2. **音频**：导出为口播母带。去掉说错、重复的句子（同一句保留最后一遍完整的），句间静音 > 0.6s 压到 0.25s，切点落在词之间，20ms 淡入淡出 → `narration_master.wav`。
3. 转写母带（Apple 芯片优先 mlx-whisper large-v3-turbo，否则 faster-whisper；zh；词级时间戳），按 script.md 的段落切分 → `segments.json`：`[{id, title, start, end, text, type: "A"|"B"}]`。
4. **原片画面**（不露脸的录屏部分）：逐段判断能不能直接当 B 页素材（清晰、操作完整、没露隐私）。能用的记到 `segments.json` 的 `src`；不能用或缺的，进第 2 步补录。
5. **先汇报**：发 `contact.jpg` + `segments.json` 摘要（每段时长、A/B、素材来源）给 lhg，确认后再往下做。

## 2. 去 WorkBuddy 真实操作补录 B 页（按 recording-sop.md）
每个镜头单独录：`shots/<id>.mov` + `shots/<id>.jsonl` 时间轴（`{t, shot, action, x, y, label, zoom}`），光标慢速移动（0.7s 缓动），每步停 1.5s。

| 段落 | 要录的操作 | 备注 |
|---|---|---|
| 下载 | 浏览器搜 WorkBuddy → 进官方网站（codebuddy.cn/work）→ 悬停「下载 WorkBuddy」 | 用官方站，不点山寨站 |
| Mac 安装 | 打开安装包 → 把图标拖向「应用程序」 | 已安装会弹「替换」→ **停，问 lhg**；也可只录拖拽过程不松手 |
| Windows 安装 | 无 Windows 电脑 → 改成 A 卡片页（三步：双击 → 下一步 → 核对发布者） | 不录 |
| 登录 | 原片有就用原片；没有就**停，交给 lhg** 扫码 | 二维码、手机号必须打码 |
| 界面 | 光标依次悬停左侧任务栏 → 中间输入框 → 右侧结果区，各停 1.5s | 以实际界面名称为准，记录到 jsonl |
| 第一次对话 | 新建任务 → 选桌面「练习-第1课」文件夹 → 输入 script.md 里的演示指令 → 发送 → 等生成 → 右侧结果区打开 Excel | 等待段后期加速；找不到对应按钮就截图问 lhg，不要猜 |

功能名称、按钮位置**以 lhg 电脑上 WorkBuddy 实际界面为准**；和 script.md 对不上的，记到 `report.md`。


## 2.5 录屏的「放大 + 高亮框」规范（必须遵守）
目的：讲到哪个功能，观众眼睛立刻落在哪个按钮上。
1. **录屏框描边**：B 页录屏框外圈一道主题色渐变描边（accent → accent2，带光晕），render_canvas.py 已内置；**只加在录屏框上**，头像圆框不加。
2. **每讲一个功能 = 一个事件**，时间轴每行除了 `{t, shot, action, x, y, label}`，**必须加 `box: [x, y, w, h]`**（pt，屏幕坐标，含刘海；就是被讲的那个按钮 / 菜单项 / 输入框的外框）。获取方式：录完对关键帧截图量出来，或用辅助功能读控件位置；量不准宁可框大一点。
3. **镜头**：`scripts/zoom_highlight.py` 读 `events.jsonl`（`{t: 成片秒, box, zoom}`），在 t 开始 0.6s 平滑放大到 box 中心；单个按钮 zoom 2.0–2.2，一整块区域（侧边栏、输入框）1.6–1.9；讲完一组回全景 `{"box":null,"zoom":1}`。
4. **高亮框**：镜头到位后 0.25s 弹出圆角框（主题主色 accent，3px 实线 + 柔光晕，比 box 外扩 6pt，从 1.12 倍缩到 1.0 倍并淡入），停到下一个事件，0.2s 淡出。
5. **对齐口播**：事件 t 对齐到口播里说出这个功能名的那个词（用词级时间戳），比如说到「新建任务」时框住「新建任务」。光标也要在该按钮上或附近。
6. 用法：`python3 scripts/zoom_highlight.py raw.mov events.jsonl scr.mp4 <原片起点秒> <时长秒> <accent色>` → 864×540，放到卡片录屏框 (108,243)。

## 3. 合成
1. **卡片**：每段写 `cards/<id>.json` → `render_canvas.py` 出 PNG（B 页用 screen 页型，录屏框透明）；同一条片子固定一个主题和 seed。
2. **B 页画面**：`zoom_highlight.py`（自动裁顶部 38pt 刘海黑条）出 864×540，带放大和高亮框 → 放到卡片底下的录屏框位置，上面叠卡片 PNG。
3. **时长对齐口播**：每页时长 = 该段口播时长。录屏偏长 → 加速（≤4 倍）或剪掉等待；偏短 → 定格最后一帧。
4. 头像圆窗放静态照片 #16；底部字幕用卡片自带字幕位或另烧录（每行 ≤14 字，按 script.md 校对，专有名词写 WorkBuddy）。
5. 音频 = `narration_master.wav`，可垫很轻的背景音乐（-28dB 左右）。
6. 输出 `ep01_v1.mp4`（1080×1440，30fps，H.264 CRF 18，AAC 192k）+ `subs.srt`。

## 4. 交付与边界
- 交付到 `~/Movies/wb/ep01/edit/`：`ep01_v1.mp4`、`segments.json`、`cards/`、`shots/`、`subs.srt`、`report.md`（时长、各段素材来源、需要 lhg 确认的点）。
- 不发布；不改原片；不改口播内容；不加 AI 配音。
- 遇到登录、付费、权限弹窗、隐私授权 → 停，交给 lhg。
