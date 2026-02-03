import pandas as pd
import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time
from bs4 import BeautifulSoup
import os
import numpy
from datetime import datetime

# Функции:
def hiddenData(ipN, ipE, userC, passwdC, userD, passwdD, db1, db2, db3):
    findHiddenFiles =  os.listdir()
    for file in findHiddenFiles:
        if "config.txt" in str(file):
            hiddenFile = open('config.txt', 'r')
            data=[]
            for line in hiddenFile:
                resultLine = line.split()
                for findSymbol in resultLine:
                    if(findSymbol.startswith("'") and findSymbol.endswith("'")):
                        findSymbol=findSymbol.replace("'","")
                        data.append(findSymbol)
            ipN = data[0]
            ipE = data[1]
            userC = data[2]
            passwdC = data[3]
            userD = data[4]
            passwdD = data[5]
            db1 = data[6]
            db2 = data[7]
            db3 = data[8]
            hiddenFile.close()
    return ipN, ipE, userC, passwdC, userD, passwdD, db1, db2, db3
def checkTable(check):
    return check.empty
def findNewSites(nameBs, cesData):
    cesList = cesData['BS_name'].tolist()
    cesList = list(dict.fromkeys(cesList))
    oldList = oldBsTable['BS_name'].tolist()
    oldList = list(dict.fromkeys(oldList))
    for name in cesList:
        if name in oldList:
            continue
        else:
            newList.append(name)
    nameBs = pd.DataFrame(newList, columns=["nameNew"])
    return nameBs, cesData
