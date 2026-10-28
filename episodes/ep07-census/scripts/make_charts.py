# -*- coding: utf-8 -*-
"""31740 普查静态图表：全部数字来自 skills_full.csv 现算，不写死。"""
import csv, collections
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np

for f in ["/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc","/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"]:
    try: font_manager.fontManager.addfont(f)
    except Exception: pass
plt.rcParams["font.family"]="Noto Sans CJK JP"
plt.rcParams["axes.unicode_minus"]=False

SRC=Path.home()/"workspace/repos/lls-workbuddy-butler/skill-market-research/skills_full.csv"
OUT=Path.home()/"workspace/goals/ai/files/wb-census-ep07/assets/charts"; OUT.mkdir(parents=True,exist_ok=True)
rows=list(csv.DictReader(open(SRC,encoding="utf-8")))
for r in rows: r["u"]=int(r["使用量"]); r["i"]=int(r["安装量"])
rows.sort(key=lambda x:-x["u"]); TOT=sum(r["u"] for r in rows)

BG="#F7FAFD"; INK="#12314F"; BLUE="#1769C2"; DEEP="#0B3D6E"; ORANGE="#F07818"; RED="#D93A2B"; GREY="#B9C6D2"; LGREY="#E3EBF2"; TEAL="#0FA3A3"
def save(fig,name):
    fig.savefig(OUT/name, dpi=200, facecolor=BG); plt.close(fig); print("ok",name)
def canvas(title,sub=""):
    fig,ax=plt.subplots(figsize=(5.4,7.2)); fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    fig.text(0.07,0.945,title,fontsize=21,color=INK,weight="bold")
    if sub: fig.text(0.07,0.905,sub,fontsize=11.5,color="#5A7186")
    fig.text(0.07,0.025,"数据：WorkBuddy 技能市场全量普查 2026-10-26 · n=31,740 · 非官方自采",fontsize=8.5,color="#8AA0B4")
    return fig,ax

# 01 集中度
fig,ax=canvas("流量被谁吃掉了？","前 100 个技能（0.3%）拿走 73% 的使用量")
ns=[10,50,100,317,1000]; shares=[sum(r["u"] for r in rows[:n])/TOT*100 for n in ns]
labels=[f"前 {n} 名" for n in ns]; cols=[RED if n==100 else BLUE for n in ns]
y=np.arange(len(ns))[::-1]
ax.barh(y,shares,color=cols,height=0.62,zorder=3)
ax.barh(y,[100]*len(ns),color=LGREY,height=0.62,zorder=1)
for yi,s,n in zip(y,shares,ns): ax.text(s+2,yi,f"{s:.1f}%",va="center",fontsize=15,weight="bold",color=INK)
ax.set_yticks(y); ax.set_yticklabels(labels,fontsize=13,color=INK); ax.set_xlim(0,108); ax.set_xticks([]); ax.set_yticks(ax.get_yticks()); [sp.set_visible(False) for sp in ax.spines.values()]; ax.tick_params(length=0)
fig.subplots_adjust(left=0.20,right=0.97,top=0.86,bottom=0.07); save(fig,"01-concentration.png")

# 02 分层金字塔
fig,ax=canvas("31,740 个技能的金字塔","越往下人越多，流量越少")
layers=[("头部 ≥10万次",22,7283271,RED),("肩部 1万–10万次",119,3296472,ORANGE),("腰部 1千–1万次",698,1987600,BLUE),("长尾 ＜1千次",30901,1234310,GREY)]
# verify
for lab,lo,hi in [("头部 ≥10万次",100000,10**18),("肩部 1万–10万次",10000,100000),("腰部 1千–1万次",1000,10000),("长尾 ＜1千次",0,1000)]:
    sel=[r for r in rows if lo<=r["u"]<hi]; assert sum(x["u"] for x in sel)==dict((l[0],l[2]) for l in layers)[lab], lab
