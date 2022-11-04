
# -----------------Helping Functions---------------
def exchangeRowsandColumns(List):
    array = [[0 for i in range(len(List))] for j in range(7)]
    for i in range(0, len(List)):
        array[0][i] = List[i][0]
        array[1][i] = List[i][1]
        array[2][i] = List[i][2]
        array[3][i] = List[i][3]
        array[4][i] = List[i][4]
        array[5][i] = List[i][5]
        array[6][i] = List[i][6]
    return array

def exchangeRowsandColumns_2(List,i):
    array = []
    array.append(List[0][i])
    array.append(List[1][i])
    array.append(List[2][i])
    array.append(List[3][i])
    array.append(List[4][i])
    array.append(List[5][i])
    array.append(List[6][i])
    return array


def DivideElementsByMaximum(array,maximum):
    for i in range(0,len(array)):
        array[i] = array[i] / maximum
    
    return array


def getObject(array,j):
    lis = []
    for l in range(7):
        lis.append(array[l][j])
    
    return lis
    
#   ---------Bucket Sort Ascending Main Function----------

def Bucketsort_asc(array,rowNumber):
    Buckets = []
    sortedarray = []
    n = 10
    for i in range(0,10):
        lis = []
        Buckets.append(lis)

    maximum = max(array[rowNumber]) + 1
    
    subarray = DivideElementsByMaximum(array[rowNumber],maximum)
    
    for j in range(0,len(array[rowNumber])):

        bucketnumber = int(n * subarray[j])
        array[rowNumber][j] = (array[rowNumber][j] * maximum)
        lis = getObject(array,j)
        Buckets[bucketnumber].append(lis)

    for k in range(0,len(Buckets)):
        L = Buckets[k]
        L = exchangeRowsandColumns(L)
        L = InsertionSort_asc(L,rowNumber)
        
        for m in range(0,len(L[0])):
            oneObject = exchangeRowsandColumns_2(L,m)
            sortedarray.append(oneObject)

    sortedarray = exchangeRowsandColumns(sortedarray)
    return sortedarray


#               ---------InsertionSort-------------
def InsertionSort_asc(array_2, rowNumber):
    for i in range(1, len(array_2[rowNumber])):

        key = getColumnFrom2D(array_2, i)
        j = i - 1
        while(j >= 0 and key[rowNumber] <= array_2[rowNumber][j]):
            array_2 = exchangeColumns(array_2, j+1, j, rowNumber)
            j = j - 1
        exchangeObject(array_2, j+1, key)

    return array_2


def getColumnFrom2D(arr_2, columnNo):
    arr = []
    for i in range(len(arr_2)):
        arr.append(arr_2[i][columnNo])
    return arr

def exchangeObject(array, columnNo, key):
    for i in range(len(key)):
        array[i][columnNo] = key[i]

def exchangeColumns(array, a, b, rowNumber):
    for i in range(len(array)):
        array[i][a] = array[i][b]
    return array



#---------------Bucket Sort Descending main Function--------------

def Bucketsort_desc(array,rowNumber):
    Buckets = []
    sortedarray = []
    n = 10
    for i in range(0,10):
        lis = []
        Buckets.append(lis)

    maximum = max(array[rowNumber]) + 1
    
    subarray = DivideElementsByMaximum(array[rowNumber],maximum)
    
    for j in range(0,len(array[rowNumber])):

        bucketnumber = int(n * subarray[j])
        array[rowNumber][j] = (array[rowNumber][j] * maximum)
        lis = getObject(array,j)
        Buckets[bucketnumber].append(lis)

    for k in range(len(Buckets)-1,-1,-1):
        L = Buckets[k]
        L = exchangeRowsandColumns(L)
        L = InsertionSort_asc(L,rowNumber)
        
        for m in range(len(L[0])-1,-1,-1):
            oneObject = exchangeRowsandColumns_2(L,m)
            sortedarray.append(oneObject)

    sortedarray = exchangeRowsandColumns(sortedarray)
    return sortedarray