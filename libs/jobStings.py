def funcImportStrToList(listContent, symbol, allContent):
    for content in allContent.split(symbol):
        listContent.append(content)
    cout = 0
    for index in listContent:
        #print(str(cout) + " - " + index)
        cout=cout+1

    return listContent, symbol, allContent
def funcDiffStringsAddList(diffString, listAdd, symbol, addSymbol1, addSymbol2):
    if symbol in diffString:
        object = addSymbol1
        listAdd.append(object)
    else:
        object = addSymbol2
        listAdd.append(object)
    return diffString, listAdd, symbol, addSymbol1, addSymbol2