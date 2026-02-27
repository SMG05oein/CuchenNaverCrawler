import time
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLineEdit, QPushButton, QComboBox, QSpinBox, QLabel,
    QCheckBox, QDateEdit, QGroupBox, QTextEdit
)
from PyQt6.QtCore import QDate


class NaverCrawlerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 메인 레이아웃 및 스타일
        main_layout = QVBoxLayout()
        self.setStyleSheet("background-color: #2b2b2b; color: #ffffff;")

        # --- 1. 위젯 생성 (AttributeError 방지 위해 선언 먼저) ---
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("ID")
        self.id_input.setStyleSheet("background-color: #3b3b3b; color: white;")

        self.pw_input = QLineEdit()
        self.pw_input.setPlaceholderText("PW")
        self.pw_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pw_input.setStyleSheet("background-color: #3b3b3b; color: white;")

        self.btn_login = QPushButton("로그인")
        self.btn_login.setStyleSheet("background-color: #28a745; font-weight: bold; padding: 5px;")

        self.cafe_list = QComboBox()
        self.cafe_list.addItem("로그인 후 목록을 불러오세요")
        self.cafe_list.setStyleSheet("background-color: #3b3b3b; color: white;")

        self.btn_fetch_cafes = QPushButton("목록 갱신")
        self.btn_fetch_cafes.setStyleSheet("background-color: #6c757d;")

        self.btn_select_cafe = QPushButton("카페 선택")
        self.btn_select_cafe.setStyleSheet("background-color: #007bff; font-weight: bold;")

        self.board_type = QComboBox()
        self.board_type.addItem("all 전체 게시글")

        self.collect_count = QSpinBox()
        self.collect_count.setRange(1, 10000)
        self.collect_count.setValue(1000)

        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText("검색 키워드 입력")

        # --- 2. 레이아웃 배치 ---
        # 로그인 섹션
        login_group = QHBoxLayout()
        login_group.addWidget(QLabel("ID"))
        login_group.addWidget(self.id_input)
        login_group.addWidget(QLabel("PW"))
        login_group.addWidget(self.pw_input)
        login_group.addWidget(self.btn_login)
        main_layout.addLayout(login_group)

        # 카페 설정 섹션
        settings_layout = QGridLayout()
        settings_layout.addWidget(QLabel("카페 목록"), 0, 0)
        settings_layout.addWidget(self.cafe_list, 0, 1)
        settings_layout.addWidget(self.btn_fetch_cafes, 0, 2)
        settings_layout.addWidget(self.btn_select_cafe, 0, 3)
        settings_layout.addWidget(QLabel("게시판 종류"), 1, 0)
        settings_layout.addWidget(self.board_type, 1, 1)
        settings_layout.addWidget(QLabel("수집 게시글"), 1, 2)
        settings_layout.addWidget(self.collect_count, 1, 3)
        settings_layout.addWidget(QLabel("검색 키워드"), 2, 0)
        settings_layout.addWidget(self.keyword_input, 2, 1, 1, 3)
        main_layout.addLayout(settings_layout)

        # 기간 설정 그룹
        date_group = QGroupBox("기간별 수집")
        date_layout = QHBoxLayout()
        self.start_date = QDateEdit(QDate.currentDate().addYears(-1))
        self.end_date = QDateEdit(QDate.currentDate())
        date_layout.addWidget(QLabel("시작"));
        date_layout.addWidget(self.start_date)
        date_layout.addWidget(QLabel("종료"));
        date_layout.addWidget(self.end_date)
        date_group.setLayout(date_layout)
        main_layout.addWidget(date_group)

        # 수집 항목 그룹
        item_group = QGroupBox("수집 항목")
        item_grid = QGridLayout()
        self.check_items = {
            "댓글 내용": QCheckBox("댓글 내용"), "아이디": QCheckBox("아이디"),
            "이메일": QCheckBox("이메일"), "닉네임": QCheckBox("닉네임"),
            "제목": QCheckBox("제목"), "내용": QCheckBox("내용"), "중복제거": QCheckBox("계정 중복제거")
        }
        for i, (name, cb) in enumerate(self.check_items.items()):
            item_grid.addWidget(cb, i // 4, i % 4)
            cb.setChecked(True)
        item_group.setLayout(item_grid)
        main_layout.addWidget(item_group)

        # 수집 시작 버튼 및 로그창
        self.btn_start = QPushButton("수집 시작")
        self.btn_start.setStyleSheet("background-color: #28a745; height: 40px; font-weight: bold;")
        main_layout.addWidget(self.btn_start)

        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setMaximumHeight(150)
        self.log_display.setStyleSheet("background-color: #1e1e1e; color: #00ff00; font-family: Consolas;")
        main_layout.addWidget(self.log_display)

        self.setLayout(main_layout)
        self.setWindowTitle("네이버 카페 데이터 수집기 v0.4")
        self.resize(600, 750)