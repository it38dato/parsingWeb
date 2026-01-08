import pandas as pd
import mysql.connector
import os
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
        else:
            with open("output.log", "w") as outfile:
                outfile.write("- Не найден файл config.txt\n")
    return ipN, ipE, userC, passwdC, userD, passwdD, db1, db2, db3
def unloadCes2gNok(table):
    listdbs = []
    listRow = []
    try: 
        mydb = mysql.connector.connect(
            host=ipNokia,
            user=userDb,
            password=passwdDb,
        )
    except mysql.connector.errors.ProgrammingError:
        with open("output.log", "a") as outfile:
            outfile.write("- Error connecting to MYSQL Platform:\n")
    mycursor = mydb.cursor()
    with open("output.log", "a") as outfile:
        outfile.write("+ Connected to the database\n")
    querrydbs = ("SHOW DATABASES")        
    mycursor.execute(querrydbs)
    for querrydbs in mycursor:
        listdbs.append(querrydbs[0])
    for db in listdbs:
        if dbCes == db:
            try:
                querry = "SELECT Reg, BS_name, CELL, SW, BSC, BCF, LAC, RAC FROM CreateSite.table_nokia_2g_v WHERE BSS='OK' AND Reg IN ('IR','SA','MD','KM','HB','BI','ANi','YA')"
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
    table = pd.DataFrame(listRow, columns =['Reg', 'BS_name', 'Sector', 'SW', 'BSC', 'BCF', 'LAC', 'RAC'])
    table.to_excel("back2gNok.xlsx") 
    with open("output.log", "a") as outfile:
        outfile.write("+ added table from the DB Createsite\n")
    mycursor.close()
    mydb.close()
    return table
def unloadCes3gNok(table):
    listdbs = []
    listRow = []
    try: 
        mydb = mysql.connector.connect(
            host=ipNokia,
            user=userDb,
            password=passwdDb,
        )
    except mysql.connector.errors.ProgrammingError:
        with open("output.log", "a") as outfile:
            outfile.write("- Error connecting to MYSQL Platform:\n")
    mycursor = mydb.cursor()
    with open("output.log", "a") as outfile:
        outfile.write("+ Connected to the database\n")
    querrydbs = ("SHOW DATABASES")        
    mycursor.execute(querrydbs)
    for querrydbs in mycursor:
        listdbs.append(querrydbs[0])
    for db in listdbs:
        if dbCes == db and dbCes in listdbs and dbCoords in listdbs:
            try:
                querry = "SELECT Reg, BS_name_RDB, Sector_name, LAC, RAC, URA, RNC_ID FROM CreateSite.table_nokia_3g_v WHERE BSS='OK' AND Reg IN ('IR','SA','MD','KM','HB','BI','AiN','YA')"
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
    table = pd.DataFrame(listRow, columns =['Reg', 'BS_name', 'Sector', 'LAC', 'RAC', 'URA', 'RNC_ID'])
    table.to_excel("back3gNok.xlsx") 
    with open("output.log", "a") as outfile:
        outfile.write("+ added table from the DB Createsite\n")
    mycursor.close()
    mydb.close()
    return table
def unloadCes4gNok(table):
    listdbs = []
    listRow = []
    try: 
        mydb = mysql.connector.connect(
            host=ipNokia,
            user=userDb,
            password=passwdDb,
        )
    except mysql.connector.errors.ProgrammingError:
        with open("output.log", "a") as outfile:
            outfile.write("- Error connecting to MYSQL Platform:\n")
    mycursor = mydb.cursor()
    with open("output.log", "a") as outfile:
        outfile.write("+ Connected to the database\n")
    querrydbs = ("SHOW DATABASES")        
    mycursor.execute(querrydbs)
    for querrydbs in mycursor:
        listdbs.append(querrydbs[0])
    for db in listdbs:
        if dbCes == db and dbCes in listdbs and dbCoords in listdbs:
            try:
                querry = "SELECT Reg, BS_name, Sector_name, TAC FROM CreateSite.table_nokia_4g_v WHERE BSS='OK' AND Reg IN ('IR','SA','MD','KM','HB','BI','AiN','YA') "
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
    table = pd.DataFrame(listRow, columns =['Reg', 'BS_name', 'Sector', 'LAC'])
    table.to_excel("back4gNok.xlsx")     
    with open("output.log", "a") as outfile:
        outfile.write("+ added table from the DB Createsite\n")
    mycursor.close()
    mydb.close()
    return table
