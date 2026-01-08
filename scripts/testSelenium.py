from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
import time
from bs4 import BeautifulSoup

# --- Configuration ---
# Path to the downloaded YandexDriver executable
YANDEX_DRIVER_PATH = r'C:\\Users\...\parserWeb\yandexdriver.exe' # Use 'r' prefix for raw string in Windows paths
# Path to the Yandex browser binary
YANDEX_BROWSER_BINARY_PATH = r'C:\\Program Files\Yandex\YandexBrowser\Application\browser.exe' 
# ---------------------

# Set up the Service object for the YandexDriver
service = Service(executable_path=YANDEX_DRIVER_PATH)

# Set up ChromeOptions and specify the Yandex browser binary location
op = webdriver.ChromeOptions()
op.add_argument('headless')
op.binary_location = YANDEX_BROWSER_BINARY_PATH

# Initialize the WebDriver
# Yandex browser is a Chromium-based browser, so we use webdriver.Chrome
#browser = webdriver.Chrome(service=service, options=op)
browser = webdriver.Chrome(service=service)

try:
    # Open a website
    #browser.get('https://...ru/p/list.aspx?op=list&k=c3a5t1r&v=c3a5ts5c1cs9r133')
    browser.get('http://.../CreateSite_web/login.php')
    print(f"Page title: {browser.title}")
    browser.maximize_window()
    soup = BeautifulSoup(browser.page_source, "html.parser")
    findUsername = browser.find_element(By.ID, "username")
    findPasswd = browser.find_element(By.ID, "password")
    findLogin = browser.find_element(By.CSS_SELECTOR, '.btn-primary')
    findUsername.send_keys("dGabunia")
    findPasswd.send_keys("BsKth68s")
    findLogin.click()
    print("... loading1")
    time.sleep(5)
    findBsslink = browser.find_element(By.CSS_SELECTOR, 'a[href="BSS_nokia_table.php"]')
    findBsslink.click()
    print("... loading2")
    time.sleep(5)
    findTecnoklogylink = browser.find_element(By.CSS_SELECTOR, 'a[href="tables_nokia_2g/table_nokia_bss_2g/index.php"]')
    findTecnoklogylink.click()
    print("... loading3")
    time.sleep(5) 
    findImportlink = browser.find_element(By.CSS_SELECTOR, 'a[href="/CreateSite_web/import_nokia_2g/index_bss.php"]')
    findImportlink.click()
    print("... loading4")
    time.sleep(5)
    alert = browser.switch_to.alert
    alert.accept()
    print("... loading5")
    time.sleep(5)
finally:
    # Close the browser
    browser.quit()
