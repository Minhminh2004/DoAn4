# tests/test_dangky.py
import re, os, pathlib, pytest
from selenium.webdriver.support.ui import WebDriverWait
from pages.dangky_page import DangKyPage
from utils.excel import read_sheet

n = lambda s: re.sub(r"\s+", " ", (s or "")).strip().lower()
DATA = read_sheet(
    os.path.join(pathlib.Path(__file__).resolve().parents[1], "data", "dangky_test.xlsx"),
    "Sheet1"
)

@pytest.mark.parametrize("row", DATA, ids=[f"row{i+1}" for i, _ in enumerate(DATA)])
def test_dangky(driver, base_url, row):
    name  = str(row.get("name") or row.get("full_name") or "")
    phone = str(row.get("phone") or "")
    email = str(row.get("email") or "")
    pwd   = str(row.get("password") or "")
    conf  = str(row.get("confirm_password") or "")
    exp   = str(row.get("expected") or "")

    page = DangKyPage(driver)
    page.open(base_url)
    page.dangky(name, email, phone, pwd, conf)

    print("\nTEST ĐĂNG KÝ")
    print(f"Họ tên: {name}")
    print(f"Số điện thoại: {phone}")
    print(f"Email: {email}")
    print(f"Mật khẩu: {pwd}")
    print(f"Xác nhận mật khẩu: {conf}")
    print(f"Expected: {exp}")

    if n(exp) == "success":
        ok = WebDriverWait(driver, 15).until(lambda d: page.is_success())
        print(f"Thực tế: {'Đăng ký thành công' if ok else 'Không thành công'}")
        print("Kết quả:", "PASS" if ok else "FAIL")
        assert ok, "Không thấy trạng thái đã đăng ký thành công"
    else:
        actual = page.get_error_text(12)
        print(f"Thông báo thực tế: {actual}")
        passed = n(exp) in n(actual)
        print("Kết quả:", "PASS" if passed else "FAIL")
        assert passed, f"Mong đợi: {exp}\nThực tế: {actual}"