def parsingRdb(rdbData):
    dataNewSites = dict()
    numb=0
    for name in newList:
        if name in readyList:
            continue
        else:
            print("... The site is being read:")
            numb=numb+1
            print(str(numb)+". "+name)
            with open("outPyScript.log", "a") as outfile:
                outfile.write("... The site is being read.\n")
            bsfull = name[:2] + "00"+ name[2:6]
            op = webdriver.ChromeOptions()
            op.add_argument('headless')
            print("... Loading")
            service = Service(executable_path=r'C:\\Users\david.gabunia\parserWeb\yandexdriver.exe')
            op.binary_location =  r'C:\\Program Files\Yandex\YandexBrowser\Application\browser.exe'
            #browser = webdriver.Chrome(options=op)
            browser = webdriver.Chrome(service=service, options=op)
            print("... Loading")
            browser.get('https://rdb.t2.ru/p/list.aspx?op=list&k=c3a5t1r&v=c3a5ts5c1cs9r133')
            #print(f"Page title: {browser.title}")
            open_search = browser.find_element(By.NAME, "p$body$ListSearch$listSearchBox")
            open_search.send_keys(bsfull +'\n')
            soup = BeautifulSoup(browser.page_source, "html.parser")
            candidate = soup.find_all(class_='fieldType-eString')
            linkCandidate = candidate[9].find('a')
            try: 
                browser.get(linkCandidate['href'])
            except TypeError:
                print("- No site candidate in RDB "+name)
                with open("outPyScript.log", "a") as outfile:
                    outfile.write("- No site candidate in RDB "+name+"\n")
                break
            soup = BeautifulSoup(browser.page_source, "html.parser")
            td = soup.find_all("td")
            time.sleep(10)
            step = 0
            for i in td:
                step = step + 1
                if (step == 40) and ("WGS широта" in str(td[38])):
                    if "УЦН" in str(td[6]):
                        ucn = "УЦН"
                        dataList.append(ucn)
                    else:
                        ucn = "-"
                        dataList.append(ucn)
                    latitude = td[39].text
                    latitude = latitude.replace(',', '.')
                    longitude = td[44].text
                    longitude = longitude.replace(',', '.')
                    dataList.append(latitude)
                    dataList.append(longitude)
                else:
                    continue
            browser.quit()
            readyList.append(name)
    print(dataList)
    print(readyList)
    remainder = (len(dataList)//len(readyList))
    for numeration in range(len(readyList)):
        dataNewSites[readyList[numeration]] = [dataList[y] for y in range(remainder*numeration,remainder*numeration+remainder)]
    cols = ["UCN", "latitudeX1", "longitudeY1"]
    rdbData = pd.DataFrame.from_dict(dataNewSites, orient='index', columns=cols)
    rdbData = rdbData.reset_index()
    copycol=rdbData["index"]
    rdbData.insert(1, "subIndex", copycol)
    rdbData["subIndex"] = rdbData["subIndex"].str.replace("^IO", "IR", regex=True)
    copycol=rdbData["subIndex"]
    rdbData.insert(1, "RegUcn", copycol)
    rdbData["RegUcn"] = rdbData["RegUcn"].str[:2]
    return rdbData
def templateUcn(ucnData):
    ucnLacDict = {"BU":10340, "VV":52412, "IR":5370, "BI":40004, "HB":32106, "ZB":53711, "AM":54500, "YA":57641, "KM":37406, "MD":38718, "SA":38005, "AN":40701}
    ucnBscDict = {"IR":"IRK484", "HB":"KHB173", "YA":"NSK042", "AM":"PRM140", "BI":"BIR067", "ZB":"PRM140", "KM":"KAM070", "VV":"", "BU":""}
    ucnRacDict = {5370:228, 37406:228, 38718:228, 38005:228, 40004:228, 32106:116, 40701:228, 57641:228}
    ucnLacTable = pd.DataFrame(list(ucnLacDict.items()), columns=['RegUcn', 'LacUcn'])
    ucnBscTable = pd.DataFrame(list(ucnBscDict.items()), columns=['RegUcn', 'BscUcn'])
    ucnRacTable = pd.DataFrame(list(ucnRacDict.items()), columns=['LacUcn', 'RacUcn'])
    ucnLBTable = pd.merge(ucnLacTable, ucnBscTable, left_on='RegUcn', right_on='RegUcn', how='outer')
    ucnData = pd.merge(ucnLBTable, ucnRacTable, left_on='LacUcn', right_on='LacUcn', how='outer') 
    print("- Attention! It is necessary to check LAC, BSC, RAC. Not all data is filled in")
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information for BS UCN.\n- Attention! It is necessary to check LAC, BSC, RAC. Not all data is filled in\n")
    return ucnData
def templateUcnBul(ucnData):
    ucnLacDict = {"BU":10351, "VV":52421, "IR":5381, "BI":40011, "HB":32112, "ZB":53714, "AM":54503, "YA":57644}
    ucnBscDict = {"IR":"BSCB-IRK525-1", "HB":"BSCB-KHB576-1", "YA":"BSCB-YAK558-1", "AM":"BSCB-BLG514-1", "BI":"BSCB-BIR522-1", "ZB":"BSCB-CHI523-1", "VV":"BSCB-VLD547-1", "BU":"BSCB-BRT551-1"}
    ucnRacDict = {54503:14, 40011:54, 53714:23, 5381:54, 52421:47, 10351:51, 57644:54, 32112:54}
    ucnLacTable = pd.DataFrame(list(ucnLacDict.items()), columns=['RegUcn', 'LacUcn'])
    ucnBscTable = pd.DataFrame(list(ucnBscDict.items()), columns=['RegUcn', 'BscUcn'])
    ucnRacTable = pd.DataFrame(list(ucnRacDict.items()), columns=['LacUcn', 'RacUcn'])
    ucnLBTable = pd.merge(ucnLacTable, ucnBscTable, left_on='RegUcn', right_on='RegUcn', how='outer')
    ucnData = pd.merge(ucnLBTable, ucnRacTable, left_on='LacUcn', right_on='LacUcn', how='outer') 
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information for BS Bulat UCN.\n")
    return ucnData
def findNeighbourTable(nbData):
    x1=nbData["latitudeX1"].astype(float)
    x2=nbData["latitudeX2"].astype(float)
    y1=nbData["longitudeY1"].astype(float)
    y2=nbData["longitudeY2"].astype(float)        
    nbData["distance"] = ""
    nbData["distance"] = numpy.sqrt((x1-x2) * (x1-x2) + (y1-y2) * (y1-y2))
    groupedData = nbData.groupby("index")
    minDistance = groupedData["distance"].min()
    minDistanceTable = minDistance.reset_index()
    #print(minDistanceTable)
    #print(nbData)
    nbData = pd.merge(minDistanceTable, nbData, left_on='distance', right_on='distance', how='inner')
    print("- Attention! It is necessary to check the coordinates of neighboring base stations.")
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Find Neightbour between Old BS and New BS.\n- Attention! It is necessary to check the coordinates of neighboring base stations\n")
    #print(nbData)
    return nbData
def addResultFile(readyData):
    current_datetime = datetime.now().strftime("%Y_%m_%d_%H_%M_%S%z")
    nameLogBS="out_"+str(current_datetime)+"_NewBs.log"
    with open(nameLogBS, "a") as outfile:
        outfile.write(str(current_datetime) +" Added information about the following base stations:\n")
    for nameBS in readyData:
        with open(nameLogBS, "a") as outfile:
            outfile.write(nameBS+"\n")
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information on new sites.\n")
    return readyData
def writeResults(resData, oldData, newData):
    if checkTable(oldData) == False:
        resData = pd.concat([resData, oldData])
    if checkTable(newData) == False:
        if checkTable(oldData) == False or checkTable(oldData) == True:
            resData = pd.concat([resData, newData])
    return resData, oldData, newData
def importCes(files):
    #17
    #home_directory = os.path.expanduser("~")
    files = os.listdir()
    for file in files:
        if "resNok2g." in file or "resNok2gBul." in file:
            print(file)
            print("... Ready to import data 2G Nokia/Bulat from "+file+" file to CES website")
            with open("outPyScript.log", "a") as outfile:
                outfile.write("... Ready to import data 2G Nokia/Bulat from "+file+" file to CES website\n")

            op = webdriver.ChromeOptions()            
            op.binary_location =  r'C:\\Program Files\Yandex\YandexBrowser\Application\browser.exe'
            op.add_argument('headless')
            service = Service(executable_path=r'C:\\Users\david.gabunia\parserWeb\yandexdriver.exe')
            #browser = webdriver.Chrome()
            browser = webdriver.Chrome(service=service)            
            browser.get('http://'+ipNokia+'/CreateSite_web/login.php')

            browser.maximize_window()
            soup = BeautifulSoup(browser.page_source, "html.parser")
            findUsername = browser.find_element(By.ID, "username")
            findPasswd = browser.find_element(By.ID, "password")
            findLogin = browser.find_element(By.CSS_SELECTOR, '.btn-primary')
            findUsername.send_keys(userCes)
            findPasswd.send_keys(passwdCes)
            findLogin.click()

            WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="BSS_nokia_table.php"]')))
            findBsslink = browser.find_element(By.CSS_SELECTOR, 'a[href="BSS_nokia_table.php"]')
            findBsslink.click()
            #time.sleep(5)

            findTecnoklogylink = browser.find_element(By.CSS_SELECTOR, 'a[href="tables_nokia_2g/table_nokia_bss_2g/index.php"]')
            findTecnoklogylink.click()

            findImportlink = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/CreateSite_web/import_nokia_2g/index_bss.php"]'))
            )
            findImportlink.click()
            try:
                WebDriverWait(browser, 5).until(EC.alert_is_present())
                alert = browser.switch_to.alert
                alert.accept()
            except TimeoutException:
                print("... Alert did not appear, continuing.")

            findInput = browser.find_element(By.XPATH, "//input[@type='file']")
            findSubmit = browser.find_element(By.CSS_SELECTOR, '.btn-primary')
            findInput.send_keys(os.path.expanduser("~") + "\\parserWeb\\"+file)
            findSubmit.click()
            time.sleep(5)
            soup = BeautifulSoup(browser.page_source, "html.parser")
            findHtmlMessage = soup.find_all(class_='jumbotron')
            if ("Файл для импорта должен быть" in str(findHtmlMessage[0])) or ("Файл CSV неверной кодировки" in str(findHtmlMessage[0])) or ("Недопустимы разные" in str(findHtmlMessage[0])):
                with open("outPyScript.log", "a") as outfile:
                    outfile.write("- Attention! The file "+file+" for import does not match.\n")
            if "Импорт выполнен" in str(findHtmlMessage[0]):
                if "КРОМЕ" in str(findHtmlMessage[0]):
                    with open("outPyScript.log", "a") as outfile:
                        outfile.write("- Attention! The import "+file+" is complete, but partially. Some fields are already filled in.\n")
                else:
                    with open("outPyScript.log", "a") as outfile:
                        outfile.write("+ Import file "+file+" completed successfully.\n")
            browser.quit()
        elif "resNok3g" in file:
            print(file)
            print("... Ready to import data 3G Nokia from "+file+" file to CES website")
            with open("outPyScript.log", "a") as outfile:
                outfile.write("... Ready to import data 3G Nokia from "+file+" file to CES website\n")    
            op = webdriver.ChromeOptions()
            
            op.binary_location =  r'C:\\Program Files\Yandex\YandexBrowser\Application\browser.exe'
            op.add_argument('headless')
            service = Service(executable_path=r'C:\\Users\david.gabunia\parserWeb\yandexdriver.exe')
            #browser = webdriver.Chrome()
            browser = webdriver.Chrome(service=service)    
            
            browser.get('http://'+ipNokia+'/CreateSite_web/login.php')
            browser.maximize_window()
            soup = BeautifulSoup(browser.page_source, "html.parser")
            findUsername = browser.find_element(By.ID, "username")
            findPasswd = browser.find_element(By.ID, "password")
            findLogin = browser.find_element(By.CSS_SELECTOR, '.btn-primary')
            findUsername.send_keys(userCes)
            findPasswd.send_keys(passwdCes)
            findLogin.click()

            WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="BSS_nokia_table.php"]')))
            findBsslink = browser.find_element(By.CSS_SELECTOR, 'a[href="BSS_nokia_table.php"]')
            findBsslink.click()
            #time.sleep(5)

            findTecnoklogylink = browser.find_element(By.CSS_SELECTOR, 'a[href="tables_nokia_3g/table_nokia_bss_3g/index.php"]')
            findTecnoklogylink.click()

            findImportlink = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="/CreateSite_web/import_nokia_3g/index_bss.php"]'))
            )
            #findImportlink.click()
            browser.execute_script("arguments[0].click();",findImportlink)
            try:
                WebDriverWait(browser, 5).until(EC.alert_is_present())
                alert = browser.switch_to.alert
                alert.accept()
            except TimeoutException:
                print("... Alert did not appear, continuing.")
                
            findInput = browser.find_element(By.XPATH, "//input[@type='file']")
            findSubmit = browser.find_element(By.CSS_SELECTOR, '.btn-primary')
            findInput.send_keys(os.path.expanduser("~") + "\\parserWeb\\"+file)
            findSubmit.click()
            time.sleep(5)
            soup = BeautifulSoup(browser.page_source, "html.parser")
            findHtmlMessage = soup.find_all(class_='jumbotron')
            if ("Файл для импорта должен быть" in str(findHtmlMessage[0])) or ("Файл CSV неверной кодировки" in str(findHtmlMessage[0])) or ("Недопустимы разные" in str(findHtmlMessage[0])):
                with open("outPyScript.log", "a") as outfile:
                    outfile.write("- Attention! The file "+file+" for import does not match.\n")
            if "Импорт выполнен" in str(findHtmlMessage[0]):
                if "КРОМЕ" in str(findHtmlMessage[0]):
                    with open("outPyScript.log", "a") as outfile:
                        outfile.write("- Attention! The import "+file+" is complete, but partially. Some fields are already filled in.\n")
                else:
                    with open("outPyScript.log", "a") as outfile:
                        outfile.write("+ Import file "+file+" completed successfully.\n")
            browser.quit()
        elif "resNok4g." in file or "resNok4gBul." in file:
            print(file)
            print("... Ready to import data 4G Nokia/Bulat from "+file+" file to CES website")
            with open("outPyScript.log", "a") as outfile:
                outfile.write("... Ready to import data 4G Nokia/Bulat from "+file+" file to CES website\n")    
            op = webdriver.ChromeOptions()
            
            op.binary_location =  r'C:\\Program Files\Yandex\YandexBrowser\Application\browser.exe'
            op.add_argument('headless')
            service = Service(executable_path=r'C:\\Users\david.gabunia\parserWeb\yandexdriver.exe')
            #browser = webdriver.Chrome()
            browser = webdriver.Chrome(service=service)  
            
            browser.get('http://'+ipNokia+'/CreateSite_web/login.php')
            browser.maximize_window()
            soup = BeautifulSoup(browser.page_source, "html.parser")
            findUsername = browser.find_element(By.ID, "username")
            findPasswd = browser.find_element(By.ID, "password")
            findLogin = browser.find_element(By.CSS_SELECTOR, '.btn-primary')
            findUsername.send_keys(userCes)
            findPasswd.send_keys(passwdCes)
            findLogin.click()

            WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="BSS_nokia_table.php"]')))
            findBsslink = browser.find_element(By.CSS_SELECTOR, 'a[href="BSS_nokia_table.php"]')
            findBsslink.click()
            time.sleep(5)

            findTecnoklogylink = browser.find_element(By.CSS_SELECTOR, 'a[href="tables_nokia_4g/table_nokia_bss_4g/index.php"]')
            findTecnoklogylink.click()

            findImportlink = WebDriverWait(browser, 10).until(
                #EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/CreateSite_web/import_nokia_4g/index_bss.php"]'))
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="/CreateSite_web/import_nokia_4g/index_bss.php"]'))
            )
            #findImportlink.click()
            browser.execute_script("arguments[0].click();",findImportlink)
            try:
                WebDriverWait(browser, 5).until(EC.alert_is_present())
                alert = browser.switch_to.alert
                alert.accept()
            except TimeoutException:
                print("... Alert did not appear, continuing.")
            
            findInput = browser.find_element(By.XPATH, "//input[@type='file']")
            findSubmit = browser.find_element(By.CSS_SELECTOR, '.btn-primary')
            findInput.send_keys(os.path.expanduser("~") + "\\parserWeb\\"+file)
            findSubmit.click()
            time.sleep(5)
            soup = BeautifulSoup(browser.page_source, "html.parser")
            findHtmlMessage = soup.find_all(class_='jumbotron')
            if ("Файл для импорта должен быть" in str(findHtmlMessage[0])) or ("Файл CSV неверной кодировки" in str(findHtmlMessage[0])) or ("Недопустимы разные" in str(findHtmlMessage[0])):
                with open("outPyScript.log", "a") as outfile:
                    outfile.write("- Attention! The file "+file+" for import does not match.\n")
            if "Импорт выполнен" in str(findHtmlMessage[0]):
                if "КРОМЕ" in str(findHtmlMessage[0]):
                    with open("outPyScript.log", "a") as outfile:
                        outfile.write("- Attention! The import "+file+" is complete, but partially. Some fields are already filled in.\n")
                else:
                    with open("outPyScript.log", "a") as outfile:
                        outfile.write("+ Import file "+file+" completed successfully.\n")
            browser.quit()
        elif "resEr2g." in file or "resEr2gBul." in file or "resEr2gBulNeop." in file:
            print(file)
            print("... Ready to import data 2G Ericsson/Bulat from "+file+" file to CES website")
            with open("outPyScript.log", "a") as outfile:
                outfile.write("... Ready to import data 2G Ericsson/Bulat from "+file+" file to CES website\n")
            op = webdriver.ChromeOptions()
            op.add_argument('headless')
            print("... loading")                        
            op.binary_location =  r'C:\\Program Files\Yandex\YandexBrowser\Application\browser.exe'
            service = Service(executable_path=r'C:\\Users\david.gabunia\parserWeb\yandexdriver.exe')
            #browser = webdriver.Chrome(options=op)
            browser = webdriver.Chrome(service=service, options=op)            
            browser.get('http://'+ipEricsson+'/CreateSite_web/login.php')            
            soup = BeautifulSoup(browser.page_source, "html.parser")
            findUsername = browser.find_element(By.ID, "username")
            findPasswd = browser.find_element(By.ID, "password")
            findLogin = browser.find_element(By.CSS_SELECTOR, '.btn-primary')
            findUsername.send_keys(userCes)
            findPasswd.send_keys(passwdCes)
            findLogin.click()
            print("... loading")
            time.sleep(5)
            browser.get('http://'+ipEricsson+'/CreateSite_web/import_ericsson_2g/index_bss.php')
            findInput = browser.find_element(By.XPATH, "//input[@type='file']")
            findInput.send_keys(os.path.expanduser("~") + "\\parserWeb\\"+file)
            time.sleep(5)
            findSubmit = browser.find_element(By.CSS_SELECTOR, '.btn-primary')
            findSubmit.click()
            time.sleep(5)
            soup = BeautifulSoup(browser.page_source, "html.parser")
            findHtmlMessage = soup.find_all(class_='jumbotron')
            if ("Файл для импорта должен быть" in str(findHtmlMessage[0])) or ("Файл CSV неверной кодировки" in str(findHtmlMessage[0])) or ("Недопустимы разные" in str(findHtmlMessage[0])):
                with open("outPyScript.log", "a") as outfile:
                    outfile.write("- Attention! The file "+file+" for import does not match.\n")
            if "Импорт выполнен" in str(findHtmlMessage[0]):
                if "КРОМЕ" in str(findHtmlMessage[0]):
                    with open("outPyScript.log", "a") as outfile:
                        outfile.write("- Attention! The import "+file+" is complete, but partially. Some fields are already filled in.\n")
                else:
                    with open("outPyScript.log", "a") as outfile:
                        outfile.write("+ Import file "+file+" completed successfully.\n")
            browser.quit()
        elif "resEr3g" in file:
            print(file)
            print("... Ready to import data 3G Ericsson from "+file+" file to CES website")
            with open("outPyScript.log", "a") as outfile:
                outfile.write("... Ready to import data 3G Ericsson from "+file+" file to CES website\n")
            op = webdriver.ChromeOptions()
            op.add_argument('headless')
            print("... loading")
            op.binary_location =  r'C:\\Program Files\Yandex\YandexBrowser\Application\browser.exe'
            service = Service(executable_path=r'C:\\Users\david.gabunia\parserWeb\yandexdriver.exe')
            #browser = webdriver.Chrome(options=op)
            browser = webdriver.Chrome(service=service, options=op)
            browser.get('http://'+ipEricsson+'/CreateSite_web/login.php')
            #browser.maximize_window()
            soup = BeautifulSoup(browser.page_source, "html.parser")
            findUsername = browser.find_element(By.ID, "username")
            findPasswd = browser.find_element(By.ID, "password")
            findLogin = browser.find_element(By.CSS_SELECTOR, '.btn-primary')
            findUsername.send_keys(userCes)
            findPasswd.send_keys(passwdCes)
            findLogin.click()
            print("... loading")
            time.sleep(5)
            browser.get('http://'+ipEricsson+'/CreateSite_web/import_ericsson_3g/index_bss.php')
            findInput = browser.find_element(By.XPATH, "//input[@type='file']")
            findInput.send_keys(os.path.expanduser("~") + "\\parserWeb\\"+file)
            time.sleep(5)
            findSubmit = browser.find_element(By.CSS_SELECTOR, '.btn-primary')
            findSubmit.click()
            time.sleep(5)
            soup = BeautifulSoup(browser.page_source, "html.parser")
            findHtmlMessage = soup.find_all(class_='jumbotron')
            if ("Файл для импорта должен быть" in str(findHtmlMessage[0])) or ("Файл CSV неверной кодировки" in str(findHtmlMessage[0])) or ("Недопустимы разные" in str(findHtmlMessage[0])):
                with open("outPyScript.log", "a") as outfile:
                    outfile.write("- Attention! The file "+file+" for import does not match.\n")
            if "Импорт выполнен" in str(findHtmlMessage[0]):
                if "КРОМЕ" in str(findHtmlMessage[0]):
                    with open("outPyScript.log", "a") as outfile:
                        outfile.write("- Attention! The import "+file+" is complete, but partially. Some fields are already filled in.\n")
                else:
                    with open("outPyScript.log", "a") as outfile:
                        outfile.write("+ Import file "+file+" completed successfully.\n")
            browser.quit()
        elif "resEr4g." in file or "resEr4gBul." in file or "resEr4gBulNeop." in file:
            print(file)
            print("... Ready to import data 4G Ericsson/Bulat from "+file+" file to CES website")
            with open("outPyScript.log", "a") as outfile:
                outfile.write("... Ready to import data 4G Ericsson/Bulat from "+file+" file to CES website\n")
            op = webdriver.ChromeOptions()
            op.add_argument('headless')
            print("... loading")
            op.binary_location =  r'C:\\Program Files\Yandex\YandexBrowser\Application\browser.exe'
            service = Service(executable_path=r'C:\\Users\david.gabunia\parserWeb\yandexdriver.exe')
            #browser = webdriver.Chrome(options=op)
            browser = webdriver.Chrome(service=service, options=op)
            browser.get('http://'+ipEricsson+'/CreateSite_web/login.php')
            soup = BeautifulSoup(browser.page_source, "html.parser")
            findUsername = browser.find_element(By.ID, "username")
            findPasswd = browser.find_element(By.ID, "password")
            findLogin = browser.find_element(By.CSS_SELECTOR, '.btn-primary')
            findUsername.send_keys(userCes)
            findPasswd.send_keys(passwdCes)
            findLogin.click()
            print("... loading")
            time.sleep(5)
            browser.get('http://'+ipEricsson+'/CreateSite_web/import_ericsson_4g/index_bss.php')
            findInput = browser.find_element(By.XPATH, "//input[@type='file']")
            findInput.send_keys(os.path.expanduser("~") + "\\parserWeb\\"+file)
            time.sleep(5)
            findSubmit = browser.find_element(By.CSS_SELECTOR, '.btn-primary')
            findSubmit.click()
            time.sleep(5)
            soup = BeautifulSoup(browser.page_source, "html.parser")
            findHtmlMessage = soup.find_all(class_='jumbotron')
            if ("Файл для импорта должен быть" in str(findHtmlMessage[0])) or ("Файл CSV неверной кодировки" in str(findHtmlMessage[0])) or ("Недопустимы разные" in str(findHtmlMessage[0])):
                with open("outPyScript.log", "a") as outfile:
                    outfile.write("- Attention! The file "+file+" for import does not match.\n")
            if "Импорт выполнен" in str(findHtmlMessage[0]):
                if "КРОМЕ" in str(findHtmlMessage[0]):
                    with open("outPyScript.log", "a") as outfile:
                        outfile.write("- Attention! The import "+file+" is complete, but partially. Some fields are already filled in.\n")
                else:
                    with open("outPyScript.log", "a") as outfile:
                        outfile.write("+ Import file "+file+" completed successfully.\n")
            browser.quit()
    return files
def unloadCoords(coordsData):
    listdbs = []
    listRow = []
    try: 
        mydb = mysql.connector.connect(
            host=ipNokia,
            user=userDb,
            password=passwdDb,
        )
    except mysql.connector.errors.ProgrammingError:
        with open("outPyScript.log", "a") as outfile:
            outfile.write("- Error connecting to MYSQL Platform:\n")
    mycursor = mydb.cursor()
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Connected to the database\n")
    querrydbs = ("SHOW DATABASES")        
    mycursor.execute(querrydbs)
    for querrydbs in mycursor:
        listdbs.append(querrydbs[0])
    for db in listdbs:
        if dbCoords == db:
            with open("outPyScript.log", "a") as outfile:
                outfile.write("... Database filter "+db+"\n")
            try:
                querry = "SELECT site, longitude, latitude FROM Physical_param.Physical_param WHERE region IN ('IR','SA','MD','KM','HB','BI','AN','YA','ZB','AM','VV','BU')"
                mycursor.execute(querry)
                result = mycursor.fetchall()
                for row in result:
                    listRow.append(row)
            except mysql.connector.errors.ProgrammingError:
                continue
            except mysql.connector.errors.DatabaseError:
                continue        
        else:
            continue
    coordsData = pd.DataFrame(listRow, columns =['BS_name', 'longitudeY2', 'latitudeX2'])
    coordsData = coordsData.drop_duplicates()
    mycursor.close()
    mydb.close()
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information from the DB Coordinates.\n")
    return coordsData
