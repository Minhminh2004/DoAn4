# pages/cart_page.py
from selenium.webdriver.common.by import By
from .base_page import BasePage

class GiohangPage(BasePage):
    CHECKOUT_BTN = (By.XPATH, "//a[contains(.,'Thanh toán') or contains(@href,'thanh-toan') or self::button[contains(.,'Thanh toán')]]")
    def proceed_to_checkout(self):
        self.click(self.CHECKOUT_BTN, t=15)
