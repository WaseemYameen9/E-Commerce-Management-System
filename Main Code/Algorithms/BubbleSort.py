def exchangeColumns(array, a, b, rowNumber):
    for i in range(0,7):
        c = array[i][a]
        array[i][a] = array[i][b]
        array[i][b] = c
    return array


#------------------------Ascending-------------------------------


def BubbleSort_asc(array,rowNumber):
    for i in range(0,len(array[rowNumber])):
        for j in range(len(array[rowNumber])-1,0,-1):
            if(array[rowNumber][j] < array[rowNumber][j - 1]):
                # temp = array[j]
                # array[j] = array[j-1]
                # array[j-1] = temp
                array = exchangeColumns(array, j, j-1, rowNumber)
    return (array)


#------------------------Descending-------------------------------


def BubbleSort_desc(array,rowNumber):
    for i in range(0,len(array[rowNumber])):
        for j in range(len(array[rowNumber])-1,0,-1):
            if(array[rowNumber][j] > array[rowNumber][j - 1]):
                # temp = array[j]
                # array[j] = array[j-1]
                # array[j-1] = temp
                array = exchangeColumns(array, j, j-1, rowNumber)
    return (array)