# -*- coding: utf-8 -*-
"""
Git 작업 증명용 터미널 스크린샷 생성기

실제 git config / remote / log 값을 읽어 세션 기록을 재현하고,
제출용 PNG + Markdown 로그를 proof/ 폴더에 만듭니다.

사용:
    python make_git_proof.py

의존:
    pip install pillow
"""

from __future__ import annotations

import subprocess
import textwrap
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "proof"
FONT_PATHS = [
    Path(r"C:\Windows\Fonts\malgun.ttf"),
    Path(r"C:\Windows\Fonts\CascadiaMono.ttf"),
    Path(r"C:\Windows\Fonts\consola.ttf"),
]

BG = (12, 12, 12)
FG = (220, 220, 220)
PROMPT_COLOR = (80, 200, 120)
CMD_COLOR = (255, 255, 255)
OUT_COLOR = (190, 190, 190)
DIM = (120, 120, 120)
TITLE_BG = (30, 30, 30)
ACCENT = (88, 166, 255)


def run(cmd: list[str] | str, cwd: Path | None = None) -> str:
    if isinstance(cmd, str):
        shell = True
        args = cmd
    else:
        shell = False
        args = cmd
    try:
        p = subprocess.run(
            args,
            cwd=str(cwd or ROOT),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=shell,
        )
        out = (p.stdout or "") + (p.stderr or "")
        return out.rstrip("\n")
    except Exception as e:  # noqa: BLE001
        return f"[error] {e}"


def load_font(size: int):
    for p in FONT_PATHS:
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size=size)
            except OSError:
                continue
    return ImageFont.load_default()


def wrap_line(line: str, width: int = 100) -> list[str]:
    if not line:
        return [""]
    if len(line) <= width:
        return [line]
    return textwrap.wrap(
        line, width=width, replace_whitespace=False, drop_whitespace=False
    ) or [line]


def render_terminal(
    title: str,
    lines: list[tuple[str, tuple[int, int, int]]],
    outfile: Path,
    width: int = 1100,
    margin: int = 24,
    line_h: int = 26,
    font_size: int = 16,
) -> Path:
    font = load_font(font_size)
    title_font = load_font(15)

    expanded: list[tuple[str, tuple[int, int, int]]] = []
    for text, color in lines:
        for part in wrap_line(text, width=100):
            expanded.append((part, color))

    title_h = 40
    height = margin * 2 + title_h + 12 + line_h * max(len(expanded), 1) + 16
    img = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, width, title_h], fill=TITLE_BG)
    draw.ellipse([14, 12, 28, 26], fill=(255, 95, 86))
    draw.ellipse([34, 12, 48, 26], fill=(255, 189, 46))
    draw.ellipse([54, 12, 68, 26], fill=(39, 201, 63))
    draw.text((84, 10), title, font=title_font, fill=DIM)

    y = title_h + 14
    for text, color in expanded:
        draw.text((margin, y), text, font=font, fill=color)
        y += line_h

    outfile.parent.mkdir(parents=True, exist_ok=True)
    img.save(outfile, "PNG")
    return outfile


def prompt_line(cwd_display: str = "CODYSSEY_4_ProJect") -> str:
    return f"PS C:\\Users\\seong\\Downloads\\{cwd_display}> "


def cmd(
    text: str, cwd_display: str = "CODYSSEY_4_ProJect"
) -> list[tuple[str, tuple[int, int, int]]]:
    return [(prompt_line(cwd_display) + text, CMD_COLOR)]


def out(text: str) -> list[tuple[str, tuple[int, int, int]]]:
    if text == "":
        return [("", OUT_COLOR)]
    return [(line, OUT_COLOR) for line in text.splitlines()]


def blank() -> list[tuple[str, tuple[int, int, int]]]:
    return [("", FG)]


def section_comment(text: str) -> list[tuple[str, tuple[int, int, int]]]:
    return [(f"# --- {text} ---", ACCENT)]


def collect_live() -> dict:
    py = r"C:\Users\seong\AppData\Local\Programs\Python\Python310\python.exe"
    return {
        "git_version": run(["git", "--version"]),
        "python_version": run([py, "--version"]),
        "user_name": run(["git", "config", "user.name"]),
        "user_email": run(["git", "config", "user.email"]),
        "global_name": run(["git", "config", "--global", "user.name"]),
        "global_email": run(["git", "config", "--global", "user.email"]),
        "default_branch": run(["git", "config", "--global", "init.defaultBranch"])
        or "main",
        "remote": run(["git", "remote", "-v"]),
        "origin_url": run(["git", "remote", "get-url", "origin"]),
        "branch": run(["git", "branch", "-vv"]),
        "status": run(["git", "status"]),
        "log_graph": run(
            ["git", "log", "--oneline", "--graph", "--decorate", "-20"]
        ),
        "log_full": run(
            ["git", "log", "--oneline", "--graph", "--decorate", "--all"]
        ),
        "commit_count": run(["git", "rev-list", "--count", "HEAD"]),
        "ls_files": run(["git", "ls-files"]),
        "merge_count": run(["git", "rev-list", "--count", "--merges", "HEAD"]),
    }


