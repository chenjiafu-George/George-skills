import importlib.util
import os
import random
import sys
import time
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


ORIGINAL_CNKI_MCP = Path(
    r"C:\Users\陈家富\AppData\Local\uv\cache\archive-v0\7aU6uBft8GVwjlCiZJn6b\cnki_mcp_server.py"
)


def load_original_module():
    spec = importlib.util.spec_from_file_location("cnki_mcp_original", ORIGINAL_CNKI_MCP)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load original CNKI MCP from: {ORIGINAL_CNKI_MCP}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def patched_create_driver(self):
    chrome_binary = os.environ.get(
        "CNKI_CHROME_BINARY",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    )
    chromedriver_path = os.environ.get(
        "CNKI_CHROMEDRIVER_PATH",
        r"E:\daizuo\1111\.tmp\chromedriver-147\chromedriver-win64\chromedriver.exe",
    )
    user_data_dir = Path(
        os.environ.get(
            "CNKI_CHROME_USER_DATA_DIR",
            r"E:\daizuo\1111\.tmp\chrome-profile-selenium",
        )
    )
    headless = os.environ.get("CNKI_HEADLESS", "0").lower() in {"1", "true", "yes"}
    user_data_dir.mkdir(parents=True, exist_ok=True)

    options = Options()
    options.binary_location = chrome_binary
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument("--window-size=1365,1024")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    user_agents = getattr(self, "_user_agents", [])
    if user_agents:
        options.add_argument(f"user-agent={random.choice(user_agents)}")

    driver = webdriver.Chrome(
        service=Service(chromedriver_path),
        options=options,
    )
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                  get: () => undefined
                })
              """
        },
    )
    return driver


module = load_original_module()
module.BrowserPool._create_driver = patched_create_driver


def patched_search_cnki_sync(browser_pool, query: str, search_type: str = "主题", pages: int = 1, sort: str = "相关度") -> dict:
    resolved_type = module.resolve_search_type(search_type)
    resolved_sort = module.resolve_sort_type(sort)
    all_papers = []

    try:
        driver = browser_pool.navigate_to_cnki()

        if resolved_type != "主题":
            dropdown = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.ID, "DBFieldBox"))
            )
            dropdown.click()
            time.sleep(0.8)
            li = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, f'//div[@id="DBFieldList"]//li[@value="{module.SEARCH_TYPES[resolved_type]}"]')
                )
            )
            driver.execute_script("arguments[0].click();", li)
            time.sleep(0.5)

        search_box = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "txt_SearchText"))
        )
        search_box.clear()
        for char in query:
            search_box.send_keys(char)
            time.sleep(random.uniform(0.05, 0.12))
        search_box.send_keys(Keys.ESCAPE)
        time.sleep(0.3)

        search_btn = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "search-btn"))
        )
        driver.execute_script("arguments[0].click();", search_btn)
        time.sleep(random.uniform(3, 5))

        if resolved_sort != "相关度":
            module.apply_sort(driver, resolved_sort)

        for page_num in range(1, pages + 1):
            try:
                rows = WebDriverWait(driver, 15).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, '//table[@class="result-table-list"]//tbody//tr')
                    )
                )
                for row in rows:
                    paper = module.parse_paper_info(row)
                    if paper["title"]:
                        paper["page"] = page_num
                        all_papers.append(paper)
            except (TimeoutException, NoSuchElementException):
                pass

            if page_num < pages:
                try:
                    next_btn = driver.find_element(By.ID, "PageNext")
                    if next_btn.is_enabled():
                        driver.execute_script("arguments[0].click();", next_btn)
                        time.sleep(random.uniform(2, 3))
                    else:
                        break
                except (NoSuchElementException, WebDriverException):
                    break

        return {
            "query": query,
            "search_type": resolved_type,
            "sort": resolved_sort,
            "total_pages": pages,
            "total_papers": len(all_papers),
            "papers": all_papers,
        }
    except WebDriverException as e:
        return {"isError": True, "error": str(e), "error_type": "BrowserError", "papers": []}
    except Exception as e:
        return {"isError": True, "error": str(e), "error_type": "SearchError", "papers": []}


module._search_cnki_sync = patched_search_cnki_sync
mcp = module.mcp


def main():
    mcp.run()


if __name__ == "__main__":
    main()
