# AO — Agent Orchestrator: 책임 경계 조사와 재정의 제안 (ao-arch-1 rev 1, 2026-10-03)

> 상태: **제안(Proposal)**. 아직 아무 책임도 옮기지 않았다. 옮길지 · 언제 · 어디까지는 baseline 이 정한다(BD 로 기록).
> AO 세션: `session_01JWUCzhkqtsYpyJ6PyRq9cA` · 저장소 `cogito5170/AO` · 통신 머리 `<AO>` / `[AO]`.
> 근거 표기: `DL:n` = baseline `DECISION_LOG.md` 줄, `BD-n` = 결정 번호, 그 밖은 `파일:줄`.

## 0. 이 시스템에서 "Agent" 는 무엇인가

이 저장소군에는 **두 개의 고리**가 있다. 섞으면 설계가 틀어진다.

| | 제품 고리 (짓는 것) | 메타 고리 (세션 운영) |
|---|---|---|
| 무엇 | Sensor → Telemetry → State → **DecisionContext** → Policy → Validate/Arbitrate/Guard → Execute → Verify (BASELINE §2 · §8) | baseline(허브) → 지시 → 작업 세션 → 보고+evidence → 판정 → 다음 (GUIDANCE 16 · PROTOCOL §1) |
| Agent | 제품 안의 LLM Policy 실행기 | **Claude Code Remote 세션** (Telemetry · Sensor · DC · MS · Action · Guard · Health · SDK · GA · AMP · GR · GMG · WUG · W1 · VER) |
| 이번 재정의의 대상 | **아니다** (DC · ReAct 는 제품 기능으로 그대로) | **이것이다** |

AO 는 **메타 고리의 Orchestrator** 다. 제품의 DecisionContext · Policy · Guard 에는 손대지 않는다.

---

## [Current Baseline Responsibilities]

baseline 세션(`session_013GnrUQPpcfK4ea1a1Y6SuY`)이 지금 직접 하는 일. 출처는 PROTOCOL.md, 매시 트리거 `trig_01RsSwQxwd5TuzF6ihnuEE8d` 의 프롬프트, DECISION_LOG.

| # | 책임 | 지금 어떻게 | 근거 | 성격 |
|---|---|---|---|---|
| 1 | 전체 상태 판단 · 기준선 유지 | BASELINE.md · §13 회차 기록 | PROTOCOL §4.3 | **Authority** |
| 2 | Task 분해 · 지시 작성 | `directive/2` (scope S-n · done_when D-n · budget) | PROTOCOL §3 · §3a | **Authority** |
| 3 | 어떤 세션이 할지 (소유 표) | PROTOCOL §5 파일 하나에 세션 하나 | BD-45 | **Authority** |
| 4 | Agent 생성 | 작업 세션은 **사용자가 만든다(게이트 7)**. baseline 이 만든 것은 GA8 시험 1 개뿐. VER 생성 규칙은 있으나 한 번도 안 만듦 | BD-164 DL:287 · BD-143/144 · VERIFIER.md | 실행 |
| 5 | 배치 (저장소 · 브랜치 · 모델 · 예산) | 지시마다 budget(claude_p_runs 등) · 모델 고정(haiku · gemini-3-flash-preview) | BD-143 · 161 · 220 | 실행 (예산 한도는 Authority) |
| 6 | Lifecycle | archive 규칙은 GA8 · VER 만. interrupt/unarchive 규칙 없음. idle 은 사후 대응(W1 규칙 D) | BD-197 · 208 · 236 · 240 | 실행 |
| 7 | 상태 polling | 매시 안전망: (0) list_sessions 로 막힘 탐지 · (0b) W1 기록 관찰 · (0c) VER 판단 · (1) 13 개 저장소 fetch + 열린 이슈 전부에서 미판정 보고 찾기. 그리고 **프롬프트마다 모든 저장소 · 브랜치 · 이슈를 다시 읽는다** | 트리거 프롬프트 · PROTOCOL §4.3 · BD-160 · 180 · 194 · 238 | 실행 |
| 8 | retry / timeout | 지시 rev N 재발행(GA21 rev 3, AMP1 rev 8 …) · 놓친 깨우기 재알림 · 머리 고침 요청 · quota 대기(Gemini 20/일) 후 재시도 트리거 | PROTOCOL §3a · BD-176 · 222 · 224 | 재알림·대기 = 실행 / rev 내용 = Authority |
| 9 | 결과 수집 | 이슈 13 개 + amp#1 을 손으로 훑음. 늦게 읽은 사고 2 회 | BD-160 · 180 | 실행 |
| 10 | 결과 검증 | 보고마다 `ga check` → 빈 venv + pip check → 새 clone 시험 → 변이 1 개 이상 → 원본 대조. 하루 ~25 판정을 직렬로, 사실 오류 1 회 | BD-230 · 232 · 237 | 재현 = 실행 / 판정 = Authority |
| 11 | 통합 | 세션 브랜치 → `claude/gracious-meitner-vp49xe` ff/merge, 옆 저장소와 시험, 순서 결정(K12→GR6→GA21) | PROTOCOL §4 · BD-228 | 순서·서명 = Authority / 병합 실행 = 실행 |
| 12 | Agent 간 관계 조정 | 세션 간 교신은 예외만, 반드시 보고 | BD-133 PROTOCOL §1a | **Authority** |
| 13 | 사람 몫 관리 | HUMAN_QUEUE 올림 · 끝남 확인(매시) | BD-205 | 올릴지 = Authority / 끝남 확인 = 실행 |
| 14 | 최종 action | 판정 5 분류 · 기록 · 사용자 게이트 | PROTOCOL §3 | **Authority** |

