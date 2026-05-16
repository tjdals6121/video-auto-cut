# 영상 자동화 컷편집 파이프라인

## 1줄 요약
영상 전사 → AI 컷편집(EDL) → 모션 그래픽 합성 → 최종 렌더링을 자동화하는 Python 파이프라인.

## 파일 구조
- `pipeline.py` — 전체 파이프라인 진입점
- `.env` — API 키 (git 커밋 금지)
- `edit/` — 전사 결과·EDL·렌더 출력 (git 커밋 금지)
- `*.mp4` — 원본 영상 (git 커밋 금지)

## 실행 방법
```bash
# 전사만
python pipeline.py --transcribe-only

# 전체 (EDL 있을 때)
python pipeline.py .

# 특정 폴더 + EDL 지정
python pipeline.py /path/to/videos --edl edit/edit.json
```

## 외부 의존성
- `~/Developer/video-use` — 전사·렌더 헬퍼
- `~/Developer/hyperframes` — 모션 그래픽 렌더러
- ElevenLabs API 키 → `.env`의 `ELEVENLABS_API_KEY`

## 행동 원칙
1. **Think First** — 가정 명시. 모호하면 질문, 추측 X.
2. **Simplicity** — 요청된 것만. 예측적 추상화 X.
3. **Surgical** — 변경된 모든 줄이 요청을 직접 추적.
4. **Goal-Driven** — 성공 기준 먼저 정의, 자동 검증.

## 핵심 룰
- `.env` 절대 커밋 금지 (API 키 포함)
- `*.mp4`, `edit/` 폴더 커밋 금지 (용량 큼)
- 파이프라인 4단계: 전사 → EDL 생성 → 모션 렌더 → 최종 렌더
- 버전 번호 변경 전 반드시 사용자 확인

## 참조
- 삽질 노트: `.claude/wiki/gotchas.md`
- 의사결정: `.claude/wiki/decisions.md`
