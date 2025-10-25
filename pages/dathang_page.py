# pages/dathang_page.py
import re, time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from pages.base_page import BasePage

n = lambda s: re.sub(r"\s+", " ", (s or "")).strip()

class DathangPage(BasePage):
    URL_PATH = "/thong-tin-khach-hang.html"

    # ----- text fields -----
    NAME    = (By.ID, "name_cart")
    PHONE   = (By.ID, "phone_cart")
    EMAIL   = (By.ID, "email_cart")
    ADDRESS = (By.ID, "address_cart")
    NOTE    = (By.ID, "note")

    # <select name="..."> (bị Select2 bọc)
    TINH_SELECT  = (By.NAME, "tinh")
    HUYEN_SELECT = (By.NAME, "huyen")
    XA_SELECT    = (By.NAME, "xa")

    # Combobox/Select2
    PROVINCE_COMBO_ANY  = (By.XPATH, "(//span[@role='combobox'])[1]")   # ô Tỉnh đầu tiên
    PROVINCE_COMBO_OPEN = (By.XPATH, "//span[@aria-expanded='true']")   # trạng thái đã mở
    DISTRICT_CONTAINER  = (By.XPATH, "//span[@id='select2-district_cart-container']")  # Quận/Huyện
    WARD_CONTAINER      = (By.XPATH, "//span[@id='select2-ward_cart-container']")      # Phường/Xã (đã thêm)

    # Đặt hàng
    PLACE   = (By.XPATH, "//button[contains(.,'Đặt Hàng') or contains(.,'Đặt hàng') or contains(.,'Hoàn tất')]")
    SUCCESS = (By.XPATH, "//*[contains(.,'Đặt hàng thành công') or contains(@class,'order-success')]")

    def open_info(self, base_url: str):
        self.open(base_url.rstrip("/") + self.URL_PATH)

    # -------------------- helpers --------------------
    def _visible_select_choose(self, select_el, text):
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", select_el)
        Select(select_el).select_by_visible_text(text)

    def _type_in_select2_search(self, text, timeout=12):
        inp = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH, "//input[contains(@class,'select2-search__field')]"))
        )
        inp.clear()
        inp.send_keys(text)
        time.sleep(0.25)
        inp.send_keys(Keys.ENTER)
        # chờ dropdown đóng
        WebDriverWait(self.driver, timeout).until_not(
            EC.presence_of_element_located((By.XPATH, "//input[contains(@class,'select2-search__field')]"))
        )

    def _select2_choose(self, hidden_select_locator, text, label):
        sel = WebDriverWait(self.driver, 12).until(EC.presence_of_element_located(hidden_select_locator))
        cands = sel.find_elements(
            By.XPATH, "following-sibling::*[contains(@class,'select2')][1]//span[contains(@class,'select2-selection')]"
        ) or sel.find_elements(By.XPATH, "following::span[contains(@class,'select2-selection')][1]")
        if not cands:
            raise RuntimeError("Không tìm thấy Select2 box cho " + label)
        box = cands[0]
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", box)
        WebDriverWait(self.driver, 8).until(EC.element_to_be_clickable(box))
        try:
            box.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", box)
        self._type_in_select2_search(text)

    # ----- Tỉnh: click combobox rồi đợi aria-expanded='true' -----
    def select_province_via_aria_expanded(self, province_text):
        try:
            combo = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.PROVINCE_COMBO_ANY)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", combo)
            try:
                combo.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", combo)

            WebDriverWait(self.driver, 6).until(
                EC.presence_of_element_located(self.PROVINCE_COMBO_OPEN)
            )
            self._type_in_select2_search(province_text, timeout=10)
        except Exception as e:
            # Fallback: qua <select name="tinh">
            try:
                self._select2_choose(self.TINH_SELECT, province_text, "Tỉnh/Thành phố")
            except Exception as ee:
                import pytest
                pytest.fail(f"Không thể chọn Tỉnh/Thành phố = '{province_text}' ({ee or e})")

    # ----- Huyện: ưu tiên click đúng //span[@id='select2-district_cart-container'] -----
    def select_district(self, district_text):
        try:
            box = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.DISTRICT_CONTAINER)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", box)
            try:
                box.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", box)

            self._type_in_select2_search(district_text, timeout=10)
            return
        except Exception:
            # Fallback: chọn qua <select name="huyen">
            try:
                el = WebDriverWait(self.driver, 6).until(EC.presence_of_element_located(self.HUYEN_SELECT))
                if el.tag_name.lower() == "select" and el.is_displayed():
                    self._visible_select_choose(el, district_text)
                else:
                    self._select2_choose(self.HUYEN_SELECT, district_text, "Quận/Huyện")
            except Exception as e:
                import pytest
                pytest.fail(f"Không thể chọn Quận/Huyện = '{district_text}' ({e})")

    # ----- Xã: ưu tiên click đúng //span[@id='select2-ward_cart-container'] -----
    def select_ward(self, ward_text):
        try:
            box = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.WARD_CONTAINER)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", box)
            try:
                box.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", box)

            self._type_in_select2_search(ward_text, timeout=10)
            return
        except Exception:
            # Fallback: chọn qua <select name="xa"> / Select2 bọc
            try:
                el = WebDriverWait(self.driver, 6).until(EC.presence_of_element_located(self.XA_SELECT))
                if el.tag_name.lower() == "select" and el.is_displayed():
                    self._visible_select_choose(el, ward_text)
                else:
                    self._select2_choose(self.XA_SELECT, ward_text, "Phường/Xã")
            except Exception as e:
                import pytest
                pytest.fail(f"Không thể chọn Phường/Xã = '{ward_text}' ({e})")

    # -------------------- public API --------------------
    def fill_info(self, name, phone, email, province, district, ward, address, note=""):
        print(">> Nhập thông tin KH…")
        self.type(self.NAME, name, 12)
        self.type(self.PHONE, phone, 12)
        self.type(self.EMAIL, email, 8)

        # Tỉnh → Huyện → Xã theo Excel
        self.select_province_via_aria_expanded(province); time.sleep(0.4)
        self.select_district(district); time.sleep(0.4)
        self.select_ward(ward)

        self.type(self.ADDRESS, address, 10)
        if note:
            self.type(self.NOTE, note, 6)

    def place_order(self): self.click(self.PLACE, 12)
    def is_success(self):  return self.exists(self.SUCCESS, 12)
