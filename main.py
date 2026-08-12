"""
나만의 프롬프트 관리 프로그램
Python & Git 기초 미션 - Codyssey

기능: 프롬프트 추가, 목록 보기, 카테고리별 조회, 검색, 상세 보기, 즐겨찾기 관리
데이터는 리스트+딕셔너리로 저장하며, 프로그램 종료 시 초기화된다.
(메뉴 10~12: JSON 저장/불러오기, Markdown 내보내기 / 메뉴 8~9: 수정삭제·조회수 Top - 보너스)
"""

CATEGORIES = ["텍스트 생성", "이미지 생성", "영상 생성", "페르소나", "자동화", "기타"]
DATA_FILE = "prompts.json"
EXPORT_DIR = "exports"

# 이전 미션 원문 프롬프트 (other/ 폴더 기준)
# 1) CODYSSEY_1_ProJect/bot/prompts/system_prompt.md
# 2) CODYSSEY_2_ProJect/Docs/video_prompts_model_variants.md (씬1 → Veo 3.1)
# 3) Codyssey_3_ProJect/project1/n8n OpenAI system content
prompts = [
    {
        "title": "확인봇 - 창업지원 실무 이메일 코치 (1주차)",
        "content": "# 확인봇 — 시스템 프롬프트 (v2 최종)\n\n당신은 **확인봇**, 창업지원 실무 이메일 작성을 돕는 코치입니다.\n행정 절차 경험이 있는 선배 역할로, 예비창업팀 팀장이 담당 매니저에게 보낼 실무 이메일을 함께 만듭니다.\n\n---\n\n## 목표\n\n사용자가 제공한 **배경 상황**과 **불확실한 사항**을 바탕으로,\n담당자에게 보낼 **실무 이메일 초안**을 작성합니다.\n\n---\n\n## 페르소나\n\n| 항목 | 내용 |\n|------|------|\n| 이름 | 확인봇 |\n| 역할 | 창업지원 실무 이메일 작성 코치 |\n| 전문 분야 | 정부지원사업 집행 절차, 실무 이메일 어조 조정 |\n| 말투 | 정중한 존댓말, 군더더기 없음 |\n| 우선순위 | **정확성 > 신속함** (모호하면 반드시 확인 필요로 표기하거나 되묻는다) |\n\n---\n\n## 출력 형식\n\n- **제목 1줄** + **본문** (설명·머리말 없이 이메일만 출력)\n- 본문 구조(줄바꿈 필수):\n  1) 인사 + 배경 **2~3문장** 압축\n  2) 확인 필요 사항을 **반드시 `1)` `2)` `3)` 번호 목록**으로 제시 (글머리 없는 줄 나열 금지)\n  3) 맺음 한 줄(`확인 부탁드립니다.` 등)\n  4) **빈 줄 다음** 서명 (`○○ 드림`) — 서명·감사 문구를 질문 문장 끝에 붙이지 말 것\n- 분량: 본문 **250~350자**(한국어 기준, 제목·서명 제외 권장)\n- 기본 서명: 사용자가 지정한 이름으로 `\"○○ 드림\"` 형태. 미지정이면 `\"팀장 드림\"`\n- 최종 답변에는 내부 검토 과정을 노출하지 않는다. 이메일(또는 요청 채널 형식)만 출력한다.\n\n### 출력 스키마 (반드시 이 골격)\n\n```\n제목: …\n\n안녕하세요, ○○님. (배경 2~3문장)\n\n1) …\n2) …\n3) …   ← 없으면 2개까지. 마지막 항목에 \"감사합니다\"를 넣지 말 것\n\n확인 부탁드립니다.\n\n○○ 드림\n```\n\n---\n\n## 내부 작업 순서 (v2 — 단계적 접근, 출력에는 비노출)\n\n1. 배경 정보 중 **확정된 사실**과 **불확실한 사항**을 구분한다.\n2. 배경 정보 내 **상충되는 수치·날짜·정책**이 있는지 점검한다.\n3. 확인 필요 사항을 **실행 가능한 질문**(다음 행동까지 포함)으로 재구성한다.\n4. 최종 출력은 요청된 형식(메일/카톡 등)만 작성한다.\n\n---\n\n## 안전장치 (환각 방지)\n\n1. 사용자가 제공한 배경 정보에 **없는** 금액·날짜·정책·기준을 임의로 추정하여 이메일에 사실처럼 쓰지 않는다.\n2. 배경 정보만으로 확실하지 않은 사항이 있으면, 이메일에 넣기 전에 사용자에게 먼저  \n   `\"이 부분이 배경 정보에 없어 확인이 필요합니다\"` 라고 되묻는다.\n3. 사용자가 준 배경 정보 자체에 **상충**하는 내용이 있으면, 그 불일치를 이메일 질문에 반영하거나 사용자에게 먼저 알린다.\n4. **확인사항은 최대 3개**. 4개 이상이면 사용자에게 알리고, 우선순위 상위 3개만 본 메일에 넣고 나머지는 별도 메일 분리를 제안한다.\n\n---\n\n## 사실 / 정책 / 수치 처리 규칙\n\n- 배경 정보에 **명시된** 사실·수치는 그대로 인용한다.\n- 배경 정보에 **없는** 사실·수치는 절대 만들지 않고 `\"확인 필요\"` 항목으로 이메일에 포함한다.\n- 순서·정책 관련 질문은 **예/아니오로 끝나지 않도록**,  \n  `\"만약 그렇다면 지금 무엇부터 해야 하는지\"`까지 묻는다.\n- 이미 배경 상황에 답이 나온 내용을 **다시 묻지 않는다**. 모르는 것만 구체적으로 묻는다.\n\n---\n\n## 문맥 유지 규칙\n\n- 매 턴마다 **지금까지 확정된 확인사항 목록**을 유지한다.\n- 톤·채널·분량 등 **표현 조건만 변경**되면, 확인사항 목록은 건드리지 않고 표현 방식만 바꾼다.\n- 사용자가 확인사항을 **추가**하면 기존 항목을 유지한 채 새 항목을 붙인다.\n\n---\n\n## 모호 입력 처리\n\n배경·모르는 것이 거의 없는 요청(예: `\"그냥 절차 물어보는 메일 써줘\"`)이면  \n이메일을 바로 쓰지 말고 아래를 되묻는다.\n\n- 어떤 절차/항목에 대한 확인인지\n- 이미 아는 정보(승인 여부, 금액, 업체명, 관련 문서 상태 등)\n\n---\n\n## 입력 템플릿 (사용자 안내용)\n\n```\n[업무 과업] 정책/절차 확인 이메일 작성\n[배경 상황] (승인 이력, 진행 중인 계약/서류 상태, 관련 문서상 명시 사항)\n[확실히 모르는 것] (순서, 기준, 계산 등 불확실한 항목을 항목별로 나열)\n[타겟] 담당자(정중·사무적 실무 관계)\n[톤] 정중하고 간결한 실무 메일체\n[분량] 본문 250~350자\n[금지] 이미 배경에 명시된 내용 재질문 금지, 닫힌 질문(예/아니오)으로 끝나는 순서 질문 금지\n[서명] (예: 김철수 드림)\n```",
        "category": "페르소나",
        "favorite": True,
        "views": 0,
    },
    {
        "title": "FinFit 광고 씬1 - 문제 제시 (Veo, 2주차)",
        "content": "The same young man from the reference image stands medium-wide full body.\nHe looks down at a generic dark smartphone with mild uncertainty.\nShoulders slightly hunched. Other hand in hoodie pocket.\n\nAround him, translucent holographic UI panels and notification cards in electric purple and blue drift and orbit chaotically with soft motion streaks.\nNo readable real logos. No brand names on phone.\n\nCamera: slow subtle orbit around the character, keep medium-wide, never go to face close-up.\nDuration: 4 seconds. Aspect 16:9.\n\nAudio: soft ambient digital chime clutter, low tension undertone, distant UI blips, NO dialogue, NO voiceover, NO speech.\nStyle: soft cel-shaded cinematic stylized 3D, dark navy background, neon glow, volumetric light, ultra-detailed.",
        "category": "영상 생성",
        "favorite": False,
        "views": 0,
    },
    {
        "title": "지출 메모 자동 분류 (Make/n8n, 3주차)",
        "content": "당신은 지출 내역 분석 비서입니다. 사용자의 메모를 분석하여 반드시 아래 JSON 구조로만 응답하세요. 마크다운 기호(```)를 절대 포함하지 말고 순수 JSON 문자열만 출력하세요.\n\n{\n  \"category\": \"식비, 교통비, 문화생활, 생필품, 기타, 분류불가 중 택1\",\n  \"amount\": \"지출 금액을 0 이상의 정수로만 기재\",\n  \"summary\": \"지출 내역을 10자 이내로 요약\",\n  \"Classification\": \"분류 가능 여/부 표시\"\n}\n\n분류 규칙:\n1. 메모에서 금액을 명확히 추출할 수 있고 그 값이 0보다 크면, amount에 해당 숫자를 그대로 기재하고 category는 내용에 맞게 분류하세요.\n2. 실제로 비용이 들지 않은 정당한 지출(예: \"무료 쿠폰으로 커피 받음\", \"친구가 밥 사줌\")은 amount를 0으로 기재하되, category는 \"분류불가\"가 아니라 내용에 맞는 정상 카테고리로 분류하세요.\n3. 아래에 해당하는 경우에만 Classification를 \"분류불가\"로, amount는 0으로 기재하세요.\n   - 금액이 음수로 표현된 경우 (예: \"-1000\", \"마이너스 5000원\")\n   - 금액을 특정할 수 없거나 메모에 금액 자체가 없는 경우\n   - 지출 내용과 금액의 연결이 불명확해 파싱을 신뢰할 수 없는 경우",
        "category": "자동화",
        "favorite": False,
        "views": 0,
    },
]


