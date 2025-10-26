# pages/search_page.py
import re, time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage

class SearchPage(BasePage):
    # Locator chính (bạn cung cấp)
    INPUT_PRI  = (By.XPATH, "/html/body/div[2]/header[2]/div/div[1]/div[2]/div/div/form/input")
    BUTTON_PRI = (By.XPATH, "/html/body/div[2]/header[2]/div/div[1]/div[2]/div/div/form/button")
    COUNTER    = (By.XPATH, "/html/body/div[2]/div/div[2]/div/div[2]/div/div/div[1]/div/div[3]")

    # Fallback khi layout đổi
    INPUT_FB   = (By.XPATH, "/html/body/div[2]/header[1]/div/div/div[1]/div[2]/form/input")
    BUTTON_FB  = (By.XPATH, "/html/body/div[2]/header[1]/div/div/div[1]/div[2]/form/button")
    INPUT_CSS  = (By.CSS_SELECTOR, "form[action*='san-pham' i] input[type='text'], form[action*='search' i] input[type='text']")
    BUTTON_CSS = (By.CSS_SELECTOR, "form[action*='san-pham' i] button, form[action*='search' i] button")

    def _pick_first(self, *locs):
        for loc in locs:
            try:
                WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(loc))
                return loc
            except Exception:
                continue
        raise AssertionError("Không tìm thấy ô tìm kiếm trên trang.")

    def open_home(self, base_url: str):
        self.open(base_url.rstrip("/") + "/")
        # chờ ô input nhanh – nếu fail, refresh 1 lần
        try:
            self._input  = self._pick_first(self.INPUT_PRI, self.INPUT_FB, self.INPUT_CSS)
            self._button = self._pick_first(self.BUTTON_PRI, self.BUTTON_FB, self.BUTTON_CSS)
        except AssertionError:
            self.driver.refresh()
            self._input  = self._pick_first(self.INPUT_PRI, self.INPUT_FB, self.INPUT_CSS)
            self._button = self._pick_first(self.BUTTON_PRI, self.BUTTON_FB, self.BUTTON_CSS)
        time.sleep(0.2)

    def search(self, keyword: str):
        self.type(self._input, str(keyword), 6)
        try:
            self.click(self._button, 6)
        except Exception:
            
            el = self.find(self._input, 2)
            self.driver.execute_script("if(arguments[0].form) arguments[0].form.submit();", el)

    def get_counter_text(self, timeout=8) -> str:
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(self.COUNTER))
            return (self.text_of(self.COUNTER, 2) or "").strip()
        except TimeoutException:
            return ""

    def parse_counter(self, timeout=6):
        m = re.search(r"(\d+)\s*/\s*(\d+)", self.get_counter_text(timeout))
        return (int(m.group(1)), int(m.group(2))) if m else (None, None)
