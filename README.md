# 나만의 프롬프트 관리 프로그램

> **Python & Git 기초 미션 (Codyssey)**  
> 이전 미션에서 쌓인 프롬프트를 등록·조회·검색·즐겨찾기하는 프로그램입니다.

| 항목 | 내용 |
|---|---|
| 저장소 | https://github.com/seongbin45/CODYSSEY_4_ProJect |
| 언어 | Python 3.10 이상 (`python -V` → Python 3.10.11) |
| Git | 2.53.0 · `user.name=seongbin45` · `user.email=sungbin45@office365.kunsan.ac.kr` |
| 필수 실행 | `main.py` (콘솔, 외부 라이브러리 없음) |
| 평가자 권장 실행 | `app.py` (PyQt GUI, 클릭만으로 기능 확인) |
| 브랜치 | `main` (목록 기능은 `feature/show-list` 에서 작업 후 merge) |
| merge 커밋 | `0b62e68` — `merge: feature/show-list 브랜치 병합` |

---

## 1. 평가자 빠른 시작 (3분)

### 방법 A — GUI (권장, 가장 쉬움)

1. 이 저장소를 연다 (Clone 또는 ZIP 해제).
2. VS Code에서 **`app.py`** 파일을 연다.
3. **Run ▶** 을 누르거나, 터미널에서 아래를 실행한다.

```bash
python app.py
```

- **PyQt5가 없으면** 첫 실행 시 자동 설치를 시도합니다.  
- 자동 설치가 안 되면 아래를 한 번만 실행하세요.

```bash
python -m pip install -r requirements.txt
```

4. 창이 열리면:
   - **왼쪽 목록**을 클릭 → 상세 보기 (메뉴 5)
   - 상단 **프롬프트 검색 / 목록 / 즐겨찾기 / 조회수 Top** 버튼 사용
   - 하단 **프롬프트 추가·수정·삭제**, **JSON 저장/불러오기** 등 사용

### 방법 B — 콘솔 (과제 필수 형태)

```bash
python main.py
```

메뉴 번호(0~12)를 입력해 기능을 선택합니다.  
**외부 라이브러리 없이** 표준 라이브러리만 사용합니다.

---

## 2. 이 프로그램이 하는 일

터미널(또는 GUI)에서 프롬프트를 관리합니다.

- 프롬프트 **추가 / 목록 / 카테고리별 조회 / 검색 / 상세 보기**
- **즐겨찾기** 추가·해제 및 즐겨찾기만 모아 보기
- (보너스) **수정·삭제**, **조회수 Top**, **JSON 저장·불러오기**, **Markdown 내보내기**

실행 중 데이터는 **메모리(리스트)** 에 유지됩니다.  
프로그램을 종료하면 초기화되며, **메뉴 10번(JSON으로 저장)** 으로 파일에 남길 수 있습니다.

---

## 3. 기능 목록 (콘솔 메뉴)

| 번호 | 기능 | 설명 | 구분 |
|:---:|---|---|---|
| 1 | 프롬프트 추가 | 제목 / 내용 / 카테고리 입력 후 등록 | 필수 |
| 2 | 프롬프트 목록 | 전체 목록을 번호와 함께 출력 | 필수 |
| 3 | 카테고리별 조회 | 선택한 카테고리만 출력 | 필수 |
| 4 | 프롬프트 검색 | 제목·내용 키워드 검색 | 필수 |
| 5 | 프롬프트 상세 보기 | 전체 내용 출력, 조회수 +1 | 필수 |
| 6 | 즐겨찾기 관리 | 즐겨찾기 추가 / 해제 | 필수 |
| 7 | 즐겨찾기 목록 | 즐겨찾기한 항목만 보기 | 필수 |
| 8 | 프롬프트 수정/삭제 | 기존 항목 편집 또는 삭제 | 보너스 |
| 9 | 조회수 Top 목록 | 조회수 높은 순 정렬 | 보너스 |
| 10 | JSON으로 저장 | `prompts.json` 에 저장 | 보너스 |
| 11 | JSON에서 불러오기 | `prompts.json` 복원 | 보너스 |
| 12 | Markdown 내보내기 | `exports/카테고리.md` 생성 | 보너스 |
| 0 | 종료 | 프로그램 종료 | 필수 |

### 카테고리

`텍스트 생성` · `이미지 생성` · `영상 생성` · `페르소나` · `자동화` · `기타`  
(추가 시 목록 선택 또는 **직접 입력** 가능)

---

## 4. GUI 버튼 ↔ 콘솔 메뉴 대응

