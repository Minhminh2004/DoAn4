# tests/test_search.py
import os, re, pytest, unicodedata, pathlib
from selenium.webdriver.support.ui import WebDriverWait
from pages.search_page import SearchPage
from utils.excel import read_sheet

n = lambda s: re.sub(r"\s+"," ",(s or "")).strip().lower()
strip = lambda s: "".join(c for c in unicodedata.normalize("NFD", str(s)) if not unicodedata.combining(c))
k = lambda k: re.sub(r"\s+","_", strip(k).lower().strip())
f = lambda r, c: next((r.get(c) or r.get(k(c)) for c in c if (r.get(c) or r.get(k(c)))), "")

DATA = read_sheet(os.path.join(pathlib.Path(__file__).resolve().parents[1], "data", "search_test.xlsx"), "Sheet1")

@pytest.mark.parametrize("r", DATA, ids=[f(r,['case','ten_case','id']) or f"row{i+1}" for i,r in enumerate(DATA)])
def test_search(driver, base_url, r):
    kw, exp = str(f(r,['keyword','tu_khoa','từ khóa']) or ""), str(f(r,['expected','ket_qua','counter']) or "")
    p = SearchPage(driver); p.open_home(base_url); p.search(kw)
    WebDriverWait(driver, 10).until(lambda d: p.get_counter_text(1) != "")
    act = p.get_counter_text(2)
    print("\nTEST TÌM KIẾM"); print("Từ khóa:", kw); print("Expected:", exp); print("Actual:", act)
    ok = n(exp) in n(act); print("Kết quả:", "PASS" if ok else "FAIL")
    assert ok, f"Mong đợi: {exp}\nThực tế: {act}"
