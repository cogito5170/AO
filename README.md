# AO
Agent Orchestration — baseline 을 위한 Agent Orchestrator.

- 설계 · 책임 경계: [`ARCHITECTURE.md`](ARCHITECTURE.md) (제안, baseline 판정 대기)
- 통신 규칙: [`COMMS.md`](COMMS.md) (baseline CMD-AO1, BD-251). 통로: baseline#18 하나.
- 원칙: baseline 은 Authority(목표 · 정책 · 판정 · 기록), AO 는 Orchestration(감시 · 전달 · 재시도 · 수명 · 재현 · 집계). AO 는 판정하지 않는다.
