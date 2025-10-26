# pages/danhsach_page.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from .base_page import BasePage

class ProductListPage(BasePage):
    SEARCH_INPUT = (By.XPATH, "/html/body/div[2]/header[2]/div/div[1]/div[2]/div/div/form/input")
    SEARCH_BTN   = (By.XPATH, "/html/body/div[2]/header[2]/div/div[1]/div[2]/div/div/form/button")

    # Khu vực danh sách & nút thêm giỏ
    PRODUCT_CARD = (By.XPATH, "//div[contains(@class,'product') or contains(@class,'item-product')]")
    ADD_BTN_ANY  = (By.XPATH, "(//button[contains(.,'Thêm vào giỏ') or contains(.,'Mua ngay')])[1]")

    # Mini-cart popup & nút Thanh toán
    MINICART_ANY     = (By.XPATH, "/html/body/div[5]") 
    CHECKOUT_BUTTONS = [
        (By.XPATH, "/html/body/div[5]/div[2]/div[4]/a[2]"),
        (By.XPATH, "//a[contains(.,'Thanh toán')]"),
        (By.XPATH, "//button[contains(.,'Thanh toán')]"),
        (By.XPATH, "//a[contains(@href,'thong-tin-khach-hang')]"),
    ]

    def open_home_and_search(self, base_url: str, keyword: str):
        """Mở trang chủ, nhập keyword và submit form tìm kiếm."""
        self.open(base_url)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.SEARCH_INPUT))
        self.type(self.SEARCH_INPUT, str(keyword), 8)
        try:
            self.click(self.SEARCH_BTN, 6)
        except Exception:
            el = self.driver.find_element(*self.SEARCH_INPUT)
            self.driver.execute_script("if(arguments[0].form) arguments[0].form.submit();", el)

    def wait_for_products(self, timeout: int = 12):
        """Đợi danh sách sản phẩm xuất hiện."""
        WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(self.PRODUCT_CARD))

    def _hover_first_card(self, timeout: int = 8):
        card = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(self.PRODUCT_CARD))
        try:
            ActionChains(self.driver).move_to_element(card).perform()
            time.sleep(0.3)  
        except Exception:
            pass

    def add_first_product_to_cart(self, timeout: int = 10):
        """Bấm 'Thêm vào giỏ hàng' cho sản phẩm đầu danh sách."""
        last_err = None
     
        self._hover_first_card()

        try:
            btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.ADD_BTN_ANY)
            )
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
            try:
                btn.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", btn)
            return
        except Exception as e:
            last_err = e


        try:
            btn = self.driver.find_element(*self.ADD_BTN_ANY)
            self.driver.execute_script("arguments[0].click();", btn)
            return
        except Exception as e:
            last_err = e

        raise AssertionError(
            f"Không tìm thấy nút 'Thêm vào giỏ/Mua ngay' trên trang danh sách. ({last_err})"
        )


    def add_first_to_cart(self, timeout: int = 10):
        return self.add_first_product_to_cart(timeout)

    def go_to_checkout_from_popup(self, timeout: int = 12):
        """Đợi mini-cart xuất hiện rồi bấm 'Thanh toán' để sang trang Thông tin khách hàng."""
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(self.MINICART_ANY)
        )
        time.sleep(0.5)  

     
        for by in self.CHECKOUT_BUTTONS:
            els = self.driver.find_elements(*by)
            if not els:
                continue
            btn = els[0]
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
            try:
                WebDriverWait(self.driver, 5).until(lambda d: btn.is_displayed())
                try:
                    btn.click()
                except Exception:
                    self.driver.execute_script("arguments[0].click();", btn)
                # Đợi URL sang trang checkout
                WebDriverWait(self.driver, 12).until(
                    lambda d: "thong-tin-khach-hang" in d.current_url
                )
                return

            except Exception:
                continue

        raise AssertionError("Không bấm được nút 'Thanh toán' trong mini-cart.")
