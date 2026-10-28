# 特辑 成片任务书：31740 技能普查（给剪辑/合成）

> 方法：lhg-x/lhg-workbuddy 的 skills/workbuddy-card-video。稿：script.md；段表：segments.json；分镜：shotlist.md。

## 0. 成片长什么样
- 3:4，1080×1440，30fps。主题 ocean、seed 3174 全片固定。
- 画面 = A 卡片页（cards-hole/ 挖洞版，左下圆窗放 lhg 口播露脸裁圆，名牌「Liu Lao Shi」）+ 全屏数据插入（图表 PNG / 动效 MP4，均为 1080×1440）。
- 本期没有 B 录屏页：全程数据解读，不演示操作。
- 声音只用 lhg 口播；字幕按 segments.json 的 captions（≤14 字/行，卡片自带字幕位或独立字幕轨）。

## 1. 物料（全部已生成，先验货再剪）
- 卡片：cards/ 13 页成品 + cards-hole/ 13 页挖洞版 + cards.json 源 + layout.json（圆窗/录屏框坐标在里面）。
- 静态图表：assets/charts/ 10 张（01 集中度 / 02 金字塔 / 03 僵尸环图 / 04 月度 / 05 分类 / 06 来源 / 07 Top20 / 08 平台赛道 / 09 同名停更 / 10 机会地图），数字全部由 CSV 现算，见《数据核验表.md》。
- 动效：assets/anim/ 6 条 MP4 + 同名 GIF 预览（00 数字滚动 3s / 01 集中度 / 02 华夫饼 / 03 月度 / 04 来源 / 05 Top10，各 4s，24fps，无声）。
- 图片：assets/img/cover-bg-data-ocean（AI 底图，无文字）+ cover-final-1080x1440.png（封面成品，发布封面直接用；卡片 page_01 是片内封面页，两者不要混）。
- 引流物：Top100必装清单+避坑清单.md（评论区扣「清单」后发放）。

## 2. 合成顺序
1. lhg 录口播原片 → 按 skill 流程：量 cam_crop、词级时间戳转写、按 segments.json 的段 id 切段，**用真实时间戳覆盖 segments.json 里的预估 src_start/src_end**。
2. 先跑 compose_card_video.py 出 A 卡主体（--only hook,zombie 两段先给 lhg 看）。
3. 全屏插入按 shotlist.md：在对应段的指定句子处，卡片段让位给动效 MP4（全屏播完 3–4s）→ 切同主题静态图停留到段尾 → 回卡片。插入期间口播与字幕不停。
4. 自检（照 skill 清单）：字幕同步无错字；数字与《数据核验表.md》逐个对；封面与标题一致；无其他平台名导流、无承诺类说法。

## 3. 本机渲染备注（重要，踩过）
- 本 VM 里 render_canvas.py 自带的 Chrome 截图不出图（meta-chromium headless 只退 0 不落 PNG）。已用替代路线产出成品：render_canvas.py --keep-html 留 HTML → Playwright(Chromium) 以 viewport 720×960、deviceScaleFactor 1.5 逐页截图 → 挖洞版再调用原脚本的 cut_holes 函数。本目录 cards/ 即此路线产物，尺寸 1080×1440 已核。
- 在 lhg 的 Mac 上跑原脚本无此问题（本地 Chrome 正常）。

## 4. 交付与边界
- 成片、segments.json（校准版）、report.md 回到本目录；不发布，发布由 lhg 本人操作。
- 稿中数字口径：数据截至 2026-10-26、非官方自采，片中方法段已声明，不要删。