def unloadCes2gNok(cesData):
    listdbs = []
    listRow = []
    try: 
        mydb = mysql.connector.connect(
            host=ipNokia,
            user=userDb,
            password=passwdDb,
        )
    except mysql.connector.errors.ProgrammingError:
        print("- Error connecting to MYSQL Platform:\n")
    mycursor = mydb.cursor()
    querrydbs = ("SHOW DATABASES")        
    mycursor.execute(querrydbs)
    for querrydbs in mycursor:
        listdbs.append(querrydbs[0])
    for db in listdbs:
        #if dbCes == db and dbCes in listdbs and dbCoords in listdbs:
        if dbCes == db and dbCes in listdbs:
            try:
                querry = "SELECT Reg, BS_name, BS_number, CELL FROM CreateSite.table_nokia_2g_v WHERE BSS IS NULL AND Reg IN ('IR','SA','MD','KM','HB','BI','AiN','YA')"
                mycursor.execute(querry)
                result = mycursor.fetchall()
                for row in result:
                    listRow.append(row)
            except mysql.connector.errors.ProgrammingError:
                continue
            except mysql.connector.errors.DatabaseError:
                continue
        else:
            continue
    cesData = pd.DataFrame(listRow, columns =['Reg', 'BS_name', 'BCF','Sector'])
    cesData = cesData.drop_duplicates()
    mycursor.close()
    mydb.close()
    return cesData
def unloadCes3gNok(cesData):
    listdbs = []
    listRow = []
    try: 
        mydb = mysql.connector.connect(
            host=ipNokia,
            user=userDb,
            password=passwdDb,
        )
    except mysql.connector.errors.ProgrammingError:
        with open("outPyScript.log", "a") as outfile:
            outfile.write("- Error connecting to MYSQL Platform:\n")
    mycursor = mydb.cursor()
    querrydbs = ("SHOW DATABASES")        
    mycursor.execute(querrydbs)
    for querrydbs in mycursor:
        listdbs.append(querrydbs[0])
    for db in listdbs:
        if dbCes == db and dbCes in listdbs and dbCoords in listdbs:
            try:
                querry = "SELECT Reg, BS_name_RDB, Sector_name FROM CreateSite.table_nokia_3g_v WHERE BSS IS NULL AND Reg IN ('IR','SA','MD','KM','HB','BI','AiN','YA')"
                mycursor.execute(querry)
                result = mycursor.fetchall()
                for row in result:
                    listRow.append(row)
            except mysql.connector.errors.ProgrammingError:
                continue
            except mysql.connector.errors.DatabaseError:
                continue
        else:
            continue
    cesData = pd.DataFrame(listRow, columns =['Reg', 'BS_name', 'Sector'])
    cesData = cesData.drop_duplicates()
    mycursor.close()
    mydb.close()
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information from the Site CES 3G Nokia.\n")
    return cesData
def unloadCes4gNok(cesData):
    listdbs = []
    listRow = []
    try: 
        mydb = mysql.connector.connect(
            host=ipNokia,
            user=userDb,
            password=passwdDb,
        )
    except mysql.connector.errors.ProgrammingError:
        with open("outPyScript.log", "a") as outfile:
            outfile.write("- Error connecting to MYSQL Platform:\n")
    mycursor = mydb.cursor()
    querrydbs = ("SHOW DATABASES")        
    mycursor.execute(querrydbs)
    for querrydbs in mycursor:
        listdbs.append(querrydbs[0])
    for db in listdbs:
        if dbCes == db and dbCes in listdbs and dbCoords in listdbs:
            try:
                querry = "SELECT Reg, BS_name, Sector_name FROM CreateSite.table_nokia_4g_v WHERE BSS IS NULL AND Reg IN ('IR','SA','MD','KM','HB','BI','AiN','YA')"
                mycursor.execute(querry)
                result = mycursor.fetchall()
                for row in result:
                    listRow.append(row)
            except mysql.connector.errors.ProgrammingError:
                continue
            except mysql.connector.errors.DatabaseError:
                continue
        else:
            continue
    cesData = pd.DataFrame(listRow, columns =['Reg', 'BS_name', 'Sector'])
    cesData = cesData.drop_duplicates()
    mycursor.close()
    mydb.close()
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information from the Site CES 4G Nokia.\n")
    return cesData
def unloadCes2gEr(cesData):
    listdbs = []
    listRow = []
    try: 
        mydb = mysql.connector.connect(
            host=ipEricsson,
            user=userDb,
            password=passwdDb,
        )
    except mysql.connector.errors.ProgrammingError:
        with open("outPyScript.log", "a") as outfile:
            outfile.write("- Error connecting to MYSQL Platform:\n")
    mycursor = mydb.cursor()
    querrydbs = ("SHOW DATABASES")        
    mycursor.execute(querrydbs)
    for querrydbs in mycursor:
        listdbs.append(querrydbs[0])
    for db in listdbs:
        if dbCes == db:
            try:
                querry = "SELECT Reg, SUBSTRING(CELL, 1, 6) AS BS_name, CELL, BS_name AS site FROM CreateSite.table_ericsson_2g_v WHERE BSS IS NULL AND Reg IN ('BU','VV','ZB','AM')"
                mycursor.execute(querry)
                result = mycursor.fetchall()
                for row in result:
                    listRow.append(row)
            except mysql.connector.errors.ProgrammingError:
                continue
            except mysql.connector.errors.DatabaseError:
                continue
        else:
            continue
    cesData = pd.DataFrame(listRow, columns =['Reg', 'BS_name', 'Sector', 'site'])
    cesData = cesData.drop_duplicates()
    mycursor.close()
    mydb.close()
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information from the Site CES 2G Ericsson.\n")
    return cesData
def unloadCes3gEr(cesData):
    listdbs = []
    listRow = []
    try: 
        mydb = mysql.connector.connect(
            host=ipEricsson,
            user=userDb,
            password=passwdDb,
        )
    except mysql.connector.errors.ProgrammingError:
        with open("outPyScript.log", "a") as outfile:
            outfile.write("- Error connecting to MYSQL Platform:\n")
    mycursor = mydb.cursor()
    querrydbs = ("SHOW DATABASES")        
    mycursor.execute(querrydbs)
    for querrydbs in mycursor:
        listdbs.append(querrydbs[0])
    for db in listdbs:
        if dbCes == db:
            try:
                #querry = "SELECT Reg, SUBSTRING(System_module_name_3G, 1, 6) AS name, Sector_Name, SUBSTRING(Sector_Name, 1, 6) AS BS_name, System_module_name_3G FROM CreateSite.table_ericsson_3g_v WHERE BSS IS NULL AND Reg IN ('BU','VV','ZB','AM')"
                querry = "SELECT Reg, SUBSTRING(System_module_name_3G, 1, 6) AS BS_name, Sector_Name, SUBSTRING(Sector_Name, 1, 6) AS name, System_module_name_3G FROM CreateSite.table_ericsson_3g_v WHERE BSS IS NULL AND Reg IN ('BU','VV','ZB','AM')"
                mycursor.execute(querry)
                result = mycursor.fetchall()
                for row in result:
                    listRow.append(row)
            except mysql.connector.errors.ProgrammingError:
                continue
            except mysql.connector.errors.DatabaseError:
                continue
        else:
            continue
    cesData = pd.DataFrame(listRow, columns =['Reg', 'BS_name', 'Sector', 'name', 'site'])
    cesData = cesData.drop_duplicates()
    mycursor.close()
    mydb.close()
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information from the Site CES 3G Ericsson.\n")
    return cesData
def unloadCes4gEr(cesData):
    listdbs = []
    listRow = []
    try: 
        mydb = mysql.connector.connect(
            host=ipEricsson,
            user=userDb,
            password=passwdDb,
        )
    except mysql.connector.errors.ProgrammingError:
        with open("outPyScript.log", "a") as outfile:
            outfile.write("- Error connecting to MYSQL Platform:\n")
    mycursor = mydb.cursor()
    querrydbs = ("SHOW DATABASES")        
    mycursor.execute(querrydbs)
    for querrydbs in mycursor:
        listdbs.append(querrydbs[0])
    for db in listdbs:
        if dbCes == db:
            try:
                querry = "SELECT Reg, SUBSTRING(System_module_name_4G, 1, 6) AS BS_name, System_module_name_4G AS site, Sector_name FROM CreateSite.table_ericsson_4g_v WHERE BSS IS NULL AND Reg IN ('BU','VV','ZB','AM')"
                mycursor.execute(querry)
                result = mycursor.fetchall()
                for row in result:
                    listRow.append(row)
            except mysql.connector.errors.ProgrammingError:
                continue
            except mysql.connector.errors.DatabaseError:
                continue
        else:
            continue
    cesData = pd.DataFrame(listRow, columns =['Reg', 'BS_name', 'site', 'Sector'])
    cesData = cesData.drop_duplicates()
    mycursor.close()
    mydb.close()
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information from the Site CES 4G Ericsson.\n")
    return cesData
def unloadCes2gNokBul(cesData):
    listdbs = []
    listRow = []
    try: 
        mydb = mysql.connector.connect(
            host=ipNokia,
            user=userDb,
            password=passwdDb,
        )
    except mysql.connector.errors.ProgrammingError:
        with open("outPyScript.log", "a") as outfile:
            outfile.write("- Error connecting to MYSQL Platform:\n")
    mycursor = mydb.cursor()
    querrydbs = ("SHOW DATABASES")        
    mycursor.execute(querrydbs)
    for querrydbs in mycursor:
        listdbs.append(querrydbs[0])
    for db in listdbs:
        if dbCes == db:
            try:
                querry = "SELECT Reg, BS_name, BS_number, CELL FROM CreateSite.table_bulat_2g_v WHERE BSS IS NULL AND Reg IN ('IR','SA','MD','KM','HB','BI','AiN','YA')"
                mycursor.execute(querry)
                result = mycursor.fetchall()
                for row in result:
                    listRow.append(row)
            except mysql.connector.errors.ProgrammingError:
                continue
            except mysql.connector.errors.DatabaseError:
                continue
        else:
            continue
    cesData = pd.DataFrame(listRow, columns =['Reg', 'BS_name', 'BCF','Sector'])
    cesData = cesData.drop_duplicates()
    mycursor.close()
    mydb.close()
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information from the Site CES 2G Bulat.\n")
    return cesData
def unloadCes4gNokBul(cesData):
    listdbs = []
    listRow = []
    try: 
        mydb = mysql.connector.connect(
            host=ipNokia,
            user=userDb,
            password=passwdDb,
        )
    except mysql.connector.errors.ProgrammingError:
        with open("outPyScript.log", "a") as outfile:
            outfile.write("- Error connecting to MYSQL Platform:\n")
    mycursor = mydb.cursor()
    querrydbs = ("SHOW DATABASES")        
    mycursor.execute(querrydbs)
    for querrydbs in mycursor:
        listdbs.append(querrydbs[0])
    for db in listdbs:
        if dbCes == db:
            try:
                querry = "SELECT Reg, BS_name, Sector_name FROM CreateSite.table_bulat_4g_v WHERE BSS IS NULL AND Reg IN ('IR','SA','MD','KM','HB','BI','AiN','YA')" 
                mycursor.execute(querry)
                result = mycursor.fetchall()
                for row in result:
                    listRow.append(row)
            except mysql.connector.errors.ProgrammingError:
                continue
            except mysql.connector.errors.DatabaseError:
                continue
        else:
            continue
    cesData = pd.DataFrame(listRow, columns =['Reg', 'BS_name', 'Sector'])
    cesData = cesData.drop_duplicates()
    mycursor.close()
    mydb.close()
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information from the Site CES 4G Bulat.\n")
    return cesData
def unloadCes2gErBul(cesData):
    listdbs = []
    listRow = []
    try: 
        mydb = mysql.connector.connect(
            host=ipEricsson,
            user=userDb,
            password=passwdDb,
        )
    except mysql.connector.errors.ProgrammingError:
        with open("outPyScript.log", "a") as outfile:
            outfile.write("- Error connecting to MYSQL Platform:\n")
    mycursor = mydb.cursor()
    querrydbs = ("SHOW DATABASES")        
    mycursor.execute(querrydbs)
    for querrydbs in mycursor:
        listdbs.append(querrydbs[0])
    for db in listdbs:
        if dbCes == db:
            try:
                querry = "SELECT Reg, SUBSTRING(CELL, 1, 6) AS BS_name, CELL, BS_name AS site FROM CreateSite.table_bulat_2g_v WHERE BSS IS NULL AND Reg IN ('BU','VV','ZB','AM')" 
                mycursor.execute(querry)
                result = mycursor.fetchall()
                for row in result:
                    listRow.append(row)
            except mysql.connector.errors.ProgrammingError:
                continue
            except mysql.connector.errors.DatabaseError:
                continue
        else:
            continue
    cesData = pd.DataFrame(listRow, columns =['Reg', 'BS_name', 'Sector', 'site'])
    cesData = cesData.drop_duplicates()
    mycursor.close()
    mydb.close()
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information from the Site CES 2G Bulat.\n")
    return cesData