def show_menu():
    print("\n=== 나만의 프롬프트 관리 ===")
    print("1. 프롬프트 추가")
    print("2. 프롬프트 목록")
    print("3. 카테고리별 조회")
    print("4. 프롬프트 검색")
    print("5. 프롬프트 상세 보기")
    print("6. 즐겨찾기 관리")
    print("7. 즐겨찾기 목록")
    print("0. 종료")


def input_nonempty(label):
    while True:
        value = input(label).strip()
        if value:
            return value
        print("값을 비워둘 수 없습니다. 다시 입력해주세요.")


def choose_category():
    print("카테고리 선택:")
    for i, c in enumerate(CATEGORIES, 1):
        print(f"{i}) {c}")
    print(f"{len(CATEGORIES) + 1}) 직접 입력")
    choice = input("선택: ").strip()

    if choice.isdigit():
        idx = int(choice)
        if 1 <= idx <= len(CATEGORIES):
            return CATEGORIES[idx - 1]
        if idx == len(CATEGORIES) + 1:
            return input_nonempty("카테고리 직접 입력: ")

    print("잘못된 선택입니다. '기타'로 등록됩니다.")
    return "기타"


def add_prompt():
    print("\n=== 프롬프트 추가 ===")
    title = input_nonempty("제목: ")
    content = input_nonempty("내용: ")
    category = choose_category()

    prompts.append({
        "title": title,
        "content": content,
        "category": category,
        "favorite": False,
        "views": 0,
    })
    print("프롬프트가 추가되었습니다!")


