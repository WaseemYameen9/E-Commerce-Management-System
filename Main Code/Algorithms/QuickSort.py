
def exchangeColumns(a, b,mainList):
    for i in range(0,7):
        c = mainList[i][a]
        mainList[i][a] = mainList[i][b]
        mainList[i][b] = c
    
#  ------------For Ascending--------------

def Sort_asc(subArray,left,right,mainList):
    pivot = subArray[right]
    i = left - 1
    
    for k in range(left,right):
        if(subArray[k] <= pivot):
            i = i + 1
            exchangeColumns(k, i, mainList)
           
    
    exchangeColumns(right, i+1, mainList)
              
    return i+1



def QuickSort_asc(array,rowNumber,left,right,mainList):
    if(left<right):
        pivot = Sort_asc(array,left,right,mainList)
        QuickSort_asc(array, rowNumber,left, pivot-1,mainList)
        QuickSort_asc(array, rowNumber,pivot+1, right,mainList)
        
        

def getsorted2DarraybyQuickSort_asc(mainList,rowNumber):
    QuickSort_asc(mainList[rowNumber], rowNumber, 0, len(mainList[0])-1,mainList)
    return mainList


#  ------------For Descending--------------


def Sort_desc(subArray,left,right,mainList):
    pivot = subArray[right]
    i = left - 1
    
    for k in range(left,right):
        if(subArray[k] >= pivot):
            i = i + 1
            exchangeColumns(k, i, mainList)
           
    
    exchangeColumns(right, i+1, mainList)
              
    return i+1



def QuickSort_desc(array,rowNumber,left,right,mainList):
    if(left<right):
        pivot = Sort_desc(array,left,right,mainList)
        QuickSort_desc(array, rowNumber,left, pivot-1,mainList)
        QuickSort_desc(array, rowNumber,pivot+1, right,mainList)
        
        

def getsorted2DarraybyQuickSort_desc(mainList,rowNumber):
    QuickSort_desc(mainList[rowNumber], rowNumber, 0, len(mainList[0])-1,mainList)
    return mainList

