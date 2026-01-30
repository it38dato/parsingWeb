from libs.importKeysJson import funcLoadConfig, CONFIG_FILE_PATH
from libs.importSqlToPandas import funcImportSqlToPandas
from libs.importDataFromSite import funcPowerDrivaer, funcFindAndClickObjectSite, funcFindObjectsSite, funcFindFilterClick2ObjectSite, funcFindFilterClick1ObjectSite, funcClick1ObjectSite, funcClickAlert1ObjectSite, funcFindObjectSite
from libs.jobStings import funcImportStrToList, funcDiffStringsAddList
from libs.jobDf import funcImport2listsToDf, funcGetSuffRenameColDf, funcFindNeighbour, funcJoin2Df, funcGet1DfFrom2Lists, funcJoin3df, funcJoin2Df2
import pandas as pd
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

CONFIG_DATA = funcLoadConfig(CONFIG_FILE_PATH)
print(CONFIG_DATA)

def checkTable(check):
    return check.empty

def funcParsingRdb(browser, filterObjectSite):
    #print(filterObjectSite)

    listTegs, symbol, tegs = funcImportStrToList([], ", ", CONFIG_DATA.get("TEGSSITE1"))
    #print(listTegs)

    browser, tegSearch, tegCandidate, filterObjectSite = funcFindAndClickObjectSite(browser, listTegs[0], listTegs[1], filterObjectSite)

    browser, teg, findTd = funcFindObjectsSite(browser, listTegs[2], [])
    needData1 = findTd[1].text
    needData2 = findTd[13].text
    needData3 = findTd[15].text
    return needData1, needData2, needData3

def funcAddDfTemplateUcn(df):
    dictLac = {"BU":10340, "VV":52412, "IR":5370, "BI":40004, "HB":32106, "ZB":53711, "AM":54500, "YA":57641, "KM":37406, "MD":38718, "SA":38005, "AN":40701}
    dictBsc = {"BU":"-", "VV":"-", "IR":"IRK484", "BI":"BIR067", "HB":"KHB173", "ZB":"PRM140", "AM":"PRM140", "YA":"NSK042", "KM":"KAM070", "MD":"-", "SA":"-", "AN":"-"}
    dictRac = {10340:0, 52412:0, 5370:228, 40004:228, 32106:116, 53711:0, 54500:0, 57641:228, 37406:228, 38718:228, 38005:228, 40701:228}
    dfLac = pd.DataFrame(list(dictLac.items()), columns=["RegUcn", "LAC"])
    dfBsc = pd.DataFrame(list(dictBsc.items()), columns=["RegUcn", "BSC"])
    dfRac = pd.DataFrame(list(dictRac.items()), columns=["LAC", "RAC"])
    ucnLBTable = pd.merge(dfLac, dfBsc, left_on="RegUcn", right_on="RegUcn", how="outer")
    df = pd.merge(ucnLBTable, dfRac, left_on="LAC", right_on="LAC", how="outer") 
    return df
def funcAddDfTemplateUcnBulat(df):
    dictLac = {"BU":10351, "VV":52421, "IR":5381, "BI":40011, "HB":32112, "ZB":53714, "AM":54503, "YA":57644}
    dictBsc = {"IR":"BSCB-IRK525-1", "HB":"BSCB-KHB576-1", "YA":"BSCB-YAK558-1", "AM":"BSCB-BLG514-1", "BI":"BSCB-BIR522-1", "ZB":"BSCB-CHI523-1", "VV":"BSCB-VLD547-1", "BU":"BSCB-BRT551-1"}
    dictRac = {54503:14, 40011:54, 53714:23, 5381:54, 52421:47, 10351:51, 57644:54, 32112:54}
    dfLac = pd.DataFrame(list(dictLac.items()), columns=["RegUcn", "LAC"])
    dfBsc = pd.DataFrame(list(dictBsc.items()), columns=["RegUcn", "BSC"])
    dfRac = pd.DataFrame(list(dictRac.items()), columns=["LAC", "RAC"])
    #dfLac = pd.DataFrame(list(dictLac.items()), columns=['RegUcn', 'LacUcn'])
    #dfBsc = pd.DataFrame(list(dictBsc.items()), columns=['RegUcn', 'BscUcn'])
    #dfRac = pd.DataFrame(list(dictRac.items()), columns=['LacUcn', 'RacUcn'])
    ucnLBTable = pd.merge(dfLac, dfBsc, left_on='RegUcn', right_on='RegUcn', how='outer')
    df = pd.merge(ucnLBTable, dfRac, left_on="LAC", right_on="LAC", how="outer")
    #df = pd.merge(ucnLBTable, dfRac, left_on='LacUcn', right_on='LacUcn', how='outer')
    return df

def funcParsingCes(browser, filterObjectSite):
    #print(filterObjectSite)

    listTegs, symbol, tegs = funcImportStrToList([], ", ", filterObjectSite)
    #print(listTegs)

    browser.maximize_window()

    browser, tegUsername, tegPasswd, click, username, passwd = funcFindFilterClick2ObjectSite(browser, listTegs[0], listTegs[1], listTegs[2], CONFIG_DATA.get("USERSITE2"), CONFIG_DATA.get("PASSWDSITE2"))

    WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, listTegs[3])))

    browser, tegBsslink = funcClick1ObjectSite(browser, listTegs[3])

    browser, tegTecnoklogylink = funcClick1ObjectSite(browser, listTegs[4])

    browser, tegImportlink = funcClickAlert1ObjectSite(browser, listTegs[5])
    #print(file)
    #print(os.getcwd()+"\\"+file)
    browser, tegPublicationFile, click, filterFile = funcFindFilterClick1ObjectSite(browser, listTegs[6], listTegs[2], os.getcwd()+"\\"+file)
    time.sleep(5)

    browser, tegClass, findHtmlMessage = funcFindObjectSite(browser, listTegs[7], "")

    if ("Файл для импорта должен быть" in str(findHtmlMessage[0])) or ("Файл CSV неверной кодировки" in str(findHtmlMessage[0])) or ("Недопустимы разные" in str(findHtmlMessage[0])):
        print("- Attention! The file "+file+" for import does not match.")
    if "Импорт выполнен" in str(findHtmlMessage[0]):
        if "КРОМЕ" in str(findHtmlMessage[0]):
            print("- Attention! The import "+file+" is complete, but partially. Some fields are already filled in.")
        else:
            print("+ Import file "+file+" completed successfully.")
    return

def funcCorrectCols2gNok(dfResult):
    dfResult["BCF"] = dfResult["BCF"].astype("int64")
    dfResult["SW"] = "MR10"
    dfResult = dfResult.reindex(columns=["Reg", "Sector", "SW", "BSC", "BCF", "LAC", "RAC"])
    return dfResult
def funcCorrectCols4gNok(dfResult):
    if "BS_name_x" in dfResult:
        dfResult.insert(1, "BS_name", dfResult["BS_name_x"])
    dfResult = dfResult.reindex(columns=["Reg", "BS_name", "Sector", "LAC"])
    return dfResult
def funcCorrectCols2gEr(dfResult):
    #dfResult.insert(1, "BS_name", dfResult["BS_name_x"])
    if "BS_name_x" in dfResult:
        dfResult.insert(1, "BS_name", dfResult["BS_name_x"])
    dfResult["TG"] = "0"
    dfResult["SW"] = "-"
    dfResult["RBL2_1"] = "-"
    dfResult["RBL2_2"] = "-"
    dfResult["OETM_1"] = "-"
    dfResult["OETM_2"] = "-"
    if ("BscUcn" in dfResult) and ("LacUcn" in dfResult):
        dfResult.insert(1, "BSC", dfUcn["BscUcn"])
        dfResult.insert(1, "LAC", dfUcn["LacUcn"])
    dfResult = dfResult.reindex(columns=["Reg", "site", "BSC", "TG", "BS_name", "SW", "LAC", "RBL2_1", "RBL2_2", "OETM_1", "OETM_2","Sector"])
    return dfResult
def funcCorrectCols3gEr(dfResult):
    dfResult = dfResult.reindex(columns=["Reg", "site", "RNC_ID", "URA", "LAC", "RAC", "RRU", "Sector"])
    return dfResult
def funcCorrectCols4gEr(dfResult):
    dfResult = dfResult.reindex(columns=["Reg", "site", "LAC", "Sector"])
    return dfResult

df2gNok, dbIp, dbUser, dbPasswd, dbName, dbTable, dbCondition, dbFilter = funcImportSqlToPandas(
    pd.DataFrame(), 
    CONFIG_DATA.get("IPDB1"), 
    CONFIG_DATA.get("USERDB1"), 
    CONFIG_DATA.get("PASSWDB1"), 
    CONFIG_DATA.get("DB1"), 
    CONFIG_DATA.get("TABLE1"), 
    CONFIG_DATA.get("CONDITION1"),
    CONFIG_DATA.get("FILTER1")
    )
#print(df2gNok)

df3gNok, dbIp, dbUser, dbPasswd, dbName, dbTable, dbCondition, dbFilter = funcImportSqlToPandas(
    pd.DataFrame(), 
    CONFIG_DATA.get("IPDB1"), 
    CONFIG_DATA.get("USERDB1"), 
    CONFIG_DATA.get("PASSWDB1"), 
    CONFIG_DATA.get("DB1"), 
    CONFIG_DATA.get("TABLE4"), 
    CONFIG_DATA.get("CONDITION1"),
    CONFIG_DATA.get("FILTER4")
    )
#print(df3gNok)

df4gNok, dbIp, dbUser, dbPasswd, dbName, dbTable, dbCondition, dbFilter = funcImportSqlToPandas(
    pd.DataFrame(), 
    CONFIG_DATA.get("IPDB1"), 
    CONFIG_DATA.get("USERDB1"), 
    CONFIG_DATA.get("PASSWDB1"), 
    CONFIG_DATA.get("DB1"), 
    CONFIG_DATA.get("TABLE5"), 
    CONFIG_DATA.get("CONDITION1"),
    CONFIG_DATA.get("FILTER5")
    )
#print(df4gNok)

df2gNokBul, dbIp, dbUser, dbPasswd, dbName, dbTable, dbCondition, dbFilter = funcImportSqlToPandas(
    pd.DataFrame(), 
    CONFIG_DATA.get("IPDB1"), 
    CONFIG_DATA.get("USERDB1"), 
    CONFIG_DATA.get("PASSWDB1"), 
    CONFIG_DATA.get("DB1"), 
    CONFIG_DATA.get("TABLE9"), 
    CONFIG_DATA.get("CONDITION1"),
    CONFIG_DATA.get("FILTER9")
    )
#print(df2gNokBul)

df4gNokBul, dbIp, dbUser, dbPasswd, dbName, dbTable, dbCondition, dbFilter = funcImportSqlToPandas(
    pd.DataFrame(), 
    CONFIG_DATA.get("IPDB1"), 
    CONFIG_DATA.get("USERDB1"), 
    CONFIG_DATA.get("PASSWDB1"), 
    CONFIG_DATA.get("DB1"), 
    CONFIG_DATA.get("TABLE8"), 
    CONFIG_DATA.get("CONDITION1"),
    CONFIG_DATA.get("FILTER8")
    )
#print(df4gNokBul)

