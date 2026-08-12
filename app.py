# -*- coding: utf-8 -*-
"""
나만의 프롬프트 관리 프로그램 — PyQt GUI

VS Code에서 이 파일만 실행하면 됩니다.
  Run  ▶  또는  터미널:  python app.py

PyQt5가 없으면 첫 실행 시 자동 설치를 시도합니다.
데이터/기본 프롬프트는 main.py 와 동일 소스를 사용합니다.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def _ensure_workdir() -> Path:
    """실행 위치를 프로젝트 폴더로 고정 (prompts.json / exports 경로)."""
    root = Path(__file__).resolve().parent
    os.chdir(root)
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    return root


def _ensure_pyqt5() -> None:
    try:
        import PyQt5  # noqa: F401
        return
    except ImportError:
        pass

    print("PyQt5가 없습니다. 설치를 시도합니다... (pip install PyQt5)")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "PyQt5"],
            stdout=sys.stdout,
            stderr=sys.stderr,
        )
    except subprocess.CalledProcessError as e:
        print("PyQt5 설치에 실패했습니다. 터미널에서 직접 실행하세요:")
        print(f"  {sys.executable} -m pip install PyQt5")
        raise SystemExit(1) from e

    try:
        import PyQt5  # noqa: F401
    except ImportError as e:
        print("설치 후에도 PyQt5를 import 할 수 없습니다. VS Code 인터프리터를 확인하세요.")
        raise SystemExit(1) from e


_ROOT = _ensure_workdir()
_ensure_pyqt5()

from PyQt5.QtCore import Qt  # noqa: E402
from PyQt5.QtGui import QFont, QKeySequence  # noqa: E402
from PyQt5.QtWidgets import (  # noqa: E402
    QApplication,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSplitter,
    QStatusBar,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QAbstractItemView,
    QShortcut,
)

# main.py 의 데이터·상수 재사용 (콘솔 버전과 동일 기본 프롬프트)
import main as core  # noqa: E402


APP_STYLE = """
QMainWindow, QWidget {
    background: #0f1419;
    color: #e7ecf3;
    font-size: 13px;
}
QLabel#title {
    font-size: 18px;
    font-weight: 700;
    color: #f5f7fb;
    padding: 4px 0;
}
QLabel#subtitle {
    color: #9aa7b8;
    font-size: 12px;
}
QLineEdit, QTextEdit, QComboBox, QListWidget {
    background: #1a222d;
    border: 1px solid #2b3645;
    border-radius: 8px;
    padding: 8px;
    color: #e7ecf3;
    selection-background-color: #3d7eff;
}
QListWidget::item {
    padding: 8px;
    border-radius: 6px;
}
QListWidget::item:selected {
    background: #243247;
    color: #ffffff;
}
QListWidget::item:hover {
    background: #1f2a3a;
}
QPushButton {
    background: #243247;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 8px 12px;
    color: #e7ecf3;
    font-weight: 600;
}
QPushButton:hover {
    background: #2d3e56;
}
QPushButton:pressed {
    background: #1c2838;
}
QPushButton#primary {
    background: #3d7eff;
    border: 1px solid #3d7eff;
    color: white;
}
QPushButton#primary:hover {
    background: #5b91ff;
}
QPushButton#danger {
    background: #3a1f24;
    border: 1px solid #7f1d1d;
    color: #fecaca;
}
QPushButton#danger:hover {
    background: #4b2429;
}
QStatusBar {
    background: #0b1016;
    color: #9aa7b8;
}
QSplitter::handle {
    background: #1a222d;
}
"""


class PromptEditDialog(QDialog):
    """추가 / 수정 공용 다이얼로그."""

    def __init__(self, parent=None, prompt: dict | None = None, categories: list[str] | None = None):
        super().__init__(parent)
        is_edit = prompt is not None
        self.setWindowTitle("프롬프트 수정" if is_edit else "프롬프트 추가")
        self.resize(560, 480)
        self._categories = categories or list(core.CATEGORIES)

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("예: 블로그 초안 작성 도우미")
        form.addRow("제목 *", self.title_edit)

        self.category_combo = QComboBox()
        self.category_combo.setEditable(True)
        self.category_combo.addItems(self._categories)
        self.category_combo.setToolTip("목록에서 고르거나, 직접 새 카테고리 이름을 입력할 수 있습니다.")
        form.addRow("카테고리 *", self.category_combo)

        self.content_edit = QTextEdit()
        self.content_edit.setPlaceholderText("프롬프트 본문 전체를 입력하세요.")
        form.addRow("내용 *", self.content_edit)

        layout.addLayout(form)

        buttons = QDialogButtonBox()
        save_btn = buttons.addButton(
            "수정 저장" if is_edit else "추가하기", QDialogButtonBox.AcceptRole
        )
        cancel_btn = buttons.addButton("취소", QDialogButtonBox.RejectRole)
        save_btn.setObjectName("primary")
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        if prompt:
            self.title_edit.setText(prompt.get("title", ""))
            cat = prompt.get("category", "기타")
            idx = self.category_combo.findText(cat)
            if idx >= 0:
                self.category_combo.setCurrentIndex(idx)
            else:
                self.category_combo.setEditText(cat)
            self.content_edit.setPlainText(prompt.get("content", ""))

    def get_data(self) -> dict | None:
        title = self.title_edit.text().strip()
        content = self.content_edit.toPlainText().strip()
        category = self.category_combo.currentText().strip() or "기타"
        if not title or not content:
            QMessageBox.warning(
                self,
                "입력 확인",
                "제목과 내용은 비워 둘 수 없습니다.\n필수 항목(*)을 모두 입력해 주세요.",
            )
            return None
        return {"title": title, "content": content, "category": category}


class PromptManagerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("나만의 프롬프트 관리 프로그램")
        self.resize(1180, 740)
        self.setMinimumSize(960, 600)

        # 필터 상태: all | favorites | category | search | top
        self._mode = "all"
        self._filter_category: str | None = None
        self._search_keyword = ""
        self._view_indices: list[int] = []  # 리스트에 보이는 항목 → prompts 인덱스

        self._build_ui()
        self._bind_shortcuts()
        self.refresh_list()
        self.statusBar().showMessage(
            f"준비 완료 · 기본 등록 프롬프트 {len(core.prompts)}개 · "
            "왼쪽 목록을 클릭하면 상세 내용을 볼 수 있습니다."
        )

    # ── UI ───────────────────────────────────────────
    def _build_ui(self) -> None:
        root = QWidget()
        self.setCentralWidget(root)
        outer = QVBoxLayout(root)
        outer.setContentsMargins(16, 16, 16, 12)
        outer.setSpacing(10)

        header = QVBoxLayout()
        title = QLabel("나만의 프롬프트 관리")
        title.setObjectName("title")
        subtitle = QLabel(
            "평가자용 화면 · VS Code에서 app.py 만 실행하면 됩니다  ·  "
            "아래 버튼 이름 = 실제 기능 이름"
        )
        subtitle.setObjectName("subtitle")
        header.addWidget(title)
        header.addWidget(subtitle)
        outer.addLayout(header)

        # 검색 / 조회 줄 (콘솔 메뉴 2·3·4·7·9 대응)
        filter_row = QHBoxLayout()
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText(
            "검색어 입력 후 [프롬프트 검색] 클릭 또는 Enter"
        )
        self.search_edit.setToolTip("제목 또는 내용에 포함된 단어로 찾습니다. (메뉴 4)")
        self.search_edit.returnPressed.connect(self.on_search)
        filter_row.addWidget(self.search_edit, 3)

        self.category_filter = QComboBox()
        self.category_filter.addItem("카테고리별 조회: 전체", None)
        for c in core.CATEGORIES:
            self.category_filter.addItem(f"카테고리별 조회: {c}", c)
        self.category_filter.setToolTip(
            "카테고리를 고르면 해당 분류 프롬프트만 목록에 표시합니다. (메뉴 3)"
        )
        self.category_filter.currentIndexChanged.connect(self.on_category_filter)
        filter_row.addWidget(self.category_filter, 2)

        btn_search = QPushButton("프롬프트 검색")
        btn_search.setObjectName("primary")
        btn_search.setToolTip("입력한 검색어로 제목·내용을 검색합니다. (메뉴 4)")
        btn_search.clicked.connect(self.on_search)
        filter_row.addWidget(btn_search)

        btn_all = QPushButton("프롬프트 목록 (전체)")
        btn_all.setToolTip("등록된 모든 프롬프트를 다시 보여 줍니다. (메뉴 2)")
        btn_all.clicked.connect(self.show_all)
        filter_row.addWidget(btn_all)

        btn_fav = QPushButton("즐겨찾기 목록")
        btn_fav.setToolTip("즐겨찾기로 표시한 프롬프트만 모아서 봅니다. (메뉴 7)")
        btn_fav.clicked.connect(self.show_favorites)
        filter_row.addWidget(btn_fav)

        btn_top = QPushButton("조회수 Top 목록")
        btn_top.setToolTip("상세 보기를 많이 한 순서(조회수 높은 순)로 정렬합니다. (메뉴 9)")
        btn_top.clicked.connect(self.show_top)
        filter_row.addWidget(btn_top)

        outer.addLayout(filter_row)

        splitter = QSplitter(Qt.Horizontal)

        # 왼쪽: 목록
        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 0, 0)
        list_caption = QLabel("프롬프트 목록 — 항목을 클릭하면 오른쪽에서 상세 보기")
        list_caption.setObjectName("subtitle")
        left_layout.addWidget(list_caption)
        self.list_widget = QListWidget()
        self.list_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.list_widget.setToolTip("한 줄을 클릭하면 상세 보기(메뉴 5)가 열리고 조회수가 1 증가합니다.")
        self.list_widget.currentRowChanged.connect(self.on_select)
        left_layout.addWidget(self.list_widget)
        self.count_label = QLabel("0개")
        self.count_label.setObjectName("subtitle")
        left_layout.addWidget(self.count_label)
        splitter.addWidget(left)

        # 오른쪽: 상세
        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(0, 0, 0, 0)

        detail_caption = QLabel("프롬프트 상세 보기")
        detail_caption.setObjectName("subtitle")
        right_layout.addWidget(detail_caption)

        self.detail_meta = QLabel("왼쪽 목록에서 프롬프트를 선택하세요.")
        self.detail_meta.setObjectName("subtitle")
        self.detail_meta.setWordWrap(True)
        right_layout.addWidget(self.detail_meta)

        self.detail_content = QTextEdit()
        self.detail_content.setReadOnly(True)
        self.detail_content.setPlaceholderText(
            "선택한 프롬프트의 전체 내용이 여기에 표시됩니다. (메뉴 5: 상세 보기)"
        )
        right_layout.addWidget(self.detail_content, 1)

        # 관리 버튼 1행 — 메뉴 1, 6, 8
        manage_row = QHBoxLayout()
        manage_hint = QLabel("선택 항목 관리:")
        manage_hint.setObjectName("subtitle")
        manage_row.addWidget(manage_hint)

        self.btn_add = QPushButton("프롬프트 추가")
        self.btn_add.setObjectName("primary")
        self.btn_add.setToolTip("새 프롬프트를 등록합니다. (메뉴 1)")
        self.btn_add.clicked.connect(self.on_add)
        manage_row.addWidget(self.btn_add)

        self.btn_edit = QPushButton("프롬프트 수정")
        self.btn_edit.setToolTip("선택한 프롬프트의 제목·내용·카테고리를 고칩니다. (메뉴 8)")
        self.btn_edit.clicked.connect(self.on_edit)
        manage_row.addWidget(self.btn_edit)

        self.btn_del = QPushButton("프롬프트 삭제")
        self.btn_del.setObjectName("danger")
        self.btn_del.setToolTip("선택한 프롬프트를 목록에서 제거합니다. (메뉴 8)")
        self.btn_del.clicked.connect(self.on_delete)
        manage_row.addWidget(self.btn_del)

        self.btn_star = QPushButton("즐겨찾기 추가/해제")
        self.btn_star.setToolTip(
            "선택한 프롬프트를 즐겨찾기에 넣거나 빼니다. (메뉴 6: 즐겨찾기 관리)"
        )
        self.btn_star.clicked.connect(self.on_toggle_favorite)
        manage_row.addWidget(self.btn_star)
        manage_row.addStretch(1)
        right_layout.addLayout(manage_row)

        # 파일 버튼 2행 — 메뉴 10, 11, 12
        file_row = QHBoxLayout()
        file_hint = QLabel("파일 저장·불러오기:")
        file_hint.setObjectName("subtitle")
        file_row.addWidget(file_hint)

        self.btn_save = QPushButton("JSON으로 저장")
        self.btn_save.setToolTip(
            f"현재 프롬프트 전체를 '{core.DATA_FILE}' 파일로 저장합니다. (메뉴 10)"
        )
        self.btn_save.clicked.connect(self.on_save_json)
        file_row.addWidget(self.btn_save)

        self.btn_load = QPushButton("JSON에서 불러오기")
        self.btn_load.setToolTip(
            f"'{core.DATA_FILE}' 파일을 읽어 목록을 복원합니다. (메뉴 11)"
        )
        self.btn_load.clicked.connect(self.on_load_json)
        file_row.addWidget(self.btn_load)

        self.btn_export = QPushButton("Markdown 파일로 내보내기")
        self.btn_export.setToolTip(
            f"카테고리별 .md 파일을 '{core.EXPORT_DIR}/' 폴더에 만듭니다. (메뉴 12)"
        )
        self.btn_export.clicked.connect(self.on_export_md)
        file_row.addWidget(self.btn_export)
        file_row.addStretch(1)
        right_layout.addLayout(file_row)

        splitter.addWidget(right)

        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 3)
        outer.addWidget(splitter, 1)

        self.setStatusBar(QStatusBar())

    def _bind_shortcuts(self) -> None:
        QShortcut(QKeySequence("Ctrl+N"), self, self.on_add)
        QShortcut(QKeySequence("Ctrl+S"), self, self.on_save_json)
        QShortcut(QKeySequence("Ctrl+F"), self, lambda: self.search_edit.setFocus())
        QShortcut(QKeySequence("F5"), self, self.refresh_list)

    # ── 목록 ─────────────────────────────────────────
    def _filtered_indices(self) -> list[int]:
        items = list(enumerate(core.prompts))

        if self._mode == "favorites":
            items = [(i, p) for i, p in items if p.get("favorite")]
        elif self._mode == "category" and self._filter_category:
            items = [(i, p) for i, p in items if p.get("category") == self._filter_category]
        elif self._mode == "search" and self._search_keyword:
            kw = self._search_keyword.lower()
            items = [
                (i, p)
                for i, p in items
                if kw in p.get("title", "").lower() or kw in p.get("content", "").lower()
            ]
        elif self._mode == "top":
            items = sorted(items, key=lambda x: x[1].get("views", 0), reverse=True)

        return [i for i, _ in items]

    def refresh_list(self, keep_prompt_index: int | None = None) -> None:
        prev = keep_prompt_index
        if prev is None:
            prev = self.current_prompt_index()

        self.list_widget.blockSignals(True)
        self.list_widget.clear()
        self._view_indices = self._filtered_indices()

        for i in self._view_indices:
            p = core.prompts[i]
            star = "★" if p.get("favorite") else "☆"
            views = p.get("views", 0)
            text = f"{star}  [{p.get('category', '')}]  {p.get('title', '')}   ·  조회 {views}"
            item = QListWidgetItem(text)
            item.setData(Qt.UserRole, i)
            self.list_widget.addItem(item)

        self.list_widget.blockSignals(False)

        mode_label = {
            "all": "전체",
            "favorites": "즐겨찾기",
            "category": f"카테고리:{self._filter_category}",
            "search": f"검색:{self._search_keyword}",
            "top": "조회수 Top",
        }.get(self._mode, self._mode)
        self.count_label.setText(f"{len(self._view_indices)}개 표시  ·  전체 {len(core.prompts)}개  ·  {mode_label}")

        # 선택 복원 (조회수 증가 없이 상세만 표시 — 시그널 차단)
        self.list_widget.blockSignals(True)
        if prev is not None and prev in self._view_indices:
            row = self._view_indices.index(prev)
            self.list_widget.setCurrentRow(row)
            self.list_widget.blockSignals(False)
            self._show_detail(prev, count_view=False)
        elif self._view_indices:
            self.list_widget.setCurrentRow(0)
            self.list_widget.blockSignals(False)
            self._show_detail(self._view_indices[0], count_view=False)
        else:
            self.list_widget.blockSignals(False)
            self.detail_meta.setText("표시할 프롬프트가 없습니다.")
            self.detail_content.clear()

    def current_prompt_index(self) -> int | None:
        row = self.list_widget.currentRow()
        if row < 0 or row >= len(self._view_indices):
            return None
        return self._view_indices[row]

    def on_select(self, row: int) -> None:
        if row < 0 or row >= len(self._view_indices):
            return
        # 사용자가 목록에서 고른 경우만 조회수 +1 (콘솔 show_detail 과 동일)
        self._show_detail(self._view_indices[row], count_view=True)

    def _show_detail(self, idx: int, count_view: bool = True) -> None:
        if idx < 0 or idx >= len(core.prompts):
            return
        p = core.prompts[idx]
        if count_view:
            p["views"] = int(p.get("views", 0)) + 1

        star = "★" if p.get("favorite") else "☆"
        self.detail_meta.setText(
            f"{star}  {p.get('title', '')}\n"
            f"카테고리: {p.get('category', '')}   ·   조회수: {p.get('views', 0)}   ·   인덱스: {idx + 1}"
        )
        self.detail_content.setPlainText(p.get("content", ""))

        if idx in self._view_indices:
            row = self._view_indices.index(idx)
            item = self.list_widget.item(row)
            if item:
                item.setText(
                    f"{star}  [{p.get('category', '')}]  {p.get('title', '')}   ·  조회 {p.get('views', 0)}"
                )

    # ── 필터 ─────────────────────────────────────────
    def show_all(self) -> None:
        self._mode = "all"
        self._filter_category = None
        self._search_keyword = ""
        self.search_edit.clear()
        self.category_filter.blockSignals(True)
        self.category_filter.setCurrentIndex(0)
        self.category_filter.blockSignals(False)
        self.refresh_list()
        self.statusBar().showMessage("전체 목록")

    def show_favorites(self) -> None:
        self._mode = "favorites"
        self.refresh_list()
        self.statusBar().showMessage("즐겨찾기 목록")

    def show_top(self) -> None:
        self._mode = "top"
        self.refresh_list()
        self.statusBar().showMessage("조회수 Top 목록")

    def on_category_filter(self) -> None:
        cat = self.category_filter.currentData()
        if cat is None:
            self._mode = "all"
            self._filter_category = None
        else:
            self._mode = "category"
            self._filter_category = cat
        self.refresh_list()

    def on_search(self) -> None:
        kw = self.search_edit.text().strip()
        if not kw:
            self.show_all()
            return
        self._mode = "search"
        self._search_keyword = kw
        self.refresh_list()
        self.statusBar().showMessage(f"검색: {kw} → {len(self._view_indices)}건")

    # ── CRUD ─────────────────────────────────────────
    def on_add(self) -> None:
        dlg = PromptEditDialog(self)
        if dlg.exec_() != QDialog.Accepted:
            return
        data = dlg.get_data()
        if not data:
            return
        core.prompts.append(
            {
                "title": data["title"],
                "content": data["content"],
                "category": data["category"],
                "favorite": False,
                "views": 0,
            }
        )
        self._mode = "all"
        self.refresh_list(keep_prompt_index=len(core.prompts) - 1)
        self.statusBar().showMessage(f"추가됨: {data['title']}")

    def on_edit(self) -> None:
        idx = self.current_prompt_index()
        if idx is None:
            QMessageBox.information(self, "알림", "수정할 항목을 선택하세요.")
            return
        p = core.prompts[idx]
        dlg = PromptEditDialog(self, prompt=p)
        if dlg.exec_() != QDialog.Accepted:
            return
        data = dlg.get_data()
        if not data:
            return
        p["title"] = data["title"]
        p["content"] = data["content"]
        p["category"] = data["category"]
        self.refresh_list(keep_prompt_index=idx)
        self.statusBar().showMessage(f"수정됨: {p['title']}")

    def on_delete(self) -> None:
        idx = self.current_prompt_index()
        if idx is None:
            QMessageBox.information(self, "알림", "삭제할 항목을 선택하세요.")
            return
        p = core.prompts[idx]
        reply = QMessageBox.question(
            self,
            "삭제 확인",
            f"'{p.get('title', '')}' 프롬프트를 삭제할까요?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if reply != QMessageBox.Yes:
            return
        removed = core.prompts.pop(idx)
        self.refresh_list()
        self.statusBar().showMessage(f"삭제됨: {removed.get('title', '')}")

    def on_toggle_favorite(self) -> None:
        idx = self.current_prompt_index()
        if idx is None:
            QMessageBox.information(self, "알림", "항목을 선택하세요.")
            return
        p = core.prompts[idx]
        p["favorite"] = not bool(p.get("favorite"))
        state = "추가" if p["favorite"] else "해제"
        self.refresh_list(keep_prompt_index=idx)
        self.statusBar().showMessage(f"즐겨찾기 {state}: {p.get('title', '')}")

    # ── 영속화 ───────────────────────────────────────
    def on_save_json(self) -> None:
        path = _ROOT / core.DATA_FILE
        with open(path, "w", encoding="utf-8") as f:
            json.dump(core.prompts, f, ensure_ascii=False, indent=2)
        self.statusBar().showMessage(f"저장 완료: {path.name} ({len(core.prompts)}개)")
        QMessageBox.information(self, "JSON 저장", f"'{path.name}' 에 저장했습니다.")

    def on_load_json(self) -> None:
        path = _ROOT / core.DATA_FILE
        if not path.exists():
            QMessageBox.warning(self, "JSON 불러오기", f"'{path.name}' 파일이 없습니다.")
            return
        with open(path, "r", encoding="utf-8") as f:
            loaded = json.load(f)
        if not isinstance(loaded, list):
            QMessageBox.warning(self, "JSON 불러오기", "파일 형식이 올바르지 않습니다.")
            return
        core.prompts.clear()
        core.prompts.extend(loaded)
        self.show_all()
        self.statusBar().showMessage(f"불러오기 완료: {len(core.prompts)}개")
        QMessageBox.information(
            self, "JSON 불러오기", f"'{path.name}' 에서 {len(core.prompts)}개를 불러왔습니다."
        )

    def on_export_md(self) -> None:
        if not core.prompts:
            QMessageBox.information(self, "Markdown 내보내기", "내보낼 프롬프트가 없습니다.")
            return
        export_dir = _ROOT / core.EXPORT_DIR
        export_dir.mkdir(exist_ok=True)
        by_cat: dict[str, list] = {}
        for p in core.prompts:
            by_cat.setdefault(p.get("category", "기타"), []).append(p)
        for category, items in by_cat.items():
            filename = export_dir / f"{category}.md"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"# {category}\n\n")
                for p in items:
                    star = "★" if p.get("favorite") else "☆"
                    f.write(f"## {p.get('title', '')} {star}\n\n{p.get('content', '')}\n\n")
        self.statusBar().showMessage(f"Markdown 내보내기 완료: {export_dir}/")
        QMessageBox.information(
            self,
            "Markdown 내보내기",
            f"'{core.EXPORT_DIR}/' 폴더에 카테고리별 .md 파일을 만들었습니다.",
        )


def main() -> None:
    # 고해상도 디스플레이
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(APP_STYLE)
    font = QFont("Malgun Gothic", 10)
    app.setFont(font)

    win = PromptManagerWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