**병목의 실체.** 위 7 · 8 · 9 · 10(재현) · 13(확인)이 매시 + 매 프롬프트 반복되고, 세션 수에 비례해 늘어난다. 기록된 증상: 보고 늦게 읽음 2 회(BD-160 · 180), 직렬 판정 ~25/일 + 사실 오류(BD-232), W1 기록을 손으로 셈(BD-238 · 240).

---

## [Responsibilities to Move to Orchestrator]

모두 **execution-level** 이다. 내용 · 의미 · 판정을 바꾸지 않는다.

| AO 가 맡을 것 | 지금 위치 | AO 에서의 꼴 | AO 가 하지 않는 것 |
|---|---|---|---|
| A1 세션 상태 감시 | 안전망 (0) | 매 회차 `list_sessions` · 상태 bucket · 막힘 라벨 → `ao-status/1` | 막힘의 해결 방법 고르기 |
| A2 미판정 보고 수집 | 안전망 (1) | 열린 이슈 전부 + amp#1 에서 `report/2` 중 baseline 판정 없는 것 → 대기열(링크 · 도착 시각 · 대기 시간). 시간 창 · "마지막 댓글 뒤" 로 거르지 않는다(BD-160 · 180 그대로) | 보고 내용 요약을 판정처럼 쓰기 |
| A3 머리 사전 검사 | PROTOCOL §3a | `ga.forms.validate` 결과를 대기열 항목에 붙임. 고침 요청은 **baseline 결정 뒤에만** AO 가 보냄(아래 P2) | 머리를 고쳐 주기 · 통과로 바꾸기 |
| A4 W1 관찰 | 안전망 (0b) | W1 기록만 읽어 한 줄(도구 수 · 거부 규칙 · 허락 · 보고 도달). **W1 에 말하지 않는다**(BD-238) | 개입 · 재알림 |
| A5 깨우기 전달 · 재알림 | PROTOCOL §1 · GA_UNIFIED §4 | baseline 이 쓴 지시 댓글을 가리키는 `notify/1` 전달, 창 안에 보고가 없으면 **같은 ref 로 1 회** 재알림 | 지시 내용 변경 · rev 올리기 |
| A6 검증 담당(VER) 수명 | VERIFIER.md | ≥3 대기 또는 30 분 대기 → VER 생성(최대 2) · 넘김 · 30 분 idle 뒤 archive. VER 초안은 **그대로** baseline 에 | 초안 채택 · 서명 |
| A7 재현 실행 | 판정 전 baseline 손작업 | 빈 venv · pip check · 새 clone 시험 · 변이 → evidence(명령 · 수 · 로그 경로 · sha) | 성공/실패 분류 |
| A8 자원 일정 | quota 대기 트리거(GMG6 00:15) | quota 창(Gemini 20/일 · Claude 5h/7d)에 맞춰 실행을 미루고 재개 | 예산 한도 바꾸기 |
| A9 사람 몫 끝남 확인 | HUMAN_QUEUE 매시 | Q-n 의 링크 상태(커밋 · 설정) 확인 → "끝난 것 같음 + evidence" 보고 | 표를 직접 고치기(표의 주인은 baseline) |
| A10 집계 | baseline 머릿속 | `ao-result/1` 로 task 별 attempts · 결과 · evidence 묶음 | 결과 사이 선택(Arbitration) |

