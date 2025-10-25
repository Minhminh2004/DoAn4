# conftest.py
import os, time, logging, pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

BASE_URL = "https://www.ketnoitieudung.vn/"
RUN_TS = time.strftime("%Y%m%d_%H%M%S")
ROOT = os.path.join("artifacts", RUN_TS)
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
    d.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    yield
    rep = call.excinfo
    if not rep: return
    drv = item.funcargs.get("driver")
    if drv:
        path = os.path.join(SS_DIR, f"{item.name}_{time.strftime('%H%M%S')}.png")
        try:
            drv.save_screenshot(path)
            log.error(f"[FAIL] {item.name} -> {path}")
            print(f"\n[FAIL] {item.name} -> screenshot: {path}")
        except Exception as e:
            log.error(f"Screenshot failed: {e}")