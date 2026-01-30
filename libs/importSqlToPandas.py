import mysql.connector
import pandas as pd

def funcImportSqlToPandas(df, ipDb, userDb, passwdDb, nameDb, nameTable, conditionTable, filterTable):
    listdbs = []
    listRow = []
    #dbCoords = "Physical_param"
    try: 
        mydb = mysql.connector.connect(
            host=ipDb,
            user=userDb,
            password=passwdDb,
        )
    except mysql.connector.errors.ProgrammingError:
        print("- Error connecting to MYSQL Platform")
    mycursor = mydb.cursor()
    querrydbs = ("SHOW DATABASES")        
    mycursor.execute(querrydbs)
    for querrydbs in mycursor:
        listdbs.append(querrydbs[0])
    for db in listdbs:
        #if nameDb == db and nameDb in listdbs and dbCoords in listdbs:
        if nameDb == db and nameDb in listdbs:        
            try:
                querry = f"SELECT {filterTable} FROM {nameDb}.{nameTable} {conditionTable}"  
                print(querry)
                mycursor.execute(querry)
                # Извлекаем названия столбцов из описания курсора
                columns = [col[0] for col in mycursor.description]
                result = mycursor.fetchall()
                for row in result:
                    listRow.append(row)
            except mysql.connector.errors.ProgrammingError:
                continue
            except mysql.connector.errors.DatabaseError:
                continue
        else:
            continue

    #df = pd.DataFrame(listRow)
    df = pd.DataFrame(listRow, columns=columns)
    df = df.drop_duplicates()
    mycursor.close()
    mydb.close()
    return df, ipDb, userDb, passwdDb, nameDb, nameTable, conditionTable, filterTable
