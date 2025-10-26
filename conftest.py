# conftest.py
import os, time, logging, pytest, re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from openpyxl import Workbook

BASE_URL = "https://www.ketnoitieudung.vn/"
RUN_TS = time.strftime("%Y%m%d_%H%M%S")
ROOT = os.path.join("report", RUN_TS)
SS_DIR = os.path.join(ROOT, "screenshots")
os.makedirs(SS_DIR, exist_ok=True)

log = logging.getLogger("e2e")
if not log.handlers:
    log.setLevel(logging.INFO)
    fh = logging.FileHandler(os.path.join(ROOT, "test_run.log"), encoding="utf-8")
    fh.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    log.addHandler(fh)

@pytest.fixture(scope="session")
def base_url(): return BASE_URL

@pytest.fixture
def driver():
    o = Options(); o.add_argument("--start-maximized")
    if os.getenv("HEADLESS") == "1": o.add_argument("--headless=new")
    o.add_experimental_option("excludeSwitches", ["enable-automation"])
    o.add_experimental_option("useAutomationExtension", False)
    d = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=o)
    d.set_page_load_timeout(45); d.implicitly_wait(5)
    yield d
    try: d.quit()
    except: pass

_RUN_ROWS, _DATA_HDRS = [], []
_EXTRA = ["Actual", "Status", "Time", "Screenshot"]

def _param_row(item):
    if getattr(item, "callspec", None):
        for k in ("row","r","data"):
            v = item.callspec.params.get(k)
            if isinstance(v, dict): return v
    return {}

def _keep_hdrs(d):
    global _DATA_HDRS
    if not _DATA_HDRS and d: _DATA_HDRS = list(d.keys())

def _actual_from_stdout(s):
    for lab in ("Actual message","Actual URL","Actual","Actual result"):
        m = re.search(rf"{lab}\s*:\s*(.*)", s or "", re.I)
        if m: return m.group(1).strip()
    return ""

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    out = yield; rep = out.get_result()
    if rep.when != "call": return
    status = "PASS" if rep.passed else "FAIL"
    shot = ""
    drv = item.funcargs.get("driver")
    if rep.failed and drv:
        shot = os.path.join(SS_DIR, f"{item.name}_{time.strftime('%H%M%S')}.png")
        try: drv.save_screenshot(shot); print(f"\n[FAIL] {item.name} -> {shot}"); log.error(f"[FAIL] {item.name} -> {shot}")
        except Exception as e: log.error(f"shot failed: {e}")

    data = _param_row(item); _keep_hdrs(data)
    _RUN_ROWS.append({
        **data,
        "Actual": _actual_from_stdout(rep.capstdout),
        "Status": status,
        "Time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "Screenshot": shot
    })

def pytest_sessionfinish(session, exitstatus):
    os.makedirs(ROOT, exist_ok=True)
    hdrs = list(_DATA_HDRS) + [h for h in _EXTRA if h not in _DATA_HDRS]
    wb = Workbook(); ws = wb.active; ws.title = "BaoCao"; ws.append(hdrs)
    for r in _RUN_ROWS: ws.append([r.get(h,"") for h in hdrs])
    out = os.path.join(ROOT, "BaoCao.xlsx"); wb.save(out)
    print(f"\n[REPORT] Saved: {out}"); log.info(f"Saved: {out}")
