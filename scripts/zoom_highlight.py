"""录屏跟随放大 + 目标高亮框。
events.jsonl 每行: {"t":输出秒, "box":[x,y,w,h](pt,含刘海坐标) 或 null, "zoom":倍数(1=全景)}
相机在 t 开始 0.6s 平滑移到 box 中心；高亮框在到位后 0.25s 弹出(1.12→1.0 + 淡入)，到下个事件 t 时 0.2s 淡出。"""
import json,subprocess,sys,numpy as np,cv2
SRC,EV,OUT,RAW0,DUR,ACC=sys.argv[1],sys.argv[2],sys.argv[3],float(sys.argv[4]),float(sys.argv[5]),sys.argv[6]
import os
_pr=subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height','-of','csv=p=0',SRC],capture_output=True,text=True).stdout.strip().split(',')
W,H=int(_pr[0]),int(_pr[1]); SC=float(os.environ.get('ZH_SCALE',2))  # 像素/pt（Retina=2）
TOP=int(os.environ.get('ZH_TOP',38 if (W,H)==(2940,1912) else 0))  # 顶部刘海裁掉的 pt
SW,SH=W/SC,H/SC-TOP; OW,OH=864,540; TR=0.6; FPS=30
acc=tuple(int(ACC.lstrip('#')[i:i+2],16) for i in (4,2,0))  # BGR
V0=min(SW,SH*OW/OH)  # 全景视宽：填满 16:10 框
ev=[json.loads(l) for l in open(EV) if l.strip()]
def target(e):
    z=e.get('zoom',1.0)
    if not e.get('box') or z<=1: return (SW/2,SH/2,1.0)
    x,y,w,h=e['box']; cx,cy=x+w/2,y+h/2-TOP
    vw=V0/z; vh=vw*OH/OW
    return (min(max(cx,vw/2),SW-vw/2),min(max(cy,vh/2),SH-vh/2),z)
keys=[(0,(SW/2,SH/2,1.0))]+[(e['t'],target(e)) for e in ev]
ease=lambda u:(lambda v:v*v*(3-2*v))(min(max(u,0),1))
def cam(t):
    cur=keys[0][1]
    for ts,k in keys[1:]:
        if t<ts: break
        u=ease((t-ts)/TR); p=cur
        cur=(p[0]+(k[0]-p[0])*u,p[1]+(k[1]-p[1])*u,float(np.exp(np.log(p[2])+(np.log(k[2])-np.log(p[2]))*u)))
    return cur
def hl_state(t):
    for i,e in enumerate(ev):
        nxt=ev[i+1]['t'] if i+1<len(ev) else 1e9
        if e.get('box') and e['t']+TR<=t<nxt+0.2:
            a=min(1,(t-e['t']-TR)/0.25); s=1.12-0.12*ease(a)
            if t>nxt: a*=max(0,1-(t-nxt)/0.2)
            return e['box'],a,s
    return None
def draw(img,box,a,s,M):
    x,y,w,h=box; pad=6; cx,cy=x+w/2,y+h/2; w,h=(w+2*pad)*s,(h+2*pad)*s
    pts=np.array([[cx-w/2,cy-h/2-TOP],[cx+w/2,cy+h/2-TOP]])*SC
    p=(pts@M[:,:2].T+M[:,2]); (x0,y0),(x1,y1)=p
    r=int(min(14,(y1-y0)/2)); lay=np.zeros_like(img); m=np.zeros(img.shape[:2],np.uint8)
    def rr(dst,col,th):
        x0i,y0i,x1i,y1i=map(int,(x0,y0,x1,y1))
        for c,ang in [((x0i+r,y0i+r),180),((x1i-r,y0i+r),270),((x1i-r,y1i-r),0),((x0i+r,y1i-r),90)]:
            cv2.ellipse(dst,c,(r,r),ang,0,90,col,th,cv2.LINE_AA)
        cv2.line(dst,(x0i+r,y0i),(x1i-r,y0i),col,th,cv2.LINE_AA);cv2.line(dst,(x0i+r,y1i),(x1i-r,y1i),col,th,cv2.LINE_AA)
        cv2.line(dst,(x0i,y0i+r),(x0i,y1i-r),col,th,cv2.LINE_AA);cv2.line(dst,(x1i,y0i+r),(x1i,y1i-r),col,th,cv2.LINE_AA)
    # 光晕
    g=np.zeros(img.shape[:2],np.float32); gm=np.zeros(img.shape[:2],np.uint8); rr(gm,255,10); g=cv2.GaussianBlur(gm.astype(np.float32)/255,(0,0),7)*0.55*a
    # 实线
    lm=np.zeros(img.shape[:2],np.uint8); rr(lm,255,3); l=lm.astype(np.float32)/255*a
    al=np.clip(g+l,0,1)[...,None]; col=np.array(acc,np.float32)
    return (img*(1-al)+col*al).astype(np.uint8)
n=W*H*3
dec=subprocess.Popen(['ffmpeg','-v','error','-ss',str(RAW0),'-t',str(DUR),'-i',SRC,'-vf',f'fps={FPS}','-f','rawvideo','-pix_fmt','bgr24','-'],stdout=subprocess.PIPE)
enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{OW}x{OH}','-r',str(FPS),'-i','-','-c:v','libx264','-crf','16','-pix_fmt','yuv420p',OUT],stdin=subprocess.PIPE)
i=0
while True:
    b=dec.stdout.read(n)
    if len(b)<n: break
    f=np.frombuffer(b,np.uint8).reshape(H,W,3)[int(TOP*SC):]; t=i/FPS
    cx,cy,z=cam(t); vw=V0/z; vh=vw*OH/OW; x0,y0=(cx-vw/2)*SC,(cy-vh/2)*SC; s=OW/(vw*SC)
    M=np.float32([[s,0,-x0*s],[0,s,-y0*s]])
    o=cv2.warpAffine(f,M,(OW,OH),flags=cv2.INTER_AREA if z<1.6 else cv2.INTER_LANCZOS4)
    h=hl_state(t)
    if h: o=draw(o,h[0],h[1],h[2],M)
    enc.stdin.write(o.tobytes()); i+=1
enc.stdin.close(); enc.wait(); print('frames',i)
