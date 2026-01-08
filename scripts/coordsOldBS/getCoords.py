import pandas as pd
import os
import re
import numpy as np
import mysql.connector

listRegCes = ["VV","BU","IO","IR","SA","MD","KM","BI", "AN"] # + NEED UPDATE?
listReg = ["IRK","MGD","SAH","KAM","BRT","VLD"]
oldBsList=[]
oldDataList=[]
dataOldSites = dict()
oldDataTable = pd.DataFrame()
locDir = "unloading/"
netDir = "data/"
netDir = "data/"

#6 Отсортировать файлы, собранные из rdb, в котором есть данные LAC И BSC:
for root, dirs, files in os.walk(netDir):
    lengthDir = len(netDir)
    allDir = root[lengthDir:]
    #print(allDir)

    if ("old" in allDir):
        continue
    elif allDir in listReg:
        #print(allDir)
        for kmlFile in files:
            #print(listRegCes, kmlFile)
            for prefix in listRegCes:
                #print(prefix)
                #if prefixs[0] in kmlFile:
                if prefix in kmlFile:
                    needDir = netDir+allDir+"/"+kmlFile
                    print(needDir)
                    with open(needDir,"r", encoding="utf8") as rdbFile:
                        file = rdbFile.read()
                    #print(file)
                    #7 Добавить данные LAC и BSC в таблицу:
                    Placemark = re.findall(r"<Placemark>(.*?)</Placemark>", file, re.DOTALL)
                    for linePlacemark in Placemark:
                        #print(linePlacemark)
                        if ("<longitude>" in linePlacemark) and ("LAC" in linePlacemark) and ("BSC: " in linePlacemark):
                            #print(linePlacemark)
                            if ("<longitude></longitude>" in linePlacemark) and ("<latitude></latitude>" in linePlacemark):
                                continue
                            else:
                                listBs = re.findall(r"<name>(.*?)</name>", linePlacemark, re.DOTALL)
                                for bs in listBs:
                                    if (len(bs)==6) == True:
                                        #print(bs)
                                        oldBsList.append(bs)
                                    else:
                                        continue
                                listСoords = re.findall(r"<longitude>(.*?)</latitude>", linePlacemark, re.DOTALL)
                                for coords in listСoords:
                                    #print(coords)
                                    coordinates = coords.split("</longitude>\n     <latitude>")
                                    #print(coordinates)
                                    longitude = coordinates[0]
                                    latitude = coordinates[1]
                                    #print(longitude + " " + latitude + "\n")
                                    #with open("output.txt", "a") as outfile:
                                    #    outfile.write(longitude + " " + latitude + "\n")
                                    oldDataList.append(longitude)
                                    oldDataList.append(latitude)
                                listBscTac = re.findall(r"<description>BSC: (.*?)</description>", linePlacemark, re.DOTALL)
                                #print(listBscTac)
                                for bsctac in listBscTac:
                                    #print(bsctac)
                                    data = bsctac.split(" LAC: ")
                                    #print(data)
                                    bsc = data[0]
                                    lac = data[1]
                                    #print(bsc + " " + lac + "\n")
                                    #with open("output.txt", "a") as outfile:
                                    #    outfile.write(bsc + " " + lac + "\n")
                                    oldDataList.append(bsc)
                                    oldDataList.append(lac)
                        elif ("<longitude>" in linePlacemark) and ("LAC" in linePlacemark) and ("URA: " in linePlacemark):
                            #print("ВОЗМОЖНО, эти данные понадобятся для заполнения 3g!")
                            #print(linePlacemark)
                            continue
                        else:
                            continue
print("Список старых базовых станций:")
print(oldBsList)
print("Список координат, LAC И BSC для старых базовых станций:")
print(oldDataList)
remainder = (len(oldDataList)//len(oldBsList))
for numeration in range(len(oldBsList)):
    dataOldSites[oldBsList[numeration]] = [oldDataList[y] for y in range(remainder*numeration,remainder*numeration+remainder)]
print("Список старых базовых станций, их координат, LAC И BSC:")
print(dataOldSites)
cols = ["longitude", "latitude", "BSC", "LAC"]
oldDataTable = pd.DataFrame.from_dict(dataOldSites, orient='index', columns=cols)
oldDataTable = oldDataTable.reset_index()
oldDataTable.to_excel('googleEarthData.xlsx')
