# pages/dangky_page.py
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage

class DangKyPage(BasePage):
    PATH = "/dang-ky-tai-khoan.html"

    FORM  = (By.XPATH, "//form[.//button[contains(normalize-space(.),'Đăng ký')]]")
    NAME  = (By.XPATH, "//form[.//button[contains(.,'Đăng ký')]]//input[@name='fullname' or @id='FullName' or @type='text']")
    EMAIL = (By.XPATH, "//form[.//button[contains(.,'Đăng ký')]]//input[@type='email' or @name='email' or @id='Email']")
    PHONE = (By.XPATH, "//form[.//button[contains(.,'Đăng ký')]]//input[@type='tel' or @name='phone' or @id='Phone']")
    PASS  = (By.XPATH, "//form[.//button[contains(.,'Đăng ký')]]//input[@type='password' or @name='password' or @id='Password']")
    CONF  = (By.XPATH, "//form[.//button[contains(.,'Đăng ký')]]//input[@type='password' or @name='confirm_password' or @id='ConfirmPassword']")
    SUBMIT= (By.XPATH, "//form[.//button[contains(.,'Đăng ký')]]//button[@type='submit' or contains(.,'Đăng ký')]")
    ERR   = (By.XPATH, "/html/body/div[8]/div/div[2]")
    OK    = (By.CSS_SELECTOR, "a[href*='dang-xuat'], a[href*='tai-khoan'], .header-user-logged, .account-logged")

    def open(self, base_url):
        super().open(base_url.rstrip("/") + self.PATH)
        for loc in (self.FORM,self.NAME,self.EMAIL,self.PHONE,self.PASS,self.CONF,self.SUBMIT): self.wait_visible(loc, 15)

    def dangky(self, name, email, phone, password, confirm):
        self.type(self.NAME, name); self.type(self.EMAIL, email); self.type(self.PHONE, phone)
        self.type(self.PASS, password); self.type(self.CONF, confirm); self.click(self.SUBMIT)

    def get_error_text(self, t=10):
        try: return self.text_of(self.ERR, t)
        except TimeoutException: return ""

    def is_success(self): return self.exists(self.OK, 8)
