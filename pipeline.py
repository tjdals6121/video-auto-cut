"""
영상 자동화 컷편집 파이프라인
video-use (전사/컷편집) + hyperframes (모션 그래픽) 통합
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

VIDEO_USE = Path.home() / "Developer" / "video-use"
HYPERFRAMES_CLI = Path.home() / "Developer" / "hyperframes" / "packages" / "cli" / "dist" / "cli.js"
HELPERS = VIDEO_USE / "helpers"
VENV_PYTHON = VIDEO_USE / ".venv" / "Scripts" / "python"


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, check=True, text=True, capture_output=False)


def transcribe(videos_dir: Path) -> Path:
    """원본 영상들을 전사하고 takes_packed.md 생성"""
    print("=== [1/4] 전사 시작 ===")
    run([str(VENV_PYTHON), str(HELPERS / "transcribe_batch.py"), str(videos_dir)])
    run([str(VENV_PYTHON), str(HELPERS / "pack_transcripts.py"), "--edit-dir", str(videos_dir / "edit")])
    packed = videos_dir / "edit" / "takes_packed.md"
    print(f"전사 완료: {packed}")
    return packed


def render_video(edl_path: Path, output: Path, subtitles: bool = True) -> Path:
    """EDL JSON으로 최종 영상 렌더링"""
    print("=== [3/4] 영상 렌더링 ===")
    cmd = [str(VENV_PYTHON), str(HELPERS / "render.py"), str(edl_path), "-o", str(output)]
    if subtitles:
        cmd.append("--build-subtitles")
    run(cmd)
    print(f"렌더 완료: {output}")
    return output


def create_motion(motion_dir: Path, name: str) -> Path:
    """HyperFrames 모션 그래픽 프로젝트 초기화"""
    print("=== [2/4] 모션 그래픽 프로젝트 생성 ===")
    project_dir = motion_dir / name
    if not project_dir.exists():
        run(["node", str(HYPERFRAMES_CLI), "init", name], cwd=motion_dir)
    return project_dir


def render_motion(motion_project: Path) -> Path:
    """HyperFrames HTML → MP4 렌더링"""
    print(f"모션 렌더링: {motion_project}")
    run(["node", str(HYPERFRAMES_CLI), "render"], cwd=motion_project)
    output = motion_project / "dist" / "output.mp4"
    return output


def run_pipeline(videos_dir: Path, edl_path: Path | None = None) -> None:
    """
    전체 파이프라인 실행

    1. 전사 → takes_packed.md
    2. EDL 로드 (없으면 안내 메시지)
    3. 모션 그래픽 렌더링 (EDL에 overlays 있으면)
    4. 최종 영상 렌더링
    """
    edit_dir = videos_dir / "edit"
    edit_dir.mkdir(exist_ok=True)

    packed = transcribe(videos_dir)
    print(f"\n전사 결과: {packed}")

    if edl_path is None:
        edl_path = edit_dir / "edit.json"

    if not edl_path.exists():
        print(f"""
=== EDL이 없습니다 ===
takes_packed.md를 참고하여 편집 계획을 세우고
{edl_path} 파일을 생성하세요.

EDL 형식:
{{
  "sources": {{"clip_id": "/path/to/file.mp4"}},
  "ranges": [
    {{"source": "clip_id", "start": 0.0, "end": 5.0, "beat": "HOOK", "quote": "...", "reason": "..."}}
  ],
  "grade": "warm_cinematic",
  "overlays": [],
  "subtitles": null
}}

/video-use 스킬로 AI와 대화하여 EDL을 자동 생성할 수 있습니다.
""")
        return

    edl = json.loads(edl_path.read_text(encoding="utf-8"))
    motion_dir = videos_dir / "motion"

    if edl.get("overlays"):
        motion_dir.mkdir(exist_ok=True)
        print(f"\n오버레이 {len(edl['overlays'])}개 감지됨")

    final = edit_dir / "final.mp4"
    render_video(edl_path, final, subtitles=bool(edl.get("subtitles") is not False))
    print(f"\n=== [4/4] 완료 ===\n최종 영상: {final}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="영상 자동화 컷편집 파이프라인")
    parser.add_argument("videos_dir", nargs="?", default=".", help="영상 폴더 경로")
    parser.add_argument("--edl", help="EDL JSON 경로 (선택)")
    parser.add_argument("--transcribe-only", action="store_true", help="전사만 실행")
    args = parser.parse_args()

    videos = Path(args.videos_dir).resolve()
    edl = Path(args.edl) if args.edl else None

    if args.transcribe_only:
        transcribe(videos)
    else:
        run_pipeline(videos, edl)