def unloadCes2gEr(table):
    listdbs = []
    listRow = []
    try: 
        mydb = mysql.connector.connect(
            host=ipEricsson,
            user=userDb,
            password=passwdDb,
        )
    except mysql.connector.errors.ProgrammingError:
        with open("output.log", "a") as outfile:
            outfile.write("- Error connecting to MYSQL Platform:\n")
    mycursor = mydb.cursor()
    with open("output.log", "a") as outfile:
        outfile.write("+ Connected to the database\n")
    querrydbs = ("SHOW DATABASES")        
    mycursor.execute(querrydbs)
    for querrydbs in mycursor:
        listdbs.append(querrydbs[0])
    for db in listdbs:
        if dbCes == db:
            try:
                querry = "SELECT Reg, BS_name, BSC, TG, CELL, RSITE, SW, LAC, RBL2_1, RBL2_2, OETM_1, OETM_2 FROM CreateSite.table_ericsson_2g_v WHERE BSS='OK' AND Reg IN ('BU','VV','ZB','AM')"
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
    table = pd.DataFrame(listRow, columns =['Reg', 'BS_name', 'BSC', 'TG', 'Sector', 'RSITE', 'SW', 'LAC', 'RBL2_1', 'RBL2_2', 'OETM_1', 'OETM_2'])
    table.to_excel("back2gEr.xlsx") 
    with open("output.log", "a") as outfile:
        outfile.write("+ added table from the DB Createsite\n")
    mycursor.close()
    mydb.close()
    return table
def unloadCes3gEr(table):
    listdbs = []
    listRow = []
    try: 
        mydb = mysql.connector.connect(
            host=ipEricsson,
            user=userDb,
            password=passwdDb,
        )
    except mysql.connector.errors.ProgrammingError:
        with open("output.log", "a") as outfile:
            outfile.write("- Error connecting to MYSQL Platform:\n")
    mycursor = mydb.cursor()
    with open("output.log", "a") as outfile:
        outfile.write("+ Connected to the database\n")
    querrydbs = ("SHOW DATABASES")        
    mycursor.execute(querrydbs)
    for querrydbs in mycursor:
        listdbs.append(querrydbs[0])
    for db in listdbs:
        if dbCes == db:
            try:
                querry = "SELECT Reg, System_module_name_3G, RNC_ID, URA, LAC, RAC, Sector_Name, RRU_Power FROM CreateSite.table_ericsson_3g_v WHERE BSS='OK' AND Reg IN ('BU','VV','ZB','AM')"
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
    table = pd.DataFrame(listRow, columns =['Reg', 'BS_name', 'RNC_ID', 'URA', 'LAC', 'RAC', 'Sector', 'RRU_Power'])
    table.to_excel("back3gEr.xlsx") 
    with open("output.log", "a") as outfile:
        outfile.write("+ added table from the DB Createsite\n")
    mycursor.close()
    mydb.close()
    return table
def unloadCes4gEr(table):
    listdbs = []
    listRow = []
    try: 
        mydb = mysql.connector.connect(
            host=ipEricsson,
            user=userDb,
            password=passwdDb,
        )
    except mysql.connector.errors.ProgrammingError:
        with open("output.log", "a") as outfile:
            outfile.write("- Error connecting to MYSQL Platform:\n")
    mycursor = mydb.cursor()
    with open("output.log", "a") as outfile:
        outfile.write("+ Connected to the database\n")
    querrydbs = ("SHOW DATABASES")        
    mycursor.execute(querrydbs)
    for querrydbs in mycursor:
        listdbs.append(querrydbs[0])
    for db in listdbs:
        if dbCes == db:
            try:
                querry = "SELECT Reg, System_module_name_4G, TAC, Sector_name FROM CreateSite.table_ericsson_4g_v WHERE BSS='OK' AND Reg IN ('BU','VV','ZB','AM')"
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
    table = pd.DataFrame(listRow, columns =['Reg', 'BS_name', 'LAC', 'Sector'])
    table.to_excel("back4gEr.xlsx") 
    with open("output.log", "a") as outfile:
        outfile.write("+ added table from the DB Createsite\n")
    mycursor.close()
    mydb.close()
    return table
