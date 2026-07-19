# video-auto-cut 삽질 노트 (gotchas)

> AGENTS.md가 참조하는 파일. 삽질 발견 시 날짜와 함께 덧붙인다 (덮어쓰기 금지).
> 2026-07-19 생성 — 아래 초기 항목은 CLAUDE.md 주의사항에 이미 기록돼 있던 것을 이관.

- **bun이 PATH에 없음** — `~/.bun/bin/bun` 직접 지정 필요
- **실제 도구는 이 폴더 밖에 있음** — video-use = `~/Developer/video-use/`, hyperframes CLI = `~/Developer/hyperframes/packages/cli/dist/cli.js`. 이 폴더만 보고 "도구가 없다"고 판단하지 말 것
- ffmpeg는 N-123074 버전 설치돼 있음 / Node.js v24, Python 3.14 환경
- `.env`(API 키)·`*.mp4`·`edit/` 폴더는 git 커밋 금지 (키 노출·용량)
