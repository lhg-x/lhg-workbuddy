#!/usr/bin/env python3
"""卡片视频合成：口播原片 + 露脸裁圆 + 卡片页(A) / 录屏页(B, 放大+高亮框) → 3:4 成片。

  python3 scripts/compose_card_video.py episodes/ep01-install/segments.json --out ~/Movies/wb/ep01/edit

segments.json 见 skills/workbuddy-card-video/SKILL.md「segments.json 格式」。
"""
import argparse, json, subprocess, sys, tempfile
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "templates" / "canvas"))
from themes import THEMES  # noqa: E402

FPS = 30
CAM = (106, 925, 310)          # 头像圆窗左上角 x, y, 直径（与 render_canvas 的 cam_circle 一致）
SCR = (108, 243)               # 录屏框左上角（864×540）

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"命令失败: {' '.join(map(str, cmd))[:300]}\n{r.stderr[-1500:]}")

def render_pages(cfg, seg, si, total, work):
    """每条字幕渲染一张同版式卡片（镂空头像圆 + 录屏框）。"""
    pngs = []
    for ci, cap in enumerate(seg["captions"]):
        page = dict(seg["page"], caption=cap["text"], page_no=[si + 1, total])
        if seg["type"] == "B":
            page["type"] = "screen"
        c = {k: cfg[k] for k in ("host", "nav") if k in cfg}
        c.update(avatars=[], pages=[page])
        j = work / f"s{si:02d}_c{ci:02d}.json"
        j.write_text(json.dumps(c, ensure_ascii=False), encoding="utf-8")
        od = work / f"s{si:02d}_c{ci:02d}"
        run([sys.executable, str(HERE / "render_canvas.py"), str(j), "--out", str(od),
             "--theme", cfg["theme"], "--seed", str(cfg["seed"]), "--hole"])
        pngs.append(od / "page_01.png")
    return pngs

def build_segment(cfg, seg, si, total, work, base):
    src = str((base / cfg["source"]).expanduser())
    dur = seg["src_end"] - seg["src_start"]
    pngs = render_pages(cfg, seg, si, total, work)
    inputs = ["-ss", str(seg["src_start"]), "-t", str(dur), "-i", src]
    x, y, w = cfg["cam_crop"]
    fc = [f"[0:v]fps={FPS},crop={w}:{w}:{x}:{y},scale={CAM[2]}:{CAM[2]}:flags=lanczos,setsar=1[cam]",
          f"color=c=white:s=1080x1440:r={FPS}:d={dur}[bg]", f"[bg][cam]overlay={CAM[0]}:{CAM[1]}[l0]"]
    last, n = "l0", 1
    if seg["type"] == "B":
        s = seg["screen"]
        scr = work / f"s{si:02d}_scr.mp4"
        run([sys.executable, str(HERE / "zoom_highlight.py"), str((base / s["raw"]).expanduser()), str(base / s["events"]), str(scr),
             str(s.get("raw_start", 0)), str(dur), THEMES[cfg["theme"]]["accent"]])
        inputs += ["-i", str(scr)]
        fc.append(f"[{n}:v]setpts=PTS-STARTPTS[scr]"); fc.append(f"[{last}][scr]overlay={SCR[0]}:{SCR[1]}[l1]")
        last, n = "l1", n + 1
    caps = seg["captions"]
    for ci, png in enumerate(pngs):
        inputs += ["-i", str(png)]
        t0 = caps[ci]["t"]; t1 = caps[ci + 1]["t"] if ci + 1 < len(caps) else dur + 1
        out = f"p{ci}"
        fc.append(f"[{last}][{n}:v]overlay=0:0:enable='between(t,{t0},{t1 - 0.001})'[{out}]")
        last, n = out, n + 1
    fc.append(f"[{last}]format=yuv420p[v]")
    fc.append(f"[0:a]afade=t=in:d=0.03,afade=t=out:st={max(0, dur - 0.03)}:d=0.03[a]")
    out = work / f"seg_{si:02d}.mp4"
    run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]",
         "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-c:a", "pcm_s16le", "-t", str(dur), str(out).replace(".mp4", ".mov")])
    return Path(str(out).replace(".mp4", ".mov"))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("segments"); ap.add_argument("--out", required=True); ap.add_argument("--only", help="只合成某些段, 逗号分隔 id")
    a = ap.parse_args()
    sp = Path(a.segments); cfg = json.loads(sp.read_text(encoding="utf-8")); base = sp.parent
    segs = cfg["segments"]
    if a.only:
        keep = set(a.only.split(",")); segs = [s for s in segs if s["id"] in keep]
    out = Path(a.out).expanduser(); out.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="ccv_", dir=out))
    parts = [build_segment(cfg, s, i, len(cfg["segments"]), work, base) for i, s in enumerate(segs)]
    lst = work / "list.txt"; lst.write_text("".join(f"file '{p}'\n" for p in parts))
    final = out / cfg.get("output", "ep_v1.mp4")
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c:v", "copy",
         "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(final)])
    print("✓", final)

if __name__ == "__main__":
    main()
