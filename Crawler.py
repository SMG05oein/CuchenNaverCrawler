import time
import pyperclip
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class NaverCrawler:
    def __init__(self):
        self.driver = None
        self.wait = None

    def init_driver(self):
        """드라이버 초기화 및 봇 감지 회피 설정"""
        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--start-maximized")

        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        })
        self.wait = WebDriverWait(self.driver, 20)

    def login(self, user_id, user_pw):
        """로그인 로직"""
        if not self.driver:
            self.init_driver()

        self.driver.get("https://nid.naver.com/nidlogin.login")
        time.sleep(1)

        # ID/PW 입력 (복사 붙여넣기 방식)
        pyperclip.copy(user_id)
        self.wait.until(EC.presence_of_element_located((By.ID, 'id'))).send_keys(Keys.CONTROL + 'v')
        time.sleep(0.5)
        pyperclip.copy(user_pw)
        self.driver.find_element(By.ID, 'pw').send_keys(Keys.CONTROL + 'v')
        pyperclip.copy('')
        self.driver.find_element(By.ID, 'log.login').click()

        # 로그인 완료(URL 변경) 대기
        self.wait.until(lambda d: "nid.naver.com" not in d.current_url)
        return True

    def get_cafe_list(self):
        """가입 카페 목록 추출"""
        self.driver.get("https://section.cafe.naver.com/ca-fe/home")
        time.sleep(2)

        selector = ".section_home_my .cafe_name"
        elements = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector)))

        cafe_dict = {e.text: e.get_attribute("href") for e in elements if e.text}
        return cafe_dict