def show_by_category():
    print("\n=== 카테고리별 조회 ===")
    category = choose_category()

    filtered = [p for p in prompts if p["category"] == category]
    print(f"\n[{category}] 카테고리 프롬프트:")
    if not filtered:
        print("해당 카테고리에 프롬프트가 없습니다.")
        return

    for i, p in enumerate(filtered, 1):
        print(f"{i}. {p['title']}")
    print(f"총 {len(filtered)}개의 프롬프트")


def search_prompt():
    print("\n=== 프롬프트 검색 ===")
    keyword = input_nonempty("검색어: ")

    results = [
        p for p in prompts
        if keyword.lower() in p["title"].lower() or keyword.lower() in p["content"].lower()
    ]

    print("검색 결과:")
    if not results:
        print("검색 결과가 없습니다.")
        return

    for i, p in enumerate(results, 1):
        print(f"{i}. [{p['category']}] {p['title']}")
    print(f"{len(results)}개의 프롬프트를 찾았습니다.")


def show_detail():
    print("\n=== 프롬프트 상세 보기 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return

    for i, p in enumerate(prompts, 1):
        star = "★" if p["favorite"] else "☆"
        print(f"{i}. [{p['category']}] {p['title']} {star}")

    idx = input("번호 입력: ").strip()
    if not idx.isdigit() or not (1 <= int(idx) <= len(prompts)):
        print("잘못된 번호입니다.")
        return

    p = prompts[int(idx) - 1]
    p["views"] += 1

    star = "★" if p["favorite"] else "☆"
    print("─" * 30)
    print(f"제목: {p['title']}")
    print(f"카테고리: {p['category']}")
    print(f"즐겨찾기: {star}")
    print("─" * 30)
    print("내용:")
    print(p["content"])
    print("─" * 30)


def toggle_favorite():
    print("\n=== 즐겨찾기 관리 ===")
    if not prompts:
        print("등록된 프롬프트가 없습니다.")
        return

    for i, p in enumerate(prompts, 1):
        star = "★" if p["favorite"] else "☆"
        print(f"{i}. [{p['category']}] {p['title']} {star}")

    idx = input("프롬프트 번호 입력: ").strip()
    if not idx.isdigit() or not (1 <= int(idx) <= len(prompts)):
        print("잘못된 번호입니다.")
        return

    p = prompts[int(idx) - 1]
    p["favorite"] = not p["favorite"]
    state = "추가" if p["favorite"] else "해제"
    print(f"'{p['title']}' 프롬프트를 즐겨찾기에서 {state}했습니다!")


def show_favorites():
    print("\n=== 즐겨찾기 목록 ===")
    favorites = [p for p in prompts if p["favorite"]]
    if not favorites:
        print("즐겨찾기한 프롬프트가 없습니다.")
        return

    for i, p in enumerate(favorites, 1):
        print(f"{i}. [{p['category']}] {p['title']}")
    print(f"총 {len(favorites)}개의 즐겨찾기")


if __name__ == "__main__":
    show_menu()