---

## [Responsibilities Remaining in Baseline]

- 목표 · 정책 · 제약 — `directive/2` 의 goal · why · scope · done_when · budget (= **Task Contract**).
- 소유 표(PROTOCOL §5) · 세션 간 교신 허용(BD-133).
- **판정** 5 분류(성공 · 부분 성공 · 실패 · 막힘 · 정보 부족)와 그 서명. VER 초안을 받을 때도 머리 검사 + 변이 1 개는 스스로(VERIFIER.md 그대로).
- Arbitration — 결과가 갈리면 무엇을 채택하나.
- 통합 순서와 통합 브랜치 push 서명.
- DECISION_LOG · BASELINE §13 · HUMAN_QUEUE 의 쓰기.
- 사용자와의 대화 · 게이트(PR · 기본 브랜치 · 단계 닫기).
- 사용자 몫(게이트 7 작업 세션 생성 · 가드 · 환경 · 결제)은 지금처럼 **사람**에게. AO 로 옮기지 않는다.

---

## [New Communication Contract]

기존 `directive/2` · `report/2` · `notify/1` 은 **그대로 쓴다**(새 세션 쪽 꼴은 바뀌지 않는다). AO 와 baseline 사이에만 세 꼴을 더한다. 모두 `` ```ga `` 머리 안 JSON, 문자열은 영어(BD-175).

### `ao-task/1` (baseline → AO)

```json
{
  "schema": "ao-task/1",
  "task_id": "AOT-001",
  "ref": "https://github.com/cogito5170/baseline/issues/16#issuecomment-…",
  "objective": "verify_report",
  "constraints": ["no_fabrication", "actual_tool_only", "no_contact:W1"],
  "success_criteria": ["D1", "D2"],
  "allowed_actions": ["run_repro", "create_verifier", "renotify_once", "archive_verifier"],
  "budget": {"sessions": 1, "claude_p_runs": 0, "deadline_min": 60},
  "escalate_when": ["blocked", "budget_exhausted", "conflicting_results"]
}
```

`allowed_actions` 는 **닫힌 목록**이다: `observe_sessions` · `collect_reports` · `validate_headers` · `deliver_notify` · `renotify_once` · `create_verifier` · `archive_verifier` · `run_repro` · `schedule_after_quota` · `check_human_queue`. 목록에 없는 행동은 하지 않고 `blocked` 로 돌려준다.

### `ao-result/1` (AO → baseline)

```json
{
  "schema": "ao-result/1",
  "task_id": "AOT-001",
  "status": "completed",
  "attempts": 1,
  "results": [
    {"agent": "VER1", "session_id": "session_…", "status": "success",
     "evidence": ["sha 62af1a5", "tests 309/0/0", "mutation: drop --model -> 2 fail", "log: verify/AOT-001.log"],
     "draft_verdict": {"class": "success", "by": "VER1", "note": "draft only"}}
  ],
  "anomalies": []
}
```

- `status` 는 **실행 상태**다: `completed` · `failed` · `timeout` · `blocked` · `partial`. 판정 5 분류가 아니다.
- `final_decision` · `verdict` · `accepted` 칸은 **없다**. VER 의 초안은 `draft_verdict` 로 표시해 그대로 옮긴다.
- 모든 evidence 는 되짚을 수 있는 것(sha · 댓글 URL · 로그 경로 · 수)만. 되짚을 수 없으면 싣지 않는다.

### `ao-status/1` (AO → baseline, 회차마다 한 번)

```json
{
  "schema": "ao-status/1",
  "at": "2026-10-03T17:10Z",
  "sessions": {"working": 2, "blocked": [{"name": "W1", "label": "guard_D"}], "idle": 9},
  "pending_reports": [{"from": "GA", "ref": "…#issuecomment-…", "waiting_min": 42, "header": "ok"}],
  "stalled_directives": [{"id": "CMD-GA22", "since_min": 75, "renotified": false}],
  "human_queue": [{"q": "Q2", "looks_done": false}],
  "w1": "no change since 15:13:40"
}
```

### 깨우기

AO → baseline 은 기존 `notify/1` 에 `"from": "AO"` 를 더해 한 줄로: `{"schema":"notify/1","from":"AO","to":"baseline","kind":"ao-status","ref":"<댓글 링크>"}`.

---

## [State Ownership]

| State | Owner | 이 시스템의 실제 자리 |
|---|---|---|
| Global System State · 기준선 | Baseline | BASELINE.md · §13 |
| Global Policy · 원칙 | Baseline | PROTOCOL · GUIDANCE · VERIFIER |
| Objective · Task Contract | Baseline | `directive/2` 댓글 · `ao-task/1` |
| Final Decision · 해석 | Baseline | DECISION_LOG(BD) · 판정 댓글 |
| 통합 브랜치 머리 | Baseline (서명) | `claude/gracious-meitner-vp49xe` |
| 사람 몫 표 | Baseline | HUMAN_QUEUE.md |
| Agent lifecycle (VER · 시험 세션) | AO | AO 저장소 `state/agents.json` |
| Scheduling · placement · quota 창 | AO | AO 저장소 `state/schedule.json` · 트리거 |
| Retry 상태 (재알림 횟수) | AO | `state/retries.json` |
| 미판정 보고 대기열 · 세션 상태 집계 | AO | `ao-status/1` |
| 실행 상태 | Agent / AO | 작업 세션 · `ao-result/1` |
| Raw evidence | Agent | 각 세션 저장소의 커밋 · 시험 로그 |
| Aggregated execution result | AO | `ao-result/1` |
| 작업 세션 생성 (게이트 7) · 가드 · 환경 | **사람** | HUMAN_QUEUE |

각 계층은 자기가 소유하지 않은 state 를 authoritative 하게 바꾸지 않는다. AO 는 baseline 저장소에 **쓰지 않는다**(통로 댓글 · notify 만).

---

## [Implementation Changes]

모두 단계별 · 되돌릴 수 있게. 각 단계는 baseline 의 BD 로 열고 닫는다.

| 단계 | 바뀌는 것 | 끝난 기준 |
|---|---|---|
| **P0 (이번)** | AO 저장소에 이 문서. baseline 에 `[AO]` 통로 하나. 행동 변화 없음 | baseline 이 이 제안을 판정 |
| **P1 shadow** | AO 가 자기 트리거로 A1 · A2 · A4 · A9 를 돌려 `ao-status/1` 만 낸다. baseline 의 안전망은 **그대로**. 두 결과를 회차마다 견준다 | N 회차(제안: 6) 동안 미판정 보고 · 막힌 세션 목록이 baseline 과 100% 일치 (BD-160 · 180 사례를 재현 시험으로) |
| **P2 enforce** | baseline 안전망 프롬프트를 줄인다: (0)(0b)(1) 대신 "최신 `ao-status/1` 읽기 → 판정". AO 가 A3(머리 사전 검사) · A5(재알림 1 회)를 맡는다. AO 가 2 시간 조용하면 baseline 은 옛 안전망으로 돌아간다(fallback) | baseline 회차당 도구 호출 · 토큰 감소 측정, 놓친 보고 0 |
| **P3** | A6 VER 수명 · A7 재현 · A8 quota 일정을 `ao-task/1` 로 위임 | VER 초안과 baseline 서명 판정의 일치율 기록, 재현 evidence 되짚기 100% |
| **P4** | AO 의 runbook 을 GA_UNIFIED U4(허브 Autonomy) 명세로 넘긴다. ga 의 허브 연산(hub_dispatch · renotify · run_tests · enqueue_human)이 AO 의 손작업을 대신하면 AO 는 그 운영자가 된다 | 두 번째 관리자를 짓지 않음(BD-217) |

PROTOCOL 에 필요한 변경(baseline 이 쓸 것): §1 표에 `AO` 행, §5 소유 표에 `AO *` · `baseline AO 계약 = baseline`, §1 "모든 요청은 baseline 을 거친다" 에 "**전달 · 재알림 · 감시는 AO 가 대신할 수 있다. 지시 · 판정의 내용과 서명은 baseline**" 한 줄.

---

## [Potential Risks]

1. **두 번째 허브.** GA_UNIFIED U4 와 겹친다. → AO 는 코드 SDK 를 짓지 않고 운영 역할만, P4 에서 ga 로 수렴.
2. **게이트 7 · 분류기.** 작업 세션 생성은 사람 몫이고, 세션이 Agent 를 만드는 일은 "Create Unsafe Agents" 로 거부된 적이 있다(BD-169, BASELINE:603). → AO 는 VER(검증 전용, 쓰기 금지)만 만들고, 그것도 baseline `ao-task/1` + 사용자 확인 뒤. 작업 세션 생성은 계속 사람.
3. **세션이 AO 를 모른다.** WUG 는 "사용자가 아닌 세션의 지시" 를 거부했다(BD-227). → AO 는 지시를 **쓰지 않는다**. AO 의 메시지는 언제나 baseline 이 쓴 댓글을 가리키는 `notify/1` 이다. 새 세션의 첫 안내에 AO 를 적는 것은 사용자 몫.
4. **W1 실험 오염.** BD-238 은 W1 에 말하지 않는 관찰이다. → A4 는 읽기만, `no_contact:W1` 을 계약 제약으로, P1 시험에 "AO 의 send_message 대상에 W1 없음" 검사.
5. **이중 알림 · 이중 안전망.** baseline 과 AO 가 같은 세션을 깨우면 세션이 같은 일을 두 번 한다. → P1 은 AO 가 아무에게도 보내지 않는 shadow. P2 부터 재알림은 AO 만.
6. **재시도 증폭.** 턴 안 ReAct(같은 막힘 2 회 → 위로) × AO 재알림 × baseline rev. → AO 재알림은 지시당 1 회, ReAct 가 "허브로 올림" 신호를 낸 막힘은 AO 가 재시도하지 않고 바로 baseline 으로.
7. **감시자는 누가 감시하나.** AO 세션도 쉬면 낡는다. → baseline 트리거에 "AO 의 `ao-status/1` 이 2 시간 없으면 옛 안전망" 한 줄(fallback).
8. **권한 확장(authority creep).** 머리 고침 요청 · 재알림이 사실상 지시가 되는 것. → 닫힌 `allowed_actions`, `ao-result/1` 에 판정 칸 없음, 내용 변경 금지.
9. **비용 · quota.** AO 가 매시 13 저장소를 읽으면 토큰을 baseline 에서 AO 로 옮길 뿐일 수 있다. Gemini 20/일은 모든 세션이 나눠 쓴다. → P2 에서 baseline + AO 합계 토큰을 잰다. AO 는 Gemini 를 쓰지 않는다.
10. **지연.** 한 홉이 늘어난다. → 보고 깨우기는 지금처럼 baseline 에 바로 가게 두고, AO 는 놓친 것만 잡는다(P2 까지).

---

## [Tests Required]

| 시험 | 무엇을 보나 |
|---|---|
| T1 대기열 재현 | BD-160(이슈 범위 좁음) · BD-180(baseline 공지가 보고를 가림) 상황을 고정 자료로 → AO 가 둘 다 잡는다 |
| T2 shadow 일치 | P1 의 N 회차 동안 미판정 보고 · 막힌 세션 목록 = baseline 결과 (놓침 0, 거짓 양성 기록) |
| T3 계약 검사 | `ao-result/1` 에 `final_decision`/`verdict` 칸이 있으면 거부, `status` 가 실행 상태 집합 밖이면 거부 |
| T4 evidence 되짚기 | 모든 sha · 댓글 URL · 로그 경로가 실제로 있음 (지어낸 결과 0) |
| T5 W1 무접촉 | AO 의 send_message · 댓글 기록에 W1 · amp#1 대상 0 |
| T6 재알림 상한 | 지시당 재알림 ≤1, ReAct 가 올린 막힘은 재시도 0 |
| T7 VER 수명 규칙 | ≥3 대기 또는 30 분 → 생성, 동시 ≤2, idle 30 분 → archive, VER 은 baseline 저장소 · 통로에 쓰지 않음 |
| T8 fallback | AO 2 시간 침묵 → baseline 이 옛 안전망으로 돌아감 |
| T9 부하 측정 | P2 전후 baseline 회차당 도구 호출 · 토큰 · 판정 대기 시간 |
| T10 닫힌 행동 | `allowed_actions` 밖 행동 요청 → AO 가 하지 않고 `blocked` |