def checkTable(table):
    return table.empty
def unloadDaily2gNok(table):
    listdbs = []
    listRow = []
    try: 
        mydb = mysql.connector.connect(
            host=ipNokia,
            user=userDb,
            password=passwdDb,
        )
    except mysql.connector.errors.ProgrammingError:
        with open("output.log", "a") as outfile:
            outfile.write("- Error connecting to MYSQL Platform:\n")
    mycursor = mydb.cursor()
    with open("output.log", "a") as outfile:
        outfile.write("+ Connected to the database\n")
    querrydbs = ("SHOW DATABASES")        
    mycursor.execute(querrydbs)
    for querrydbs in mycursor:
        listdbs.append(querrydbs[0])
    for db in listdbs:
        if dbCes == db:
            try:
                querry = "SELECT lac, racode, nwName, int_name FROM Config_all.Config WHERE reg IN ('IR','SA','MD','KM','HB','BI','AiN','YA')"         
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
    #table = pd.DataFrame(listRow, columns =['BS_name', 'BSC', 'BCF', 'LAC', 'RAC'])
    table = pd.DataFrame(listRow, columns =['LAC', 'RAC', 'Sector', 'BSC'])
    with open("output.log", "a") as outfile:
        outfile.write("+ added table from the DB Createsite\n")
    mycursor.close()
    mydb.close()
    return table
def unloadDaily3gNok(table):
    listdbs = []
    listRow = []
    try: 
        mydb = mysql.connector.connect(
            host=ipNokia,
            user=userDb,
            password=passwdDb,
        )
    except mysql.connector.errors.ProgrammingError:
        with open("output.log", "a") as outfile:
            outfile.write("- Error connecting to MYSQL Platform:\n")
    mycursor = mydb.cursor()
    with open("output.log", "a") as outfile:
        outfile.write("+ Connected to the database\n")
    querrydbs = ("SHOW DATABASES")        
    mycursor.execute(querrydbs)
    for querrydbs in mycursor:
        listdbs.append(querrydbs[0])
    for db in listdbs:
        if dbCes == db:
            try:
                #querry = "SELECT SUBSTRING(Sectorname, 1, 6) AS BS_name, lac, rac, uralist, rncid FROM Config_all.config_3g WHERE region IN ('HB','IR')" 
                querry = "SELECT lac, Sectorname, rac, uralist, rncid FROM Config_all.config_3g WHERE region IN ('IR','SA','MD','KM','HB','BI','AiN','YA')"                
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
    table = pd.DataFrame(listRow, columns =['LAC', 'Sector', 'RAC', 'URA', 'RNC_ID'])
    with open("output.log", "a") as outfile:
        outfile.write("+ added table from the DB Createsite\n")
    mycursor.close()
    mydb.close()
    return table
def unloadDaily4gNok(table):
    listdbs = []
    listRow = []
    try: 
        mydb = mysql.connector.connect(
            host=ipNokia,
            user=userDb,
            password=passwdDb,
        )
    except mysql.connector.errors.ProgrammingError:
        with open("output.log", "a") as outfile:
            outfile.write("- Error connecting to MYSQL Platform:\n")
    mycursor = mydb.cursor()
    with open("output.log", "a") as outfile:
        outfile.write("+ Connected to the database\n")
    querrydbs = ("SHOW DATABASES")        
    mycursor.execute(querrydbs)
    for querrydbs in mycursor:
        listdbs.append(querrydbs[0])
    for db in listdbs:
        if dbCes == db:
            try:
                querry = "SELECT Sectorname, tac FROM Config_all.config4g WHERE reg IN ('IR','SA','MD','KM','HB','BI','AiN','YA')" 
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
    table = pd.DataFrame(listRow, columns =['Sector','LAC'])
    with open("output.log", "a") as outfile:
        outfile.write("+ added table from the DB Createsite\n")
    mycursor.close()
    mydb.close()
    return table
