import sys
import time
from PyQt6.QtWidgets import QApplication
from CrawlerGUI import NaverCrawlerGUI
from Crawler import NaverCrawler

class MainApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.gui = NaverCrawlerGUI()
        self.engine = NaverCrawler()
        self.cafe_data = {}

        # 시그널-슬롯 연결 (GUI의 버튼들과 MainApp의 함수 연결)
        self.gui.btn_login.clicked.connect(self.run_login)
        self.gui.btn_fetch_cafes.clicked.connect(self.run_fetch_cafes)
        self.gui.btn_select_cafe.clicked.connect(self.run_select_cafe)
        self.gui.btn_start.clicked.connect(self.run_start_crawling)

    def log(self, text):
        self.gui.log_display.append(f"[{time.strftime('%H:%M:%S')}] {text}")

    def run_login(self):
        id_val = self.gui.id_input.text()
        pw_val = self.gui.pw_input.text()
        if not id_val or not pw_val:
            self.log("⚠️ ID/PW를 입력해주세요.")
            return

        self.log("🚀 로그인 시도 중...")
        try:
            if self.engine.login(id_val, pw_val):
                self.log("✅ 로그인 성공!")
                self.run_fetch_cafes()
        except Exception as e:
            self.log(f"❌ 로그인 오류: {str(e)}")

    def run_fetch_cafes(self):
        self.log("📂 카페 목록 갱신 중...")
        try:
            self.cafe_data = self.engine.get_cafe_list()
            self.gui.cafe_list.clear()
            for name in self.cafe_data.keys():
                self.gui.cafe_list.addItem(name)
            self.log(f"✅ {len(self.cafe_data)}개 카페 로드 완료")
        except Exception as e:
            self.log(f"❌ 목록 로드 오류: {str(e)}")

    def run_select_cafe(self):
        name = self.gui.cafe_list.currentText()
        if name in self.cafe_data:
            self.engine.driver.get(self.cafe_data[name])
            self.log(f"📍 '{name}' 이동 완료")
        else:
            self.log("⚠️ 카페를 먼저 선택해 주세요.")

    def run_start_crawling(self):
        keyword = self.gui.keyword_input.text()
        if not keyword:
            self.log("⚠️ 검색 키워드를 입력해 주세요.")
            return
        self.log(f"🔍 키워드 '{keyword}' 수집을 준비합니다...")

    def run(self):
        self.gui.show()
        sys.exit(self.app.exec())

if __name__ == "__main__":
    MainApp().run()