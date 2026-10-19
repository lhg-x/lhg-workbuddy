# 录屏 SOP（给 Computer-Use Agent：Antigravity / Codex / ZCode）

> 用法：把本文件 + 某期 `episodes/epXX/shotlist.md` 一起发给 agent，说「按 SOP 执行这一期」。
> 分工：agent 操作 + 录屏 + 记时间轴；lhg 负责登录/扫码/付款/隐私；剪辑合成由 Notion AI 完成。

## 0. 环境（本机）
- MacBook，逻辑分辨率 **1470×956 pt**（截图像素 2940×1912，Retina ×2）。
  pyautogui / cliclick 用 **pt 坐标**；从截图量的像素坐标要 **÷2**。
- 已授权录屏：Screen Studio、Codex Computer Use、ZCode Computer Use、Antigravity（终端/Python）。

## 1. 录前准备（每期一次）
1. 关通知：开「勿扰模式」；关微信/邮件等弹窗应用。
2. WorkBuddy **真全屏**：`Ctrl+Cmd+F`（菜单栏、Dock 隐藏）。字体已调大，不要改。
3. 隐私：侧栏「空间」里无关项目先折叠；不要打开含个人信息的任务。
4. 录屏方式（二选一，默认 A）：
   - **A. Screen Studio**：录「Display」，60fps；开启 Auto zoom、光标平滑、点击高亮；隐藏 Dock。
   - **B. 系统录屏**：`screencapture -v -C -k ~/Movies/wb/epXX_raw.mov`（-C 带光标，-k 显示点击），Ctrl+C 结束。
5. 开始录制后等 2 秒再操作；结束前停 2 秒。

## 2. 操作节奏（最重要：像真人）
- 鼠标移动：`pyautogui.moveTo(x, y, duration=0.7, tween=pyautogui.easeInOutQuad)`，**禁止瞬移**。
- 点击前悬停 0.5s，点击后停 **1.5s**（给观众看结果 + 方便放大）。
- 输入文字：中文用剪贴板粘贴（`pbcopy` + `Cmd+V`）；英文 `pyautogui.write(s, interval=0.06)`。
- 等待 AI 生成：不要动鼠标，直到输出完成再继续。
- 每个分镜之间多停 1s，方便剪辑。
- 出错：不要慌乱补救，停 2s，记录 `"retake": true`，从该分镜重来。

## 3. 时间轴日志（必须）
录制开始时记 `t0 = time.time()`，每个动作追加一行到 `~/Movies/wb/epXX_timeline.jsonl`：
```json
{"t": 12.34, "shot": 3, "action": "click", "x": 735, "y": 478, "label": "点击 新建任务", "zoom": [600, 380, 900, 560]}
```
- `t`：相对 t0 秒；`x,y`：pt 坐标；`zoom`：建议放大区域 [x1,y1,x2,y2]（pt），可省略。
- action：`move / click / type / wait_start / wait_end / scroll / note / retake`。

## 4. 交付（每期）
放到 `~/Movies/wb/epXX/`：
- `epXX_raw.mov`（或 Screen Studio 导出的 mp4，1.54:1 原比例，不加背景/边框）
- `epXX_timeline.jsonl`
- `epXX_notes.md`：哪几镜需重录、遇到的界面变化/报错。
然后告诉 lhg「录完」，由 lhg 发给 Notion AI。

## 5. 必须停下交给 lhg 的情况
登录 / 扫码 / 验证码 / 付款 / 授权弹窗 / 出现个人隐私（手机号、路径里的用户名、聊天记录）/ 系统权限弹窗。
停下时：截图 + 在 notes 写明在第几镜。

## 6. 通用提示词（复制给 agent）
> 读取 recording-sop.md 和 episodes/epXX/shotlist.md。按 SOP 第 1 步准备，确认后开始录制，
> 逐镜执行分镜表「操作」列，严格遵守第 2 步节奏和第 3 步日志；遇第 5 步情况立即暂停叫我。
> 完成后按第 4 步交付。