df2gEr, dbIp, dbUser, dbPasswd, dbName, dbTable, dbCondition, dbFilter = funcImportSqlToPandas(
    pd.DataFrame(), 
    CONFIG_DATA.get("IPDB2"), 
    CONFIG_DATA.get("USERDB2"), 
    CONFIG_DATA.get("PASSWDB2"), 
    CONFIG_DATA.get("DB4"), 
    CONFIG_DATA.get("TABLE10"), 
    CONFIG_DATA.get("CONDITION5"),
    CONFIG_DATA.get("FILTER10")
    )
#print(df2gEr)

df3gEr, dbIp, dbUser, dbPasswd, dbName, dbTable, dbCondition, dbFilter = funcImportSqlToPandas(
    pd.DataFrame(), 
    CONFIG_DATA.get("IPDB2"), 
    CONFIG_DATA.get("USERDB2"), 
    CONFIG_DATA.get("PASSWDB2"), 
    CONFIG_DATA.get("DB4"), 
    CONFIG_DATA.get("TABLE11"), 
    CONFIG_DATA.get("CONDITION5"),
    CONFIG_DATA.get("FILTER11")
    )
#print(df3gEr)

df4gEr, dbIp, dbUser, dbPasswd, dbName, dbTable, dbCondition, dbFilter = funcImportSqlToPandas(
    pd.DataFrame(), 
    CONFIG_DATA.get("IPDB2"), 
    CONFIG_DATA.get("USERDB2"), 
    CONFIG_DATA.get("PASSWDB2"), 
    CONFIG_DATA.get("DB4"), 
    CONFIG_DATA.get("TABLE12"), 
    CONFIG_DATA.get("CONDITION5"),
    CONFIG_DATA.get("FILTER12")
    )
#print(df4gEr)

df2gErBul, dbIp, dbUser, dbPasswd, dbName, dbTable, dbCondition, dbFilter = funcImportSqlToPandas(
    pd.DataFrame(), 
    CONFIG_DATA.get("IPDB2"), 
    CONFIG_DATA.get("USERDB2"), 
    CONFIG_DATA.get("PASSWDB2"), 
    CONFIG_DATA.get("DB4"), 
    CONFIG_DATA.get("TABLE13"), 
    CONFIG_DATA.get("CONDITION5"),
    CONFIG_DATA.get("FILTER13")
    )
#print(df2gErBul)

df4gErBul, dbIp, dbUser, dbPasswd, dbName, dbTable, dbCondition, dbFilter = funcImportSqlToPandas(
    pd.DataFrame(), 
    CONFIG_DATA.get("IPDB2"), 
    CONFIG_DATA.get("USERDB2"), 
    CONFIG_DATA.get("PASSWDB2"), 
    CONFIG_DATA.get("DB4"), 
    CONFIG_DATA.get("TABLE14"), 
    CONFIG_DATA.get("CONDITION5"),
    CONFIG_DATA.get("FILTER14")
    )
#print(df4gErBul)

df2gErBulNeop, dbIp, dbUser, dbPasswd, dbName, dbTable, dbCondition, dbFilter = funcImportSqlToPandas(
    pd.DataFrame(), 
    CONFIG_DATA.get("IPDB2"), 
    CONFIG_DATA.get("USERDB2"), 
    CONFIG_DATA.get("PASSWDB2"), 
    CONFIG_DATA.get("DB4"), 
    CONFIG_DATA.get("TABLE15"), 
    CONFIG_DATA.get("CONDITION5"),
    CONFIG_DATA.get("FILTER15")
    )
#print(df2gErBulNeop)

df4gErBulNeop, dbIp, dbUser, dbPasswd, dbName, dbTable, dbCondition, dbFilter = funcImportSqlToPandas(
    pd.DataFrame(), 
    CONFIG_DATA.get("IPDB2"), 
    CONFIG_DATA.get("USERDB2"), 
    CONFIG_DATA.get("PASSWDB2"), 
    CONFIG_DATA.get("DB4"), 
    CONFIG_DATA.get("TABLE16"), 
    CONFIG_DATA.get("CONDITION5"),
    CONFIG_DATA.get("FILTER16")
    )
#print(df4gErBulNeop)

listNameNewBs = []
listReady = []
listData = []
#===================================TEST!
#df2gNok["Reg"] = ["IR", "IR"]
#df2gNok["BS_name"] =["IO0265", "IR1159"]
#df2gNok["BCF"] = ["0265", "1159"]
#df2gNok["Sector"] = ["IO02651", "IR11592"]
#===================================TEST!

if checkTable(df2gNok) == False:
    print("Empty table (df2gNok):")
    print(df2gNok)

    dfDaily, dbIp, dbUser, dbPasswd, dbName, dbTable, dbCondition, dbFilter = funcImportSqlToPandas(
        pd.DataFrame(), 
        CONFIG_DATA.get("IPDB1"), 
        CONFIG_DATA.get("USERDB1"), 
        CONFIG_DATA.get("PASSWDB1"), 
        CONFIG_DATA.get("DB2"), 
        CONFIG_DATA.get("TABLE2"), 
        CONFIG_DATA.get("CONDITION2"),
        CONFIG_DATA.get("FILTER2")
        )
    #print(dfDaily)

    dfOld = pd.merge(df2gNok, dfDaily, left_on="BS_name", right_on="BS_name", how="inner")    
    #print(dfOld)

    '''listTech = df2gNok["BS_name"].tolist()
    listTech = list(dict.fromkeys(listTech))
    listTechOld = dfOld["BS_name"].tolist()
    listTechOld = list(dict.fromkeys(listTechOld))
    for name in listTech:
        if name in listTechOld:
            continue
        else:
            listNameNewBs.append(name)
    #===================================TEST!
    #listNameNewBs.append("IO0265")
    #listNameNewBs.append("IR0045")
    #===================================TEST!
    dfNameNewBs = pd.DataFrame(listNameNewBs, columns=["nameNew"])'''
    dfNameNewBs, df2gNok, dfOld, listNameNewBs, str2gNokCol, strOldCol = funcGet1DfFrom2Lists(
        pd.DataFrame(), df2gNok, dfOld, listNameNewBs,
        "BS_name", "BS_name"
    )
    #print(dfNameNewBs)

    dfNew = pd.DataFrame()
    if checkTable(dfNameNewBs) == False:
        dataNewSites = dict()
        numb=0
        for name in listNameNewBs:
            if name in listReady:
                #print(str(numb)+". The site "+name+" already read")
                continue
            else:
                numb=numb+1
                #print(str(numb)+". The site "+name+" is being read:")                
                
                findUcn, findLatitude, findLongitude  = funcPowerDrivaer(
                    driver_path = CONFIG_DATA.get("LINKPO1"),
                    binary_path = CONFIG_DATA.get("LINKPO2"),
                    url = CONFIG_DATA.get("LINKSITE1"),
                    action_func = funcParsingRdb,
                    filterObjectSite = name[:2] + "00"+ name[2:6]
                )
                #print(findUcn)
                #print(findLatitude)
                #print(findLongitude)

                findUcn, listData, symbol, addSymbol1, addSymbol2 = funcDiffStringsAddList(
                    findUcn, listData,
                    "УЦН", "УЦН", "-"
                )

                listData.append(findLatitude.replace(',', '.'))
                listData.append(findLongitude.replace(',', '.')) 
                listReady.append(name)

        #print(listData)
        #print(listReady)
        listData, listReady, dfRdb, dataNewSites, cols = funcImport2listsToDf(
            listData, listReady, pd.DataFrame(), dataNewSites,
            ["UCN", "latitudeX1", "longitudeY1"]
        )
        #print(dfRdb)

        dfRdb, fromCol, toCol, fromRenameSymbol, toRenameSymbol, numbCol = funcGetSuffRenameColDf(
            dfRdb,
            "index", "RegUcn", "IO", "IR", 2
        )
        #print(dfRdb)

        dfCoords, dbIp, dbUser, dbPasswd, dbName, dbTable, dbCondition, dbFilter = funcImportSqlToPandas(
            pd.DataFrame(),
            CONFIG_DATA.get("IPDB1"),
            CONFIG_DATA.get("USERDB1"),
            CONFIG_DATA.get("PASSWDB1"),
            CONFIG_DATA.get("DB3"),
            CONFIG_DATA.get("TABLE3"),
            CONFIG_DATA.get("CONDITION3"),
            CONFIG_DATA.get("FILTER3")
        )
        #print(dfCoords)
        dfDaily = pd.merge(dfDaily, dfCoords, left_on="BS_name", right_on="BS_name", how="inner")
        #print(dfDaily)
        dfUcnTemplate = funcAddDfTemplateUcn(pd.DataFrame())
        #print(dfUcnTemplate)

        dfNoUcn = pd.DataFrame()
        dfNoUcn = pd.concat([dfRdb, dfNoUcn])
        dfNoUcn = dfNoUcn[dfNoUcn["UCN"].isin(["-"])]
        if checkTable(dfNoUcn) == False:
            '''dfNoUcn = pd.merge(dfNoUcn, df2gNok, left_on="index", right_on="BS_name", how="inner")
            dfNeighbour = dfNoUcn.merge(dfDaily, how="cross")'''
            dfNeighbour, dfNoUcn, df2gNok, dfDaily, strNoUcn, str2gNok = funcJoin3df(
                pd.DataFrame(), dfNoUcn, df2gNok, dfDaily,
                "index", "BS_name"
            )
            dfNoUcn = funcFindNeighbour(dfNeighbour)

            '''dfNoUcn["BCF"] = dfNoUcn["BCF"].astype("int64")
            dfNoUcn["SW"] = "MR10"
            dfNoUcn = dfNoUcn.reindex(columns=["Reg", "Sector", "SW", "BSC", "BCF", "LAC", "RAC"])'''
            dfNoUcn = funcCorrectCols2gNok(dfNoUcn)
            dfNew = pd.concat([dfNew, dfNoUcn])
        #print(dfNoUcn)

        dfUcn = pd.DataFrame()
        dfUcn = pd.concat([dfRdb, dfUcn])
        dfUcn = dfUcn[dfUcn["UCN"].isin(["УЦН"])]
        if checkTable(dfUcn) == False:
            '''dfUcn = pd.merge(dfUcn, df2gNok, left_on="index", right_on="BS_name", how="inner")
            dfUcn = pd.merge(dfUcn, dfUcnTemplate, left_on="RegUcn", right_on="RegUcn", how="inner")'''
            dfUcn, df2gNok, dfUcnTemplate, strUcn1, strUcn2, str2gNok, strUcnTemplate  = funcJoin2Df2(
                dfUcn, df2gNok, dfUcnTemplate,
                "index", "RegUcn", "BS_name", "RegUcn"
            )
            #print(dfUcn)

            '''dfUcn["BCF"] = dfUcn["BCF"].astype("int64")
            dfUcn["SW"]="MR10"
            dfUcn = dfUcn.reindex(columns=["Reg", "Sector", "SW", "BSC", "BCF", "LAC", "RAC"])'''
            dfUcn = funcCorrectCols2gNok(dfUcn)
            dfNew = pd.concat([dfNew, dfUcn])
        #print(dfUcn)
    #print(dfNew)

    '''dfOld["SW"]="MR10"
    dfOld["BCF"]=dfOld["BCF"].astype("int64")
    dfOld = dfOld.reindex(columns=["Reg", "Sector", "SW", "BSC", "BCF", "LAC", "RAC"])'''
    dfOld = funcCorrectCols2gNok(dfOld)
    #print(dfOld)

    df2gNok, dfOld, dfNew = funcJoin2Df(
        pd.DataFrame(), dfOld, dfNew
    )
    print("Data ready (df2gNok)")
    print(df2gNok)
    df2gNok.to_csv("df2gNok.csv", sep=";", index=False, header=False, encoding="UTF-8-SIG")

    listFiles = os.listdir()
    #print(listFiles)
    for file in listFiles:
        if "df2gNok." in file:
            #print(file)
            dataFromSite  = funcPowerDrivaer(
                driver_path = CONFIG_DATA.get("LINKPO1"),
                binary_path = CONFIG_DATA.get("LINKPO2"),
                url = CONFIG_DATA.get("LINKSITE2"),
                action_func = funcParsingCes,
                filterObjectSite = CONFIG_DATA.get("TEGSSITE2")
            )
            #print(dataFromSite)
            print("+ Add Data (df2gNok) to site CES")
