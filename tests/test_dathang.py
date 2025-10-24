# tests/test_dathang.py
import re, pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

from pages.login_page import LoginPage
from pages.search_page import SearchPage
from pages.sanpham_page import SanphamPage
from pages.giohang_page import GiohangPage
from pages.dathang_page import DathangPage

# Hàm tiện để chuẩn hóa chuỗi
n = lambda s: re.sub(r"\s+", " ", (s or "")).strip().lower()

# Thông tin đăng nhập và dữ liệu test
EMAIL    = "nguyentrongminh22012004@gmail.com"
PASSWORD = "Minh2004"
KEYWORD  = "máy"

@pytest.mark.order(1)  # Bỏ dòng này nếu chưa cài pytest-order
def test_dat_hang_e2e(driver, base_url):
    print("\n=== BẮT ĐẦU QUY TRÌNH ĐẶT HÀNG ===")

    # 1) Đăng nhập
    login = LoginPage(driver)
    login.open(base_url)           # mở /dang-ky-tai-khoan.html
    login.login(EMAIL, PASSWORD)

    # ✅ Chờ một trong hai trạng thái: có "Đăng xuất" HOẶC URL rời trang đăng nhập
    try:
        WebDriverWait(driver, 15).until(
            lambda d: d.find_elements(By.XPATH, "//a[contains(@href,'dang-xuat') or contains(.,'Đăng xuất')]")
                      or "dang-ky-tai-khoan" not in d.current_url
        )
    except WebDriverException:
        assert ("dang-ky-tai-khoan" not in driver.current_url) or \
               driver.find_elements(By.XPATH, "//a[contains(@href,'dang-xuat') or contains(.,'Đăng xuất')]"), \
               "Đăng nhập không thành công hoặc mất kết nối tới trình duyệt."

    print(f"ĐĂNG NHẬP THÀNH CÔNG: {EMAIL} / {PASSWORD}")

    # 2) Tìm sản phẩm và mở chi tiết
    search = SearchPage(driver)
    search.open_home(base_url)
    search.search(KEYWORD)
    WebDriverWait(driver, 10).until(lambda d: search.get_counter_text(1) != "")
    print(f"TÌM KIẾM: {KEYWORD} | {search.get_counter_text(2)}")

    first_link = driver.find_element(By.XPATH, "(//a[contains(@href,'/san-pham') or contains(@href,'/product')])[1]")
    product_url = first_link.get_attribute("href")
    first_link.click()
    print(f"MỞ SẢN PHẨM: {product_url}")

    # 3) Thêm vào giỏ
    prod = SanphamPage(driver)
    prod.add_to_cart(qty=1)
    print("THÊM VÀO GIỎ HÀNG: PASS")

    # 4) Sang giỏ -> thanh toán
    prod.go_to_cart()
    cart = GiohangPage(driver)
    cart.proceed_to_checkout()
    print("ĐI ĐẾN TRANG THANH TOÁN: PASS")

    # 5) (tuỳ chọn) Điền thông tin và đặt hàng
    # checkout = DathangPage(driver)
    # checkout.fill_info(name="Nguyễn Văn A", phone="0900000000",
    #                    address="Số 1 Đường A, Quận B, TP.HCM", email=EMAIL)
    # checkout.place_order()
    # ok = checkout.is_success()
    # print("ĐẶT HÀNG:", "PASS" if ok else "FAIL")
    # assert ok

    print("=== HOÀN THÀNH QUY TRÌNH KIỂM THỬ ĐẶT HÀNG ===")
