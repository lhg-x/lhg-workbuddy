import json,subprocess,sys,os
R='/data/wb/repo/scripts'; FPS=30; CAM=(106,925,310); SCR=(108,243)
S=json.load(open('segs.json')); N=len(S)
def run(c):
    r=subprocess.run(c,capture_output=True,text=True)
    if r.returncode: sys.exit(' '.join(map(str,c))[:300]+'\n'+r.stderr[-1500:])
nav={"logo":"W","brand":"WorkBuddy","topic":"AI 员工 · 第 01 课","tabs":["安装","技能","提问"]}
step=sys.argv[1] if len(sys.argv)>1 else 'all'
if step in('all','cards'):
    pages=[]
    for si,s in enumerate(S):
        for c in s['caps']:
            p=dict(s['page'],caption=c['text'],page_no=[si+1,N])
            if s['type']=='B': p['type']='screen'
            pages.append(p)
    json.dump({"host":"lhg·AI实验室","nav":nav,"avatars":[],"pages":pages},open('cards.json','w'),ensure_ascii=False)
    run([sys.executable,f'{R}/render_canvas.py','cards.json','--out','cards','--theme','mint','--seed','7','--hole']); print('cards ok',flush=True)
# demo time map: narration abs -> demo sec
K=[(97.5,0),(99.2,6.0),(100.6,8.5),(102.9,10.0),(106.9,12.5),(113.9,14.5),(117.9,18.0),(127.2,23.0),(136.5,25.0),(141.5,28.0),(145.5,34.0),(255.6,123.0)]
if step in('all','screens'):
    fc=[];L=[]
    for i in range(len(K)-1):
        (n0,d0),(n1,d1)=K[i],K[i+1]
        fc.append(f"[0:v]trim={d0}:{d1},setpts=(PTS-STARTPTS)*{(n1-n0)/(d1-d0):.5f},fps={FPS}[p{i}]");L.append(f"[p{i}]")
    fc.append(''.join(L)+f"concat=n={len(L)}:v=1:a=0,crop=1728:1080,scale=864:540:flags=lanczos,setsar=1,format=yuv420p[v]")
    run(['ffmpeg','-v','error','-y','-i','demo.mp4','-filter_complex',';'.join(fc),'-map','[v]','-c:v','libx264','-crf','16','-preset','fast','demo_map.mp4'])
    s=S[2]; run([sys.executable,'zh.py','win.mov','ev_s3.jsonl','scr_site.mp4',str(s['a']),str(s['b']-s['a']),'#0fa36b']); print('screens ok',flush=True)
if step in('all','segs'):
    k=0;parts=[]
    for si,s in enumerate(S):
        a,b=s['a'],s['b'];d=b-a;caps=s['caps']
        inp=['-ss',str(a),'-t',str(d),'-i','cam.mov','-ss',str(a),'-t',str(d),'-i','win.mov']
        fc=[f"[0:v]fps={FPS},crop=900:900:370:130,hflip,scale={CAM[2]}:{CAM[2]}:flags=lanczos,setsar=1[cam]",
            f"color=c=white:s=1080x1440:r={FPS}:d={d}[bg]","[bg][cam]overlay=%d:%d[l0]"%CAM[:2]];last='l0';n=2
        if s['type']=='B':
            if s['screen']['kind']=='zoom': inp+=['-i','scr_site.mp4']
            else: inp+=['-ss',str(a-K[0][0]),'-t',str(d),'-i','demo_map.mp4']
            fc+= [f"[{n}:v]setpts=PTS-STARTPTS[scr]",f"[{last}][scr]overlay={SCR[0]}:{SCR[1]}:eof_action=repeat[l1]"];last='l1';n+=1
        for ci,c in enumerate(caps):
            k+=1; inp+=['-i',f'cards/page_{k:02d}.png']
            t0=0 if ci==0 else c['t']-a; t1=(caps[ci+1]['t']-a) if ci+1<len(caps) else d+1
            fc.append(f"[{last}][{n}:v]overlay=0:0:enable='between(t,{t0:.3f},{t1-0.001:.3f})'[c{ci}]");last=f'c{ci}';n+=1
        fc.append(f"[{last}]format=yuv420p[v]")
        o=f'out/seg{si:02d}.mov'
        run(['ffmpeg','-v','error','-y',*inp,'-filter_complex',';'.join(fc),'-map','[v]','-map','1:a','-c:v','libx264','-crf','18','-preset','fast','-c:a','pcm_s16le','-t',str(d),o])
        parts.append(o); print('seg',si,flush=True)
    open('out/list.txt','w').write(''.join(f"file '{os.path.basename(p)}'\n" for p in parts))
    run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','out/list.txt','-c:v','copy','-af','loudnorm=I=-16:TP=-1.5:LRA=11','-c:a','aac','-b:a','192k','-movflags','+faststart','ep01_v2.mp4'])
    print('DONE',flush=True)
