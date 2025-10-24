import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager   

BASE_URL = "https://www.ketnoitieudung.vn/"

@pytest.fixture(scope="session")
def base_url():
    return BASE_URL
@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless=new")  # cần thì bật CI
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--lang=vi-VN")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    d = webdriver.Chrome(service=service, options=options)
    d.set_page_load_timeout(45)
    d.implicitly_wait(5)
    yield d
    try:
        d.quit()
    except Exception:
        pass


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless=new")   # nếu chạy không cần GUI
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()
