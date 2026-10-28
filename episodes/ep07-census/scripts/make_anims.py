# -*- coding: utf-8 -*-
"""数据动效：matplotlib 逐帧渲染 -> ffmpeg 合成 MP4（1080x1440, 24fps, 无声）"""
import subprocess, shutil
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np

font_manager.fontManager.addfont("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc")
font_manager.fontManager.addfont("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc")
plt.rcParams["font.family"]="Noto Sans CJK JP"; plt.rcParams["axes.unicode_minus"]=False
BG="#F7FAFD"; INK="#12314F"; BLUE="#1769C2"; ORANGE="#F07818"; RED="#D93A2B"; GREY="#B9C6D2"; LGREY="#E3EBF2"; TEAL="#0FA3A3"
ROOT=Path.home()/"workspace/goals/ai/files/wb-census-ep07/assets/anim"; ROOT.mkdir(parents=True,exist_ok=True)
TMP=Path("/tmp/anim_frames")
def ease(t): return 1-(1-t)**3
import os
def render(name, frames_fn, nframes):
    if os.environ.get("ONLY") and name not in os.environ["ONLY"].split(","): return
    d=TMP/name; shutil.rmtree(d,ignore_errors=True); d.mkdir(parents=True)
    for i in range(nframes):
        fig=frames_fn(i/nframes, i)
        fig.savefig(d/f"f{i:04d}.png",dpi=200,facecolor=BG); plt.close(fig)
    out=ROOT/f"{name}.mp4"
    subprocess.run(["ffmpeg","-v","error","-y","-framerate","24","-i",str(d/"f%04d.png"),
                    "-c:v","libx264","-pix_fmt","yuv420p","-crf","18","-vf","scale=1080:1440",str(out)],check=True)
    # 同步出 GIF 预览（480宽）
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(out),"-vf","scale=480:-1:flags=lanczos,fps=12",str(ROOT/f"{name}.gif")],check=True)
    print("ok",out)
def base(title,sub=""):
    fig,ax=plt.subplots(figsize=(5.4,7.2)); fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    fig.text(0.07,0.945,title,fontsize=21,color=INK,weight="bold")
    if sub: fig.text(0.07,0.905,sub,fontsize=11.5,color="#5A7186")
    fig.text(0.07,0.025,"数据：WorkBuddy 技能市场全量普查 2026-10-26 · n=31,740 · 非官方自采",fontsize=8.5,color="#8AA0B4")
    return fig,ax

# anim00 数字滚动
def f_counter(t,i):
    fig,ax=base("我把技能市场，全爬了一遍","WorkBuddy「专家·技能·连接器」全量清单")
    ax.axis("off"); k=ease(min(1,t*1.15))
    ax.text(0.5,0.62,f"{int(31740*k):,}",ha="center",fontsize=64,weight="bold",color=INK,transform=ax.transAxes)
    ax.text(0.5,0.52,"个技能 · 一条不落",ha="center",fontsize=17,color="#5A7186",transform=ax.transAxes)
    if t>0.45:
        k2=ease((t-0.45)/0.55)
        ax.text(0.5,0.36,f"总使用 {int(13801653*k2):,} 次",ha="center",fontsize=21,weight="bold",color=BLUE,transform=ax.transAxes)
        ax.text(0.5,0.29,f"总安装 {int(6665631*k2):,} 次",ha="center",fontsize=21,weight="bold",color=TEAL,transform=ax.transAxes)
    return fig
render("anim00-counter",f_counter,72)

# anim01 集中度条生长
NS=[10,50,100,317,1000]; SH=[40.6,64.7,73.0,83.9,92.1]
def f_conc(t,i):
    fig,ax=base("流量被谁吃掉了？","占比按使用量累计，从高到低")
    y=np.arange(len(NS))[::-1]
    ax.barh(y,[100]*len(NS),color=LGREY,height=0.62)
    for j,(n,s) in enumerate(zip(NS,SH)):
        lt=np.clip(t*1.6-j*0.12,0,1); v=s*ease(lt)
        ax.barh(y[j],[v],color=RED if n==100 else BLUE,height=0.62)
        if lt>0.85: ax.text(s+2,y[j],f"{s:.1f}%",va="center",fontsize=15,weight="bold",color=INK)
    ax.set_yticks(y); ax.set_yticklabels([f"前 {n} 名" for n in NS],fontsize=13,color=INK)
    ax.set_xlim(0,108); ax.set_xticks([]); [sp.set_visible(False) for sp in ax.spines.values()]; ax.tick_params(length=0)
    fig.subplots_adjust(left=0.20,right=0.97,top=0.86,bottom=0.07); return fig
render("anim01-concentration",f_conc,96)

