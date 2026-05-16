# 영상 자동화 컷편집 — 프로젝트 가이드

## 파이프라인 구조
```
원본 영상 → [video-use] 전사/컷편집 → EDL JSON
                                          ↓
모션 그래픽 ← [hyperframes] HTML 작성 ← 오버레이 명세
     ↓
[video-use render.py] 최종 합성 → final.mp4
```

## 핵심 도구 경로
- **video-use**: `~/Developer/video-use/` — Python, ffmpeg 기반 컷편집
- **hyperframes CLI**: `~/Developer/hyperframes/packages/cli/dist/cli.js`
- **파이프라인**: `pipeline.py` (전사 → EDL → 렌더)

## 스킬 사용법
- `/video-use` — AI와 대화로 컷편집 (전사, EDL 생성, 렌더)
- `/hyperframes` — HTML 기반 모션 그래픽 작성
- `/hyperframes-cli` — CLI 명령어 (init, preview, render)
- `/hyperframes-media` — TTS, 전사, 배경 제거
- `/gsap`, `/animejs`, `/lottie` — 애니메이션 엔진 선택

## 빠른 시작
```bash
# 1. 영상 폴더에서 전사만
python pipeline.py ./videos --transcribe-only

# 2. EDL 있으면 전체 파이프라인
python pipeline.py ./videos --edl ./videos/edit/edit.json

# 3. HyperFrames 모션 그래픽 생성
node ~/Developer/hyperframes/packages/cli/dist/cli.js init my-overlay
node ~/Developer/hyperframes/packages/cli/dist/cli.js preview  # 브라우저 미리보기
node ~/Developer/hyperframes/packages/cli/dist/cli.js render   # MP4 출력
```

## API 키 설정
`.env` 파일에 `ELEVENLABS_API_KEY=` 설정 필요 (전사 기능)

## EDL 형식 (video-use)
```json
{
  "sources": {"clip_id": "/path/to/file.mp4"},
  "ranges": [{"source": "clip_id", "start": 0.0, "end": 5.0, "beat": "HOOK"}],
  "grade": "warm_cinematic",
  "overlays": [{"file": "motion/output.mp4", "start_in_output": 0.0, "duration": 5.0}],
  "subtitles": null
}
```

## 주의사항
- ffmpeg 필수 설치됨 (N-123074 버전)
- Node.js v24, Python 3.14 환경
- bun은 `~/.bun/bin/bun` 경로 (PATH에 추가 필요)
- hyperframes 빌드 완료: `~/Developer/hyperframes/packages/cli/dist/cli.js`
- ⚠️ 버전 번호는 사용자에게 먼저 확인 후 결정
