# pages/login_page.py
from selenium.webdriver.common.by import By
from .base_page import BasePage

class LoginPage(BasePage):
    URL_PATH = "/dang-ky-tai-khoan.html"

    # --- locators (giữ nguyên như bạn đang dùng) ---
    EMAIL  = (By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div[1]/div/div/form/div[1]/input")
    PASS   = (By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div[1]/div/div/form/div[2]/input")
    SUBMIT = (By.XPATH, "/html/body/div[2]/div/div[2]/div/div/div[1]/div/div/form/button")
    ERROR  = (By.XPATH, "/html/body/div[8]/div/div[2]")
    LOGOUT = (By.XPATH, "//a[contains(@href,'dang-xuat') or contains(.,'Đăng xuất')]")

    # --- actions ---
    def open(self, base_url: str):
        # dùng super().open để tránh đệ quy
        super().open(base_url.rstrip("/") + self.URL_PATH)

    def login(self, email: str, password: str):
        self.type(self.EMAIL, email)
        self.type(self.PASS, password)
        self.click(self.SUBMIT)

    def get_error_text(self) -> str:
        return self.text_of(self.ERROR, 12)

    def is_logged_in(self, timeout: int = 5) -> bool:
        # có link Đăng xuất => đã đăng nhập
        return self.exists(self.LOGOUT, timeout)
