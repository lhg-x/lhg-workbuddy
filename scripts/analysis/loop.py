import cv2,numpy as np,sys
fn,cx,cy,r=sys.argv[1],*map(int,sys.argv[2:5])
cap=cv2.VideoCapture(fn);fs=[]
while True:
  ok,f=cap.read()
  if not ok:break
  g=cv2.cvtColor(f[cy-r:cy+r,cx-r:cx+r],cv2.COLOR_BGR2GRAY);H=2*r
  g=g[int(H*.12):int(H*.55),int(H*.2):int(H*.8)]  # hair+eyes, no mouth
  fs.append(cv2.resize(g,(48,32)).astype(np.float32).ravel())
X=np.array(fs);X-=X.mean(1,keepdims=True);X/=np.linalg.norm(X,axis=1,keepdims=True);n=len(X)
S=X@X.T
fw=[];bw=[]
for L in range(30,n-60):
  fw.append(np.mean([S[t,t+L] for t in range(0,n-L)]))
fw=np.array(fw);top=np.argsort(fw)[-5:][::-1]+30
print('forward lag peaks (frames,score):',[(int(l),round(float(fw[l-30]),4)) for l in top],'median',round(float(np.median(fw)),4))
# per-frame best match far away (>2s) and its lag
lags=[];sc=[]
for t in range(n):
  s=S[t].copy();s[max(0,t-60):t+60]=-1;j=s.argmax();lags.append(j-t);sc.append(s[j])
sc=np.array(sc);print('far-match score p10/p50/p90',np.round(np.percentile(sc,[10,50,90]),4))
L=np.array(lags)[sc>np.percentile(sc,70)];v,c=np.unique(L,return_counts=True);o=np.argsort(c)[-6:][::-1];print('common lags',list(zip(v[o].tolist(),c[o].tolist())))
