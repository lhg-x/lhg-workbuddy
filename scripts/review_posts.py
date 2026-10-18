# /// script
# requires-python = ">=3.10"
# ///
"""发布复盘（规则见 playbook/rules.md R2-R5）。用法：uv run scripts/review_posts.py data/posts.csv"""
import argparse, csv, statistics
from datetime import datetime


def f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return 0.0


def hrs(r):
    try:
        return (datetime.fromisoformat(r["checked_at"]) - datetime.fromisoformat(r["published_at"])).total_seconds() / 3600
    except Exception:
        return None


def tier(p):
    return "权重低" if p < 10 else "待观察" if p < 1000 else "正常"


def doujia(p, h):
    if h is None:
        return "-"
    if h <= 1 and p >= 10000:
        return "立刻投"
    if h <= 6 and p >= 30000:
        return "可试投"
    return "不投"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    rows = list(csv.DictReader(open(ap.parse_args().csv, encoding="utf-8")))
    if not rows:
        print("暂无数据"); return
    med = statistics.median(f(r["plays"]) for r in rows)
    print("标题 | 播放 | 小时 | 层级 | 抖加 | 赞率 | 转率 | 藏率 | 隐藏?")
    for r in rows:
        p, h = f(r["plays"]), hrs(r)
        rate = lambda k: f"{f(r[k]) / p * 100:.1f}%" if p else "-"
        hide = "建议隐藏" if len(rows) >= 10 and (p < 1000 or p < med * 0.1) and r.get("status") != "hidden" else ""
        print(f"{r['title'][:20]} | {p:.0f} | {h and round(h, 1)} | {tier(p)} | {doujia(p, h)} | "
              f"{rate('likes')} | {rate('shares')} | {rate('favorites')} | {hide}")
    recent = [f(r["plays"]) for r in rows[-10:]]
    if len(recent) >= 5 and max(recent) < 1000:
        print("\n⚠ 触发废号条件（近 5–10 条均 <1000）：先跑 playbook/weilanx-sop.md 第 9 步自查清单，再决定注销；注销后冷却 ≥48h。")


if __name__ == "__main__":
    main()
