import json,subprocess,numpy as np,cv2,sys
SRC,TL,OUT='raw.mov','tl.jsonl','zoom_card.mp4'
T0,T1=1.5,14.5; TOP=38; SW,SH=1470,956-TOP   # pt content area (去刘海黑条)
OW,OH=864,540; Z=2.2; MOVE=0.7; TR=0.6
ev=[json.loads(l) for l in open(TL) if l.strip()]
def clampc(cx,cy,z):
    vw=SW/z; vh=vw*OH/OW
    return min(max(cx,vw/2),SW-vw/2), min(max(cy-TOP,vh/2),SH-vh/2)
keys=[(0,(SW/2,SH/2,1.0))]
for e in ev:
    cx,cy=clampc(e['x'],e['y'],Z); keys.append((e['t'],None)); keys[-1]=(e['t'],(cx,cy,Z))
last=ev[-1]['t']+MOVE+1.6; keys.append((last,(SW/2,SH/2,1.0)))
def ease(u): u=min(max(u,0),1); return u*u*(3-2*u)
def cam(t):
    cur=keys[0][1]
    for i in range(1,len(keys)):
        ts,k=keys[i]; prev=keys[i-1][1] if i==1 else None
        if t<ts: break
        u=ease((t-ts)/TR); p=cur
        cur=(p[0]+(k[0]-p[0])*u, p[1]+(k[1]-p[1])*u, float(np.exp(np.log(p[2])+(np.log(k[2])-np.log(p[2]))*u)))
    return cur
W,H=2940,1912; n=W*H*3
dec=subprocess.Popen(['ffmpeg','-v','error','-ss',str(T0),'-to',str(T1),'-i',SRC,'-f','rawvideo','-pix_fmt','bgr24','-'],stdout=subprocess.PIPE)
enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{OW}x{OH}','-r','60','-i','-','-c:v','libx264','-crf','16','-pix_fmt','yuv420p',OUT],stdin=subprocess.PIPE)
i=0
while True:
    b=dec.stdout.read(n)
    if len(b)<n: break
    f=np.frombuffer(b,np.uint8).reshape(H,W,3)[TOP*2:]
    cx,cy,z=cam(T0+i/60); vw=SW/z; vh=vw*OH/OW
    x0,y0=(cx-vw/2)*2,(cy-vh/2)*2
    M=np.float32([[OW/(vw*2),0,-x0*OW/(vw*2)],[0,OH/(vh*2),-y0*OH/(vh*2)]])
    enc.stdin.write(cv2.warpAffine(f,M,(OW,OH),flags=cv2.INTER_AREA if z<1.6 else cv2.INTER_LANCZOS4).tobytes()); i+=1
enc.stdin.close(); enc.wait(); print('frames',i)
