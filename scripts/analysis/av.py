import cv2,numpy as np,sys
fn,cx,cy,r=sys.argv[1],*map(int,sys.argv[2:5])
cap=cv2.VideoCapture(fn);fs=[]
while True:
  ok,f=cap.read()
  if not ok:break
  fs.append(cv2.cvtColor(f[cy-r:cy+r,cx-r:cx+r],cv2.COLOR_BGR2GRAY).astype(np.float32))
fs=np.array(fs);n=len(fs);H=2*r
ref=fs[0]
sh=[cv2.phaseCorrelate(ref,f)[0] for f in fs]
sh=np.array(sh);print('frames',n,'shift px max',np.abs(sh).max(0).round(2),'std',sh.std(0).round(2))
eye=fs[:,int(H*.30):int(H*.45),int(H*.25):int(H*.75)];mou=fs[:,int(H*.62):int(H*.80),int(H*.33):int(H*.67)];bg=fs[:,int(H*.05):int(H*.2),int(H*.05):int(H*.3)]
for nm,a in [('eye',eye),('mouth',mou),('bg',bg)]:
  d=np.abs(a-a.mean(0)).mean((1,2));print(nm,'dev mean',d.mean().round(2),'max',d.max().round(2))
# blink: eye-region darkness spikes
e=eye.mean((1,2));z=(e-np.median(e))/ (e.std()+1e-6);print('eye bright z>2.5 frames',int((z>2.5).sum()),'z<-2.5',int((z<-2.5).sum()))
# loop detection: similarity of whole-crop to frames >1s later
X=fs.reshape(n,-1);X=X-X.mean(1,keepdims=True);X/=np.linalg.norm(X,axis=1,keepdims=True)
best=[]
for i in range(0,n,30):
  s=X[i]@X.T; s[max(0,i-30):i+30]=-1;j=s.argmax();best.append((i,j,round(float(s[j]),4)))
print('nearest far frames',best[:8])
