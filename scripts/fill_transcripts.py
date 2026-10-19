"""把 data/asr-2026-10-19/*.json 回填到 teardowns/*/transcripts/*.md 的「口播文稿」节（可重复跑）。依赖：pip install opencc-python-reimplemented"""
import json,os,re,glob
from pathlib import Path
os.chdir(Path(__file__).resolve().parent.parent)
from opencc import OpenCC
cc=OpenCC('t2s')
FIX={'检集':'剪辑','剪集':'剪辑','chat cart':'ChatCut','Chat cart':'ChatCut','Cdance':'Seedance','无休改':'无修改',
     'Work Buddy':'WorkBuddy','work buddy':'WorkBuddy','Workbuddy':'WorkBuddy','workbuddy':'WorkBuddy','Walkbuddy':'WorkBuddy','Wordbuddy':'WorkBuddy',
     'SKU':'skill','Skil ':'skill ','附用':'复用','检视频':'剪视频','WalkBuddy':'WorkBuddy','OrgBuddy':'WorkBuddy','领基分':'领积分','基分':'积分',
     'Clod Code':'Claude Code','ClodCode':'Claude Code','宝木机':'保姆级','薄目机':'保姆级','保姆及':'保姆级','斯基尔':'skill','思gill':'skill'}
def clean(t):
    t=cc.convert(t)
    for a,b in FIX.items(): t=t.replace(a,b)
    return t.strip()
n=0
for md in glob.glob('teardowns/2026-10-19-*/transcripts/*.md'):
    i=os.path.basename(md)[:-3]; js=f'data/asr-2026-10-19/{i}.json'
    if not os.path.exists(js): continue
    a=json.load(open(js)); segs=a['segments']
    s=open(md,encoding='utf-8').read()
    head=s.split('## 口播文稿')[0].rstrip()
    lines=[]; buf=''; t0=None
    for g in segs:
        if t0 is None: t0=g['s']
        buf+=clean(g['t'])+('' if re.search('[，。？！,.?!]$',clean(g['t'])) else '，')
        if g['e']-t0>=15 or g is segs[-1]:
            m,sec=divmod(int(t0),60); lines.append(f'- `{m:02d}:{sec:02d}` {buf.rstrip("，")}'); buf=''; t0=None
    note='> faster-whisper small（int8，CPU）自动转写，**未人工校对**；已做繁转简和常见专有名词纠错。'
    if a.get('truncated'): note+=f' 原片 {int(a["dur"])}s，只转写了前 {a.get("asr_seconds",300)}s（开头钩子和结构）。'
    body='\n'.join(lines) if lines else '（无可识别人声：纯音乐 / 无口播）'
    if len(''.join(clean(g['t']) for g in segs))<20: body='（几乎无口播，疑似纯音乐 + 字幕）\n'+body
    open(md,'w',encoding='utf-8').write(f'{head}\n\n## 口播文稿\n{note}\n\n{body}\n')
    n+=1
print('filled',n)
