# pages/base_page.py
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def _wait(self, cond, timeout=10):
        return WebDriverWait(self.driver, timeout).until(cond)

    def wait_visible(self, loc, t=10):
        return self._wait(EC.visibility_of_element_located(loc), t)

    def wait_clickable(self, loc, t=10):
        return self._wait(EC.element_to_be_clickable(loc), t)

    def click(self, loc, t=None, timeout=10):
        if t is None:
            t = timeout
        self.wait_clickable(loc, t).click()

    def type(self, loc, value, clear=True, t=10):
        el = self.wait_visible(loc, t)
        if clear:
            el.clear()
        el.send_keys(value)

    def text_of(self, loc, t=10):
        try:
            return (self.wait_visible(loc, t).get_attribute("textContent") or "").strip()
        except Exception:
            return ""

    def exists(self, loc, t=2):
        try:
            self.wait_visible(loc, t)
            return True
        except Exception:
            return False

    def open(self, url):
        self.driver.get(url)