if checkTable(df2gNokBul) == False:
    print("Empty table (df2gNokBul):")
    print(df2gNokBul)

    dfDaily, dbIp, dbUser, dbPasswd, dbName, dbTable, dbCondition, dbFilter = funcImportSqlToPandas(
        pd.DataFrame(),
        CONFIG_DATA.get("IPDB1"),
        CONFIG_DATA.get("USERDB1"),
        CONFIG_DATA.get("PASSWDB1"),
        CONFIG_DATA.get("DB2"),
        CONFIG_DATA.get("TABLE2"),
        CONFIG_DATA.get("CONDITION2"),
        CONFIG_DATA.get("FILTER2")
        )
    #print(dfDaily)

    dfOld = pd.merge(df2gNokBul, dfDaily, left_on="BS_name", right_on="BS_name", how="inner")
    #print(dfOld)

    dfNameNewBs, df2gNokBul, dfOld, listNameNewBs, str2gNokBulCol, strOldCol = funcGet1DfFrom2Lists(
        pd.DataFrame(), df2gNokBul, dfOld, listNameNewBs,
        "BS_name", "BS_name"
    )
    #print(dfNameNewBs)

    dfNew = pd.DataFrame()
    if checkTable(dfNameNewBs) == False:
        dataNewSites = dict()
        numb = 0
        for name in listNameNewBs:
            if name in listReady:
                # print(str(numb)+". The site "+name+" already read")
                continue
            else:
                numb = numb + 1
                # print(str(numb)+". The site "+name+" is being read:")

                findUcn, findLatitude, findLongitude = funcPowerDrivaer(
                    driver_path=CONFIG_DATA.get("LINKPO1"),
                    binary_path=CONFIG_DATA.get("LINKPO2"),
                    url=CONFIG_DATA.get("LINKSITE1"),
                    action_func=funcParsingRdb,
                    filterObjectSite=name[:2] + "00" + name[2:6]
                )
                # print(findUcn)
                # print(findLatitude)
                # print(findLongitude)

                findUcn, listData, symbol, addSymbol1, addSymbol2 = funcDiffStringsAddList(
                    findUcn, listData,
                    "УЦН", "УЦН", "-"
                )

                listData.append(findLatitude.replace(',', '.'))
                listData.append(findLongitude.replace(',', '.'))
                listReady.append(name)

        # print(listData)
        # print(listReady)
        listData, listReady, dfRdb, dataNewSites, cols = funcImport2listsToDf(
            listData, listReady, pd.DataFrame(), dataNewSites,
            ["UCN", "latitudeX1", "longitudeY1"]
        )
        # print(dfRdb)

        dfRdb, fromCol, toCol, fromRenameSymbol, toRenameSymbol, numbCol = funcGetSuffRenameColDf(
            dfRdb,
            "index", "RegUcn", "IO", "IR", 2
        )
        # print(dfRdb)

        dfCoords, dbIp, dbUser, dbPasswd, dbName, dbTable, dbCondition, dbFilter = funcImportSqlToPandas(
            pd.DataFrame(),
            CONFIG_DATA.get("IPDB1"),
            CONFIG_DATA.get("USERDB1"),
            CONFIG_DATA.get("PASSWDB1"),
            CONFIG_DATA.get("DB3"),
            CONFIG_DATA.get("TABLE3"),
            CONFIG_DATA.get("CONDITION3"),
            CONFIG_DATA.get("FILTER3")
        )
        # print(dfCoords)
        dfDaily = pd.merge(dfDaily, dfCoords, left_on="BS_name", right_on="BS_name", how="inner")
        # print(dfDaily)
        dfUcnTemplate = funcAddDfTemplateUcnBulat(pd.DataFrame())
        # print(dfUcnTemplate)

        dfNoUcn = pd.DataFrame()
        dfNoUcn = pd.concat([dfRdb, dfNoUcn])
        dfNoUcn = dfNoUcn[dfNoUcn["UCN"].isin(["-"])]
        if checkTable(dfNoUcn) == False:
            print("Внимание! Еще не было данных не УЦН по булату. необходимо проверить код ниже.")
            dfNeighbour, dfNoUcn, df2gNokBul, dfDaily, strNoUcn, str2gNokBul = funcJoin3df(
                pd.DataFrame(), dfNoUcn, df2gNokBul, dfDaily,
                "index", "BS_name"
            )
            dfNoUcn = funcFindNeighbour(dfNeighbour)

            dfNoUcn = funcCorrectCols2gNok(dfNoUcn)
            dfNew = pd.concat([dfNew, dfNoUcn])
        # print(dfNoUcn)

        dfUcn = pd.DataFrame()
        dfUcn = pd.concat([dfRdb, dfUcn])
        dfUcn = dfUcn[dfUcn["UCN"].isin(["УЦН"])]
        if checkTable(dfUcn) == False:
            print("Внимание! В Булате отображается названия таблица не как в нокиа - LAC, RAC. Я заменил парамеетры в функции (funcAddDfTemplateUcnBulat) название колонок, но лучше перероверить.")
            dfUcn, df2gNokBul, dfUcnTemplate, strUcn1, strUcn2, str2gNokBul, strUcnTemplate = funcJoin2Df2(
                dfUcn, df2gNokBul, dfUcnTemplate,
                "index", "RegUcn", "BS_name", "RegUcn"
            )
            # print(dfUcn)

            dfUcn = funcCorrectCols2gNok(dfUcn)
            dfNew = pd.concat([dfNew, dfUcn])
        # print(dfUcn)
    # print(dfNew)
    dfOld = funcCorrectCols2gNok(dfOld)
    #print(dfOld)

    df2gNokBul, dfOld, dfNew = funcJoin2Df(
        pd.DataFrame(), dfOld, dfNew
    )
    print("Data ready (df2gNokBul)")
    print(df2gNokBul)
    df2gNokBul.to_csv("df2gNokBul.csv", sep=";", index=False, header=False, encoding="UTF-8-SIG")

    listFiles = os.listdir()
    #print(listFiles)
    for file in listFiles:
        if "df2gNokBul." in file:
            #print(file)
            dataFromSite  = funcPowerDrivaer(
                driver_path = CONFIG_DATA.get("LINKPO1"),
                binary_path = CONFIG_DATA.get("LINKPO2"),
                url = CONFIG_DATA.get("LINKSITE2"),
                action_func = funcParsingCes,
                filterObjectSite = CONFIG_DATA.get("TEGSSITE2")
            )
            #print(dataFromSite)
            print("+ Add Data (df2gNokBul) to site CES")
if checkTable(df3gNok) == False:
    print("Empty table (df3gNok):")
    print(df3gNok)

    dfDaily, dbIp, dbUser, dbPasswd, dbName, dbTable, dbCondition, dbFilter = funcImportSqlToPandas(
        pd.DataFrame(), 
        CONFIG_DATA.get("IPDB1"), 
        CONFIG_DATA.get("USERDB1"), 
        CONFIG_DATA.get("PASSWDB1"), 
        CONFIG_DATA.get("DB2"), 
        CONFIG_DATA.get("TABLE6"), 
        CONFIG_DATA.get("CONDITION4"),
        CONFIG_DATA.get("FILTER6")
        )
    print(dfDaily)
