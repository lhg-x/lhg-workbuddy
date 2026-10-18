# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "pillow", "librosa"]
# ///
"""机器拆解参考视频。

产出：analysis.json（镜头表/运动强度/色板/响度/节拍）、contact_sheet.jpg、keyframes/
用法：uv run scripts/analyze_video.py template/x.mp4 --out teardowns/2026-10-18-x
"""
import argparse, json, re, subprocess, sys, tempfile
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def probe(path):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type,width,height,r_frame_rate",
             "-of", "json", str(path)])
    d = json.loads(r.stdout)
    v = next(s for s in d["streams"] if s["codec_type"] == "video")
    num, den = v["r_frame_rate"].split("/")
    return {"duration": float(d["format"]["duration"]), "width": v["width"], "height": v["height"],
            "fps": round(float(num) / float(den), 3),
            "has_audio": any(s["codec_type"] == "audio" for s in d["streams"])}


def scene_cuts(path, thr):
    r = run(["ffmpeg", "-i", str(path), "-vf", f"select='gt(scene,{thr})',showinfo", "-an", "-f", "null", "-"])
    return [round(float(t), 3) for t in re.findall(r"pts_time:([\d.]+)", r.stderr)]


def sample_frames(path, fps, size, tmp):
    out = Path(tmp) / "f_%05d.png"
    run(["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"fps={fps},scale={size}:-2", str(out)])
    return sorted(Path(tmp).glob("f_*.png"))


def motion_per_second(frames, fps):
    arrs = [np.asarray(Image.open(f).convert("L"), dtype=np.float32) for f in frames]
    diffs = [0.0] + [float(np.mean(np.abs(a - b))) for a, b in zip(arrs[1:], arrs[:-1])]
    per_sec = [round(float(np.mean(diffs[i:i + fps])), 2) for i in range(0, len(diffs), fps)]
    return per_sec


def palette(frames, k=6):
    imgs = [np.asarray(Image.open(f).convert("RGB")) for f in frames[:: max(1, len(frames) // 40)]]
    px = np.concatenate([i.reshape(-1, 3) for i in imgs])
    img = Image.fromarray(px.reshape(-1, 1, 3).astype(np.uint8))
    q = img.quantize(colors=k, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()[: k * 3]
    counts = sorted(q.getcolors(), reverse=True)
    main = [{"hex": "#%02x%02x%02x" % tuple(pal[i * 3:i * 3 + 3]), "pct": round(c / len(px) * 100, 1)} for c, i in counts]
    # 强调色：只统计高饱和像素，避免被大面积背景淹没
    f = px.astype(np.float32) / 255
    mx, mn = f.max(1), f.min(1)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    colorful = px[(sat > 0.45) & (mx > 0.35)]
    accent = []
    if len(colorful) > 50:
        ci = Image.fromarray(colorful.reshape(-1, 1, 3).astype(np.uint8)).quantize(colors=3, method=Image.Quantize.MEDIANCUT)
        cp = ci.getpalette()[:9]
        for c, i in sorted(ci.getcolors(), reverse=True):
            accent.append({"hex": "#%02x%02x%02x" % tuple(cp[i * 3:i * 3 + 3]), "pct_of_colorful": round(c / len(colorful) * 100, 1)})
    return main, accent, round(len(colorful) / len(px) * 100, 2)


def keyframes(path, times, outdir):
    outdir.mkdir(parents=True, exist_ok=True)
    paths = []
    for i, t in enumerate(times):
        p = outdir / f"kf_{i:03d}_{t:07.2f}s.jpg"
        run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", str(path), "-frames:v", "1", "-vf", "scale=360:-2", str(p)])
        if p.exists():
            paths.append(p)
    return paths


def contact_sheet(path, duration, out, step=3, cols=6):
    with tempfile.TemporaryDirectory() as tmp:
        times = list(np.arange(0, duration, step))
        tiles = []
        for t in times:
            p = Path(tmp) / f"c_{t:.1f}.jpg"
            run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", str(path), "-frames:v", "1", "-vf", "scale=240:-2", str(p)])
            if p.exists():
                im = Image.open(p).convert("RGB")
                ImageDraw.Draw(im).text((6, 6), f"{t:.0f}s", fill=(255, 255, 0))
                tiles.append(im)
        if not tiles:
            return
        w, h = tiles[0].size
        rows = (len(tiles) + cols - 1) // cols
        sheet = Image.new("RGB", (w * cols, h * rows), (0, 0, 0))
        for i, im in enumerate(tiles):
            sheet.paste(im.resize((w, h)), ((i % cols) * w, (i // cols) * h))
        sheet.save(out, quality=85)


def loudness(path):
    r = run(["ffmpeg", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"])
    s = r.stderr[r.stderr.rfind("Summary:"):]
    g = lambda k: (m := re.search(k + r":\s+(-?[\d.]+)", s)) and float(m.group(1))
    return {"integrated_lufs": g("I"), "lra": g("LRA"), "true_peak_dbfs": g("Peak")}


def beats(path):
    try:
        import librosa
    except ImportError:
        return {"error": "librosa 未安装，用 uv run 运行即可自动安装"}
    with tempfile.TemporaryDirectory() as tmp:
        wav = Path(tmp) / "a.wav"
        run(["ffmpeg", "-v", "error", "-i", str(path), "-ac", "1", "-ar", "22050", str(wav)])
        y, sr = librosa.load(wav, sr=22050)
    tempo, bt = librosa.beat.beat_track(y=y, sr=sr)
    onset = librosa.onset.onset_strength(y=y, sr=sr)
    bt_times = librosa.frames_to_time(bt, sr=sr)
    strength = onset[bt] if len(bt) else np.array([])
    # 重拍：节拍点中能量最高的前 8 个
    top = sorted(np.argsort(strength)[-8:]) if len(strength) else []
    rms = librosa.feature.rms(y=y)[0]
    rt = librosa.frames_to_time(np.arange(len(rms)), sr=sr)
    # 换气点：RMS 低谷后急升
    drops = [round(float(rt[i]), 2) for i in range(10, len(rms) - 10)
             if rms[i] < np.percentile(rms, 15) and rms[i + 10] > np.percentile(rms, 70)]
    dedup = []
    for d in drops:
        if not dedup or d - dedup[-1] > 2:
            dedup.append(d)
    return {"bpm": round(float(np.atleast_1d(tempo)[0]), 1), "beat_count": int(len(bt_times)),
            "beats": [round(float(t), 2) for t in bt_times],
            "accent_beats": [round(float(bt_times[i]), 2) for i in top],
            "re_entry_points": dedup[:6]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--out", required=True)
    ap.add_argument("--scene", type=float, default=0.3, help="硬切阈值 0-1")
    ap.add_argument("--fps", type=int, default=5, help="运动分析采样帧率")
    a = ap.parse_args()
    v, out = Path(a.video), Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    info = probe(v)
    print("probe", info, file=sys.stderr)
    cuts = scene_cuts(v, a.scene)
    bounds = [0.0] + cuts + [info["duration"]]
    shots = [{"i": i, "start": round(s, 2), "end": round(e, 2), "len": round(e - s, 2)}
             for i, (s, e) in enumerate(zip(bounds[:-1], bounds[1:])) if e - s > 0.05]
    with tempfile.TemporaryDirectory() as tmp:
        frames = sample_frames(v, a.fps, 160, tmp)
        motion = motion_per_second(frames, a.fps)
        main_pal, accent, colorful_pct = palette(frames)
    peaks = sorted(range(len(motion)), key=lambda i: motion[i], reverse=True)[:5]
    keyframes(v, [max(0, (s["start"] + s["end"]) / 2) for s in shots], out / "keyframes")
    contact_sheet(v, info["duration"], out / "contact_sheet.jpg")
    res = {"file": v.name, "info": info,
           "shots": {"count": len(shots), "avg_len": round(info["duration"] / max(1, len(shots)), 2), "list": shots},
           "motion_per_second": motion, "motion_peaks_s": sorted(peaks),
           "palette": {"main": main_pal, "accent": accent, "colorful_pixel_pct": colorful_pct}}
    if info["has_audio"]:
        res["audio"] = {"loudness": loudness(v), "rhythm": beats(v)}
        acc = res["audio"]["rhythm"].get("accent_beats", [])
        # 对齐：重拍附近 ±0.15s 内是否有硬切
        res["sync"] = [{"beat": b, "cut_near": any(abs(b - c) <= 0.15 for c in cuts)} for b in acc]
    (out / "analysis.json").write_text(json.dumps(res, ensure_ascii=False, indent=2))
    print(f"OK → {out}/analysis.json  镜头 {len(shots)}  平均 {res['shots']['avg_len']}s  运动峰值 {sorted(peaks)}")


if __name__ == "__main__":
    main()
