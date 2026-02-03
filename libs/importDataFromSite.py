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
    #findClick.click()
    browser.execute_script("arguments[0].click();", findClick)#https://www.google.com/search?q=%D0%95%D1%81%D1%82%D1%8C+%D0%BA%D1%83%D1%81%D0%BE%D0%BA+%D0%BA%D0%BE%D0%B4%D0%B0%3A%0A...%0Adef+funcParsingCes%28browser%2C+filterObjectSite%29%3A%0A++++listTegs%2C+symbol%2C+tegs+%3D+funcImportStrToList%28%5B%5D%2C+%22%2C+%22%2C+filterObjectSite%29%0A++++browser.maximize_window%28%29%0A++++browser%2C+tegUsername%2C+tegPasswd%2C+click%2C+username%2C+passwd+%3D+funcFindFilterClick2ObjectSite%28browser%2C+listTegs%5B0%5D%2C+listTegs%5B1%5D%2C+listTegs%5B2%5D%2C+CONFIG_DATA.get%28%22USERSITE2%22%29%2C+CONFIG_DATA.get%28%22PASSWDSITE2%22%29%29%0A++++WebDriverWait%28browser%2C+10%29.until%28EC.element_to_be_clickable%28%28By.CSS_SELECTOR%2C+listTegs%5B3%5D%29%29%29%0A++++browser%2C+tegBsslink+%3D+funcClick1ObjectSite%28browser%2C+listTegs%5B3%5D%29%0A++++browser%2C+tegTecnoklogylink+%3D+funcClick1ObjectSite%28browser%2C+listTegs%5B4%5D%29%0A++++browser%2C+tegImportlink+%3D+funcClickAlert1ObjectSite%28browser%2C+listTegs%5B5%5D%29%0A++++browser%2C+tegPublicationFile%2C+click%2C+filterFile+%3D+funcFindFilterClick1ObjectSite%28browser%2C+listTegs%5B6%5D%2C+listTegs%5B2%5D%2C+os.getcwd%28%29%2B%22%5C%5C%22%2Bfile%29%0A++++time.sleep%285%29%0A++++browser%2C+tegClass%2C+findHtmlMessage+%3D+funcFindObjectSite%28browser%2C+listTegs%5B7%5D%2C+%22%22%29%0A++++if+%28%22%D0%A4%D0%B0%D0%B9%D0%BB+%D0%B4%D0%BB%D1%8F+%D0%B8%D0%BC%D0%BF%D0%BE%D1%80%D1%82%D0%B0+%D0%B4%D0%BE%D0%BB%D0%B6%D0%B5%D0%BD+%D0%B1%D1%8B%D1%82%D1%8C%22+in+str%28findHtmlMessage%5B0%5D%29%29+or+%28%22%D0%A4%D0%B0%D0%B9%D0%BB+CSV+%D0%BD%D0%B5%D0%B2%D0%B5%D1%80%D0%BD%D0%BE%D0%B9+%D0%BA%D0%BE%D0%B4%D0%B8%D1%80%D0%BE%D0%B2%D0%BA%D0%B8%22+in+str%28findHtmlMessage%5B0%5D%29%29+or+%28%22%D0%9D%D0%B5%D0%B4%D0%BE%D0%BF%D1%83%D1%81%D1%82%D0%B8%D0%BC%D1%8B+%D1%80%D0%B0%D0%B7%D0%BD%D1%8B%D0%B5%22+in+str%28findHtmlMessage%5B0%5D%29%29%3A%0A++++++++print%28%22-+Attention%21+The+file+%22%2Bfile%2B%22+for+import+does+not+match.%22%29%0A++++if+%22%D0%98%D0%BC%D0%BF%D0%BE%D1%80%D1%82+%D0%B2%D1%8B%D0%BF%D0%BE%D0%BB%D0%BD%D0%B5%D0%BD%22+in+str%28findHtmlMessage%5B0%5D%29%3A%0A++++++++if+%22%D0%9A%D0%A0%D0%9E%D0%9C%D0%95%22+in+str%28findHtmlMessage%5B0%5D%29%3A%0A++++++++++++print%28%22-+Attention%21+The+import+%22%2Bfile%2B%22+is+complete%2C+but+partially.+Some+fields+are+already+filled+in.%22%29%0A++++++++else%3A%0A++++++++++++print%28%22%2B+Import+file+%22%2Bfile%2B%22+completed+successfully.%22%29%0A++++return%0A...%0Aif+checkTable%28df4gNok%29+%3D%3D+False%3A%0A++++dfDaily%2C+dbIp%2C+dbUser%2C+dbPasswd%2C+dbName%2C+dbTable%2C+dbCondition%2C+dbFilter+%3D+funcImportSqlToPandas%28%0A++++++++pd.DataFrame%28%29%2C+%0A++++++++CONFIG_DATA.get%28%22IPDB1%22%29%2C+%0A++++++++CONFIG_DATA.get%28%22USERDB1%22%29%2C+%0A++++++++CONFIG_DATA.get%28%22PASSWDB1%22%29%2C+%0A++++++++CONFIG_DATA.get%28%22DB2%22%29%2C+%0A++++++++CONFIG_DATA.get%28%22TABLE7%22%29%2C+%0A++++++++CONFIG_DATA.get%28%22CONDITION2%22%29%2C%0A++++++++CONFIG_DATA.get%28%22FILTER7%22%29%0A++++++++%29%0A++++dfOld+%3D+pd.merge%28df4gNok%2C+dfDaily%2C+left_on%3D%22BS_name%22%2C+right_on%3D%22BS_name%22%2C+how%3D%22inner%22%29++++%0A++++dfNameNewBs%2C+df4gNok%2C+dfOld%2C+listNameNewBs%2C+str4gNokCol%2C+strOldCol+%3D+funcGet1DfFrom2Lists%28%0A++++++++pd.DataFrame%28%29%2C+df4gNok%2C+dfOld%2C+listNameNewBs%2C%0A++++++++%22BS_name%22%2C+%22BS_name%22%0A++++%29%0A++++dfNew+%3D+pd.DataFrame%28%29%0A++++if+checkTable%28dfNameNewBs%29+%3D%3D+False%3A%0A++++++++dataNewSites+%3D+dict%28%29%0A++++++++numb%3D0%0A++++++++for+name+in+listNameNewBs%3A%0A++++++++++++if+name+in+listReady%3A%0A++++++++++++++++continue%0A++++++++++++else%3A%0A++++++++++++++++numb%3Dnumb%2B1%0A++++++++++++++++findUcn%2C+findLatitude%2C+findLongitude++%3D+funcPowerDrivaer%28%0A++++++++++++++++++++driver_path+%3D+CONFIG_DATA.get%28%22LINKPO1%22%29%2C%0A++++++++++++++++++++binary_path+%3D+CONFIG_DATA.get%28%22LINKPO2%22%29%2C%0A++++++++++++++++++++url+%3D+CONFIG_DATA.get%28%22LINKSITE1%22%29%2C%0A++++++++++++++++++++action_func+%3D+funcParsingRdb%2C%0A++++++++++++++++++++filterObjectSite+%3D+name%5B%3A2%5D+%2B+%2200%22%2B+name%5B2%3A6%5D%0A++++++++++++++++%29%0A++++++++++++++++findUcn%2C+listData%2C+symbol%2C+addSymbol1%2C+addSymbol2+%3D+funcDiffStringsAddList%28%0A++++++++++++++++++++findUcn%2C+listData%2C%0A++++++++++++++++++++%22%D0%A3%D0%A6%D0%9D%22%2C+%22%D0%A3%D0%A6%D0%9D%22%2C+%22-%22%0A++++++++++++++++%29%0A++++++++++++++++listData.append%28findLatitude.replace%28%27%2C%27%2C+%27.%27%29%29%0A++++++++++++++++listData.append%28findLongitude.replace%28%27%2C%27%2C+%27.%27%29%29+%0A++++++++++++++++listReady.append%28name%29%0A++++++++listData%2C+listReady%2C+dfRdb%2C+dataNewSites%2C+cols+%3D+funcImport2listsToDf%28%0A++++++++++++listData%2C+listReady%2C+pd.DataFrame%28%29%2C+dataNewSites%2C%0A++++++++++++%5B%22UCN%22%2C+%22latitudeX1%22%2C+%22longitudeY1%22%5D%0A++++++++%29%0A++++++++dfRdb%2C+fromCol%2C+toCol%2C+fromRenameSymbol%2C+toRenameSymbol%2C+numbCol+%3D+funcGetSuffRenameColDf%28%0A++++++++++++dfRdb%2C%0A++++++++++++%22index%22%2C+%22RegUcn%22%2C+%22IO%22%2C+%22IR%22%2C+2%0A++++++++%29%0A++++++++dfCoords%2C+dbIp%2C+dbUser%2C+dbPasswd%2C+dbName%2C+dbTable%2C+dbCondition%2C+dbFilter+%3D+funcImportSqlToPandas%28%0A++++++++++++pd.DataFrame%28%29%2C%0A++++++++++++CONFIG_DATA.get%28%22IPDB1%22%29%2C%0A++++++++++++CONFIG_DATA.get%28%22USERDB1%22%29%2C%0A++++++++++++CONFIG_DATA.get%28%22PASSWDB1%22%29%2C%0A++++++++++++CONFIG_DATA.get%28%22DB3%22%29%2C%0A++++++++++++CONFIG_DATA.get%28%22TABLE3%22%29%2C%0A++++++++++++CONFIG_DATA.get%28%22CONDITION3%22%29%2C%0A++++++++++++CONFIG_DATA.get%28%22FILTER3%22%29%0A++++++++%29%0A++++++++dfDaily+%3D+pd.merge%28dfDaily%2C+dfCoords%2C+left_on%3D%22BS_name%22%2C+right_on%3D%22BS_name%22%2C+how%3D%22inner%22%29%0A++++++++dfUcnTemplate+%3D+funcAddDfTemplateUcn%28pd.DataFrame%28%29%29%0A++++++++dfNoUcn+%3D+pd.DataFrame%28%29%0A++++++++dfNoUcn+%3D+pd.concat%28%5BdfRdb%2C+dfNoUcn%5D%29%0A++++++++dfNoUcn+%3D+dfNoUcn%5BdfNoUcn%5B%22UCN%22%5D.isin%28%5B%22-%22%5D%29%5D%0A++++++++if+checkTable%28dfNoUcn%29+%3D%3D+False%3A%0A++++++++++++dfNeighbour%2C+dfNoUcn%2C+df4gNok%2C+dfDaily%2C+strNoUcn%2C+str4gNok+%3D+funcJoin3df%28%0A++++++++++++++++pd.DataFrame%28%29%2C+dfNoUcn%2C+df4gNok%2C+dfDaily%2C%0A++++++++++++++++%22index%22%2C+%22BS_name%22%0A++++++++++++%29%0A++++++++++++dfNoUcn+%3D+funcFindNeighbour%28dfNeighbour%29%0A++++++++++++dfNoUcn+%3D+funcCorrectCols4gNok%28dfNoUcn%29%0A++++++++++++dfNew+%3D+pd.concat%28%5BdfNew%2C+dfNoUcn%5D%29%0A++++++++dfUcn+%3D+pd.DataFrame%28%29%0A++++++++dfUcn+%3D+pd.concat%28%5BdfRdb%2C+dfUcn%5D%29%0A++++++++dfUcn+%3D+dfUcn%5BdfUcn%5B%22UCN%22%5D.isin%28%5B%22%D0%A3%D0%A6%D0%9D%22%5D%29%5D%0A++++++++if+checkTable%28dfUcn%29+%3D%3D+False%3A%0A++++++++++++dfUcn%2C+df4gNok%2C+dfUcnTemplate%2C+strUcn1%2C+strUcn2%2C+str4gNok%2C+strUcnTemplate++%3D+funcJoin2Df2%28%0A++++++++++++++++dfUcn%2C+df4gNok%2C+dfUcnTemplate%2C%0A++++++++++++++++%22index%22%2C+%22RegUcn%22%2C+%22BS_name%22%2C+%22RegUcn%22%0A++++++++++++%29%0A++++++++++++dfUcn+%3D+funcCorrectCols4gNok%28dfUcn%29%0A++++++++++++dfNew+%3D+pd.concat%28%5BdfNew%2C+dfUcn%5D%29%0A++++dfOld+%3D+funcCorrectCols4gNok%28dfOld%29%0A++++df4gNok%2C+dfOld%2C+dfNew+%3D+funcJoin2Df%28pd.DataFrame%28%29%2C+dfOld%2C+dfNew%29%0A++++df4gNok.to_csv%28%22df4gNok.csv%22%2C+sep%3D%22%3B%22%2C+index%3DFalse%2C+header%3DFalse%2C+encoding%3D%22UTF-8-SIG%22%29%0A++++listFiles+%3D+os.listdir%28%29%0A++++for+file+in+listFiles%3A%0A++++++++if+%22df4gNok.%22+in+file%3A%0A++++++++++++dataFromSite++%3D+funcPowerDrivaer%28%0A++++++++++++++++driver_path+%3D+CONFIG_DATA.get%28%22LINKPO1%22%29%2C%0A++++++++++++++++binary_path+%3D+CONFIG_DATA.get%28%22LINKPO2%22%29%2C%0A++++++++++++++++url+%3D+CONFIG_DATA.get%28%22LINKSITE2%22%29%2C%0A++++++++++++++++action_func+%3D+funcParsingCes%2C%0A++++++++++++++++%23filterObjectSite+%3D+%22%22%0A++++++++++++++++filterObjectSite+%3D+CONFIG_DATA.get%28%22TEGSSITE3%22%29%0A++++++++++++%29%0A++++++++++++print%28%22%2B+Add+Data+%28df4gNok%29+to+site+CES%22%29%0A...%0A%D0%BF%D0%BE%D1%81%D0%BB%D0%B5+%D0%BA%D0%BE%D1%82%D0%BE%D1%80%D0%BE%D0%B3%D0%BE+%D0%BF%D0%BE%D1%8F%D0%B2%D0%BB%D1%8F%D0%B5%D1%82%D1%81%D1%8F+%D1%81%D0%BB%D0%B5%D0%B4%D1%83%D1%8E%D1%89%D0%B0%D1%8F+%D0%BE%D1%88%D0%B8%D0%B1%D0%BA%D0%B0%2C+%D0%BA%D0%BE%D0%B3%D0%B4%D0%B0+%D1%8F+%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D0%BA%D0%B0%D1%8E+%D1%87%D0%B5%D1%80%D0%B5%D0%B7+%D0%BF%D0%BB%D0%B0%D0%BD%D0%B8%D1%80%D0%BE%D0%B2%D1%89%D0%B8%D0%BA+%D0%B7%D0%B0%D0%B4%D0%B0%D1%87+%D0%B2+Windows%3A%0ATraceback+%28most+recent+call+last%29%3A%0A++File+%22C%3A%5CUsers%5Cd%5CparserWeb%5Cmain.py%22%2C+line+749%2C+in+%3Cmodule%3E%0A++++dataFromSite++%3D+funcPowerDrivaer%28%0A++File+%22C%3A%5CUsers%5Cd%5CparserWeb%5Clibs%5CimportDataFromSite.py%22%2C+line+23%2C+in+funcPowerDrivaer%0A++++result+%3D+action_func%28browser%2C+filterObjectSite%29%0A++File+%22C%3A%5CUsers%5Cd%5CparserWeb%5Cmain.py%22%2C+line+74%2C+in+funcParsingCes%0A++++browser%2C+tegImportlink+%3D+funcClickAlert1ObjectSite%28browser%2C+listTegs%5B5%5D%29%0A++File+%22C%3A%5CUsers%5Cd%5CparserWeb%5Clibs%5CimportDataFromSite.py%22%2C+line+66%2C+in+funcClickAlert1Obj%0AectSite%0A++++findClick.click%28%29%0A++File+%22C%3A%5CUsers%5Cd%5CenvParserWeb%5Clib%5Csite-packages%5Cselenium%5Cwebdriver%5Cremote%5Cwebelement.p%0Ay%22%2C+line+119%2C+in+click%0A++++self._execute%28Command.CLICK_ELEMENT%29%0A++File+%22C%3A%5CUsers%5Cd%5CenvParserWeb%5Clib%5Csite-packages%5Cselenium%5Cwebdriver%5Cremote%5Cwebelement.p%0Ay%22%2C+line+572%2C+in+_execute%0A++++return+self._parent.execute%28command%2C+params%29%0A++File+%22C%3A%5CUsers%5Cd%5CenvParserWeb%5Clib%5Csite-packages%5Cselenium%5Cwebdriver%5Cremote%5Cwebdriver.py%0A%22%2C+line+458%2C+in+execute%0A++++self.error_handler.check_response%28response%29%0A++File+%22C%3A%5CUsers%5Cd%5CenvParserWeb%5Clib%5Csite-packages%5Cselenium%5Cwebdriver%5Cremote%5Cerrorhandler%0A.py%22%2C+line+233%2C+in+check_response%0A++++raise+exception_class%28message%2C+screen%2C+stacktrace%29%0Aselenium.common.exceptions.ElementClickInterceptedException%3A+Message%3A+element+click+intercepted%3A+Ele%0Ament+%3Ca+class%3D%22btn+btn-primary%22+href%3D%22%2FCreateSite_web%2Fimport_nokia_4g%2Findex_bss.php%22%3E...%3C%2Fa%3E+is+not%0Aclickable+at+point+%28348%2C+314%29.+Other+element+would+receive+the+click%3A+%3Cth+class%3D%22sorting%22+tabindex%3D%22%0A0%22+aria-controls%3D%22user_data%22+rowspan%3D%221%22+colspan%3D%221%22+style%3D%22width%3A+121px%3B%22+aria-label%3D%22...%3A+activate%0A+to+sort+column+ascending%22%3EDate%3C%2Fth%3E%0A++%28Session+info%3A+chrome%3D142.0.7444.1289%29%3B+For+documentation+on+this+error%2C+please+visit%3A+https%3A%2F%2Fwww%0A.selenium.dev%2Fdocumentation%2Fwebdriver%2Ftroubleshooting%2Ferrors%23elementclickinterceptedexception%0AStacktrace%3A%0ASymbols+not+available.+Dumping+unresolved+backtrace%3A%0A++++++++0x7ff6c6b6dfb5%0A++++++++0x7ff6c6aad970%0A++++++++0x7ff6c68f2b6d%0A++++++++0x7ff6c6953409%0A++++++++0x7ff6c6950dbb%0A++++++++0x7ff6c694dce1%0A++++++++0x7ff6c694cba0%0A++++++++0x7ff6c693e3d8%0A++++++++0x7ff6c69762fa%0A++++++++0x7ff6%0A%D0%A1%D0%BA%D1%80%D0%B8%D0%BF%D1%82+%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D0%B0%D0%B5%D1%82+%D0%B5%D1%81%D0%BB%D0%B8+%D0%B7%D0%B0%D0%BF%D1%83%D1%81%D1%82%D0%B8%D1%82%D1%8C+%D1%87%D0%B5%D1%80%D0%B5%D0%B7+%D1%82%D0%B5%D1%80%D0%BC%D0%B8%D0%BD%D0%B0%D0%BB+shell%2C+%D0%B8%D0%BB%D0%B8+%D0%BF%D1%80%D0%BE%D1%81%D1%82%D0%BE+python.&rlz=1C1GCEB_enRU1113RU1113&sourceid=chrome&ie=UTF-8&udm=50&aep=48&cud=0&qsubts=1770011076765&source=chrome.crn.obic&mstk=AUtExfDiCo3j-220Q5BbImPu6f2ib1SGk2ke0cXQelD1VrLbNSpbUgVoQU9sio-ICTjXYQQF9qHK_c5LgMM3Av-cOq67MH3Rx0_8yZ4CqR3eqnUuLEWOWk388fjMBU42v9HW39tEMmLTw6g4BZumeI1-MBqUlpflhbN1tQI&csuir=1
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