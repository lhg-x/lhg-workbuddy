# /// script
# requires-python = ">=3.10"
# ///
"""对标打分（规则见 playbook/rules.md R1）。用法：uv run scripts/score_benchmark.py data/benchmarks.csv --top 10"""
import argparse, csv
from datetime import datetime


def f(x, d=0.0):
    try:
        return float(x)
    except (TypeError, ValueError):
        return d


def hours(a, b):
    try:
        return max(0.1, (datetime.fromisoformat(b) - datetime.fromisoformat(a)).total_seconds() / 3600)
    except Exception:
        return None


def score(r):
    plays, likes = f(r["plays"]), f(r["likes"])
    h = hours(r["published_at"], r["checked_at"])
    s, why = 0, []
    if h is not None:
        vel = plays / h
        s += 30 if vel >= 5000 else 22 if vel >= 1000 else 12 if vel >= 300 else 0
        s += 10 if h <= 6 else 6 if h <= 24 else 0 if h <= 72 else -15
        why.append(f"{h:.1f}h {vel:.0f}播/h")
    s += 10 if plays >= 10000 else 6 if plays >= 3000 else 0
    fol = f(r["followers"], -1)
    if 0 <= fol < 10000:
        s += 10; why.append("小号也爆")
    if likes > 0:
        sr, cr = f(r["shares"]) / likes, f(r["comments"]) / likes
        s += 15 if sr >= 1 else 8 if sr >= 0.3 else 0
        s += 5 if cr >= 0.05 else 0
        why.append(f"转/赞{sr:.2f} 评/赞{cr:.2f}")
    s += int(f(r["drawable"])) * 4 + int(f(r["controversy"])) * 3
    s = max(0, min(100, s))
    grade = "S" if s >= 80 else "A" if s >= 60 else "B" if s >= 40 else "C"
    return s, grade, "; ".join(why)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--top", type=int, default=20)
    a = ap.parse_args()
    rows = list(csv.DictReader(open(a.csv, encoding="utf-8")))
    scored = sorted(((score(r), r) for r in rows), key=lambda x: -x[0][0])[: a.top]
    print(f"{'分':>3} 级  标题 | 依据")
    for (s, g, why), r in scored:
        print(f"{s:>3} {g}  {r['title'][:24]} | {why}")


if __name__ == "__main__":
    main()
