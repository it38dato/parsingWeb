import pandas as pd
import numpy

def checkTable(check):
    return check.empty

def funcImport2listsToDf(listGet1, listGet2, df, dictData, listCols):
    remainder = (len(listGet1)//len(listGet2))
    for numeration in range(len(listGet2)):
            dictData[listGet2[numeration]] = [listGet1[y] for y in range(remainder*numeration,remainder*numeration+remainder)]
    df = pd.DataFrame.from_dict(dictData, orient="index", columns=listCols)
    df = df.reset_index()
    return listGet1, listGet2, df, dictData, listCols
def funcGetSuffRenameColDf(df, fromCol, toCol, fromRenameSymbol, toRenameSymbol, numbCol):
    df.insert(0, toCol, df[fromCol])        
    df[toCol] = df[toCol].str.replace("^"+fromRenameSymbol, toRenameSymbol, regex=True)
    df[toCol] = df[toCol].str[:numbCol]
    return df, fromCol, toCol, fromRenameSymbol, toRenameSymbol, numbCol
def funcFindNeighbour(df):
    x1=df["latitudeX1"].astype(float)
    x2=df["latitudeX2"].astype(float)
    y1=df["longitudeY1"].astype(float)
    y2=df["longitudeY2"].astype(float)        
    df["distance"] = ""
    df["distance"] = numpy.sqrt((x1-x2) * (x1-x2) + (y1-y2) * (y1-y2))
    groupedData = df.groupby("index")
    minDistance = groupedData["distance"].min()
    minDistanceTable = minDistance.reset_index()
    #print(minDistanceTable)
    #print(df)
    df = pd.merge(minDistanceTable, df, left_on="distance", right_on="distance", how="inner")
    #print(df)
    return df

def funcJoin2Df(dfResult, df1, df2):
    if checkTable(df1) == False:
        dfResult = pd.concat([dfResult, df1])
    if checkTable(df2) == False:
        #if checkTable(df1) == False or checkTable(df1) == True:
        dfResult = pd.concat([dfResult, df2])
    return dfResult, df1, df2

def funcGet1DfFrom2Lists(dfResult, df1, df2, listResult, strCol1, strCol2):
    list1 = df1[strCol1].tolist()
    list1 = list(dict.fromkeys(list1))
    list2 = df2[strCol2].tolist()
    list2 = list(dict.fromkeys(list2))
    for name in list1:
        if name in list2:
            continue
        else:
            listResult.append(name)
    #===================================TEST!
    #listResult.append("IO0265")
    #listResult.append("IR0045")
    #===================================TEST!
    dfResult = pd.DataFrame(listResult, columns=["nameNew"])
    return dfResult, df1, df2, listResult, strCol1, strCol2

def funcJoin3df(dfResult, df1, df2, df3, strDf1, strDf2):
    df1 = pd.merge(df1, df2, left_on=strDf1, right_on=strDf2, how="inner")
    dfResult = df1.merge(df3, how="cross")
    return dfResult, df1, df2, df3, strDf1, strDf2

def funcJoin2Df2(dfResult, df1, df2, strResult1, strResult2, strDf1, strDf2):
    dfResult = pd.merge(dfResult, df1, left_on=strResult1, right_on=strDf1, how="inner")
    dfResult = pd.merge(dfResult, df2, left_on=strResult2, right_on=strDf2, how="inner")
    return dfResult, df1, df2, strResult1, strResult2, strDf1, strDf2
