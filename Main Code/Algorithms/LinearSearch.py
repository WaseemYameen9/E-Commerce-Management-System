
def exchangeRowsandColumns(List):
    array = [[0 for i in range(len(List))] for j in range(7)]
    for i in range(0,len(List)):
        array[0][i] = List[i][0]
        array[1][i] = List[i][1]
        array[2][i] = List[i][2]
        array[3][i] = List[i][3]
        array[4][i] = List[i][4]
        array[5][i] = List[i][5]
        array[6][i] = List[i][6]
    return array
        


def Search(source,key,rowNumber):
    if(rowNumber == 0 or rowNumber == 1):   
        if key in source:
            return True
    else:
        if(source == key):            
            return True
            
            


def LinearSearch(data,rowNumber,key):
    dataColumnList = []
    searchedData = []
    for i in range(0,len(data[0])):
        if(Search(data[rowNumber][i],key,rowNumber)):
            dataColumnList.append(i)


    for k in range(0,len(dataColumnList)):
        lis = []
        for s in range(0,7):
            lis.append(data[s][dataColumnList[k]])
        
        searchedData.append(lis)
    Data = exchangeRowsandColumns(searchedData)
    return Data

#        ------Searching With Filters-------------


def wordStartWith(firstLetter, comparisonLetter):
    firstLetter = list(firstLetter)
    comparisonLetter = list(comparisonLetter)
    for i in range(len(comparisonLetter)):
        if (comparisonLetter[i] != firstLetter[i]):
            return False
    return True
def wordExactEquals(firstLetter,comparisonLetter):
    if firstLetter == comparisonLetter:
        return True
    else:
        return False
def wordEndWith(firstLetter, comparisonLetter):
    firstLetter = list(firstLetter)
    comparisonLetter = list(comparisonLetter)
    firstLetter = firstLetter[::-1]
    comparisonLetter = comparisonLetter[::-1]
    for i in range(len(comparisonLetter)):
        if (comparisonLetter[i] != firstLetter[i]):
            return False
    return True
def wordContains(firstLetter, comparisonLetter):
    if comparisonLetter in firstLetter:
        return True
    return False





def compareBySwitchingCondition(firstLetter,comparisonLetter,switchingNo):
    if(switchingNo == 0): # start With
        return wordStartWith(firstLetter,comparisonLetter)
    if(switchingNo == 1): # End With
        return wordEndWith(firstLetter,comparisonLetter)
    if(switchingNo == 2): # Contains With
        return wordContains(firstLetter,comparisonLetter)
    if(switchingNo == 3): # Exact With
        return wordExactEquals(firstLetter,comparisonLetter)
    return False
   
            
            


def LinearSearch_Filter(data,rowNumber,comparisonLetter,switchingNo):
    comparisonLetter = str(comparisonLetter)
    dataColumnList = []
    searchedData = []
    for i in range(0,len(data[0])):
        if(compareBySwitchingCondition(str(data[rowNumber][i]),comparisonLetter,switchingNo)):
            dataColumnList.append(i)


    for k in range(0,len(dataColumnList)):
        lis = []
        for s in range(0,7):
            lis.append(data[s][dataColumnList[k]])
        
        searchedData.append(lis)
    Data = exchangeRowsandColumns(searchedData)
    return Data,dataColumnList
        
        