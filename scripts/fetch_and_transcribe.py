"""下载 transcripts/ 里对应的抖音视频（aweme feed 免签名接口）并用 faster-whisper small 转写。
用法：python3 scripts/fetch_and_transcribe.py  → 视频进 template/asr-media/（wav 不入库），转写进 data/asr-2026-10-19/
然后跑 python3 scripts/fill_transcripts.py 回填 md。超过 300s 的长视频只转写前 120s。
"""
import os,json,time,subprocess,urllib.request,pandas as pd
from pathlib import Path
os.chdir(Path(__file__).resolve().parent.parent)
os.makedirs('template/asr-media',exist_ok=True); os.makedirs('data/asr-2026-10-19',exist_ok=True)
d=pd.read_csv('data/raw-2026-10-19/video_pool.csv').drop_duplicates('id').set_index('id')
ids=[(f[:-3],'workbuddy') for f in os.listdir('teardowns/2026-10-19-workbuddy/transcripts')]+[(f[:-3],'leviiii2026') for f in os.listdir('teardowns/2026-10-19-leviiii2026/transcripts')]
def dur(i): return d.loc[int(i),'duration_ms']/1000 if int(i) in d.index else 45
ids.sort(key=lambda x:dur(x[0]))
UA={'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)'}
def fetch(i):
    mp4=f'template/asr-media/{i}.mp4'
    if os.path.exists(mp4) and os.path.getsize(mp4)>50000: return mp4
    j=json.load(urllib.request.urlopen(urllib.request.Request(f'https://aweme.snssdk.com/aweme/v1/feed/?aweme_id={i}',headers=UA),timeout=20))
    a=[x for x in j['aweme_list'] if x['aweme_id']==i][0]
    for u in a['video']['play_addr']['url_list']:
        r=subprocess.run(['curl','-sL','-m','180','-A',UA['User-Agent'],'-o',mp4,u])
        if r.returncode==0 and os.path.getsize(mp4)>50000: time.sleep(1.5); return mp4
    raise Exception('dl fail')
if __name__=='__main__':
    import sys
    extra=[x for x in sys.argv[1:]]
    for i in extra: print('fetch',i,fetch(i),flush=True)
    from faster_whisper import WhisperModel
    m=WhisperModel('small',device='cpu',compute_type='int8',cpu_threads=2)
    for i,grp in ids:
        out=f'data/asr-2026-10-19/{i}.json'
        if os.path.exists(out): continue
        try:
            mp4=fetch(i); wav=f'template/asr-media/{i}.wav'; lim=300 if dur(i)<=300 else 120
            subprocess.run(['ffmpeg','-y','-loglevel','error','-i',mp4,'-t',str(lim),'-ac','1','-ar','16000',wav],check=True)
            import wave,numpy as np
            with wave.open(wav) as w: au=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
            segs,info=m.transcribe(au,language='zh',vad_filter=True,beam_size=1,initial_prompt='以下是普通话的句子，关于WorkBuddy、skill、AI智能体。')
            S=[{'s':round(s.start,1),'e':round(s.end,1),'t':s.text} for s in segs]
            json.dump({'id':i,'group':grp,'dur':dur(i),'truncated':bool(dur(i)>300),'asr_seconds':lim,'segments':S},open(out,'w'),ensure_ascii=False)
            print('ok',i,grp,dur(i),len(S),flush=True)
        except Exception as e: print('ERR',i,e,flush=True)
    print('DONE',flush=True)
