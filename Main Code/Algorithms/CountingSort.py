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


#-----------------------------For Ascending------------------

def makeASingleList_asc(List):
    MList = []
    for k in range(0,len(List)):
        lis = List[k]
        
        for q in range(0,len(lis)):
            subList = []
            subList.append(lis[q][0])
            subList.append(lis[q][1])
            subList.append(lis[q][2])
            subList.append(lis[q][3])
            subList.append(lis[q][4])
            subList.append(lis[q][5])
            subList.append(lis[q][6])
            
            MList.append(subList)
            
    
    return MList


def exchange(arr,indexes,columnNumber,i):
    lis = []
    lis.append(arr[0][i])
    lis.append(arr[1][i])
    lis.append(arr[2][i])
    lis.append(arr[3][i])
    lis.append(arr[4][i])
    lis.append(arr[5][i])
    lis.append(arr[6][i])
    indexes[columnNumber].append(lis)
    return indexes



def countingSort_asc(arr,rowNumber):
    maximum = 100000
    indexes=[[] for i in range(maximum)]
    for i in range(0,len(arr[0])):
        if(rowNumber == 6):
            indexes = exchange(arr, indexes, int(arr[rowNumber][i]*10),i)
        else:
            indexes = exchange(arr, indexes, int(arr[rowNumber][i]),i)
            
        
    indexes = [i for i in indexes if i != []]
    indexes = makeASingleList_asc(indexes)
    indexes = exchangeRowsandColumns(indexes)
    return indexes



#      --------------Descending------------------


def makeASingleList_desc(List):
    MList = []
    for k in range(len(List)-1,-1,-1):
        lis = List[k]
        
        for q in range(0,len(lis)):
            subList = []
            subList.append(lis[q][0])
            subList.append(lis[q][1])
            subList.append(lis[q][2])
            subList.append(lis[q][3])
            subList.append(lis[q][4])
            subList.append(lis[q][5])
            subList.append(lis[q][6])
            
            MList.append(subList)
            
    
    return MList


def countingSort_desc(arr,rowNumber):
    maximum = 100000
    indexes=[[] for i in range(maximum)]
    for i in range(0,len(arr[0])):
        if(rowNumber == 6):
            indexes = exchange(arr, indexes, int(arr[rowNumber][i]*10),i)
        else:
            indexes = exchange(arr, indexes, int(arr[rowNumber][i]),i)
            
        
    indexes = [i for i in indexes if len(i) > 0]
    indexes = makeASingleList_desc(indexes)
    indexes = exchangeRowsandColumns(indexes)
    return indexes
    