`app.py` 버튼 이름은 **기능 이름과 동일**하게 맞춰 두었습니다.  
마우스를 버튼 위에 올리면 짧은 설명(툴팁)도 표시됩니다.

| GUI에서 보이는 이름 | 하는 일 | 콘솔 |
|---|---|:---:|
| 프롬프트 검색 | 제목·내용 키워드 검색 | 4 |
| 프롬프트 목록 (전체) | 전체 목록 다시 보기 | 2 |
| 즐겨찾기 목록 | 즐겨찾기만 모아 보기 | 7 |
| 조회수 Top 목록 | 조회수 높은 순 정렬 | 9 |
| 카테고리별 조회 (상단 콤보) | 카테고리 필터 | 3 |
| 왼쪽 목록 클릭 | 상세 보기 (조회수 +1) | 5 |
| 프롬프트 추가 | 새 프롬프트 등록 | 1 |
| 프롬프트 수정 | 선택 항목 편집 | 8 |
| 프롬프트 삭제 | 선택 항목 삭제 | 8 |
| 즐겨찾기 추가/해제 | 즐겨찾기 on/off | 6 |
| JSON으로 저장 | `prompts.json` 저장 | 10 |
| JSON에서 불러오기 | `prompts.json` 복원 | 11 |
| Markdown 파일로 내보내기 | `exports/` 폴더에 .md 생성 | 12 |

**단축키**

| 키 | 동작 |
|---|---|
| `Ctrl + N` | 프롬프트 추가 |
| `Ctrl + S` | JSON으로 저장 |
| `Ctrl + F` | 검색창으로 이동 |
| `F5` | 목록 새로고침 |

---

## 5. 기본 프롬프트 3개 (이전 미션 원문)

프로그램 시작 시 **이전 미션에서 실제 사용한 프롬프트 원문** 3개가 미리 등록되어 있습니다.

