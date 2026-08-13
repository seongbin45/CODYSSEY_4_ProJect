# Git 명령 사용 기록 (제출 증명용)

- 생성 시각: 2026-08-13 14:59:36
- 프로젝트: `C:\Users\seong\Downloads\CODYSSEY_4_ProJect`
- GitHub: https://github.com/seongbin45/CODYSSEY_4_ProJect.git
- user.name: `seongbin45`
- user.email: `sungbin45@office365.kunsan.ac.kr`
- 커밋 수: **27**
- merge 커밋 수: **1**

## 1. 계정 / 환경
```text
python -V
Python 3.10.11
python --version
Python 3.10.11
git --version
git version 2.53.0.windows.2
git config --global user.name "seongbin45"
git config --global user.email "sungbin45@office365.kunsan.ac.kr"
git config --global init.defaultBranch main
git config user.name  → seongbin45
git config user.email → sungbin45@office365.kunsan.ac.kr
snapshot: python=Python 3.10.11 | git=git version 2.53.0.windows.2 | user.name=seongbin45 | user.email=sungbin45@office365.kunsan.ac.kr
```

## 2. init / add / commit / origin / push
```text
git init
git add .
git commit -m "chore: 프로젝트 초기 설정 (.gitignore, README)"
git remote add origin https://github.com/seongbin45/CODYSSEY_4_ProJect.git
git remote -v
origin	https://github.com/seongbin45/CODYSSEY_4_ProJect.git (fetch)
origin	https://github.com/seongbin45/CODYSSEY_4_ProJect.git (push)
git push -u origin main
```

## 3. 기능 단위 커밋 (10개+)
```text
* d70bb27 (HEAD -> main, origin/main) 변경 사항 반영
* 5a8093d docs: 참고 저장소 링크 추가 (CODYSSEY 1~3, clone 샘플)
* 4964a9e docs: README에 proof 이미지를 Markdown 임베드 (![]())
* 236b441 docs: 평가자용 README 전면 재작성 (빠른 시작·기능·Git 증거)
* a3ab66c docs: Git 작업 증거 자료(proof/) 및 생성 스크립트 업로드
* 7ce8968 ui: 버튼·안내 문구를 기능명과 1:1로 명확화 (초심자용)
* dbf1786 변경 사항 반영
* 20e36fe chore: requirements.txt 추가 (PyQt5) 및 gitignore 예외
* 60de304 feat: PyQt GUI (app.py) — 평가자가 VS Code에서 바로 실행
* 3def54c docs: README pull 실습 메모 정리
* 64f771a docs: README 소폭 수정 (pull 실습)
* 27f1623 chore: 로컬 참고 파일 무시 규칙 보강
* ad8b822 docs: README에 기능 목록·실행 방법·프롬프트 출처 작성
* 1a45c42 feat(bonus): JSON 저장/불러오기, Markdown 내보내기 기능 추가
* ba71300 feat(bonus): 프롬프트 수정/삭제, 조회수 Top 기능 추가
*   0b62e68 merge: feature/show-list 브랜치 병합
|\  
| * 50f1278 feat: show_list 프롬프트 목록 기능 구현
|/  
* db764ac feat: main 함수에서 메뉴 분기 연결 (목록 제외)
* c1166a3 feat: toggle_favorite, show_favorites 즐겨찾기 기능 구현
* 0df0d7c feat: show_detail 상세 보기 기능 구현
* 235bc33 feat: search_prompt 키워드 검색 기능 구현
* effc516 feat: show_by_category 카테고리별 조회 기능 구현
* 897c343 feat: add_prompt 프롬프트 추가 기능 구현
* 196781e feat: input_nonempty, choose_category 입력 유틸 추가
* b7a0ed2 feat: show_menu 메뉴 화면 구현
* 7743368 feat: 프로그램 기본 골격과 이전 미션 프롬프트 3개 데이터 추가
* b432872 chore: 프로젝트 초기 설정 (.gitignore, README)
```

## 4. checkout / merge (feature/show-list)
```text
git checkout -b feature/show-list
git commit -m "feat: show_list 프롬프트 목록 기능 구현"
git checkout main
git merge --no-ff feature/show-list -m "merge: feature/show-list 브랜치 병합"
git branch -d feature/show-list
```

## 5. clone
```text
git clone https://github.com/seongbin45/Command-to-commit-changes-from-Git.git sample-clone-git-demo
git log --oneline -5
# 확인 후 삭제
```

## 6. pull
```text
git pull origin main
```

## 7. 현재 상태 (실측)
```text
On branch main
Your branch is up to date with 'origin/main'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   README.md
	modified:   main.py
	modified:   make_git_proof.py

no changes added to commit (use "git add" and/or "git commit -a")

* main d70bb27 [origin/main] 변경 사항 반영

git log --oneline --graph --decorate -20
* d70bb27 (HEAD -> main, origin/main) 변경 사항 반영
* 5a8093d docs: 참고 저장소 링크 추가 (CODYSSEY 1~3, clone 샘플)
* 4964a9e docs: README에 proof 이미지를 Markdown 임베드 (![]())
* 236b441 docs: 평가자용 README 전면 재작성 (빠른 시작·기능·Git 증거)
* a3ab66c docs: Git 작업 증거 자료(proof/) 및 생성 스크립트 업로드
* 7ce8968 ui: 버튼·안내 문구를 기능명과 1:1로 명확화 (초심자용)
* dbf1786 변경 사항 반영
* 20e36fe chore: requirements.txt 추가 (PyQt5) 및 gitignore 예외
* 60de304 feat: PyQt GUI (app.py) — 평가자가 VS Code에서 바로 실행
* 3def54c docs: README pull 실습 메모 정리
* 64f771a docs: README 소폭 수정 (pull 실습)
* 27f1623 chore: 로컬 참고 파일 무시 규칙 보강
* ad8b822 docs: README에 기능 목록·실행 방법·프롬프트 출처 작성
* 1a45c42 feat(bonus): JSON 저장/불러오기, Markdown 내보내기 기능 추가
* ba71300 feat(bonus): 프롬프트 수정/삭제, 조회수 Top 기능 추가
*   0b62e68 merge: feature/show-list 브랜치 병합
|\  
| * 50f1278 feat: show_list 프롬프트 목록 기능 구현
|/  
* db764ac feat: main 함수에서 메뉴 분기 연결 (목록 제외)
* c1166a3 feat: toggle_favorite, show_favorites 즐겨찾기 기능 구현
* 0df0d7c feat: show_detail 상세 보기 기능 구현
```

## 생성된 터미널 이미지

- `01_env_config.png`
- `02_init_add_commit_origin_push.png`
- `03_feature_commits.png`
- `04_checkout_merge.png`
- `05_clone.png`
- `06_pull.png`
- `07_final_verify.png`
- `08_checklist.png`
- `09_git_log_graph.png`