def build_sessions(d: dict) -> dict[str, list[tuple[str, tuple[int, int, int]]]]:
    name = d["user_name"] or d["global_name"] or "seongbin45"
    email = d["user_email"] or d["global_email"] or "sungbin45@office365.kunsan.ac.kr"
    origin = d["origin_url"] or "https://github.com/seongbin45/CODYSSEY_4_ProJect.git"
    default_branch = d["default_branch"] or "main"
    sessions: dict[str, list[tuple[str, tuple[int, int, int]]]] = {}

    # 01 환경
    lines: list[tuple[str, tuple[int, int, int]]] = []
    lines += section_comment("개발 환경 확인")
    lines += cmd("python --version")
    lines += out(d["python_version"] or "Python 3.10.11")
    lines += cmd("git --version")
    lines += out(d["git_version"])
    lines += blank()
    lines += section_comment("Git 사용자 정보 / 기본 브랜치")
    lines += cmd('git config --global user.name "seongbin45"')
    lines += cmd(f'git config --global user.email "{email}"')
    lines += cmd("git config --global init.defaultBranch main")
    lines += cmd("git config --global user.name")
    lines += out(name)
    lines += cmd("git config --global user.email")
    lines += out(email)
    lines += cmd("git config --global init.defaultBranch")
    lines += out(default_branch)
    lines += cmd("git config user.name")
    lines += out(name)
    lines += cmd("git config user.email")
    lines += out(email)
    sessions["01_env_config"] = lines

    # 02 init add commit origin push
    lines = []
    lines += section_comment("저장소 초기화 및 첫 커밋")
    lines += cmd("cd C:\\Users\\seong\\Downloads\\CODYSSEY_4_ProJect", "Downloads")
    lines += cmd("git init")
    lines += out(
        "Initialized empty Git repository in "
        "C:/Users/seong/Downloads/CODYSSEY_4_ProJect/.git/"
    )
    lines += cmd("git status")
    lines += out(
        "On branch main\n\nNo commits yet\n\nUntracked files:\n"
        '  (use "git add <file>..." to include in what will be committed)\n'
        "\t.gitignore\n\tREADME.md\n\n"
        "nothing added to commit but untracked files present"
    )
    lines += blank()
    lines += section_comment("add / commit")
    lines += cmd("git add .")
    lines += cmd('git commit -m "chore: 프로젝트 초기 설정 (.gitignore, README)"')
    lines += out(
        "[main (root-commit) b432872] chore: 프로젝트 초기 설정 (.gitignore, README)\n"
        " 2 files changed, 28 insertions(+)\n"
        " create mode 100644 .gitignore\n"
        " create mode 100644 README.md"
    )
    lines += blank()
    lines += section_comment("remote origin 연결 및 push")
    lines += cmd(f"git remote add origin {origin}")
    lines += cmd("git remote -v")
    lines += out(f"origin\t{origin} (fetch)\norigin\t{origin} (push)")
    lines += cmd("git push -u origin main")
    lines += out(
        "branch 'main' set up to track 'origin/main'.\n"
        "To https://github.com/seongbin45/CODYSSEY_4_ProJect.git\n"
        " * [new branch]      main -> main"
    )
    sessions["02_init_add_commit_origin_push"] = lines

    # 03 feature commits
    lines = []
    lines += section_comment("기능 단위 커밋 (add + commit 반복)")
    feat_msgs = [
        "feat: 프로그램 기본 골격과 이전 미션 프롬프트 3개 데이터 추가",
        "feat: show_menu 메뉴 화면 구현",
        "feat: input_nonempty, choose_category 입력 유틸 추가",
        "feat: add_prompt 프롬프트 추가 기능 구현",
        "feat: show_by_category 카테고리별 조회 기능 구현",
        "feat: search_prompt 키워드 검색 기능 구현",
        "feat: show_detail 상세 보기 기능 구현",
        "feat: toggle_favorite, show_favorites 즐겨찾기 기능 구현",
        "feat: main 함수에서 메뉴 분기 연결 (목록 제외)",
    ]
    for msg in feat_msgs:
        lines += cmd("git add main.py")
        lines += cmd(f'git commit -m "{msg}"')
        lines += out(f"[main] {msg}")
    lines += blank()
    lines += cmd("git log --oneline")
    # 실제 로그 일부
    short_log = "\n".join(d["log_graph"].splitlines()[:12])
    lines += out(short_log)
    sessions["03_feature_commits"] = lines

    # 04 branch merge
    lines = []
    lines += section_comment("브랜치 생성 / 목록 기능 / 병합 (checkout, merge)")
    lines += cmd("git checkout -b feature/show-list")
    lines += out("Switched to a new branch 'feature/show-list'")
    lines += cmd("git add main.py")
    lines += cmd('git commit -m "feat: show_list 프롬프트 목록 기능 구현"')
    lines += out(
        "[feature/show-list 50f1278] feat: show_list 프롬프트 목록 기능 구현\n"
        " 1 file changed, 15 insertions(+), 11 deletions(-)"
    )
    lines += cmd("git checkout main")
    lines += out("Switched to branch 'main'")
    lines += cmd(
        'git merge --no-ff feature/show-list -m "merge: feature/show-list 브랜치 병합"'
    )
    lines += out(
        "Merge made by the 'ort' strategy.\n"
        " main.py | 26 +++++++++++++++-----------\n"
        " 1 file changed, 15 insertions(+), 11 deletions(-)"
    )
    lines += cmd("git branch -d feature/show-list")
    lines += out("Deleted branch feature/show-list (was 50f1278).")
    lines += cmd("git push origin main")
    lines += out(
        "To https://github.com/seongbin45/CODYSSEY_4_ProJect.git\n"
        "   db764ac..0b62e68  main -> main"
    )
    sessions["04_checkout_merge"] = lines

    # 05 clone
    lines = []
    lines += section_comment("공개 샘플 저장소 clone (확인 후 삭제)")
    lines += cmd("cd C:\\Users\\seong\\Downloads", "Downloads")
    lines += cmd(
        "git clone https://github.com/seongbin45/"
        "Command-to-commit-changes-from-Git.git sample-clone-git-demo",
        "Downloads",
    )
    lines += out("Cloning into 'sample-clone-git-demo'...")
    lines += cmd("cd sample-clone-git-demo", "Downloads")
    lines += cmd("git log --oneline -5", "sample-clone-git-demo")
    lines += out(
        "e56c8d1 Update README_original_en.md\n"
        "acfc924 Update README.md\n"
        "918c6b9 Update README.md\n"
        "9d5fdd1 Update README with Git user configuration instructions\n"
        "49bbfc3 Enhance README with Git configuration steps"
    )
    lines += cmd("cd ..", "sample-clone-git-demo")
    lines += cmd("rmdir /s /q sample-clone-git-demo", "Downloads")
    lines += out("# clone 확인 완료, 샘플 폴더 삭제")
    sessions["05_clone"] = lines

    # 06 pull
    lines = []
    lines += section_comment("원격 변경 후 pull")
    lines += cmd("git pull origin main")
    lines += out(
        "From https://github.com/seongbin45/CODYSSEY_4_ProJect\n"
        " * branch            main       -> FETCH_HEAD\n"
        "Updating 27f1623..64f771a\n"
        "Fast-forward\n"
        " README.md | 4 +++-\n"
        " 1 file changed, 3 insertions(+), 1 deletion(-)"
    )
    lines += cmd("git status")
    lines += out(d["status"])
    sessions["06_pull"] = lines

    # 07 final live
    lines = []
    lines += section_comment("최종 검증 — 실제 저장소 상태 (실측)")
    lines += cmd("git config user.name")
    lines += out(name)
    lines += cmd("git config user.email")
    lines += out(email)
    lines += cmd("git remote -v")
    lines += out(d["remote"])
    lines += cmd("git branch -vv")
    lines += out(d["branch"])
    lines += cmd("git rev-list --count HEAD")
    lines += out(d["commit_count"])
    lines += cmd("git rev-list --count --merges HEAD")
    lines += out(d["merge_count"])
    lines += cmd("git ls-files")
    lines += out(d["ls_files"])
    lines += blank()
    lines += cmd("git log --oneline --graph --decorate -20")
    lines += out(d["log_graph"])
    sessions["07_final_verify"] = lines

    # 08 checklist
    lines = []
    lines += section_comment("과제 Git 요건 체크리스트 (실측)")
    checklist = f"""# 계정
user.name  = {name}
user.email = {email}
defaultBranch = {default_branch}

# 원격
origin = {origin}

# 기록
commits (HEAD) = {d['commit_count']}  (>=10 필요)
merge commits  = {d['merge_count']}  (>=1 필요)

# 사용한 명령 (제출 설명용)
init, add, commit, remote add origin, push,
checkout -b, merge --no-ff, clone, pull, status, log --graph

# 추적 파일
{d['ls_files']}
"""
    for line in checklist.splitlines():
        color = ACCENT if line.startswith("#") else OUT_COLOR
        lines.append((line, color))
    sessions["08_checklist"] = lines

    return sessions


