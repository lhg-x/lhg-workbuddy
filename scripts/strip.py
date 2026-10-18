# /// script
# requires-python = ">=3.10"
# dependencies = ["pillow"]
# ///
"""动效切片：在时间窗内等间隔取 n 帧拼成一条，每格标"秒 + 相对帧号"，用来数入场/转场几帧完成、判断缓动。

用法：uv run scripts/strip.py template/x.mp4 --at 16.6 --span 1.2 --n 8 --out teardowns/x/strips/t16.6.jpg
"""
import argparse, json, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw


def fps_of(v):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate",
                        "-of", "json", v], capture_output=True, text=True)
    n, d = json.loads(r.stdout)["streams"][0]["r_frame_rate"].split("/")
    return float(n) / float(d)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("--at", type=float, required=True, help="窗口起点秒")
    ap.add_argument("--span", type=float, default=1.0); ap.add_argument("--n", type=int, default=8)
    ap.add_argument("--width", type=int, default=240); ap.add_argument("--out", required=True)
    a = ap.parse_args()
    fps = fps_of(a.video)
    tiles = []
    with tempfile.TemporaryDirectory() as tmp:
        for i in range(a.n):
            t = a.at + a.span * i / max(1, a.n - 1)
            p = Path(tmp) / f"{i}.jpg"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", a.video, "-frames:v", "1",
                            "-vf", f"scale={a.width}:-2", str(p)])
            if p.exists():
                im = Image.open(p).convert("RGB")
                ImageDraw.Draw(im).text((5, 5), f"{t:.2f}s +{round((t - a.at) * fps)}f", fill=(255, 255, 0))
                tiles.append(im)
    if not tiles:
        raise SystemExit("没有取到帧，检查 --at 是否超出时长")
    w, h = tiles[0].size
    strip = Image.new("RGB", (w * len(tiles), h))
    for i, im in enumerate(tiles):
        strip.paste(im, (i * w, 0))
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    strip.save(a.out, quality=88)
    print(f"OK → {a.out}  ({len(tiles)} 帧, {fps:.0f}fps)")


if __name__ == "__main__":
    main()