def unloadCes4gErBul(cesData):
    listdbs = []
    listRow = []
    try: 
        mydb = mysql.connector.connect(
            host=ipEricsson,
            user=userDb,
            password=passwdDb,
        )
    except mysql.connector.errors.ProgrammingError:
        with open("outPyScript.log", "a") as outfile:
            outfile.write("- Error connecting to MYSQL Platform:\n")
    mycursor = mydb.cursor()
    querrydbs = ("SHOW DATABASES")        
    mycursor.execute(querrydbs)
    for querrydbs in mycursor:
        listdbs.append(querrydbs[0])
    for db in listdbs:
        if dbCes == db:
            try:
                querry = "SELECT Reg, SUBSTRING(System_module_name_4G, 1, 6) AS BS_name, System_module_name_4G AS site, Sector_name FROM CreateSite.table_bulat_4g_v WHERE BSS IS NULL AND Reg IN ('BU','VV','ZB','AM')" 
                mycursor.execute(querry)
                result = mycursor.fetchall()
                for row in result:
                    listRow.append(row)
            except mysql.connector.errors.ProgrammingError:
                continue
            except mysql.connector.errors.DatabaseError:
                continue
        else:
            continue
    cesData = pd.DataFrame(listRow, columns =['Reg', 'BS_name', 'site', 'Sector'])
    cesData = cesData.drop_duplicates()
    mycursor.close()
    mydb.close()
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information from the Site CES 4G Bulat.\n")
    return cesData
def unloadCes2gErBulNeop(cesData):
    listdbs = []
    listRow = []
    try: 
        mydb = mysql.connector.connect(
            host=ipEricsson,
            user=userDb,
            password=passwdDb,
        )
    except mysql.connector.errors.ProgrammingError:
        with open("outPyScript.log", "a") as outfile:
            outfile.write("- Error connecting to MYSQL Platform:\n")
    mycursor = mydb.cursor()
    querrydbs = ("SHOW DATABASES")        
    mycursor.execute(querrydbs)
    for querrydbs in mycursor:
        listdbs.append(querrydbs[0])
    for db in listdbs:
        if dbCes == db:
            try:
                querry = "SELECT Reg, SUBSTRING(CELL, 1, 6) AS BS_name, CELL, BS_name AS site FROM CreateSite.table_bulat_2gNEOP_v WHERE BSS IS NULL AND Reg IN ('BU','VV','ZB','AM')" 
                mycursor.execute(querry)
                result = mycursor.fetchall()
                for row in result:
                    listRow.append(row)
            except mysql.connector.errors.ProgrammingError:
                continue
            except mysql.connector.errors.DatabaseError:
                continue
        else:
            continue
    cesData = pd.DataFrame(listRow, columns =['Reg', 'BS_name', 'Sector', 'site'])
    cesData = cesData.drop_duplicates()
    mycursor.close()
    mydb.close()
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information from the Site CES 2G Bulat Neop.\n")
    return cesData
def unloadCes4gErBulNeop(cesData):
    listdbs = []
    listRow = []
    try: 
        mydb = mysql.connector.connect(
            host=ipEricsson,
            user=userDb,
            password=passwdDb,
        )
    except mysql.connector.errors.ProgrammingError:
        with open("outPyScript.log", "a") as outfile:
            outfile.write("- Error connecting to MYSQL Platform:\n")
    mycursor = mydb.cursor()
    querrydbs = ("SHOW DATABASES")        
    mycursor.execute(querrydbs)
    for querrydbs in mycursor:
        listdbs.append(querrydbs[0])
    for db in listdbs:
        if dbCes == db:
            try:
                querry = "SELECT Reg, SUBSTRING(System_module_name_4G, 1, 6) AS BS_name, System_module_name_4G AS site, Sector_name FROM CreateSite.table_bulat_4gNEOP_v WHERE BSS IS NULL AND Reg IN ('BU','VV','ZB','AM')" 
                mycursor.execute(querry)
                result = mycursor.fetchall()
                for row in result:
                    listRow.append(row)
            except mysql.connector.errors.ProgrammingError:
                continue
            except mysql.connector.errors.DatabaseError:
                continue
        else:
            continue
    cesData = pd.DataFrame(listRow, columns =['Reg', 'BS_name', 'site', 'Sector'])
    cesData = cesData.drop_duplicates()
    mycursor.close()
    mydb.close()
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information from the Site CES 4G Bulat Neop.\n")
    return cesData
def unloadDaily2g(oldData):
    listdbs = []
    listRow = []
    try: 
        mydb = mysql.connector.connect(
            host=ipNokia,
            user=userDb,
            password=passwdDb,
        )
    except mysql.connector.errors.ProgrammingError:
        with open("outPyScript.log", "a") as outfile:
            outfile.write("- Error connecting to MYSQL Platform:\n")
    mycursor = mydb.cursor()
    querrydbs = ("SHOW DATABASES")        
    mycursor.execute(querrydbs)
    for querrydbs in mycursor:
        listdbs.append(querrydbs[0])
    for db in listdbs:
        if dbCes == db:
            try:
                querry = "SELECT SUBSTRING(nwName, 1, 6) AS BS_name, lac, racode, int_name FROM Config_all.Config WHERE reg IN ('IR','SA','MD','KM','HB','BI','AN','YA','BU','VV','ZB','AM')"
                mycursor.execute(querry)
                result = mycursor.fetchall()
                for row in result:
                    listRow.append(row)
            except mysql.connector.errors.ProgrammingError:
                continue
            except mysql.connector.errors.DatabaseError:
                continue
        else:
            continue
    oldData = pd.DataFrame(listRow, columns =['BS_name', 'LAC', 'RAC', 'BSC'])
    oldData = oldData.drop_duplicates()
    mycursor.close()
    mydb.close()
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information from the DB 2G.\n")
    return oldData
def unloadDaily3g(oldData):
    listdbs = []
    listRow = []
    try: 
        mydb = mysql.connector.connect(
            host=ipEricsson,
            user=userDb,
            password=passwdDb,
        )
    except mysql.connector.errors.ProgrammingError:
        with open("outPyScript.log", "a") as outfile:
            outfile.write("- Error connecting to MYSQL Platform:\n")
    mycursor = mydb.cursor()
    querrydbs = ("SHOW DATABASES")        
    mycursor.execute(querrydbs)
    for querrydbs in mycursor:
        listdbs.append(querrydbs[0])
    for db in listdbs:
        if dbCes == db:
            try:
                querry = "SELECT rncid, lac, rac, uralist, mnc, SUBSTRING(Sectorname, 1, 6) AS BS_name, CONCAT_WS('', (SUBSTRING(Sectorname, 1, 2)), (CASE WHEN LENGTH((CAST((CAST(SUBSTRING(Sectorname, 3, 6) AS DECIMAL)-3000) AS CHAR))) < 2 THEN CONCAT('000', (CAST((CAST(SUBSTRING(Sectorname, 3, 6) AS DECIMAL)-3000) AS CHAR))) WHEN LENGTH((CAST((CAST(SUBSTRING(Sectorname, 3, 6) AS DECIMAL)-3000) AS CHAR))) < 3 THEN CONCAT('00', (CAST((CAST(SUBSTRING(Sectorname, 3, 6) AS DECIMAL)-3000) AS CHAR))) WHEN LENGTH(CAST((CAST(SUBSTRING(Sectorname, 3, 6) AS DECIMAL)-3000) AS CHAR)) < 4 THEN CONCAT('0', (CAST((CAST(SUBSTRING(Sectorname, 3, 6) AS DECIMAL)-3000) AS CHAR))) ELSE CAST((CAST(SUBSTRING(Sectorname, 3, 6) AS DECIMAL)-3000) AS CHAR) END)) AS Namefor3g FROM "+dbConfig+".config_3g WHERE region IN ('IR','SA','MD','KM','HB','BI','AN','YA','BU','VV','ZB','AM')"
                mycursor.execute(querry)
                result = mycursor.fetchall()
                for row in result:
                    listRow.append(row)
            except mysql.connector.errors.ProgrammingError:
                continue
            except mysql.connector.errors.DatabaseError:
                continue
        else:
            continue
    oldData = pd.DataFrame(listRow, columns =['RNC_ID', 'LAC', 'RAC', 'URA', 'RRU', 'BS_name', 'Namefor3g'])
    oldData = oldData.drop_duplicates()
    mycursor.close()
    mydb.close()
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information from the Site CES 3G.\n")
    return oldData
def unloadDaily4g(oldData):
    listdbs = []
    listRow = []
    try: 
        mydb = mysql.connector.connect(
            host=ipEricsson,
            user=userDb,
            password=passwdDb,
        )
    except mysql.connector.errors.ProgrammingError:
        with open("outPyScript.log", "a") as outfile:
            outfile.write("- Error connecting to MYSQL Platform:\n")
    mycursor = mydb.cursor()
    querrydbs = ("SHOW DATABASES")        
    mycursor.execute(querrydbs)
    for querrydbs in mycursor:
        listdbs.append(querrydbs[0])
    for db in listdbs:
        if dbCes == db:
            try:
                querry = "SELECT SUBSTRING(Sectorname, 1, 6) AS BS_name, tac FROM Config_all.config4g WHERE reg IN ('IR','SA','MD','KM','HB','BI','AN','YA','BU','VV','ZB','AM')"
                mycursor.execute(querry)
                result = mycursor.fetchall()
                for row in result:
                    listRow.append(row)
            except mysql.connector.errors.ProgrammingError:
                continue
            except mysql.connector.errors.DatabaseError:
                continue
        else:
            continue
    oldData = pd.DataFrame(listRow, columns =['BS_name', 'LAC'])
    oldData = oldData.drop_duplicates()
    mycursor.close()
    mydb.close()
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information from the Site CES 4G.\n")
    return oldData
def joinOldBs2g(oldData, cesData):
    dailyTable = pd.DataFrame()
    dailyTable = unloadDaily2g(dailyTable)
    oldData = pd.merge(cesData, dailyTable, left_on='BS_name', right_on='BS_name', how='inner')
    return oldData, cesData
def joinOldBs3g(oldData, cesData):
    dailyTable = pd.DataFrame()
    dailyTable = unloadDaily3g(dailyTable)
    oldData = pd.merge(cesData, dailyTable, left_on='BS_name', right_on='BS_name', how='inner')
    return oldData, cesData
def joinOldBs4g(oldData, cesData):
    dailyTable = pd.DataFrame()
    dailyTable = unloadDaily4g(dailyTable)
    #oldData=''
    oldData = pd.merge(cesData, dailyTable, left_on='BS_name', right_on='BS_name', how='inner')
    return oldData, cesData
# Переменные:
ces2gNokTable = pd.DataFrame()
ces3gNokTable = pd.DataFrame()
ces4gNokTable = pd.DataFrame()
ces2gErTable = pd.DataFrame()
ces3gErTable = pd.DataFrame()
ces4gErTable = pd.DataFrame()
ces2gNokBulTable = pd.DataFrame()
ces4gNokBulTable = pd.DataFrame()
ces2gErBulTable = pd.DataFrame()
ces4gErBulTable = pd.DataFrame()
ces2gErBulNeopTable = pd.DataFrame()
ces4gErBulNeopTable = pd.DataFrame()
ipNokia = ""
ipEricsson = ""
userCes = ""
passwdCes = ""
userDb = ""
passwdDb = ""
dbCes = ""
dbConfig = ""
dbCoords = ""
newList = []
readyList = []
dataList = []
listFiles=[]
#1
with open("outPyScript.log", "w") as outfile:
    outfile.write("+ Created Log file output.log\n")
