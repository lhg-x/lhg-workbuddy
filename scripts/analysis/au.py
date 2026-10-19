import subprocess,numpy as np,sys
fn=sys.argv[1]
x=np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',fn,'-ac','1','-ar','44100','-f','f32le','-'],capture_output=True).stdout,np.float32)
sr=44100;N=4096
fr=np.lib.stride_tricks.sliding_window_view(x,N)[::2048]*np.hanning(N)
P=(np.abs(np.fft.rfft(fr))**2).mean(0);f=np.fft.rfftfreq(N,1/sr)
db=10*np.log10(P+1e-12);
for lo,hi in [(4000,6000),(6000,8000),(8000,10000),(10000,11000),(11000,12000),(12000,14000),(14000,16000),(16000,20000)]:
  m=(f>=lo)&(f<hi);print(f'{lo//1000}-{hi//1000}k {db[m].mean():.1f}dB',end=' | ')
print()
# pauses via 20ms RMS
w=int(sr*.02);r=np.sqrt((x[:len(x)//w*w].reshape(-1,w)**2).mean(1));thr=r.max()*10**(-35/20)
q=r<thr;runs=[];c=0
for v in q:
  if v:c+=1
  else:
    if c:runs.append(c*20);c=0
runs=[d for d in runs if d>=100];print('dur',round(len(x)/sr,1),'pauses>=100ms',len(runs),'max',max(runs) if runs else 0,'total ms',sum(runs))
# music bed? check energy floor during low frames
print('rms p5/p50 dB',np.round(20*np.log10(np.percentile(r,[5,50])+1e-9),1))
