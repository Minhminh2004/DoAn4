# pages/login_page.py
from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    URL_PATH = "/dang-ky-tai-khoan.html"
    EMAIL = (By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div[1]/div/div/form/div[1]/input")
    PASS  = (By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div[1]/div/div/form/div[2]/input")
    SUBMIT= (By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div[1]/div/div/form/button")
    ERROR = (By.XPATH, "/html/body/div[8]/div/div[2]")

    def open(self, base): super().open(base.rstrip("/") + self.URL_PATH)
    def login(self, email, pwd):
        self.type(self.EMAIL, email); self.type(self.PASS, pwd); self.click(self.SUBMIT)
    def get_error_text(self): return self.text_of(self.ERROR, 12)
