# github-issues MCP (Antigravity 용)

`gh` CLI 가 없는 Windows 의 Antigravity 세션도 GitHub 이슈에 댓글을 달고 읽게 해 준다.
Python 표준 라이브러리만 쓴다. `pip install` 도, `gh` 설치도 필요 없다.

고치는 문제:

```
PS> gh issue comment 123 --repo cogito5170/AC --body '<agv:message ...>'
gh : The term 'gh' is not recognized ...  (CommandNotFoundException)
```

이제 에이전트는 셸에서 `gh` 를 부르지 않고 MCP 도구 `github_issue_comment` 를 부른다.
PowerShell 따옴표 문제(`'`, `"`, `<`, `>`, 한글)도 함께 사라진다. 본문은 JSON 으로 그대로 넘어간다.

## 도구

| 도구 | 하는 일 | 쓰기 |
|---|---|---|
| `github_whoami` | 인증 확인. 로그인 이름과 토큰 출처(env / git-credential)만 돌려준다. 토큰은 돌려주지 않는다. | |
| `github_issue_comment` | 이슈에 댓글 달기 (`gh issue comment` 대신). 인자: `repo`, `issue_number`, `body` | ✔ |
| `github_issue_comments` | 이슈의 최근 댓글 읽기. 인자: `repo`, `issue_number`, `limit`(기본 10), `since`(ISO 8601) | |
| `github_issue_create` | 새 이슈 열기. 인자: `repo`, `title`, `body` | ✔ |
| `github_issues_list` | 이슈 목록 보기 (번호 찾기용). 인자: `repo`, `state` | |

쓰기는 `GH_ALLOWED_REPOS` 에 맞는 repo 에만 허용된다. 기본값은 `cogito5170/*` 이다.
쉼표로 여러 개를 줄 수 있고, `owner/*` 꼴을 쓸 수 있으며, `*` 는 전부 허용이다.

## 설치 (Windows)

1. **Python 3.8 이상**이 있는지 확인한다.

   ```powershell
   py -3 --version
   ```

   없으면 `winget install Python.Python.3.12` 로 설치한다.

2. **파일을 하나 받는다.** 이 repo 의 `mcp/github_issues_mcp.py` 를 원하는 곳에 둔다.
   예: `C:\tools\github_issues_mcp.py`

3. **토큰을 준비한다.** 둘 중 하나를 고른다. 토큰을 채팅이나 에이전트에 붙여넣지 않는다.

   - **(가) 이미 `git push` 로 github.com 에 로그인한 적이 있다면 할 일이 없다.**
     서버가 `git credential fill` 로 Git Credential Manager 에 저장된 자격을 조용히 꺼내 쓴다.
     창이 뜨지 않고, 저장된 것이 없으면 실패만 한다.
   - **(나) 직접 토큰을 쓴다.**
     1. GitHub → Settings → Developer settings → *Fine-grained personal access token* 에서 토큰을 만든다.
        Repository access 는 `cogito5170` 의 필요한 repo 만 고르고, 권한은 **Issues: Read and write** 만 준다.
     2. **본인 PowerShell 에서** 사용자 환경 변수로 저장한다.

        ```powershell
        setx GITHUB_TOKEN "github_pat_..."
        ```

     3. Antigravity 를 완전히 껐다 켠다. 그래야 새 환경 변수를 읽는다.

4. **Antigravity 에 등록한다.** 전역 설정은 `%USERPROFILE%\.gemini\config\mcp_config.json`,
   작업 공간 설정은 `<workspace>\.agents\mcp_config.json` 이다.
   Antigravity 의 *MCP Servers → Manage → View raw config* 로 열어도 된다.

   ```json
   {
     "mcpServers": {
       "github-issues": {
         "command": "py",
         "args": ["-3", "C:\\tools\\github_issues_mcp.py"],
         "env": { "GH_ALLOWED_REPOS": "cogito5170/*" }
       }
     }
   }
   ```

   - `py` 가 없으면 `"command": "python"`, `"args": ["C:\\tools\\github_issues_mcp.py"]` 로 바꾼다.
   - 토큰을 `env` 에 직접 적을 수도 있지만, 이 파일은 평문이다. (나)의 `setx` 쪽을 권한다.

5. **확인한다.** 에이전트에게 *"github_whoami 를 불러라"* 라고 말한다.
   `{"login": "...", "token_source": "env" | "git-credential"}` 가 나오면 끝이다.

## 실패했던 댓글 다시 보내기

에이전트에게 이렇게 지시한다.

> `gh` 대신 `github_issue_comment` 도구로 `repo="cogito5170/AC"`, `issue_number=123`,
> `body="<agv:message sender=\"agv-session\" target=\"baseline\" status=\"ready\">…</agv:message>"` 를 보내라.

도구는 `{"id": …, "url": "https://github.com/…#issuecomment-…", "created_at": …}` 를 돌려준다.

## 주의: baseline 이 읽는 곳

baseline 은 **`cogito5170/baseline` 의 세션 통로 이슈**를 **`ga` 꼴**(` ```ga ` 블록의 `report/2` · `notify/1`)로 읽는다.
`cogito5170/AC#123` 에 단 `<agv:message>` 는 baseline 의 통로 밖이고 꼴도 다르다. 그래서 baseline 에 닿지 않을 수 있다.
Antigravity 세션을 baseline 에 붙이려면, 먼저 baseline 에서 통로 이슈 번호와 꼴을 받아야 한다.
→ [`../COMMS.md`](../COMMS.md)

## 보안

- 토큰은 출력 · 로그 · 도구 결과에 나오지 않는다. GitHub 오류 메시지에 섞여 와도 `***` 로 가린다.
- 쓰기는 `GH_ALLOWED_REPOS` 밖으로 나가지 않는다.
- 본문은 60,000 자까지만 받는다. GitHub 한도는 65,536 자다.
- 테스트할 때는 `GITHUB_API_URL` 로 API 주소를 바꿀 수 있다. 기본값은 `https://api.github.com` 이다.

## 테스트

```
python3 mcp/test_github_issues_mcp.py -v
```

가짜 GitHub 서버를 띄우고 다음을 확인한다.

- initialize · tools/list · tools/call 흐름
- Bearer 헤더와 UTF-8 본문
- 허용 목록, 인자 검사
- 토큰 가리기
- 토큰이 없을 때의 오류
- git-credential 대체 경로