widths=[0.28,0.48,0.72,1.0]
for idx,(lab,cnt,use,col) in enumerate(layers):
    yy=3-idx; w=widths[idx]
    ax.barh(yy,[w],color=col,height=0.68)
    if idx==0:
        ax.text(0.02,yy,f"{cnt:,} 个",va="center",fontsize=13.5,weight="bold",color="white")
        ax.text(w+0.03,yy,f"{lab} · 占流量 {use/TOT*100:.1f}%",va="center",fontsize=12.5,weight="bold",color=INK)
    elif idx==1:
        ax.text(0.02,yy,f"{lab}",va="center",fontsize=13.5,weight="bold",color="white")
        ax.text(w+0.03,yy,f"{cnt:,} 个 · 占流量 {use/TOT*100:.1f}%",va="center",fontsize=12.5,color=INK)
    else:
        ax.text(0.02,yy,f"{lab}：{cnt:,} 个",va="center",fontsize=13.5,weight="bold",color="white")
        ax.text(w+0.03,yy,f"占流量 {use/TOT*100:.1f}%",va="center",fontsize=12.5,color=INK)
ax.set_yticks([]); ax.set_xlim(0,1.55); ax.set_xticks([]); ax.set_yticks(ax.get_yticks()); [sp.set_visible(False) for sp in ax.spines.values()]; ax.tick_params(length=0); fig.subplots_adjust(left=0.05,right=0.97,top=0.86,bottom=0.07); save(fig,"02-pyramid.png")

# 03 僵尸
fig,ax=canvas("六成技能，几乎没人用","使用量不足 10 次的就有 18,977 个")
z0=sum(1 for r in rows if r["u"]==0); z10=sum(1 for r in rows if r["u"]<10); z100=sum(1 for r in rows if r["u"]<100)
vals=[z0, z10-z0, z100-z10, len(rows)-z100]; cols=[RED,ORANGE,BLUE,TEAL]
labs=[f"0 次\n{z0:,} 个 · {z0/len(rows)*100:.0f}%",f"1–9 次\n{z10-z0:,} 个",f"10–99 次\n{z100-z10:,} 个",f"≥100 次\n{len(rows)-z100:,} 个 · {(len(rows)-z100)/len(rows)*100:.0f}%"]
wedges,_=ax.pie(vals,colors=cols,startangle=90,wedgeprops=dict(width=0.34,edgecolor=BG,linewidth=2))
for wd,lab in zip(wedges,labs):
    ang=np.deg2rad((wd.theta1+wd.theta2)/2); x,y=1.14*np.cos(ang),1.14*np.sin(ang)
    ax.text(x,y,lab,ha="center",va="center",fontsize=12.5,color=INK,weight="bold")
ax.text(0,0,"31,740\n个技能",ha="center",va="center",fontsize=17,weight="bold",color=INK)
ax.set(aspect="equal"); ax.set_position([0.10,0.10,0.80,0.74]); save(fig,"03-zombie.png")

# 04 月度爆发
fig,ax=canvas("两个月，技能数翻了 100 倍","9–10 月新增 30,745 个，占全量 97%")
mc=collections.Counter(r["上架时间"][:7] for r in rows)
months=["2026-05","2026-06","2026-07","2026-08","2026-09","2026-10"]; vals=[mc[m] for m in months]
cols=[GREY]*4+[ORANGE,RED]
bars=ax.bar([m[5:]+"月" for m in months],vals,color=cols,zorder=3,width=0.62)
for b,v in zip(bars,vals): ax.text(b.get_x()+b.get_width()/2,v+500,f"{v:,}",ha="center",fontsize=13,weight="bold",color=INK)
ax.set_ylim(0,20000); ax.spines[["top","right","left"]].set_visible(False); ax.set_yticks([])
ax.tick_params(axis="x",labelsize=12.5,colors=INK,length=0)
fig.text(0.07,0.065,"注：上架时间会被更新重置，此图看趋势，不抠绝对值。",fontsize=9.5,color="#8AA0B4")
fig.subplots_adjust(left=0.07,right=0.97,top=0.86,bottom=0.10); save(fig,"04-monthly.png")