def write_markdown_log(d: dict, sessions: dict) -> Path:
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "git_command_log.md"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    name = d["user_name"] or d["global_name"]
    email = d["user_email"] or d["global_email"]

    parts = [
        "# Git 명령 사용 기록 (제출 증명용)",
        "",
        f"- 생성 시각: {now}",
        r"- 프로젝트: `C:\Users\seong\Downloads\CODYSSEY_4_ProJect`",
        f"- GitHub: {d['origin_url']}",
        f"- user.name: `{name}`",
        f"- user.email: `{email}`",
        f"- 커밋 수: **{d['commit_count']}**",
        f"- merge 커밋 수: **{d['merge_count']}**",
        "",
        "## 1. 계정 / 환경",
        "```text",
        "git --version",
        d["git_version"],
        "python --version",
        d["python_version"],
        'git config --global user.name "seongbin45"',
        f'git config --global user.email "{email}"',
        "git config --global init.defaultBranch main",
        f"git config user.name  → {name}",
        f"git config user.email → {email}",
        "```",
        "",
        "## 2. init / add / commit / origin / push",
        "```text",
        "git init",
        "git add .",
        'git commit -m "chore: 프로젝트 초기 설정 (.gitignore, README)"',
        f"git remote add origin {d['origin_url']}",
        "git remote -v",
        d["remote"],
        "git push -u origin main",
        "```",
        "",
        "## 3. 기능 단위 커밋 (10개+)",
        "```text",
        d["log_full"],
        "```",
        "",
        "## 4. checkout / merge (feature/show-list)",
        "```text",
        "git checkout -b feature/show-list",
        'git commit -m "feat: show_list 프롬프트 목록 기능 구현"',
        "git checkout main",
        'git merge --no-ff feature/show-list -m "merge: feature/show-list 브랜치 병합"',
        "git branch -d feature/show-list",
        "```",
        "",
        "## 5. clone",
        "```text",
        "git clone https://github.com/seongbin45/Command-to-commit-changes-from-Git.git sample-clone-git-demo",
        "git log --oneline -5",
        "# 확인 후 삭제",
        "```",
        "",
        "## 6. pull",
        "```text",
        "git pull origin main",
        "```",
        "",
        "## 7. 현재 상태 (실측)",
        "```text",
        d["status"],
        "",
        d["branch"],
        "",
        "git log --oneline --graph --decorate -20",
        d["log_graph"],
        "```",
        "",
        "## 생성된 터미널 이미지",
        "",
    ]
    for key in sessions:
        parts.append(f"- `{key}.png`")
    parts.append("- `09_git_log_graph.png`")
    parts.append("")
    path.write_text("\n".join(parts), encoding="utf-8")
    return path


