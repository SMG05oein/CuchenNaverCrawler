import sys
import time
from threading import Thread
from CrawlerGUI2 import ScraperGUI
from Crawler2 import CafeScraperEngine


class MainController:
    def __init__(self):
        self.gui = ScraperGUI()
        # GUI 버튼 클릭 이벤트 연결
        self.gui.btn_start.configure(command=self.start_threads)

    def log_to_gui(self, message, cafe_id="SYSTEM"):
        # GUI의 로그 텍스트박스에 실시간으로 메시지 기록
        self.gui.log_text.insert("end", f"[{time.strftime('%H:%M:%S')}][{cafe_id}] {message}\n")
        self.gui.log_text.see("end")

    def get_tasks_from_gui(self):
        """GUI 위젯들로부터 현재 입력된 태스크(카테고리/키워드) 정보 추출"""
        tasks = []
        for g in self.gui.category_groups:
            cat = g.entry_cat.get().strip()
            target = g.option_target.get()
            kws = [k.strip() for k in g.entry_kws.get().split(",") if k.strip()]
            if cat and kws:
                tasks.append({"category": cat, "target": target, "keywords": kws})
        return tasks

    def start_threads(self):
        # 1. 입력값 검증
        urls = [g.entry_url.get().strip() for g in self.gui.cafe_groups if g.entry_url.get().strip()]
        if not urls: return

        # 2. 버튼 비활성화
        self.gui.btn_start.configure(state="disabled", text="⏳ 수집 중...")

        # 3. 모든 설정값 패키징
        params = {
            "id": self.gui.entry_id.get().strip(),
            "pw": self.gui.entry_pw.get().strip(),
            "start_date": self.gui.entry_start.get().strip(),
            "end_date": self.gui.entry_end.get().strip(),
            "tasks": self.get_tasks_from_gui()
        }

        # 4. 각 카페 URL 별로 개별 스레드 실행
        for target_url in urls:
            engine = CafeScraperEngine(self.log_to_gui)
            Thread(target=engine.run_scraper_for_cafe, args=(target_url, params), daemon=True).start()

        # 5. 일정 시간 후 버튼 복구 (또는 수집 완료 로직에 맞게 조정)
        self.gui.after(5000, lambda: self.gui.btn_start.configure(state="normal", text="🚀 수집 시작"))

    def run(self):
        self.gui.mainloop()


if __name__ == "__main__":
    MainController().run()