if checkTable(df4gNok) == False:
    print("Empty table (df4gNok):")
    print(df4gNok)

    dfDaily, dbIp, dbUser, dbPasswd, dbName, dbTable, dbCondition, dbFilter = funcImportSqlToPandas(
        pd.DataFrame(), 
        CONFIG_DATA.get("IPDB1"), 
        CONFIG_DATA.get("USERDB1"), 
        CONFIG_DATA.get("PASSWDB1"), 
        CONFIG_DATA.get("DB2"), 
        CONFIG_DATA.get("TABLE7"), 
        CONFIG_DATA.get("CONDITION2"),
        CONFIG_DATA.get("FILTER7")
        )
    #print(dfDaily)
    dfOld = pd.merge(df4gNok, dfDaily, left_on="BS_name", right_on="BS_name", how="inner")    
    #print(dfOld)

    '''listTech = df4gNok["BS_name"].tolist()
    listTech = list(dict.fromkeys(listTech))
    listTechOld = dfOld["BS_name"].tolist()
    listTechOld = list(dict.fromkeys(listTechOld))
    for name in listTech:
        if name in listTechOld:
            continue
        else:
            listNameNewBs.append(name)
    dfNameNewBs = pd.DataFrame(listNameNewBs, columns=["nameNew"])'''
    dfNameNewBs, df4gNok, dfOld, listNameNewBs, str4gNokCol, strOldCol = funcGet1DfFrom2Lists(
        pd.DataFrame(), df4gNok, dfOld, listNameNewBs,
        "BS_name", "BS_name"
    )
    #print(dfNameNewBs)

    dfNew = pd.DataFrame()
    if checkTable(dfNameNewBs) == False:
        dataNewSites = dict()
        numb=0
        for name in listNameNewBs:
            if name in listReady:
                #print(str(numb)+". The site "+name+" already read")
                continue
            else:
                numb=numb+1
                #print(str(numb)+". The site "+name+" is being read:")                
                
                findUcn, findLatitude, findLongitude  = funcPowerDrivaer(
                    driver_path = CONFIG_DATA.get("LINKPO1"),
                    binary_path = CONFIG_DATA.get("LINKPO2"),
                    url = CONFIG_DATA.get("LINKSITE1"),
                    action_func = funcParsingRdb,
                    filterObjectSite = name[:2] + "00"+ name[2:6]
                )
                #print(findUcn)
                #print(findLatitude)
                #print(findLongitude)

                findUcn, listData, symbol, addSymbol1, addSymbol2 = funcDiffStringsAddList(
                    findUcn, listData,
                    "УЦН", "УЦН", "-"
                )

                listData.append(findLatitude.replace(',', '.'))
                listData.append(findLongitude.replace(',', '.')) 
                listReady.append(name)
        #print(listData)
        #print(listReady)

        listData, listReady, dfRdb, dataNewSites, cols = funcImport2listsToDf(
            listData, listReady, pd.DataFrame(), dataNewSites,
            ["UCN", "latitudeX1", "longitudeY1"]
        )
        #print(dfRdb)
        dfRdb, fromCol, toCol, fromRenameSymbol, toRenameSymbol, numbCol = funcGetSuffRenameColDf(
            dfRdb,
            "index", "RegUcn", "IO", "IR", 2
        )
        #print(dfRdb)

        dfCoords, dbIp, dbUser, dbPasswd, dbName, dbTable, dbCondition, dbFilter = funcImportSqlToPandas(
            pd.DataFrame(),
            CONFIG_DATA.get("IPDB1"),
            CONFIG_DATA.get("USERDB1"),
            CONFIG_DATA.get("PASSWDB1"),
            CONFIG_DATA.get("DB3"),
            CONFIG_DATA.get("TABLE3"),
            CONFIG_DATA.get("CONDITION3"),
            CONFIG_DATA.get("FILTER3")
        )
        #print(dfCoords)
        dfDaily = pd.merge(dfDaily, dfCoords, left_on="BS_name", right_on="BS_name", how="inner")
        #print(dfDaily)
        dfUcnTemplate = funcAddDfTemplateUcn(pd.DataFrame())
        #print(dfUcnTemplate)

        dfNoUcn = pd.DataFrame()
        dfNoUcn = pd.concat([dfRdb, dfNoUcn])
        dfNoUcn = dfNoUcn[dfNoUcn["UCN"].isin(["-"])]
        if checkTable(dfNoUcn) == False:
            '''dfNoUcn = pd.merge(dfNoUcn, df4gNok, left_on="index", right_on="BS_name", how="inner")
            dfNeighbour = dfNoUcn.merge(dfDaily, how="cross")'''
            dfNeighbour, dfNoUcn, df4gNok, dfDaily, strNoUcn, str4gNok = funcJoin3df(
                pd.DataFrame(), dfNoUcn, df4gNok, dfDaily,
                "index", "BS_name"
            )
            dfNoUcn = funcFindNeighbour(dfNeighbour)
            # print(dfNoUcn)

            '''dfNoUcn.insert(1, "BS_name", dfNoUcn["BS_name_x"])
            dfNoUcn = dfNoUcn.reindex(columns=["Reg", "BS_name", "Sector", "LAC"])'''
            dfNoUcn = funcCorrectCols4gNok(dfNoUcn)
            dfNew = pd.concat([dfNew, dfNoUcn])
        # print(dfNoUcn)

        dfUcn = pd.DataFrame()
        dfUcn = pd.concat([dfRdb, dfUcn])
        dfUcn = dfUcn[dfUcn["UCN"].isin(["УЦН"])]
        if checkTable(dfUcn) == False:
            print("Внимание! необходимо проверить заполнение данных таблицы dfUcn.")
            '''dfUcn = pd.merge(dfUcn, df4gNok, left_on="index", right_on="BS_name", how="inner")
            dfUcn = pd.merge(dfUcn, dfUcnTemplate, left_on="RegUcn", right_on="RegUcn", how="inner")'''
            dfUcn, df4gNok, dfUcnTemplate, strUcn1, strUcn2, str4gNok, strUcnTemplate  = funcJoin2Df2(
                dfUcn, df4gNok, dfUcnTemplate,
                "index", "RegUcn", "BS_name", "RegUcn"
            )
            #print(dfUcn)

            '''dfUcn.insert(1, "BS_name", dfNoUcn["BS_name_x"])
            dfUcn = dfUcn.reindex(columns=["Reg", "BS_name", "Sector", "LAC"])'''
            dfUcn = funcCorrectCols4gNok(dfUcn)
            dfNew = pd.concat([dfNew, dfUcn])
        #print(dfUcn)
    #print(dfNew)

    #dfOld = dfOld.reindex(columns=["Reg", "BS_name", "Sector", "LAC"])
    dfOld = funcCorrectCols4gNok(dfOld)
    #print(dfOld)

    df4gNok, dfOld, dfNew = funcJoin2Df(pd.DataFrame(), dfOld, dfNew)
    print("Data ready (df4gNok)")
    print(df4gNok)

    df4gNok.to_csv("df4gNok.csv", sep=";", index=False, header=False, encoding="UTF-8-SIG")

    listFiles = os.listdir()
    #print(listFiles)
    for file in listFiles:
        if "df4gNok." in file:
            #print(file)
            dataFromSite  = funcPowerDrivaer(
                driver_path = CONFIG_DATA.get("LINKPO1"),
                binary_path = CONFIG_DATA.get("LINKPO2"),
                url = CONFIG_DATA.get("LINKSITE2"),
                action_func = funcParsingCes,
                #filterObjectSite = ""
                filterObjectSite = CONFIG_DATA.get("TEGSSITE3")
            )
            #print(dataFromSite)
            print("+ Add Data (df4gNok) to site CES")
if checkTable(df4gNokBul) == False:
    print("Empty table (df4gNokBul):")
    print(df4gNokBul)

    dfDaily, dbIp, dbUser, dbPasswd, dbName, dbTable, dbCondition, dbFilter = funcImportSqlToPandas(
        pd.DataFrame(), 
        CONFIG_DATA.get("IPDB1"), 
        CONFIG_DATA.get("USERDB1"), 
        CONFIG_DATA.get("PASSWDB1"), 
        CONFIG_DATA.get("DB2"), 
        CONFIG_DATA.get("TABLE7"), 
        CONFIG_DATA.get("CONDITION2"),
        CONFIG_DATA.get("FILTER7")
        )
    #print(dfDaily)
    dfOld = pd.merge(df4gNokBul, dfDaily, left_on="BS_name", right_on="BS_name", how="inner")
    #print(dfOld)

    dfNameNewBs, df4gNokBul, dfOld, listNameNewBs, str4gNokBulCol, strOldCol = funcGet1DfFrom2Lists(
        pd.DataFrame(), df4gNokBul, dfOld, listNameNewBs,
        "BS_name", "BS_name"
    )
    #print(dfNameNewBs)

    dfNew = pd.DataFrame()
    if checkTable(dfNameNewBs) == False:
        dataNewSites = dict()
        numb = 0
        for name in listNameNewBs:
            if name in listReady:
                # print(str(numb)+". The site "+name+" already read")
                continue
            else:
                numb = numb + 1
                # print(str(numb)+". The site "+name+" is being read:")

                findUcn, findLatitude, findLongitude = funcPowerDrivaer(
                    driver_path=CONFIG_DATA.get("LINKPO1"),
                    binary_path=CONFIG_DATA.get("LINKPO2"),
                    url=CONFIG_DATA.get("LINKSITE1"),
                    action_func=funcParsingRdb,
                    filterObjectSite=name[:2] + "00" + name[2:6]
                )
                # print(findUcn)
                # print(findLatitude)
                # print(findLongitude)

                findUcn, listData, symbol, addSymbol1, addSymbol2 = funcDiffStringsAddList(
                    findUcn, listData,
                    "УЦН", "УЦН", "-"
                )

                listData.append(findLatitude.replace(',', '.'))
                listData.append(findLongitude.replace(',', '.'))
                listReady.append(name)
        # print(listData)
        # print(listReady)

        listData, listReady, dfRdb, dataNewSites, cols = funcImport2listsToDf(
            listData, listReady, pd.DataFrame(), dataNewSites,
            ["UCN", "latitudeX1", "longitudeY1"]
        )
        # print(dfRdb)
        dfRdb, fromCol, toCol, fromRenameSymbol, toRenameSymbol, numbCol = funcGetSuffRenameColDf(
            dfRdb,
            "index", "RegUcn", "IO", "IR", 2
        )
        # print(dfRdb)
        dfCoords, dbIp, dbUser, dbPasswd, dbName, dbTable, dbCondition, dbFilter = funcImportSqlToPandas(
            pd.DataFrame(),
            CONFIG_DATA.get("IPDB1"),
            CONFIG_DATA.get("USERDB1"),
            CONFIG_DATA.get("PASSWDB1"),
            CONFIG_DATA.get("DB3"),
            CONFIG_DATA.get("TABLE3"),
            CONFIG_DATA.get("CONDITION3"),
            CONFIG_DATA.get("FILTER3")
        )
        #print(dfCoords)
        dfDaily = pd.merge(dfDaily, dfCoords, left_on="BS_name", right_on="BS_name", how="inner")
        #print(dfDaily)
        dfUcnTemplate = funcAddDfTemplateUcnBulat(pd.DataFrame())
        #print(dfUcnTemplate)

        dfNoUcn = pd.DataFrame()
        dfNoUcn = pd.concat([dfRdb, dfNoUcn])
        dfNoUcn = dfNoUcn[dfNoUcn["UCN"].isin(["-"])]
        if checkTable(dfNoUcn) == False:

            dfNeighbour, dfNoUcn, df4gNokBul, dfDaily, strNoUcn, str4gNokBul = funcJoin3df(
                pd.DataFrame(), dfNoUcn, df4gNokBul, dfDaily,
                "index", "BS_name"
            )
            dfNoUcn = funcFindNeighbour(dfNeighbour)
            # print(dfNoUcn)

            dfNoUcn = funcCorrectCols4gNok(dfNoUcn)
            dfNew = pd.concat([dfNew, dfNoUcn])
        # print(dfNoUcn)

        dfUcn = pd.DataFrame()
        dfUcn = pd.concat([dfRdb, dfUcn])
        dfUcn = dfUcn[dfUcn["UCN"].isin(["УЦН"])]
        if checkTable(dfUcn) == False:
            print("Внимание! необходимо проверить заполнение данных таблицы dfUcn.")
            dfUcn, df4gNokBul, dfUcnTemplate, strUcn1, strUcn2, str4gNokBul, strUcnTemplate  = funcJoin2Df2(
                dfUcn, df4gNokBul, dfUcnTemplate,
                "index", "RegUcn", "BS_name", "RegUcn"
            )
            #print(dfUcn)

            dfUcn = funcCorrectCols4gNok(dfUcn)
            dfNew = pd.concat([dfNew, dfUcn])
        #print(dfUcn)
    #print(dfNew)

    dfOld = funcCorrectCols4gNok(dfOld)
    #print(dfOld)

    df4gNokBul, dfOld, dfNew = funcJoin2Df(pd.DataFrame(), dfOld, dfNew)
    print("Data ready (df4gNokBul)")
    print(df4gNokBul)
    df4gNokBul.to_csv("df4gNokBul.csv", sep=";", index=False, header=False, encoding="UTF-8-SIG")

    listFiles = os.listdir()
    #print(listFiles)
    for file in listFiles:
        if "df4gNokBul." in file:
            #print(file)
            dataFromSite  = funcPowerDrivaer(
                driver_path = CONFIG_DATA.get("LINKPO1"),
                binary_path = CONFIG_DATA.get("LINKPO2"),
                url = CONFIG_DATA.get("LINKSITE2"),
                action_func = funcParsingCes,
                #filterObjectSite = ""
                filterObjectSite = CONFIG_DATA.get("TEGSSITE3")
            )
            #print(dataFromSite)
            print("+ Add Data (df4gNokBul) to site CES")