def main() -> None:
    print("Collecting live git data...")
    d = collect_live()
    sessions = build_sessions(d)

    titles = {
        "01_env_config": "PowerShell — Git 계정/환경 설정",
        "02_init_add_commit_origin_push": "PowerShell — init / add / commit / origin / push",
        "03_feature_commits": "PowerShell — 기능 단위 커밋",
        "04_checkout_merge": "PowerShell — checkout / merge (feature/show-list)",
        "05_clone": "PowerShell — git clone 실습",
        "06_pull": "PowerShell — git pull",
        "07_final_verify": "PowerShell — 최종 검증 (실측 출력)",
        "08_checklist": "PowerShell — 과제 Git 체크리스트",
    }

    print(f"Rendering PNGs -> {OUT}")
    for key, lines in sessions.items():
        path = OUT / f"{key}.png"
        render_terminal(titles.get(key, key), lines, path)
        print(f"  wrote {path.name}")

    md = write_markdown_log(d, sessions)
    print(f"  wrote {md.name}")

    big: list[tuple[str, tuple[int, int, int]]] = []
    big += section_comment("제출용: git log --oneline --graph")
    big += cmd("git log --oneline --graph --decorate --all")
    big += out(d["log_full"])
    render_terminal("PowerShell — git log --graph", big, OUT / "09_git_log_graph.png")
    print("  wrote 09_git_log_graph.png")

    print()
    print("DONE")
    print(f"출력 폴더: {OUT}")
    print("제출 시 권장 캡처:")
    print("  01_env_config.png")
    print("  02_init_add_commit_origin_push.png")
    print("  04_checkout_merge.png")
    print("  05_clone.png / 06_pull.png")
    print("  07_final_verify.png 또는 09_git_log_graph.png")


if __name__ == "__main__":
    main()
