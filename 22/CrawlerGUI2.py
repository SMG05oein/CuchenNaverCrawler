import customtkinter as ctk
import time

class CafeUrlGroup(ctk.CTkFrame):
    def __init__(self, master, on_delete, placeholder_text=""):
        super().__init__(master, fg_color="transparent")
        self.on_delete = on_delete
        self.pack(fill="x", pady=2, padx=5)
        self.entry_url = ctk.CTkEntry(self, placeholder_text=placeholder_text, height=32)
        self.entry_url.pack(side="left", padx=(5, 5), pady=2, expand=True, fill="x")
        self.btn_del = ctk.CTkButton(self, text="✕", width=35, height=32, fg_color="#e74c3c", hover_color="#c0392b",
                                     command=self.delete_self)
        self.btn_del.pack(side="right", padx=5)

    def delete_self(self):
        self.on_delete(self)
        self.destroy()

class CategoryGroup(ctk.CTkFrame):
    def __init__(self, master, on_delete):
        super().__init__(master, fg_color="transparent")
        self.on_delete = on_delete
        self.pack(fill="x", pady=2, padx=5)
        self.entry_cat = ctk.CTkEntry(self, placeholder_text="카테고리", width=100, height=32)
        self.entry_cat.pack(side="left", padx=5, pady=2)
        self.option_target = ctk.CTkOptionMenu(self, values=["글+댓글", "제목만", "작성자", "댓글"], width=110, height=32)
        self.option_target.set("글+댓글")
        self.option_target.pack(side="left", padx=5, pady=2)
        self.entry_kws = ctk.CTkEntry(self, placeholder_text="키워드 (쉼표 구분)", height=32)
        self.entry_kws.pack(side="left", padx=5, pady=2, expand=True, fill="x")
        self.btn_del = ctk.CTkButton(self, text="✕", width=35, height=32, fg_color="#e74c3c", hover_color="#c0392b",
                                     command=self.delete_self)
        self.btn_del.pack(side="right", padx=5)

    def delete_self(self):
        self.on_delete(self)
        self.destroy()

class ScraperGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Naver Cafe Pro Scraper v3.9 (Modularized)")
        self.geometry("1650x950")

        self.cafe_groups = []
        self.category_groups = []
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=15, pady=15)

        self.left_panel = ctk.CTkFrame(self.main_container, width=850)
        self.left_panel.pack(side="left", fill="both", expand=False, padx=(0, 10))
        self.left_panel.pack_propagate(False)

        ctk.CTkLabel(self.left_panel, text="⚙️ SCRAPER SETTINGS", font=("Pretendard", 22, "bold"),
                     text_color="#3498db").pack(pady=20)
        self.btn_start = ctk.CTkButton(self.left_panel, text="🚀 수집 시작",
                                       fg_color="#2ecc71", hover_color="#27ae60", height=65,
                                       font=("Pretendard", 18, "bold"))
        self.btn_start.pack(side="bottom", pady=25, padx=20, fill="x")

        self.scroll_area = ctk.CTkScrollableFrame(self.left_panel, fg_color="transparent")
        self.scroll_area.pack(side="top", fill="both", expand=True, padx=5, pady=5)

        self.box_login = self.create_box(self.scroll_area, "🔑 로그인 설정")
        self.entry_id = ctk.CTkEntry(self.box_login, placeholder_text="아이디", width=250)
        self.entry_id.pack(side="left", padx=25, pady=15, expand=True)
        self.entry_pw = ctk.CTkEntry(self.box_login, placeholder_text="비밀번호", width=250, show="*")
        self.entry_pw.pack(side="left", padx=25, pady=15, expand=True)

        self.box_cafe = self.create_box(self.scroll_area, "🌐 카페 URL")
        self.cafe_container = ctk.CTkFrame(self.box_cafe, fg_color="transparent")
        self.cafe_container.pack(fill="x", padx=5)
        ctk.CTkButton(self.box_cafe, text="+ URL 추가", fg_color="#34495e", height=30, command=self.add_cafe).pack(pady=10)
        self.add_cafe(placeholder_text="https://cafe.naver.com/...")

        self.box_date = self.create_box(self.scroll_area, "📅 분석 기간")
        self.date_inner = ctk.CTkFrame(self.box_date, fg_color="transparent")
        self.date_inner.pack(pady=10)
        self.entry_start = ctk.CTkEntry(self.date_inner, placeholder_text="시작일", width=180)
        self.entry_start.insert(0, "2026-01-01")
        self.entry_start.pack(side="left", padx=10)
        ctk.CTkLabel(self.date_inner, text="~", font=("Pretendard", 18)).pack(side="left")
        self.entry_end = ctk.CTkEntry(self.date_inner, placeholder_text="종료일", width=180)
        self.entry_end.insert(0, "2026-03-02")
        self.entry_end.pack(side="left", padx=10)

        self.box_kw = self.create_box(self.scroll_area, "🔍 분류 및 필터")
        self.group_container = ctk.CTkFrame(self.box_kw, fg_color="transparent")
        self.group_container.pack(fill="x", padx=5)
        ctk.CTkButton(self.box_kw, text="+ 카테고리 추가", fg_color="#34495e", height=30, command=self.add_category).pack(pady=10)
        self.add_category()

        self.right_panel = ctk.CTkFrame(self.main_container)
        self.right_panel.pack(side="right", fill="both", expand=True)
        self.log_text = ctk.CTkTextbox(self.right_panel, font=("Consolas", 14), border_width=1)
        self.log_text.pack(fill="both", expand=True, padx=15, pady=15)

    def create_box(self, master, title):
        box = ctk.CTkFrame(master, border_width=2, border_color="#3B3B3B")
        box.pack(pady=10, padx=10, fill="x")
        ctk.CTkLabel(box, text=title, font=("Pretendard", 13, "bold")).pack(pady=5)
        return box

    def add_cafe(self, placeholder_text="https://cafe.naver.com/..."):
        group = CafeUrlGroup(self.cafe_container, self.remove_cafe, placeholder_text=placeholder_text)
        self.cafe_groups.append(group)

    def remove_cafe(self, group):
        if group in self.cafe_groups: self.cafe_groups.remove(group)

    def add_category(self):
        group = CategoryGroup(self.group_container, self.remove_category)
        self.category_groups.append(group)

    def remove_category(self, group):
        if group in self.category_groups: self.category_groups.remove(group)