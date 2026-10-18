---
name: post-review
description: 发布复盘。根据我的发布数据做 6 小时诊断、抖加决策、隐藏建议、废号判断，并计算后台比率、提炼结论写回规则库。用户说"看看数据""要不要投抖加""要不要隐藏""这个号还能救吗"时使用。
---

# post-review

## 输入
- `data/posts.csv`（用户贴截图时先读数填表）。字段：
  `post_id,published_at,checked_at,title,topic,anchor_word,benchmark_url,plays,likes,comments,shares,favorites,completion_5s,bounce_2s,avg_watch_s,duration_s,dou_plus_cny,status`

## 流程
1. 运行：`uv run scripts/review_posts.py data/posts.csv`
2. 对每条给出：层级（R2）、抖加建议（R3）、是否隐藏（R4）。
3. 账号层面：是否触发废号条件（R5）→ 触发则先输出自查清单逐项问用户。
4. **比率对比**：累计 ≥ 10 条后，按 topic / 标题句式 / 锚词分组比较 分享率、5s 完播、2s 跳出，找差异最大的因素。
5. **写回规则**：只有在样本 ≥ 5 且差异明显时，写入 `playbook/rules.md` 的"我的数据结论"，格式 `- [日期][n=] 结论 —— 依据`；样本不足写"相关，待验证"。
6. 更新 `account/profile.md` 锚词库的播放列。

## 输出
一张表 + 3 条以内的下一步动作（发什么、隐藏什么、投不投）。