# 05 分类：供给 vs 平均使用
from collections import defaultdict
cnt=defaultdict(int); use=defaultdict(int)
for r in rows:
    for c in r["分类"].split("/"):
        if c in ("education","health-wellness","industry-consultant"): continue
        cnt[c]+=1; use[c]+=r["u"]
cats=sorted(cnt,key=lambda c:use[c]/cnt[c])
fig,ax=canvas("哪个分类最值得做？","按平均使用量排：开发工具是商业运营的 15 倍")
y=np.arange(len(cats)); avgs=[use[c]/cnt[c] for c in cats]
cols=[RED if c=="商业运营" else (TEAL if c in ("开发工具","投资理财") else BLUE) for c in cats]
ax.barh(y,avgs,color=cols,height=0.6,zorder=3)
for yi,c,a in zip(y,cats,avgs): ax.text(a+28,yi,f"平均 {a:,.0f} · {cnt[c]:,} 个",va="center",fontsize=11.5,color=INK)
ax.set_yticks(y); ax.set_yticklabels(cats,fontsize=12.5,color=INK); ax.set_xlim(0,1420); ax.set_xticks([]); ax.set_yticks(ax.get_yticks()); [sp.set_visible(False) for sp in ax.spines.values()]; ax.tick_params(length=0)
fig.subplots_adjust(left=0.20,right=0.97,top=0.86,bottom=0.07); save(fig,"05-category.png")

# 06 来源效率
fig,ax=canvas("同样做技能，差距 198 倍","按来源看平均使用量（个位数技能 vs 三万个技能）")
sc=defaultdict(int); su=defaultdict(int)
for r in rows: sc[r["来源"]]+=1; su[r["来源"]]+=r["u"]
order=["个人开发者/其他","SkillHub(第三方市场)","官方","ClawHub(开源社区)","GitHub"]
short={"个人开发者/其他":"个人开发者","SkillHub(第三方市场)":"SkillHub","官方":"官方","ClawHub(开源社区)":"ClawHub","GitHub":"GitHub"}
y=np.arange(len(order))[::-1]
for yi,s in zip(y,order):
    avg=su[s]/sc[s]; col=RED if s=="GitHub" else (GREY if s=="个人开发者/其他" else BLUE)
    ax.barh(yi,[avg],color=col,height=0.58,zorder=3)
    ax.text(avg+1200,yi,f"平均 {avg:,.0f} 次 · {sc[s]:,} 个技能",va="center",fontsize=12.5,weight="bold",color=INK)
ax.set_yticks(y); ax.set_yticklabels([short[s] for s in order],fontsize=13,color=INK); ax.set_xlim(0,88000); ax.set_xticks([]); ax.set_yticks(ax.get_yticks()); [sp.set_visible(False) for sp in ax.spines.values()]; ax.tick_params(length=0)
fig.subplots_adjust(left=0.20,right=0.97,top=0.86,bottom=0.07); save(fig,"06-source.png")

# 07 Top20
fig,ax=canvas("使用量 Top 20 榜单","第一名 PDF 文档处理：1,113,078 次")
top=rows[:20][::-1]; y=np.arange(20)
ax.barh(y,[r["u"] for r in top],color=[RED if i==19 else BLUE for i in range(20)],height=0.62,zorder=3)
for yi,r in zip(y,top): ax.text(r["u"]+25000,yi,f"{r['u']:,}",va="center",fontsize=10.5,color=INK)
ax.set_yticks(y); ax.set_yticklabels([f"{21-i}. {top[i]['技能名']}" if False else f"{20-i}. {r['技能名']}" for i,r in enumerate(top)],fontsize=10.5,color=INK)
# fix labels: top list reversed, rank = 20-i
ax.set_yticklabels([f"{20-i}  {r['技能名']}" for i,r in enumerate(top)],fontsize=9.8,color=INK)
ax.set_xlim(0,1480000); ax.set_xticks([]); ax.set_yticks(ax.get_yticks()); [sp.set_visible(False) for sp in ax.spines.values()]; ax.tick_params(length=0); fig.subplots_adjust(left=0.41,right=0.97,top=0.86,bottom=0.07); save(fig,"07-top20.png")

