from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

def funcPowerDrivaer(driver_path, binary_path, url, action_func, filterObjectSite):
    #op = webdriver.ChromeOptions()
    op = Options()
    op.add_argument("headless")
    op.binary_location = binary_path
    
    service = Service(executable_path=driver_path)
    browser = webdriver.Chrome(service=service)
    #browser = webdriver.Chrome(service=service, options=op)
    
    try:
        browser.get(url)
        # Вызываем переданную логику и возвращаем результат 
        result = action_func(browser, filterObjectSite)
        return result
    finally:
        browser.quit()
def funcFindAndClickObjectSite(browser, tegSearch, tegClick, filter):
    # Поиск
    findSearch = browser.find_element(By.NAME, tegSearch)
    findSearch.send_keys(filter + "\n")    
    # Клик
    findClick = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, tegClick))
    )
    findClick.click()
    return browser, tegSearch, tegClick, filter
def funcFindObjectsSite(browser, teg, listTeg):
    # Сбор данных
    listTeg = browser.find_elements(By.CSS_SELECTOR, teg)
    return browser, teg, listTeg
def funcFindFilterClick2ObjectSite(browser, tegSearch1, tegSearch2, tegClick, filter1, filter2):
    # Поиск
    findSearch1 = browser.find_element(By.ID, tegSearch1)
    findSearch2 = browser.find_element(By.ID, tegSearch2)
    findSearch1.send_keys(filter1)    
    findSearch2.send_keys(filter2)
    # Клик
    findClick = browser.find_element(By.CSS_SELECTOR, tegClick)
    findClick.click()
    return browser, tegSearch1, tegSearch2, tegClick, filter1, filter2
def funcFindFilterClick1ObjectSite(browser, tegSearch, tegClick, filter):
    findSearch = browser.find_element(By.XPATH, tegSearch)
    #findInput.send_keys(os.path.expanduser("~") + "\\test2\\"+file)
    findSearch.send_keys(filter)
    findClick = browser.find_element(By.CSS_SELECTOR, tegClick)
    findClick.click()
    return browser, tegSearch, tegClick, filter
def funcClick1ObjectSite(browser, tegClick):
    findClick = browser.find_element(By.CSS_SELECTOR, tegClick)
    findClick.click()  
    return browser, tegClick
def funcClickAlert1ObjectSite(browser, tegClick):
    findClick = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, tegClick))
    )
    findClick.click()
    try:
        WebDriverWait(browser, 5).until(EC.alert_is_present())
        alert = browser.switch_to.alert
        alert.accept()
    except TimeoutException:
        print("... Alert did not appear, continuing.")
    return browser, tegClick
def funcFindObjectSite(browser, tegSearch, findSearch):
    soup = BeautifulSoup(browser.page_source, "html.parser")
    findSearch = soup.find_all(class_=tegSearch)
    return browser, tegSearch, findSearch