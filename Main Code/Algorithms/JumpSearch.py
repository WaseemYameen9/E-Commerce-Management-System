import math


#      -----Helping Functions of Selection Sort-------

def exchangeColumns(array, a, b, rowNumber):
    for i in range(0,7):
        c = array[i][a]
        array[i][a] = array[i][b]
        array[i][b] = c
    return array


def minimum(array , start, rowNumber):
    minimumNumber = array[rowNumber][start]
    minimumIndex = start
    for i in range(start , len(array[rowNumber])):
        if(minimumNumber > array[rowNumber][i]):
            minimumNumber = array[rowNumber][i]
            minimumIndex = i
    return minimumIndex    



def SelectionSort_asc(array , rowNumber):
    for i in range (0,len(array[rowNumber])):
        minIndex = minimum(array, i,rowNumber)
        array = exchangeColumns(array, minIndex, i, rowNumber)
    return array


#        ------Helping Linear Search Functions-------

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
            




def LinearSearch(data,rowNumber,key,startingidx,end):
    dataColumnList = []
    searchedData = []
    for i in range(startingidx,end):
        if(Search(data[rowNumber][i],key,rowNumber)):
            dataColumnList.append(i)


    for k in range(0,len(dataColumnList)):
        lis = []
        for s in range(0,7):
            lis.append(data[s][dataColumnList[k]])
        
        searchedData.append(lis)
    Data = exchangeRowsandColumns(searchedData)
    return Data
 

#         --------------------------------------------


#         ---------Main Jump Search Function----------
def JumpSearch(arr,rowNumber,key):
    arr = SelectionSort_asc(arr, rowNumber)
    gap = int(math.sqrt(len(arr[rowNumber])))
    for i in range(0,len(arr[rowNumber]),gap):
        if(arr[rowNumber][i] == key and i == 0):
            startingidx = i
            
        elif(arr[rowNumber][i] >= key):
            startingidx = i-gap
            break
       
    
    array = LinearSearch(arr, rowNumber, key, startingidx ,len(arr[rowNumber]))
    return array
        


#-------------------Jump Search With Filters---------------



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
            





def LinearSearch_filter(data,rowNumber,comparisonletter,startingidx,end,switchingNo):
    comparisonletter = str(comparisonletter)
    dataColumnList = []
    searchedData = []
    for i in range(startingidx,end):
        if(compareBySwitchingCondition(str(data[rowNumber][i]),comparisonletter,switchingNo)):
            dataColumnList.append(i)


    for k in range(0,len(dataColumnList)):
        lis = []
        for s in range(0,7):
            lis.append(data[s][dataColumnList[k]])
        
        searchedData.append(lis)
    Data = exchangeRowsandColumns(searchedData)
    return Data,dataColumnList
 

#         --------------------------------------------


#         ---------Main Jump Search Function----------
def JumpSearch_Filter(arr,rowNumber,comparisonletter,switchingNo):
    arr = SelectionSort_asc(arr, rowNumber)
    # gap = int(math.sqrt(len(arr[rowNumber])))
    gap = 3
    for i in range(0,len(arr[rowNumber]),gap):
        if(arr[rowNumber][i] == comparisonletter and i == 0):
            startingidx = i
            
        elif(arr[rowNumber][i] >= comparisonletter):
            startingidx = i-gap
            break
       
    
    array,dataColList = LinearSearch_filter(arr, rowNumber, comparisonletter, startingidx ,len(arr[rowNumber]),switchingNo)
    return array,dataColList
        
        