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

def MakeratingsInteger(arr):
    for i in range(0,len(arr[0])):
        arr[6][i] = arr[6][i] * 10
    return arr
    
def MakeratingsFloat(arr):
    for i in range(0,len(arr[0])):
        arr[6][i] = int(arr[6][i]) / 10
    return arr
#    -------------For Ascending---------------------

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



def storeCompleteObject(arr,rowNumber,i,idx,sortedarraywithZeros):
    lis = []
    for k in range(7):
        lis.append(arr[k][i])
    sortedarraywithZeros[int(idx)].append(lis)
    return sortedarraywithZeros
    

def PigeonHoleSort_asc(arr,rowNumber):
    if(rowNumber == 6):
        arr = MakeratingsInteger(arr)
    maximum = max(arr[rowNumber])
    minimum = min(arr[rowNumber])
    Range = maximum - minimum + 1
    
    sortedarraywithZeros = [[] for i in range(int(Range))]
    sortedarray = []

    
    for i in range(0,len(arr[rowNumber])):
        idx = arr[rowNumber][i] - minimum
        sortedarraywithZeros = storeCompleteObject(arr,rowNumber,i,idx,sortedarraywithZeros)
    
    sortedarray = [i for i in sortedarraywithZeros if len(i) > 0]
    sortedarray = makeASingleList_asc(sortedarray)
    sortedarray = exchangeRowsandColumns(sortedarray)
    if(rowNumber == 6):
        sortedarray = MakeratingsFloat(sortedarray)
    return sortedarray




#--------------------for Descending----------------------
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

def PigeonHoleSort_desc(arr,rowNumber):
    if(rowNumber == 6):
        arr = MakeratingsInteger(arr)
    maximum = max(arr[rowNumber])
    minimum = min(arr[rowNumber])
    Range = maximum - minimum + 1
    
    sortedarraywithZeros = [[] for i in range(int(Range))]
    sortedarray = []

    
    for i in range(0,len(arr[rowNumber])):
        idx = arr[rowNumber][i] - minimum
        sortedarraywithZeros = storeCompleteObject(arr,rowNumber,i,idx,sortedarraywithZeros)
    
    sortedarray = [i for i in sortedarraywithZeros if len(i) > 0]
    sortedarray = makeASingleList_desc(sortedarray)
    sortedarray = exchangeRowsandColumns(sortedarray)
    if(rowNumber == 6):
        sortedarray = MakeratingsFloat(sortedarray)
    return sortedarray
  