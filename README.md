# lhg-viral-lab

短视频起号实验室。目标：**快速找到自己的对标 → 把对标拆透 → 盯住热点 → 用数据反哺选题**，服务 Liu Keep 的账号（AI 工具科普 / 火柴人 / 手绘费曼视频）。

方法论主要吸收自 @蔚蓝WEILANX 的《Opus 5.5 抖音起号超级保姆级教程》（2026-10-18），并改造成可被 Claude Code 直接调用的 Skill。

## 核心闭环

```
热点雷达(trend-radar) ─┐
                      ├─► 对标发现(benchmark-finder) ─► 对标拆解(benchmark-distill) ─► 制作
账号定位(account/) ────┘                                                        │
        ▲                                                                      ▼
        └──────────── 数据复盘(post-review)：结论写回 playbook/rules.md ◄──── 发布
```

## 目录

| 路径 | 内容 |
| --- | --- |
| `playbook/weilanx-sop.md` | 原文学习笔记：账号完整生命周期 9 步 |
| `playbook/teardown-method.md` | **拆解方法论**：账号层 → 视频层 → 画面语法层 |
| `playbook/quick-find.md` | **对标速查卡**：30 分钟从找到拆出一个可做选题 |
| `playbook/rules.md` | **可执行规则库**（阈值、判断标准），随数据不断更新 |
| `account/profile.md` | 我的账号定位、标签、锚词库 |
| `skills/trend-radar/` | 热点雷达：每日扫描热点 → 可画选题 |
| `skills/benchmark-finder/` | 对标发现：找"最新 + 已爆 + 小号也爆"的视频并打分 |
| `skills/account-teardown/` | 对标账号拆解：包装/作品矩阵/Top3 → 跟不跟、抄什么 |
| `skills/benchmark-distill/` | 对标拆解：机器拆 + 人眼拆 → 风格配方卡 |
| `skills/post-review/` | 发布复盘：6 小时诊断 + 后台比率分析 |
| `scripts/analyze_video.py` | 视频机器拆解脚本（镜头表/运动/色板/联系表/响度/节拍） |
| `scripts/strip.py` | 动效切片：数入场/转场帧数、判断缓动 |
| `scripts/score_benchmark.py` | 对标打分 |
| `scripts/review_posts.py` | 帖子数据比率计算 + 层级诊断 |
| `data/benchmarks.csv` | 对标池 |
| `data/posts.csv` | 我的发布记录 |
| `teardowns/` | 每条对标的拆解报告 |
| `template/` | 下载的参考视频（**不入库**，仅本地学习） |

## 快速开始

```bash
brew install ffmpeg uv
# 拆解一条对标
uv run scripts/analyze_video.py template/xxx.mp4 --out teardowns/2026-10-18-xxx
# 打分对标池
uv run scripts/score_benchmark.py data/benchmarks.csv
# 复盘发布数据
uv run scripts/review_posts.py data/posts.csv
```

在仓库里打开 Claude Code，它会读取 `CLAUDE.md` 和 `skills/`。

## 版权边界

- 参考视频只用于拆解学习，放 `template/`，已在 `.gitignore` 中排除。
- 学：选题、结构节奏、画面语法、音乐调性。不搬：原文案、字幕、水印、原配乐、创作者素材。
