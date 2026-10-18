---
name: benchmark-finder
description: 对标发现。按"最新、已爆、小号也爆、能画出来、评论有争议"标准寻找并评估对标视频与对标账号，入池 data/benchmarks.csv 并打分排序。用户说"帮我找对标""这条值不值得跟""找同类号"时使用。
---

# benchmark-finder

## 两种对标
1. **对标视频**（每天找）：用来复刻选题与结构。
2. **对标账号**（起号时找 3–5 个）：用来抄包装（名字/头像/简介）和长期观察更新节奏、系列选题。

## 找对标视频
1. 入口优先级：
   1. `#Vibe知识大赏` 话题 → **最新**
   2. 关键词搜索 → 筛选"最多点赞 + 一天内"
   3. 对标账号主页最新作品
   4. `trend-radar` 给出的选题关键词
2. 对每条候选记录（用户提供截图/链接时从中读取）：
   `url, title, account, followers, published_at, checked_at, plays, likes, comments, shares, favorites, drawable(0-3), controversy(0-3), notes`
3. 追加到 `data/benchmarks.csv`，运行：
   ```bash
   uv run scripts/score_benchmark.py data/benchmarks.csv --top 10
   ```
4. 解读分数（规则见 `playbook/rules.md#R1`）：
   - **S（≥80）**：立即下载拆解 → `benchmark-distill`
   - **A（60–79）**：今天内做
   - **B（40–59）**：观察，6h 后复查数据
   - **C（<40）**：放弃
5. 对 S/A 级写一句"为什么爆"假设：选题钩子 / 争议点 / 情绪（替自己说话？涨知识？反常识？）。

## 找对标账号
- 搜 `#Vibe知识大赏` → 最多点赞 + 一周内 → 进主页。
- 记录：名字、头像风格、简介、粉丝、近 10 条播放分布、更新频率、主力风格。
- 写进 `benchmarks/accounts.md`，标出"可抄包装要素"。

## 注意
- 抖音数据不能直接爬时，让用户贴截图或分享链接，从图里读数字；数字必须标 `checked_at`，因为速度比总量更重要。
- 下载的原片只放 `template/`，不入库。