| # | 제목 | 카테고리 | 출처 저장소 · 파일 |
|:---:|---|---|---|
| 1 | 확인봇 - 창업지원 실무 이메일 코치 (1주차) | 페르소나 | [CODYSSEY_1_ProJect](https://github.com/seongbin45/CODYSSEY_1_ProJect) · `bot/prompts/system_prompt.md` |
| 2 | FinFit 광고 씬1 - 문제 제시 (Veo, 2주차) | 영상 생성 | [CODYSSEY_2_ProJect](https://github.com/seongbin45/CODYSSEY_2_ProJect) · `Docs/video_prompts_model_variants.md` (Veo 3.1) |
| 3 | 지출 메모 자동 분류 (Make/n8n, 3주차) | 자동화 | [Codyssey_3_ProJect](https://github.com/seongbin45/Codyssey_3_ProJect) · project1 n8n / Make OpenAI 시스템 프롬프트 |

각 프롬프트는 제목, 내용, 카테고리, 즐겨찾기 여부, 조회수를 가집니다.

### 참고한 저장소

| 구분 | 저장소 | 이 프로젝트에서의 역할 |
|---|---|---|
| 1주차 · 페르소나 프롬프트 | https://github.com/seongbin45/CODYSSEY_1_ProJect | 확인봇 시스템 프롬프트 원문 |
| 2주차 · 영상 프롬프트 | https://github.com/seongbin45/CODYSSEY_2_ProJect | FinFit Veo 씬1 프롬프트 원문 |
| 3주차 · 자동화 프롬프트 | https://github.com/seongbin45/Codyssey_3_ProJect | 지출 메모 자동 분류 시스템 프롬프트 원문 |
| Git clone 실습 샘플 | https://github.com/seongbin45/Command-to-commit-changes-from-Git | 공개 저장소 `git clone` 연습용 |
| CloneUp 실습 프로그램 | https://github.com/seongbin45/CloneUp | 공개 저장소 릴리스 탭, Window 프로그램 |
| 이번 미션 (본 저장소) | https://github.com/seongbin45/CODYSSEY_4_ProJect | 프롬프트 관리 프로그램 |

---

## 6. 프로젝트 구조

```
CODYSSEY_4_ProJect/
├── main.py              # 콘솔 프로그램 (필수) + 공통 데이터
├── app.py               # PyQt GUI (평가자 권장)
├── requirements.txt     # GUI용: PyQt5
├── README.md            # 이 문서
├── .gitignore
├── make_git_proof.py    # Git 증거 이미지 생성 스크립트
└── proof/               # Git 작업 증거 자료 (이미지·로그)
    ├── 01_env_config.png
    ├── 02_init_add_commit_origin_push.png
    ├── 03_feature_commits.png
    ├── 04_checkout_merge.png
    ├── 05_clone.png
    ├── 06_pull.png
    ├── 07_final_verify.png
    ├── 08_checklist.png
    ├── 09_git_log_graph.png
    └── git_command_log.md
```

실행 후 생성될 수 있는 파일(저장소에는 커밋하지 않음):

| 파일/폴더 | 설명 |
|---|---|
| `prompts.json` | 메뉴 10번으로 저장한 데이터 |
| `exports/` | 메뉴 12번 Markdown 내보내기 결과 |

---

## 7. 설계 의도 · 자료구조 · 동작 규칙

### 7.1 왜 리스트 + 딕셔너리인가 (선택 이유 · trade-off)

| 선택 | 이유 |
|---|---|
| **리스트 (`prompts`)** | 등록 순서를 그대로 유지하고, 메뉴 번호(1, 2, 3…)과 1:1로 대응하기 쉽습니다. 삽입(`append`)·삭제(`pop`)가 직관적입니다. |
| **딕셔너리 (각 항목)** | 한 프롬프트의 여러 속성(`title`, `content`, …)을 필드 이름으로 읽기 쉽습니다. |

| 관점 | 장점 | 단점 (한계) |
|---|---|---|
| 삽입 | 맨 뒤 추가 O(1)에 가깝고 구현이 단순 | 중간 삽입은 느릴 수 있음 (이 프로그램에선 거의 없음) |
| 검색 | 전체 순회 + 부분문자열로 충분 (데이터 수십~수백 건 가정) | 제목 인덱스가 없어 데이터가 매우 커지면 선형 탐색 비용 증가 |
| 정렬 | `sorted(..., key=views)` 로 조회수 Top 구현 용이 | 정렬 시 새 리스트 생성 (원본 순서는 목록 번호용으로 유지) |
| 대안 대비 | DB/클래스 없이 과제 범위(기본 문법)에 맞음 | 제목 유니크 제약·전문 검색 엔진 수준의 기능은 없음 |

**정리**: 학습·제출용 규모에서는 리스트+딕셔너리가 **구현 비용 대비 가독성·메뉴 번호 매핑**에 가장 유리합니다.

### 7.2 한 항목(필드) 사양

| 필드 | 타입 | 설명 | 기본값 |
|---|---|---|---|
| `title` | `str` | 제목 (비어 있으면 등록 불가) | — |
| `content` | `str` | 본문 (비어 있으면 등록 불가) | — |
| `category` | `str` | 카테고리 이름 | 잘못된 선택 시 `"기타"` |
| `favorite` | `bool` | 즐겨찾기 여부 | `False` |
| `views` | `int` | 상세 보기 횟수 | `0` |

### 7.3 동명(같은 제목) · 카테고리 충돌 규칙

| 상황 | 정책 |
|---|---|
| **같은 제목 중복 등록** | **허용**. 제목을 고유키로 쓰지 않습니다. 구분 기준은 **목록 번호(리스트 인덱스 + 1)** 입니다. |
| **같은 제목 + 다른 내용** | 둘 다 유지. 수정·삭제·즐겨찾기는 **번호로 지정한 항목**에만 적용됩니다. |
| **카테고리 직접 입력** | 앞뒤 공백은 `strip()` 으로 제거. 비어 있으면 `input_nonempty` 가 다시 받습니다. |
| **카테고리 목록 밖 값** | 직접 입력 문자열을 그대로 저장. 미리 정의된 6개와 **병합·자동 정규화하지 않음**. |
| **잘못된 카테고리 번호** | 안내 후 카테고리를 `"기타"` 로 등록. |
| **JSON 불러오기 시 충돌** | 파일 내용으로 **메모리 목록 전체를 교체** (`clear` 후 `extend`). 기존 항목과 제목 기준 병합은 하지 않습니다. |

### 7.4 입력 검증 규칙

| 입력 | 검증 |
|---|---|
| 제목 · 내용 | `input_nonempty`: 공백만 있으면 거부하고 재입력 |
| 카테고리 (번호) | 1~6 → 고정 목록, 7 → 직접 입력, 그 외 → `"기타"` |
| 카테고리 (직접 입력) | 비어 있으면 재입력 |
| 메뉴 번호 | `0`~`12` 만 처리, 그 외 `"잘못된 번호입니다"` 후 메뉴 재표시 |
| 목록 번호 (상세/즐겨찾기/수정삭제) | 숫자이며 1 ~ `len(prompts)` 범위인지 검사 |

### 7.5 검색 방식

- **부분 일치**: 키워드가 제목 **또는** 내용 문자열에 포함되면 매칭 (`in`).
- **대소문자**: `.lower()` 로 비교해 영문 대/소문자를 구분하지 않습니다.
- **공백·특수문자**: 별도 정규화(연속 공백 제거, 특수문자 무시)는 **하지 않습니다**. 입력한 그대로 부분 문자열 검색합니다.
- **한계**: 완전 일치 옵션·정규식·형태소 분석은 없습니다.

### 7.6 즐겨찾기 피드백 예시 (콘솔)

```text
'확인봇 - ...' 프롬프트를 즐겨찾기에서 추가했습니다!
'확인봇 - ...' 프롬프트를 즐겨찾기에서 해제했습니다!
```

(`favorite` 를 `not` 으로 토글한 뒤, True → 「추가」, False → 「해제」 문구)

### 7.7 프로그램 루프

`main()` 은 `while True` 로 메뉴를 반복 출력합니다.  
메뉴 **0** 을 고르면 종료 메시지를 출력하고 `break` 로 루프를 빠져나갑니다.  
(한 번 실행 후 끝나지 않고, 여러 기능을 이어서 쓰기 위한 구조입니다.)

### 7.8 주요 함수 책임 (한 줄)

| 함수 | 책임 (입력 → 동작 / 부수효과) |
|---|---|
| `show_menu` | 메뉴 0~12 출력 (선택 범위 안내 포함) |
| `input_nonempty` | 라벨 출력 → 비어 있지 않은 문자열 반환 |
| `choose_category` | 번호/직접입력 → 카테고리 문자열 반환 |
| `add_prompt` | 제목·내용·카테고리 입력 → `prompts` 에 append |
| `show_list` | 전체 목록 출력 (★/☆) |
| `show_by_category` | 카테고리 선택 → 해당 항목만 출력 |
| `search_prompt` | 키워드 → 제목·내용 부분일치 결과 출력 |
| `show_detail` | 번호 → 본문 출력, `views` +1 |
| `toggle_favorite` | 번호 → `favorite` 토글 + 안내 문구 |
| `show_favorites` | `favorite==True` 만 출력 |
| `edit_or_delete_prompt` | 번호 → 수정 또는 삭제 |
| `show_top_viewed` | `views` 내림차순 출력 |
| `save_to_json` / `load_from_json` | 파일 저장 / 메모리 교체 복원 |
| `export_to_markdown` | 카테고리별 `.md` 생성 |
| `main` | 메뉴 루프와 분기 |

### 7.9 JSON 스키마 · 영속화 방침

`prompts.json` 은 **객체 배열** 입니다.

```json
[
  {
    "title": "문자열",
    "content": "문자열",
    "category": "문자열",
    "favorite": true,
    "views": 0
  }
]
```

| 정책 | 내용 |
|---|---|
| 스키마 버전 필드 | 별도 `version` 키 없음 (학습용 단순 형식) |
| 불러오기 | 파일이 없거나 리스트가 아니면 오류 안내. 정상이면 **전체 교체** |
| 필드 누락 | 코드는 키 접근 시 기본값을 쓰는 GUI 경로가 있고, 콘솔은 정상 저장본을 전제 |
| 마이그레이션 | 구버전 변환 로직 없음. 수동으로 필드를 맞춘 뒤 불러오면 됨 |
| Git 추적 | `prompts.json` 은 `.gitignore` — 실행 결과물이며 제출 코드에 포함하지 않음 |

### 7.10 기술 스택 요약

- **콘솔(`main.py`)**: 외부 라이브러리 없음 (`json`, `os` 는 보너스 영속화·내보내기)
- **GUI(`app.py`)**: PyQt5, `main.py` 의 `prompts` 를 공유
- **추가 시 유효성**: 제목/내용 필수 → 실패 시 재입력(콘솔) 또는 경고 후 다이얼로그 유지(GUI)

---

## 8. Git 작업 기록 (평가 포인트)

### 환경 스냅샷 (실측)

```text
python -V
Python 3.10.11

git --version
git version 2.53.0.windows.2

git config user.name
seongbin45

git config user.email
sungbin45@office365.kunsan.ac.kr
```

한 줄 요약: `python=Python 3.10.11 | git=2.53.0.windows.2 | user.name=seongbin45 | user.email=sungbin45@office365.kunsan.ac.kr`

### 확인 방법

```bash
python -V
git log --oneline --graph --decorate
git rev-list --count HEAD          # 커밋 수 (10개 이상)
git rev-list --count --merges HEAD # merge 커밋 존재 여부
```

### 브랜치 · merge 요약

| 항목 | 값 |
|---|---|
| 기본 브랜치 | `main` |
| 기능 브랜치 | `feature/show-list` (프롬프트 목록 기능 전용) |
| merge 커밋 | **`0b62e68`** `merge: feature/show-list 브랜치 병합` |
| 브랜치 기준 | **기능 단위**로 브랜치를 만들고, 동작 확인 후 `main` 에 `--no-ff` merge. 단순 문서/설정 수정은 `main` 에서 직접 커밋 |

### 커밋 메시지 규칙 (예시)

```text
feat: 기능 추가          예) feat: show_list 프롬프트 목록 기능 구현
feat(bonus): 보너스      예) feat(bonus): JSON 저장/불러오기
fix: 문서               예) docs: README 평가자 안내
chore: 설정·잡무         예) chore: 프로젝트 초기 설정
merge: 브랜치 병합       예) merge: feature/show-list 브랜치 병합
```

### 사용한 Git 명령

| 명령 | 용도 |
|---|---|
| `git init` | 저장소 시작 |
| `git add` / `git commit` | 기능 단위 커밋 |
| `git remote add origin` / `git push` | GitHub 업로드 |
| `git checkout -b` / `git merge` | 브랜치 작업·병합 (`feature/show-list`) |
| `git clone` | 공개 샘플 저장소 내려받기 실습 |
| `git pull` | 원격 변경 반영 |

- **clone 실습 대상**: [Command-to-commit-changes-from-Git](https://github.com/seongbin45/Command-to-commit-changes-from-Git)  
  (기록: `proof/05_clone.png`, `proof/git_command_log.md`)  
- **프롬프트 목록(`show_list`)** 기능은 `feature/show-list` 브랜치에서 작업 후 **main에 merge** 했습니다.  
- 커밋은 기능 단위로 나뉘어 있으며, 그래프에 merge 분기가 보입니다.  

### 증거 자료 (`proof/` — README에 바로 표시)

GitHub에서 이 README를 열면 아래 이미지가 본문에 보입니다.  
문법: `![설명](proof/파일명.png)`

#### 01. 계정 · 환경 설정

![Git 계정/환경 설정](proof/01_env_config.png)

#### 02. init / add / commit / origin / push

![init add commit origin push](proof/02_init_add_commit_origin_push.png)

#### 03. 기능 단위 커밋

![기능 단위 커밋](proof/03_feature_commits.png)

#### 04. checkout / merge (feature/show-list)

![checkout merge](proof/04_checkout_merge.png)

#### 05. clone

![git clone](proof/05_clone.png)

#### 06. pull

![git pull](proof/06_pull.png)

#### 07. 최종 검증 (실측)

![최종 검증](proof/07_final_verify.png)

#### 08. 요건 체크리스트

![체크리스트](proof/08_checklist.png)

#### 09. git log --graph

![git log graph](proof/09_git_log_graph.png)

#### 텍스트 로그

- 상세 명령 기록: [`proof/git_command_log.md`](proof/git_command_log.md)

이미지를 다시 만들려면:

```bash
python -m pip install pillow
python make_git_proof.py
```

---

## 9. 환경 요구 사항

| 항목 | 요구 |
|---|---|
| Python | 3.10 이상 |
| Git | 설치 및 사용자 이름·이메일 설정 |
| 콘솔 버전 | 추가 패키지 **없음** |
| GUI 버전 | `PyQt5` (`requirements.txt`) |

사용자 정보 확인 예 (원문 명령):

```bash
python -V
python --version
git --version
git config user.name
git config user.email
```

실측 결과 예:

```text
python -V          → Python 3.10.11
git --version      → git version 2.53.0.windows.2
git config user.name  → seongbin45
git config user.email → sungbin45@office365.kunsan.ac.kr
```

---

## 10. 문제 해결

| 증상 | 해결 |
|---|---|
| `app.py` 실행 시 PyQt 오류 | `python -m pip install PyQt5` 후 다시 실행 |
| `python` 을 찾을 수 없음 | VS Code 우측 하단에서 Python 3.10 인터프리터 선택 |
| 한글이 깨짐 | 터미널 인코딩 UTF-8, 파일 저장 인코딩 UTF-8 확인 |
| JSON 불러오기 실패 | 먼저 [JSON으로 저장]을 한 번 실행했는지 확인 |

---

## 11. 라이선스 / 작성

- 학습 미션 제출용 개인 프로젝트입니다.
- 작성: seongbin45  
- 원격 저장소: https://github.com/seongbin45/CODYSSEY_4_ProJect
