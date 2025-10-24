# pages/search_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage
import re, time

class SearchPage(BasePage):
    INPUT  = (By.XPATH, "/html/body/div[2]/header[2]/div/div[1]/div[2]/div/div/form/input")
    BTN    = (By.XPATH, "/html/body/div[2]/header[2]/div/div[1]/div[2]/div/div/form/button")
    COUNTER= (By.XPATH, "/html/body/div[2]/div/div[2]/div/div[2]/div/div/div[1]/div/div[3]")

    def open_home(self, base_url):
        super().open(base_url)
        try: WebDriverWait(self.driver, 8).until(EC.presence_of_element_located(self.INPUT))
        except TimeoutException: self.driver.refresh(); WebDriverWait(self.driver, 6).until(EC.presence_of_element_located(self.INPUT))
        time.sleep(0.2)

    def search(self, keyword):
        self.type(self.INPUT, str(keyword))
        try: self.click(self.BTN)
        except Exception:
            el = self.driver.find_element(*self.INPUT)
            self.driver.execute_script("if(arguments[0].form) arguments[0].form.submit();", el)

    def get_counter_text(self, t=10):
        try:
            WebDriverWait(self.driver, t).until(EC.presence_of_element_located(self.COUNTER))
            return self.text_of(self.COUNTER, 4)
        except TimeoutException: return ""

    def parse_counter(self, t=8):
        m = re.search(r"(\d+)\s*/\s*(\d+)", self.get_counter_text(t))
        return (int(m.group(1)), int(m.group(2))) if m else (None, None)