if checkTable(df2gEr) == False:
    print("Empty table (df2gEr):")
    print(df2gEr)

    dfDaily, dbIp, dbUser, dbPasswd, dbName, dbTable, dbCondition, dbFilter = funcImportSqlToPandas(
        pd.DataFrame(),
        CONFIG_DATA.get("IPDB1"),
        CONFIG_DATA.get("USERDB1"),
        CONFIG_DATA.get("PASSWDB1"),
        CONFIG_DATA.get("DB2"),
        CONFIG_DATA.get("TABLE2"),
        CONFIG_DATA.get("CONDITION2"),
        CONFIG_DATA.get("FILTER2")
    )
    #print(dfDaily)
    dfOld = pd.merge(df2gEr, dfDaily, left_on="BS_name", right_on="BS_name", how="inner")
    #print(dfOld)

    dfNameNewBs, df2gEr, dfOld, listNameNewBs, str2gErCol, strOldCol = funcGet1DfFrom2Lists(
        pd.DataFrame(), df2gEr, dfOld, listNameNewBs,
        "BS_name", "BS_name"
    )
    #print(dfNameNewBs)

    dfNew = pd.DataFrame()
    if checkTable(dfNameNewBs) == False:
        print("Внимание! необходимо проверить новые данные для таблицы (dfNameNewBs)")
        dataNewSites = dict()
        numb = 0
        for name in listNameNewBs:
            if name in listReady:
                # print(str(numb)+". The site "+name+" already read")
                continue
            else:
                numb = numb + 1
                # print(str(numb)+". The site "+name+" is being read:")

                findUcn, findLatitude, findLongitude = funcPowerDrivaer(
                    driver_path=CONFIG_DATA.get("LINKPO1"),
                    binary_path=CONFIG_DATA.get("LINKPO2"),
                    url=CONFIG_DATA.get("LINKSITE1"),
                    action_func=funcParsingRdb,
                    filterObjectSite=name[:2] + "00" + name[2:6]
                )
                # print(findUcn)
                # print(findLatitude)
                # print(findLongitude)

                findUcn, listData, symbol, addSymbol1, addSymbol2 = funcDiffStringsAddList(
                    findUcn, listData,
                    "УЦН","УЦН", "-"
                )

                listData.append(findLatitude.replace(',', '.'))
                listData.append(findLongitude.replace(',', '.'))
                listReady.append(name)

        # print(listData)
        # print(listReady)
        listData, listReady, dfRdb, dataNewSites, cols = funcImport2listsToDf(
            listData, listReady, pd.DataFrame(), dataNewSites,
            ["UCN", "latitudeX1", "longitudeY1"]
        )
        # print(dfRdb)

        dfRdb, fromCol, toCol, fromRenameSymbol, toRenameSymbol, numbCol = funcGetSuffRenameColDf(
            dfRdb,
            "index","RegUcn", "IO", "IR",2
        )
        # print(dfRdb)

        dfCoords, dbIp, dbUser, dbPasswd, dbName, dbTable, dbCondition, dbFilter = funcImportSqlToPandas(
            pd.DataFrame(),
            CONFIG_DATA.get("IPDB1"),
            CONFIG_DATA.get("USERDB1"),
            CONFIG_DATA.get("PASSWDB1"),
            CONFIG_DATA.get("DB3"),
            CONFIG_DATA.get("TABLE3"),
            CONFIG_DATA.get("CONDITION3"),
            CONFIG_DATA.get("FILTER3")
        )
        # print(dfCoords)
        dfDaily = pd.merge(dfDaily, dfCoords, left_on="BS_name", right_on="BS_name", how="inner")
        # print(dfDaily)
        dfUcnTemplate = funcAddDfTemplateUcn(pd.DataFrame())
        # print(dfUcnTemplate)

        dfNoUcn = pd.DataFrame()
        dfNoUcn = pd.concat([dfRdb, dfNoUcn])
        dfNoUcn = dfNoUcn[dfNoUcn["UCN"].isin(["-"])]
        if checkTable(dfNoUcn) == False:
            dfNeighbour, dfNoUcn, df2gEr, dfDaily, strNoUcn, str2gEr = funcJoin3df(
                pd.DataFrame(), dfNoUcn, df2gEr, dfDaily,
                "index", "BS_name"
            )
            dfNoUcn = funcFindNeighbour(dfNeighbour)

            dfNoUcn = funcCorrectCols2gEr(dfNoUcn)
            dfNew = pd.concat([dfNew, dfNoUcn])
        #print(dfNoUcn)

        dfUcn = pd.DataFrame()
        dfUcn = pd.concat([dfRdb, dfUcn])
        dfUcn = dfUcn[dfUcn["UCN"].isin(["УЦН"])]
        if checkTable(dfUcn) == False:
            dfUcn, df2gEr, dfUcnTemplate, strUcn1, strUcn2, str2gEr, strUcnTemplate = funcJoin2Df2(
                dfUcn, df2gEr, dfUcnTemplate,
                "index","RegUcn","BS_name","RegUcn"
            )
            #print(dfUcn)

            dfUcn = funcCorrectCols2gEr(dfUcn)
            dfNew = pd.concat([dfNew, dfUcn])
        #print(dfUcn)
    #print(dfNew)

    dfOld = funcCorrectCols2gEr(dfOld)
    #print(dfOld)

    df2gEr, dfOld, dfNew = funcJoin2Df(pd.DataFrame(), dfOld, dfNew)
    print("Data ready (df2gEr)")
    print(df2gEr)
    df2gEr.to_csv("df2gEr.csv", sep=",", index=False, header=False, encoding="UTF-8-SIG")

    listFiles = os.listdir()
    #print(listFiles)
    for file in listFiles:
        if "df2gEr." in file:
            #print(file)
            dataFromSite  = funcPowerDrivaer(
                driver_path = CONFIG_DATA.get("LINKPO1"),
                binary_path = CONFIG_DATA.get("LINKPO2"),
                url = CONFIG_DATA.get("LINKSITE3"),
                action_func = funcParsingCes,
                filterObjectSite = CONFIG_DATA.get("TEGSSITE6")
            )
            #print(dataFromSite)
            print("+ Add Data (df2gEr) to site CES")
if checkTable(df2gErBul) == False:
    print("Empty table (df2gErBul):")
    print(df2gErBul)

    dfDaily, dbIp, dbUser, dbPasswd, dbName, dbTable, dbCondition, dbFilter = funcImportSqlToPandas(
        pd.DataFrame(),
        CONFIG_DATA.get("IPDB1"),
        CONFIG_DATA.get("USERDB1"),
        CONFIG_DATA.get("PASSWDB1"),
        CONFIG_DATA.get("DB2"),
        CONFIG_DATA.get("TABLE2"),
        CONFIG_DATA.get("CONDITION2"),
        CONFIG_DATA.get("FILTER2")
    )
    #print(dfDaily)
    dfOld = pd.merge(df2gErBul, dfDaily, left_on="BS_name", right_on="BS_name", how="inner")
    #print(dfOld)

    dfNameNewBs, df2gErBul, dfOld, listNameNewBs, str2gErBulCol, strOldCol = funcGet1DfFrom2Lists(
        pd.DataFrame(), df2gErBul, dfOld, listNameNewBs,
        "BS_name", "BS_name"
    )
    #print(dfNameNewBs)

    dfNew = pd.DataFrame()
    if checkTable(dfNameNewBs) == False:
        print("Внимание! необходимо проверить новые данные для таблицы (dfNameNewBs)")
        dataNewSites = dict()
        numb = 0
        for name in listNameNewBs:
            if name in listReady:
                # print(str(numb)+". The site "+name+" already read")
                continue
            else:
                numb = numb + 1
                # print(str(numb)+". The site "+name+" is being read:")

                findUcn, findLatitude, findLongitude = funcPowerDrivaer(
                    driver_path=CONFIG_DATA.get("LINKPO1"),
                    binary_path=CONFIG_DATA.get("LINKPO2"),
                    url=CONFIG_DATA.get("LINKSITE1"),
                    action_func=funcParsingRdb,
                    filterObjectSite=name[:2] + "00" + name[2:6]
                )
                # print(findUcn)
                # print(findLatitude)
                # print(findLongitude)

                findUcn, listData, symbol, addSymbol1, addSymbol2 = funcDiffStringsAddList(
                    findUcn, listData,
                    "УЦН","УЦН", "-"
                )

                listData.append(findLatitude.replace(',', '.'))
                listData.append(findLongitude.replace(',', '.'))
                listReady.append(name)
        # print(listData)
        # print(listReady)

        listData, listReady, dfRdb, dataNewSites, cols = funcImport2listsToDf(
            listData, listReady, pd.DataFrame(), dataNewSites,
            ["UCN", "latitudeX1", "longitudeY1"]
        )
        # print(dfRdb)
        dfRdb, fromCol, toCol, fromRenameSymbol, toRenameSymbol, numbCol = funcGetSuffRenameColDf(
            dfRdb,
            "index","RegUcn", "IO", "IR",2
        )
        # print(dfRdb)

        dfCoords, dbIp, dbUser, dbPasswd, dbName, dbTable, dbCondition, dbFilter = funcImportSqlToPandas(
            pd.DataFrame(),
            CONFIG_DATA.get("IPDB1"),
            CONFIG_DATA.get("USERDB1"),
            CONFIG_DATA.get("PASSWDB1"),
            CONFIG_DATA.get("DB3"),
            CONFIG_DATA.get("TABLE3"),
            CONFIG_DATA.get("CONDITION3"),
            CONFIG_DATA.get("FILTER3")
        )
        # print(dfCoords)
        dfDaily = pd.merge(dfDaily, dfCoords, left_on="BS_name", right_on="BS_name", how="inner")
        # print(dfDaily)
        dfUcnTemplate = funcAddDfTemplateUcnBulat(pd.DataFrame())
        # print(dfUcnTemplate)

        dfNoUcn = pd.DataFrame()
        dfNoUcn = pd.concat([dfRdb, dfNoUcn])
        dfNoUcn = dfNoUcn[dfNoUcn["UCN"].isin(["-"])]
        if checkTable(dfNoUcn) == False:
            dfNeighbour, dfNoUcn, df2gErBul, dfDaily, strNoUcn, str2gErBul = funcJoin3df(
                pd.DataFrame(), dfNoUcn, df2gErBul, dfDaily,
                "index", "BS_name"
            )
            dfNoUcn = funcFindNeighbour(dfNeighbour)

            dfNoUcn = funcCorrectCols2gEr(dfNoUcn)
            dfNew = pd.concat([dfNew, dfNoUcn])
        #print(dfNoUcn)

        dfUcn = pd.DataFrame()
        dfUcn = pd.concat([dfRdb, dfUcn])
        dfUcn = dfUcn[dfUcn["UCN"].isin(["УЦН"])]
        if checkTable(dfUcn) == False:
            dfUcn, df2gErBul, dfUcnTemplate, strUcn1, strUcn2, str2gErBul, strUcnTemplate = funcJoin2Df2(
                dfUcn, df2gErBul, dfUcnTemplate,
                "index","RegUcn","BS_name","RegUcn"
            )
            #print(dfUcn)

            dfUcn = funcCorrectCols2gEr(dfUcn)
            dfNew = pd.concat([dfNew, dfUcn])
        #print(dfUcn)
    #print(dfNew)

    dfOld = funcCorrectCols2gEr(dfOld)
    #print(dfOld)

    df2gErBul, dfOld, dfNew = funcJoin2Df(pd.DataFrame(), dfOld, dfNew)
    print("Data ready (df2gErBul)")
    print(df2gErBul)
    df2gErBul.to_csv("df2gErBul.csv", sep=",", index=False, header=False, encoding="UTF-8-SIG")

    listFiles = os.listdir()
    #print(listFiles)
    for file in listFiles:
        if "df2gErBul." in file:
            #print(file)
            dataFromSite  = funcPowerDrivaer(
                driver_path = CONFIG_DATA.get("LINKPO1"),
                binary_path = CONFIG_DATA.get("LINKPO2"),
                url = CONFIG_DATA.get("LINKSITE3"),
                action_func = funcParsingCes,
                filterObjectSite = CONFIG_DATA.get("TEGSSITE6")
            )
            #print(dataFromSite)
            print("+ Add Data (df2gErBul) to site CES")
