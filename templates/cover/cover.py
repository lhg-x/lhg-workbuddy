"""9:16 封面模板（苹果风）。python3 cover.py cover.json → cover_<style>.png
cover.json: {ep, series, title:[行1,行2], hl(标题里渐变高亮的词), sub, host, face, app}"""
import json,sys,subprocess,os,base64
cfg=json.load(open(sys.argv[1] if len(sys.argv)>1 else 'cover.json'))
def b64(p): return 'data:image/png;base64,'+base64.b64encode(open(p,'rb').read()).decode()
F,A=b64(cfg['face']),b64(cfg['app'])
def T(s): return s.replace(cfg['hl'],f'<span class="g">{cfg["hl"]}</span>') if cfg.get('hl') else s
title='<br>'.join(T(x) for x in cfg['title'])
base='''*{margin:0;box-sizing:border-box}body{width:1080px;height:1920px;overflow:hidden;font-family:"Noto Sans SC",sans-serif;-webkit-font-smoothing:antialiased;position:relative}
.ser{font-size:38px;font-weight:500;letter-spacing:2px}.ep{font-size:40px;font-weight:700}
h1{font-size:150px;line-height:1.08;font-weight:900;letter-spacing:-4px}.sub{font-size:44px;font-weight:500;line-height:1.5}
.g{background:linear-gradient(100deg,#0fa36b 0%,#12b981 40%,#f5c400 100%);-webkit-background-clip:text;color:transparent}
.win{border-radius:30px;overflow:hidden}.win img{display:block;width:100%}
.face{border-radius:50%;overflow:hidden}.face img{width:100%;display:block}
.host{position:absolute;top:110px;left:0;right:0;justify-content:center;font-size:32px;font-weight:700;display:flex;align-items:center;gap:14px}.dot{width:16px;height:16px;border-radius:50%;background:#0fa36b}'''
S={}
S['light']=('''body{background:#f5f5f7;color:#1d1d1f}
.top{position:absolute;top:230px;left:60px;right:60px;text-align:center}
.ep{color:#0fa36b}.ser{color:#86868b;margin-top:14px}
h1{margin-top:50px}.sub{color:#6e6e73;margin-top:40px}
.win{position:absolute;left:90px;right:90px;top:1090px;box-shadow:0 40px 90px rgba(0,0,0,.18),0 0 0 1px rgba(0,0,0,.05)}
.face{position:absolute;width:230px;height:230px;left:56px;top:1440px;border:10px solid #fff;box-shadow:0 20px 50px rgba(0,0,0,.2)}
.host{color:#86868b}''',
'<div class="top"><div class="ep">第 {ep} 课</div><div class="ser">{series}</div><h1>{title}</h1><div class="sub">{sub}</div></div><div class="win"><img src="{A}"></div><div class="face"><img src="{F}"></div><div class="host"><i class="dot"></i>{host}</div>')
S['dark']=('''body{background:#000;color:#f5f5f7}
.glow{position:absolute;left:-200px;right:-200px;top:900px;height:900px;background:radial-gradient(closest-side,rgba(15,163,107,.55),rgba(245,196,0,.12) 60%,transparent)}
.big{position:absolute;right:50px;top:150px;font-size:340px;font-weight:100;color:transparent;-webkit-text-stroke:2px rgba(255,255,255,.18);line-height:1}
.top{position:absolute;top:240px;left:90px;right:60px}
.ep{color:#f5c400}.ser{color:#a1a1a6;margin-top:14px}h1{margin-top:60px}.sub{color:#a1a1a6;margin-top:40px}
.win{position:absolute;left:90px;right:90px;top:1160px;box-shadow:0 0 0 1px rgba(255,255,255,.12),0 30px 120px rgba(15,163,107,.45)}
.face{position:absolute;width:220px;height:220px;right:56px;top:1560px;border:6px solid #000;box-shadow:0 0 0 3px #0fa36b}
.host{color:#a1a1a6}''',
'<div class="glow"></div><div class="big">{ep}</div><div class="top"><div class="ep">第 {ep} 课</div><div class="ser">{series}</div><h1>{title}</h1><div class="sub">{sub}</div></div><div class="win"><img src="{A}"></div><div class="face"><img src="{F}"></div><div class="host"><i class="dot"></i>{host}</div>')
S['glass']=('''body{background:#e9eef6;color:#1d1d1f}
.b{position:absolute;border-radius:50%;filter:blur(120px)}
.card{position:absolute;left:70px;right:70px;top:440px;padding:150px 50px 64px;z-index:1;border-radius:56px;background:rgba(255,255,255,.55);backdrop-filter:blur(40px);box-shadow:0 30px 80px rgba(40,60,90,.15),inset 0 0 0 1.5px rgba(255,255,255,.8)}
.ep{color:#0fa36b}.ser{color:#6e6e73;margin-top:10px}h1{margin-top:36px;font-size:140px}.sub{color:#515154;margin-top:32px;font-size:38px}
.face{position:absolute;width:260px;height:260px;left:410px;top:300px;border:10px solid rgba(255,255,255,.9);box-shadow:0 20px 60px rgba(40,60,90,.25);z-index:2}
.win{position:absolute;left:140px;right:140px;top:1230px;box-shadow:0 30px 80px rgba(40,60,90,.25);border-radius:24px}
.host{color:#515154}''',
'<div class="b" style="width:700px;height:700px;left:-200px;top:-100px;background:#7dd3c0"></div><div class="b" style="width:800px;height:800px;right:-300px;top:500px;background:#a5b4fc"></div><div class="b" style="width:700px;height:700px;left:-100px;bottom:-100px;background:#fde68a"></div><div class="face"><img src="{F}"></div><div class="card" style="text-align:center"><div class="ep">第 {ep} 课</div><div class="ser">{series}</div><h1>{title}</h1><div class="sub">{sub}</div></div><div class="win"><img src="{A}"></div><div class="host"><i class="dot"></i>{host}</div>')
for k,(css,body) in [(x,S[x]) for x in (sys.argv[2].split(',') if len(sys.argv)>2 else S)]:
    h=body.replace('{A}',A).replace('{F}',F).replace('{title}',title)
    for f in('ep','series','sub','host'): h=h.replace('{'+f+'}',cfg[f])
    open(f'c_{k}.html','w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>{base}{css}</style></head><body>{h}</body></html>')
    subprocess.run(['chromium','--headless','--no-sandbox','--hide-scrollbars','--disable-gpu','--force-device-scale-factor=1','--window-size=1080,1920',f'--screenshot=cover_{k}.png',f'file://{os.path.abspath(f"c_{k}.html")}'],capture_output=True)
    print(k)
