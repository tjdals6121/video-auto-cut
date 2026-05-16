"""base.mp4 위에 overlays + subtitles만 합성 (세그먼트 재추출 없음)"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path.home() / "Developer" / "video-use" / "helpers"))
from render import build_final_composite, resolve_path  # noqa: E402

PROJECT = Path(__file__).parent
EDL_PATH = PROJECT / "edit" / "edit.json"
BASE_PATH = PROJECT / "edit" / "base.mp4"
OUT_PATH  = PROJECT / "edit" / "final.mp4"

edl = json.loads(EDL_PATH.read_text(encoding="utf-8"))
edit_dir = EDL_PATH.parent

overlays = edl.get("overlays") or []

subs_path: Path | None = None
if edl.get("subtitles"):
    subs_path = resolve_path(edl["subtitles"], edit_dir)
    if not subs_path.exists():
        print(f"warning: SRT not found: {subs_path}")
        subs_path = None
    else:
        print(f"subtitles: {subs_path}")

print(f"overlays: {len(overlays)}")
for i, ov in enumerate(overlays):
    p = resolve_path(ov["file"], edit_dir)
    exists = p.exists()
    print(f"  [{i}] {ov.get('label','')}: {'OK' if exists else 'MISSING'}")

import subprocess

print("\nstarting composite...")
try:
    build_final_composite(BASE_PATH, overlays, subs_path, OUT_PATH, edit_dir)
    print(f"\ndone: {OUT_PATH}")
except subprocess.CalledProcessError as e:
    print("ffmpeg stderr:")
    print(e.stderr.decode("utf-8", errors="replace") if e.stderr else "(no stderr)")
    raise
