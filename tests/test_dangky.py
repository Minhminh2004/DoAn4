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

n = lambda s: re.sub(r"\s+"," ",(s or "")).strip().lower()
EMAIL, PASSWORD, KEYWORD = "nguyentrongminh22012004@gmail.com", "Minh2004", "vít"

@pytest.mark.order(1)
def test_dat_hang_e2e(driver, base_url):
    print("\n=== BẮT ĐẦU QUY TRÌNH ĐẶT HÀNG ===")

    # 1️⃣ Đăng nhập
    login = LoginPage(driver)
    login.open(base_url)
    login.login(EMAIL, PASSWORD)
    try:
        WebDriverWait(driver, 15).until(
            lambda d: d.find_elements(By.XPATH, "//a[contains(@href,'dang-xuat') or contains(.,'Đăng xuất')]")
                      or "dang-ky-tai-khoan" not in d.current_url
        )
    except WebDriverException:
        assert ("dang-ky-tai-khoan" not in driver.current_url) or \
               driver.find_elements(By.XPATH, "//a[contains(@href,'dang-xuat') or contains(.,'Đăng xuất')]"), \
               " Đăng nhập thất bại hoặc mất kết nối."
    print(f" ĐĂNG NHẬP: {EMAIL} / {PASSWORD}")

    # 2️⃣ Tìm sản phẩm
    search = SearchPage(driver)
    search.open_home(base_url)
    search.search(KEYWORD)
    WebDriverWait(driver, 10).until(lambda d: search.get_counter_text(1) != "")
    print(f"🔍 TÌM KIẾM: {KEYWORD} | {search.get_counter_text(2)}")

    first_link = driver.find_element(By.XPATH, "(//a[contains(@href,'/san-pham/') and not(contains(@href,'?'))])[1]")
    product_url = first_link.get_attribute("href")
    first_link.click()
    print(f"🛒 MỞ SẢN PHẨM: {product_url}")

    # 3 Thêm vào giỏ
    prod = SanphamPage(driver)
    prod.add_to_cart(qty=1)
    print("THÊM VÀO GIỎ HÀNG THÀNH CÔNG")

    # 4️ Giỏ hàng → Thanh toán
    prod.go_to_cart()
    cart = GiohangPage(driver)
    cart.proceed_to_checkout()
    print(" ĐI ĐẾN TRANG THANH TOÁN")

    # 5️ Điền thông tin & Đặt hàng
    checkout = DathangPage(driver)
    checkout.fill_info(
        name="Nguyễn Trọng Minh",
        phone="0901234567",
        address="123 Nguyễn Trãi, Quận 1, TP.HCM",
        email=EMAIL,
        note="Tự động test thanh toán"
    )
    checkout.place_order()

    ok = checkout.is_success()
    print(" KẾT QUẢ ĐẶT HÀNG:", "PASS " if ok else "FAIL ")
    assert ok, "Không thấy thông báo thành công sau khi đặt hàng."

    print("=== HOÀN TẤT KIỂM THỬ ĐẶT HÀNG ===")
