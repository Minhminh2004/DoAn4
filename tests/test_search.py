# tests/test_search.py
import os, re, pytest, unicodedata, pathlib
from selenium.webdriver.support.ui import WebDriverWait
from pages.search_page import SearchPage
from utils.excel import read_sheet

n = lambda s: re.sub(r"\s+"," ",(s or "")).strip().lower()
strip = lambda s: "".join(c for c in unicodedata.normalize("NFD", str(s or "")) if not unicodedata.combining(c))
keynorm = lambda x: re.sub(r"\s+","_", strip(x).lower().strip())
first = lambda row, cols: next((row.get(c) or row.get(keynorm(c)) for c in cols if (row.get(c) or row.get(keynorm(c)))), "")

DATA = read_sheet(os.path.join(pathlib.Path(__file__).resolve().parents[1], "data", "search_test.xlsx"), "Sheet1")

@pytest.mark.parametrize("row", DATA, ids=[str(first(r, ['case','ten_case','id']) or f"row{i+1}") for i, r in enumerate(DATA)])
def test_search(driver, base_url, row):
    kw  = str(first(row, ['keyword','tu_khoa','từ khóa']) or "")
    exp = str(first(row, ['expected','ket_qua','counter']) or "")

    p = SearchPage(driver)
    p.open_home(base_url)
    p.search(kw)
    WebDriverWait(driver, 10).until(lambda d: p.get_counter_text(1) != "")
    act = p.get_counter_text(2)

    print("\nTEST TÌM KIẾM")
    print("Từ khóa:", kw)
    print("Expected:", exp)
    print("Actual:", act)
    ok = n(exp) in n(act)
    print("Kết quả:", "PASS" if ok else "FAIL")
    assert ok, f"Mong đợi: {exp}\nThực tế: {act}"