def unloadDaily2gEr(table):
    listdbs = []
    listRow = []
    try: 
        mydb = mysql.connector.connect(
            host=ipNokia,
            user=userDb,
            password=passwdDb,
        )
    except mysql.connector.errors.ProgrammingError:
        with open("output.log", "a") as outfile:
            outfile.write("- Error connecting to MYSQL Platform:\n")
    mycursor = mydb.cursor()
    with open("output.log", "a") as outfile:
        outfile.write("+ Connected to the database\n")
    querrydbs = ("SHOW DATABASES")        
    mycursor.execute(querrydbs)
    for querrydbs in mycursor:
        listdbs.append(querrydbs[0])
    for db in listdbs:
        if dbCes == db:
            try:
                querry = "SELECT lac, nwName, int_name FROM Config_all.Config WHERE reg IN ('BU','VV','ZB','AM')"         
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
    table = pd.DataFrame(listRow, columns =['LAC', 'Sector', 'BSC'])
    with open("output.log", "a") as outfile:
        outfile.write("+ added table from the DB Createsite\n")
    mycursor.close()
    mydb.close()
    return table
def unloadDaily3gEr(table):
    listdbs = []
    listRow = []
    try: 
        mydb = mysql.connector.connect(
            host=ipNokia,
            user=userDb,
            password=passwdDb,
        )
    except mysql.connector.errors.ProgrammingError:
        with open("output.log", "a") as outfile:
            outfile.write("- Error connecting to MYSQL Platform:\n")
    mycursor = mydb.cursor()
    with open("output.log", "a") as outfile:
        outfile.write("+ Connected to the database\n")
    querrydbs = ("SHOW DATABASES")        
    mycursor.execute(querrydbs)
    for querrydbs in mycursor:
        listdbs.append(querrydbs[0])
    for db in listdbs:
        if dbCes == db:
            try:
                querry = "SELECT mnc, rncid, lac, Sectorname, rac, uralist FROM Config_all.config_3g WHERE region IN ('BU','VV','ZB','AM')"         
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
    table = pd.DataFrame(listRow, columns =['RRU_Power', 'RNC_ID', 'LAC', 'Sector', 'RAC', 'URA'])
    with open("output.log", "a") as outfile:
        outfile.write("+ added table from the DB Createsite\n")
    mycursor.close()
    mydb.close()
    return table
def unloadDaily4gEr(table):
    listdbs = []
    listRow = []
    try: 
        mydb = mysql.connector.connect(
            host=ipNokia,
            user=userDb,
            password=passwdDb,
        )
    except mysql.connector.errors.ProgrammingError:
        with open("output.log", "a") as outfile:
            outfile.write("- Error connecting to MYSQL Platform:\n")
    mycursor = mydb.cursor()
    with open("output.log", "a") as outfile:
        outfile.write("+ Connected to the database\n")
    querrydbs = ("SHOW DATABASES")        
    mycursor.execute(querrydbs)
    for querrydbs in mycursor:
        listdbs.append(querrydbs[0])
    for db in listdbs:
        if dbCes == db:
            try:
                querry = "SELECT Sectorname, tac FROM Config_all.config4g WHERE reg IN ('BU','VV','ZB','AM')"         
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
    table = pd.DataFrame(listRow, columns =['Sector', 'LAC'])
    with open("output.log", "a") as outfile:
        outfile.write("+ added table from the DB Createsite\n")
    mycursor.close()
    mydb.close()
    return table