if checkTable(df2gErBulNeop) == False:
    print("Empty table (df2gErBulNeop):")
    print(df2gErBulNeop)

    dfDaily, dbIp, dbUser, dbPasswd, dbName, dbTable, dbCondition, dbFilter = funcImportSqlToPandas(
        pd.DataFrame(),
        CONFIG_DATA.get("IPDB1"),
        CONFIG_DATA.get("USERDB1"),
        CONFIG_DATA.get("PASSWDB1"),
        CONFIG_DATA.get("DB2"),
        CONFIG_DATA.get("TABLE2"),
        CONFIG_DATA.get("CONDITION2"),
        CONFIG_DATA.get("FILTER2")
    )
    # print(dfDaily)
    dfOld = pd.merge(df2gErBulNeop, dfDaily, left_on="BS_name", right_on="BS_name", how="inner")
    # print(dfOld)

    dfNameNewBs, df2gErBulNeop, dfOld, listNameNewBs, str2gErNeopBulCol, strOldCol = funcGet1DfFrom2Lists(
        pd.DataFrame(), df2gErBulNeop, dfOld, listNameNewBs,
        "BS_name", "BS_name"
    )
    # print(dfNameNewBs)

    dfNew = pd.DataFrame()
    if checkTable(dfNameNewBs) == False:
        print("Внимание! необходимо проверить новые данные для таблицы (dfNameNewBs)")
        dataNewSites = dict()
        numb = 0
        for name in listNameNewBs:
            if name in listReady:
                # print(str(numb)+". The site "+name+" already read")
                continue
            else:
                numb = numb + 1
                # print(str(numb)+". The site "+name+" is being read:")

                findUcn, findLatitude, findLongitude = funcPowerDrivaer(
                    driver_path=CONFIG_DATA.get("LINKPO1"),
                    binary_path=CONFIG_DATA.get("LINKPO2"),
                    url=CONFIG_DATA.get("LINKSITE1"),
                    action_func=funcParsingRdb,
                    filterObjectSite=name[:2] + "00" + name[2:6]
                )
                # print(findUcn)
                # print(findLatitude)
                # print(findLongitude)

                findUcn, listData, symbol, addSymbol1, addSymbol2 = funcDiffStringsAddList(
                    findUcn, listData,
                    "УЦН", "УЦН", "-"
                )

                listData.append(findLatitude.replace(',', '.'))
                listData.append(findLongitude.replace(',', '.'))
                listReady.append(name)
        # print(listData)
        # print(listReady)

        listData, listReady, dfRdb, dataNewSites, cols = funcImport2listsToDf(
            listData, listReady, pd.DataFrame(), dataNewSites,
            ["UCN", "latitudeX1", "longitudeY1"]
        )
        # print(dfRdb)
        dfRdb, fromCol, toCol, fromRenameSymbol, toRenameSymbol, numbCol = funcGetSuffRenameColDf(
            dfRdb,
            "index", "RegUcn", "IO", "IR", 2
        )
        # print(dfRdb)

        dfCoords, dbIp, dbUser, dbPasswd, dbName, dbTable, dbCondition, dbFilter = funcImportSqlToPandas(
            pd.DataFrame(),
            CONFIG_DATA.get("IPDB1"),
            CONFIG_DATA.get("USERDB1"),
            CONFIG_DATA.get("PASSWDB1"),
            CONFIG_DATA.get("DB3"),
            CONFIG_DATA.get("TABLE3"),
            CONFIG_DATA.get("CONDITION3"),
            CONFIG_DATA.get("FILTER3")
        )
        # print(dfCoords)
        dfDaily = pd.merge(dfDaily, dfCoords, left_on="BS_name", right_on="BS_name", how="inner")
        # print(dfDaily)
        dfUcnTemplate = funcAddDfTemplateUcnBulat(pd.DataFrame())
        # print(dfUcnTemplate)

        dfNoUcn = pd.DataFrame()
        dfNoUcn = pd.concat([dfRdb, dfNoUcn])
        dfNoUcn = dfNoUcn[dfNoUcn["UCN"].isin(["-"])]
        if checkTable(dfNoUcn) == False:
            dfNeighbour, dfNoUcn, df2gErBulNeop, dfDaily, strNoUcn, str2gErBulNeop = funcJoin3df(
                pd.DataFrame(), dfNoUcn, df2gErBulNeop, dfDaily,
                "index", "BS_name"
            )
            dfNoUcn = funcFindNeighbour(dfNeighbour)

            dfNoUcn = funcCorrectCols2gEr(dfNoUcn)
            dfNew = pd.concat([dfNew, dfNoUcn])
        # print(dfNoUcn)

        dfUcn = pd.DataFrame()
        dfUcn = pd.concat([dfRdb, dfUcn])
        dfUcn = dfUcn[dfUcn["UCN"].isin(["УЦН"])]
        if checkTable(dfUcn) == False:
            dfUcn, df2gErBulNeop, dfUcnTemplate, strUcn1, strUcn2, str2gErBulNeop, strUcnTemplate = funcJoin2Df2(
                dfUcn, df2gErBulNeop, dfUcnTemplate,
                "index", "RegUcn", "BS_name", "RegUcn"
            )
            # print(dfUcn)

            dfUcn = funcCorrectCols2gEr(dfUcn)
            dfNew = pd.concat([dfNew, dfUcn])
        # print(dfUcn)
    # print(dfNew)

    dfOld = funcCorrectCols2gEr(dfOld)
    # print(dfOld)

    df2gErBulNeop, dfOld, dfNew = funcJoin2Df(pd.DataFrame(), dfOld, dfNew)
    print("Data ready (df2gErBulNeop)")
    print(df2gErBulNeop)
    df2gErBulNeop.to_csv("df2gErBulNeop.csv", sep=",", index=False, header=False, encoding="UTF-8-SIG")

    listFiles = os.listdir()
    # print(listFiles)
    for file in listFiles:
        if "df2gErBulNeop." in file:
            # print(file)
            dataFromSite = funcPowerDrivaer(
                driver_path=CONFIG_DATA.get("LINKPO1"),
                binary_path=CONFIG_DATA.get("LINKPO2"),
                url=CONFIG_DATA.get("LINKSITE3"),
                action_func=funcParsingCes,
                filterObjectSite=CONFIG_DATA.get("TEGSSITE6")
            )
            # print(dataFromSite)
            print("+ Add Data (df2gErBulNeop) to site CES")
if checkTable(df3gEr) == False:
    print("Empty table (df3gEr):")
    print(df3gEr)

    dfDaily, dbIp, dbUser, dbPasswd, dbName, dbTable, dbCondition, dbFilter = funcImportSqlToPandas(
        pd.DataFrame(),
        CONFIG_DATA.get("IPDB1"),
        CONFIG_DATA.get("USERDB1"),
        CONFIG_DATA.get("PASSWDB1"),
        CONFIG_DATA.get("DB2"),
        CONFIG_DATA.get("TABLE6"),
        CONFIG_DATA.get("CONDITION4"),
        CONFIG_DATA.get("FILTER6")
    )
    #print(dfDaily)

    dfOld = pd.merge(df3gEr, dfDaily, left_on="BS_name", right_on="BS_name", how="inner")
    #dfOld = pd.merge(df3gEr, dfDaily, left_on="BS_name", right_on="Namefor3g", how="inner")
    print("Внимание! необходимо проверить соединение таблиц по стоблцу BS_name. Если таблица находим данные по столбцу Namefor3g, тогда необходимо раскомментировать ниже строки #dfOld = ... и #listTechOld = с заменой на текущие строки в коде и доработать ниже код, особенно с BS_name, Так как столбцы по названию могут отличаться.")
    #print(dfOld)

    dfNameNewBs, df3gEr, dfOld, listNameNewBs, str3gErCol, strOldCol = funcGet1DfFrom2Lists(
        pd.DataFrame(), df3gEr, dfOld, listNameNewBs,
        "BS_name", "BS_name"
    )
    #dfNameNewBs, df3gEr, dfOld, listNameNewBs, str3gErCol, strOldCol = funcGet1DfFrom2Lists(pd.DataFrame(), df3gEr, dfOld, listNameNewBs, "BS_name", "Namefor3g")
    #print(dfNameNewBs)

    dfNew = pd.DataFrame()
    if checkTable(dfNameNewBs) == False:
        dataNewSites = dict()
        numb = 0
        for name in listNameNewBs:
            if name in listReady:
                #print(str(numb)+". The site "+name+" already read")
                continue
            else:
                numb = numb + 1
                # print(str(numb)+". The site "+name+" is being read:")                

                findUcn, findLatitude, findLongitude = funcPowerDrivaer(
                    driver_path=CONFIG_DATA.get("LINKPO1"),
                    binary_path=CONFIG_DATA.get("LINKPO2"),
                    url=CONFIG_DATA.get("LINKSITE1"),
                    action_func=funcParsingRdb,
                    filterObjectSite=name[:2] + "00" + name[2:6]
                )
                # print(findUcn)
                # print(findLatitude)
                # print(findLongitude)

                findUcn, listData, symbol, addSymbol1, addSymbol2 = funcDiffStringsAddList(
                    findUcn, listData,
                    "УЦН","УЦН", "-"
                )

                listData.append(findLatitude.replace(',', '.'))
                listData.append(findLongitude.replace(',', '.'))
                listReady.append(name)

        #print(listData)
        #print(listReady)
        listData, listReady, dfRdb, dataNewSites, cols = funcImport2listsToDf(
            listData, listReady, pd.DataFrame(), dataNewSites,
            ["UCN", "latitudeX1", "longitudeY1"]
        )
        #print(dfRdb)

        dfRdb, fromCol, toCol, fromRenameSymbol, toRenameSymbol, numbCol = funcGetSuffRenameColDf(
            dfRdb,
            "index","RegUcn", "IO", "IR",2
        )
        #print(dfRdb)

        dfCoords, dbIp, dbUser, dbPasswd, dbName, dbTable, dbCondition, dbFilter = funcImportSqlToPandas(
            pd.DataFrame(),
            CONFIG_DATA.get("IPDB1"),
            CONFIG_DATA.get("USERDB1"),
            CONFIG_DATA.get("PASSWDB1"),
            CONFIG_DATA.get("DB3"),
            CONFIG_DATA.get("TABLE3"),
            CONFIG_DATA.get("CONDITION3"),
            CONFIG_DATA.get("FILTER3")
        )
        #print(dfCoords)
        #dfDaily = pd.merge(dfDaily, dfCoords, left_on="BS_name", right_on="BS_name", how="inner")
        dfDaily = pd.merge(dfDaily, dfCoords, left_on="Namefor3g", right_on="BS_name", how="inner")
        #print(dfDaily)
        dfUcnTemplate = funcAddDfTemplateUcn(pd.DataFrame())
        #print(dfUcnTemplate)

        dfNoUcn = pd.DataFrame()
        dfNoUcn = pd.concat([dfRdb, dfNoUcn])
        dfNoUcn = dfNoUcn[dfNoUcn["UCN"].isin(["-"])]
        if checkTable(dfNoUcn) == False:
            dfNeighbour, dfNoUcn, df3gEr, dfDaily, strNoUcn, str3gEr = funcJoin3df(
                pd.DataFrame(), dfNoUcn, df3gEr, dfDaily,
                "index", "BS_name"
            )
            dfNoUcn = funcFindNeighbour(dfNeighbour)
            #print(dfNoUcn)

            dfNoUcn = funcCorrectCols3gEr(dfNoUcn)
            dfNew = pd.concat([dfNew, dfNoUcn])
        #print(dfNoUcn)

        dfUcn = pd.DataFrame()
        dfUcn = pd.concat([dfRdb, dfUcn])
        dfUcn = dfUcn[dfUcn["UCN"].isin(["УЦН"])]
        if checkTable(dfUcn) == False:
            print("Внимание! необходимо проверить заполнение данных таблицы dfUcn.")
            dfUcn, df3gEr, dfUcnTemplate, strUcn1, strUcn2, str3gEr, strUcnTemplate = funcJoin2Df2(
                dfUcn, df3gEr, dfUcnTemplate,
                "index","RegUcn","BS_name","RegUcn"
            )
            # print(dfUcn)

            dfUcn = funcCorrectCols3gEr(dfUcn)
            dfNew = pd.concat([dfNew, dfUcn])
        #print(dfUcn)
    #print(dfNew)

    dfOld = funcCorrectCols3gEr(dfOld)
    #print(dfOld)

    df3gEr, dfOld, dfNew = funcJoin2Df(pd.DataFrame(), dfOld, dfNew)
    print("Data ready (df3gEr)")
    print(df3gEr)

    df3gEr.to_csv("df3gEr.csv", sep=",", index=False, header=False, encoding="UTF-8-SIG")

    listFiles = os.listdir()
    # print(listFiles)
    for file in listFiles:
        if "df3gEr." in file:
            #print(file)
            dataFromSite = funcPowerDrivaer(
                driver_path=CONFIG_DATA.get("LINKPO1"),
                binary_path=CONFIG_DATA.get("LINKPO2"),
                url=CONFIG_DATA.get("LINKSITE3"),
                action_func=funcParsingCes,
                filterObjectSite=CONFIG_DATA.get("TEGSSITE5")
            )
            # print(dataFromSite)
            print("+ Add Data (df3gEr) to site CES")