# anim02 华夫饼：100 格 = 全部技能
def f_waffle(t,i):
    fig,ax=base("100 个技能里，88 个用量不到百次","每一格 = 全部技能的 1%")
    ax.axis("off"); ax.set_xlim(-0.6,10.6); ax.set_ylim(-1.8,10.6)
    # 顺序：>=100 teal 12, 10-99 blue 28, 1-9 orange 44, 0 red 16
    seq=[TEAL]*12+[BLUE]*28+[ORANGE]*44+[RED]*16
    n=int(ease(min(1,t*1.1))*100)
    for idx in range(100):
        x,y=idx%10,9-idx//10
        col=seq[idx] if idx<n else LGREY
        ax.add_patch(plt.Rectangle((x+0.08,y+0.08),0.84,0.84,color=col))
    done10=sum(1 for idx in range(min(n,100)) if idx>=40)
    ax.text(5,-1.2,f"使用量不足 10 次：{done10} / 60",ha="center",fontsize=16,weight="bold",color=RED if n>=84 else INK)
    return fig
render("anim02-waffle",f_waffle,96)

# anim03 月度柱生长
MONTHS=["05月","06月","07月","08月","09月","10月"]; VALS=[174,49,87,685,12988,17757]
def f_month(t,i):
    fig,ax=base("两个月，技能数翻了 100 倍","每月新增技能数（上架时间口径，看趋势）")
    cols=[GREY]*4+[ORANGE,RED]
    for j,(m,v) in enumerate(zip(MONTHS,VALS)):
        lt=np.clip(t*1.7-j*0.13,0,1); h=v*ease(lt)
        ax.bar(j,[h],color=cols[j],width=0.62,zorder=3)
        if lt>0.9: ax.text(j,v+500,f"{v:,}",ha="center",fontsize=13,weight="bold",color=INK)
    ax.set_xticks(range(6)); ax.set_xticklabels(MONTHS,fontsize=12.5,color=INK)
    ax.set_ylim(0,20000); ax.set_yticks([]); [ax.spines[s].set_visible(False) for s in ("top","right","left")]; ax.tick_params(length=0)
    fig.subplots_adjust(left=0.07,right=0.97,top=0.86,bottom=0.10); return fig
render("anim03-monthly",f_month,96)

# anim04 来源效率条 + 数字
SRC_L=["个人开发者","SkillHub","官方","ClawHub","GitHub"]; SRC_V=[286,13001,27189,38085,56592]; SRC_C=[31556,78,52,39,15]
def f_src(t,i):
    fig,ax=base("同样做技能，差距 198 倍","平均使用量：GitHub 来源 vs 个人开发者")
    y=np.arange(len(SRC_L))[::-1]; k=ease(min(1,t*1.15))
    for j,(lab,v,c) in enumerate(zip(SRC_L,SRC_V,SRC_C)):
        ax.barh(y[j],[v*k],color=RED if lab=="GitHub" else (GREY if lab=="个人开发者" else BLUE),height=0.58)
        ax.text(v*k+1200,y[j],f"{int(v*k):,} 次 · {c:,} 个",va="center",fontsize=12,weight="bold",color=INK)
    ax.set_yticks(y); ax.set_yticklabels(SRC_L,fontsize=13,color=INK); ax.set_xlim(0,90000)
    ax.set_xticks([]); [sp.set_visible(False) for sp in ax.spines.values()]; ax.tick_params(length=0)
    fig.subplots_adjust(left=0.20,right=0.97,top=0.86,bottom=0.07); return fig
render("anim04-source",f_src,96)

# anim05 Top10 赛跑
NAMES=["PDF 文档处理","AI交付自检","NeoData金融","Skill安全审计","Excel 表格处理","Web Access","PPT 演示文稿","去AI味","AIHOT","金山文档|WPS"]
VALS10=[1113078,931247,760281,659257,593884,417332,360967,289658,288576,195225]
def f_top(t,i):
    fig,ax=base("使用量 Top 10","第一名一个技能，顶 3 万个长尾")
    y=np.arange(10)[::-1]
    for j,(nm,v) in enumerate(zip(NAMES,VALS10)):
        lt=np.clip(t*1.8-j*0.09,0,1); w=v*ease(lt)
        ax.barh(y[j],[w],color=RED if j==0 else BLUE,height=0.6)
        if lt>0.85: ax.text(v+25000,y[j],f"{v:,}",va="center",fontsize=11,color=INK)
    ax.set_yticks(y); ax.set_yticklabels([f"{j+1} {nm}" for j,nm in enumerate(NAMES)],fontsize=11,color=INK)
    ax.set_xlim(0,1360000); ax.set_xticks([]); [sp.set_visible(False) for sp in ax.spines.values()]; ax.tick_params(length=0)
    fig.subplots_adjust(left=0.32,right=0.97,top=0.86,bottom=0.07); return fig
render("anim05-top10",f_top,96)
print("ANIMS DONE")
