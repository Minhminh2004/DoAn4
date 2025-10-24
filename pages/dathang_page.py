# pages/dathang_page.py
from selenium.webdriver.common.by import By
from .base_page import BasePage

class DathangPage(BasePage):
    URL_PATH = "/thong-tin-khach-hang.html"

    NAME    = (By.XPATH, "//input[@name='fullname' or @name='name' or contains(@placeholder,'Họ') or contains(@placeholder,'Tên')]")
    PHONE   = (By.XPATH, "//input[@name='phone' or @type='tel' or contains(@placeholder,'điện thoại') or contains(@placeholder,'phone')]")
    EMAIL   = (By.XPATH, "//input[@type='email' or @name='email']")
    ADDRESS = (By.XPATH, "//input[@name='address' or contains(@placeholder,'địa chỉ') or @id='address']")
    NOTE    = (By.XPATH, "//textarea[@name='note' or contains(@placeholder,'ghi chú') or contains(@placeholder,'note')]")
    PLACE   = (By.XPATH, "//button[contains(.,'Đặt hàng') or contains(.,'Hoàn tất') or contains(.,'Thanh toán')]")
    SUCCESS_MARK = (By.XPATH, "//*[contains(.,'Đặt hàng thành công') or contains(@class,'order-success')]")

    def open_info(self, base_url: str):
        self.open(base_url.rstrip('/') + self.URL_PATH)

    def fill_info(self, name, phone, address, email="", note=""):
        self.type(self.NAME, name, 15)
        self.type(self.PHONE, phone, 15)
        if email: self.type(self.EMAIL, email, 10)
        self.type(self.ADDRESS, address, 15)
        if note: self.type(self.NOTE, note, 10)

    def place_order(self):
        self.click(self.PLACE, 20)

    def is_success(self):
        return self.exists(self.SUCCESS_MARK, 12)
