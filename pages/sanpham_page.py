# pages/sanpham_page.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class SanphamPage(BasePage):
    # Nút thêm giỏ trong trang chi tiết (nhiều biến thể)
    ADD_BTN_CANDIDATES = [
        (By.XPATH, "//button[contains(.,'Thêm vào giỏ') or contains(.,'Mua ngay')]"),
        (By.CSS_SELECTOR, ".btn-add-cart, .btn-buy, .add-to-cart, button[name='add']"),
    ]

    def _click_js(self, el):
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        WebDriverWait(self.driver, 6).until(lambda d: el.is_displayed())
        try:
            el.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", el)

    def add_to_cart(self, qty=1, timeout=15):
        # (nếu có ô số lượng bạn có thể thêm vào đây)
        last_err = None
        for loc in self.ADD_BTN_CANDIDATES:
            try:
                btn = WebDriverWait(self.driver, 6).until(EC.element_to_be_clickable(loc))
                self._click_js(btn)
                time.sleep(0.5)  # đợi mini-cart pop
                return
            except Exception as e:
                last_err = e
        raise AssertionError(f"Không click được 'Thêm vào giỏ/Mua ngay' trong trang chi tiết. ({last_err})")
