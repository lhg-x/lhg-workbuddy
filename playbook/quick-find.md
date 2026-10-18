# 对标速查卡（30 分钟出一个可做选题）

> 下次找对标时，从上到下照做即可。阈值以 `rules.md` 为准。

## ⏱ 0–10 分钟：找
- [ ] 抖音搜 `#Vibe知识大赏` → 话题 → **最新**（不是最热）
- [ ] 也搜 1–2 个自己方向关键词（如"AI 工具""思维模型"）→ 筛选：最多点赞 + 一天内
- [ ] 每条候选只看 4 个数：**发布几小时 / 播放 / 点赞 / 分享**
- [ ] 入选信号（满足 ≥3 条）：
  - 发布 ≤ 6h 且播放 ≥ 3000
  - 账号粉丝 < 1 万
  - 分享 ≥ 点赞
  - 评论区在吵
  - 有能画出来的载体
- [ ] 截图或链接发给 Claude → 入 `data/benchmarks.csv` → `score_benchmark.py`

## ⏱ 10–15 分钟：判号
- [ ] 点进 S/A 级视频的主页，按 `teardown-method.md §1` 速看：主力题材、播放分布、系列化、粉丝
- [ ] 一句话结论：这个号靠什么活？能抄什么？

## ⏱ 15–30 分钟：拆片
- [ ] 下载无水印原片 → `template/`
- [ ] `uv run scripts/analyze_video.py template/x.mp4 --out teardowns/<日期>-<slug>`
- [ ] 判节奏骨架类型（元素进出 / 剪辑 / 安静+爆点）
- [ ] 联系表分画面类别 → 列组件清单
- [ ] 招牌时刻切片：`uv run scripts/strip.py template/x.mp4 --at <秒> --span 0.6 --n 12 --out ...`
- [ ] 填 `templates/teardown-report.md`：为什么爆 / 结构时间线 / 配方卡 / 没搬的 / 超越点 / 我的版本

## 输出给生产线
- 标题草案（≤20 字、第二人称 + 痛点、不给答案）
- 锚词 + 两个高潮位置
- 走哪条线：火柴人 `lhg-stickman-director` / 手绘费曼 `lhg-feynman-teach`
