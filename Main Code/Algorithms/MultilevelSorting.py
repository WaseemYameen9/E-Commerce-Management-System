#_________________________________ Multi Lvl Logic _________________________________________
def multiLevelComparison(firstElementDetails,secondElementDetails,comparisonOrderList,comparisonRowNo):
    if(len(comparisonOrderList)==comparisonRowNo):
        # check last condition and not further call of multiLvl and finalize the answer
        if(firstElementDetails[comparisonOrderList[comparisonRowNo-1]]==secondElementDetails[comparisonOrderList[comparisonRowNo-1]]):
            return 0
        elif(firstElementDetails[comparisonOrderList[comparisonRowNo-1]] > secondElementDetails[comparisonOrderList[comparisonRowNo-1]]):
            return 1
        else:
            return 2
    else:# check Current condition and and if same them move to next comparisonNo by calling MultiLvl sorting
        if(firstElementDetails[comparisonOrderList[comparisonRowNo]]==secondElementDetails[comparisonOrderList[comparisonRowNo]]):
            return multiLevelComparison(firstElementDetails,secondElementDetails,comparisonOrderList,comparisonRowNo+1)
        elif(firstElementDetails[comparisonOrderList[comparisonRowNo]] > secondElementDetails[comparisonOrderList[comparisonRowNo]]):
            return 1
        else:
            return 2
def MultiLvlComparisonBool(key, comapare,TrueOnList,orderList,orderNo):
    # pass the both object and trueOnList on which comaprison Value (0,1,2) it give back the true otherwise False 
    comparisonValue=multiLevelComparison(key,comapare,orderList,orderNo)
    for i in TrueOnList:
        if(comparisonValue==i):
            return True
    return False
def exchangeColumns(array, a, b, rowNumber):
    for i in range(len(array)):
        array[i][a],array[i][b] = array[i][b],array[i][a]
    return array


def exchangeObject(array, columnNo, key):
    for i in range(len(key)):
        array[i][columnNo] = key[i]


def getColumnFrom2D(arr_2, columnNo):
    return [arr_2[x][columnNo] for x in range(len(arr_2))]
#________________________________     Insertion ____________________________________________
#--------------------------------    For Ascending ----------------------------------------------
def InsertionSort_MultiLvlAsc(array_2, rowNumber,orderList):
    for i in range(1, len(array_2[rowNumber])):
        key = getColumnFrom2D(array_2, i)
        j = i - 1
        # while(j >= 0 and key[rowNumber] <= array_2[rowNumber][j]):
        # [0,1] ======> compareElement is equal to the key or greater 
        while(j >= 0 and MultiLvlComparisonBool(key,getColumnFrom2D(array_2,j),[0,2],orderList,0)):

            # array_2[j + 1] = array_2[j]
            array_2 = exchangeColumns(array_2, j+1, j, rowNumber)
            j = j - 1

        # array_2[j + 1] = key
        exchangeObject(array_2, j+1, key)

    return array_2
#--------------------------------    For Descending ----------------------------------------------
def InsertionSort_MultiLvlDesc(array_2, rowNumber,orderList):
    for i in range(1, len(array_2[rowNumber])):
        key = getColumnFrom2D(array_2, i)
        j = i - 1
        # while(j >= 0 and key[rowNumber] >= array_2[rowNumber][j]):
        # [0,1] ======> key is equal to the compareElement or greater 
        while(j >= 0 and MultiLvlComparisonBool(key,getColumnFrom2D(array_2,j),[0,1],orderList,0)):

            # array_2[j + 1] = array_2[j]
            array_2 = exchangeColumns(array_2, j+1, j, rowNumber)
            j = j - 1

        # array_2[j + 1] = key
        exchangeObject(array_2, j+1, key)

    return array_2
#________________________________      Selection   ______________________________________________
#--------------------------------    For Ascending ----------------------------------------------

def minimum(array , start, rowNumber,orderList):
    # minimumNumber = array[rowNumber][start]
    minimumCol=getColumnFrom2D(array,start)
    minimumIndex = start
    for i in range(start+1 , len(array[rowNumber])):
        # if(minimumNumber > array[rowNumber][i]):
        if(MultiLvlComparisonBool(minimumCol,getColumnFrom2D(array,i),[1],orderList,0)):
            # minimumNumber = array[rowNumber][i]
            minimumCol=getColumnFrom2D(array,i)
            minimumIndex = i
    return minimumIndex    



def SelectionSort_MultiLvlAsc(array , rowNumber,orderList):
    for i in range (0,len(array[rowNumber])):
        # print('D')
        minIndex = minimum(array, i,rowNumber,orderList)
        array = exchangeColumns(array, minIndex, i, rowNumber)
    return array
#--------------------------------    For Descendng ----------------------------------------------

def maximum(array , start, rowNumber,orderList):
    minimumCol=getColumnFrom2D(array,start)
    maximumIndex = start
    for i in range(start , len(array[rowNumber])):
        # if(minimumNumber < array[rowNumber][i]):
        if(MultiLvlComparisonBool(minimumCol,getColumnFrom2D(array,i),[2],orderList,0)):
            # minimumNumber = array[rowNumber][i]
            minimumCol=getColumnFrom2D(array,i)
            maximumIndex = i
    return maximumIndex    

def SelectionSort_MultiLvlDesc(array , rowNumber,orderList):
    for i in range (0,len(array[rowNumber])):
        maxIndex = maximum(array, i,rowNumber,orderList)
        array = exchangeColumns(array, maxIndex, i, rowNumber)
    return array
#________________________________      Bubble   ______________________________________________
#--------------------------------    Ascending  ----------------------------------------------
def BubbleSort_MultiLvlAsc(array,rowNumber,orderList):
    for i in range(0,len(array[rowNumber])):
        for j in range(len(array[rowNumber])-1,0,-1):
            key=getColumnFrom2D(array,j)
            comapare=getColumnFrom2D(array,j - 1)
            # if(array[rowNumber][j] < array[rowNumber][j - 1]):
            if(MultiLvlComparisonBool(key,comapare,[2],orderList,0)):
                # temp = array[j]
                # array[j] = array[j-1]
                # array[j-1] = temp
                array = exchangeColumns(array, j, j-1, rowNumber)
    return array
#--------------------------------    Descending  ----------------------------------------------
def BubbleSort_MultiLvlDesc(array,rowNumber,orderList):
    for i in range(0,len(array[rowNumber])):
        for j in range(len(array[rowNumber])-1,0,-1):
            key=getColumnFrom2D(array,j)
            comapare=getColumnFrom2D(array,j - 1)
            # if(array[rowNumber][j] < array[rowNumber][j - 1]):
            if(MultiLvlComparisonBool(key,comapare,[1],orderList,0)):
                # temp = array[j]
                # array[j] = array[j-1]
                # array[j-1] = temp
                array = exchangeColumns(array, j, j-1, rowNumber)
    return array