def mergeOldBs(table1, table2, table3):
    table1 = pd.merge(table2, table3, left_on='Sector', right_on='Sector', how='inner')
    table1 = table1.drop_duplicates()
    return table1, table2, table3
# Переменные:
ces2gNokTable = pd.DataFrame()
ces3gNokTable = pd.DataFrame()
ces4gNokTable = pd.DataFrame()
ces2gErTable = pd.DataFrame()
ces3gErTable = pd.DataFrame()
ces4gErTable = pd.DataFrame()
daily2gNokTable = pd.DataFrame()
daily3gNokTable = pd.DataFrame()
daily4gNokTable = pd.DataFrame()
daily2gErTable = pd.DataFrame()
daily3gErTable = pd.DataFrame()
daily4gErTable = pd.DataFrame()
oldBsTable = pd.DataFrame()
ipNokia = ""
ipEricsson = ""
userCes = ""
passwdCes = ""
userDb = ""
passwdDb = ""
dbCes = ""
dbConfig = ""
dbCoords = ""
#1
with open("output.log", "w") as outfile:
    outfile.write("+ created Log file output.log\n")
ipNokia, ipEricsson, userCes, passwdCes, userDb, passwdDb, dbCes, dbConfig, dbCoords = hiddenData(ipNokia, ipEricsson, userCes, passwdCes, userDb, passwdDb, dbCes, dbConfig, dbCoords)
#2
#ces2gNokTable = unloadCes2gNok(ces2gNokTable)
#ces3gNokTable = unloadCes3gNok(ces3gNokTable)
ces4gNokTable = unloadCes4gNok(ces4gNokTable)
#ces2gErTable = unloadCes2gEr(ces2gErTable)
#ces3gErTable = unloadCes3gEr(ces3gErTable)
ces4gErTable = unloadCes4gEr(ces4gErTable)
#3
if checkTable(ces2gNokTable) == False:
    res2gNokTable = pd.DataFrame()
    print("таблица (ces2gNokTable) 2G Nokia:")
    print(ces2gNokTable)
    #4
    daily2gNokTable = unloadDaily2gNok(daily2gNokTable)
    #5
    oldBsTable, ces2gNokTable, daily2gNokTable = mergeOldBs(oldBsTable, ces2gNokTable, daily2gNokTable)
    #6 
    #print(oldBsTable.dtypes) 
    oldBsTable["LAC_x"]=oldBsTable["LAC_x"].astype("int64")
    oldBsTable = oldBsTable[oldBsTable['LAC_x'] != oldBsTable['LAC_y']]
    print(oldBsTable)
    #7
    if checkTable(oldBsTable) == False:
        res2gNokTable = oldBsTable.reindex(columns=["Reg", "Sector", "SW", "BSC_y", "BCF", "LAC_y", "RAC_y"])
    print("Заполнена таблица (res2gNokTable) 2G Nokia:")
    print(res2gNokTable)
    res2gNokTable.to_csv("res2gNokTable.csv", sep=',', index=False, header=False, encoding='UTF-8-SIG')
if checkTable(ces3gNokTable) == False:
    res3gNokTable = pd.DataFrame()
    print("таблица (ces3gNokTable) 3G Nokia:")
    print(ces3gNokTable)
    #4
    daily3gNokTable = unloadDaily3gNok(daily3gNokTable)
    #5
    oldBsTable, ces3gNokTable, daily3gNokTable = mergeOldBs(oldBsTable, ces3gNokTable, daily3gNokTable)
    #6 
    oldBsTable["LAC_x"]=oldBsTable["LAC_x"].astype("int64")
    oldBsTable = oldBsTable[oldBsTable['LAC_x'] != oldBsTable['LAC_y']]
    print(oldBsTable)
    #7
    if checkTable(oldBsTable) == False:
        res3gNokTable = oldBsTable.reindex(columns=["Reg", "BS_name", "Sector", "LAC_y", "RAC_y", "URA_y", "RNC_ID_y"])
    print("Заполнена таблица (res3gNokTable) 3G Nokia:")
    print(res3gNokTable)
    res3gNokTable.to_csv("res3gNokTable.csv", sep=',', index=False, header=False, encoding='UTF-8-SIG')
