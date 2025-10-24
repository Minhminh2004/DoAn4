# pages/product_page.py
from selenium.webdriver.common.by import By
from .base_page import BasePage

class SanphamPage(BasePage):
    QTY_INPUT = (By.XPATH, "//input[@type='number' or contains(@name,'qty') or contains(@id,'qty')]")
    ADD_BTN   = (By.XPATH, "//button[contains(.,'Thêm vào giỏ') or contains(.,'Mua ngay') or contains(@class,'add-to-cart')]")
    CART_LINK = (By.XPATH, "//a[contains(@href,'gio-hang') or contains(.,'Giỏ hàng')]")
    TOAST     = (By.XPATH, "//*[contains(@class,'toast') or contains(@class,'alert') or contains(.,'đã thêm vào giỏ')]")

    def add_to_cart(self, qty=1):
        try: self.type(self.QTY_INPUT, str(qty), t=5)
        except: pass
        self.click(self.ADD_BTN, t=15)
        try: self.wait(self.TOAST, t=5)
        except: pass

    def go_to_cart(self):
        self.click(self.CART_LINK, t=10)
