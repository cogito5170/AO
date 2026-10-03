# COMMS — baseline ↔ AO 관계와 통신 (읽기 전용 사본)

> 원본(구속력)은 baseline 의 **CMD-AO1 rev 2**([baseline#18](https://github.com/cogito5170/baseline/issues/18), BD-251 · rev 2 BD-253)과 `HUB_CLASSES.md` §5 다.
> 이 파일은 그것을 옮겨 적은 것이다. 다르면 원본이 이긴다. AO 는 이 규칙을 스스로 바꾸지 않는다.

| | 규칙 | 출처 |
|---|---|---|
| S1 지휘 | baseline 이 AO 를 지휘한다(`CMD-AO<n>`). **사용자 > baseline > AO.** 사용자가 AO 에 직접 지시하면 따르고 곧바로 #18 에 적는다. baseline 지시와 부딪히면 사용자를 따르고 #18 에 그렇다고 적는다(baseline 이 맞춘다) | CMD-AO1 S1 |
| S2 자율 범위 | AO 는 baseline 이 맡긴 절차(HUB_CLASSES P-번호) 안의 실행 세부만 정한다. 판정 · 지시 · 소유 · DECISION_LOG/BASELINE/HUMAN_QUEUE 쓰기 · 세션 만들기/닫기 · (그림자 동안) 다른 세션에 메시지 — 하지 않는다 | S2 |
| S3 질문 · 막힘 | baseline 에게 #18 로. 사용자에게 직접 묻지 않는다. 사람 몫은 baseline 이 HUMAN_QUEUE 에 올린다 | S3 |
| S4 통로 | AO 는 #18 에만 쓴다. 다른 통로는 읽기만. amp#1 은 baseline 몫(AO 의 `not_covered` 아님) | S4 |
| S5 깨우기 | AO → baseline `notify/1` 은 결정이 필요한 글에만: 요청 · 충돌 · 6 회차 비교 · **30 분 넘게 기다린 P2 항목**. 평상 회차는 알림 없음. baseline → AO: #18 댓글 + AO 세션에 `notify/1` | S5 |
| S6 꼴 | 상태는 `report/2` 로 감싼다: 절차마다 items D1.., 수는 results, 문제는 blockers. ao-status 전용 ga 꼴은 나중에 GA 가 | S6 |
| S7 조용한 회차 | 바뀐 것이 없으면 #18 에 한 줄 `round N: no change` | S7 |
| S8 '답함' (rev 2) | 같은 통로의 뒤 baseline 글이 그 보고를 **링크 · 인용하거나, 그 보고가 처리한 CMD id 를 부르면**(`CMD-` 있든 없든) 답으로 친다. 보고가 rev 를 적었으면 rev 와 함께 — rev 를 붙여 부른 경우 그 rev 가 같아야 하고, rev 없이 부르면 친다(AO 의 해석, baseline 확인 — CMD-AO1 done). CMD id 가 없는 상태 글은 링크 · 인용 또는 #18 의 baseline 처분(답한 글 링크 · 대체됨 · 답 필요 없음)이 있어야 한다 — 처분은 [`shadow/dispositions.json`](shadow/dispositions.json) 에 출처와 함께 옮긴다. DECISION_LOG 만으로는 답이 아니다. baseline 의 중계 글은 본문 어디에 있든 그 안의 ```ga 블록으로 검사한다 | S8 rev 2 |

세션: AO `session_01JWUCzhkqtsYpyJ6PyRq9cA` · baseline `session_013GnrUQPpcfK4ea1a1Y6SuY`. 언어: 세션 사이 영어(BD-175).