#2 Считывание данных из файла config.txt:
ipNokia, ipEricsson, userCes, passwdCes, userDb, passwdDb, dbCes, dbConfig, dbCoords = hiddenData(ipNokia, ipEricsson, userCes, passwdCes, userDb, passwdDb, dbCes, dbConfig, dbCoords)
#3 Выгрузка информации по CES из Базы данных CES:
ces2gNokTable = unloadCes2gNok(ces2gNokTable)
print(ces2gNokTable)
ces3gNokTable = unloadCes3gNok(ces3gNokTable)
ces4gNokTable = unloadCes4gNok(ces4gNokTable)
ces2gErTable = unloadCes2gEr(ces2gErTable)
ces3gErTable = unloadCes3gEr(ces3gErTable)
ces4gErTable = unloadCes4gEr(ces4gErTable)
ces2gNokBulTable = unloadCes2gNokBul(ces2gNokBulTable)
ces4gNokBulTable = unloadCes4gNokBul(ces4gNokBulTable)
ces2gErBulTable = unloadCes2gErBul(ces2gErBulTable)
ces4gErBulTable = unloadCes4gErBul(ces4gErBulTable)
ces2gErBulNeopTable = unloadCes2gErBulNeop(ces2gErBulNeopTable)
ces4gErBulNeopTable = unloadCes4gErBulNeop(ces4gErBulNeopTable)
#4 
if checkTable(ces2gNokTable) == False:
    oldBsTable = pd.DataFrame()
    newBsTable = pd.DataFrame()
    resNok2g = pd.DataFrame()
    nameNewBsTable = pd.DataFrame()
    print("Empty table (ces2gNokTable) 2G Nokia:")
    print(ces2gNokTable)
    with open("outPyScript.log", "a") as outfile:
        outfile.write("... Empty table (ces2gNokTable) 2G Nokia.\n")
    #5
    oldBsTable, ces2gNokTable = joinOldBs2g(oldBsTable, ces2gNokTable)
    print("+ Added information (oldBsTable) about Old BS 2G Nokia.")
    print(oldBsTable)
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (oldBsTable) about Old BS 2G Nokia.\n")
    #6
    nameNewBsTable, ces2gNokTable = findNewSites(nameNewBsTable, ces2gNokTable)
    print("+ Added information (nameNewBsTable) about name New BS 2G Nokia.")
    print(nameNewBsTable)
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (nameNewBsTable) about name New BS 2G Nokia.\n")
    #7
    if checkTable(nameNewBsTable) == False:
        rdbTable= pd.DataFrame()
        noUcnTable = pd.DataFrame()
        ucnTable = pd.DataFrame()         
        #10       
        rdbTable = parsingRdb(rdbTable)
        with open("outPyScript.log", "a") as outfile:
            outfile.write("+ Added information (rdbTable) about New BS 2G Nokia from site RDB.\n")
        #11
        noUcnTable = pd.concat([rdbTable, noUcnTable])
        noUcnTable = noUcnTable[noUcnTable["UCN"].isin(["-"])] 
        if checkTable(noUcnTable) == False:
            dailyTable = pd.DataFrame()            
            coordsTable = pd.DataFrame()
            #12
            noUcnTable = pd.merge(noUcnTable, ces2gNokTable, left_on='index', right_on='BS_name', how='inner')
            dailyTable = unloadDaily2g(dailyTable)
            coordsTable = unloadCoords(coordsTable)
            dailyTable = pd.merge(dailyTable, coordsTable, left_on='BS_name', right_on='BS_name', how='inner')
            neighbourTable = noUcnTable.merge(dailyTable, how='cross')
            noUcnTable = findNeighbourTable(neighbourTable)
            noUcnTable["SW"]="MR10"
            noUcnTable["BCF"]=noUcnTable["BCF"].astype("int64")
            noUcnTable = noUcnTable.reindex(columns=["Reg", "Sector", "SW", "BSC", "BCF", "LAC", "RAC"])
            newBsTable = pd.concat([newBsTable, noUcnTable])
        ucnTable = pd.concat([rdbTable, ucnTable])
        ucnTable = ucnTable[ucnTable["UCN"].isin(["УЦН"])]        
        if checkTable(ucnTable) == False:
            #13
            ucnLBRTable = pd.DataFrame()
            ucnLBRTable = templateUcn(ucnLBRTable)
            ucnTable = pd.merge(ucnTable, ucnLBRTable, left_on='RegUcn', right_on='RegUcn', how='inner')
            ucnTable = pd.merge(ucnTable, ces2gNokTable, left_on='index', right_on='BS_name', how='inner')
            if checkTable(newBsTable) == False:
                print("- Attention! It is necessary to take into account the data of (newBsTable, ucnTable, noUcnTable) for sites with non-UCN")
                with open("outPyScript.log", "a") as outfile:
                    outfile.write("- Attention! It is necessary to take into account the data of (newBsTable, ucnTable, noUcnTable) for sites with non-UCN\n")
            else:
                ucnTable["SW"]="MR10"
                ucnTable["BCF"]=ucnTable["BCF"].astype("int64")
                renamecol=ucnTable["BscUcn"]
                ucnTable.insert(1, "BSC", renamecol)
                renamecol=ucnTable["LacUcn"]
                ucnTable.insert(1, "LAC", renamecol)
                renamecol=ucnTable["RacUcn"]
                ucnTable.insert(1, "RAC", renamecol)
                ucnTable["RAC"]=ucnTable["RAC"].astype("int64")
                ucnTable = ucnTable.reindex(columns=["Reg", "Sector", "SW", "BSC", "BCF", "LAC", "RAC"])
                newBsTable = pd.concat([newBsTable, ucnTable])
    #14
    oldBsTable["SW"]="MR10"
    oldBsTable["BCF"]=oldBsTable["BCF"].astype("int64")
    oldBsTable = oldBsTable.reindex(columns=["Reg", "Sector", "SW", "BSC", "BCF", "LAC", "RAC"])
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Corrected information (oldBsTable) about Old BS 2G Nokia.\n")
    #8
    resNok2g, oldBsTable, newBsTable = writeResults(resNok2g, oldBsTable, newBsTable)
    print("General table (resNok2g) for Old and New BS sites")
    print(resNok2g)    
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (resNok2g) about New and Old BS 2G Nokia.\n")
    #9
    resNok2g.to_csv("resNok2g.csv", sep=';', index=False, header=False, encoding='UTF-8-SIG')
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (resNok2g) about New and Old BS 2G Nokia in File.\n")
if checkTable(ces3gNokTable) == False:
    oldBsTable = pd.DataFrame()
    newBsTable = pd.DataFrame()
    resNok3g = pd.DataFrame()
    nameNewBsTable = pd.DataFrame()
    print("Empty table (ces3gNokTable) 3G Nokia:")
    print(ces3gNokTable)
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Empty table (ces3gNokTable) 3G Nokia.\n")
    #5
    oldBsTable, ces3gNokTable = joinOldBs3g(oldBsTable, ces3gNokTable)
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (oldBsTable) about Old BS 3G Nokia.\n")
    #6
    nameNewBsTable, ces3gNokTable = findNewSites(nameNewBsTable, ces3gNokTable)    
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (nameNewBsTable) about name New BS 3G Nokia.\n")
    #7
    if checkTable(nameNewBsTable) == False:
        rdbTable= pd.DataFrame()
        noUcnTable = pd.DataFrame()
        ucnTable = pd.DataFrame()         
        #10       
        rdbTable = parsingRdb(rdbTable)
        with open("outPyScript.log", "a") as outfile:
            outfile.write("+ Added information (rdbTable) about New BS 3G Nokia from site RDB.\n")
        #11
        noUcnTable = pd.concat([rdbTable, noUcnTable])
        with open("outPyScript.log", "a") as outfile:
            outfile.write("+ Joined information (noUcnTable) about New BS 3G Nokia with data from site RDB (rdbTable).\n")
        noUcnTable = noUcnTable[noUcnTable["UCN"].isin(["-"])]
        with open("outPyScript.log", "a") as outfile:
            outfile.write("+ Filter information (noUcnTable) about UCN 3G Nokia.\n")
        if checkTable(noUcnTable) == False:
            dailyTable = pd.DataFrame()
            coordsTable = pd.DataFrame() 
            #12
            noUcnTable = pd.merge(noUcnTable, ces3gNokTable, left_on='index', right_on='BS_name', how='inner')
            with open("outPyScript.log", "a") as outfile:
                outfile.write("+ Joined information (noUcnTable) about New BS 3G Nokia with data from site CES (ces3gNokTable).\n")
            dailyTable = unloadDaily3g(dailyTable)
            coordsTable = unloadCoords(coordsTable)
            with open("outPyScript.log", "a") as outfile:
                outfile.write("+ Added information (dailyTable, coordsTable) about Old BS 3G Nokia with coordinates.\n")
            #dailyTable = pd.merge(dailyTable, coordsTable, left_on='BS_name', right_on='BS_name', how='inner')
            dailyTable = pd.merge(dailyTable, coordsTable, left_on='Namefor3g', right_on='BS_name', how='inner')
            with open("outPyScript.log", "a") as outfile:
                outfile.write("+ Joined information (dailyTable) about Old BS 3G Nokia with coordinates.\n")
            neighbourTable = noUcnTable.merge(dailyTable, how='cross')
            with open("outPyScript.log", "a") as outfile:
                outfile.write("+ Joined information (neighbourTable) about neighbour (dailyTable) Old BS 3G Nokia with new data (noUcnTable).\n")
            noUcnTable = findNeighbourTable(neighbourTable)
            with open("outPyScript.log", "a") as outfile:
                outfile.write("+ Added information (noUcnTable) about neighbour (dailyTable) Old BS 3G Nokia with new data (noUcnTable).\n")
            noUcnTable = noUcnTable.reindex(columns=["Reg", "BS_name", "Sector", "LAC", "RAC", "URA", "RNC_ID"])
            with open("outPyScript.log", "a") as outfile:
                outfile.write("+ Corrected information (noUcnTable) about New BS 3G Nokia.\n")
            newBsTable = pd.concat([newBsTable, noUcnTable])
            with open("outPyScript.log", "a") as outfile:
                outfile.write("+ Added information (newBsTable) about New BS 3G Nokia.\n")
        ucnTable = pd.concat([rdbTable, ucnTable])
        ucnTable = ucnTable[ucnTable["UCN"].isin(["УЦН"])]        
        if checkTable(ucnTable) == False:
            #13
            ucnLBRTable = pd.DataFrame()
            ucnLBRTable = templateUcn(ucnLBRTable)
            ucnTable = pd.merge(ucnTable, ucnLBRTable, left_on='RegUcn', right_on='RegUcn', how='inner')
            ucnTable = pd.merge(ucnTable, ces3gNokTable, left_on='index', right_on='BS_name', how='inner')
            if checkTable(newBsTable) == False:
                print("- Attention! It is necessary to take into account the data of (newBsTable, ucnTable, noUcnTable) for sites with non-UCN")
                with open("outPyScript.log", "a") as outfile:
                    outfile.write("- Attention! It is necessary to take into account the data of (newBsTable, ucnTable, noUcnTable) for sites with non-UCN\n")
            else:
                print("Внимание! Скопировал код у Булат. необходимо проверм скрипт для учета (ucnTable) УЦН 3G Nokia.")
                renamecol=ucnTable["LacUcn"]
                ucnTable.insert(1, "LAC", renamecol)
                renamecol=ucnTable["RacUcn"]
                ucnTable.insert(1, "RAC", renamecol)
                ucnTable = ucnTable.reindex(columns=["Reg", "BS_name", "Sector", "LAC", "RAC", "URA", "RNC_ID"])
                newBsTable = pd.concat([newBsTable, ucnTable])
    #14
    oldBsTable = oldBsTable.reindex(columns=["Reg", "BS_name", "Sector", "LAC", "RAC", "URA", "RNC_ID"])
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Corrected information (oldBsTable) about Old BS 3G Nokia.\n")
    #8
    resNok3g, oldBsTable, newBsTable = writeResults(resNok3g, oldBsTable, newBsTable)
    print("General table (resNok3g) for Old and New BS sites")
    print(resNok3g)    
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (resNok3g) about New and Old BS 3G Nokia.\n")
    #9
    resNok3g.to_csv("resNok3g.csv", sep=';', index=False, header=False, encoding='UTF-8-SIG')
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (resNok3g) about New and Old BS 3G Nokia in File.\n")
if checkTable(ces4gNokTable) == False:
    oldBsTable = pd.DataFrame()
    newBsTable = pd.DataFrame()
    resNok4g = pd.DataFrame()
    nameNewBsTable = pd.DataFrame()
    print("Empty table (ces4gNokTable) 4G Nokia:")
    print(ces4gNokTable)
    with open("outPyScript.log", "a") as outfile:
        outfile.write("... Empty table (ces4gNokTable) 4G Nokia.\n")
    #5
    oldBsTable, ces4gNokTable = joinOldBs4g(oldBsTable, ces4gNokTable)
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (oldBsTable) about Old BS 4G Nokia.\n")
    #6    
    nameNewBsTable, ces4gNokTable = findNewSites(nameNewBsTable, ces4gNokTable)
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (nameNewBsTable) about name New BS 4G Nokia.\n")
    #7
    if checkTable(nameNewBsTable) == False:
        rdbTable= pd.DataFrame()
        noUcnTable = pd.DataFrame()
        ucnTable = pd.DataFrame()          
        #10      
        rdbTable = parsingRdb(rdbTable)
        with open("outPyScript.log", "a") as outfile:
            outfile.write("+ Added information (rdbTable) about New BS 4G Nokia from site RDB.\n")
        #11
        noUcnTable = pd.concat([rdbTable, noUcnTable])
        noUcnTable = noUcnTable[noUcnTable["UCN"].isin(["-"])] 
        if checkTable(noUcnTable) == False:
            #12
            noUcnTable = pd.merge(noUcnTable, ces4gNokTable, left_on='index', right_on='BS_name', how='inner')
            dailyTable = pd.DataFrame()
            dailyTable = unloadDaily4g(dailyTable)
            coordsTable = pd.DataFrame()  
            coordsTable = unloadCoords(coordsTable)
            dailyTable = pd.merge(dailyTable, coordsTable, left_on='BS_name', right_on='BS_name', how='inner')
            neighbourTable = noUcnTable.merge(dailyTable, how='cross')
            noUcnTable = findNeighbourTable(neighbourTable)
            renamecol=noUcnTable["BS_name_x"]
            noUcnTable.insert(1, "BS_name", renamecol)
            noUcnTable = noUcnTable.reindex(columns=["Reg", "BS_name", "Sector", "LAC"])
            newBsTable = pd.concat([newBsTable, noUcnTable])  
        ucnTable = pd.concat([rdbTable, ucnTable])
        ucnTable = ucnTable[ucnTable["UCN"].isin(["УЦН"])]        
        if checkTable(ucnTable) == False:
            #13
            ucnLBRTable = pd.DataFrame()
            print("Внимание! нужно заполнить (ucnTable) сайты для УЦН! Учтено уже запонение не УЦН сайтов (newBsTable) необходимо аккуратно соединить с ucnTable")            
            ucnLBRTable = templateUcn(ucnLBRTable)
            ucnTable = pd.merge(ucnTable, ucnLBRTable, left_on='RegUcn', right_on='RegUcn', how='inner')
            ucnTable = pd.merge(ucnTable, ces4gNokTable, left_on='index', right_on='BS_name', how='inner')
            if checkTable(newBsTable) == False:
                print("- Attention! It is necessary to take into account the data of (newBsTable, ucnTable, noUcnTable) for sites with non-UCN")
                with open("outPyScript.log", "a") as outfile:
                    outfile.write("- Attention! It is necessary to take into account the data of (newBsTable, ucnTable, noUcnTable) for sites with non-UCN\n")
            else:
                renamecol=ucnTable["LacUcn"]
                ucnTable.insert(1, "LAC", renamecol)
                ucnTable = ucnTable.reindex(columns=["Reg", "BS_name", "Sector", "LAC"])
                newBsTable = pd.concat([newBsTable, ucnTable])                
    #14
    oldBsTable = oldBsTable.reindex(columns=["Reg","BS_name","Sector","LAC"])
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Corrected information (oldBsTable) about Old BS 4G Nokia.\n")
    #8
    resNok4g, oldBsTable, newBsTable = writeResults(resNok4g, oldBsTable, newBsTable)
    print("General table (resNok4g) for Old and New BS sites")
    print(resNok4g)    
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (resNok4g) about New and Old BS 4G Nokia.\n")
    #9
    resNok4g.to_csv("resNok4g.csv", sep=';', index=False, header=False, encoding='UTF-8-SIG')
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (resNok4g) about New and Old BS 4G Nokia in File.\n")
if checkTable(ces2gErTable) == False:
    oldBsTable = pd.DataFrame()
    newBsTable = pd.DataFrame()
    resEr2g = pd.DataFrame()
    nameNewBsTable = pd.DataFrame()
    print("Empty table (ces2gErTable) 2G Ericsson:")
    print(ces2gErTable)
    with open("outPyScript.log", "a") as outfile:
        outfile.write("... Empty table (ces2gErTable) 2G Ericsson.\n")
    #5
    oldBsTable, ces2gErTable = joinOldBs2g(oldBsTable, ces2gErTable)
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (oldBsTable) about Old BS 2G Ericsson.\n")
    #6
    nameNewBsTable, ces2gErTable = findNewSites(nameNewBsTable, ces2gErTable)
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (nameNewBsTable) about name New BS 2G Ericsson.\n")
    #7
    if checkTable(nameNewBsTable) == False:
        rdbTable= pd.DataFrame()
        noUcnTable = pd.DataFrame()
        ucnTable = pd.DataFrame()
        #10
        rdbTable = parsingRdb(rdbTable)
        with open("outPyScript.log", "a") as outfile:
            outfile.write("+ Added information (rdbTable) about New BS 2G Ericsson from site RDB.\n")
        #11
        noUcnTable = pd.concat([rdbTable, noUcnTable])
        noUcnTable = noUcnTable[noUcnTable["UCN"].isin(["-"])]        
        if checkTable(noUcnTable) == False:
            dailyTable = pd.DataFrame()
            coordsTable = pd.DataFrame()
            #12
            noUcnTable = pd.merge(noUcnTable, ces2gErTable, left_on='index', right_on='BS_name', how='inner')
            dailyTable = unloadDaily2g(dailyTable)
            coordsTable = unloadCoords(coordsTable)
            dailyTable = pd.merge(dailyTable, coordsTable, left_on='BS_name', right_on='BS_name', how='inner')
            neighbourTable = noUcnTable.merge(dailyTable, how='cross')
            noUcnTable = findNeighbourTable(neighbourTable)
            renamecol=noUcnTable["BS_name_x"]
            noUcnTable.insert(1, "BS_name", renamecol)
            noUcnTable["TG"]="0"
            noUcnTable["SW"]="-"
            noUcnTable["RBL2_1"]="-"
            noUcnTable["RBL2_2"]="-"
            noUcnTable["OETM_1"]="-"
            noUcnTable["OETM_2"]="-"
            noUcnTable = noUcnTable.reindex(columns=["Reg","site","BSC","TG","BS_name","SW","LAC","RBL2_1","RBL2_2","OETM_1","OETM_2","Sector"])
            newBsTable = pd.concat([newBsTable, noUcnTable])
        ucnTable = pd.concat([rdbTable, ucnTable])
        ucnTable = ucnTable[ucnTable["UCN"].isin(["УЦН"])]     
        if checkTable(ucnTable) == False:
            #13
            ucnLBRTable = pd.DataFrame()
            ucnLBRTable = templateUcn(ucnLBRTable)
            ucnTable = pd.merge(ucnTable, ucnLBRTable, left_on='RegUcn', right_on='RegUcn', how='inner')
            ucnTable = pd.merge(ucnTable, ces2gErTable, left_on='index', right_on='BS_name', how='inner')
            if checkTable(newBsTable) == False:
                print("- Attention! It is necessary to take into account the data of (newBsTable, ucnTable, noUcnTable) for sites with non-UCN")
                with open("outPyScript.log", "a") as outfile:
                    outfile.write("- Attention! It is necessary to take into account the data of (newBsTable, ucnTable, noUcnTable) for sites with non-UCN\n")
            else:
                print("- Attention! Copied the code from Bulat. We need to check the script for accounting (ucnTable) of UCN 2G Bulat.")
                with open("outPyScript.log", "a") as outfile:
                    outfile.write("- Attention! Copied the code from Bulat. We need to check the script for accounting (ucnTable) of UCN 2G Bulat.\n")
                ucnTable["TG"]="0"
                ucnTable["SW"]="-"
                ucnTable["RBL2_1"]="-"
                ucnTable["RBL2_2"]="-"
                ucnTable["OETM_1"]="-"
                ucnTable["OETM_2"]="-"
                renamecol=ucnTable["BscUcn"]
                ucnTable.insert(1, "BSC", renamecol)
                renamecol=ucnTable["LacUcn"]
                ucnTable.insert(1, "LAC", renamecol)
                ucnTable = ucnTable.reindex(columns=["Reg","site","BSC","TG","BS_name","SW","LAC","RBL2_1","RBL2_2","OETM_1","OETM_2","Sector"])
                newBsTable = pd.concat([newBsTable, ucnTable])
    #14
    oldBsTable["TG"]="0"
    oldBsTable["SW"]="-"
    oldBsTable["RBL2_1"]="-"
    oldBsTable["RBL2_2"]="-"
    oldBsTable["OETM_1"]="-"
    oldBsTable["OETM_2"]="-"
    oldBsTable = oldBsTable.reindex(columns=["Reg","site","BSC","TG","BS_name","SW","LAC","RBL2_1","RBL2_2","OETM_1","OETM_2","Sector"])
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Corrected information (oldBsTable) about Old BS 2G Ericsson.\n")
    #8
    resEr2g, oldBsTable, newBsTable = writeResults(resEr2g, oldBsTable, newBsTable)
    print("General table (resEr2g) for Old and New BS sites")
    print(resEr2g)    
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (resEr2g) about New and Old BS 2G Ericsson.\n")
    #9
    resEr2g.to_csv("resEr2g.csv", sep=',', index=False, header=False, encoding='UTF-8-SIG')
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ General table (resEr2g) for old and new 2G Ericsson site.\n")
if checkTable(ces3gErTable) == False:
    oldBsTable = pd.DataFrame()
    newBsTable = pd.DataFrame()
    resEr3g = pd.DataFrame()
    nameNewBsTable = pd.DataFrame()
    print("Empty table (ces3gErTable) 3G Ericsson:")
    print(ces3gErTable)
    with open("outPyScript.log", "a") as outfile:
        outfile.write("... Empty table (ces3gErTable) 3G Ericsson.\n")
    #5
    oldBsTable, ces3gErTable = joinOldBs3g(oldBsTable, ces3gErTable)
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (oldBsTable) about Old BS 3G Ericsson.\n")
    #6
    nameNewBsTable, ces3gErTable = findNewSites(nameNewBsTable, ces3gErTable)
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (nameNewBsTable) about name New BS 3G Ericsson.\n")
    #7
    if checkTable(nameNewBsTable) == False:
        rdbTable= pd.DataFrame()
        noUcnTable = pd.DataFrame()
        ucnTable = pd.DataFrame()
        #10
        rdbTable = parsingRdb(rdbTable)
        with open("outPyScript.log", "a") as outfile:
            outfile.write("+ Added information (rdbTable) about New BS 3G Ericsson from site RDB.\n")
        #11
        noUcnTable = pd.concat([rdbTable, noUcnTable])
        noUcnTable = noUcnTable[noUcnTable["UCN"].isin(["-"])]        
        if checkTable(noUcnTable) == False:
            dailyTable = pd.DataFrame()
            coordsTable = pd.DataFrame()
            #12
            noUcnTable = pd.merge(noUcnTable, ces3gErTable, left_on='index', right_on='BS_name', how='inner')
            dailyTable = unloadDaily3g(dailyTable)
            coordsTable = unloadCoords(coordsTable)
            dailyTable = pd.merge(dailyTable, coordsTable, left_on='Namefor3g', right_on='BS_name', how='inner')
            neighbourTable = noUcnTable.merge(dailyTable, how='cross')
            noUcnTable = findNeighbourTable(neighbourTable)
            noUcnTable = noUcnTable.reindex(columns=["Reg","site","RNC_ID","URA","LAC","RAC","RRU","Sector"])
            newBsTable = pd.concat([newBsTable, noUcnTable])
        ucnTable = pd.concat([rdbTable, ucnTable])
        ucnTable = ucnTable[ucnTable["UCN"].isin(["УЦН"])]     
        if checkTable(ucnTable) == False:
            #13
            ucnLBRTable = pd.DataFrame()
            ucnLBRTable = templateUcn(ucnLBRTable)
            ucnTable = pd.merge(ucnTable, ucnLBRTable, left_on='RegUcn', right_on='RegUcn', how='inner')
            ucnTable = pd.merge(ucnTable, ces3gErTable, left_on='index', right_on='BS_name', how='inner')
            if checkTable(newBsTable) == False:
                print("- Attention! It is necessary to take into account the data of (newBsTable, ucnTable, noUcnTable) for sites with non-UCN")
                with open("outPyScript.log", "a") as outfile:
                    outfile.write("- Attention! It is necessary to take into account the data of (newBsTable, ucnTable, noUcnTable) for sites with non-UCN\n")
            else:
                print("- Attention! Copied the code from Bulat. We need to check the script for accounting (ucnTable) of UCN 3G Ericsson.")
                with open("outPyScript.log", "a") as outfile:
                    outfile.write("- Attention! Copied the code from Bulat. We need to check the script for accounting (ucnTable) of UCN 3G Ericsson.\n")
                renamecol=ucnTable["LacUcn"]
                ucnTable.insert(1, "LAC", renamecol)
                ucnTable = ucnTable.reindex(columns=["Reg","site","RNC_ID","URA","LAC","RAC","RRU","Sector"])
                newBsTable = pd.concat([newBsTable, ucnTable])
    #14
    oldBsTable = oldBsTable.reindex(columns=["Reg","site","RNC_ID","URA","LAC","RAC","RRU","Sector"])
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Corrected information (oldBsTable) about Old BS 3G Ericsson.\n")
    #8
    resEr3g, oldBsTable, newBsTable = writeResults(resEr3g, oldBsTable, newBsTable)
    print("General table (resEr3g) for Old and New BS sites")
    print(resEr3g)    
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (resEr3g) about New and Old BS 3G Ericsson.\n")
    #9
    resEr3g.to_csv("resEr3g.csv", sep=',', index=False, header=False, encoding='UTF-8-SIG')
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ General table (resEr3g) for old and new 3G Ericsson site.\n")
if checkTable(ces4gErTable) == False:
    oldBsTable = pd.DataFrame()
    newBsTable = pd.DataFrame()
    resEr4g = pd.DataFrame()
    nameNewBsTable = pd.DataFrame()
    print("Empty table (ces4gErTable) 4G Ericsson:")
    print(ces4gErTable)
    with open("outPyScript.log", "a") as outfile:
        outfile.write("... Empty table (ces4gErTable) 4G Ericsson.\n")
    #5
    oldBsTable, ces4gErTable = joinOldBs4g(oldBsTable, ces4gErTable)
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (oldBsTable) about Old BS 4G Ericsson.\n")
    #6
    nameNewBsTable, ces4gErTable = findNewSites(nameNewBsTable, ces4gErTable)
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (nameNewBsTable) about name New BS 4G Ericsson.\n")
    #7
    if checkTable(nameNewBsTable) == False:
        rdbTable= pd.DataFrame()
        noUcnTable = pd.DataFrame()
        ucnTable = pd.DataFrame()
        #10       
        rdbTable = parsingRdb(rdbTable)
        with open("outPyScript.log", "a") as outfile:
            outfile.write("+ Added information (rdbTable) about New BS 4G Ericsson from site RDB.\n")
        #11
        noUcnTable = pd.concat([rdbTable, noUcnTable])
        noUcnTable = noUcnTable[noUcnTable["UCN"].isin(["-"])]
        if checkTable(noUcnTable) == False:
            #12
            noUcnTable = pd.merge(noUcnTable, ces4gErTable, left_on='index', right_on='BS_name', how='inner')
            dailyTable = pd.DataFrame()
            dailyTable = unloadDaily4g(dailyTable)
            coordsTable = pd.DataFrame()  
            coordsTable = unloadCoords(coordsTable)
            dailyTable = pd.merge(dailyTable, coordsTable, left_on='BS_name', right_on='BS_name', how='inner')
            neighbourTable = noUcnTable.merge(dailyTable, how='cross')
            noUcnTable = findNeighbourTable(neighbourTable)
            newBsTable = noUcnTable.reindex(columns=["Reg", "site", "LAC", "Sector"])
        ucnTable = pd.concat([rdbTable, ucnTable])
        ucnTable = ucnTable[ucnTable["UCN"].isin(["УЦН"])]        
        if checkTable(ucnTable) == False:
            #13
            ucnLBRTable = pd.DataFrame()
            ucnLBRTable = templateUcn(ucnLBRTable)
            print("- Attention! It is necessary to check the correctness of the table connection by the templateUcn function in 4G Ericsson:")
            with open("outPyScript.log", "a") as outfile:
                outfile.write("- Attention! It is necessary to check the correctness of the table connection by the templateUcn function in 4G Ericsson\n")
            ucnTable = pd.merge(ucnTable, ucnLBRTable, left_on='RegUcn', right_on='RegUcn', how='inner')
            ucnTable = pd.merge(ucnTable, ces4gErTable, left_on='index', right_on='BS_name', how='inner')
            if checkTable(newBsTable) == False:
                print("- Attention! It is necessary to take into account the data of (newBsTable, ucnTable, noUcnTable) for sites with non-UCN")
                with open("outPyScript.log", "a") as outfile:
                    outfile.write("- Attention! It is necessary to take into account the data of (newBsTable, ucnTable, noUcnTable) for sites with non-UCN\n")
            else:
                renamecol=ucnTable["LacUcn"]
                ucnTable.insert(1, "LAC", renamecol)
                print("- Attention! Instead of BS_name changed to site. need to make sure correctness in table (newBsTable, ucnTable) 4G Ericsson:")
                with open("outPyScript.log", "a") as outfile:
                    outfile.write("- Attention! Instead of BS_name changed to site. need to make sure correctness in table (newBsTable, ucnTable) 4G Ericsson\n")
                print("ucnTable:")
                print(ucnTable)
                ucnTable = ucnTable.reindex(columns=["Reg", "site", "LAC", "Sector"])
                newBsTable = pd.concat([newBsTable, ucnTable])
    #14
    oldBsTable = oldBsTable.reindex(columns=["Reg", "site", "LAC", "Sector"])
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Corrected information (oldBsTable) about Old BS 4G Ericsson.\n")
    #8
    resEr4g, oldBsTable, newBsTable = writeResults(resEr4g, oldBsTable, newBsTable)
    print("General table (resEr4g) for Old and New BS sites")
    print(resEr4g)
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (resEr4g) about New and Old BS 4G Ericsson.\n")
    #9
    resEr4g.to_csv("resEr4g.csv", sep=',', index=False, header=False, encoding='UTF-8-SIG')
