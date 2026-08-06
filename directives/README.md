# directives/

이 폴더는 Claude(웹/모바일)가 작성한 Claude Code용 작업 지침 문서를 보관합니다.

- 이 저장소의 다른 파일(루트의 `*.txt`, `*-DIAGNOSE/`, `*-FIX/` 등)은 **증적(evidence)** 전용이며
  기존 원칙(공유 워킹트리 직접 커밋 금지, 임시 worktree 경유)이 그대로 적용됩니다.
- `directives/` 폴더는 **지시(directive)** 문서 전용이며, Claude(웹) 한 곳에서만 씁니다.
  Claude Code(터미널)는 이 폴더를 **읽기만** 합니다 — 여기 파일을 수정하거나 커밋하지 마세요.

## 사용법
1. Claude(웹)가 `directives/<작업명>.md` 파일을 생성해 push합니다.
2. 사용자는 터미널에 다음과 같이 입력합니다:
   ```
   verify 저장소 pull 받고 directives/<작업명>.md 읽어서 그대로 수행해줘
   ```
3. 완료보고는 기존 방식대로 verify 저장소 루트(또는 하위 폴더)에 별도 push합니다.
   (완료보고 자체를 `directives/` 안에 넣지 마세요 — 지시와 증적을 분리 유지)
