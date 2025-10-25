# tests/test_dathang.py
import pytest
from selenium.webdriver.support.ui import WebDriverWait
from pages.danhsach_page import ProductListPage
from pages.dathang_page import DathangPage
from utils.excel import read_sheet

@pytest.mark.order(1)
def test_dat_hang_e2e(driver, base_url):
    print("\n=== BẮT ĐẦU QUY TRÌNH ĐẶT HÀNG ===")

    row = read_sheet("data/dathang_test.xlsx", "Sheet1")[0]
    keyword = (row.get("keyword") or row.get("tu_khoa") or row.get("từ khóa") or "").strip()
    assert keyword, "Thiếu cột keyword (hoặc tu_khoa / từ khóa) trong Excel."

    # Tìm sản phẩm và thêm vào giỏ
    plist = ProductListPage(driver)
    plist.open_home_and_search(base_url, keyword)
    plist.wait_for_products()
    plist.add_first_to_cart()
    plist.go_to_checkout_from_popup()

    # Điền thông tin khách hàng và đặt hàng
    checkout = DathangPage(driver)
    checkout.fill_info(
        name=row["name"],
        phone=row["phone"],
        email=row["email"],
        province=row["tinh"],
        district=row["huyen"],
        ward=row["xa"],
        address=row["diachi"],
        note=row.get("note", "")
    )
    checkout.place_order()

    # Kiểm tra kết quả
    ok = checkout.is_success()
    assert ok, "Đặt hàng không thành công."
    print("=== ĐẶT HÀNG THÀNH CÔNG ===")