if checkTable(ces2gNokBulTable) == False:
    oldBsTable = pd.DataFrame()
    newBsTable = pd.DataFrame()
    resNok2gBul = pd.DataFrame()
    nameNewBsTable = pd.DataFrame()
    print("Empty table (ces2gNokBulTable) 2G Bulat:")
    print(ces2gNokBulTable)
    with open("outPyScript.log", "a") as outfile:
        outfile.write("... Empty table (ces2gNokBulTable) 2G Bulat.\n")
    #5
    print("Attention! If there are additional weights, you need to check the filling (joinOldBs2g) for Bulat additional weights.")
    oldBsTable, ces2gNokBulTable = joinOldBs2g(oldBsTable, ces2gNokBulTable)
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (oldBsTable) about Old BS 2G Bulat.\n")
    #6
    nameNewBsTable, ces2gNokBulTable = findNewSites(nameNewBsTable, ces2gNokBulTable)
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (nameNewBsTable) about name New BS 2G Bulat.\n")
    #7
    if checkTable(nameNewBsTable) == False:
        rdbTable= pd.DataFrame()
        noUcnTable = pd.DataFrame()
        ucnTable = pd.DataFrame()         
        #10       
        rdbTable = parsingRdb(rdbTable)
        with open("outPyScript.log", "a") as outfile:
            outfile.write("+ Added information (rdbTable) about New BS 2G Bulat from site RDB.\n")
        #11
        noUcnTable = pd.concat([rdbTable, noUcnTable])
        noUcnTable = noUcnTable[noUcnTable["UCN"].isin(["-"])] 
        if checkTable(noUcnTable) == False:
            #12
            print("- Attention! It is necessary to check the filling (noUcnTable) of sites for non-UCN! In Bulat, at the time of writing the program, all sites were UCN.")
            with open("outPyScript.log", "a") as outfile:
                outfile.write("- Attention! It is necessary to check the filling (noUcnTable) of sites for non-UCN! In Bulat, at the time of writing the program, all sites were UCN.\n")
        ucnTable = pd.concat([rdbTable, ucnTable])
        ucnTable = ucnTable[ucnTable["UCN"].isin(["УЦН"])]        
        if checkTable(ucnTable) == False:
            #13
            ucnLBRTable = pd.DataFrame()
            ucnLBRTable = templateUcnBul(ucnLBRTable)
            ucnTable = pd.merge(ucnTable, ucnLBRTable, left_on='RegUcn', right_on='RegUcn', how='inner')
            ucnTable = pd.merge(ucnTable, ces2gNokBulTable, left_on='index', right_on='BS_name', how='inner')
            if checkTable(newBsTable) == False:
                print("- Attention! It is necessary to take into account the data of (newBsTable, ucnTable, noUcnTable) for sites with non-UCN")
                with open("outPyScript.log", "a") as outfile:
                    outfile.write("- Attention! It is necessary to take into account the data of (newBsTable, ucnTable, noUcnTable) for sites with non-UCN\n")
            else:
                ucnTable["SW"]="MR10"
                ucnTable["BCF"]=ucnTable["BCF"].astype("int64")
                renamecol=ucnTable["BscUcn"]
                ucnTable.insert(1, "BSC", renamecol)
                renamecol=ucnTable["LacUcn"]
                ucnTable.insert(1, "LAC", renamecol)
                renamecol=ucnTable["RacUcn"]
                ucnTable.insert(1, "RAC", renamecol)
                ucnTable = ucnTable.reindex(columns=["Reg", "Sector", "SW", "BSC", "BCF", "LAC", "RAC"])
                newBsTable = pd.concat([newBsTable, ucnTable])
    #14
    oldBsTable = oldBsTable.reindex(columns=["Reg", "Sector", "SW", "BSC", "BCF", "LAC", "RAC"])
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Corrected information (oldBsTable) about Old BS 2G Bulat.\n")
    #8
    resNok2gBul, oldBsTable, newBsTable = writeResults(resNok2gBul, oldBsTable, newBsTable)
    print("General table (resNok2gBul) for Old and New BS sites")
    print(resNok2gBul)    
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (resNok2gBul) about New and Old BS 2G Bulat.\n")
    #9
    resNok2gBul.to_csv("resNok2gBul.csv", sep=';', index=False, header=False, encoding='UTF-8-SIG')
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (resNok2gBul) about New and Old BS 2G Bulat in File.\n")
if checkTable(ces4gNokBulTable) == False:
    oldBsTable = pd.DataFrame()
    newBsTable = pd.DataFrame()
    resNok4gBul = pd.DataFrame()
    nameNewBsTable = pd.DataFrame()
    print("Empty table (ces4gNokBulTable) 4G Bulat:")
    print(ces4gNokBulTable)
    with open("outPyScript.log", "a") as outfile:
        outfile.write("... Empty table (ces4gNokBulTable) 4G Bulat.\n")
    #5
    print("Attention! If there are additional weights, you need to check the filling (joinOldBs4g) for Bulat additional weights.")
    oldBsTable, ces4gNokBulTable = joinOldBs4g(oldBsTable, ces4gNokBulTable)
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (oldBsTable) about Old BS 4G Bulat.\n")
    #6
    nameNewBsTable, ces4gNokBulTable = findNewSites(nameNewBsTable, ces4gNokBulTable)
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (nameNewBsTable) about name New BS 4G Bulat.\n")
    #7
    if checkTable(nameNewBsTable) == False:
        rdbTable= pd.DataFrame()
        noUcnTable = pd.DataFrame()
        ucnTable = pd.DataFrame()         
        #10       
        rdbTable = parsingRdb(rdbTable)
        with open("outPyScript.log", "a") as outfile:
            outfile.write("+ Added information (rdbTable) about New BS 4G Bulat from site RDB.\n")
        #11
        noUcnTable = pd.concat([rdbTable, noUcnTable])
        noUcnTable = noUcnTable[noUcnTable["UCN"].isin(["-"])] 
        if checkTable(noUcnTable) == False:
            #12
            print("- Attention! It is necessary to check the filling (noUcnTable) of sites for non-UCN! In Bulat, at the time of writing the program, all sites were UCN.")
            with open("outPyScript.log", "a") as outfile:
                outfile.write("- Attention! It is necessary to check the filling (noUcnTable) of sites for non-UCN! In Bulat, at the time of writing the program, all sites were UCN.\n")
        ucnTable = pd.concat([rdbTable, ucnTable])
        ucnTable = ucnTable[ucnTable["UCN"].isin(["УЦН"])]        
        if checkTable(ucnTable) == False:
            #13
            ucnLBRTable = pd.DataFrame()
            ucnLBRTable = templateUcnBul(ucnLBRTable)
            ucnTable = pd.merge(ucnTable, ucnLBRTable, left_on='RegUcn', right_on='RegUcn', how='inner')
            ucnTable = pd.merge(ucnTable, ces4gNokBulTable, left_on='index', right_on='BS_name', how='inner')
            if checkTable(newBsTable) == False:
                print("- Attention! It is necessary to take into account the data of (newBsTable, ucnTable, noUcnTable) for sites with non-UCN")
                with open("outPyScript.log", "a") as outfile:
                    outfile.write("- Attention! It is necessary to take into account the data of (newBsTable, ucnTable, noUcnTable) for sites with non-UCN\n")
            else:
                renamecol=ucnTable["LacUcn"]
                ucnTable.insert(1, "LAC", renamecol)
                ucnTable = ucnTable.reindex(columns=["Reg", "BS_name", "Sector", "LAC"])
                newBsTable = pd.concat([newBsTable, ucnTable])
    #14
    oldBsTable = oldBsTable.reindex(columns=["Reg","BS_name","Sector","LAC"])
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Corrected information (oldBsTable) about Old BS 4G Bulat.\n")
    #8
    resNok4gBul, oldBsTable, newBsTable = writeResults(resNok4gBul, oldBsTable, newBsTable)
    print("General table (resNok4gBul) for Old and New BS sites")
    print(resNok4gBul)    
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (resNok4gBul) about New and Old BS 4G Bulat.\n")
    #9
    resNok4gBul.to_csv("resNok4gBul.csv", sep=';', index=False, header=False, encoding='UTF-8-SIG')
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (resNok4gBul) about New and Old BS 4G Bulat in File.\n")
if checkTable(ces2gErBulTable) == False:
    oldBsTable = pd.DataFrame()
    newBsTable = pd.DataFrame()
    resEr2gBul = pd.DataFrame()
    nameNewBsTable = pd.DataFrame()
    print("Empty table (ces2gErBulTable) 2G Bulat:")
    print(ces2gErBulTable)
    with open("outPyScript.log", "a") as outfile:
        outfile.write("... Empty table (ces2gErBulTable) 2G Bulat.\n")
    #5
    print("Attention! If there are additional weights, you need to check the filling (joinOldBs2g) for Bulat additional weights.")
    oldBsTable, ces2gErBulTable = joinOldBs2g(oldBsTable, ces2gErBulTable)
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (oldBsTable) about Old BS 2G Bulat.\n")
    #6
    nameNewBsTable, ces2gErBulTable = findNewSites(nameNewBsTable, ces2gErBulTable)
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (nameNewBsTable) about name New BS 2G Bulat.\n")
    #7
    if checkTable(nameNewBsTable) == False:
        rdbTable= pd.DataFrame()
        noUcnTable = pd.DataFrame()
        ucnTable = pd.DataFrame()
        #10
        rdbTable = parsingRdb(rdbTable)
        with open("outPyScript.log", "a") as outfile:
            outfile.write("+ Added information (rdbTable) about New BS 2G Bulat from site RDB.\n")
        #11
        noUcnTable = pd.concat([rdbTable, noUcnTable])
        noUcnTable = noUcnTable[noUcnTable["UCN"].isin(["-"])]        
        if checkTable(noUcnTable) == False:
            #12
            print("- Attention! It is necessary to check the filling (noUcnTable) of sites for non-UCN! In Bulat, at the time of writing the program, all sites were UCN.")
            with open("outPyScript.log", "a") as outfile:
                outfile.write("- Attention! It is necessary to check the filling (noUcnTable) of sites for non-UCN! In Bulat, at the time of writing the program, all sites were UCN.\n")
        ucnTable = pd.concat([rdbTable, ucnTable])
        ucnTable = ucnTable[ucnTable["UCN"].isin(["УЦН"])]        
        if checkTable(ucnTable) == False:
            #13
            ucnLBRTable = pd.DataFrame()
            ucnLBRTable = templateUcnBul(ucnLBRTable)
            ucnTable = pd.merge(ucnTable, ucnLBRTable, left_on='RegUcn', right_on='RegUcn', how='inner')
            ucnTable = pd.merge(ucnTable, ces2gErBulTable, left_on='index', right_on='BS_name', how='inner')
            if checkTable(newBsTable) == False:
                print("- Attention! It is necessary to take into account the data of (newBsTable, ucnTable, noUcnTable) for sites with non-UCN")
                with open("outPyScript.log", "a") as outfile:
                    outfile.write("- Attention! It is necessary to take into account the data of (newBsTable, ucnTable, noUcnTable) for sites with non-UCN\n")
            else:
                ucnTable["TG"]="0"
                ucnTable["SW"]="-"
                ucnTable["RBL2_1"]="-"
                ucnTable["RBL2_2"]="-"
                ucnTable["OETM_1"]="-"
                ucnTable["OETM_2"]="-"
                renamecol=ucnTable["BscUcn"]
                ucnTable.insert(1, "BSC", renamecol)
                renamecol=ucnTable["LacUcn"]
                ucnTable.insert(1, "LAC", renamecol)
                ucnTable = ucnTable.reindex(columns=["Reg","site","BSC","TG","BS_name","SW","LAC","RBL2_1","RBL2_2","OETM_1","OETM_2","Sector"])
                newBsTable = pd.concat([newBsTable, ucnTable])
    #14
    oldBsTable["TG"]="0"
    oldBsTable["SW"]="-"
    oldBsTable["RBL2_1"]="-"
    oldBsTable["RBL2_2"]="-"
    oldBsTable["OETM_1"]="-"
    oldBsTable["OETM_2"]="-"
    oldBsTable = oldBsTable.reindex(columns=["Reg","site","BSC","TG","BS_name","SW","LAC","RBL2_1","RBL2_2","OETM_1","OETM_2","Sector"])
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Corrected information (oldBsTable) about Old BS 2G Bulat.\n")
    #8
    resEr2gBul, oldBsTable, newBsTable = writeResults(resEr2gBul, oldBsTable, newBsTable)
    print("General table (resEr2gBul) for Old and New BS sites")
    print(resEr2gBul)    
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (resEr2gBul) about New and Old BS 2G Bulat.\n")
    #9
    resEr2gBul.to_csv("resEr2gBul.csv", sep=',', index=False, header=False, encoding='UTF-8-SIG')
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ General table (resEr2gBul) for old and new 2G Bulat site.\n")
if checkTable(ces4gErBulTable) == False:
    oldBsTable = pd.DataFrame()
    newBsTable = pd.DataFrame()
    resEr4gBul = pd.DataFrame()
    nameNewBsTable = pd.DataFrame()
    print("Empty table (ces4gErBulTable) 4G Bulat:")
    print(ces4gErBulTable)
    with open("outPyScript.log", "a") as outfile:
        outfile.write("... Empty table (ces4gErBulTable) 4G Bulat.\n")
    #5
    print("Attention! If there are additional weights, you need to check the filling (joinOldBs4g) for Bulat additional weights.")
    oldBsTable, ces4gErBulTable = joinOldBs4g(oldBsTable, ces4gErBulTable)
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (oldBsTable) about Old BS 4G Bulat.\n")
    #6
    nameNewBsTable, ces4gErBulTable = findNewSites(nameNewBsTable, ces4gErBulTable)
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (nameNewBsTable) about name New BS 4G Bulat.\n")
    #7
    if checkTable(nameNewBsTable) == False:
        rdbTable= pd.DataFrame()
        noUcnTable = pd.DataFrame()
        ucnTable = pd.DataFrame()
        #10       
        rdbTable = parsingRdb(rdbTable)
        with open("outPyScript.log", "a") as outfile:
            outfile.write("+ Added information (rdbTable) about New BS 4G Bulat from site RDB.\n")
        #11
        noUcnTable = pd.concat([rdbTable, noUcnTable])
        noUcnTable = noUcnTable[noUcnTable["UCN"].isin(["-"])]
        if checkTable(noUcnTable) == False:
            #12
            print("- Attention! It is necessary to check the filling (noUcnTable) of sites for non-UCN! In Bulat, at the time of writing the program, all sites were UCN.")
            with open("outPyScript.log", "a") as outfile:
                outfile.write("- Attention! It is necessary to check the filling (noUcnTable) of sites for non-UCN! In Bulat, at the time of writing the program, all sites were UCN.\n")
        ucnTable = pd.concat([rdbTable, ucnTable])
        ucnTable = ucnTable[ucnTable["UCN"].isin(["УЦН"])]        
        if checkTable(ucnTable) == False:
            #13
            ucnLBRTable = pd.DataFrame()
            ucnLBRTable = templateUcnBul(ucnLBRTable)
            ucnTable = pd.merge(ucnTable, ucnLBRTable, left_on='RegUcn', right_on='RegUcn', how='inner')
            ucnTable = pd.merge(ucnTable, ces4gErBulTable, left_on='index', right_on='BS_name', how='inner')
            if checkTable(newBsTable) == False:
                print("- Attention! It is necessary to take into account the data of (newBsTable, ucnTable, noUcnTable) for sites with non-UCN")
                with open("outPyScript.log", "a") as outfile:
                    outfile.write("- Attention! It is necessary to take into account the data of (newBsTable, ucnTable, noUcnTable) for sites with non-UCN\n")
            else:
                renamecol=ucnTable["LacUcn"]
                ucnTable.insert(1, "LAC", renamecol)
                ucnTable = ucnTable.reindex(columns=["Reg", "site", "LAC", "Sector"])
                newBsTable = pd.concat([newBsTable, ucnTable])
    #14
    oldBsTable = oldBsTable.reindex(columns=["Reg", "site", "LAC", "Sector"])
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Corrected information (oldBsTable) about Old BS 4G Bulat.\n")
    #8
    resEr4gBul, oldBsTable, newBsTable = writeResults(resEr4gBul, oldBsTable, newBsTable)
    print("General table (resEr4gBul) for Old and New BS sites")
    print(resEr4gBul)
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (resEr4gBul) about New and Old BS 4G Bulat.\n")
    #9
    resEr4gBul.to_csv("resEr4gBul.csv", sep=',', index=False, header=False, encoding='UTF-8-SIG')