if checkTable(df4gEr) == False:
    print("Empty table (df4gEr):")
    print(df4gEr)

    dfDaily, dbIp, dbUser, dbPasswd, dbName, dbTable, dbCondition, dbFilter = funcImportSqlToPandas(
        pd.DataFrame(),
        CONFIG_DATA.get("IPDB1"),
        CONFIG_DATA.get("USERDB1"),
        CONFIG_DATA.get("PASSWDB1"),
        CONFIG_DATA.get("DB2"),
        CONFIG_DATA.get("TABLE7"),
        CONFIG_DATA.get("CONDITION2"),
        CONFIG_DATA.get("FILTER7")
    )
    #print(dfDaily)

    dfOld = pd.merge(df4gEr, dfDaily, left_on="BS_name", right_on="BS_name", how="inner")
    #print(dfOld)

    dfNameNewBs, df4gEr, dfOld, listNameNewBs, str4gErCol, strOldCol = funcGet1DfFrom2Lists(
        pd.DataFrame(), df4gEr, dfOld, listNameNewBs,
        "BS_name", "BS_name"
    )
    #print(dfNameNewBs)

    dfNew = pd.DataFrame()
    if checkTable(dfNameNewBs) == False:
        print("Внимание! Заполнена таблица (dfNameNewBs) необходимо проверить весь ниже код.")
        dataNewSites = dict()
        numb = 0
        for name in listNameNewBs:
            if name in listReady:
                #print(str(numb)+". The site "+name+" already read")
                continue
            else:
                numb = numb + 1
                # print(str(numb)+". The site "+name+" is being read:")                

                findUcn, findLatitude, findLongitude = funcPowerDrivaer(
                    driver_path=CONFIG_DATA.get("LINKPO1"),
                    binary_path=CONFIG_DATA.get("LINKPO2"),
                    url=CONFIG_DATA.get("LINKSITE1"),
                    action_func=funcParsingRdb,
                    filterObjectSite=name[:2] + "00" + name[2:6]
                )
                # print(findUcn)
                # print(findLatitude)
                # print(findLongitude)

                findUcn, listData, symbol, addSymbol1, addSymbol2 = funcDiffStringsAddList(
                    findUcn, listData,
                    "УЦН","УЦН", "-"
                )

                listData.append(findLatitude.replace(',', '.'))
                listData.append(findLongitude.replace(',', '.'))
                listReady.append(name)

        # print(listData)
        # print(listReady)
        listData, listReady, dfRdb, dataNewSites, cols = funcImport2listsToDf(
            listData, listReady, pd.DataFrame(), dataNewSites,
            ["UCN", "latitudeX1", "longitudeY1"]
        )
        # print(dfRdb)

        dfRdb, fromCol, toCol, fromRenameSymbol, toRenameSymbol, numbCol = funcGetSuffRenameColDf(
            dfRdb,
            "index","RegUcn", "IO", "IR",2
        )
        # print(dfRdb)

        dfCoords, dbIp, dbUser, dbPasswd, dbName, dbTable, dbCondition, dbFilter = funcImportSqlToPandas(
            pd.DataFrame(),
            CONFIG_DATA.get("IPDB1"),
            CONFIG_DATA.get("USERDB1"),
            CONFIG_DATA.get("PASSWDB1"),
            CONFIG_DATA.get("DB3"),
            CONFIG_DATA.get("TABLE3"),
            CONFIG_DATA.get("CONDITION3"),
            CONFIG_DATA.get("FILTER3")
        )
        # print(dfCoords)
        dfDaily = pd.merge(dfDaily, dfCoords, left_on="BS_name", right_on="BS_name", how="inner")
        # print(dfDaily)
        dfUcnTemplate = funcAddDfTemplateUcn(pd.DataFrame())
        # print(dfUcnTemplate)

        dfNoUcn = pd.DataFrame()
        dfNoUcn = pd.concat([dfRdb, dfNoUcn])
        dfNoUcn = dfNoUcn[dfNoUcn["UCN"].isin(["-"])]
        if checkTable(dfNoUcn) == False:
            '''dfNoUcn = pd.merge(dfNoUcn, df4gEr, left_on="index", right_on="BS_name", how="inner")
            dfNeighbour = dfNoUcn.merge(dfDaily, how="cross")'''
            dfNeighbour, dfNoUcn, df4gEr, dfDaily, strNoUcn, str4gEr = funcJoin3df(
                pd.DataFrame(), dfNoUcn, df4gEr, dfDaily,
                "index", "BS_name"
            )
            dfNoUcn = funcFindNeighbour(dfNeighbour)

            #dfNoUcn = dfNoUcn.reindex(columns=["Reg", "site", "LAC", "Sector"])
            dfNoUcn = funcCorrectCols4gEr(dfNoUcn)
            dfNew = pd.concat([dfNew, dfNoUcn])
        # print(dfNoUcn)

        dfUcn = pd.DataFrame()
        dfUcn = pd.concat([dfRdb, dfUcn])
        dfUcn = dfUcn[dfUcn["UCN"].isin(["УЦН"])]
        if checkTable(dfUcn) == False:
            # print(dfUcn)
            dfUcn, df4gEr, dfUcnTemplate, strUcn1, strUcn2, str4gEr, strUcnTemplate = funcJoin2Df2(
                dfUcn, df4gEr, dfUcnTemplate,
                "index","RegUcn","BS_name","RegUcn"
            )

            dfNoUcn = funcCorrectCols4gEr(dfNoUcn)
            dfNew = pd.concat([dfNew, dfUcn])
        # print(dfUcn)
    #print(dfNew)

    dfOld = funcCorrectCols4gEr(dfOld)
    #print(dfOld)

    df4gEr, dfOld, dfNew = funcJoin2Df(pd.DataFrame(), dfOld, dfNew)
    print("Data ready (df4gEr)")
    print(df4gEr)

    df4gEr.to_csv("df4gEr.csv", sep=",", index=False, header=False, encoding="UTF-8-SIG")

    listFiles = os.listdir()
    # print(listFiles)
    for file in listFiles:
        if "df4gEr." in file:
            #print(file)
            dataFromSite = funcPowerDrivaer(
                driver_path=CONFIG_DATA.get("LINKPO1"),
                binary_path=CONFIG_DATA.get("LINKPO2"),
                url=CONFIG_DATA.get("LINKSITE3"),
                action_func=funcParsingCes,
                filterObjectSite=CONFIG_DATA.get("TEGSSITE4")
            )
            # print(dataFromSite)
            print("+ Add Data (df4gEr) to site CES")
