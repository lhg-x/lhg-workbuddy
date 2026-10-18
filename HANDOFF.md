# 工作交接：WorkBuddy 抖音对标 + leviiii2026 画布拆解（2026-10-19）

> 给 Claude：数据采集已全部做完，你直接从"三、待办"开始干杂活，不用重复扒数据。
> 仓库：`lhg-skills/lhg-viral-lab`（本目录）。用户战略：workbuddy 免费内容引流涨粉 → 进阶付费视频，围绕 AI 讲。

## 一、数据清单（全部在仓库内，除视频文件外均可提交 GitHub）

| 内容 | 路径 | 规模 |
| --- | --- | --- |
| workbuddy 视频元数据（去重） | `data/raw-2026-10-19/video_pool_dedup.json` | 120 条（赞/评/转/藏/作者/文案/话题/播放地址） |
| 同上 CSV | `data/raw-2026-10-19/video_pool.csv` | 120 条 |
| 账号画像 | `data/raw-2026-10-19/users.csv` | 75 个账号（昵称/抖音号/粉丝/签名） |
| 各关键词原始 JSON | `data/raw-2026-10-19/video_*.json` | 8 个文件 |
| workbuddy 视频文件 | `template/workbuddy-2026-10-19/` | 53 条 mp4（.gitignore，不提交） |
| workbuddy 对标报告（账号层） | `teardowns/2026-10-19-workbuddy/report.md` | 核心结论见下 |
| workbuddy 文稿（发布文案+数据） | `teardowns/2026-10-19-workbuddy/transcripts/<id>.md` | 51 份 |
| workbuddy 展示形式抽帧 | `teardowns/2026-10-19-workbuddy/formats/<id>_<作者>/` | Top6 作者各 3 帧 |
| leviiii2026 视频详情 JSON | `data/raw-2026-10-19-leviiii2026/detail_*.json` | 4 条 |
| leviiii2026 视频文件 | `template/leviiii2026_<id>.mp4` | 4 条（.gitignore） |
| leviiii2026 全量分析 | `teardowns/2026-10-19-leviiii2026/va_<id>/`（抽帧/头像裁剪/音频/wav）+ `videos_analysis.json` | 4 条 |
| leviiii2026 画布拆解+复现指南 | `teardowns/2026-10-19-leviiii2026/report.md` | 完整版式规格 |
| leviiii2026 文稿 | `teardowns/2026-10-19-leviiii2026/transcripts/<id>.md` | 4 份 |
| 对标账号池 | `benchmarks/accounts.md`（已追加 4 个号） | |
| 对标视频池 | `data/benchmarks.csv`（已追加 20 条） | |

## 二、已确认的结论（不用重做）

### workbuddy 对标（账号层）
- 核心对标：**小k的AI日记**（抖音号 28555886949，3.2 万粉），"一天一个workbuddy小技巧"日更到 32 期（18:00–21:00）
- 爆款公式：白嫖利益（第9期自动领积分 21551赞）/ 清单排名（第12期必装8个skill 10363赞）/ 自动＿（第31期自动剪辑 7221赞）；工具教程收藏≈点赞（0.9+）、分享率 20%+
- 生态：大V偶发爆款（珍妮丁丁说 24.9万赞）破圈 + 垂直小号（小羊-workbuddy、张瑞麟AI、Neil的AI笔记…）吃长尾
- 展示形式：**录屏演示 + 底部大字幕** 为主，珍妮丁丁说加了真人小窗（右下）

### leviiii2026 画布（用户要复用的格式）
- 3:4 画布：伪 App 导航栏（每期换主题）+ 编号徽章 + 黑蓝撞色大标题 + 数据子卡片 + 右上页码 + **左下圆形出镜窗** + 底部大字幕；5–9 页/条，6–7 秒一页
- 出镜+声音：**照片驱动 talking head + 克隆声**（4 条音频全部 0 停顿；头像 28 秒头部不动只有嘴动）
- 复现路线：用户真人出镜（10 秒）+ 1 分钟干声克隆 → PPT 画布模板 → 剪映合成；抖音 AI 生成内容须显著标识

## 三、待办（Claude 按顺序做）

1. **口播转写**：55 份 transcripts 的"口播文稿"节是空的。装 faster-whisper，转写 `template/` 下对应 mp4 的音频后填入（leviiii2026 的 4 条 wav 已在 `va_<id>/audio.wav`）
2. **画面层深拆**：对 workbuddy Top 视频跑 `scripts/analyze_video.py`（镜头表/色板/运动曲线），重点看小k第9期、珍妮丁丁说、小羊-workbuddy；输出风格配方卡
3. **画布 HTML 模板**：按 `teardowns/2026-10-19-leviiii2026/report.md` §1 的版式规格，做一个填文案即出 5 页卡片的模板（可复用 vibe 产线的 render.py 思路）
4. **出镜+声音 pipeline**：等用户提供 10 秒出镜视频 + 1 分钟干声后，跑通"声音克隆（GPT-SoVITS/CosyVoice/MiniMax）+ talking head（HeyGen/D-ID/剪映数字人）"第一条 workbuddy 样片
5. **选题库**：基于 `data/raw-2026-10-19/video_pool.csv` 按"白嫖/清单/自动＿/场景化"四类整理 30 个免费层选题 + 5 个付费课大纲（散点 vs 体系切分）

## 四、环境与坑（必读）

- 沙盒出网必须走代理：`proxy = os.environ.get("https_proxy")`（密码轮换，勿写死）；`DouyinSearch(proxy=...)`，请求间隔 ≥1.5s
- 抖音搜索 API（`lhg-douyin-get` skill）**刷不出小号自己的作品**；单视频详情走 `https://aweme.snssdk.com/aweme/v1/feed/?aweme_id=<id>`（免签名）；作者作品列表/网页端需登录签名——这是留给你的硬骨头
- `custom.github` 连接器里的 token 已失效；GitHub 操作走 `~/.config/x-tech-posts/gh-pat`（`GH_TOKEN=$(cat ...)`），推送前按惯例跟用户打招呼
- `template/` 在 .gitignore 中：视频文件不进仓库是**设计如此**（345MB+），只提交数据/文档/代码
- leviiii2026 网页端显示"用户不存在"（短链/APP 端正常），不要在这上面浪费时间