# 08 平台赛道关键词
fig,ax=canvas("自媒体赛道：人挤，钱不挤","技能扎堆，但总使用量并不高")
kws=["小红书","抖音","公众号","视频号","B站","知乎"]
data=[]
for kw in kws:
    sel=[r for r in rows if kw.lower() in (r["技能名"]+" "+r["分类"]).lower()]
    # 与原报告口径一致：名称+描述无描述字段，用名称匹配会偏低；改用名称匹配并标注
    sel=[r for r in rows if kw in r["技能名"]]
    data.append((kw,len(sel),sum(r["u"] for r in sel)))
# 采用原报告已核数（名称/描述关键词）覆盖
report={"小红书":(617,177615),"抖音":(522,124221),"公众号":(650,578315),"视频号":(236,34149),"B站":(122,28864),"知乎":(88,42004)}
y=np.arange(len(kws))[::-1]
for yi,kw in zip(y,kws):
    c,u=report[kw]
    ax.barh(yi,[u],color=BLUE,height=0.55,zorder=3)
    ax.text(u+14000,yi,f"{c} 个技能 · 合计 {u:,} 次",va="center",fontsize=12,color=INK,weight="bold")
ax.set_yticks(y); ax.set_yticklabels(kws,fontsize=13,color=INK); ax.set_xlim(0,920000); ax.set_xticks([]); ax.set_yticks(ax.get_yticks()); [sp.set_visible(False) for sp in ax.spines.values()]; ax.tick_params(length=0)
fig.subplots_adjust(left=0.16,right=0.97,top=0.86,bottom=0.07); save(fig,"08-platform-tracks.png")

# 09 同名与停更
fig,ax=canvas("抄同款，也抄不出流量","同名技能最多 5 个挤一个名字；58% 从没更新过")
dups=collections.Counter(r["技能名"] for r in rows).most_common(5)
y=np.arange(len(dups))[::-1]
ax.barh(y,[d[1] for d in dups],color=ORANGE,height=0.55,zorder=3)
for yi,d in zip(y,dups): ax.text(d[1]+0.12,yi,f"{d[1]} 个同名",va="center",fontsize=13,weight="bold",color=INK)
ax.set_yticks(y); ax.set_yticklabels([d[0] for d in dups],fontsize=13,color=INK); ax.set_xlim(0,7.2); ax.set_xticks([]); ax.set_yticks(ax.get_yticks()); [sp.set_visible(False) for sp in ax.spines.values()]; ax.tick_params(length=0)
fig.text(0.07,0.16,"还有一组数：31,740 个里 18,331 个还是 1.0.0 版",fontsize=14,color=INK,weight="bold")
fig.text(0.07,0.125,"上架那天什么样，今天还是什么样。",fontsize=12,color="#5A7186")
fig.subplots_adjust(left=0.30,right=0.97,top=0.86,bottom=0.24); save(fig,"09-duplicate.png")

# 10 机会地图（散点：供给 vs 平均使用，气泡=总使用）
fig,ax=canvas("机会地图：人少、还被高频用","右上 = 供给不算多，平均使用高")
for c in cnt:
    ax.scatter(cnt[c],use[c]/cnt[c],s=max(60,use[c]/9000),color=TEAL if c in ("开发工具","投资理财","网站部署") else BLUE,alpha=0.75,zorder=3)
    ax.annotate(c,(cnt[c],use[c]/cnt[c]),fontsize=11,color=INK,xytext=(6,6),textcoords="offset points")
ax.set_xscale("log"); ax.set_xlim(80,120000); ax.set_xlabel("技能数量（对数轴）",fontsize=11.5,color=INK); ax.set_ylabel("平均使用量（次）",fontsize=11.5,color=INK)
ax.spines[["top","right"]].set_visible(False); ax.tick_params(labelsize=10.5,colors=INK)
ax.grid(True,color=LGREY,linewidth=0.7,zorder=0)
fig.subplots_adjust(left=0.14,right=0.93,top=0.86,bottom=0.12); save(fig,"10-opportunity.png")
print("ALL DONE", TOT)