if checkTable(ces4gNokTable) == False:
    res4gNokTable = pd.DataFrame()
    print("таблица (ces4gNokTable) 4G Nokia:")
    print(ces4gNokTable)
    #4
    daily4gNokTable = unloadDaily4gNok(daily4gNokTable)
    #5
    oldBsTable, ces4gNokTable, daily4gNokTable = mergeOldBs(oldBsTable, ces4gNokTable, daily4gNokTable)
    #6 
    oldBsTable["LAC_x"]=oldBsTable["LAC_x"].astype("int64")
    oldBsTable = oldBsTable[oldBsTable['LAC_x'] != oldBsTable['LAC_y']]
    #print(oldBsTable)
    #7
    if checkTable(oldBsTable) == False:
        res4gNokTable = oldBsTable.reindex(columns=["Reg", "BS_name", "Sector", "LAC_y"])        
    print("Заполнена таблица (res4gNokTable) 4G Nokia:")
    print(res4gNokTable)
    res4gNokTable.to_csv("res4gNokTable.csv", sep=',', index=False, header=False, encoding='UTF-8-SIG')
    #8
    daily2gNokTable = unloadDaily2gNok(daily2gNokTable)
    #print("ces4gNokTable:")
    #print(daily2gNokTable)
    daily2gNokTable["Sector"] = daily2gNokTable["Sector"].str[:6]
    daily2gNokTable = daily2gNokTable.drop_duplicates()
    #print("daily2gNokTable:")
    #print(daily2gNokTable)
    lac4g2gTable = pd.merge(ces4gNokTable, daily2gNokTable, left_on='BS_name', right_on='Sector', how='inner')
    #print(lac4g2gTable.dtypes) 
    lac4g2gTable["LAC_x"]=lac4g2gTable["LAC_x"].astype("int64")
    lac4g2gTable = lac4g2gTable[lac4g2gTable['LAC_x'] != lac4g2gTable['LAC_y']]
    #print("lac4g2gTable:")
    #print(lac4g2gTable)
    if checkTable(lac4g2gTable) == False:
        resLac4g2gNokTable = lac4g2gTable.reindex(columns=["Reg", "BS_name", "Sector_x", "LAC_y"])
        print("Подтянул данные Nokia (resLac4g2gNokTable) LAC 4G из 2G:")
        print(resLac4g2gNokTable)
        resLac4g2gNokTable.to_csv("resLac4g2gNokTable.csv", sep=',', index=False, header=False, encoding='UTF-8-SIG')
if checkTable(ces2gErTable) == False:
    res2gErTable = pd.DataFrame()
    print("таблица (ces2gErTable) 2G Ericsson:")
    print(ces2gErTable)
    #4
    daily2gErTable = unloadDaily2gEr(daily2gErTable)
    #print(daily2gErTable)
    #5
    oldBsTable, ces2gErTable, daily2gErTable = mergeOldBs(oldBsTable, ces2gErTable, daily2gErTable)
    #6 
    oldBsTable["LAC_x"]=oldBsTable["LAC_x"].astype("int64")
    oldBsTable = oldBsTable[oldBsTable['LAC_x'] != oldBsTable['LAC_y']]
    print(oldBsTable)
    #7
    if checkTable(oldBsTable) == False:
        res2gErTable = oldBsTable.reindex(columns=["Reg", "BS_name", "BSC_y", "TG", "RSITE", "SW", "LAC_y", "RBL2_1", "RBL2_2", "OETM_1", "OETM_2", "Sector"])        
    print("Заполнена таблица (res2gErTable) 2G Ericsson:")
    print(res2gErTable)
    res2gErTable.to_csv("res2gErTable.csv", sep=',', index=False, header=False, encoding='UTF-8-SIG')