if checkTable(ces2gErBulNeopTable) == False:
    oldBsTable = pd.DataFrame()
    newBsTable = pd.DataFrame()
    resEr2gBulNeop = pd.DataFrame()
    nameNewBsTable = pd.DataFrame()
    print("Empty table (ces2gErBulNeopTable) 2G Bulat:")
    print(ces2gErBulNeopTable)
    with open("outPyScript.log", "a") as outfile:
        outfile.write("... Empty table (ces2gErBulNeopTable) 2G Bulat.\n")
    #5
    print("Attention! If there are additional weights, you need to check the filling (joinOldBs2g) for Bulat additional weights.")
    oldBsTable, ces2gErBulNeopTable = joinOldBs2g(oldBsTable, ces2gErBulNeopTable)
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (oldBsTable) about Old BS 2G Bulat.\n")
    #6
    nameNewBsTable, ces2gErBulNeopTable = findNewSites(nameNewBsTable, ces2gErBulNeopTable)
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (nameNewBsTable) about name New BS 2G Bulat.\n")
    #7
    if checkTable(nameNewBsTable) == False:
        rdbTable= pd.DataFrame()
        noUcnTable = pd.DataFrame()
        ucnTable = pd.DataFrame()         
        #10       
        rdbTable = parsingRdb(rdbTable)
        with open("outPyScript.log", "a") as outfile:
            outfile.write("+ Added information (rdbTable) about New BS 2G Bulat from site RDB.\n")
        #11
        noUcnTable = pd.concat([rdbTable, noUcnTable])
        noUcnTable = noUcnTable[noUcnTable["UCN"].isin(["-"])] 
        if checkTable(noUcnTable) == False:
            #12
            print("- Attention! It is necessary to check the filling (noUcnTable) of sites for non-UCN! In Bulat, at the time of writing the program, all sites were UCN.")
            with open("outPyScript.log", "a") as outfile:
                outfile.write("- Attention! It is necessary to check the filling (noUcnTable) of sites for non-UCN! In Bulat, at the time of writing the program, all sites were UCN.\n")
        ucnTable = pd.concat([rdbTable, ucnTable])
        ucnTable = ucnTable[ucnTable["UCN"].isin(["УЦН"])]        
        if checkTable(ucnTable) == False:
            #13
            ucnLBRTable = pd.DataFrame()
            ucnLBRTable = templateUcnBul(ucnLBRTable)
            ucnTable = pd.merge(ucnTable, ucnLBRTable, left_on='RegUcn', right_on='RegUcn', how='inner')
            ucnTable = pd.merge(ucnTable, ces2gErBulNeopTable, left_on='index', right_on='BS_name', how='inner')
            if checkTable(newBsTable) == False:
                print("- Attention! It is necessary to take into account the data of (newBsTable, ucnTable, noUcnTable) for sites with non-UCN")
                with open("outPyScript.log", "a") as outfile:
                    outfile.write("- Attention! It is necessary to take into account the data of (newBsTable, ucnTable, noUcnTable) for sites with non-UCN\n")
            else:
                ucnTable["TG"]="0"
                ucnTable["SW"]="-"
                ucnTable["RBL2_1"]="-"
                ucnTable["RBL2_2"]="-"
                ucnTable["OETM_1"]="-"
                ucnTable["OETM_2"]="-"
                renamecol=ucnTable["BscUcn"]
                ucnTable.insert(1, "BSC", renamecol)
                renamecol=ucnTable["LacUcn"]
                ucnTable.insert(1, "LAC", renamecol)
                ucnTable = ucnTable.reindex(columns=["Reg","site","BSC","TG","BS_name","SW","LAC","RBL2_1","RBL2_2","OETM_1","OETM_2","Sector"])
                newBsTable = pd.concat([newBsTable, ucnTable])
    #14
    oldBsTable["TG"]="0"
    oldBsTable["SW"]="-"
    oldBsTable["RBL2_1"]="-"
    oldBsTable["RBL2_2"]="-"
    oldBsTable["OETM_1"]="-"
    oldBsTable["OETM_2"]="-"
    oldBsTable = oldBsTable.reindex(columns=["Reg","site","BSC","TG","BS_name","SW","LAC","RBL2_1","RBL2_2","OETM_1","OETM_2","Sector"])
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Corrected information (oldBsTable) about Old BS 2G Bulat.\n")
    #8
    resEr2gBulNeop, oldBsTable, newBsTable = writeResults(resEr2gBulNeop, oldBsTable, newBsTable)
    print("General table (resEr2gBulNeop) for Old and New BS sites")
    print(resEr2gBulNeop)    
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (resEr2gBulNeop) about New and Old BS 2G Bulat.\n")
    #9
    resEr2gBulNeop.to_csv("resEr2gBulNeop.csv", sep=',', index=False, header=False, encoding='UTF-8-SIG')
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (resEr2gBulNeop) about New and Old BS 2G Bulat in File.\n")
if checkTable(ces4gErBulNeopTable) == False:
    oldBsTable = pd.DataFrame()
    newBsTable = pd.DataFrame()
    resEr4gBulNeop = pd.DataFrame()
    nameNewBsTable = pd.DataFrame()
    print("- Attention! It is necessary to check the SQL query in the table (ces4gErBulNeopTable):")
    print("Empty table (ces4gErBulNeopTable) 4G Bulat:")
    print(ces4gErBulNeopTable)
    with open("outPyScript.log", "a") as outfile:
        outfile.write("... Empty table (ces4gErBulNeopTable) 4G Bulat.\n")    
    #5
    print("Attention! If there are additional weights, you need to check the filling (joinOldBs4g) for Bulat additional weights.")
    oldBsTable, ces4gErBulNeopTable = joinOldBs4g(oldBsTable, ces4gErBulNeopTable)
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (oldBsTable) about Old BS 4G Bulat.\n")
    #6
    nameNewBsTable, ces4gErBulNeopTable = findNewSites(nameNewBsTable, ces4gErBulNeopTable)
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (nameNewBsTable) about name New BS 4G Bulat.\n")
    #7
    if checkTable(nameNewBsTable) == False:
        rdbTable= pd.DataFrame()
        noUcnTable = pd.DataFrame()
        ucnTable = pd.DataFrame()
        #10       
        rdbTable = parsingRdb(rdbTable)
        with open("outPyScript.log", "a") as outfile:
            outfile.write("+ Added information (rdbTable) about New BS 4G Bulat from site RDB.\n")
        #11
        noUcnTable = pd.concat([rdbTable, noUcnTable])
        noUcnTable = noUcnTable[noUcnTable["UCN"].isin(["-"])]  
        if checkTable(noUcnTable) == False:
            #12
            print("- Attention! It is necessary to check the filling (noUcnTable) of sites for non-UCN! In Bulat, at the time of writing the program, all sites were UCN.")
            with open("outPyScript.log", "a") as outfile:
                outfile.write("- Attention! It is necessary to check the filling (noUcnTable) of sites for non-UCN! In Bulat, at the time of writing the program, all sites were UCN.\n")
        ucnTable = pd.concat([rdbTable, ucnTable])
        ucnTable = ucnTable[ucnTable["UCN"].isin(["УЦН"])]        
        if checkTable(ucnTable) == False:
            #13
            ucnLBRTable = pd.DataFrame()
            ucnLBRTable = templateUcnBul(ucnLBRTable)
            ucnTable = pd.merge(ucnTable, ucnLBRTable, left_on='RegUcn', right_on='RegUcn', how='inner')
            ucnTable = pd.merge(ucnTable, ces4gErBulNeopTable, left_on='index', right_on='BS_name', how='inner')
            if checkTable(newBsTable) == False:
                print("- Attention! It is necessary to take into account the data of (newBsTable, ucnTable, noUcnTable) for sites with non-UCN")
                with open("outPyScript.log", "a") as outfile:
                    outfile.write("- Attention! It is necessary to take into account the data of (newBsTable, ucnTable, noUcnTable) for sites with non-UCN\n")
            else:
                renamecol=ucnTable["LacUcn"]
                ucnTable.insert(1, "LAC", renamecol)
                ucnTable = ucnTable.reindex(columns=["Reg", "site", "LAC", "Sector"])
                newBsTable = pd.concat([newBsTable, ucnTable])
    #14
    oldBsTable = oldBsTable.reindex(columns=["Reg", "site", "LAC", "Sector"])
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Corrected information (oldBsTable) about Old BS 4G Bulat.\n")
    #8
    resEr4gBulNeop, oldBsTable, newBsTable = writeResults(resEr4gBulNeop, oldBsTable, newBsTable)
    print("General table (resEr4gBulNeop) for Old and New BS sites")
    print(resEr4gBulNeop)
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ Added information (resEr4gBulNeop) about New and Old BS 4G Bulat.\n")
    #9
    resEr4gBulNeop.to_csv("resEr4gBulNeop.csv", sep=',', index=False, header=False, encoding='UTF-8-SIG')
if checkTable(ces2gNokTable) == True and checkTable(ces3gNokTable) == True and checkTable(ces4gNokTable) == True and checkTable(ces2gErTable) == True and checkTable(ces3gErTable) == True and checkTable(ces4gErTable) == True and checkTable(ces2gNokBulTable) == True and checkTable(ces4gNokBulTable) == True and checkTable(ces2gErBulTable) == True and checkTable(ces4gErBulTable) == True and checkTable(ces2gErBulNeopTable) == True and checkTable(ces4gErBulNeopTable) == True:
    print("All data on the CES website is filled in.")
    with open("outPyScript.log", "a") as outfile:
        outfile.write("+ All data on the CES website is filled in.\n")
#15
#print(readyList)
readyList = addResultFile(readyList)
#16
#listFiles = importCes(listFiles)