if checkTable(df4gErBul) == False:
    print("Empty table (df4gErBul):")
    print(df4gErBul)

    dfDaily, dbIp, dbUser, dbPasswd, dbName, dbTable, dbCondition, dbFilter = funcImportSqlToPandas(
        pd.DataFrame(),
        CONFIG_DATA.get("IPDB1"),
        CONFIG_DATA.get("USERDB1"),
        CONFIG_DATA.get("PASSWDB1"),
        CONFIG_DATA.get("DB2"),
        CONFIG_DATA.get("TABLE7"),
        CONFIG_DATA.get("CONDITION2"),
        CONFIG_DATA.get("FILTER7")
    )
    #print(dfDaily)

    dfOld = pd.merge(df4gErBul, dfDaily, left_on="BS_name", right_on="BS_name", how="inner")
    #print(dfOld)

    dfNameNewBs, df4gErBul, dfOld, listNameNewBs, str4gErBulCol, strOldCol = funcGet1DfFrom2Lists(
        pd.DataFrame(), df4gErBul, dfOld, listNameNewBs,
        "BS_name", "BS_name"
    )
    #print(dfNameNewBs)

    dfNew = pd.DataFrame()
    if checkTable(dfNameNewBs) == False:
        print("Внимание! Заполнена таблица (dfNameNewBs) необходимо проверить весь ниже код.")
        dataNewSites = dict()
        numb = 0
        for name in listNameNewBs:
            if name in listReady:
                #print(str(numb)+". The site "+name+" already read")
                continue
            else:
                numb = numb + 1
                # print(str(numb)+". The site "+name+" is being read:")

                findUcn, findLatitude, findLongitude = funcPowerDrivaer(
                    driver_path=CONFIG_DATA.get("LINKPO1"),
                    binary_path=CONFIG_DATA.get("LINKPO2"),
                    url=CONFIG_DATA.get("LINKSITE1"),
                    action_func=funcParsingRdb,
                    filterObjectSite=name[:2] + "00" + name[2:6]
                )
                # print(findUcn)
                # print(findLatitude)
                # print(findLongitude)

                findUcn, listData, symbol, addSymbol1, addSymbol2 = funcDiffStringsAddList(
                    findUcn, listData,
                    "УЦН","УЦН", "-"
                )

                listData.append(findLatitude.replace(',', '.'))
                listData.append(findLongitude.replace(',', '.'))
                listReady.append(name)

        # print(listData)
        # print(listReady)
        listData, listReady, dfRdb, dataNewSites, cols = funcImport2listsToDf(
            listData, listReady, pd.DataFrame(), dataNewSites,
            ["UCN", "latitudeX1", "longitudeY1"]
        )
        # print(dfRdb)

        dfRdb, fromCol, toCol, fromRenameSymbol, toRenameSymbol, numbCol = funcGetSuffRenameColDf(
            dfRdb,
            "index","RegUcn", "IO", "IR",2
        )
        # print(dfRdb)

        dfCoords, dbIp, dbUser, dbPasswd, dbName, dbTable, dbCondition, dbFilter = funcImportSqlToPandas(
            pd.DataFrame(),
            CONFIG_DATA.get("IPDB1"),
            CONFIG_DATA.get("USERDB1"),
            CONFIG_DATA.get("PASSWDB1"),
            CONFIG_DATA.get("DB3"),
            CONFIG_DATA.get("TABLE3"),
            CONFIG_DATA.get("CONDITION3"),
            CONFIG_DATA.get("FILTER3")
        )
        # print(dfCoords)
        dfDaily = pd.merge(dfDaily, dfCoords, left_on="BS_name", right_on="BS_name", how="inner")
        # print(dfDaily)
        dfUcnTemplate = funcAddDfTemplateUcn(pd.DataFrame())
        # print(dfUcnTemplate)

        dfNoUcn = pd.DataFrame()
        dfNoUcn = pd.concat([dfRdb, dfNoUcn])
        dfNoUcn = dfNoUcn[dfNoUcn["UCN"].isin(["-"])]
        if checkTable(dfNoUcn) == False:
            '''dfNoUcn = pd.merge(dfNoUcn, df4gErBul, left_on="index", right_on="BS_name", how="inner")
            dfNeighbour = dfNoUcn.merge(dfDaily, how="cross")'''
            dfNeighbour, dfNoUcn, df4gErBul, dfDaily, strNoUcn, str4gErBul = funcJoin3df(
                pd.DataFrame(), dfNoUcn, df4gErBul, dfDaily,
                "index", "BS_name"
            )
            dfNoUcn = funcFindNeighbour(dfNeighbour)

            #dfNoUcn = dfNoUcn.reindex(columns=["Reg", "site", "LAC", "Sector"])
            dfNoUcn = funcCorrectCols4gEr(dfNoUcn)
            dfNew = pd.concat([dfNew, dfNoUcn])
        # print(dfNoUcn)

        dfUcn = pd.DataFrame()
        dfUcn = pd.concat([dfRdb, dfUcn])
        dfUcn = dfUcn[dfUcn["UCN"].isin(["УЦН"])]
        if checkTable(dfUcn) == False:
            # print(dfUcn)
            dfUcn, df4gErBul, dfUcnTemplate, strUcn1, strUcn2, str4gErBul, strUcnTemplate = funcJoin2Df2(
                dfUcn, df4gErBul, dfUcnTemplate,
                "index","RegUcn","BS_name","RegUcn"
            )

            dfNoUcn = funcCorrectCols4gEr(dfNoUcn)
            dfNew = pd.concat([dfNew, dfUcn])
        # print(dfUcn)
    #print(dfNew)

    dfOld = funcCorrectCols4gEr(dfOld)
    #print(dfOld)

    df4gErBul, dfOld, dfNew = funcJoin2Df(pd.DataFrame(), dfOld, dfNew)
    print("Data ready (df4gErBul)")
    print(df4gErBul)

    df4gErBul.to_csv("df4gErBul.csv", sep=",", index=False, header=False, encoding="UTF-8-SIG")

    listFiles = os.listdir()
    # print(listFiles)
    for file in listFiles:
        if "df4gErBul." in file:
            #print(file)
            dataFromSite = funcPowerDrivaer(
                driver_path=CONFIG_DATA.get("LINKPO1"),
                binary_path=CONFIG_DATA.get("LINKPO2"),
                url=CONFIG_DATA.get("LINKSITE3"),
                action_func=funcParsingCes,
                filterObjectSite=CONFIG_DATA.get("TEGSSITE4")
            )
            # print(dataFromSite)
            print("+ Add Data (df4gErBul) to site CES")
if checkTable(df4gErBulNeop) == False:
    print("Empty table (df4gErBulNeop):")
    print(df4gErBulNeop)

    dfDaily, dbIp, dbUser, dbPasswd, dbName, dbTable, dbCondition, dbFilter = funcImportSqlToPandas(
        pd.DataFrame(),
        CONFIG_DATA.get("IPDB1"),
        CONFIG_DATA.get("USERDB1"),
        CONFIG_DATA.get("PASSWDB1"),
        CONFIG_DATA.get("DB2"),
        CONFIG_DATA.get("TABLE7"),
        CONFIG_DATA.get("CONDITION2"),
        CONFIG_DATA.get("FILTER7")
    )
    #print(dfDaily)

    dfOld = pd.merge(df4gErBulNeop, dfDaily, left_on="BS_name", right_on="BS_name", how="inner")
    #print(dfOld)

    dfNameNewBs, df4gErBulNeop, dfOld, listNameNewBs, str4gErBulCol, strOldCol = funcGet1DfFrom2Lists(
        pd.DataFrame(), df4gErBulNeop, dfOld, listNameNewBs,
        "BS_name", "BS_name"
    )
    #print(dfNameNewBs)

    dfNew = pd.DataFrame()
    if checkTable(dfNameNewBs) == False:
        print("Внимание! Заполнена таблица (dfNameNewBs) необходимо проверить весь ниже код.")
        dataNewSites = dict()
        numb = 0
        for name in listNameNewBs:
            if name in listReady:
                #print(str(numb)+". The site "+name+" already read")
                continue
            else:
                numb = numb + 1
                # print(str(numb)+". The site "+name+" is being read:")

                findUcn, findLatitude, findLongitude = funcPowerDrivaer(
                    driver_path=CONFIG_DATA.get("LINKPO1"),
                    binary_path=CONFIG_DATA.get("LINKPO2"),
                    url=CONFIG_DATA.get("LINKSITE1"),
                    action_func=funcParsingRdb,
                    filterObjectSite=name[:2] + "00" + name[2:6]
                )
                # print(findUcn)
                # print(findLatitude)
                # print(findLongitude)

                findUcn, listData, symbol, addSymbol1, addSymbol2 = funcDiffStringsAddList(
                    findUcn, listData,
                    "УЦН","УЦН", "-"
                )

                listData.append(findLatitude.replace(',', '.'))
                listData.append(findLongitude.replace(',', '.'))
                listReady.append(name)

        # print(listData)
        # print(listReady)
        listData, listReady, dfRdb, dataNewSites, cols = funcImport2listsToDf(
            listData, listReady, pd.DataFrame(), dataNewSites,
            ["UCN", "latitudeX1", "longitudeY1"]
        )
        # print(dfRdb)

        dfRdb, fromCol, toCol, fromRenameSymbol, toRenameSymbol, numbCol = funcGetSuffRenameColDf(
            dfRdb,
            "index","RegUcn", "IO", "IR",2
        )
        # print(dfRdb)

        dfCoords, dbIp, dbUser, dbPasswd, dbName, dbTable, dbCondition, dbFilter = funcImportSqlToPandas(
            pd.DataFrame(),
            CONFIG_DATA.get("IPDB1"),
            CONFIG_DATA.get("USERDB1"),
            CONFIG_DATA.get("PASSWDB1"),
            CONFIG_DATA.get("DB3"),
            CONFIG_DATA.get("TABLE3"),
            CONFIG_DATA.get("CONDITION3"),
            CONFIG_DATA.get("FILTER3")
        )
        # print(dfCoords)
        dfDaily = pd.merge(dfDaily, dfCoords, left_on="BS_name", right_on="BS_name", how="inner")
        # print(dfDaily)
        dfUcnTemplate = funcAddDfTemplateUcn(pd.DataFrame())
        # print(dfUcnTemplate)

        dfNoUcn = pd.DataFrame()
        dfNoUcn = pd.concat([dfRdb, dfNoUcn])
        dfNoUcn = dfNoUcn[dfNoUcn["UCN"].isin(["-"])]
        if checkTable(dfNoUcn) == False:
            '''dfNoUcn = pd.merge(dfNoUcn, df4gEr, left_on="index", right_on="BS_name", how="inner")
            dfNeighbour = dfNoUcn.merge(dfDaily, how="cross")'''
            dfNeighbour, dfNoUcn, df4gErBulNeop, dfDaily, strNoUcn, str4gErBul = funcJoin3df(
                pd.DataFrame(), dfNoUcn, df4gErBulNeop, dfDaily,
                "index", "BS_name"
            )
            dfNoUcn = funcFindNeighbour(dfNeighbour)

            #dfNoUcn = dfNoUcn.reindex(columns=["Reg", "site", "LAC", "Sector"])
            dfNoUcn = funcCorrectCols4gEr(dfNoUcn)
            dfNew = pd.concat([dfNew, dfNoUcn])
        # print(dfNoUcn)

        dfUcn = pd.DataFrame()
        dfUcn = pd.concat([dfRdb, dfUcn])
        dfUcn = dfUcn[dfUcn["UCN"].isin(["УЦН"])]
        if checkTable(dfUcn) == False:
            # print(dfUcn)
            dfUcn, df4gErBulNeop, dfUcnTemplate, strUcn1, strUcn2, str4gErBul, strUcnTemplate = funcJoin2Df2(
                dfUcn, df4gErBulNeop, dfUcnTemplate,
                "index","RegUcn","BS_name","RegUcn"
            )

            dfNoUcn = funcCorrectCols4gEr(dfNoUcn)
            dfNew = pd.concat([dfNew, dfUcn])
        # print(dfUcn)
    #print(dfNew)

    dfOld = funcCorrectCols4gEr(dfOld)
    #print(dfOld)

    df4gErBulNeop, dfOld, dfNew = funcJoin2Df(pd.DataFrame(), dfOld, dfNew)
    print("Data ready (df4gErBulNeop)")
    print(df4gErBulNeop)

    df4gErBulNeop.to_csv("df4gErBulNeop.csv", sep=",", index=False, header=False, encoding="UTF-8-SIG")

    listFiles = os.listdir()
    # print(listFiles)
    for file in listFiles:
        if "df4gErBulNeop." in file:
            #print(file)
            dataFromSite = funcPowerDrivaer(
                driver_path=CONFIG_DATA.get("LINKPO1"),
                binary_path=CONFIG_DATA.get("LINKPO2"),
                url=CONFIG_DATA.get("LINKSITE3"),
                action_func=funcParsingCes,
                filterObjectSite=CONFIG_DATA.get("TEGSSITE4")
            )
            # print(dataFromSite)
            print("+ Add Data (df4gErBulNeop) to site CES")

if (checkTable(df2gNok) == True) and (checkTable(df2gNokBul) == True) and (checkTable(df3gNok) == True) and (checkTable(df4gNok) == True )and (checkTable(df4gNokBul) == True) and (checkTable(df2gEr) == True) and (checkTable(df2gErBul) == True) and (checkTable(df2gErBulNeop) == True) and (checkTable(df3gEr) == True) and (checkTable(df4gEr) == True) and (checkTable(df4gErBul) == True) and (checkTable(df4gErBulNeop) == True):
    print("All data on the CES website is filled in.")