if checkTable(ces3gErTable) == False:
    res3gErTable = pd.DataFrame()
    print("таблица (ces3gErTable) 3G Ericsson:")
    print(ces3gErTable)
    #4
    daily3gErTable = unloadDaily3gEr(daily3gErTable)
    #print(daily3gErTable)
    #5
    oldBsTable, ces3gErTable, daily3gErTable = mergeOldBs(oldBsTable, ces3gErTable, daily3gErTable)
    #print(oldBsTable)
    #6 
    oldBsTable["LAC_x"]=oldBsTable["LAC_x"].astype("int64")
    oldBsTable = oldBsTable[oldBsTable['LAC_x'] != oldBsTable['LAC_y']]
    print(oldBsTable)
    #7
    if checkTable(oldBsTable) == False:
        res3gErTable = oldBsTable.reindex(columns=["Reg", "BS_name", "RNC_ID_y", "URA_y", "LAC_y", "RAC_y", "RRU_Power_y", "Sector"])        
    print("Заполнена таблица (res3gErTable) 3G Ericsson:")
    print(res3gErTable)
    res3gErTable.to_csv("res3gErTable.csv", sep=',', index=False, header=False, encoding='UTF-8-SIG')
if checkTable(ces4gErTable) == False:
    res4gErTable = pd.DataFrame()
    print("таблица (ces4gErTable) 4G Ericsson:")
    print(ces4gErTable)
    #4
    daily4gErTable = unloadDaily4gEr(daily4gErTable)
    #print(daily4gErTable)
    #5
    oldBsTable, ces4gErTable, daily4gErTable = mergeOldBs(oldBsTable, ces4gErTable, daily4gErTable)
    #print(oldBsTable)
    #6 
    oldBsTable["LAC_x"]=oldBsTable["LAC_x"].astype("int64")
    oldBsTable = oldBsTable[oldBsTable['LAC_x'] != oldBsTable['LAC_y']]
    #print(oldBsTable)
    #7
    if checkTable(oldBsTable) == False:
        res4gErTable = oldBsTable.reindex(columns=["Reg", "BS_name", "LAC_y", "Sector"])        
    print("Заполнена таблица (res4gErTable) 4G Ericsson:")
    print(res4gErTable)
    res4gErTable.to_csv("res4gErTable.csv", sep=',', index=False, header=False, encoding='UTF-8-SIG')
    #8
    daily2gErTable = unloadDaily2gEr(daily2gErTable)
    #print("ces4gErTable:")
    #print(ces4gErTable)
    #print("daily2gErTable:")
    #print(daily2gErTable)
    copycol=ces4gErTable["Sector"]
    ces4gErTable.insert(1, "mergeName", copycol)
    ces4gErTable["mergeName"] = ces4gErTable["mergeName"].str[:6]
    #print("ces4gErTable:")
    #print(ces4gErTable)
    daily2gErTable["Sector"] = daily2gErTable["Sector"].str[:6]
    daily2gErTable = daily2gErTable.drop_duplicates()
    #print("daily2gErTable:")
    #print(daily2gErTable)
    lac4g2gTable = pd.merge(ces4gErTable, daily2gErTable, left_on='mergeName', right_on='Sector', how='inner')
    #print("lac4g2gTable:")
    #print(lac4g2gTable)
    #print(lac4g2gTable.dtypes) 
    lac4g2gTable["LAC_x"]=lac4g2gTable["LAC_x"].astype("int64")
    lac4g2gTable = lac4g2gTable[lac4g2gTable['LAC_x'] != lac4g2gTable['LAC_y']]
    #print("lac4g2gTable:")
    #print(lac4g2gTable)
    if checkTable(lac4g2gTable) == False:
        resLac4g2gErTable = lac4g2gTable.reindex(columns=["Reg", "BS_name", "LAC_y", "Sector_x"])
        print("Подтянул данные Ericcson (resLac4g2gErTable) LAC 4G из 2G:")
        print(resLac4g2gErTable)
        resLac4g2gErTable.to_csv("resLac4g2gErTable.csv", sep=',', index=False, header=False, encoding='UTF-8-SIG')